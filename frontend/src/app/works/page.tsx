import type { Metadata } from "next";
import Link from "next/link";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import WorksCatalog from "@/components/WorksCatalog";
import { SITE_URL } from "@/lib/site";
import { allWorks, loadHome, publishedCategories } from "@/lib/works";

const title = "Галерея робіт: кухні, шафи і гардероби в Дніпрі";
const description =
  "Фото кухонь, шаф і гардеробних на замовлення в Дніпрі. У кожній роботі видно планування, матеріали і кому підходить цей варіант.";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: "/works", languages: { uk: "/works" } },
  openGraph: {
    title: `${title} | ProProstir`,
    description,
    url: "/works",
    locale: "uk_UA",
    type: "website",
  },
};

export default async function WorksPage() {
  const data = await loadHome();
  const categories = publishedCategories(data.work_categories);
  const works = allWorks(data.work_categories);
  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Головна", item: SITE_URL },
          { "@type": "ListItem", position: 2, name: "Галерея робіт", item: `${SITE_URL}/works` },
        ],
      },
      {
        "@type": "ItemList",
        name: title,
        itemListElement: works.map((item, index) => ({
          "@type": "ListItem",
          position: index + 1,
          name: item.title,
          url: `${SITE_URL}/works/${item.slug}`,
        })),
      },
    ],
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      <Header settings={data.settings} navigation={data.navigation} />
      <main id="content" className="service-page">
        <div className="wrap">
          <nav className="service-crumbs" aria-label="Навігаційний ланцюжок">
            <Link href="/">Головна</Link>
            <span aria-hidden="true">/</span>
            <span>Галерея</span>
          </nav>
          <p className="label label--oak">Приклади робіт</p>
          <h1 className="font-serif work-page-title">Галерея робіт</h1>
          <p className="service-lead">{description}</p>
          <WorksCatalog categories={categories} />
        </div>
      </main>
      <Footer settings={data.settings} navigation={data.navigation} />
    </>
  );
}
