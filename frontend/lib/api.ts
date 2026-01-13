import type { ApiErrorPayload } from "@/lib/apiTypes";
import { getAccessToken } from "./auth";

// NOTE: For 401/session-expiry policy, the server-side API wrapper (`apiFetchServer`)
// and middleware are the primary enforcement points.
// Client-side calls now use JWT tokens in Authorization header for auth.

export class ApiError extends Error {
  status: number;
  details?: unknown;

  constructor(message: string, status: number, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

type ApiFetchOptions = Omit<RequestInit, "body"> & {
  body?: unknown;
};

export async function apiFetch<T>(path: string, options: ApiFetchOptions = {}): Promise<T> {
  // For client-side API calls, we should use the frontend's proxy route
  // This ensures proper authentication handling and cookie management
  // The proxy route will handle path transformations and backend communication

  // Check if path already starts with /api/proxy to avoid double-prefixing
  let proxyPath: string;
  if (path.startsWith('/api/proxy/')) {
    proxyPath = path; // Path already includes proxy prefix
  } else {
    proxyPath = `/api/proxy${path.startsWith('/') ? path : '/' + path}`;
  }

  const url = proxyPath; // Use relative path so it goes to the same origin (frontend)

  const headers = new Headers(options.headers);
  headers.set("Accept", "application/json");

  // Add JWT token to Authorization header if available
  const token = getAccessToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  if (options.body !== undefined) {
    headers.set("Content-Type", "application/json");
  }

  const res = await fetch(url, {
    ...options,
    headers,
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  });

  if (res.status === 204) {
    return undefined as T;
  }

  let payload: unknown = null;
  const contentType = res.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    payload = await res.json().catch(() => null);
  } else {
    payload = await res.text().catch(() => null);
  }

  if (!res.ok) {
    const maybeObj = typeof payload === "object" && payload ? (payload as ApiErrorPayload) : null;
    const message = maybeObj?.message ? String(maybeObj.message) : `Request failed (${res.status})`;
    throw new ApiError(message, res.status, payload);
  }

  return payload as T;
}
