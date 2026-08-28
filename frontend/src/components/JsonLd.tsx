import type { SiteSettings } from "@/lib/types";
import { SITE_URL } from "@/lib/site";

type JsonLdProps = {
  settings: SiteSettings;
};

export default function JsonLd({ settings }: JsonLdProps) {
  const data = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "FurnitureStore"],
    name: settings.brand_name,
    description: settings.seo_description,
    url: SITE_URL,
    telephone: settings.phone,
    email: settings.email,
    foundingDate: String(settings.founded_year),
    priceRange: settings.jsonld_price_range,
    address: {
      "@type": "PostalAddress",
      streetAddress: settings.address,
      addressLocality: settings.jsonld_city,
      addressCountry: settings.jsonld_country,
    },
    areaServed: {
      "@type": "City",
      name: settings.jsonld_city,
    },
    sameAs: [settings.instagram_url, settings.telegram_url].filter(Boolean),
    ...(settings.og_image_url ? { image: settings.og_image_url } : {}),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
