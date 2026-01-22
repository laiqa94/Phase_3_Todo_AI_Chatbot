import { NextResponse } from "next/server";

function baseUrl() {
  const url = process.env.API_BASE_URL;
  console.log("Environment variable API_BASE_URL:", url); // For debugging
  if (!url) {
    console.error("ERROR: API_BASE_URL environment variable is not set!");
    throw new Error("API_BASE_URL is not set");
  }
  return url;
}

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => null);

    console.log("Register called with body:", body);

    // Proxy to backend
    const backendUrl = `${baseUrl()}/api/v1/auth/register`;

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Backend error' }));
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Register error:", error);
    return NextResponse.json(
      { message: "Registration failed", error: String(error) },
      { status: 500 }
    );
  }
}