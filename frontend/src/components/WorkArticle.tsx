import Link from "next/link";
import type { NavItem, SiteSettings, WorkCategory, WorkItem } from "@/lib/types";
import { SITE_URL } from "@/lib/site";
import { telHref } from "@/lib/phone";
import { absoluteUrl, serviceForCategory, workHref, workPageTitle } from "@/lib/works";
import Header from "./Header";
import Footer from "./Footer";
import OutboundLink from "./OutboundLink";

type WorkArticleProps = {
  item: WorkItem;
  category: WorkCategory;
  related: WorkItem[];
  settings: SiteSettings;
  navigation: NavItem[];
};

export default function WorkArticle({
  item,
  category,
  related,
  settings,
  navigation,
}: WorkArticleProps) {
  const pageUrl = `${SITE_URL}${workHref(item.slug)}`;
  const service = serviceForCategory(category.slug);
  const phoneHref = telHref(settings.phone);
  const enquiryText = settings.header_cta_text || "Замовити прорахунок";
  const photos = item.gallery?.filter((photo) => photo.url).length
    ? [...item.gallery].filter((photo) => photo.url).sort((a, b) => a.order - b.order)
    : item.image_url
      ? [{ id: item.id, url: item.image_url, caption: item.title, order: 0 }]
      : [];

  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Головна", item: SITE_URL },
          { "@type": "ListItem", position: 2, name: "Галерея робіт", item: `${SITE_URL}/works` },
          {
            "@type": "ListItem",
            position: 3,
            name: category.name,
            item: `${SITE_URL}/works#${category.slug}`,
          },
          { "@type": "ListItem", position: 4, name: item.title, item: pageUrl },
        ],
      },
      {
        "@type": "WebPage",
        name: workPageTitle(item),
        description: item.summary || item.description,
        url: pageUrl,
        inLanguage: "uk",
        primaryImageOfPage: absoluteUrl(photos[0]?.url || ""),
        about: item.title,
        isPartOf: { "@type": "WebSite", name: settings.brand_name, url: SITE_URL },
      },
    ],
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      <Header settings={settings} navigation={navigation} />
      <main id="content" className="service-page">
        <article className="wrap">
          <nav className="service-crumbs" aria-label="Навігаційний ланцюжок">
            <Link href="/">Головна</Link>
            <span aria-hidden="true">/</span>
            <Link href="/works">Галерея</Link>
            <span aria-hidden="true">/</span>
            <Link href={`/works#${category.slug}`}>{category.name}</Link>
            <span aria-hidden="true">/</span>
            <span>{item.title}</span>
          </nav>
          <p className="label label--oak">{category.name}</p>
          <h1 className="font-serif work-page-title">{item.title}</h1>
          {item.summary ? <p className="service-lead">{item.summary}</p> : null}
          <div className="service-actions">
            <OutboundLink className="btn-primary" href={phoneHref} location="work">
              {settings.phone}
            </OutboundLink>
            <OutboundLink
              className="btn-ghost"
              href="/#contacts"
              location="work"
              eventName="enquiry_cta_click"
            >
              {enquiryText}
            </OutboundLink>
          </div>

          {photos.length > 0 ? (
            <div className="work-page-photos">
              {photos.map((photo, index) => (
                <figure key={photo.id} className="work-page-figure">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={photo.url}
                    alt={photo.caption || item.title}
                    loading={index === 0 ? "eager" : "lazy"}
                    decoding="async"
                    fetchPriority={index === 0 ? "high" : "low"}
                  />
                  {photo.caption ? <figcaption>{photo.caption}</figcaption> : null}
                </figure>
              ))}
            </div>
          ) : null}

          {item.description ? <div className="work-page-body">{item.description}</div> : null}

          {service ? (
            <p className="work-page-service">
              <Link href={`/${service.slug}`}>{service.h1}</Link>
            </p>
          ) : null}

          {related.length > 0 ? (
            <section className="service-more" aria-labelledby="related-works">
              <h2 id="related-works" className="font-serif">
                Інші {category.name.toLowerCase()}
              </h2>
              <ul>
                {related.map((entry) => (
                  <li key={entry.slug}>
                    <Link href={workHref(entry.slug)}>{entry.title}</Link>
                    {entry.summary ? <p>{entry.summary}</p> : null}
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
        </article>
      </main>
      <Footer settings={settings} navigation={navigation} />
    </>
  );
}
