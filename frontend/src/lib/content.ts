import type { NavItem, PageSection } from "./types";

export function getSection(
  sections: PageSection[],
  key: string,
): PageSection | undefined {
  return sections.find((section) => section.key === key);
}

/** Hash links from the CMS point at the homepage sections. */
export function homeHref(href: string): string {
  if (!href) return "/";
  if (href.startsWith("#")) return `/${href}`;
  return href;
}

export function navByLocation(nav: NavItem[], location: string): NavItem[] {
  return nav
    .filter((item) => item.location === location && item.is_visible !== false)
    .sort((a, b) => a.order - b.order);
}
