import { cookies } from "next/headers";
import { AdminPageClient } from "@/components/admin/admin-page-client";
import {
  ADMIN_SESSION_COOKIE,
  isValidAdminSession,
} from "@/lib/admin-auth";

export default async function AdminPage() {
  const cookieStore = await cookies();
  const session = cookieStore.get(ADMIN_SESSION_COOKIE)?.value;

  return <AdminPageClient authenticated={await isValidAdminSession(session)} />;
}
