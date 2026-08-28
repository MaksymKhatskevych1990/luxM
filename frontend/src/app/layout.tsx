import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import { SITE_URL } from "@/lib/site";
import "./globals.css";

const TITLE = "Форма Studio — меблі на замовлення в Києві";
const DESCRIPTION =
  "Преміальні меблі на замовлення: проєктування, виробництво та монтаж. Кухні, гардеробні, вітальні та кабінети.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: TITLE,
    template: "%s | Форма Studio",
  },
  description: DESCRIPTION,
  keywords: ["меблі на замовлення", "кухні Київ", "гардеробні", "Forma Studio"],
  authors: [{ name: "Форма Studio" }],
  creator: "Форма Studio",
  openGraph: {
    type: "website",
    locale: "uk_UA",
    url: SITE_URL,
    siteName: "Форма Studio",
    title: TITLE,
    description: DESCRIPTION,
  },
  twitter: {
    card: "summary_large_image",
    title: TITLE,
    description: DESCRIPTION,
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
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
