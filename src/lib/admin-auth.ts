export const ADMIN_SESSION_COOKIE = "admin_session";

const SESSION_TTL_SECONDS = 60 * 60 * 8;

type SessionPayload = {
  exp: number;
  role: "admin";
};

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing environment variable: ${name}`);
  }
  return value;
}

function requireAdminToken(): string {
  return requireEnv("ADMIN_IMPORT_TOKEN");
}

function requireSessionSecret(): string {
  return requireEnv("ADMIN_SESSION_SECRET");
}

function encodeBase64Url(input: string): string {
  return btoa(input).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function decodeBase64Url(input: string): string {
  const normalized = input.replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized + "=".repeat((4 - (normalized.length % 4)) % 4);
  return atob(padded);
}

async function signValue(value: string): Promise<string> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(requireSessionSecret()),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );

  const signature = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(value)
  );

  const signatureBytes = new Uint8Array(signature);
  const binary = String.fromCharCode(...signatureBytes);
  return encodeBase64Url(binary);
}

async function verifySignature(value: string, signature: string): Promise<boolean> {
  const expected = await signValue(value);
  return expected === signature;
}

export function verifyAdminPassword(password: string): boolean {
  return password === requireAdminToken();
}

export async function createAdminSessionValue(): Promise<string> {
  const payload: SessionPayload = {
    role: "admin",
    exp: Math.floor(Date.now() / 1000) + SESSION_TTL_SECONDS,
  };

  const encodedPayload = encodeBase64Url(JSON.stringify(payload));
  const signature = await signValue(encodedPayload);
  return `${encodedPayload}.${signature}`;
}

export async function isValidAdminSession(
  sessionValue: string | undefined
): Promise<boolean> {
  if (!sessionValue) {
    return false;
  }

  const [encodedPayload, signature] = sessionValue.split(".");
  if (!encodedPayload || !signature) {
    return false;
  }

  if (!(await verifySignature(encodedPayload, signature))) {
    return false;
  }

  try {
    const payload = JSON.parse(decodeBase64Url(encodedPayload)) as SessionPayload;
    return (
      payload.role === "admin" &&
      typeof payload.exp === "number" &&
      payload.exp > Math.floor(Date.now() / 1000)
    );
  } catch {
    return false;
  }
}
