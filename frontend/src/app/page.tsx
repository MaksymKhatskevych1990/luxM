import type { Metadata } from "next";
import { fetchHome } from "@/lib/api";
import { fallbackHome } from "@/lib/fallback";
import { SITE_URL } from "@/lib/site";
import Site from "@/components/Site";
import type { SiteSettings } from "@/lib/types";

function metadataFromSettings(settings: SiteSettings): Metadata {
  const keywords = settings.seo_keywords
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);

  return {
    title: settings.seo_title,
    description: settings.seo_description,
    keywords,
    authors: [{ name: settings.brand_name }],
    creator: settings.brand_name,
    openGraph: {
      type: "website",
      locale: "uk_UA",
      url: SITE_URL,
      siteName: settings.brand_name,
      title: settings.seo_title,
      description: settings.seo_description,
      ...(settings.og_image_url
        ? { images: [{ url: settings.og_image_url }] }
        : {}),
    },
    twitter: {
      card: "summary_large_image",
      title: settings.seo_title,
      description: settings.seo_description,
      ...(settings.og_image_url ? { images: [settings.og_image_url] } : {}),
    },
  };
}

export async function generateMetadata(): Promise<Metadata> {
  try {
    const data = await fetchHome();
    return metadataFromSettings(data.settings);
  } catch {
    return metadataFromSettings(fallbackHome.settings);
  }
}

export default async function HomePage() {
  let data = fallbackHome;

  try {
    data = await fetchHome();
  } catch {
    data = fallbackHome;
  }

  return <Site data={data} />;
}
