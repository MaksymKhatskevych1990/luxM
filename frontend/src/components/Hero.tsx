import type { SiteSettings } from "@/lib/types";
import FloorPlan from "./FloorPlan";

type HeroProps = {
  settings: SiteSettings;
};

export default function Hero({ settings }: HeroProps) {
  const stats = [
    { value: settings.stats_projects, label: "Виконаних проєктів" },
    { value: settings.stats_years, label: "Років досвіду" },
    { value: settings.stats_masters, label: "Майстри в команді" },
    { value: settings.stats_production, label: "Власне виробництво" },
  ];

  return (
    <section
      style={{
        position: "relative",
        minHeight: "100svh",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      <div className="hero-bg" />
      <div
        aria-hidden="true"
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 0,
            bottom: 0,
            left: "25%",
            width: 1,
            background: "rgba(37, 37, 37, 0.05)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: 0,
            bottom: 0,
            left: "50%",
            width: 1,
            background: "rgba(37, 37, 37, 0.05)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: 0,
            bottom: 0,
            left: "75%",
            width: 1,
            background: "rgba(37, 37, 37, 0.05)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: "45%",
            left: 0,
            right: 0,
            height: 1,
            background: "rgba(37, 37, 37, 0.04)",
          }}
        />
      </div>

      <div
        className="wrap"
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          paddingTop: 48,
          paddingBottom: 80,
          position: "relative",
          zIndex: 1,
        }}
      >
        <div
          className="anim-up"
          style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 56 }}
        >
          <span className="label">Форма Studio · Київ, Україна</span>
          <span
            style={{
              display: "inline-block",
              width: 40,
              height: 1,
              background: "var(--c-oak)",
            }}
          />
          <span className="label label--oak">Заснована {settings.founded_year}</span>
        </div>

        <div className="hero-grid" style={{ minHeight: "auto", padding: 0 }}>
          <div>
            <h1
              className="anim-up d1 font-serif"
              style={{
                fontSize: "clamp(3.75rem, 7.5vw, 7rem)",
                lineHeight: 1,
                letterSpacing: "-0.025em",
                color: "var(--c-ink)",
                margin: 0,
              }}
            >
              Меблі,
              <br />
              <em style={{ fontStyle: "italic", color: "var(--c-oak)" }}>створені</em>
              <br />
              під ваш простір.
            </h1>
            <div
              className="anim-up d2"
              style={{ display: "flex", alignItems: "center", gap: 20, marginTop: 36 }}
            >
              <div style={{ width: 2, height: 40, background: "var(--c-oak)" }} />
              <p
                style={{
                  fontFamily: "var(--f-sans)",
                  fontSize: "0.9375rem",
                  letterSpacing: "0.1em",
                  color: "var(--c-stone)",
                  margin: 0,
                }}
              >
                Проєктування · Виробництво · Монтаж
              </p>
            </div>
            <div
              className="anim-up d3"
              style={{ display: "flex", flexWrap: "wrap", gap: 12, marginTop: 48 }}
            >
              <a href="#проєкти" className="btn-primary">
                Дивитись проєкти
              </a>
              <a href="#процес" className="btn-ghost">
                Про процес
              </a>
            </div>
          </div>

          <div className="hero-svg anim-up d2" style={{ opacity: 0.55 }}>
            <FloorPlan idPrefix="hero" />
            <div
              style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 12 }}
            >
              <div style={{ width: 20, height: 1, background: "var(--c-oak)" }} />
              <span className="label" style={{ fontSize: "0.625rem" }}>
                Технічне креслення · Масштаб 1:25
              </span>
            </div>
          </div>
        </div>

        <div
          className="anim-up d4"
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "24px 56px",
            marginTop: 80,
            paddingTop: 32,
            borderTop: "1px solid rgba(37, 37, 37, 0.1)",
          }}
        >
          {stats.map((stat) => (
            <div key={stat.label}>
              <div
                className="font-serif"
                style={{ fontSize: "2.25rem", color: "var(--c-ink)", lineHeight: 1 }}
              >
                {stat.value}
              </div>
              <div className="label" style={{ marginTop: 6 }}>
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div
        className="anim-up d5"
        style={{
          position: "absolute",
          bottom: 40,
          left: "50%",
          transform: "translateX(-50%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 10,
          zIndex: 1,
        }}
      >
        <span className="label" style={{ fontSize: "0.5625rem" }}>
          Гортати
        </span>
        <div
          style={{
            width: 1,
            height: 44,
            background: "linear-gradient(var(--c-oak), transparent)",
            animation: "bob 2s ease infinite",
          }}
        />
      </div>
    </section>
  );
}
