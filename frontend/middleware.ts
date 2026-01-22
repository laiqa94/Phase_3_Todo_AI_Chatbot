import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

const SESSION_COOKIE = "access_token";

export function middleware(req: NextRequest) {
  const session = req.cookies.get(SESSION_COOKIE)?.value;
  const pathname = req.nextUrl.pathname;

  // Allow access to public routes without authentication
  if (pathname === '/login' || pathname === '/register' || pathname === '/') {
    return NextResponse.next();
  }

  // If user has a session, let them proceed
  if (session) {
    return NextResponse.next();
  }

  // If no session and on a protected route, redirect to login
  // Store the original path so user can be redirected back after login
  const nextUrl = req.nextUrl.clone();
  nextUrl.pathname = "/login";
  nextUrl.searchParams.set("next", req.nextUrl.pathname + req.nextUrl.search);
  return NextResponse.redirect(nextUrl);
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico|login|register|_vercel).*)'],
};
