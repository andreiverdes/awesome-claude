# Template anatomy — architecture-city-template.html

The template (`assets/architecture-city-template.html`, ~3100 lines, ~835 KB) is a complete, working, single-file visualization of a fictional live-video backend ("Acme Live") used as the worked example. Its content doubles as the canonical example of every data shape. Adapting it = replacing the content sections and rebuilding the geometry that is content-specific, while keeping the machinery untouched.

Line numbers drift the moment you edit — navigate by grepping the anchors given below.

## File layout

| Section | Anchor (grep for) | What it is |
|---|---|---|
| CSS + HTML chrome | `<style>`, `id="hint"` | Top stat bar, sidebar chips, tabs, flow controls, caption bar, theme + mode buttons. Title strings are content |
| Three.js r160 UMD | `t.REVISION` (~lines 250–553) | Minified bundle. NEVER edit. |
| Icons | `var ICONS = {` | simple-icons SVG path data (24×24 viewBox), keyed by brand slug. CONTENT |
| Tone colors | `var TONE = {`, `var INK = {` | Six tone families, dark (`TONE`) and light (`INK`) variants. Keep the keys; the meanings can be re-labelled in `LEGEND` |
| Content: floors | `var FLOORS = [` | Hero-tower floor order, bottom → top, by node code. Floor count is derived from this array everywhere |
| Content: stats | `var STATS = [` | The top stat bar entries |
| Content: groups | `var GROUPS = [` | Sidebar sections (key, title, tone) |
| Content: nodes | `var NODES = [` | All components (see shape below) |
| Content: flows | `var FLOWS = [` | End-to-end flows (see shape below) |
| Content: system card | `var DEFAULT_CARD` | The at-rest right-panel card (see shape below) |
| Theme palettes | `var THEME = {` | Dark + light. Every color in the scene lives here, including `dg*` diagram keys |
| Canvas helpers | `function cv(`, `icon(`, `wordmark(`, `fitFont(` | 2D drawing utilities for all baked textures |
| HTML wiring | `function renderCard(`, `pick(`, `setHover(` | Sidebar/card/pin machinery — generic, keep |
| City ground plan | `var LINES = [`, `var GATE = {`, `var LOTS = [` | Road spans, building↔road connection points, painted parcels. CONTENT-SPECIFIC |
| Routing | `function shortest(`, `roadPath(` | Intersection graph + Dijkstra. Generic, keep |
| Ground texture | `function cityTexture(` | One 2048² canvas bakes ALL ground markings, parcels, driveways, and the unbuilt-lot hatch. No lettering here |
| District lettering | `planeTag('` calls (near `streetlights`) | The baked district/approach labels. CONTENT |
| Plates & banners | `var BANNER = {`, `var GOBANNER`, `bannerTexture(` | Per-building banner copy (logo · PURPOSE · subtitle) and card rendering |
| Buildings | `buildWarehouse(`, `buildLot(`, `buildSubstation(`, `buildDatabase(`, `buildStore(`, `buildTower(`, `buildStreamer(`, `buildViewers(` | Geometry vocabulary — reusable builders. The invocation list is content-specific |
| Hero tower | `var TOWER = new T.Group` | The monolith: one floor per `FLOORS` entry, exterior lift, roof, banner |
| Ambience | `streetlights`, `planeTag(` | Lamps, trees, district tags |
| Mode system | `var MODE = 'city'`, `modeRoot(` | city ⇄ diagram toggle wiring. Generic, keep |
| Diagram mode | `var DGPKG = [`, `dgNodeBox(`, `dgEdges(`, `buildDiagram(` | Package layout (`DGPKG`) is content-specific; box/edge/pulse machinery is generic |
| Camera | `var HOMES = {`, `fitHome(`, `flyTo(` | Per-mode home/fit/fly. Generic; fit points partly content-specific |
| Visual state | `setState(`, `refreshStates(` | hot/dim/normal per node, shared by both modes. Keep |
| Flow player | `var FLOWCOLOR`, `var FLOWVEH`, `var VS`, `function veh(`, `runStep(`, `startDemo(` | Vehicles, ribbons, captions, boot demo loop |
| Theme toggle | `function toggleTheme(` | Repaints everything via `userData.regen` + shell-tint passes. Keep; extend only for new material families |

## Data shapes (copy the template's own entries as your example)

**Node** — one per component:
```js
{ code:'LK', name:'LIVEKIT SFU', group:'media', tone:'media',
  pos:[26, 5.0, 5.8],   // REQUIRED for every building node: [x, label-height, z]. Builders read x/z; banner/label height reads y
  one:'rooms/tracks + embedded TURN + data channels',   // sidebar one-liner
  what:'…prose with [[term]] highlights…',              // "what it does" card
  how:'…prose…',                                        // "how it's built" card
  cond:['open item 1', …],                              // optional punch list
  phase:'M0 live', badge:'live',                        // chip annotations (badge: live|planned|ext|app|off|partial|orphaned — free text, styled by class where one exists)
  floor:7,          // ONLY for hero-tower modules (index into FLOORS); floor nodes have no pos
  ghost:true,       // ONLY for planned-but-not-deployed components (renders as unbuilt lot)
  cluster:true,     // ONLY for a node drawn as a group of several objects (template: the viewer phones)
  wordmark:'HIVE' } // ONLY when no icon exists for the brand — used by every plate/banner in place of the icon
```
`group` must match a `GROUPS` key; `tone` one of `control|media|money|mod|data|ext|client`.

**Flow** — one per end-to-end story (3–5; five is the ceiling because `veh()` implements five silhouettes — `taxi` (default), `bus`, `emerg`, `van`, `armor`; a sixth flow needs a sixth silhouette):
```js
{ name:'1 · JOB SESSION END TO END',
  steps:[ {p:['PS','A','SE'], t:'open session — token minted under the job policy'}, … ] }
```
`p` = codes participating in the step (adjacent pairs become vehicle legs / diagram edges), `t` = caption. The FIRST flow is the boot demo. Size `FLOWCOLOR` and `FLOWVEH` to the flow count.

**Banner** — one per building (not per floor): `BANNER['LK'] = {icon:'livekit', purpose:'MEDIA ROUTING', sub:'LiveKit SFU', hh:2.95}`; optional `dx` (sideways nudge when banners project onto each other) and `ghost:1`. The hero uses `GOBANNER` with a bigger `hh`. `icon:null` falls back to the node's `wordmark`.

**Default card** — `{code, name, tone, one, what, how, meta:[[k,v],…], cond:[…], foot}`.

## Icons

`ICONS` holds simple-icons path strings. Zero-network applies at RUNTIME, not while authoring: fetch paths from the `simple-icons` package (npm, or any vendored copy) or its CDN while building, then inline them. If you cannot obtain a path, use `wordmark:` — a clean text mark beats a wrong or invented glyph. Delete unused entries from the template (each is ~1 KB of dead bytes).

## Adaptation recipe (in this order)

1. **Replace content**: `FLOORS`, `STATS`, `GROUPS`, `NODES`, `FLOWS`, `DEFAULT_CARD`, `BANNER`/`GOBANNER`, `ICONS`, `LEGEND` labels, all title/heading strings in the HTML chrome, `<title>`.
2. **Redraw the ground plan**: `LINES` (roads), `GATE` (one entry per building keyed by node code + `TOWER`; despite the name this is routing data — doors to the street), `LOTS` (painted parcels; ghost lots take `empty:1, tone:'<tone>'` and any number of them are hatched), the `planeTag(...)` district lettering.
3. **Re-invoke builders**: keep the builder functions; change the invocation list (`buildWarehouse(BY.X …)` etc.). The hero `TOWER` rebuilds itself from `FLOORS`. Reuse the geometry vocabulary before inventing new builders.
4. **Diagram layout**: rewrite `DGPKG` (package title, grid, member codes, position) to mirror the city's geography. Edges derive automatically from `FLOWS`.
5. **Tune**: `FLOWCOLOR`/`FLOWVEH` to flow count; camera `HOMES`/fit points if the footprint changed; per-node `focusDist` if fly-to crops a banner; `THEME` only if the target wants a different mood (keep both palettes in sync — every key must exist in both).

## Pitfalls (all learned the hard way)

| Pitfall | Reality |
|---|---|
| `GATE` looks like the visual gate | It is traffic routing data (building↔road doors). The visual arch was removed by design. Never delete `GATE`; rename its keys to your node codes. |
| Editing the Three.js bundle | Never. All fixes belong in app code. Two upstream bugs are already patched IN APP CODE: `setTrans()` (material transparent-flag program rebake) and the diagram A* uses `Float64Array` (Float32 rounding broke stale-entry checks). Keep both. |
| Floor count | Roof, lift top, and the hero-banner fit point all derive from `FLOORS.length` — change the array, not the geometry. |
| Light theme "looks broken" during the demo | Off-flow dim (opacity ×0.44) over a pale ground is by design. Judge light theme with the demo cleared (Escape) before "fixing" it. |
| One console error on first tab-open via DevTools MCP | `Unsafe attempt to load URL file://…` is a harness artifact of tab creation. Reload — a healthy file logs zero messages. Any other error is real. |
| Banner/label height changes | `fitHome()` probes label tops and per-node `focusDist` frames the fly-to. Taller cards ⇒ re-verify reset fit AND pinned framing per node. |
| Theme keys | Every `THEME.dark` key must exist in `THEME.light` (and vice versa). Materials that bypass the shell-tint pass need their own line in `toggleTheme` or a `userData.regen`. |
| Self-containment | Zero runtime network requests. Everything is inlined (fonts: system stack only). Verify: exactly 1 request, the document. |
| Wide scene, tall viewport | Letterboxing is a known accepted quirk, not a bug. |

## Performance budget

Draw calls and fps are printed live in the bottom-right status text (`#fps`). The template ships at ~284 draw calls / 120 fps (city, at rest) and ~69 draws (diagram). Instanced lamps/trees, one baked ground texture (2 draws incl. water), no postprocessing. Stay in that neighborhood: if an adaptation meaningfully exceeds ~300 draws or drops below ~100 fps at 1600×960, simplify (bake, instance, merge) before shipping.
