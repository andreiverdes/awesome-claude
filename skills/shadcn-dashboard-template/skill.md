# shadcn Dashboard + Landing Template Expert

You are an expert in the shadcn-dashboard-landing-template (github.com/shadcnstore/shadcn-dashboard-landing-template). This skill makes you deeply knowledgeable about its architecture, components, layout patterns, and conventions so you can build new frontends that match its design language perfectly.

## When to Use

- Building `frontend-dashboard` or `frontend-landing` for the Hired project
- Creating dashboard pages, landing pages, or app pages that follow this template's patterns
- Adapting the template's component patterns to a different backend/data model
- Questions about how a specific feature or layout works in this template

## Reference Repository

The cloned template lives at: `/Users/andrei/Developer/AI/hired/shadcn-dashboard-landing-template`

When you need to check exact implementation details, read files directly from the **vite-version** directory (preferred over next-version for this project since Hired uses Vite).

## Architecture Overview

### Tech Stack
- **React 19** + **TypeScript 5.9** + **Vite 7**
- **Tailwind CSS v4** with OKLCH color model and `@theme inline` config
- **shadcn/ui v3** (new-york style, neutral base) — 38 UI components
- **Radix UI** for accessible primitives
- **TanStack Table** for advanced data tables with sorting, filtering, pagination
- **Recharts 3** for charts (area, line, bar, pie)
- **React Hook Form + Zod** for form validation
- **@dnd-kit** for drag-and-drop
- **React Resizable Panels** for resizable layouts (mail app)
- **Zustand** for minimal global state
- **Sonner** for toast notifications
- **Lucide React** for icons
- **date-fns** for date utilities
- **cmdk** for command palette (Cmd+K search)

### File Organization
```
vite-version/src/
├── app/                    # Route-based page directories
│   ├── dashboard/          # Dashboard v1 (stats, chart, table)
│   ├── dashboard-2/        # Dashboard v2 (sales, revenue, products)
│   ├── mail/               # 3-panel resizable email app
│   ├── tasks/              # Task management with TanStack Table
│   ├── chat/               # Real-time chat with conversations
│   ├── calendar/           # Calendar with events
│   ├── users/              # User CRUD with data table
│   ├── landing/            # Full marketing landing page
│   │   └── sections/       # Hero, Features, Pricing, Team, etc.
│   ├── auth/               # 9 auth variants (3 sign-in, 3 sign-up, 3 forgot)
│   ├── settings/           # 6 settings pages
│   ├── errors/             # 5 error pages (401-503)
│   ├── pricing/            # Pricing plans
│   └── faqs/               # FAQ with categories
├── components/
│   ├── ui/                 # 38 shadcn/ui base components
│   ├── layouts/            # BaseLayout wrapper
│   ├── theme-customizer/   # Live theme editor
│   ├── landing/            # Landing-specific (MegaMenu)
│   ├── app-sidebar.tsx     # Main sidebar navigation
│   ├── nav-main.tsx        # Nav group with collapsible sub-items
│   ├── nav-user.tsx        # User profile in sidebar footer
│   ├── site-header.tsx     # Top header bar
│   ├── site-footer.tsx     # Footer
│   ├── command-search.tsx  # Cmd+K search dialog
│   ├── mode-toggle.tsx     # Dark/light toggle
│   └── logo.tsx            # Brand logo
├── hooks/                  # use-mobile, use-theme, use-sidebar-config, etc.
├── lib/                    # utils.ts (cn helper), fonts.ts
├── contexts/               # ThemeProvider, SidebarConfig contexts
├── config/                 # routes.tsx, theme-data.ts
└── utils/                  # Theme presets, analytics
```

## Layout System

### BaseLayout (All Dashboard/App Pages)
```
┌──────────────────────────────────────────────┐
│ SidebarProvider                               │
│ ┌──────────┬────────────────────────────────┐│
│ │          │ SidebarInset                    ││
│ │          │ ┌────────────────────────────┐  ││
│ │ App      │ │ SiteHeader (fixed)         │  ││
│ │ Sidebar  │ ├────────────────────────────┤  ││
│ │ (16rem)  │ │                            │  ││
│ │          │ │ Page Content               │  ││
│ │          │ │ (px-4 lg:px-6, py-4)       │  ││
│ │          │ │                            │  ││
│ │          │ ├────────────────────────────┤  ││
│ │          │ │ SiteFooter                 │  ││
│ │          │ └────────────────────────────┘  ││
│ └──────────┴────────────────────────────────┘│
└──────────────────────────────────────────────┘
```

**Key CSS**: The sidebar uses CSS variable `--sidebar-width: 16rem` (collapsible to `--sidebar-width-icon: 3rem`). Header height is `--header-height: calc(var(--spacing) * 14)`.

### Landing Page Layout
No sidebar. Full-width scrolling page with alternating section backgrounds:
```
┌─────────────────────────────────────────┐
│ Navbar (sticky, backdrop-blur)          │
├─────────────────────────────────────────┤
│ Hero (gradient bg + dot pattern)        │
│ Logo Carousel                           │
│ Stats (bg-primary/8 gradient)           │
│ About                                   │
│ Features (bg-muted/30)                  │
│ Team                                    │
│ Pricing (bg-muted/40)                   │
│ Testimonials                            │
│ Blog (bg-muted/50)                      │
│ FAQ                                     │
│ CTA (bg-muted/80)                       │
│ Contact                                 │
│ Footer                                  │
└─────────────────────────────────────────┘
```

## Component Patterns

### Stat/KPI Cards
Used in Dashboard, Dashboard-2, Tasks, Users. Pattern:
```tsx
<Card className="@container/card">
  <CardHeader>
    <CardDescription>Label</CardDescription>
    <CardTitle className="text-2xl font-semibold @[250px]/card:text-3xl tabular-nums">
      Value
    </CardTitle>
    <CardAction>
      <Badge variant="outline">+12.5% <TrendingUp /></Badge>
    </CardAction>
  </CardHeader>
  <CardFooter className="flex-col items-start gap-1 text-sm">
    <div className="flex gap-2 font-medium">Trend text <TrendingUp className="size-4" /></div>
    <div className="text-muted-foreground">Subtitle</div>
  </CardFooter>
</Card>
```
Cards use `from-primary/5 to-card` gradient background. Container queries (`@container/card`) adapt text size.

### Page Header Pattern
```tsx
<div className="flex items-center justify-between px-4 lg:px-6">
  <div>
    <h1 className="text-2xl font-bold tracking-tight">Page Title</h1>
    <p className="text-muted-foreground">Description text</p>
  </div>
  <div className="flex items-center gap-2">
    {/* Action buttons */}
  </div>
</div>
```

### Section Header Pattern (Landing)
```tsx
<div className="mx-auto mb-12 max-w-3xl text-center">
  <Badge variant="outline" className="mb-4">Section Label</Badge>
  <h2 className="mb-4 text-3xl font-bold tracking-tight sm:text-4xl">
    Heading with <span className="text-primary">highlight</span>
  </h2>
  <p className="text-lg text-muted-foreground">Description paragraph</p>
</div>
```

### Data Table Pattern
TanStack Table with this standard setup:
- Drag-and-drop rows via @dnd-kit
- Checkbox selection column
- Sortable column headers
- Faceted filtering with badges
- Column visibility toggle
- Pagination (first/prev/next/last)
- Row actions dropdown (edit, delete)
- Mobile: Drawer for row details
- Zod schema for data validation

### Chart Pattern
```tsx
<Card>
  <CardHeader>
    <CardTitle>Chart Title</CardTitle>
    <CardDescription>Subtitle</CardDescription>
    <CardAction>
      <ToggleGroup type="single" value={range} onValueChange={setRange}>
        <ToggleGroupItem value="90d">3 months</ToggleGroupItem>
        <ToggleGroupItem value="30d">30 days</ToggleGroupItem>
        <ToggleGroupItem value="7d">7 days</ToggleGroupItem>
      </ToggleGroup>
    </CardAction>
  </CardHeader>
  <CardContent>
    <ChartContainer config={chartConfig}>
      <AreaChart data={data}>
        <CartesianGrid horizontal={true} vertical={false} />
        <XAxis dataKey="date" tickFormatter={formatDate} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Area type="natural" dataKey="value" fill="url(#gradient)" stroke="var(--color-primary)" />
      </AreaChart>
    </ChartContainer>
  </CardContent>
</Card>
```

### Form Pattern (Auth, Settings, Contact)
```tsx
const schema = z.object({ email: z.string().email(), password: z.string().min(8) })
const form = useForm({ resolver: zodResolver(schema) })

<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    <FormField control={form.control} name="email" render={({ field }) => (
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl><Input {...field} /></FormControl>
        <FormMessage />
      </FormItem>
    )} />
    <Button type="submit">Submit</Button>
  </form>
</Form>
```

## Sidebar Navigation Structure

Three nav groups in `app-sidebar.tsx`:

```typescript
const navGroups = [
  {
    title: "Dashboards",
    items: [
      { title: "Dashboard", url: "/dashboard", icon: LayoutDashboard },
      { title: "Dashboard 2", url: "/dashboard-2", icon: LayoutPanelLeft },
    ]
  },
  {
    title: "Apps",
    items: [
      { title: "Mail", url: "/mail", icon: Mail },
      { title: "Tasks", url: "/tasks", icon: ListChecks },
      { title: "Chat", url: "/chat", icon: MessageCircle },
      { title: "Calendar", url: "/calendar", icon: Calendar },
      { title: "Users", url: "/users", icon: Users },
    ]
  },
  {
    title: "Pages",
    items: [
      { title: "Auth", icon: Shield, children: [/* 9 auth variants */] },
      { title: "Errors", icon: AlertTriangle, children: [/* 5 error pages */] },
      { title: "Settings", url: "/settings/user", icon: Settings },
      { title: "FAQs", url: "/faqs", icon: HelpCircle },
      { title: "Pricing", url: "/pricing", icon: CreditCard },
    ]
  }
]
```

Active state detection uses `useLocation().pathname`.

## Landing Page Sections (in order)

1. **Navbar** — Sticky, `bg-background/80 backdrop-blur-xl`, NavigationMenu with mega dropdown for Solutions, ModeToggle, mobile Sheet menu
2. **Hero** — Gradient bg + DotPattern overlay, announcement Badge, large headline with gradient text (`from-primary to-primary/60 bg-clip-text text-transparent`), 2 CTAs, dashboard preview image with glow effect
3. **Logo Carousel** — Auto-scrolling horizontal marquee of partner logos
4. **Stats** — 4-column grid on gradient bg, `bg-background/60 backdrop-blur-sm` cards, big numbers + descriptions
5. **About** — 4 value cards with CardDecorator, centered section header, GitHub/Discord CTAs
6. **Features** — 2 alternating rows (image + feature grid), `bg-muted/30`, 3D perspective images
7. **Team** — Member cards with Avatar, name, role, social links
8. **Pricing** — Monthly/Yearly ToggleGroup, 3-tier cards (Free/Pro/Lifetime), feature checklists with Check icons
9. **Testimonials** — Grid of quote cards with Avatar + name/role
10. **Blog** — 3-column card grid, aspect-video images, category labels, "Learn More" links
11. **FAQ** — Accordion with CircleHelp icons, "Ask a Question" CTA
12. **CTA** — Badge with stats, gradient headline, 2 large buttons, trust indicators
13. **Contact** — 2-column: contact option cards (left) + contact form (right) with RHF+Zod
14. **Footer** — Newsletter signup, 4-column link grid, social icons, copyright

## Theming System

### CSS Variables (OKLCH)
All colors use OKLCH color space. Key variables:
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1 through --chart-5
  --sidebar, --sidebar-foreground, --sidebar-primary, etc.
  --radius: 0.625rem;
}
.dark { /* all variables flipped */ }
```

### Theme Customizer
Live editor with tabs for Theme (colors) and Layout (sidebar variant/position). Supports import/export of theme configs. 20+ presets from shadcn/ui and tweakcn.

## Responsive Patterns

- **Container queries** (`@container/card`) for component-level responsiveness
- **Tailwind breakpoints**: `sm:`, `md:`, `lg:`, `xl:`, `@5xl:` (container)
- **Sidebar**: Collapses to icon-only (3rem) on smaller screens
- **Chart controls**: ToggleGroup → Select dropdown on narrow containers
- **Tables**: Drawer for row details on mobile
- **Landing navbar**: Full nav → Sheet menu on mobile
- **Grids**: Responsive columns (1 → 2 → 3 → 4 based on breakpoint)

## Data Patterns

Mock data lives in JSON files alongside page components:
- `app/dashboard/data.json` — table rows
- `app/tasks/tasks.json` — 100+ tasks
- `app/chat/conversations.json`, `messages.json`, `users.json`
- `app/calendar/events.json`, `event-dates.json`
- `app/users/data.json` — user list
- `app/settings/billing-history.json`, `current-plan.json`
- `app/faqs/faqs.json`, `features.json`, `categories.json`

Each data file has a matching Zod schema for type validation.

## Key shadcn/ui Components Used

| Component | Import | Common Usage |
|-----------|--------|-------------|
| Button | `@/components/ui/button` | `variant="default\|outline\|ghost\|destructive\|secondary"`, `size="default\|sm\|lg\|icon"` |
| Card | `@/components/ui/card` | `Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, CardAction` |
| Badge | `@/components/ui/badge` | `variant="default\|secondary\|outline\|destructive"` |
| Tabs | `@/components/ui/tabs` | `Tabs, TabsList, TabsTrigger, TabsContent` |
| Dialog | `@/components/ui/dialog` | Modal dialogs for forms, confirmations |
| Drawer | `@/components/ui/drawer` | Mobile-friendly bottom sheets |
| Sheet | `@/components/ui/sheet` | Side panels (mobile nav, details) |
| Table | `@/components/ui/table` | `Table, TableHeader, TableRow, TableHead, TableBody, TableCell` |
| Sidebar | `@/components/ui/sidebar` | Full sidebar system with `SidebarProvider, SidebarMenu, SidebarMenuItem, etc.` |
| Command | `@/components/ui/command` | Cmd+K search palette |
| Accordion | `@/components/ui/accordion` | FAQ sections |
| NavigationMenu | `@/components/ui/navigation-menu` | Landing page navbar |
| ToggleGroup | `@/components/ui/toggle-group` | Time range selectors, billing period toggles |
| Progress | `@/components/ui/progress` | Progress bars |
| Skeleton | `@/components/ui/skeleton` | Loading states |
| Separator | `@/components/ui/separator` | Visual dividers |

## How to Use This Skill

When building `frontend-dashboard` or `frontend-landing` for Hired:

1. **Read the actual source** from `/Users/andrei/Developer/AI/hired/shadcn-dashboard-landing-template/vite-version/src/` for exact implementation details
2. **Copy the layout structure** — BaseLayout + AppSidebar + SiteHeader for dashboard pages, sticky Navbar for landing
3. **Adapt data models** — Replace mock JSON data with Hired's API hooks (useApplications, usePortfolio, etc.)
4. **Keep the component patterns** — Card with CardAction for stats, TanStack Table for data, Recharts for charts
5. **Preserve the styling conventions** — OKLCH variables, container queries, gradient cards, `text-muted-foreground` for secondary text
6. **Match responsive behavior** — Container queries for cards, sidebar collapse, drawer for mobile table rows

### Quick Reference for Common Tasks

**Adding a new dashboard stat card**: Copy `section-cards.tsx` pattern from `app/dashboard/components/`
**Adding a data table**: Copy `data-table.tsx` from `app/tasks/components/` or `app/users/components/`
**Adding a chart**: Copy `chart-area-interactive.tsx` from `app/dashboard/components/`
**Adding a landing section**: Follow the section header pattern + grid layout from `app/landing/sections/`
**Adding an auth page**: Copy one of the 9 variants from `app/auth/`
**Adding a settings page**: Follow pattern from `app/settings/`
