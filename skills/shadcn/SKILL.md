---
name: shadcn
description: Use when building UIs with shadcn/ui, scaffolding a new shadcn project, choosing a dashboard template, or looking for free polished admin/dashboard starter kits with Tailwind CSS. Triggers on mentions of shadcn, Tailwind dashboard, admin template, or UI component library selection.
---

# shadcn/ui — Setup, Templates & Resources

## Overview

shadcn/ui is a collection of reusable, accessible components built with Radix UI and Tailwind CSS. Unlike traditional component libraries, you copy components into your project — giving full ownership and customization. It's the go-to free alternative to paid UI kits like HeroUI Pro.

## When to Use

- User wants a polished, free UI component system
- Building a dashboard, admin panel, or SaaS frontend
- Need a production-ready starter template
- Comparing UI frameworks or looking for free alternatives to paid kits (HeroUI Pro, Tremor Pro, etc.)

## Quick Setup

```bash
# New Next.js project with shadcn
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app
npx shadcn@latest init

# Add components as needed
npx shadcn@latest add button card table dialog chart
```

Key config file: `components.json` — controls style, paths, and Tailwind config for shadcn CLI.

## Best Free Dashboard Templates

Ranked by polish and completeness. All are MIT-licensed.

### Tier 1 — Production-Ready

| Template | Stack | Highlights | Link |
|----------|-------|------------|------|
| **shadcn-admin** | Vite + TanStack Router | Auth pages, settings, error states, Clerk integration. Fast SPA admin without Next.js overhead. | github.com/satnaing/shadcn-admin |
| **next-shadcn-dashboard-starter** | Next.js + App Router | Analytics, server-side data tables, RBAC nav, multi-tenant workspaces, billing flows. | github.com/Kiranism/next-shadcn-dashboard-starter |
| **shadcn-dashboard-landing-template** | React/Next.js + Vite | Full dashboard (mail, tasks, chat, calendar) AND marketing landing page. shadcn/ui v3 + Tailwind v4. | github.com/silicondeck/shadcn-dashboard-landing-template |

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

## Template Selection Guide

```
Need a dashboard?
├── Want Vite (SPA, no SSR)? → shadcn-admin
├── Want Next.js App Router? → next-shadcn-dashboard-starter
├── Need dashboard + landing page? → shadcn-dashboard-landing-template
├── Need heavy data viz? → Tremor
└── Just exploring? → Official shadcn dashboard example
```

## Component Architecture

shadcn components live in `src/components/ui/`. Key patterns:

```
src/
├── components/
│   ├── ui/              # shadcn base components (button, card, dialog...)
│   ├── layouts/         # Page layouts, sidebars, navbars
│   └── features/        # Domain-specific composed components
├── lib/
│   └── utils.ts         # cn() helper for merging Tailwind classes
└── app/
    └── globals.css      # CSS variables for theming
```

### The `cn()` helper

Every shadcn project uses this for conditional class merging:

```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Theming

shadcn uses CSS variables for theming. Override in `globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    /* ... */
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... */
  }
}
```

Use the official theme generator at **ui.shadcn.com/themes** to create custom palettes.

## Adding Components to Existing Projects

```bash
# Browse available components
npx shadcn@latest add

# Add specific ones
npx shadcn@latest add sidebar data-table chart command

# Add all (not recommended — adds bloat)
npx shadcn@latest add --all
```

Common dashboard components: `sidebar`, `data-table`, `chart`, `card`, `dialog`, `sheet`, `dropdown-menu`, `command`, `tabs`, `badge`, `avatar`.

## Resource Hub

- **awesome-shadcn-ui** — Curated list of shadcn resources, templates, blocks, and plugins: github.com/birobirobiro/awesome-shadcn-ui
- **shadcn/ui Blocks** — Pre-built page sections (hero, pricing, auth forms): ui.shadcn.com/blocks
- **shadcn/ui Themes** — Theme generator: ui.shadcn.com/themes
- **shadcn/ui Charts** — Chart components built on Recharts: ui.shadcn.com/charts
- **v0.dev** — AI-powered UI generator that outputs shadcn components

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Installing shadcn as npm package | It's a CLI that copies files — run `npx shadcn@latest add`, not `npm install` |
| Editing `ui/` components directly for one-off changes | Compose wrapper components in `features/` instead |
| Not using `cn()` for conditional classes | Always use `cn()` — it handles Tailwind class conflicts properly |
| Skipping the theme generator | Use ui.shadcn.com/themes for consistent color palettes before hand-tuning |
| Using `--all` to add every component | Only add what you need — keeps bundle small and tree clean |
