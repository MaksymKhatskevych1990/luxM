"use client";

import Image from "next/image";
import { useState, type MouseEvent } from "react";
import type { PageSection, Project, SiteSettings } from "@/lib/types";

type ProjectsProps = {
  section: PageSection;
  projects: Project[];
  settings: SiteSettings;
};

function pad(n: number) {
  return String(n).padStart(2, "0");
}

function craftPoints(project: Project): string[] {
  const category = `${project.category} ${project.title}`.toLocaleLowerCase("uk");
  if (category.includes("кух")) {
    return [
      "Корпус виставлений по рівню, стик зі стіною без щілини",
      "Фасади в одну лінію, однаковий зазор по всіх швах",
      "Петлі, доводчики і техніка відрегульовані на місці",
    ];
  }
  if (category.includes("гард")) {
    return [
      "Секції зібрані в одну площину по всій висоті",
      "Напрямні ящиків і штанги виставлені без перекосу",
      "Підсвітка і зазори дверцят перевірені після встановлення",
    ];
  }
  return [
    "Корпус підігнаний до стіни, підлоги і сусідніх секцій",
    "Фасади і ящики ходять рівно, фурнітура відрегульована",
    "Після збірки перевірений кожен стик і зазор",
  ];
}

export default function Projects({ section, projects }: ProjectsProps) {
  const items = [...projects].sort((a, b) => a.order - b.order).slice(0, 4);
  const [activeId, setActiveId] = useState(items[0]?.id ?? null);
  const active = items.find((project) => project.id === activeId) ?? items[0];
  const [origin, setOrigin] = useState({ x: 50, y: 42 });
  const [zoomed, setZoomed] = useState(false);

  if (!active) return null;

  const points = craftPoints(active);

  function track(event: MouseEvent<HTMLDivElement>) {
    const rect = event.currentTarget.getBoundingClientRect();
    setOrigin({
      x: ((event.clientX - rect.left) / rect.width) * 100,
      y: ((event.clientY - rect.top) / rect.height) * 100,
    });
    setZoomed(true);
  }

  return (
    <section id={section.section_id || undefined} className="section-pad">
      <div className="wrap">
        <div className="craft-heading">
          <div>
            {section.eyebrow ? <span className="label">{section.eyebrow}</span> : null}
            <h2 className="font-serif craft-title">
              {section.title}
              {section.title_line2 ? (
                <>
                  <br />
                  {section.title_line2}
                </>
              ) : null}
              {section.title_emphasis ? (
                <>
                  {" "}
                  <em>{section.title_emphasis}</em>
                </>
              ) : null}
            </h2>
          </div>
          <p className="craft-lead">
            {section.subtitle ||
              "Наведіть на фото — побачите руку збирача: зазори фасадів, фурнітуру і підгонку до стіни."}
          </p>
        </div>

        <div className="craft-layout">
          <div
            className={`craft-zoom${zoomed ? " is-on" : ""}`}
            onMouseMove={track}
            onMouseLeave={() => setZoomed(false)}
          >
            <Image
              src={active.image_url}
              alt={active.title}
              fill
              priority
              sizes="(max-width: 768px) 100vw, 62vw"
              className="craft-zoom-img"
              style={{ transformOrigin: `${origin.x}% ${origin.y}%` }}
            />
            <span className="craft-zoom-hint label">
              {zoomed ? "Зум збірки" : "Наведіть — зум"}
            </span>
          </div>

          <div className="craft-side">
            <p className="label">{pad(active.order)} · {active.materials_label}</p>
            <h3 className="font-serif craft-name">{active.title}</h3>
            <ul className="craft-points">
              {points.map((point) => (
                <li key={point}>{point}</li>
              ))}
            </ul>
            <div className="craft-switch" role="listbox" aria-label="Оберіть роботу для зуму">
              {items.map((project) => {
                const selected = project.id === active.id;
                return (
                  <button
                    key={project.id}
                    type="button"
                    role="option"
                    aria-selected={selected}
                    className={`craft-switch-btn${selected ? " is-on" : ""}`}
                    onClick={() => {
                      setActiveId(project.id);
                      setZoomed(false);
                      setOrigin({ x: 50, y: 42 });
                    }}
                  >
                    <span className="craft-switch-thumb">
                      <Image
                        src={project.image_url}
                        alt=""
                        fill
                        sizes="72px"
                        style={{ objectFit: "cover" }}
                      />
                    </span>
                    <span>{project.title}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
