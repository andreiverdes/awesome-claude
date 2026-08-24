---
name: mosby
description: Use when asked to create a 3D architecture visualization, map, or "city" of a codebase or system — triggers on "arch viz", "architecture city/map", "visualize this project's architecture in 3D", "three.js architecture", "/mosby <path>", or being pointed at a repo and asked to show its components as buildings. Skip for 2D-only diagram requests (mermaid, graphviz, static UML images) and for UI mockups.
---

# Mosby

Turn any codebase into an interactive 3D architecture visualization: a city where buildings are components, roads carry flows, and a toggle flips to a clean UML-style diagram — one self-contained Three.js HTML file, no build step, no network.

You do not build this from scratch. `assets/architecture-city-template.html` is a complete working visualization of a fictional example backend, carrying several sessions of accumulated machinery (routing, flow player, banner system, dual themes, city/diagram modes, performance work, upstream-bug patches). Adaptation beats reinvention every time: the machinery is generic, the content is swappable, and the template's own content is the worked example of every data shape.

## Workflow

1. **Recon the target** (read-only). From code, docs, compose/deploy files, derive: components and their grouping (core vs supporting vs external vs clients vs data), what each does in one line and one paragraph, real end-to-end flows (3–5, as ordered component hops with a plain-language caption per hop), open items / phases if the project tracks them. Verify wiring, not just existence: grep who imports/calls each component — "implemented and tested but called by nothing" is a common and load-bearing finding, and it gets the *built, not wired* treatment in the design language. When docs and code disagree, code wins; surface the drift itself in the system card's open-items list. Everything you present must be true of the code — the visualization is documentation, not decoration.
2. **Author the content model** in the template's exact shapes (nodes, flows, banners, default card). Shapes and field meanings: `references/template-anatomy.md` → "Data shapes".
3. **Map the metaphor** using the table in `references/design-language.md` — which component is the hero building, what sits downtown, what lives across the river, what is a ghost lot. Placement must express the architecture's trust and ownership boundaries.
4. **Adapt the template.** Copy `assets/architecture-city-template.html` to the target project as `ARCHITECTURE-CITY.html` and follow the ordered recipe in `references/template-anatomy.md` → "Adaptation recipe". For non-trivial targets, dispatch ONE implementation agent with everything in a single self-contained prompt: file path, "read the file thoroughly first — all machinery and data are inside it", the content model, the metaphor map, the keep-working list, and the verification loop below. One complete brief has repeatedly outperformed incremental instructions; agents cannot rely on resuming with prior context.
5. **Verify in a real browser** (chrome-devtools MCP or equivalent): open the `file://` URL, screenshot, fix what you can actually see, iterate at least twice. Check every item on the "Delivery bar" list at the end of `references/design-language.md`, in both themes, both modes, at 1600×960 and 1280×800. Close your tabs when done.
6. **Deliver** the single HTML file. If iterating on an existing visualization, back up the last verified state on disk first — mid-edit interruptions with no backup have hurt before.

## Quick reference

| Need | Where |
|---|---|
| File section map + grep anchors | `references/template-anatomy.md` |
| Node/flow/banner data shapes | `references/template-anatomy.md` → Data shapes |
| What to change vs never touch | `references/template-anatomy.md` → Adaptation recipe + Pitfalls |
| Metaphor mapping, color rules, banner anatomy | `references/design-language.md` |
| Done criteria | `references/design-language.md` → Delivery bar |

## Common mistakes

- Building a fresh Three.js scene instead of adapting the template — you lose the flow player, themes, diagram mode, and every patched bug, and land on "cartoonish" defaults the design language exists to prevent.
- Deleting `GATE` because the visual gate is gone — it is routing data. Read the pitfalls table before touching the ground plan.
- Inventing flows or components the code doesn't have. Recon first; every node and caption must be defensible from the source.
- Judging light theme mid-demo (dim is by design), or treating the first-tab-open console error as a real bug — both in the pitfalls table.
- Decorative filler: unlabeled infill buildings, parked cars, ornamental gates. Every structure must be a named, meaningful node.
- Skipping browser verification because "the code looks right". The delivery bar requires screenshots of the real thing.
