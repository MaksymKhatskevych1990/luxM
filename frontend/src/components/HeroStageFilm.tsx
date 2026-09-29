"use client";

import { useEffect, useState } from "react";

export const HERO_STAGES = [
  {
    src: "/hero/stage-1.jpg",
    label: "01",
    title: "Оболонка",
  },
  {
    src: "/hero/stage-2.jpg",
    label: "02",
    title: "Оздоблення",
  },
  {
    src: "/hero/stage-3.jpg",
    label: "03",
    title: "Заходь і живи",
  },
] as const;

const HOLD_MS = 2800;
const FADE_MS = 1400;
const LAST = HERO_STAGES.length - 1;

type HeroStageFilmProps = {
  onSettled?: () => void;
};

export default function HeroStageFilm({ onSettled }: HeroStageFilmProps) {
  const [index, setIndex] = useState(0);
  const [settled, setSettled] = useState(false);
  const [reduceMotion, setReduceMotion] = useState(false);

  useEffect(() => {
    HERO_STAGES.forEach((stage) => {
      const image = new window.Image();
      image.src = stage.src;
    });
  }, []);

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const sync = () => setReduceMotion(media.matches);
    sync();
    media.addEventListener("change", sync);
    return () => media.removeEventListener("change", sync);
  }, []);

  useEffect(() => {
    if (reduceMotion) {
      setIndex(LAST);
      setSettled(true);
      return;
    }

    if (index >= LAST) {
      const done = window.setTimeout(() => setSettled(true), FADE_MS);
      return () => window.clearTimeout(done);
    }

    const id = window.setTimeout(() => {
      setIndex((current) => Math.min(current + 1, LAST));
    }, HOLD_MS + FADE_MS);
    return () => window.clearTimeout(id);
  }, [index, reduceMotion]);

  useEffect(() => {
    if (settled) onSettled?.();
  }, [settled, onSettled]);

  const active = reduceMotion ? LAST : index;

  return (
    <div className={`hero-film${settled ? " is-settled" : ""}`} aria-hidden="true">
      {HERO_STAGES.map((stage, i) => (
        <div
          key={stage.src}
          className={`hero-film-frame${i === active ? " is-on" : ""}`}
        >
          <img src={stage.src} alt="" />
        </div>
      ))}
      <div className="hero-film-meta">
        <span className="label label--oak">{HERO_STAGES[active].label}</span>
        <strong className="font-serif">{HERO_STAGES[active].title}</strong>
        <div className="hero-film-dots">
          {HERO_STAGES.map((stage, i) => (
            <span
              key={stage.src}
              className={i === active ? "is-on" : undefined}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
