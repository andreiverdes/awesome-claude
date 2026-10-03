# shadcn/ui — Templates, Theming & Conventions

shadcn/ui is a set of accessible components built on Radix UI and Tailwind CSS. It is a CLI that copies component source into your project — you own and edit the code. Free alternative to paid kits (HeroUI Pro, Tremor Pro).

Next.js setup commands live in `nextjs.md`. For an existing project:

```bash
npx shadcn@latest init                                   # writes components.json
npx shadcn@latest add                                    # browse components
npx shadcn@latest add sidebar data-table chart command   # add specific ones
```

`components.json` controls style, paths, and Tailwind config for the CLI.

Common dashboard components: `sidebar`, `data-table`, `chart`, `card`, `dialog`, `sheet`, `dropdown-menu`, `command`, `tabs`, `badge`, `avatar`.

## Free Dashboard Templates

Ranked by polish and completeness. All MIT-licensed.

### Tier 1 — Production-Ready

| Template | Stack | Highlights | Link |
|----------|-------|------------|------|
| **shadcn-admin** | Vite + TanStack Router | Auth pages, settings, error states, Clerk integration. Fast SPA admin without Next.js overhead. | github.com/satnaing/shadcn-admin |
| **next-shadcn-dashboard-starter** | Next.js + App Router | Analytics, server-side data tables, RBAC nav, multi-tenant workspaces, billing flows. | github.com/Kiranism/next-shadcn-dashboard-starter |
| **shadcn-dashboard-landing-template** | React/Next.js + Vite | Full dashboard (mail, tasks, chat, calendar) AND marketing landing page. Tailwind v4. | github.com/silicondeck/shadcn-dashboard-landing-template |

### Tier 2 — Solid Starters

| Template | Stack | Highlights | Link |
|----------|-------|------------|------|
| **Shadboard** | Next.js 15 | Open-source, community-driven, scalable admin dashboard. | github.com/Qualiora/shadboard |
| **Official shadcn Dashboard** | Next.js | The canonical example from shadcn itself. Clean, minimal. | ui.shadcn.com/examples/dashboard |
| **Apex Dashboard** | Next.js + React 19 | 5 dashboard variations, 20+ pages, theme customizer, dark/light, RTL. | tailwind-admin.com |

### Tier 3 — Specialized

| Template | Focus | Link |
|----------|-------|------|
| **Tremor** | Data dashboards & analytics | tremor.so |
| **TailAdmin** | Tailwind-first admin (React/Next.js versions) | tailadmin.com |
| **Horizon UI** | Chakra UI dashboard (different style system) | horizon-ui.com |

### Selection

```
Need a dashboard?
├── Vite (SPA, no SSR)? → shadcn-admin
├── Next.js App Router? → next-shadcn-dashboard-starter
├── Dashboard + landing page? → shadcn-dashboard-landing-template
├── Heavy data viz? → Tremor
└── Just exploring? → Official shadcn dashboard example
```

## Component Layout

```
src/
├── components/
│   ├── ui/              # shadcn base components (button, card, dialog...)
│   ├── layouts/         # Page layouts, sidebars, navbars
│   └── features/        # Domain-specific composed components
├── lib/
│   └── utils.ts         # cn() helper
└── app/
    └── globals.css      # CSS variables for theming
```

Every shadcn project merges conditional classes with `cn()`:

```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Theming (Tailwind v4)

Colors are OKLCH CSS variables in `globals.css`, exposed to Tailwind via `@theme inline`. There is no `tailwind.config.ts` in v4.

```css
@import "tailwindcss";

@custom-variant dark (&:is(.dark *));

:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  /* ... */
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  /* ... */
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... */
}
```

Generate palettes at **ui.shadcn.com/themes** (or tweakcn) before hand-tuning.

## Resources

- **awesome-shadcn-ui** — curated templates, blocks, plugins: github.com/birobirobiro/awesome-shadcn-ui
- **Blocks** — pre-built sections (hero, pricing, auth forms): ui.shadcn.com/blocks
- **Charts** — Recharts-based chart components: ui.shadcn.com/charts
- **v0.dev** — AI UI generator that outputs shadcn components

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Installing shadcn as an npm package | It's a CLI that copies files — `npx shadcn@latest add`, not `npm install` |
| Editing `ui/` components for one-off changes | Compose wrappers in `features/` instead |
| Conditional classes without `cn()` | Always use `cn()` — it resolves Tailwind class conflicts |
| HSL variables / `tailwind.config.ts` theming | Tailwind v4 projects use OKLCH vars + `@theme inline` |
| `add --all` | Add only what you use — keeps the tree small |
