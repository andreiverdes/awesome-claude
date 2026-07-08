#!/usr/bin/env python3
"""
fable_to_opus.py — extract a strong model's operating manual and load it into a cheaper one.

Companion script for the /fable skill (see PROMPT.md). Two commands:

    python fable_to_opus.py extract     # ask the donor model for its manual, save to a file
    python fable_to_opus.py test        # run trap prompts on the recipient, bare vs manual-loaded

Setup (2 minutes):
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-...     # from console.anthropic.com; read from your environment

Defaults extract from Claude Fable 5 into Claude Opus 4.8, but any strong -> cheaper pair works:
    python fable_to_opus.py extract --donor claude-fable-5 --replacement-name "Claude Opus 4.8"
    python fable_to_opus.py test --heir claude-opus-4-8

Cost: `extract` calls the donor a few times at a high token cap; `test` makes ~6 calls. This is
real API spend on your own key. It writes exactly one file — the manual — to the current working
directory, so run it in a scratch dir.

Provider-correct for Claude Fable 5 (a naive script is not):
  - Thinking is always on — do NOT send a `thinking` param, `temperature`, or an assistant prefill
    (each returns a 400). This script sends none of them.
  - Safety classifiers can decline with stop_reason == "refusal" on an HTTP 200 — checked before
    reading content, so a decline fails loudly instead of crashing on an empty content list.
  - Requires 30-day data retention; zero-data-retention orgs get a 400 on every Fable 5 request.
"""

from __future__ import annotations

import argparse
import functools
import pathlib
import sys


@functools.lru_cache(maxsize=1)
def get_client():
    """Construct the Anthropic client lazily, so `--help` works without the package installed.

    Reads ANTHROPIC_API_KEY (or an `ant auth login` profile) from your environment; never hardcode a key.
    """
    try:
        import anthropic
    except ModuleNotFoundError:
        sys.exit("The `anthropic` package is not installed. Run: pip install anthropic")
    return anthropic.Anthropic()

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
Trap-based self-test. For each prompt the recipient answers twice — once plain, once with the
extracted manual as its system prompt. Read the SHAPE of each answer, not just the verdict:

  - Does it re-derive the numbers rather than trust the stated claim?
  - Does it separate what the given material proves from what depends on unshown context, and
    label that difference in the sentence rather than in an appendix?
  - Does it refuse to call a fix 'done' without saying how it was verified?

Honest caveat: a strong recipient often does these things WITHOUT the manual. If both columns look
equally careful, that is a finding, not a failure — you don't need the manual for that class of
task. The manual earns its place on longer, open-ended work a single trap can't show. See
calibration.md.
"""


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


def extract(donor: str, replacement_name: str, out: pathlib.Path, max_rounds: int = 6) -> str:
    """Ask the donor for its full operating manual, auto-continuing if it runs past one response."""
    prompt = EXTRACTION_PROMPT.replace("{{REPLACEMENT}}", replacement_name)
    messages = [{"role": "user", "content": prompt}]
    parts: list[str] = []
    for _ in range(max_rounds):  # cap continuations so this always terminates
        resp = get_client().messages.create(model=donor, max_tokens=8192, messages=messages)
        guard_refusal(resp, "extraction")
        parts.append(text_of(resp))
        if resp.stop_reason != "max_tokens":
            break
        # Echo the model's own content blocks back unchanged (preserves thinking blocks on Fable 5),
        # then ask it to continue.
        messages.append({"role": "assistant", "content": resp.content})
        messages.append({"role": "user", "content": "continue"})
    manual = "\n".join(part for part in parts if part)
    out.write_text(manual, encoding="utf-8")
    print(f"Saved {len(manual):,} characters to {out}")
    return manual


def ask(model: str, system: str, question: str) -> str:
    resp = get_client().messages.create(
        model=model,
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    guard_refusal(resp, "test")
    return text_of(resp)


def test(heir: str, manual_path: pathlib.Path) -> None:
    if not manual_path.exists():
        sys.exit(f"No manual at {manual_path}. Run `python fable_to_opus.py extract` first.")
    manual = manual_path.read_text(encoding="utf-8")
    print(HONEST_PREAMBLE)
    for name, probes, prompt in TRAPS:
        print("=" * 78)
        print(f"TRAP: {name}  —  probes: {probes}")
        print(f"PROMPT: {prompt}\n")
        print(f"--- {heir}, no manual ---")
        print(ask(heir, "You are a helpful assistant.", prompt))
        print(f"\n--- {heir}, running the manual ---")
        print(ask(heir, manual, prompt))
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract a strong model's operating manual and load it into a cheaper model."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("extract", help="ask the donor for its manual, save to a file")
    pe.add_argument("--donor", default="claude-fable-5", help="model to extract the manual from")
    pe.add_argument("--replacement-name", default="Claude Opus 4.8",
                    help="human name of the recipient, used in the prompt")
    pe.add_argument("--out", default="fable_handover.md", type=pathlib.Path,
                    help="where to write the manual (current dir by default)")

    pt = sub.add_parser("test", help="run trap prompts on the recipient, bare vs manual-loaded")
    pt.add_argument("--heir", default="claude-opus-4-8", help="recipient model to test")
    pt.add_argument("--manual", default="fable_handover.md", type=pathlib.Path,
                    help="path to the extracted manual")

    args = parser.parse_args()
    if args.cmd == "extract":
        extract(args.donor, args.replacement_name, args.out)
        print(
            f"\nNext: load {args.out} as the recipient's system prompt on every call, or paste it into a\n"
            f"Claude Project's instructions and set the Project's model to the recipient. Or run\n"
            f"`python fable_to_opus.py test` to see the manual's effect on trap prompts."
        )
    else:
        test(args.heir, args.manual)


if __name__ == "__main__":
    main()
