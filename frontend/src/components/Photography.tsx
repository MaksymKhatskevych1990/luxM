import Image from "next/image";
import type { CraftDetail, PageSection } from "@/lib/types";

type PhotographyProps = {
  section: PageSection;
  details: CraftDetail[];
};

const LAYOUT = [
  { left: "0%", top: 0, width: "26%", rotate: "-0.6deg", z: 1 },
  { left: "18%", top: "5%", width: "30%", rotate: "0.4deg", z: 2 },
  { left: "42%", top: "2%", width: "27%", rotate: "-0.3deg", z: 3 },
  { left: "63%", top: "8%", width: "31%", rotate: "0.5deg", z: 4 },
];

export default function Photography({ section, details }: PhotographyProps) {
  const items = [...details].sort((a, b) => a.order - b.order);

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
            marginBottom: 64,
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
              {section.title_line2 ? (
                <>
                  <br />
                  {section.title_line2}
                </>
              ) : null}
              {section.title_emphasis ? (
                <>
                  <br />
                  <em style={{ color: "var(--c-oak)" }}>{section.title_emphasis}</em>
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
                color: "rgba(247, 246, 242, 0.4)",
                maxWidth: 260,
                lineHeight: 1.65,
                textAlign: "right",
              }}
            >
              {section.subtitle}
            </p>
          ) : null}
        </div>

        <div className="photo-stack">
          {items.map((item, i) => {
            const layout = LAYOUT[i] ?? LAYOUT[LAYOUT.length - 1];
            return (
              <div
                key={item.id}
                className="photo-frame"
                style={{
                  left: layout.left,
                  top: layout.top,
                  width: layout.width,
                  zIndex: layout.z,
                  transform: `rotate(${layout.rotate})`,
                }}
              >
                <div
                  style={{
                    overflow: "hidden",
                    background: "#333",
                    position: "relative",
                    aspectRatio: "3 / 4",
                  }}
                >
                  <Image
                    src={item.image_url}
                    alt={item.title}
                    fill
                    sizes="(max-width: 768px) 50vw, 30vw"
                    style={{ objectFit: "cover" }}
                  />
                </div>
                <div
                  style={{
                    paddingTop: 10,
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                  }}
                >
                  <div style={{ width: 14, height: 1, background: "var(--c-oak)" }} />
                  <span
                    className="label"
                    style={{ color: "rgba(247, 246, 242, 0.3)", fontSize: "0.5625rem" }}
                  >
                    {item.title}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
