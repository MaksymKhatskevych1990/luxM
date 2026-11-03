import { fetchHome } from "./api";
import { fallbackHome } from "./fallback";
import { getService, type ServicePageData } from "./services";
import { SITE_URL } from "./site";
import type { HomePayload, WorkCategory, WorkItem } from "./types";

const CATEGORY_SERVICE: Record<string, string> = {
  kitchens: "kuhni-na-zamovlennya",
  cabinets: "shafy-na-zamovlennya",
  wardrobes: "garderobni-na-zamovlennya",
};

export function workHref(slug: string): string {
  return `/works/${slug}`;
}

export function absoluteUrl(url: string): string {
  if (!url) return "";
  if (url.startsWith("http://") || url.startsWith("https://")) return url;
  return `${SITE_URL}${url.startsWith("/") ? url : `/${url}`}`;
}

export function publishedCategories(categories: WorkCategory[] | undefined): WorkCategory[] {
  return [...(categories || [])]
    .map((category) => ({
      ...category,
      items: [...(category.items || [])]
        .filter((item) => item.slug && item.title)
        .sort((a, b) => a.order - b.order),
    }))
    .filter((category) => category.items.length > 0)
    .sort((a, b) => a.order - b.order);
}

export function allWorks(categories: WorkCategory[] | undefined): WorkItem[] {
  return publishedCategories(categories).flatMap((category) => category.items);
}

export function findWork(
  categories: WorkCategory[] | undefined,
  slug: string,
): { category: WorkCategory; item: WorkItem } | null {
  for (const category of publishedCategories(categories)) {
    const item = category.items.find((entry) => entry.slug === slug);
    if (item) return { category, item };
  }
  return null;
}

export function serviceForCategory(categorySlug: string): ServicePageData | undefined {
  const serviceSlug = CATEGORY_SERVICE[categorySlug];
  return serviceSlug ? getService(serviceSlug) : undefined;
}

export function worksForService(
  categories: WorkCategory[] | undefined,
  serviceSlug: string,
): WorkItem[] {
  return publishedCategories(categories)
    .filter((category) => CATEGORY_SERVICE[category.slug] === serviceSlug)
    .flatMap((category) => category.items);
}

const TITLE_BRAND = " | ProProstir";
const TITLE_LIMIT = 60;

export function workPageTitle(item: WorkItem): string {
  const withOrder = `${item.title} на замовлення в Дніпрі`;
  if (withOrder.length + TITLE_BRAND.length <= TITLE_LIMIT) return withOrder;
  const withCity = `${item.title} в Дніпрі`;
  if (withCity.length + TITLE_BRAND.length <= TITLE_LIMIT) return withCity;
  const room = TITLE_LIMIT - TITLE_BRAND.length;
  if (item.title.length <= room) return item.title;
  return `${item.title.slice(0, room - 1).trim()}…`;
}

function metaSentences(item: WorkItem): string[] {
  const raw = `${item.summary || ""} ${item.description || ""}`.trim() || item.title;
  return raw
    .replace(/Тонкощі цього варіанту:\s*/gi, " ")
    .replace(/—/g, " ")
    .replace(/\s+/g, " ")
    .split(/(?<=[.!?])\s+/)
    .map((sentence) => sentence.trim())
    .filter(Boolean);
}

export function workMetaDescription(item: WorkItem): string {
  const sentences = metaSentences(item);
  let text = "";
  let clipped = false;
  for (const sentence of sentences) {
    const next = text ? `${text} ${sentence}` : sentence;
    if (next.length <= 160) {
      text = next;
      if (text.length >= 120) break;
      continue;
    }
    if (text.length >= 120) break;
    const room = 157 - text.length - (text ? 1 : 0);
    if (room >= 25) {
      const slice = sentence.slice(0, room).replace(/\s+\S*$/, "").trim();
      text = `${text}${text ? " " : ""}${slice || sentence.slice(0, room).trim()}…`;
      clipped = true;
    }
    break;
  }
  if (!clipped && text.length <= 148 && !/дніпр/i.test(text)) {
    text = `${text} У Дніпрі.`.trim();
  }
  if (text.length > 160) return `${text.slice(0, 157).trim()}…`;
  return text || item.title;
}

export async function loadHome(): Promise<HomePayload> {
  try {
    return await fetchHome();
  } catch {
    return fallbackHome;
  }
}
