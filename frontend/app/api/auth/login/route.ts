import { NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => null);

    console.log("Mock login called with body:", body);

    // Mock successful login response
    const mockResponse = {
      accessToken: "mock-access-token-" + Date.now(),
      tokenType: "bearer",
      user: {
        id: Math.floor(Math.random() * 1000),
        email: body?.email || "test@example.com",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
    };

    // Set the access token cookie (this is what the real backend would do)
    const cookieStore = await cookies();
    if (mockResponse.accessToken) {
      cookieStore.set("access_token", mockResponse.accessToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
        maxAge: 30 * 60, // 30 minutes
      });
    }

    // Also set the user ID in cookies
    if (mockResponse.user?.id) {
      cookieStore.set("user_id", mockResponse.user.id.toString(), {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
        maxAge: 30 * 60, // 30 minutes
      });
    }

    return NextResponse.json(mockResponse);
  } catch (error) {
    console.error("Mock login error:", error);
    return NextResponse.json(
      { message: "Login would have failed in real backend", error: String(error) },
      { status: 500 }
    );
  }
}