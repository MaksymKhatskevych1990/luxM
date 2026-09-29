import type { ReactNode } from "react";
import type { NavItem, SiteSettings } from "@/lib/types";
import { navByLocation } from "@/lib/content";
import SiteLogo from "./SiteLogo";

type FooterProps = {
  settings: SiteSettings;
  navigation: NavItem[];
};

function FooterLink({
  href,
  children,
  external = false,
}: {
  href: string;
  children: ReactNode;
  external?: boolean;
}) {
  return (
    <a
      href={href}
      {...(external
        ? { target: "_blank", rel: "noopener noreferrer" }
        : {})}
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

export default function Footer({ settings, navigation }: FooterProps) {
  const year = new Date().getFullYear();
  const services = navByLocation(navigation, "footer_services");
  const studio = navByLocation(navigation, "footer_studio");

  const socials = [
    {
      label: settings.contact_label_instagram || "Instagram",
      href: settings.instagram_url,
    },
    {
      label: settings.contact_label_telegram || "Telegram",
      href: settings.telegram_url,
    },
    {
      label: settings.contact_label_whatsapp || "WhatsApp",
      href: settings.whatsapp_url,
    },
  ].filter((item) => Boolean(item.href));

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
              <SiteLogo
                src={settings.header_logo_url}
                alt={settings.brand_name}
                size={24}
              />
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
                {settings.footer_services_heading}
              </div>
              {services.map((item) => (
                <FooterLink key={item.id} href={item.href}>
                  {item.label}
                </FooterLink>
              ))}
            </div>
            <div>
              <div className="label label--oak" style={{ marginBottom: 16, fontSize: "0.625rem" }}>
                {settings.footer_studio_heading}
              </div>
              {studio.map((item) => (
                <FooterLink key={item.id} href={item.href}>
                  {item.label}
                </FooterLink>
              ))}
            </div>
            <div>
              <div className="label label--oak" style={{ marginBottom: 16, fontSize: "0.625rem" }}>
                {settings.footer_contacts_heading}
              </div>
              {settings.email ? (
                <FooterLink href={`mailto:${settings.email}`}>{settings.email}</FooterLink>
              ) : null}
              {settings.phone ? (
                <FooterLink href={`tel:${settings.phone.replace(/\s/g, "")}`}>
                  {settings.phone}
                </FooterLink>
              ) : null}
              {socials.map((item) => (
                <FooterLink key={item.label} href={item.href} external>
                  {item.label}
                </FooterLink>
              ))}
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
            style={{ color: "rgba(247, 246, 242, 0.92)", fontSize: "0.5625rem" }}
          >
            © {year} {settings.brand_name} · {settings.footer_copyright_suffix}
          </span>
          <span
            className="label"
            style={{ color: "rgba(247, 246, 242, 0.92)", fontSize: "0.5625rem" }}
          >
            {settings.footer_location_tagline}
          </span>
        </div>
      </div>
    </footer>
  );
}
