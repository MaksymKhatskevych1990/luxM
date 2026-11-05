import Link from "next/link";
import type { WorkCategory } from "@/lib/types";
import { workHref } from "@/lib/works";

type WorksCatalogProps = {
  categories: WorkCategory[];
};

export default function WorksCatalog({ categories }: WorksCatalogProps) {
  return (
    <div className="works-catalog">
      {categories.map((category) => (
        <section key={category.slug} id={category.slug} aria-labelledby={`works-${category.slug}`}>
          <h2 id={`works-${category.slug}`} className="font-serif">
            {category.name}
          </h2>
          {category.description ? <p className="work-category-note">{category.description}</p> : null}
          <div className="work-grid">
            {category.items.map((item) => (
              <Link key={item.slug} href={workHref(item.slug)} className="proj-card work-card">
                <div className="work-card-media">
                  {item.image_url ? (
                    // Real photo URL in HTML, not only a client carousel.
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={item.image_url}
                      alt={item.title}
                      width={640}
                      height={480}
                      loading="lazy"
                      decoding="async"
                    />
                  ) : null}
                </div>
                <div className="work-card-body">
                  <span className="label">{category.name}</span>
                  <h3 className="font-serif work-card-title">{item.title}</h3>
                  {item.summary ? <p className="work-card-summary">{item.summary}</p> : null}
                </div>
              </Link>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
