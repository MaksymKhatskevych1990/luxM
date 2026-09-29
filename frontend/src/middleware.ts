import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const USER = process.env.SITE_GATE_USER || "admin";
const PASSWORD = process.env.SITE_GATE_PASSWORD || "proprostir";

function authorized(request: NextRequest): boolean {
  const header = request.headers.get("authorization");
  if (!header?.startsWith("Basic ")) return false;
  try {
    const decoded = atob(header.slice(6));
    const separator = decoded.indexOf(":");
    if (separator < 0) return false;
    const user = decoded.slice(0, separator);
    const password = decoded.slice(separator + 1);
    return user === USER && password === PASSWORD;
  } catch {
    return false;
  }
}

export function middleware(request: NextRequest) {
  if (!authorized(request)) {
    return new NextResponse("Потрібен вхід", {
      status: 401,
      headers: {
        "WWW-Authenticate": 'Basic realm="proprostir", charset="UTF-8"',
        "X-Robots-Tag": "noindex, nofollow, noarchive",
        "Cache-Control": "no-store",
      },
    });
  }

  const response = NextResponse.next();
  response.headers.set("X-Robots-Tag", "noindex, nofollow, noarchive");
  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
