"use client";

import { useCallback, useEffect, useMemo, useState, type MouseEvent } from "react";
import type { HeroScene, HeroStat, HeroZone, SiteSettings } from "@/lib/types";
import HeroStageFilm from "./HeroStageFilm";

type HeroProps = {
  settings: SiteSettings;
  stats: HeroStat[];
  scene?: HeroScene | null;
};

export default function Hero({ settings, stats, scene }: HeroProps) {
  const items = [...stats].sort((a, b) => a.order - b.order);
  const zones = useMemo(
    () => [...(scene?.zones ?? [])].sort((a, b) => a.order - b.order),
    [scene],
  );
  const [interactive, setInteractive] = useState(false);
  const [activeId, setActiveId] = useState<HeroZone["id"] | null>(null);
  const [tip, setTip] = useState<{ x: number; y: number } | null>(null);
  const [showFilm, setShowFilm] = useState(true);

  useEffect(() => {
    const media = window.matchMedia("(max-width: 768px)");
    const sync = () => setShowFilm(!media.matches);
    sync();
    media.addEventListener("change", sync);
    return () => media.removeEventListener("change", sync);
  }, []);

  const onSettled = useCallback(() => setInteractive(true), []);

  const active = zones.find((zone) => zone.id === activeId) ?? null;

  function placeTip(event: MouseEvent<SVGElement>) {
    const svg = event.currentTarget.ownerSVGElement ?? event.currentTarget;
    const rect = svg.getBoundingClientRect();
    setTip({
      x: ((event.clientX - rect.left) / rect.width) * 100,
      y: ((event.clientY - rect.top) / rect.height) * 100,
    });
  }

  function activate(zone: HeroZone, event?: MouseEvent<SVGRectElement>) {
    if (!interactive) return;
    setActiveId(zone.id);
    if (event) {
      placeTip(event);
      return;
    }
    setTip({
      x: Number(zone.x) + Number(zone.width) / 2,
      y: Number(zone.y) + Number(zone.height) / 2,
    });
  }

  function clear() {
    setActiveId(null);
    setTip(null);
  }

  return (
    <section className="hero hero--room">
      <div className="hero-room">
        <div className="hero-room-copy">
          <div className="hero-eyebrow anim-up">
            <span className="label">{settings.hero_eyebrow}</span>
          </div>

          <h1 className="hero-title anim-up d1 font-serif">
            {settings.hero_title_line1}
            <br />
            <em>{settings.hero_title_emphasis}</em>
            <br />
            {settings.hero_title_line2}
          </h1>

          <div className="hero-subline anim-up d2">
            <div className="hero-subline-bar" />
            <p>{settings.hero_subline}</p>
          </div>

          <div className="hero-cta anim-up d3">
            <a href={settings.hero_cta_primary_href} className="btn-primary">
              {settings.hero_cta_primary_text}
            </a>
            <a href={settings.hero_cta_secondary_href} className="btn-ghost">
              {settings.hero_cta_secondary_text}
            </a>
          </div>

          <div className="hero-foot anim-up d4">
            <div className="hero-brand" role="img" aria-label="ProProstir. Ремонти, дизайн, меблі">
              <svg className="hero-brand-mark" viewBox="0 0 104 98" aria-hidden="true">
                <path d="M51 1L0 30L0 87L12 87L12 38L51 16L92 38L92 79L104 79L104 30Z" />
                <path
                  fillRule="evenodd"
                  d="M30 45H74V68A11 11 0 0 1 63 79H43V97H30ZM43 57H62V65A4 4 0 0 1 58 69H43Z"
                />
              </svg>
              <p className="hero-brand-name" aria-hidden="true">
                ProProstir
              </p>
              <p className="hero-brand-tag" aria-hidden="true">
                <span>Ремонти</span>
                <span>•</span>
                <span>Дизайн</span>
                <span>•</span>
                <span>Меблі</span>
              </p>
            </div>
            <div className="hero-stats">
              {items.map((stat) => (
                <div key={stat.id}>
                  <div className="hero-stat-value font-serif">{stat.value}</div>
                  <div className="label" style={{ marginTop: 6 }}>
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {showFilm ? (
          <div
            className={`hero-room-visual${active ? " is-dimmed" : ""}${
              interactive ? " is-interactive" : ""
            }`}
          >
            <div className="hero-film-stage">
              <HeroStageFilm onSettled={onSettled} />
              <svg
                className="hero-zones"
                viewBox="0 0 100 100"
                preserveAspectRatio="none"
                aria-label="Інтерактивні зони інтер'єру"
              >
                {zones.map((zone) => (
                  <rect
                    key={zone.id}
                    x={Number(zone.x)}
                    y={Number(zone.y)}
                    width={Number(zone.width)}
                    height={Number(zone.height)}
                    className={activeId === zone.id ? "is-active" : ""}
                    onMouseEnter={(event) => activate(zone, event)}
                    onMouseMove={(event) => activate(zone, event)}
                    onMouseLeave={clear}
                    onFocus={() => activate(zone)}
                    onBlur={clear}
                    onClick={() => activate(zone)}
                    tabIndex={interactive ? 0 : -1}
                    role="button"
                    aria-label={`${zone.name}: ${zone.service}`}
                  />
                ))}
              </svg>

              {active && tip ? (
                <div
                  className="hero-tooltip"
                  style={{ left: `${tip.x}%`, top: `${tip.y}%` }}
                >
                  <span className="label label--oak">{active.name}</span>
                  {active.service ? <b>{active.service}</b> : null}
                  {active.materials ? <small>{active.materials}</small> : null}
                </div>
              ) : null}
            </div>
          </div>
        ) : null}
      </div>

      <div className="hero-scroll anim-up d5">
        <span className="label" style={{ fontSize: "0.5625rem" }}>
          {settings.hero_scroll_hint}
        </span>
        <div className="hero-scroll-line" />
      </div>
    </section>
  );
}
