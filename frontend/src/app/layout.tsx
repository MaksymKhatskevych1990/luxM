import type { Metadata, Viewport } from "next";
import {
  DM_Mono,
  DM_Serif_Display,
  Instrument_Sans,
  Montserrat,
} from "next/font/google";
import type { ReactNode } from "react";
import Analytics from "@/components/Analytics";
import { SITE_URL } from "@/lib/site";
import { fallbackHome } from "@/lib/fallback";
import "./globals.css";

const serif = DM_Serif_Display({
  subsets: ["latin"],
  weight: "400",
  style: ["normal", "italic"],
  variable: "--font-dm-serif",
  display: "swap",
});

const sans = Instrument_Sans({
  subsets: ["latin"],
  variable: "--font-instrument-sans",
  display: "swap",
});

const mono = DM_Mono({
  subsets: ["latin"],
  weight: ["300", "400", "500"],
  style: ["normal", "italic"],
  variable: "--font-dm-mono",
  display: "swap",
  preload: false,
});

const brand = Montserrat({
  subsets: ["latin", "cyrillic"],
  weight: ["500", "800"],
  variable: "--font-montserrat",
  display: "swap",
  preload: false,
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: fallbackHome.settings.seo_title,
    template: `%s | ${fallbackHome.settings.jsonld_name || fallbackHome.settings.brand_name}`,
  },
  description: fallbackHome.settings.seo_description,
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
    <html lang="uk" className={`${serif.variable} ${sans.variable} ${mono.variable} ${brand.variable}`}>
      <body>
        <a className="skip-link" href="#content">
          Перейти до вмісту
        </a>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
