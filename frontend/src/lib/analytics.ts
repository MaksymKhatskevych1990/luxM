export type AnalyticsEvent =
  | "generate_lead"
  | "phone_click"
  | "whatsapp_click"
  | "telegram_click"
  | "email_click"
  | "enquiry_cta_click";

type Gtag = (command: "event" | "js" | "config", ...args: unknown[]) => void;

declare global {
  interface Window {
    gtag?: Gtag;
    dataLayer?: unknown[];
  }
}

const SAFE_PARAMS = new Set(["link_location", "room_type", "form_id"]);

export function analyticsId(): string {
  return (process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID || "").trim();
}

export function analyticsEnabled(): boolean {
  return /^G-[A-Z0-9]+$/i.test(analyticsId());
}

/** Events fire only when the owner sets NEXT_PUBLIC_GA_MEASUREMENT_ID. No personal data. */
export function trackEvent(
  name: AnalyticsEvent,
  params?: Record<string, string | undefined>,
) {
  if (typeof window === "undefined" || !analyticsEnabled()) return;
  if (typeof window.gtag !== "function") return;

  const safe: Record<string, string> = {};
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (!value || !SAFE_PARAMS.has(key)) continue;
      safe[key] = value.slice(0, 80);
    }
  }
  window.gtag("event", name, safe);
}

export function trackHref(href: string, location: string) {
  const value = href.trim().toLowerCase();
  if (value.startsWith("tel:")) {
    trackEvent("phone_click", { link_location: location });
    return;
  }
  if (value.startsWith("mailto:")) {
    trackEvent("email_click", { link_location: location });
    return;
  }
  if (value.includes("wa.me")) {
    trackEvent("whatsapp_click", { link_location: location });
    return;
  }
  if (value.includes("t.me/") || value.includes("telegram")) {
    trackEvent("telegram_click", { link_location: location });
  }
}
