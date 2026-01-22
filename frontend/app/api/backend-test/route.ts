import { NextResponse } from "next/server";

export async function GET() {
  try {
    // Test if we can reach the backend root
    const response = await fetch('https://laiqakhan-backend.hf.space/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      }
    });

    console.log(`Backend root status: ${response.status}`);

    if (response.ok) {
      // Try to reach the specific auth endpoint
      const authResponse = await fetch('https://laiqakhan-backend.hf.space/api/v1/auth/register', {
        method: 'OPTIONS', // Try OPTIONS first to check if endpoint exists
        headers: {
          'Accept': 'application/json',
        }
      });

      console.log(`Auth endpoint status: ${authResponse.status}`);

      return NextResponse.json({
        backendAccessible: true,
        rootStatus: response.status,
        authEndpointStatus: authResponse.status,
        message: "Backend is accessible"
      });
    } else {
      return NextResponse.json({
        backendAccessible: false,
        rootStatus: response.status,
        error: "Could not reach backend root"
      }, { status: 500 });
    }
  } catch (error) {
    console.error("Backend connectivity error:", error);
    return NextResponse.json({
      backendAccessible: false,
      error: error instanceof Error ? error.message : String(error),
      message: "Failed to connect to backend"
    }, { status: 500 });
  }
}