# Next.js + shadcn/ui Patterns

## Project Scaffold

```
my-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout (fonts, theme provider, global styles)
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Tailwind + CSS variables
│   │   ├── api/
│   │   │   └── [resource]/
│   │   │       └── route.ts    # API route handlers
│   │   └── [page-name]/
│   │       ├── page.tsx        # Page component
│   │       └── loading.tsx     # Loading UI (optional)
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components (auto-generated)
│   │   └── [feature]/          # Feature-specific components
│   ├── lib/
│   │   ├── utils.ts            # cn() helper, shared utilities
│   │   └── db.ts               # Database client (if needed)
│   └── hooks/                  # Custom React hooks
├── public/                     # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
└── components.json             # shadcn/ui config
```

## Setup Commands

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app
npx shadcn@latest init
```

## API Route Handlers

```typescript
// src/app/api/items/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = parseInt(searchParams.get("page") ?? "1");

  const items = await db.items.findMany({
    skip: (page - 1) * 20,
    take: 20,
  });

  return NextResponse.json({ items, page });
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Validate input
  if (!body.name || typeof body.name !== "string") {
    return NextResponse.json({ error: "name is required" }, { status: 400 });
  }

  const item = await db.items.create({ data: body });
  return NextResponse.json(item, { status: 201 });
}
```

## Server Components (default)

```tsx
// src/app/dashboard/page.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default async function DashboardPage() {
  // Data fetching happens directly in the component — no useEffect needed
  const stats = await fetch("https://api.example.com/stats", {
    next: { revalidate: 60 }, // Cache for 60 seconds
  }).then((r) => r.json());

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {stats.map((stat) => (
        <Card key={stat.id}>
          <CardHeader>
            <CardTitle>{stat.label}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{stat.value}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
```

## Client Components (when interactivity needed)

```tsx
// src/components/feature/search-bar.tsx
"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search } from "lucide-react";

export function SearchBar({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState("");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSearch(query);
      }}
      className="flex gap-2"
    >
      <Input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <Button type="submit" size="icon">
        <Search className="h-4 w-4" />
      </Button>
    </form>
  );
}
```

## Server Actions (form mutations)

```typescript
// src/app/actions.ts
"use server";

import { revalidatePath } from "next/cache";

export async function createItem(formData: FormData) {
  const name = formData.get("name") as string;

  if (!name) {
    return { error: "Name is required" };
  }

  await db.items.create({ data: { name } });
  revalidatePath("/items");
}
```

## Layout Pattern

```tsx
// src/app/layout.tsx
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex min-h-screen">
          {/* Sidebar if needed */}
          <main className="flex-1 p-6">{children}</main>
        </div>
      </body>
    </html>
  );
}
```

## Database (Prisma — optional)

```bash
npm install prisma @prisma/client
npx prisma init
```

```prisma
// prisma/schema.prisma
model Item {
  id        String   @id @default(cuid())
  name      String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

```bash
npx prisma db push    # Apply schema
npx prisma generate   # Generate client
```
