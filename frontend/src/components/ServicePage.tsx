import Link from "next/link";
import type { NavItem, SiteSettings, WorkItem } from "@/lib/types";
import { services, type ServicePageData } from "@/lib/services";
import { SITE_URL } from "@/lib/site";
import { telHref } from "@/lib/phone";
import Header from "./Header";
import Footer from "./Footer";
import OutboundLink from "./OutboundLink";

type ServicePageProps = {
  service: ServicePageData;
  settings: SiteSettings;
  navigation: NavItem[];
  examples?: WorkItem[];
};

export default function ServicePage({
  service,
  settings,
  navigation,
  examples = [],
}: ServicePageProps) {
  const phoneHref = telHref(settings.phone);
  const enquiryText = settings.header_cta_text || "Замовити прорахунок";
  const others = services.filter((item) => item.slug !== service.slug);
  const pageUrl = `${SITE_URL}/${service.slug}`;

  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Головна", item: SITE_URL },
          { "@type": "ListItem", position: 2, name: service.h1, item: pageUrl },
        ],
      },
      {
        "@type": "Service",
        name: service.h1,
        serviceType: service.navLabel,
        description: service.description,
        url: pageUrl,
        areaServed: settings.jsonld_area_served || settings.jsonld_city || "Дніпро",
        provider: {
          "@type": "FurnitureStore",
          name: settings.brand_name,
          telephone: settings.phone,
          url: SITE_URL,
          address: {
            "@type": "PostalAddress",
            addressLocality: settings.jsonld_city || "Дніпро",
            ...(settings.jsonld_city === "Дніпро" || settings.seo_geo_region === "UA-12"
              ? { addressRegion: "Дніпропетровська область" }
              : {}),
            addressCountry: settings.jsonld_country || "UA",
          },
        },
      },
      {
        "@type": "FAQPage",
        mainEntity: service.faqs.map((faq) => ({
          "@type": "Question",
          name: faq.question,
          acceptedAnswer: { "@type": "Answer", text: faq.answer },
        })),
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
            <span>{service.navLabel}</span>
          </nav>
          <p className="label label--oak">{service.eyebrow}</p>
          <h1 className="font-serif service-title">{service.h1}</h1>
          <p className="service-lead">{service.lead}</p>
          <div className="service-actions">
            <OutboundLink className="btn-primary" href={phoneHref} location="service">
              {settings.phone}
            </OutboundLink>
            <OutboundLink
              className="btn-ghost"
              href="/#contacts"
              location="service"
              eventName="enquiry_cta_click"
            >
              {enquiryText}
            </OutboundLink>
          </div>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            className="service-photo"
            src={service.image}
            alt={service.imageAlt}
            fetchPriority="high"
            decoding="async"
          />

          <ul className="service-points">
            {service.points.map((point) => (
              <li key={point.title}>
                <h2 className="font-serif">{point.title}</h2>
                <p>{point.text}</p>
              </li>
            ))}
          </ul>

          <section className="service-steps" aria-labelledby="service-steps-title">
            <h2 id="service-steps-title" className="font-serif">
              Як це замовити
            </h2>
            <ol>
              {service.steps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>
          </section>

          <section className="service-faq" aria-labelledby="service-faq-title">
            <h2 id="service-faq-title" className="font-serif">
              Питання перед замовленням
            </h2>
            {service.faqs.map((faq) => (
              <details key={faq.question}>
                <summary>{faq.question}</summary>
                <p>{faq.answer}</p>
              </details>
            ))}
          </section>

          {examples.length > 0 ? (
            <section className="service-more" aria-labelledby="service-examples-title">
              <h2 id="service-examples-title" className="font-serif">
                Приклади: {service.navLabel.toLowerCase()}
              </h2>
              <ul>
                {examples.map((item) => (
                  <li key={item.slug}>
                    <Link href={`/works/${item.slug}`}>{item.title}</Link>
                    {item.summary ? <p>{item.summary}</p> : null}
                  </li>
                ))}
              </ul>
            </section>
          ) : null}

          <section className="service-more" aria-labelledby="service-more-title">
            <h2 id="service-more-title" className="font-serif">
              Інші меблі на замовлення
            </h2>
            <ul>
              {others.map((item) => (
                <li key={item.slug}>
                  <Link href={`/${item.slug}`}>{item.h1}</Link>
                </li>
              ))}
              <li>
                <Link href="/">Меблі на замовлення в Дніпрі</Link>
              </li>
            </ul>
          </section>
        </article>
      </main>
      <Footer settings={settings} navigation={navigation} />
    </>
  );
}
