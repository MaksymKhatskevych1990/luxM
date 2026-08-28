import type { ReactNode } from "react";
import type { SiteSettings } from "@/lib/types";

type FooterProps = {
  settings: SiteSettings;
};

const SERVICES = ["Кухні", "Гардеробні", "Вітальні", "Кабінети"];
const STUDIO = [
  { label: "Про нас", href: "#майстерня" },
  { label: "Майстерня", href: "#майстерня" },
  { label: "Процес", href: "#процес" },
  { label: "Проєкти", href: "#проєкти" },
];

function FooterLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a
      href={href}
      style={{
        display: "block",
        fontFamily: "var(--f-sans)",
        fontSize: "0.875rem",
        color: "rgba(247, 246, 242, 0.3)",
        textDecoration: "none",
        marginBottom: 10,
        transition: "color 0.2s",
      }}
    >
      {children}
    </a>
  );
}

export default function Footer({ settings }: FooterProps) {
  const year = new Date().getFullYear();

  return (
    <footer style={{ background: "#171613", padding: "56px 0 36px" }}>
      <div className="wrap">
        <div
          className="footer-grid"
          style={{
            alignItems: "flex-start",
            marginBottom: 48,
            paddingBottom: 44,
            borderBottom: "1px solid rgba(247, 246, 242, 0.06)",
          }}
        >
          <div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                marginBottom: 12,
              }}
            >
              <div className="logo-mark" aria-hidden="true" style={{ width: 24, height: 24 }}>
                <span />
                <span />
                <span />
                <span />
              </div>
              <span
                className="font-serif"
                style={{ fontSize: "1.125rem", color: "var(--c-parchment)" }}
              >
                {settings.brand_name}
              </span>
            </div>
            <p
              style={{
                fontFamily: "var(--f-sans)",
                fontSize: "0.875rem",
                color: "rgba(247, 246, 242, 0.28)",
                lineHeight: 1.6,
                maxWidth: 200,
              }}
            >
              {settings.tagline}
            </p>
          </div>

          <div className="footer-links">
            <div>
              <div className="label label--oak" style={{ marginBottom: 16, fontSize: "0.625rem" }}>
                Послуги
              </div>
              {SERVICES.map((item) => (
                <FooterLink key={item} href="#проєкти">
                  {item}
                </FooterLink>
              ))}
            </div>
            <div>
              <div className="label label--oak" style={{ marginBottom: 16, fontSize: "0.625rem" }}>
                Студія
              </div>
              {STUDIO.map((item) => (
                <FooterLink key={item.label} href={item.href}>
                  {item.label}
                </FooterLink>
              ))}
            </div>
            <div>
              <div className="label label--oak" style={{ marginBottom: 16, fontSize: "0.625rem" }}>
                Контакти
              </div>
              <FooterLink href={`mailto:${settings.email}`}>{settings.email}</FooterLink>
              <FooterLink href={`tel:${settings.phone.replace(/\s/g, "")}`}>
                {settings.phone}
              </FooterLink>
              <FooterLink href={settings.instagram_url}>Instagram</FooterLink>
              <FooterLink href={settings.telegram_url}>Telegram</FooterLink>
            </div>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: 12,
          }}
        >
          <span
            className="label"
            style={{ color: "rgba(247, 246, 242, 0.18)", fontSize: "0.5625rem" }}
          >
            © {year} {settings.brand_name} · Всі права захищено
          </span>
          <span
            className="label"
            style={{ color: "rgba(247, 246, 242, 0.18)", fontSize: "0.5625rem" }}
          >
            Київ, Україна · Виготовлено з гордістю
          </span>
        </div>
      </div>
    </footer>
  );
}
