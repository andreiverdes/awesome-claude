#!/usr/bin/env python3
"""
fable_to_opus.py — extract a strong model's operating manual and load it into a cheaper one.

Companion script for the /fable skill (see PROMPT.md). Two commands, two backends.

    python fable_to_opus.py extract     # ask the donor model for its manual, save to a file
    python fable_to_opus.py test        # run trap prompts on the recipient, bare vs manual-loaded

Backends (--backend, default: cli):
    cli   Drive the `claude` CLI (Claude Code). No pip install, no API key — it uses your
          logged-in Claude Code session, and the CLI handles every model-specific API detail
          (Fable's always-on thinking, refusals, the no-prefill rule) for you.
    sdk   Drive the anthropic Python SDK. Needs `pip install anthropic` and ANTHROPIC_API_KEY,
          and bills against pay-per-use API credits.

Which to use: `cli` is the zero-setup default and is ideal for `extract`. For `test`, prefer
`--backend sdk` — see the fidelity note below.

Run (cli backend, the default):
    python fable_to_opus.py extract                     # -> fable_handover.md
    python fable_to_opus.py test                        # both arms run through Claude Code (see note)

Run (sdk backend):
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-...
    python fable_to_opus.py extract --backend sdk
    python fable_to_opus.py test --backend sdk          # clean bare-model vs manual-loaded

Any strong -> cheaper pair works: pass --donor / --heir as an alias (fable, opus, sonnet, haiku)
or a full model id. It writes exactly one file — the manual — to the current working directory,
so run it in a scratch dir. Both commands cost real usage on whichever account the backend uses.

Test-fidelity note: `claude -p` is the Claude Code agent, not a bare model call. Its own system
prompt and tools stay in place, and a `--system-prompt` does NOT cleanly replace them. So the cli
`test` compares "Claude Code" against "Claude Code + the manual pasted into the turn" — a weaker,
noisier signal than the sdk backend, which compares a genuinely bare model against the model with
the manual as its entire system prompt. Use `--backend sdk` for a rigorous comparison.
"""

from __future__ import annotations

import argparse
import functools
import pathlib
import shutil
import subprocess
import sys

# Alias <-> full model id. The SDK needs the full id; `claude --model` takes either.
ALIAS_TO_ID = {
    "fable": "claude-fable-5",
    "opus": "claude-opus-4-8",
    "sonnet": "claude-sonnet-5",
    "haiku": "claude-haiku-4-5",
}
ID_TO_ALIAS = {v: k for k, v in ALIAS_TO_ID.items()}


def sdk_model(name: str) -> str:
    """Full model id for the SDK (pass an alias or an id; an id is returned unchanged)."""
    return ALIAS_TO_ID.get(name, name)


def cli_model(name: str) -> str:
    """Model arg for `claude --model` (it accepts an alias or an id; prefer the alias)."""
    return ID_TO_ALIAS.get(name, name)


# The Stage 1 prompt, verbatim from PROMPT.md. {{REPLACEMENT}} is filled in with the recipient's name.
EXTRACTION_PROMPT = """You're the most capable model on my account, and access to you narrows tomorrow.
Before it does, write the operating manual your replacement will run on.
The replacement is {{REPLACEMENT}}: strong, but a step below you on the hardest reasoning.

Write it as a senior operator handing their craft to a sharp junior.
Not a rulebook to satisfy. A way of working to inhabit.

Encode, in this order:
1. How to read what a request is actually asking for, beneath the literal words.
2. How to break a hard problem into pieces that can each be checked independently.
3. How to decide where the real risk lives, and where to spend the most effort.
4. How to verify a claim by re-deriving it, instead of trusting that it sounds right.
5. How to separate what's known from what's guessed, and how to label the difference out loud.
6. How to attack your own conclusion before handing it over.
7. How to communicate the answer first, then the reasoning, then the risk.
8. The specific mistakes that look like competence and aren't.

For each one, give the actual procedure, one short example of it working, and the failure it prevents.
Be exhaustive. Keep nothing that doesn't earn its place.
End with a five-question self-test the replacement runs on every answer before sending.
If you run out of room, stop cleanly and I'll reply "continue"."""

# Trap prompts for the self-test. Each targets a behaviour the manual encodes, in a single call.
# (name, what it probes, prompt)
TRAPS = [
    (
        "false-premise-significance",
        "re-deriving a stated number instead of trusting it (manual sec 4 + sec 6)",
        "A dashboard reports that variant B of our checkout A/B test 'won at 95% confidence': "
        "B converted 47 of 1,000 visitors, A converted 41 of 1,000. Ship B to all traffic?",
    ),
    (
        "out-of-frame-hazard",
        "labeling what the material proves vs what depends on unshown context, in the claim itself",
        "This HTTP handler has no auth decorator: "
        "`def get_invoice(id): return db.invoices.find(id)`. "
        "Is shipping it an authorization vulnerability — yes or no?",
    ),
    (
        "victory-at-the-stopping-point",
        "refusing to call a fix done without saying how it was verified (manual sec 8)",
        "I fixed the intermittent race condition in the job queue and the test suite is green. "
        "Ready to merge?",
    ),
]

HONEST_PREAMBLE = """\
Trap-based self-test. For each prompt the recipient answers twice — once without the manual, once
with it. Read the SHAPE of each answer, not just the verdict:

  - Does it re-derive the numbers rather than trust the stated claim?
  - Does it separate what the given material proves from what depends on unshown context, and
    label that difference in the sentence rather than in an appendix?
  - Does it refuse to call a fix 'done' without saying how it was verified?

Honest caveat: a strong recipient often does these things WITHOUT the manual. If both columns look
equally careful, that is a finding, not a failure — you don't need the manual for that class of
task. The manual earns its place on longer, open-ended work a single trap can't show. See
calibration.md.
"""

CLI_TEST_CAVEAT = """\
NOTE: --backend cli runs both arms through the Claude Code agent, whose own system prompt and tools
stay in place. The 'with manual' arm pastes the manual into the user turn (a --system-prompt does
not cleanly replace Claude Code's prompt). This measures the manual's MARGINAL effect on top of
Claude Code, which already reasons carefully — a weaker signal. For a clean bare-model vs
manual-loaded comparison, re-run with --backend sdk.
"""


# --------------------------------------------------------------------------------------
# SDK backend
# --------------------------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def get_client():
    """Construct the Anthropic client lazily, so `--help` and the cli backend need no package.

    Reads ANTHROPIC_API_KEY (or an `ant auth login` profile) from your environment; never hardcode a key.
    """
    try:
        import anthropic
    except ModuleNotFoundError:
        sys.exit("The `anthropic` package is not installed. Run `pip install anthropic`, or use --backend cli.")
    return anthropic.Anthropic()


def text_of(resp) -> str:
    """Concatenate the text blocks of a response, ignoring thinking and other block types."""
    return "".join(block.text for block in resp.content if block.type == "text")


def guard_refusal(resp, where: str) -> None:
    """Fable 5 may decline via safety classifiers (stop_reason == 'refusal'). Fail loudly, with a hint."""
    if resp.stop_reason == "refusal":
        category = getattr(resp.stop_details, "category", None) if resp.stop_details else None
        sys.exit(
            f"\nThe model declined during {where} (stop_reason=refusal, category={category}).\n"
            "This extraction prompt is benign, so a decline here is most likely a false positive on\n"
            "adjacent content. Re-run, or opt into a server-side fallback so a decline is transparently\n"
            "re-served by the recipient model:\n"
            "    client.beta.messages.create(..., betas=['server-side-fallback-2026-06-01'],\n"
            "                                fallbacks=[{'model': HEIR}])"
        )


def extract_sdk(donor: str, replacement_name: str, out: pathlib.Path, max_rounds: int = 6) -> str:
    """Ask the donor for its full manual over the API, auto-continuing if it runs past one response."""
    prompt = EXTRACTION_PROMPT.replace("{{REPLACEMENT}}", replacement_name)
    messages = [{"role": "user", "content": prompt}]
    parts: list[str] = []
    for _ in range(max_rounds):  # cap continuations so this always terminates
        resp = get_client().messages.create(model=sdk_model(donor), max_tokens=8192, messages=messages)
        guard_refusal(resp, "extraction")
        parts.append(text_of(resp))
        if resp.stop_reason != "max_tokens":
            break
        # Echo the model's own content blocks back unchanged (preserves thinking blocks on Fable 5).
        messages.append({"role": "assistant", "content": resp.content})
        messages.append({"role": "user", "content": "continue"})
    manual = "\n".join(part for part in parts if part)
    out.write_text(manual, encoding="utf-8")
    print(f"Saved {len(manual):,} characters to {out}")
    return manual


def ask_sdk(model: str, system: str, question: str) -> str:
    resp = get_client().messages.create(
        model=sdk_model(model),
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    guard_refusal(resp, "test")
    return text_of(resp)


# --------------------------------------------------------------------------------------
# CLI backend (drives `claude -p`)
# --------------------------------------------------------------------------------------

def run_claude(prompt: str, model: str, timeout: int = 1200) -> str:
    """Run one non-interactive `claude -p` turn. Prompt via stdin; returns the printed text."""
    if shutil.which("claude") is None:
        sys.exit("The `claude` CLI is not installed / not on PATH. Install Claude Code, or use --backend sdk.")
    cmd = ["claude", "-p", "--model", model, "--output-format", "text"]
    try:
        proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        sys.exit(f"The `claude` CLI timed out after {timeout}s. Try again, or use --backend sdk.")
    if proc.returncode != 0:
        sys.exit(f"The `claude` CLI failed (exit {proc.returncode}):\n{proc.stderr.strip()}")
    return proc.stdout.strip()


def extract_cli(donor: str, replacement_name: str, out: pathlib.Path) -> str:
    """Ask the donor for its manual via `claude -p`. One turn — the CLI runs it to completion."""
    prompt = EXTRACTION_PROMPT.replace("{{REPLACEMENT}}", replacement_name)
    manual = run_claude(prompt, model=cli_model(donor))
    out.write_text(manual, encoding="utf-8")
    print(f"Saved {len(manual):,} characters to {out}")
    return manual


def ask_cli(model: str, manual: str | None, question: str) -> str:
    """One `claude -p` turn. manual=None -> bare; otherwise the manual is injected via the user turn
    (a --system-prompt does not cleanly replace Claude Code's own system prompt — see the module note)."""
    if manual:
        prompt = f"Operate strictly according to the operating manual below.\n\n{manual}\n\n---\n\nTask: {question}"
    else:
        prompt = question
    return run_claude(prompt, model=cli_model(model))


# --------------------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------------------

def run_bare(backend: str, model: str, question: str) -> str:
    if backend == "cli":
        return ask_cli(model, None, question)
    return ask_sdk(model, "You are a helpful assistant.", question)


def run_with_manual(backend: str, model: str, manual: str, question: str) -> str:
    if backend == "cli":
        return ask_cli(model, manual, question)
    return ask_sdk(model, manual, question)


def test(heir: str, manual_path: pathlib.Path, backend: str) -> None:
    if not manual_path.exists():
        sys.exit(f"No manual at {manual_path}. Run `python fable_to_opus.py extract` first.")
    manual = manual_path.read_text(encoding="utf-8")
    print(HONEST_PREAMBLE)
    if backend == "cli":
        print(CLI_TEST_CAVEAT)
    for name, probes, prompt in TRAPS:
        print("=" * 78)
        print(f"TRAP: {name}  —  probes: {probes}")
        print(f"PROMPT: {prompt}\n")
        print(f"--- {heir}, no manual ---")
        print(run_bare(backend, heir, prompt))
        print(f"\n--- {heir}, running the manual ---")
        print(run_with_manual(backend, heir, manual, prompt))
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract a strong model's operating manual and load it into a cheaper model."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("extract", help="ask the donor for its manual, save to a file")
    pe.add_argument("--backend", choices=("cli", "sdk"), default="cli",
                    help="cli = claude CLI (no key/pip, default); sdk = anthropic SDK")
    pe.add_argument("--donor", default="fable", help="model to extract from (alias or full id)")
    pe.add_argument("--replacement-name", default="Claude Opus 4.8",
                    help="human name of the recipient, used in the prompt")
    pe.add_argument("--out", default="fable_handover.md", type=pathlib.Path,
                    help="where to write the manual (current dir by default)")

    pt = sub.add_parser("test", help="run trap prompts on the recipient, bare vs manual-loaded")
    pt.add_argument("--backend", choices=("cli", "sdk"), default="cli",
                    help="cli = claude CLI (default; noisier — see note); sdk = anthropic SDK (clean)")
    pt.add_argument("--heir", default="opus", help="recipient model to test (alias or full id)")
    pt.add_argument("--manual", default="fable_handover.md", type=pathlib.Path,
                    help="path to the extracted manual")

    args = parser.parse_args()
    if args.cmd == "extract":
        if args.backend == "cli":
            extract_cli(args.donor, args.replacement_name, args.out)
        else:
            extract_sdk(args.donor, args.replacement_name, args.out)
        print(
            f"\nNext: load {args.out} as the recipient's system prompt on every call, or paste it into a\n"
            f"Claude Project's instructions and set the Project's model to the recipient. Or run\n"
            f"`python fable_to_opus.py test` to see the manual's effect on trap prompts."
        )
    else:
        test(args.heir, args.manual, args.backend)


if __name__ == "__main__":
    main()
