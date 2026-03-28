import { NextRequest, NextResponse } from "next/server";
import {
  ADMIN_SESSION_COOKIE,
  isValidAdminSession,
} from "@/lib/admin-auth";

export async function middleware(req: NextRequest) {
  const session = req.cookies.get(ADMIN_SESSION_COOKIE)?.value;

  if (await isValidAdminSession(session)) {
    return NextResponse.next();
  }

  return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
}

export const config = {
  matcher: ["/api/admin/import-cards"],
};
