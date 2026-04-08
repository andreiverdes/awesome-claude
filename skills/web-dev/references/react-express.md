# React + Express Patterns

## Project Scaffold

```
my-app/
├── client/                     # React frontend (Vite)
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── ui/             # UI components
│   │   │   └── [feature]/      # Feature components
│   │   ├── hooks/
│   │   │   └── use-api.ts      # API client hook
│   │   ├── lib/
│   │   │   └── api.ts          # API client
│   │   └── pages/              # Page components (if using router)
│   ├── index.html
│   ├── vite.config.ts
│   └── tsconfig.json
├── server/                     # Express backend
│   ├── src/
│   │   ├── index.ts            # Entry point
│   │   ├── routes/
│   │   │   └── [resource].ts   # Route handlers
│   │   ├── middleware/
│   │   │   ├── error-handler.ts
│   │   │   └── validate.ts
│   │   └── lib/
│   │       └── db.ts           # Database client
│   ├── tsconfig.json
│   └── package.json
├── package.json                # Root (workspace scripts)
└── tsconfig.base.json
```

## Setup Commands

```bash
# Frontend
npm create vite@latest client -- --template react-ts
cd client && npm install react-router-dom

# Backend
mkdir -p server/src/{routes,middleware,lib}
cd server && npm init -y
npm install express cors dotenv
npm install -D typescript @types/express @types/cors tsx
```

## Express API Patterns

```typescript
// server/src/index.ts
import express from "express";
import cors from "cors";
import { itemsRouter } from "./routes/items";
import { errorHandler } from "./middleware/error-handler";

const app = express();
const port = process.env.PORT ?? 3001;

app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.json());

app.use("/api/items", itemsRouter);

app.use(errorHandler);

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

```typescript
// server/src/routes/items.ts
import { Router } from "express";

export const itemsRouter = Router();

itemsRouter.get("/", async (req, res, next) => {
  try {
    const items = await db.items.findMany();
    res.json(items);
  } catch (err) {
    next(err);
  }
});

itemsRouter.post("/", async (req, res, next) => {
  try {
    const { name } = req.body;
    if (!name || typeof name !== "string") {
      return res.status(400).json({ error: "name is required" });
    }
    const item = await db.items.create({ data: { name } });
    res.status(201).json(item);
  } catch (err) {
    next(err);
  }
});
```

```typescript
// server/src/middleware/error-handler.ts
import type { ErrorRequestHandler } from "express";

export const errorHandler: ErrorRequestHandler = (err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: "Internal server error" });
};
```

## React API Client

```typescript
// client/src/lib/api.ts
const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:3001/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(error.error ?? "Request failed");
  }

  return res.json();
}

export const api = {
  items: {
    list: () => request<Item[]>("/items"),
    create: (data: { name: string }) =>
      request<Item>("/items", {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },
};
```

## React Hook Pattern

```typescript
// client/src/hooks/use-api.ts
import { useState, useEffect, useCallback } from "react";

export function useApi<T>(fetcher: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const refetch = useCallback(() => {
    setLoading(true);
    setError(null);
    fetcher()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [fetcher]);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { data, error, loading, refetch };
}
```

## Vite Proxy (alternative to CORS)

```typescript
// client/vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:3001",
        changeOrigin: true,
      },
    },
  },
});
```

With the proxy, remove `cors()` from Express and use relative paths in the API client (`/api` instead of `http://localhost:3001/api`).

## Root package.json Scripts

```json
{
  "scripts": {
    "dev": "concurrently \"npm run dev:server\" \"npm run dev:client\"",
    "dev:client": "cd client && npm run dev",
    "dev:server": "cd server && npx tsx watch src/index.ts",
    "build": "cd client && npm run build",
    "start": "cd server && node dist/index.js"
  }
}
```
