import type { Metadata } from "next";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { fallbackHome } from "@/lib/fallback";

export const metadata: Metadata = {
  title: "Сторінку не знайдено",
  robots: { index: false, follow: true },
};

export default function NotFound() {
  return (
    <>
      <Header settings={fallbackHome.settings} navigation={fallbackHome.navigation} />
      <main className="section-pad">
        <div
          className="wrap"
          style={{ textAlign: "center", padding: "72px 0 96px", maxWidth: 720 }}
        >
          <span className="label label--oak">Помилка 404</span>
          <h1
            className="font-serif"
            style={{
              fontSize: "clamp(2.75rem, 6vw, 5rem)",
              color: "var(--c-ink)",
              margin: "18px 0 16px",
              lineHeight: 1.05,
            }}
          >
            Сторінку
            <br />
            <em style={{ color: "var(--c-oak)" }}>не знайдено.</em>
          </h1>
          <p
            style={{
              fontFamily: "var(--f-sans)",
              fontSize: "1.0625rem",
              color: "var(--c-stone)",
              lineHeight: 1.7,
              margin: "0 auto 36px",
              maxWidth: 420,
            }}
          >
            Можливо, вона була переміщена або ніколи не існувала. Поверніться на головну —
            там проєкти, процес і команда.
          </p>
          <a href="/" className="btn-primary">
            На головну
          </a>
        </div>
      </main>
      <Footer settings={fallbackHome.settings} navigation={fallbackHome.navigation} />
    </>
  );
}
