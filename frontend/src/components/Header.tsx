"use client";

import { useEffect, useState } from "react";
import type { NavItem, SiteSettings } from "@/lib/types";
import { navByLocation } from "@/lib/content";
import SiteLogo from "./SiteLogo";

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
        <a
          href="/"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            textDecoration: "none",
          }}
        >
          <SiteLogo
            src={settings.header_logo_url}
            alt={settings.brand_name}
            size={32}
          />
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
              {settings.header_logo_primary}
            </div>
            <div
              className="label label--oak"
              style={{ fontSize: "0.5rem", letterSpacing: "0.18em", marginTop: 1 }}
            >
              {settings.header_logo_secondary}
            </div>
          </div>
        </a>

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
