"use client";

import Image from "next/image";
import { useCallback, useEffect, useRef, useState } from "react";
import type { PageSection, SiteSettings } from "@/lib/types";

type BeforeAfterProps = {
  settings: SiteSettings;
  section?: PageSection;
};

export default function BeforeAfter({ settings, section }: BeforeAfterProps) {
  const frameRef = useRef<HTMLDivElement>(null);
  const dragging = useRef(false);
  const [pct, setPct] = useState(50);
  const beforeUrl = settings.before_image_url;
  const afterUrl = settings.after_image_url;
  const eyebrow = section?.eyebrow || settings.ba_eyebrow;
  const title = section?.title || settings.ba_title;
  const hint = section?.subtitle || settings.ba_hint;

  const setFromClientX = useCallback((clientX: number) => {
    const el = frameRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const next = ((clientX - rect.left) / rect.width) * 100;
    setPct(Math.min(100, Math.max(0, next)));
  }, []);

  useEffect(() => {
    const onMove = (e: PointerEvent) => {
      if (!dragging.current) return;
      setFromClientX(e.clientX);
    };
    const onUp = () => {
      dragging.current = false;
    };
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
    return () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
    };
  }, [setFromClientX]);

  return (
    <section
      id={section?.section_id || undefined}
      className="section-pad"
      style={{ background: "var(--c-parchment)" }}
    >
      <div className="wrap">
        <div style={{ textAlign: "center", marginBottom: 56 }}>
          {eyebrow ? <span className="label">{eyebrow}</span> : null}
          <h2
            className="font-serif"
            style={{
              fontSize: "clamp(2rem, 3.5vw, 3rem)",
              color: "var(--c-ink)",
              margin: "16px 0 10px",
            }}
          >
            {title}
          </h2>
          {hint ? (
            <p
              style={{
                fontFamily: "var(--f-sans)",
                fontSize: "1rem",
                color: "var(--c-stone)",
              }}
            >
              {hint}
            </p>
          ) : null}
        </div>

        <div
          ref={frameRef}
          role="slider"
          aria-label="Порівняння до і після"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(pct)}
          tabIndex={0}
          onPointerDown={(e) => {
            dragging.current = true;
            setFromClientX(e.clientX);
          }}
          onKeyDown={(e) => {
            if (e.key === "ArrowLeft") setPct((v) => Math.max(0, v - 2));
            if (e.key === "ArrowRight") setPct((v) => Math.min(100, v + 2));
          }}
          style={{
            maxWidth: 1100,
            margin: "0 auto",
            position: "relative",
            aspectRatio: "16 / 9",
            background: "var(--c-linen)",
            overflow: "hidden",
            cursor: "ew-resize",
            userSelect: "none",
            touchAction: "none",
          }}
        >
          {afterUrl ? (
            <Image
              src={afterUrl}
              alt={settings.ba_label_after}
              fill
              draggable={false}
              sizes="(max-width: 1100px) 100vw, 1100px"
              style={{ objectFit: "cover", pointerEvents: "none" }}
            />
          ) : null}

          <div
            style={{
              position: "absolute",
              inset: 0,
              clipPath: `inset(0 ${100 - pct}% 0 0)`,
            }}
          >
            {beforeUrl ? (
              <Image
                src={beforeUrl}
                alt={settings.ba_label_before}
                fill
                draggable={false}
                sizes="(max-width: 1100px) 100vw, 1100px"
                style={{ objectFit: "cover", pointerEvents: "none" }}
              />
            ) : null}
            <div
              style={{
                position: "absolute",
                top: 20,
                left: 20,
                padding: "6px 16px",
                background: "rgba(247, 246, 242, 0.9)",
                backdropFilter: "blur(8px)",
              }}
            >
              <span className="label" style={{ fontSize: "0.5625rem" }}>
                {settings.ba_label_before}
              </span>
            </div>
          </div>

          <div
            className="ba-handle"
            style={{ left: `${pct}%`, transform: "translateX(-50%)" }}
          >
            <div className="ba-knob">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden>
                <path d="M5 9L1 6V12L5 9Z" fill="#252525" />
                <path d="M13 9L17 6V12L13 9Z" fill="#252525" />
                <line x1="5.5" y1="9" x2="12.5" y2="9" stroke="#252525" strokeWidth="1.5" />
              </svg>
            </div>
          </div>

          <div
            style={{
              position: "absolute",
              top: 20,
              right: 20,
              padding: "6px 16px",
              background: "rgba(28, 27, 25, 0.75)",
              backdropFilter: "blur(8px)",
            }}
          >
            <span
              className="label"
              style={{ color: "rgba(247, 246, 242, 0.8)", fontSize: "0.5625rem" }}
            >
              {settings.ba_label_after}
            </span>
          </div>
          <div
            style={{
              position: "absolute",
              bottom: 18,
              left: "50%",
              transform: "translateX(-50%)",
              padding: "4px 14px",
              background: "rgba(247, 246, 242, 0.12)",
              backdropFilter: "blur(8px)",
              borderRadius: 2,
            }}
          >
            <span
              className="label"
              style={{ color: "rgba(247, 246, 242, 0.6)", fontSize: "0.5625rem" }}
            >
              {Math.round(pct)}%
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
