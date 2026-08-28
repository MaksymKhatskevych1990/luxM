import Image from "next/image";
import type { Material, PageSection } from "@/lib/types";

type MaterialsProps = {
  section: PageSection;
  materials: Material[];
};

export default function Materials({ section, materials }: MaterialsProps) {
  const items = [...materials].sort((a, b) => a.order - b.order);

  return (
    <section
      id={section.section_id || undefined}
      className="section-pad"
      style={{ background: "var(--c-ink)" }}
    >
      <div className="wrap">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-end",
            marginBottom: 56,
            gap: 24,
          }}
        >
          <div>
            {section.eyebrow ? (
              <span className="label label--light">{section.eyebrow}</span>
            ) : null}
            <h2
              className="font-serif"
              style={{
                fontSize: "clamp(2rem, 3.5vw, 3rem)",
                color: "var(--c-parchment)",
                margin: "12px 0 0",
              }}
            >
              {section.title}
              {section.title_emphasis ? (
                <>
                  {" "}
                  <em style={{ color: "var(--c-oak)" }}>{section.title_emphasis}</em>
                </>
              ) : null}
              {section.title_line2 ? (
                <>
                  <br />
                  {section.title_line2}
                </>
              ) : null}
            </h2>
          </div>
          {section.subtitle ? (
            <p
              className="desktop-only"
              style={{
                fontFamily: "var(--f-sans)",
                fontSize: "0.9375rem",
                color: "rgba(247, 246, 242, 0.35)",
                maxWidth: 240,
                lineHeight: 1.6,
              }}
            >
              {section.subtitle}
            </p>
          ) : null}
        </div>

        <div className="materials-grid">
          {items.map((material) => (
            <article key={material.id} className="mat-card">
              <div style={{ height: 320, overflow: "hidden", position: "relative" }}>
                <Image
                  src={material.image_url}
                  alt={material.name_uk}
                  fill
                  sizes="(max-width: 768px) 50vw, 16vw"
                  style={{ objectFit: "cover" }}
                />
              </div>
              <div className="mat-overlay">
                <p
                  className="mat-desc"
                  style={{
                    fontFamily: "var(--f-sans)",
                    fontSize: "0.8125rem",
                    color: "rgba(247, 246, 242, 0.8)",
                    lineHeight: 1.55,
                    marginBottom: 10,
                  }}
                >
                  {material.description}
                </p>
                <div
                  className="font-serif"
                  style={{ fontSize: "1.125rem", color: "var(--c-parchment)" }}
                >
                  {material.name_uk}
                </div>
                <div
                  className="label"
                  style={{
                    color: "rgba(247, 246, 242, 0.3)",
                    fontSize: "0.5625rem",
                    marginTop: 2,
                  }}
                >
                  {material.name_en}
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
