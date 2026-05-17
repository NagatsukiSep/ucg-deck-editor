import { NextRequest, NextResponse } from "next/server";

const ALLOWED_IMAGE_HOSTS = new Set([
  "img.ultraman-cardgame.com",
  "api.ultraman-cardgame.com",
]);

export async function GET(req: NextRequest) {
  const src = req.nextUrl.searchParams.get("src");

  if (!src) {
    return NextResponse.json({ error: "Missing src" }, { status: 400 });
  }

  let targetUrl: URL;
  try {
    targetUrl = new URL(src);
  } catch {
    return NextResponse.json({ error: "Invalid src" }, { status: 400 });
  }

  if (targetUrl.protocol !== "https:" || !ALLOWED_IMAGE_HOSTS.has(targetUrl.hostname)) {
    return NextResponse.json({ error: "Unsupported src" }, { status: 400 });
  }

  const upstream = await fetch(targetUrl.toString(), {
    cache: "force-cache",
  });

  if (!upstream.ok) {
    return NextResponse.json(
      { error: `Upstream image request failed with status ${upstream.status}` },
      { status: upstream.status }
    );
  }

  const contentType = upstream.headers.get("content-type") ?? "application/octet-stream";
  const cacheControl = upstream.headers.get("cache-control") ?? "public, max-age=86400";
  const body = await upstream.arrayBuffer();

  return new NextResponse(body, {
    headers: {
      "Content-Type": contentType,
      "Cache-Control": cacheControl,
    },
  });
}
