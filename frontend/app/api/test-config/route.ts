import { NextResponse } from "next/server";

export async function GET() {
  const apiUrl = process.env.API_BASE_URL;

  console.log("Testing API_BASE_URL configuration:");
  console.log("API_BASE_URL:", apiUrl);
  console.log("typeof API_BASE_URL:", typeof apiUrl);
  console.log("Is API_BASE_URL falsy?", !apiUrl);

  return NextResponse.json({
    apiBaseUrl: apiUrl,
    isSet: !!apiUrl,
    type: typeof apiUrl,
    timestamp: new Date().toISOString()
  });
}