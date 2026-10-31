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

export function workPageTitle(item: WorkItem): string {
  return `${item.title} на замовлення в Дніпрі`;
}

export function workMetaDescription(item: WorkItem): string {
  const source = (item.summary || item.description || item.title).replace(/\s+/g, " ").trim();
  const withCity = /дніпр/i.test(source) ? source : `${source} Прорахунок і збірка в Дніпрі.`;
  if (withCity.length <= 170) return withCity;
  return `${withCity.slice(0, 167).trim()}…`;
}

export async function loadHome(): Promise<HomePayload> {
  try {
    return await fetchHome();
  } catch {
    return fallbackHome;
  }
}
