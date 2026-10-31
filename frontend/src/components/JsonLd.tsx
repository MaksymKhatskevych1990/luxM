import type { Project, SiteSettings } from "@/lib/types";
import { SITE_URL } from "@/lib/site";
import { seoServices } from "@/lib/seo";

type JsonLdProps = {
  settings: SiteSettings;
  projects?: Project[];
};

function profileUrl(url: string | undefined): string | null {
  const value = (url || "").trim();
  if (!value) return null;
  if (/^https?:\/\/(www\.)?(t\.me|telegram\.me)\/?$/i.test(value)) return null;
  if (/^https?:\/\/(www\.)?instagram\.com\/?$/i.test(value)) return null;
  return value;
}

function abs(pathOrUrl: string): string {
  if (!pathOrUrl) return SITE_URL;
  if (pathOrUrl.startsWith("http://") || pathOrUrl.startsWith("https://")) {
    return pathOrUrl;
  }
  const path = pathOrUrl.startsWith("/") ? pathOrUrl : `/${pathOrUrl}`;
  return `${SITE_URL}${path}`;
}

export default function JsonLd({ settings, projects = [] }: JsonLdProps) {
  const name = settings.jsonld_name || settings.brand_name;
  const description = settings.jsonld_description || settings.seo_description;
  const image = settings.og_image_url ? abs(settings.og_image_url) : undefined;
  const services = seoServices(settings);
  const canonical = abs(settings.seo_canonical_path || "/");
  const sameAs = [profileUrl(settings.instagram_url), profileUrl(settings.telegram_url)].filter(
    (value): value is string => Boolean(value),
  );
  const street = settings.jsonld_street?.trim() || "";
  const published = projects.filter((project) => project.is_published !== false);

  const alternateName = [settings.tagline].filter(
    (value, index, list) => Boolean(value) && value !== name && list.indexOf(value) === index,
  );

  const address = {
    "@type": "PostalAddress",
    ...(street ? { streetAddress: street } : {}),
    addressLocality: settings.jsonld_city,
    ...(settings.jsonld_city === "Дніпро" || settings.seo_geo_region === "UA-12"
      ? { addressRegion: "Дніпропетровська область" }
      : {}),
    addressCountry: settings.jsonld_country,
    ...(settings.jsonld_postal_code
      ? { postalCode: settings.jsonld_postal_code }
      : {}),
  };

  const geo =
    street && settings.jsonld_latitude && settings.jsonld_longitude
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
    ...(alternateName.length
      ? { alternateName: alternateName.length === 1 ? alternateName[0] : alternateName }
      : {}),
    description,
    url: SITE_URL,
    telephone: settings.phone,
    ...(settings.email ? { email: settings.email } : {}),
    image,
    logo: settings.header_logo_url ? abs(settings.header_logo_url) : image,
    address,
    ...(geo ? { geo } : {}),
    ...(settings.jsonld_opening_hours
      ? { openingHours: settings.jsonld_opening_hours }
      : {}),
    areaServed: settings.jsonld_area_served || settings.jsonld_city,
    ...(sameAs.length ? { sameAs } : {}),
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

  const work = published.length
    ? {
        "@context": "https://schema.org",
        "@type": "ItemList",
        name: "Вибрані роботи",
        itemListElement: published.slice(0, 8).map((project, index) => ({
          "@type": "ListItem",
          position: index + 1,
          name: project.seo_title || project.title,
          ...(project.seo_description || project.short_description
            ? { description: project.seo_description || project.short_description }
            : {}),
          ...(project.image_url ? { image: abs(project.image_url) } : {}),
        })),
      }
    : null;

  const graphs = [business, website, webpage, work].filter(Boolean);

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
