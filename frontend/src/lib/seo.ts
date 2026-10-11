import type { Metadata } from "next";
import type { SiteSettings } from "./types";
import { SITE_URL } from "./site";

function absUrl(pathOrUrl: string): string {
  if (!pathOrUrl) return SITE_URL;
  if (pathOrUrl.startsWith("http://") || pathOrUrl.startsWith("https://")) {
    return pathOrUrl;
  }
  const path = pathOrUrl.startsWith("/") ? pathOrUrl : `/${pathOrUrl}`;
  return `${SITE_URL}${path}`;
}

function csv(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function lines(value: string): string[] {
  return value
    .split(/\r?\n/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export function seoServices(settings: SiteSettings): string[] {
  return lines(settings.jsonld_services || "");
}

function robotsFromSettings(value: string | undefined): Metadata["robots"] {
  const raw = (value || "index, follow").toLowerCase();
  const index = !raw.includes("noindex");
  const follow = !raw.includes("nofollow");
  return {
    index,
    follow,
    googleBot: {
      index,
      follow,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  };
}

export function metadataFromSettings(settings: SiteSettings): Metadata {
  const title = settings.seo_title;
  const description = settings.seo_description;
  const ogTitle = settings.og_title || title;
  const ogDescription = settings.og_description || description;
  const twitterTitle = settings.twitter_title || ogTitle;
  const twitterDescription = settings.twitter_description || ogDescription;
  const image = settings.og_image_url;
  const imageAlt = settings.og_image_alt || ogTitle;
  const canonical = absUrl(settings.seo_canonical_path || "/");
  const author = settings.seo_author || settings.brand_name;
  const locale = settings.seo_locale || "uk_UA";
  const keywords = csv(settings.seo_keywords || "");

  return {
    title,
    description,
    keywords,
    authors: [{ name: author, url: SITE_URL }],
    creator: author,
    publisher: settings.jsonld_name || settings.brand_name,
    category: "home",
    robots: robotsFromSettings(settings.seo_robots),
    alternates: {
      canonical,
      languages: {
        [settings.seo_html_lang || "uk"]: canonical,
      },
    },
    openGraph: {
      type: (settings.og_type as "website") || "website",
      locale,
      url: canonical,
      siteName: settings.jsonld_name || settings.brand_name,
      title: ogTitle,
      description: ogDescription,
      ...(image
        ? {
            images: [
              {
                url: absUrl(image),
                alt: imageAlt,
              },
            ],
          }
        : {}),
    },
    twitter: {
      card: (settings.twitter_card as "summary_large_image") || "summary_large_image",
      title: twitterTitle,
      description: twitterDescription,
      ...(settings.twitter_site ? { site: settings.twitter_site } : {}),
      ...(image ? { images: [absUrl(image)] } : {}),
    },
    other: {
      ...(settings.seo_geo_region ? { "geo.region": settings.seo_geo_region } : {}),
      ...(settings.seo_geo_placename
        ? { "geo.placename": settings.seo_geo_placename }
        : {}),
    },
  };
}
