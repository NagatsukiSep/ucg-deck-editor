import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.API_BASE_URL as string;
const API_PUBLIC_KEY = process.env.API_PUBLIC_KEY as string;
const API_SECRET_KEY = process.env.API_SECRET_KEY as string;

export async function GET(req: NextRequest, { params }: { params: { path: string[] } }) {
  const searchParams = req.nextUrl.searchParams.toString(); 
  const path = params.path; 

  const response = await fetch(`${API_BASE_URL}/${path}?${searchParams}`, {
    method: "GET",
    headers: {
      Authorization: `Basic ${Buffer.from(`${API_PUBLIC_KEY}:${API_SECRET_KEY}`).toString("base64")}`,
    },
  });

  if (!response.ok) {
    return NextResponse.json({ error: "Failed to fetch data" }, { status: response.status });
  }

  const data = await response.json();
  return NextResponse.json(data);
}

export async function POST(req: NextRequest, { params }: { params: { path: string[] } }) {
  const body = await req.json();
  const path = params.path;

  const response = await fetch(`${API_BASE_URL}/${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Basic ${Buffer.from(`${API_PUBLIC_KEY}:${API_SECRET_KEY}`).toString("base64")}`,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    return NextResponse.json({ error: "Failed to post data" }, { status: response.status });
  }

  const data = await response.json();
  return NextResponse.json(data);
}
