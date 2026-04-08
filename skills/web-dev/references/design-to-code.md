# Design-to-Code: Converting .pen Files to Working Code

## Extracting Design Information

Use these Pencil MCP tools in sequence:

### 1. Get the big picture

```
get_editor_state()  → understand what .pen file is open and what's selected
get_screenshot()    → see the full visual design
```

Start with a screenshot to understand the overall layout, visual style, and page structure before diving into node details.

### 2. Extract structure

```
batch_get(patterns=["*"])  → get top-level nodes (pages, frames, sections)
```

Then drill into specific sections:
```
batch_get(nodeIds=["<frame-id>"])  → get children of a specific frame
```

Walk the tree top-down: page → sections → components → elements.

### 3. Extract design tokens

```
get_style_guide()     → color palette, typography scale, spacing system
get_variables()       → CSS variables / design tokens defined in the file
```

These map directly to CSS custom properties or Tailwind config.

## Mapping .pen Nodes to Code

| .pen node type | HTML/Component equivalent |
|---|---|
| Frame with children | `<div>` / `<section>` / component wrapper |
| Text node | `<p>`, `<h1>`-`<h6>`, `<span>` depending on size/weight |
| Image node | `<img>` / `next/image` |
| Button component | `<button>` / `<Button>` from UI library |
| Input component | `<input>` / `<Input>` from UI library |
| Card component | `<Card>` with `<CardHeader>`, `<CardContent>`, etc. |
| Sidebar component | Sidebar layout component with nav items |
| Icon (Lucide) | Import from `lucide-react` or equivalent |

## Extracting Styles

From each node, extract:

- **Layout:** `display`, flex/grid direction, gap, padding, alignment → Tailwind classes or CSS
- **Typography:** font family, size, weight, line-height, color → `text-*`, `font-*` classes
- **Colors:** background, foreground, border colors → CSS variables or Tailwind config
- **Spacing:** margin, padding, gap values → spacing scale values
- **Sizing:** width, height, min/max constraints → responsive utilities
- **Effects:** shadows, border-radius, opacity → utility classes

### CSS Variable Pattern

When the .pen file uses variables like `$--background`, `$--primary`, `$--sidebar`:

```css
:root {
  --background: <extracted-value>;
  --foreground: <extracted-value>;
  --primary: <extracted-value>;
  --primary-foreground: <extracted-value>;
  /* ... map all variables from get_variables() */
}
```

## shadcn/ui Design System Mapping

If the .pen file uses shadcn components (common pattern), map them directly:

| .pen component name | shadcn/ui import |
|---|---|
| Button/Default | `import { Button } from "@/components/ui/button"` |
| Button/Destructive | `<Button variant="destructive">` |
| Button/Outline | `<Button variant="outline">` |
| Button/Ghost | `<Button variant="ghost">` |
| Badge/Default | `import { Badge } from "@/components/ui/badge"` |
| Avatar/Text | `import { Avatar, AvatarFallback } from "@/components/ui/avatar"` |
| Accordion/Open | `import { Accordion, AccordionItem, ... }` |
| Sidebar | `import { Sidebar, SidebarHeader, ... } from "@/components/ui/sidebar"` |

Install with: `npx shadcn@latest add <component-name>`

## Workflow

1. Screenshot first — understand the visual goal
2. Extract structure — build the component tree
3. Extract tokens — set up the theme/design system
4. Map components — identify which UI library components to use
5. Generate code — write components that match the design
6. Screenshot again — compare your output with the original design
