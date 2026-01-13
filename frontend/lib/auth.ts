import { Session } from "@/types/user";

export async function getSessionServer(): Promise<Session | null> {
  const { cookies } = await import("next/headers");
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;
  if (!accessToken) return null;
  return { accessToken } as Session;
}

export async function setSessionServer(session: Session) {
  const { cookies } = await import("next/headers");
  const cookieStore = await cookies();
  if (session.accessToken) {
    cookieStore.set("access_token", session.accessToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
    });
  }
}

export async function clearSessionServer() {
  const { cookies } = await import("next/headers");
  const cookieStore = await cookies();
  cookieStore.set("access_token", "", {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    expires: new Date(0),
  });
}

export function getAccessToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
}

export function setAccessToken(token: string) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
}
