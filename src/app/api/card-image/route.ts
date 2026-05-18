import { NextRequest, NextResponse } from "next/server";

const ALLOWED_IMAGE_HOSTS = new Set([
  "img.ultraman-cardgame.com",
  "api.ultraman-cardgame.com",
]);
const IMAGE_FETCH_RETRIES = 3;
const IMAGE_FETCH_RETRY_DELAY_MS = 250;
const IMAGE_FETCH_TIMEOUT_MS = 10000;

function sleep(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

async function fetchImageWithRetry(url: string) {
  let lastError: unknown;

  for (let attempt = 1; attempt <= IMAGE_FETCH_RETRIES; attempt += 1) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, IMAGE_FETCH_TIMEOUT_MS);

    try {
      return await fetch(url, {
        cache: "force-cache",
        signal: controller.signal,
      });
    } catch (error) {
      lastError = error;

      if (attempt === IMAGE_FETCH_RETRIES) {
        break;
      }

      await sleep(IMAGE_FETCH_RETRY_DELAY_MS * attempt);
    } finally {
      clearTimeout(timeoutId);
    }
  }

  throw lastError;
}

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

  let upstream: Response;
  try {
    upstream = await fetchImageWithRetry(targetUrl.toString());
  } catch (error) {
    console.error("Failed to proxy card image:", error);
    return NextResponse.json(
      { error: "Upstream image request failed" },
      { status: 502 }
    );
  }

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
