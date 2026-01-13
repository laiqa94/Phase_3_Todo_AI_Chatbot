import "server-only";

import { redirect } from "next/navigation";

import { clearSessionServer, getSessionServer } from "@/lib/auth";
import { ApiError } from "@/lib/api";
import type { ApiErrorPayload } from "@/lib/apiTypes";

function baseUrl() {
  const url = process.env.API_BASE_URL;
  if (!url) throw new Error("API_BASE_URL is not set");
  return url;
}

type ApiFetchOptions = Omit<RequestInit, "body"> & {
  body?: unknown;
  auth?: "required" | "optional" | "none";
};

export async function apiFetchServer<T>(path: string, options: ApiFetchOptions = {}): Promise<T> {
  const authMode = options.auth ?? "required";
  const session = await getSessionServer();

  if (!session && authMode === "required") {
    redirect(`/login?next=${encodeURIComponent(path)}`);
  }

  const headers = new Headers(options.headers);
  headers.set("Accept", "application/json");
  if (options.body !== undefined) headers.set("Content-Type", "application/json");
  if (session?.accessToken) headers.set("Authorization", `Bearer ${session.accessToken}`);

  // Apply the same transformations as the proxy route
  let transformedPath = path;

  // Transform /api/me/tasks to /api/v1/tasks (replace 'me' with 'v1')
  if (transformedPath.startsWith('/api/me/')) {
    transformedPath = transformedPath.replace('/api/me/', '/api/v1/');
  }
  // Transform /api/me/tasks/{id}/complete to /api/v1/tasks/{id}/toggle (for completion toggle)
  else if (transformedPath.includes('/api/me/tasks/') && transformedPath.includes('/complete')) {
    transformedPath = transformedPath.replace('/api/me/tasks/', '/api/v1/tasks/')
                                   .replace('/complete', '/toggle');
  }
  // Transform /api/tasks to /api/v1/tasks (add v1 after api) - fallback
  else if (transformedPath.startsWith('/api/tasks')) {
    transformedPath = transformedPath.replace('/api/tasks', '/api/v1/tasks');
  }
  // Transform /api/auth to /api/v1/auth (add v1 after api) - fallback for any auth calls from server
  else if (transformedPath.startsWith('/api/auth')) {
    transformedPath = transformedPath.replace('/api/auth', '/api/v1/auth');
  }

  const res = await fetch(`${baseUrl()}${transformedPath.startsWith('/') ? transformedPath : '/' + transformedPath}`, {
    ...options,
    headers,
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  });

  if (res.status === 204) return undefined as T;

  const contentType = res.headers.get("content-type") ?? "";
  const payload: unknown = contentType.includes("application/json")
    ? await res.json().catch(() => null)
    : await res.text().catch(() => null);

  if (!res.ok) {
    if (res.status === 401) {
      await clearSessionServer();
      redirect(`/login?next=${encodeURIComponent(path)}`);
    }

    const maybeObj = typeof payload === "object" && payload ? (payload as ApiErrorPayload) : null;
    const message = maybeObj?.message ? String(maybeObj.message) : `Request failed (${res.status})`;
    throw new ApiError(message, res.status, payload);
  }

  return payload as T;
}
