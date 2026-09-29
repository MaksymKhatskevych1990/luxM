import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import { SITE_URL } from "@/lib/site";
import { fallbackHome } from "@/lib/fallback";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: fallbackHome.settings.seo_title,
    template: `%s | ${fallbackHome.settings.jsonld_name || fallbackHome.settings.brand_name}`,
  },
  description: fallbackHome.settings.seo_description,
  robots: {
    index: false,
    follow: false,
    nocache: true,
    googleBot: {
      index: false,
      follow: false,
      noimageindex: true,
    },
  },
  alternates: {
    canonical: "/",
    languages: {
      uk: "/",
    },
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#f7f6f2",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="uk">
      <body>{children}</body>
    </html>
  );
}
