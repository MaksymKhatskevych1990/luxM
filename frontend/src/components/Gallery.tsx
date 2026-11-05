"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { PageSection, WorkCategory } from "@/lib/types";

type GalleryProps = {
  section: PageSection;
  categories: WorkCategory[];
};

export default function Gallery({ section, categories }: GalleryProps) {
  const visible = useMemo(
    () =>
      [...(categories || [])]
        .map((category) => ({
          ...category,
          items: [...(category.items || [])].sort((a, b) => a.order - b.order),
        }))
        .filter((category) => category.items.length > 0)
        .sort((a, b) => a.order - b.order),
    [categories],
  );
  const [slug, setSlug] = useState(visible[0]?.slug ?? "");
  const current = visible.find((category) => category.slug === slug) ?? visible[0];
  if (!current) return null;

  return (
    <section id={section.section_id || "gallery"} className="section-pad">
      <div className="wrap">
        <div className="work-heading">
          <div>
            {section.eyebrow ? <span className="label">{section.eyebrow}</span> : null}
            <h2 className="font-serif work-title">
              {section.title}
              {section.title_line2 ? (
                <>
                  <br />
                  {section.title_line2}
                </>
              ) : null}
              {section.title_emphasis ? (
                <>
                  <br />
                  <em style={{ color: "var(--c-oak-text)" }}>{section.title_emphasis}</em>
                </>
              ) : null}
            </h2>
            {section.subtitle ? <p className="work-subtitle">{section.subtitle}</p> : null}
          </div>
          <Link href="/works" className="work-all">
            Усі роботи →
          </Link>
        </div>

        {visible.length > 1 ? (
          <div className="work-filters" role="tablist" aria-label="Категорії робіт">
            {visible.map((category) => {
              const selected = category.slug === current.slug;
              return (
                <button
                  key={category.slug}
                  type="button"
                  role="tab"
                  aria-selected={selected}
                  aria-controls={`home-works-${category.slug}`}
                  className={`work-filter${selected ? " is-active" : ""}`}
                  onClick={() => setSlug(category.slug)}
                >
                  {category.name}
                  <span>{category.items.length}</span>
                </button>
              );
            })}
          </div>
        ) : null}

        {visible.map((category) => {
          const selected = category.slug === current.slug;
          return (
            <div
              key={category.slug}
              id={`home-works-${category.slug}`}
              role="tabpanel"
              hidden={!selected}
            >
              {category.description ? <p className="work-category-note">{category.description}</p> : null}
              <div className="work-grid">
                {category.items.map((item) => (
                  <Link key={item.id} href={`/works/${item.slug}`} className="proj-card work-card">
                    <div className="work-card-media">
                      {item.image_url ? (
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
            </div>
          );
        })}
      </div>
    </section>
  );
}
