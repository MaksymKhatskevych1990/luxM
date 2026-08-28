import Image from "next/image";
import type {
  PageSection,
  SiteSettings,
  WorkshopImage,
  WorkshopStat,
} from "@/lib/types";

type WorkshopProps = {
  section: PageSection;
  settings: SiteSettings;
  stats: WorkshopStat[];
  images: WorkshopImage[];
};

export default function Workshop({ section, settings, stats, images }: WorkshopProps) {
  const items = [...images].sort((a, b) => a.order - b.order);
  const statItems = [...stats].sort((a, b) => a.order - b.order);
  const hero = items[0];
  const thumbs = items.slice(1, 3);

  return (
    <section
      id={section.section_id || undefined}
      className="section-pad"
      style={{ background: "var(--c-linen)" }}
    >
      <div className="wrap">
        <div className="workshop-split" style={{ gap: 80, alignItems: "center" }}>
          <div>
            {section.eyebrow ? <span className="label">{section.eyebrow}</span> : null}
            <blockquote
              className="font-serif"
              style={{
                fontSize: "clamp(1.625rem, 2.8vw, 2.625rem)",
                color: "var(--c-ink)",
                margin: "20px 0 0",
                lineHeight: 1.25,
                letterSpacing: "-0.01em",
              }}
            >
              &ldquo;{settings.workshop_quote}&rdquo;
            </blockquote>
            <div
              style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 28 }}
            >
              <div style={{ width: 32, height: 1, background: "var(--c-oak)" }} />
              <span
                className="font-serif"
                style={{
                  fontStyle: "italic",
                  fontSize: "0.9375rem",
                  color: "var(--c-stone)",
                }}
              >
                {settings.workshop_author}
              </span>
            </div>
            <p
              style={{
                fontFamily: "var(--f-sans)",
                fontSize: "1rem",
                color: "var(--c-stone)",
                lineHeight: 1.75,
                marginTop: 36,
                marginBottom: 40,
              }}
            >
              {settings.workshop_text}
            </p>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: 28,
                borderTop: "1px solid rgba(37, 37, 37, 0.1)",
                paddingTop: 36,
              }}
            >
              {statItems.map((stat) => (
                <div key={stat.id}>
                  <div
                    className="font-serif"
                    style={{ fontSize: "1.375rem", color: "var(--c-ink)" }}
                  >
                    {stat.value}
                  </div>
                  <div className="label" style={{ marginTop: 5 }}>
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            {hero ? (
              <div
                style={{
                  gridRow: "1 / 3",
                  overflow: "hidden",
                  background: "#ddd",
                  position: "relative",
                  minHeight: 280,
                }}
              >
                <Image
                  src={hero.image_url}
                  alt={hero.title}
                  fill
                  sizes="(max-width: 768px) 50vw, 25vw"
                  style={{ objectFit: "cover" }}
                />
              </div>
            ) : null}
            {thumbs.map((image) => (
              <div
                key={image.id}
                style={{
                  overflow: "hidden",
                  aspectRatio: "1 / 1",
                  background: "#ddd",
                  position: "relative",
                }}
              >
                <Image
                  src={image.image_url}
                  alt={image.title}
                  fill
                  sizes="(max-width: 768px) 50vw, 25vw"
                  style={{ objectFit: "cover" }}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
