# Design language — the mosby look

The visual rules the template embodies. They were reached by iteration with a real reviewer; deviations tend to get reverted. Follow them unless the requester explicitly asks otherwise.

## Metaphor mapping

Map the target system onto the city with this table. The metaphor should tell the architecture's truth — placement is an argument, not decoration.

| System concept | City form |
|---|---|
| Core service / monolith | The hero building downtown: a tower whose floors are its modules, each floor a hoverable node. Exterior lift carries intra-tower flow steps. |
| Self-hosted supporting services | District buildings near downtown: warehouse (media/worker services), fenced substation (bus/cache), silo (database), gabled warehouse (object storage). |
| Third-party / external services | Tall towers literally OUTSIDE city limits — across the river, reached by bridges. Distance = trust boundary. |
| Clients / apps | Phone kiosks at the city's approach road, facing in. |
| Planned but not deployed | A ghost: fenced unbuilt lot, dashed parcel, low-opacity wireframe, hazard sign stating plainly why it isn't on. Honesty beats completeness. |
| Built but not wired (code exists, tests pass, nothing calls it) | A normal, solid building — the code is real — with `badge:'orphaned'`, the wiring gap stated first in its `cond` list, and any flow that depends on it named with a "(BUILT · NOT WIRED)" suffix. Never ghost it (that says "not built") and never draw it as plain normal (that says "in use"). |
| Ownership vs. locality conflict (a third-party binary spawned locally, an MCP server, a vendored service) | Ownership wins. Code the project's team did not write goes across the river even if it runs on the same machine; the bridge it crosses is the trust boundary the flow should visibly traverse. |
| End-to-end flows | Vehicles driving the road network (one silhouette per flow — the template ships five, so five flows is the ceiling unless you add a silhouette), lit route ribbon, step captions. Diagram mode: a pulse along orthogonal connectors. |

Zones/districts get quiet baked ground lettering ("DOWNTOWN — THE CONTROL PLANE", "DATA DISTRICT — GO-OWNED"…). A separate deployment the same team owns (a cloud backend beside a local daemon) earns its own district on the near side of the river, reached by a bridge — the bridge is the network boundary, the river is the ownership boundary. No empty-plot filler: no unlabeled infill buildings, no parked cars, no decorative gates — every structure on the map must mean something. (Infill was tried and removed by the reviewer: it diluted the named buildings.)

## Color and mood

- Late-afternoon overcast: flat neutral light, no colored sun, no bloom, no postprocessing.
- Desaturated concrete / stone / glass / dark asphalt. Toy-bright colors and building-wide glows are the #1 "cartoonish" complaint — accent color survives only as thin trim bands, signage light, and the banner hairline. Emissive intensities low.
- Two full themes (dark + light), both first-class. Light = clean print, not inverted dark.
- Six tone families (control/media/money/moderation/data/external) shared by sidebar chips, banners, ribbons, diagram stripes — color always means the same thing everywhere.
- Facades carry baked window grids so towers read as buildings, not slabs.

## Information layers

1. **Banner** (per building): rounded plate — brand logo · big PURPOSE · service-name subtitle · tone hairline. The hero's banner is the largest by a clear margin. Ghost nodes get a dashed, faded banner.
2. **Building signage**: logo/name plates on the structure itself (crown or facade).
3. **Ground lettering**: districts and approach labels, baked, low-contrast.
4. **Hover/pin card** (right panel): "what it does" / "how it's built" tabs, one-liner, phase badges, open-items (CONDITION) punch list.
5. **Flow captions**: `live demo · flow N/M · step K/J` + one sentence per step, in plain language that a reviewer could read aloud.

## Behavior contract

- Boots into a looping live demo (flow 1 end-to-end, then the rest); any PLAY/step interaction hands control to the user; RESET VIEW re-fits and restarts the demo; Escape clears.
- Hover = label hot + card; click = pin + fly-to; sidebar chips mirror scene state.
- Off-flow content dims (0.44 soft during demo) so the active flow reads instantly.
- `city · diagram` toggle: same data, same sidebar/cards/flow player; diagram = flat UML-package sheet, orthogonal connectors derived from flows, pulses instead of vehicles, drafting-camera (tight FOV, high angle).

## Delivery bar

A mosby deliverable is done when: single self-contained HTML (zero network), both modes, both themes, all flows play with correct captions, hover/pin/fly-to on every node, clean console after reload, ~300 draws / 100+ fps at 1600×960, nothing cut off at 1280×800, and it has been screenshot-verified in a real browser — not assumed.
