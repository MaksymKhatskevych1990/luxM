"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import type { NavItem, SiteSettings } from "@/lib/types";
import { navByLocation } from "@/lib/content";

type HeaderProps = {
  settings: SiteSettings;
  navigation: NavItem[];
};

export default function Header({ settings, navigation }: HeaderProps) {
  const [open, setOpen] = useState(false);
  const items = navByLocation(navigation, "header");

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
        <Link href="/" className="header-logo" aria-label={settings.brand_name}>
          <svg className="header-logo-mark" viewBox="0 0 104 98" aria-hidden="true">
            <path d="M51 1L0 30L0 87L12 87L12 38L51 16L92 38L92 79L104 79L104 30Z" />
            <path
              fillRule="evenodd"
              d="M30 45H74V68A11 11 0 0 1 63 79H43V97H30ZM43 57H62V65A4 4 0 0 1 58 69H43Z"
            />
          </svg>
          <span className="header-logo-name">{settings.header_logo_primary}</span>
        </Link>

        <nav className="desktop-nav" aria-label="Основна навігація">
          {items.map((item) => (
            <a key={item.id} href={item.href} className="nav-item">
              {item.label}
            </a>
          ))}
        </nav>

        <a href={settings.header_cta_href} className="cta-invert desktop-cta">
          {settings.header_cta_text}
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
              background: "currentColor",
              transition: "transform 0.3s, opacity 0.3s",
              transform: open ? "translateY(6px) rotate(45deg)" : "none",
            }}
          />
          <span
            style={{
              display: "block",
              width: 22,
              height: 1,
              background: "currentColor",
              transition: "transform 0.3s, opacity 0.3s",
              opacity: open ? 0 : 1,
            }}
          />
          <span
            style={{
              display: "block",
              width: 22,
              height: 1,
              background: "currentColor",
              transition: "transform 0.3s, opacity 0.3s",
              transform: open ? "translateY(-6px) rotate(-45deg)" : "none",
            }}
          />
        </button>
      </div>

      {open ? (
        <nav className="mobile-nav" aria-label="Мобільна навігація">
          {items.map((item) => (
            <a key={item.id} href={item.href} onClick={() => setOpen(false)}>
              {item.label}
            </a>
          ))}
          <a
            href={settings.header_cta_href}
            className="cta-invert"
            style={{ alignSelf: "flex-start", marginTop: 8 }}
            onClick={() => setOpen(false)}
          >
            {settings.header_cta_text}
          </a>
        </nav>
      ) : null}
    </header>
  );
}
