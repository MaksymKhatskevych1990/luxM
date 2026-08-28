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
    priceRange: "$$$",
    address: {
      "@type": "PostalAddress",
      streetAddress: settings.address,
      addressLocality: "Київ",
      addressCountry: "UA",
    },
    areaServed: {
      "@type": "City",
      name: "Київ",
    },
    sameAs: [settings.instagram_url, settings.telegram_url].filter(Boolean),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
