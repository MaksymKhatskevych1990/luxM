import type { HomePayload } from "./types";

function getServerApiUrl() {
  return (
    process.env.INTERNAL_API_URL?.replace(/\/$/, "") ||
    "http://127.0.0.1:8000/api"
  );
}

function getClientApiUrl() {
  // Same-origin `/api` works with Next rewrites + ngrok demo.
  return (
    process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
    "/api"
  );
}

export async function fetchHome(): Promise<HomePayload> {
  const res = await fetch(`${getServerApiUrl()}/home/`, {
    // Always get fresh CMS content (gallery, video, SEO) during local/dev.
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to load homepage data: ${res.status}`);
  }

  return res.json();
}

export async function submitLead(payload: {
  room_type: string;
  message: string;
  name: string;
  phone: string;
  email: string;
  telegram: string;
}) {
  const res = await fetch(`${getClientApiUrl()}/leads/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Не вдалося надіслати заявку");
  }

  return res.json();
}

export const API_URL = getClientApiUrl();
