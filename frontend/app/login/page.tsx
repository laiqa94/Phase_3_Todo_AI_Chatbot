"use client";


import Link from "next/link";
import { useRouter } from "next/navigation";
import { Suspense, useState } from "react";

import { useToast } from "@/components/ToastHost";

import { ParamsClient } from "./paramsClient";

type LoginResponse = {
  accessToken: string;
  expiresAt?: string;
  user: { id: string; email: string; displayName?: string };
};

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  );
}

function LoginForm() {
  const router = useRouter();
  const toast = useToast();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent, next: string | null) {
    e.preventDefault();
    setError(null);

    if (!email.trim() || !password) {
      setError("Email and password are required.");
      return;
    }

    try {
      setSubmitting(true);
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: "Login failed" }));
        throw new Error(errorData.message || "Login failed");
      }

      // Process the response to ensure the cookie is set
      const data = await response.json();

      // Store token and user ID in localStorage for client-side use
      if (data.accessToken) {
        localStorage.setItem('access_token', data.accessToken);
      }
      if (data.user?.id) {
        localStorage.setItem('user_id', data.user.id.toString());
      }

      toast.success("Logged in.");
      router.replace(next ?? "/dashboard");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Login failed.";
      setError(msg);
      toast.error(msg);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <ParamsClient>
      {(next) => (
        <div className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4">
          <h1 className="text-2xl font-semibold text-zinc-900">Sign in</h1>
          <p className="mt-1 text-sm text-zinc-600">Welcome back.</p>

          <form onSubmit={(e) => onSubmit(e, next)} className="mt-6 grid gap-3">
            <label className="grid gap-1">
              <span className="text-sm font-medium text-zinc-700">Email</span>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-10 rounded-md border border-zinc-200 px-3"
                autoComplete="email"
              />
            </label>

            <label className="grid gap-1">
              <span className="text-sm font-medium text-zinc-700">Password</span>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="h-10 rounded-md border border-zinc-200 px-3"
                autoComplete="current-password"
              />
            </label>

            <button
              type="submit"
              disabled={submitting}
              className="mt-2 h-10 rounded-md bg-zinc-900 px-4 text-white hover:bg-zinc-800 disabled:opacity-60"
            >
              {submitting ? "Signing in…" : "Sign in"}
            </button>

            {error ? <p className="text-sm text-red-600">{error}</p> : null}
          </form>

          <p className="mt-6 text-sm text-zinc-600">
            No account?{" "}
            <Link className="text-zinc-900 underline" href="/register">
              Create one
            </Link>
          </p>
        </div>
      )}
    </ParamsClient>
  );
}

