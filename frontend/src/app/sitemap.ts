import type { MetadataRoute } from "next";
import { services } from "@/lib/services";
import { SITE_URL } from "@/lib/site";
import { allWorks, loadHome } from "@/lib/works";

export const revalidate = 300;

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const home = await loadHome();
  const works = allWorks(home.work_categories);
  return [
    {
      url: SITE_URL,
      changeFrequency: "weekly",
      priority: 1,
    },
    {
      url: `${SITE_URL}/works`,
      changeFrequency: "weekly",
      priority: 0.8,
    },
    ...services.map((service) => ({
      url: `${SITE_URL}/${service.slug}`,
      changeFrequency: "monthly" as const,
      priority: 0.8,
    })),
    ...works.map((item) => ({
      url: `${SITE_URL}/works/${item.slug}`,
      changeFrequency: "monthly" as const,
      priority: 0.7,
    })),
  ];
}
