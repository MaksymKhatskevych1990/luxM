"use client";

import { useEffect, useState } from "react";

const NAV = [
  { href: "#проєкти", label: "Проєкти" },
  { href: "#процес", label: "Процес" },
  { href: "#майстерня", label: "Майстерня" },
  { href: "#контакти", label: "Контакти" },
];

function LogoMark() {
  return (
    <div className="logo-mark" aria-hidden="true">
      <span />
      <span />
      <span />
      <span />
    </div>
  );
}

export default function Header() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <header className="site-header">
      <div
        className="wrap"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          height: 72,
        }}
      >
        <a
          href="/"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            textDecoration: "none",
          }}
        >
          <LogoMark />
          <div>
            <div
              className="font-serif"
              style={{
                fontSize: "1.125rem",
                color: "var(--c-ink)",
                lineHeight: 1,
                letterSpacing: "-0.01em",
              }}
            >
              Форма
            </div>
            <div
              className="label label--oak"
              style={{ fontSize: "0.5rem", letterSpacing: "0.18em", marginTop: 1 }}
            >
              STUDIO
            </div>
          </div>
        </a>

        <nav className="desktop-nav" aria-label="Основна навігація">
          {NAV.map((item) => (
            <a key={item.href} href={item.href} className="nav-item">
              {item.label}
            </a>
          ))}
        </nav>

        <a href="#контакти" className="cta-invert desktop-cta">
          Обговорити проєкт
        </a>

        <button
          type="button"
          className="mobile-menu-btn"
          aria-label={open ? "Закрити меню" : "Відкрити меню"}
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          <span
            style={{
              display: "block",
              width: 22,
              height: 1,
              background: "var(--c-ink)",
              transition: "transform 0.3s, opacity 0.3s",
              transform: open ? "translateY(6px) rotate(45deg)" : "none",
            }}
          />
          <span
            style={{
              display: "block",
              width: 22,
              height: 1,
              background: "var(--c-ink)",
              transition: "transform 0.3s, opacity 0.3s",
              opacity: open ? 0 : 1,
            }}
          />
          <span
            style={{
              display: "block",
              width: 22,
              height: 1,
              background: "var(--c-ink)",
              transition: "transform 0.3s, opacity 0.3s",
              transform: open ? "translateY(-6px) rotate(-45deg)" : "none",
            }}
          />
        </button>
      </div>

      {open ? (
        <nav className="mobile-nav" aria-label="Мобільна навігація">
          {NAV.map((item) => (
            <a key={item.href} href={item.href} onClick={() => setOpen(false)}>
              {item.label}
            </a>
          ))}
          <a
            href="#контакти"
            className="cta-invert"
            style={{ alignSelf: "flex-start", marginTop: 8 }}
            onClick={() => setOpen(false)}
          >
            Обговорити проєкт
          </a>
        </nav>
      ) : null}
    </header>
  );
}
