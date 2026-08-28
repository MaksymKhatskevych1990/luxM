import type { NavItem, PageSection } from "./types";

export function getSection(
  sections: PageSection[],
  key: string,
): PageSection | undefined {
  return sections.find((section) => section.key === key);
}

export function navByLocation(nav: NavItem[], location: string): NavItem[] {
  return nav
    .filter((item) => item.location === location && item.is_visible !== false)
    .sort((a, b) => a.order - b.order);
}
