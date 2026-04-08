# Vue / Nuxt Patterns

## Project Scaffold (Nuxt 3)

```
my-app/
├── app.vue                     # Root component
├── nuxt.config.ts              # Nuxt configuration
├── pages/
│   ├── index.vue               # / route
│   └── [page-name].vue         # /page-name route
├── components/
│   ├── ui/                     # UI components
│   └── [feature]/              # Feature components
├── composables/
│   └── use-api.ts              # Composables (auto-imported)
├── server/
│   ├── api/
│   │   └── [resource].ts       # API routes (auto-registered)
│   └── middleware/              # Server middleware
├── stores/
│   └── [store-name].ts         # Pinia stores
├── assets/
│   └── css/
│       └── main.css            # Global styles
├── public/                     # Static assets
├── package.json
└── tsconfig.json
```

## Setup Commands

```bash
npx nuxi@latest init my-app
cd my-app
npm install
npm install @pinia/nuxt pinia        # State management
```

For standalone Vue (no SSR):
```bash
npm create vite@latest my-app -- --template vue-ts
cd my-app
npm install vue-router pinia
```

## API Routes (Nuxt server/)

```typescript
// server/api/items.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const page = Number(query.page) || 1;

  const items = await db.items.findMany({
    skip: (page - 1) * 20,
    take: 20,
  });

  return { items, page };
});

// server/api/items.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event);

  if (!body.name || typeof body.name !== "string") {
    throw createError({ statusCode: 400, message: "name is required" });
  }

  const item = await db.items.create({ data: body });
  return item;
});
```

## Composition API Components

```vue
<!-- pages/index.vue -->
<script setup lang="ts">
const { data: items, pending, error, refresh } = await useFetch("/api/items");
</script>

<template>
  <div class="container mx-auto p-6">
    <h1 class="text-2xl font-bold mb-4">Items</h1>

    <div v-if="pending">Loading...</div>
    <div v-else-if="error" class="text-red-500">{{ error.message }}</div>
    <div v-else class="grid gap-4 md:grid-cols-3">
      <div
        v-for="item in items"
        :key="item.id"
        class="rounded-lg border p-4"
      >
        <h2 class="font-semibold">{{ item.name }}</h2>
      </div>
    </div>
  </div>
</template>
```

## Pinia Store

```typescript
// stores/items.ts
import { defineStore } from "pinia";

interface Item {
  id: string;
  name: string;
}

export const useItemsStore = defineStore("items", () => {
  const items = ref<Item[]>([]);
  const loading = ref(false);

  async function fetchItems() {
    loading.value = true;
    try {
      const data = await $fetch<{ items: Item[] }>("/api/items");
      items.value = data.items;
    } finally {
      loading.value = false;
    }
  }

  async function createItem(name: string) {
    const item = await $fetch<Item>("/api/items", {
      method: "POST",
      body: { name },
    });
    items.value.push(item);
  }

  return { items, loading, fetchItems, createItem };
});
```

## Composable Pattern

```typescript
// composables/use-api.ts
export function useApi<T>(url: string) {
  const data = ref<T | null>(null);
  const error = ref<string | null>(null);
  const loading = ref(true);

  async function fetch() {
    loading.value = true;
    error.value = null;
    try {
      data.value = await $fetch<T>(url);
    } catch (e: any) {
      error.value = e.message;
    } finally {
      loading.value = false;
    }
  }

  onMounted(fetch);

  return { data, error, loading, refetch: fetch };
}
```

## Nuxt Config

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ["@pinia/nuxt"],
  css: ["~/assets/css/main.css"],
  devtools: { enabled: true },

  // If using Tailwind
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
});
```

## Vue Router (standalone Vue only)

```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: () => import("../pages/Home.vue") },
    { path: "/items", component: () => import("../pages/Items.vue") },
    { path: "/items/:id", component: () => import("../pages/ItemDetail.vue") },
  ],
});

export default router;
```

Nuxt auto-generates routes from the `pages/` directory — no manual router needed.
