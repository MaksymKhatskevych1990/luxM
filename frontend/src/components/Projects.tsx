import Image from "next/image";
import type { Project } from "@/lib/types";

type ProjectsProps = {
  projects: Project[];
};

function pad(n: number) {
  return String(n).padStart(2, "0");
}

export default function Projects({ projects }: ProjectsProps) {
  const items = [...projects].sort((a, b) => a.order - b.order).slice(0, 4);
  const featured = items[0];
  const portrait = items[1];
  const rest = items.slice(2);

  return (
    <section id="проєкти" className="section-pad">
      <div className="wrap">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-end",
            marginBottom: 64,
            paddingBottom: 24,
            borderBottom: "1px solid rgba(37, 37, 37, 0.1)",
          }}
        >
          <div>
            <span className="label">Вибрані роботи</span>
            <h2
              className="font-serif"
              style={{
                fontSize: "clamp(2rem, 4vw, 3.25rem)",
                color: "var(--c-ink)",
                margin: "14px 0 0",
                lineHeight: 1.1,
              }}
            >
              Кожен предмет —
              <br />
              <em style={{ color: "var(--c-oak)" }}>окрема історія.</em>
            </h2>
          </div>
          <a
            href="#контакти"
            className="desktop-only"
            style={{
              fontFamily: "var(--f-mono)",
              fontSize: "0.75rem",
              letterSpacing: "0.1em",
              color: "var(--c-stone)",
              textDecoration: "none",
              borderBottom: "1px solid rgba(119, 115, 108, 0.3)",
              paddingBottom: 2,
            }}
          >
            Всі проєкти →
          </a>
        </div>

        <div className="proj-grid-inner">
          {featured ? (
            <article
              className="proj-card"
              style={{
                gridColumn: 1,
                gridRow: 1,
                position: "relative",
                overflow: "hidden",
                cursor: "pointer",
              }}
            >
              <div
                style={{
                  aspectRatio: "16 / 9",
                  overflow: "hidden",
                  background: "var(--c-linen)",
                  position: "relative",
                }}
              >
                <Image
                  src={featured.image_url}
                  alt={featured.title}
                  fill
                  className="proj-img"
                  sizes="(max-width: 768px) 100vw, 66vw"
                  priority
                  style={{ objectFit: "cover" }}
                />
              </div>
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  background:
                    "linear-gradient(to top, rgba(28, 27, 25, 0.6) 0%, transparent 55%)",
                }}
              />
              <div
                style={{
                  position: "absolute",
                  bottom: 0,
                  left: 0,
                  right: 0,
                  padding: "28px 32px",
                }}
              >
                <div style={{ display: "flex", gap: 10, marginBottom: 8 }}>
                  <span className="label label--oak">{pad(featured.order)}</span>
                  <span className="label" style={{ color: "rgba(247, 246, 242, 0.45)" }}>
                    {featured.materials_label}
                  </span>
                </div>
                <h3
                  className="font-serif"
                  style={{
                    fontSize: "clamp(1.375rem, 2vw, 2rem)",
                    color: "var(--c-parchment)",
                    margin: 0,
                  }}
                >
                  {featured.title}
                </h3>
                {featured.seo_description ? (
                  <p
                    className="proj-meta"
                    style={{
                      fontFamily: "var(--f-sans)",
                      fontSize: "0.9rem",
                      color: "rgba(247, 246, 242, 0.7)",
                      marginTop: 8,
                      maxWidth: 560,
                    }}
                  >
                    {featured.seo_description}
                  </p>
                ) : null}
              </div>
            </article>
          ) : null}

          {portrait ? (
            <article
              className="proj-card"
              style={{
                gridColumn: 2,
                gridRow: "1 / 3",
                position: "relative",
                overflow: "hidden",
                cursor: "pointer",
              }}
            >
              <div
                style={{
                  height: "100%",
                  minHeight: 520,
                  overflow: "hidden",
                  background: "var(--c-linen)",
                  position: "relative",
                }}
              >
                <Image
                  src={portrait.image_url}
                  alt={portrait.title}
                  fill
                  className="proj-img"
                  sizes="(max-width: 768px) 100vw, 33vw"
                  style={{ objectFit: "cover" }}
                />
              </div>
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  background:
                    "linear-gradient(to top, rgba(28, 27, 25, 0.65) 0%, transparent 60%)",
                }}
              />
              <div
                style={{
                  position: "absolute",
                  bottom: 0,
                  left: 0,
                  right: 0,
                  padding: 24,
                }}
              >
                <span className="label label--oak">
                  {pad(portrait.order)} / {portrait.materials_label}
                </span>
                <h3
                  className="font-serif"
                  style={{
                    fontSize: "1.375rem",
                    color: "var(--c-parchment)",
                    margin: "8px 0 0",
                  }}
                >
                  {portrait.title}
                </h3>
                {portrait.description ? (
                  <p
                    className="proj-meta"
                    style={{
                      fontFamily: "var(--f-sans)",
                      fontSize: "0.8125rem",
                      color: "rgba(247, 246, 242, 0.7)",
                      marginTop: 6,
                    }}
                  >
                    {portrait.description}
                  </p>
                ) : null}
              </div>
            </article>
          ) : null}

          {rest.length > 0 ? (
            <div className="proj-pair" style={{ gridColumn: 1, gridRow: 2 }}>
              {rest.map((project) => (
                <article
                  key={project.id}
                  className="proj-card"
                  style={{ position: "relative", cursor: "pointer" }}
                >
                  <div
                    style={{
                      aspectRatio: "4 / 3",
                      overflow: "hidden",
                      background: "var(--c-linen)",
                      position: "relative",
                    }}
                  >
                    <Image
                      src={project.image_url}
                      alt={project.title}
                      fill
                      className="proj-img"
                      sizes="(max-width: 768px) 100vw, 33vw"
                      style={{ objectFit: "cover" }}
                    />
                  </div>
                  <div style={{ padding: "16px 0 0" }}>
                    <span className="label">
                      {pad(project.order)} · {project.materials_label}
                    </span>
                    <h3
                      className="font-serif"
                      style={{
                        fontSize: "1.125rem",
                        color: "var(--c-ink)",
                        margin: "8px 0 0",
                      }}
                    >
                      {project.title}
                    </h3>
                  </div>
                </article>
              ))}
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}
