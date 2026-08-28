"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import type { PageSection, ProcessStep } from "@/lib/types";

type ProcessProps = {
  section: PageSection;
  steps: ProcessStep[];
};

function pad(n: number) {
  return String(n).padStart(2, "0");
}

export default function Process({ section, steps }: ProcessProps) {
  const items = [...steps].sort((a, b) => a.order - b.order);
  const [active, setActive] = useState(0);
  const sectionRef = useRef<HTMLElement>(null);
  const activated = useRef(false);

  useEffect(() => {
    setActive(0);
    const el = sectionRef.current;
    if (!el) return;

    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !activated.current) {
          activated.current = true;
          setActive(0);
        }
      },
      { threshold: 0.28 },
    );

    io.observe(el);
    return () => io.disconnect();
  }, []);

  if (items.length === 0) return null;

  return (
    <section
      ref={sectionRef}
      id={section.section_id || undefined}
      className="section-pad"
      style={{ background: "var(--c-parchment)" }}
    >
      <div className="wrap">
        <div style={{ marginBottom: 64 }}>
          {section.eyebrow ? <span className="label">{section.eyebrow}</span> : null}
          <h2
            className="font-serif"
            style={{
              fontSize: "clamp(2rem, 3.5vw, 3rem)",
              color: "var(--c-ink)",
              margin: "14px 0 0",
            }}
          >
            {section.title}
            {section.title_emphasis ? (
              <>
                {" "}
                <em style={{ color: "var(--c-oak)" }}>{section.title_emphasis}</em>
              </>
            ) : null}
          </h2>
          {section.subtitle ? (
            <p
              style={{
                fontFamily: "var(--f-sans)",
                fontSize: "1rem",
                color: "var(--c-stone)",
                margin: "12px 0 0",
                maxWidth: 520,
              }}
            >
              {section.subtitle}
            </p>
          ) : null}
        </div>

        <div className="process-split" style={{ gap: 80 }}>
          <div>
            {items.map((step, i) => (
              <div
                key={step.id}
                className={`step-row${i === active ? " active" : ""}`}
                onClick={() => setActive(i)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    setActive(i);
                  }
                }}
                role="button"
                tabIndex={0}
                aria-expanded={i === active}
              >
                <span className="step-num">{pad(i + 1)}</span>
                <div>
                  <h3 className="step-title">{step.title}</h3>
                  <div className="step-body">
                    <p
                      style={{
                        fontFamily: "var(--f-sans)",
                        fontSize: "0.9375rem",
                        color: "var(--c-stone)",
                        margin: "8px 0 0",
                        lineHeight: 1.65,
                      }}
                    >
                      {step.description}
                    </p>
                  </div>
                  <div className="step-line" />
                </div>
                <span className="step-dur">{step.duration}</span>
              </div>
            ))}
          </div>

          <div style={{ position: "sticky", top: "18vh" }}>
            <div
              style={{
                overflow: "hidden",
                aspectRatio: "3 / 4",
                background: "var(--c-linen)",
                position: "relative",
              }}
            >
              {items.map((step, i) => (
                <Image
                  key={step.id}
                  src={step.image_url}
                  alt={step.title}
                  fill
                  sizes="(max-width: 768px) 100vw, 50vw"
                  style={{
                    objectFit: "cover",
                    opacity: i === active ? 1 : 0,
                    transition: "opacity 0.7s",
                  }}
                />
              ))}
            </div>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: `repeat(${items.length}, 1fr)`,
                gap: 4,
                marginTop: 14,
              }}
            >
              {items.map((step, i) => (
                <button
                  key={step.id}
                  type="button"
                  aria-label={step.title}
                  onClick={() => setActive(i)}
                  style={{
                    height: 2,
                    padding: 0,
                    border: "none",
                    cursor: "pointer",
                    background: i === active ? "var(--c-oak)" : "rgba(37, 37, 37, 0.1)",
                    transition: "background 0.3s",
                  }}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
