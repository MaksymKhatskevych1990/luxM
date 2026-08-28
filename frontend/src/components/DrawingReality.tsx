"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import type { PageSection, SiteSettings } from "@/lib/types";
import FloorPlan from "./FloorPlan";

type DrawingRealityProps = {
  settings: SiteSettings;
  section?: PageSection;
};

export default function DrawingReality({ settings, section }: DrawingRealityProps) {
  const trackRef = useRef<HTMLDivElement>(null);
  const [progress, setProgress] = useState(0);
  const afterImageUrl = settings.after_image_url;
  const eyebrow = section?.eyebrow || settings.drawing_eyebrow;
  const title = section?.title || settings.drawing_title;
  const body = section?.subtitle || settings.drawing_body;

  useEffect(() => {
    const onScroll = () => {
      const el = trackRef.current;
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const total = el.offsetHeight - window.innerHeight * 0.55;
      const scrolled = -rect.top + window.innerHeight * 0.2;
      setProgress(Math.min(1, Math.max(0, scrolled / Math.max(total, 1))));
    };

    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, []);

  const label =
    progress < 0.34
      ? settings.drawing_phase_1_label
      : progress < 0.72
        ? settings.drawing_phase_2_label
        : settings.drawing_phase_3_label;

  return (
    <section
      id={section?.section_id || undefined}
      className="section-pad"
      style={{ background: "var(--c-parchment)" }}
    >
      <div className="wrap">
        <div style={{ textAlign: "center", marginBottom: 64 }}>
          {eyebrow ? <span className="label">{eyebrow}</span> : null}
          <h2
            className="font-serif"
            style={{
              fontSize: "clamp(2rem, 3.5vw, 3rem)",
              color: "var(--c-ink)",
              margin: "16px 0 12px",
            }}
          >
            {title}
            {section?.title_emphasis ? (
              <>
                {" "}
                <em style={{ color: "var(--c-oak)" }}>{section.title_emphasis}</em>
              </>
            ) : null}
          </h2>
          {body ? (
            <p
              style={{
                fontFamily: "var(--f-sans)",
                fontSize: "1rem",
                color: "var(--c-stone)",
                maxWidth: 420,
                margin: "0 auto",
              }}
            >
              {body}
            </p>
          ) : null}
        </div>
      </div>

      <div ref={trackRef} style={{ height: "160vh", position: "relative" }}>
        <div className="wrap" style={{ position: "sticky", top: "14vh" }}>
          <div style={{ maxWidth: 960, margin: "0 auto", position: "relative" }}>
            <div
              style={{
                position: "relative",
                aspectRatio: "16 / 10",
                overflow: "hidden",
                background: "var(--c-linen)",
              }}
            >
              {afterImageUrl ? (
                <Image
                  src={afterImageUrl}
                  alt={settings.drawing_result_alt}
                  fill
                  sizes="(max-width: 960px) 100vw, 960px"
                  style={{ objectFit: "cover" }}
                />
              ) : null}
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  background: "var(--c-parchment)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  opacity: 1 - progress,
                  pointerEvents: "none",
                }}
              >
                <div style={{ width: "92%", padding: "40px 0" }}>
                  <FloorPlan idPrefix="draw" />
                </div>
              </div>
              <div
                style={{
                  position: "absolute",
                  top: 20,
                  right: 20,
                  padding: "6px 14px",
                  background: "rgba(247, 246, 242, 0.9)",
                  backdropFilter: "blur(8px)",
                }}
              >
                <span className="label" style={{ fontSize: "0.5625rem" }}>
                  {label}
                </span>
              </div>
            </div>

            <div
              style={{
                marginTop: 24,
                display: "flex",
                alignItems: "center",
                gap: 16,
              }}
            >
              <span className="label" style={{ fontSize: "0.5625rem", whiteSpace: "nowrap" }}>
                {settings.drawing_phase_1_label}
              </span>
              <div
                style={{
                  flex: 1,
                  height: 1,
                  background: "rgba(37, 37, 37, 0.1)",
                  position: "relative",
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    left: `${Math.min(100, Math.max(0, progress * 100))}%`,
                    top: "50%",
                    width: 7,
                    height: 7,
                    borderRadius: "50%",
                    background: "var(--c-oak)",
                    transform: "translate(-50%, -50%)",
                  }}
                />
                <div
                  style={{
                    height: "100%",
                    background: "var(--c-oak)",
                    width: `${progress * 100}%`,
                  }}
                />
              </div>
              <span className="label" style={{ fontSize: "0.5625rem", whiteSpace: "nowrap" }}>
                {settings.drawing_phase_2_label}
              </span>
              <div
                style={{
                  flex: 1,
                  height: 1,
                  background: "rgba(37, 37, 37, 0.1)",
                }}
              >
                <div
                  style={{
                    height: "100%",
                    background: "var(--c-oak)",
                    width: `${Math.min(100, Math.max(0, (progress - 0.5) * 200))}%`,
                  }}
                />
              </div>
              <span className="label" style={{ fontSize: "0.5625rem", whiteSpace: "nowrap" }}>
                {settings.drawing_phase_3_label}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
