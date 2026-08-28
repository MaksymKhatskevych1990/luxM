import type { HomePayload } from "./types";

function getApiUrl() {
  // Prefer internal URL for SSR inside Docker network.
  const internal = process.env.INTERNAL_API_URL?.replace(/\/$/, "");
  if (internal) return internal;
  return (
    process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
    "http://localhost:8000/api"
  );
}

export async function fetchHome(): Promise<HomePayload> {
  const res = await fetch(`${getApiUrl()}/home/`, {
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
  const clientApi =
    process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
    "http://localhost:8000/api";
  const res = await fetch(`${clientApi}/leads/`, {
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

export const API_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
  "http://localhost:8000/api";
