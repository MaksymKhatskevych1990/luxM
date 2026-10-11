import type { PageSection, Project, SiteSettings } from "@/lib/types";
import { SITE_URL } from "@/lib/site";
import { seoServices } from "@/lib/seo";

type JsonLdProps = {
  settings: SiteSettings;
  projects?: Project[];
  sections?: PageSection[];
};

function abs(pathOrUrl: string): string {
  if (!pathOrUrl) return SITE_URL;
  if (pathOrUrl.startsWith("http://") || pathOrUrl.startsWith("https://")) {
    return pathOrUrl;
  }
  const path = pathOrUrl.startsWith("/") ? pathOrUrl : `/${pathOrUrl}`;
  return `${SITE_URL}${path}`;
}

export default function JsonLd({ settings, projects = [], sections = [] }: JsonLdProps) {
  const name = settings.jsonld_name || settings.brand_name;
  const description = settings.jsonld_description || settings.seo_description;
  const image = settings.og_image_url ? abs(settings.og_image_url) : undefined;
  const services = seoServices(settings);
  const canonical = abs(settings.seo_canonical_path || "/");
  const sameAs = [
    settings.instagram_url,
    settings.telegram_url,
    settings.whatsapp_url,
  ].filter(Boolean);
  const street = settings.jsonld_street?.trim() || "";
  const published = projects.filter((project) => project.is_published !== false);

  const address = {
    "@type": "PostalAddress",
    ...(street ? { streetAddress: street } : {}),
    addressLocality: settings.jsonld_city,
    addressCountry: settings.jsonld_country,
    ...(settings.jsonld_postal_code
      ? { postalCode: settings.jsonld_postal_code }
      : {}),
  };

  const geo =
    settings.jsonld_latitude && settings.jsonld_longitude
      ? {
          "@type": "GeoCoordinates",
          latitude: settings.jsonld_latitude,
          longitude: settings.jsonld_longitude,
        }
      : undefined;

  const business = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", settings.jsonld_type || "FurnitureStore"],
    "@id": `${SITE_URL}/#business`,
    name,
    alternateName: settings.brand_name,
    description,
    url: SITE_URL,
    telephone: settings.phone,
    email: settings.email,
    priceRange: settings.jsonld_price_range,
    image,
    logo: settings.header_logo_url ? abs(settings.header_logo_url) : image,
    address,
    ...(geo ? { geo } : {}),
    ...(settings.jsonld_opening_hours
      ? { openingHours: settings.jsonld_opening_hours }
      : {}),
    areaServed: settings.jsonld_area_served || settings.jsonld_city,
    sameAs,
    ...(services.length
      ? {
          hasOfferCatalog: {
            "@type": "OfferCatalog",
            name: settings.footer_services_heading || "Послуги",
            itemListElement: services.map((service, index) => ({
              "@type": "Offer",
              itemOffered: {
                "@type": "Service",
                name: service,
              },
              position: index + 1,
            })),
          },
          knowsAbout: services,
        }
      : {}),
  };

  const website = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": `${SITE_URL}/#website`,
    name,
    url: SITE_URL,
    description,
    inLanguage: settings.seo_html_lang || "uk",
    publisher: { "@id": `${SITE_URL}/#business` },
  };

  const webpage = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": `${canonical}#webpage`,
    url: canonical,
    name: settings.seo_title,
    description: settings.seo_description,
    inLanguage: settings.seo_html_lang || "uk",
    isPartOf: { "@id": `${SITE_URL}/#website` },
    about: { "@id": `${SITE_URL}/#business` },
    primaryImageOfPage: image,
  };

  const breadcrumbs = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      {
        "@type": "ListItem",
        position: 1,
        name: name,
        item: SITE_URL,
      },
      ...sections
        .filter((section) => section.is_visible !== false && section.section_id)
        .map((section, index) => ({
          "@type": "ListItem",
          position: index + 2,
          name: section.title || section.eyebrow || section.section_id,
          item: `${SITE_URL}/#${section.section_id}`,
        })),
    ],
  };

  const work = published.length
    ? {
        "@context": "https://schema.org",
        "@type": "ItemList",
        name: "Проєкти",
        itemListElement: published.slice(0, 8).map((project, index) => ({
          "@type": "ListItem",
          position: index + 1,
          name: project.seo_title || project.title,
          description: project.seo_description || project.short_description,
          url: `${SITE_URL}/#projects`,
          image: project.image_url ? abs(project.image_url) : undefined,
        })),
      }
    : null;

  const graphs = [business, website, webpage, breadcrumbs, work].filter(Boolean);

  return (
    <>
      {graphs.map((node, index) => (
        <script
          key={index}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(node) }}
        />
      ))}
    </>
  );
}
