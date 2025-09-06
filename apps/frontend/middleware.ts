import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const csp = "default-src 'self'; object-src 'none'; frame-ancestors 'none'";

export function middleware(_req: NextRequest) {
  const res = NextResponse.next();
  res.headers.set('Content-Security-Policy', csp);
  res.headers.set('X-Frame-Options', 'DENY');
  res.headers.set('X-Content-Type-Options', 'nosniff');
  res.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.headers.set('Permissions-Policy', 'geolocation=()');
  return res;
}

export const config = {
  matcher: '/:path*',
};
