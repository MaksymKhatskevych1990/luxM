"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import type { Project, SiteSettings } from "@/lib/types";

type ProjectDetailProps = {
  project: Project;
  settings: SiteSettings;
};

function pad(n: number) {
  return String(n).padStart(2, "0");
}

const STAGE_MS = 4200;

export default function ProjectDetail({ project, settings }: ProjectDetailProps) {
  const stages = [...project.stages].sort((a, b) => a.order - b.order);
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [progress, setProgress] = useState(0);
  const remaining = useRef(STAGE_MS);

  useEffect(() => {
    remaining.current = STAGE_MS;
    setProgress(0);
  }, [index]);

  useEffect(() => {
    if (!playing || stages.length === 0) return;

    const start = Date.now();
    const initial = remaining.current;

    const tick = window.setInterval(() => {
      const left = initial - (Date.now() - start);
      remaining.current = left;
      setProgress(Math.min(1, Math.max(0, 1 - left / STAGE_MS)));
      if (left <= 0) {
        remaining.current = STAGE_MS;
        setIndex((i) => (i + 1) % stages.length);
      }
    }, 50);

    return () => window.clearInterval(tick);
  }, [playing, index, stages.length]);

  if (stages.length === 0) return null;

  const current = stages[index];
  const paragraphs = project.description.split("\n\n").filter(Boolean);
  const meta = [
    { label: settings.meta_label_area, value: project.area },
    { label: settings.meta_label_materials, value: project.materials_label },
    { label: settings.meta_label_duration, value: project.duration },
    {
      label: settings.meta_label_year,
      value: project.year ? String(project.year) : "",
    },
    { label: settings.meta_label_location, value: project.location },
  ].filter((row) => row.value);

  return (
    <section className="section-pad" style={{ background: "var(--c-linen)" }}>
      <div className="wrap">
        <div style={{ marginBottom: 52 }}>
          <span className="label">
            {settings.detail_eyebrow_prefix} · {pad(project.order)}
          </span>
          <h2
            className="font-serif"
            style={{
              fontSize: "clamp(1.75rem, 3vw, 2.75rem)",
              color: "var(--c-ink)",
              margin: "12px 0 0",
            }}
          >
            {settings.detail_section_title}
          </h2>
        </div>

        <div className="detail-split">
          <div>
            <div style={{ position: "relative", background: "var(--c-ink)" }}>
              <div
                style={{
                  aspectRatio: "16 / 10",
                  overflow: "hidden",
                  position: "relative",
                }}
              >
                {stages.map((stage, i) => (
                  <Image
                    key={stage.id}
                    src={stage.image_url}
                    alt={stage.title}
                    fill
                    sizes="(max-width: 768px) 100vw, 57vw"
                    style={{
                      objectFit: "cover",
                      opacity: i === index ? 1 : 0,
                      transition: "opacity 0.9s",
                    }}
                  />
                ))}
              </div>
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  background: "rgba(28, 27, 25, 0.25)",
                  pointerEvents: "none",
                }}
              />
              <div
                style={{
                  position: "absolute",
                  top: 24,
                  left: 24,
                  display: "flex",
                  gap: 12,
                  alignItems: "center",
                }}
              >
                <span
                  className="font-mono"
                  style={{
                    fontSize: "0.625rem",
                    letterSpacing: "0.15em",
                    color: "rgba(247, 246, 242, 0.45)",
                  }}
                >
                  {pad(index + 1)} / {pad(stages.length)}
                </span>
                <span
                  className="font-serif"
                  style={{ fontSize: "1.375rem", color: "var(--c-parchment)" }}
                >
                  {current.title}
                </span>
              </div>
              <button
                type="button"
                aria-label={playing ? "Пауза" : "Відтворити"}
                onClick={() => setPlaying((v) => !v)}
                style={{
                  position: "absolute",
                  bottom: 20,
                  right: 20,
                  width: 44,
                  height: 44,
                  background: "rgba(247, 246, 242, 0.12)",
                  border: "1px solid rgba(247, 246, 242, 0.2)",
                  cursor: "pointer",
                  color: "var(--c-parchment)",
                  fontSize: 14,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  backdropFilter: "blur(8px)",
                }}
              >
                {playing ? "⏸" : "▶"}
              </button>
              <div
                style={{
                  position: "absolute",
                  bottom: 0,
                  left: 0,
                  right: 0,
                  height: 2,
                  background: "rgba(247, 246, 242, 0.12)",
                }}
              >
                <div
                  style={{
                    height: "100%",
                    background: "var(--c-oak)",
                    width: `${((index + progress) / stages.length) * 100}%`,
                    transition: playing ? "width 0.05s linear" : "width 0.6s",
                  }}
                />
              </div>
            </div>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: `repeat(${stages.length}, 1fr)`,
                borderBottom: "1px solid rgba(37, 37, 37, 0.1)",
              }}
            >
              {stages.map((stage, i) => (
                <button
                  key={stage.id}
                  type="button"
                  className={`stage-tab${i === index ? " active" : ""}`}
                  onClick={() => {
                    setIndex(i);
                    setPlaying(true);
                  }}
                >
                  <span style={{ marginRight: 5, opacity: 0.45 }}>{pad(i + 1)}</span>
                  {stage.title}
                </button>
              ))}
            </div>
          </div>

          <div style={{ paddingLeft: 0 }}>
            <div style={{ position: "sticky", top: "12vh" }}>
              <div
                style={{
                  borderLeft: "2px solid var(--c-oak)",
                  paddingLeft: 22,
                  marginBottom: 32,
                }}
              >
                <span className="label" style={{ display: "block", marginBottom: 10 }}>
                  {settings.detail_number_prefix} {pad(project.order)}
                  {project.year ? ` · ${project.year}` : ""}
                </span>
                <h3
                  className="font-serif"
                  style={{
                    fontSize: "clamp(1.625rem, 2.2vw, 2.25rem)",
                    color: "var(--c-ink)",
                    margin: 0,
                    lineHeight: 1.2,
                  }}
                >
                  {project.subtitle || project.title}
                </h3>
              </div>
              {paragraphs.map((text) => (
                <p
                  key={text.slice(0, 24)}
                  style={{
                    fontFamily: "var(--f-sans)",
                    fontSize: "1rem",
                    color: "var(--c-stone)",
                    lineHeight: 1.75,
                    marginBottom: 28,
                  }}
                >
                  {text}
                </p>
              ))}
              <div
                style={{
                  borderTop: "1px solid rgba(37, 37, 37, 0.1)",
                  paddingTop: 28,
                }}
              >
                {meta.map((row) => (
                  <div
                    key={row.label}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      gap: 16,
                      padding: "11px 0",
                      borderBottom: "1px solid rgba(37, 37, 37, 0.06)",
                    }}
                  >
                    <span className="label">{row.label}</span>
                    <span
                      style={{
                        fontFamily: "var(--f-sans)",
                        fontSize: "0.9375rem",
                        color: "var(--c-ink)",
                        textAlign: "right",
                      }}
                    >
                      {row.value}
                    </span>
                  </div>
                ))}
              </div>
              <a
                href={settings.detail_cta_href}
                className="btn-primary"
                style={{ marginTop: 32 }}
              >
                {settings.detail_cta_text}
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
