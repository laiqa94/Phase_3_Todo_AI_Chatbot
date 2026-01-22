import { Session } from "@/types/user";

export async function getSessionServer(): Promise<Session | null> {
  const { cookies } = await import("next/headers");
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;
  const userId = cookieStore.get("user_id")?.value;

  if (!accessToken) return null;

  return {
    accessToken,
    userId: userId ? parseInt(userId, 10) : undefined
  } as Session;
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
  if (session.userId) {
    cookieStore.set("user_id", session.userId.toString(), {
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
  cookieStore.set("user_id", "", {
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

export function getUserId(): number | null {
  if (typeof window !== 'undefined') {
    const userIdStr = localStorage.getItem('user_id');
    return userIdStr ? parseInt(userIdStr, 10) : null;
  }
  return null;
}

export function setAccessToken(token: string) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
}

export function setUserId(userId: number) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('user_id', userId.toString());
  }
}
