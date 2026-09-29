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

function leadErrorMessage(data: unknown): string {
  if (!data || typeof data !== "object") return "Не вдалося надіслати заявку";
  const record = data as Record<string, unknown>;
  if (typeof record.detail === "string" && record.detail) return record.detail;
  for (const value of Object.values(record)) {
    if (typeof value === "string" && value) return value;
    if (Array.isArray(value) && typeof value[0] === "string") return value[0];
  }
  return "Не вдалося надіслати заявку";
}

export async function submitLead(payload: {
  room_type: string;
  message: string;
  name: string;
  phone: string;
  email: string;
  telegram: string;
  attachment?: File | null;
}) {
  const body = new FormData();
  body.append("room_type", payload.room_type);
  body.append("message", payload.message);
  body.append("name", payload.name);
  body.append("phone", payload.phone);
  body.append("email", payload.email);
  body.append("telegram", payload.telegram);
  if (payload.attachment) {
    body.append("attachment", payload.attachment);
  }

  const res = await fetch(`${getClientApiUrl()}/leads/`, {
    method: "POST",
    body,
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(leadErrorMessage(data));
  }

  return res.json();
}

export const API_URL = getClientApiUrl();
