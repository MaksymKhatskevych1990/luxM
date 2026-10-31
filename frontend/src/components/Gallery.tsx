"use client";

import Image from "next/image";
import { useMemo, useState } from "react";
import type { PageSection, SiteSettings, WorkCategory, WorkItem } from "@/lib/types";
import WorkModal from "./WorkModal";

type GalleryProps = {
  section: PageSection;
  categories: WorkCategory[];
  settings: SiteSettings;
};

export default function Gallery({ section, categories, settings }: GalleryProps) {
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
  const [active, setActive] = useState<WorkItem | null>(null);

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
                  <em>{section.title_emphasis}</em>
                </>
              ) : null}
            </h2>
            {section.subtitle ? <p className="work-subtitle">{section.subtitle}</p> : null}
          </div>
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

        {current.description ? <p className="work-category-note">{current.description}</p> : null}

        <div className="work-grid">
          {current.items.map((item) => (
            <article
              key={item.id}
              className="proj-card work-card"
              role="button"
              tabIndex={0}
              onClick={() => setActive(item)}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  setActive(item);
                }
              }}
            >
              <div className="work-card-media">
                {item.image_url ? (
                  <Image
                    src={item.image_url}
                    alt={item.title}
                    fill
                    className="proj-img"
                    sizes="(max-width: 768px) 100vw, 33vw"
                    style={{ objectFit: "cover" }}
                  />
                ) : null}
              </div>
              <div className="work-card-body">
                <span className="label">{current.name}</span>
                <h3 className="font-serif work-card-title">{item.title}</h3>
                {item.summary ? <p className="work-card-summary">{item.summary}</p> : null}
              </div>
            </article>
          ))}
        </div>
      </div>

      <WorkModal item={active} settings={settings} onClose={() => setActive(null)} />
    </section>
  );
}
