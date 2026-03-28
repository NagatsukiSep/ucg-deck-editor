import { NextRequest } from "next/server";

export function hasValidOrigin(req: NextRequest): boolean {
  const origin = req.headers.get("origin");
  return origin === req.nextUrl.origin;
}
