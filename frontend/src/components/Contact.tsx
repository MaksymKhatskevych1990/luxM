"use client";

import { FormEvent, useState } from "react";
import { submitLead } from "@/lib/api";
import type { SiteSettings } from "@/lib/types";

type ContactProps = {
  settings: SiteSettings;
};

const ROOMS = [
  { uk: "Кухня", value: "kitchen" },
  { uk: "Гардеробна", value: "wardrobe" },
  { uk: "Вітальня", value: "living" },
  { uk: "Спальня", value: "bedroom" },
  { uk: "Інше", value: "other" },
];

export default function Contact({ settings }: ContactProps) {
  const [room, setRoom] = useState(ROOMS[0].value);
  const [message, setMessage] = useState("");
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [telegram, setTelegram] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");
  const [error, setError] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!name.trim() || !phone.trim()) {
      setStatus("error");
      setError("Будь ласка, вкажіть ім'я та телефон.");
      return;
    }

    setStatus("sending");
    setError("");

    try {
      await submitLead({
        room_type: room,
        message: message.trim(),
        name: name.trim(),
        phone: phone.trim(),
        email: email.trim(),
        telegram: telegram.trim(),
      });
      setStatus("success");
    } catch (err) {
      setStatus("error");
      setError(err instanceof Error ? err.message : "Не вдалося надіслати заявку");
    }
  }

  const rows = [
    { label: "Адреса", value: settings.address },
    { label: "Телефон", value: settings.phone, href: `tel:${settings.phone.replace(/\s/g, "")}` },
    { label: "Email", value: settings.email, href: `mailto:${settings.email}` },
    { label: "Telegram", value: settings.telegram, href: settings.telegram_url },
  ];

  return (
    <section
      id="контакти"
      className="section-pad-lg"
      style={{ background: "var(--c-void)" }}
    >
      <div className="wrap">
        <div className="contact-split" style={{ gap: 100 }}>
          <div>
            <span className="label label--light">Зв&apos;язатися</span>
            <h2
              className="font-serif"
              style={{
                fontSize: "clamp(2.5rem, 4.5vw, 4.5rem)",
                color: "var(--c-parchment)",
                margin: "20px 0 0",
                lineHeight: 1.05,
                letterSpacing: "-0.02em",
              }}
            >
              Розкажіть
              <br />
              про свій
              <br />
              <em style={{ color: "var(--c-oak)" }}>простір.</em>
            </h2>
            <p
              style={{
                fontFamily: "var(--f-sans)",
                fontSize: "1.0625rem",
                color: "rgba(247, 246, 242, 0.45)",
                lineHeight: 1.75,
                margin: "32px 0 56px",
                maxWidth: 380,
              }}
            >
              Надішліть план приміщення, фотографію або просто ідею — ми зв&apos;яжемося
              протягом одного робочого дня.
            </p>
            <div>
              {rows.map((row) => (
                <div
                  key={row.label}
                  style={{
                    display: "flex",
                    gap: 20,
                    padding: "16px 0",
                    borderBottom: "1px solid rgba(247, 246, 242, 0.06)",
                  }}
                >
                  <span className="label label--light" style={{ minWidth: 72 }}>
                    {row.label}
                  </span>
                  {row.href ? (
                    <a
                      href={row.href}
                      style={{
                        fontFamily: "var(--f-sans)",
                        fontSize: "0.9375rem",
                        color: "rgba(247, 246, 242, 0.65)",
                      }}
                    >
                      {row.value}
                    </a>
                  ) : (
                    <span
                      style={{
                        fontFamily: "var(--f-sans)",
                        fontSize: "0.9375rem",
                        color: "rgba(247, 246, 242, 0.65)",
                      }}
                    >
                      {row.value}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div style={{ paddingTop: 8 }}>
            {status === "success" ? (
              <div style={{ paddingTop: 24 }}>
                <span className="label label--oak" style={{ display: "block", marginBottom: 16 }}>
                  Надіслано
                </span>
                <h3
                  className="font-serif"
                  style={{
                    fontSize: "clamp(1.75rem, 3vw, 2.5rem)",
                    color: "var(--c-parchment)",
                    margin: "0 0 16px",
                    lineHeight: 1.2,
                  }}
                >
                  Дякуємо, ми отримали ваш запит.
                </h3>
                <p
                  style={{
                    fontFamily: "var(--f-sans)",
                    fontSize: "1rem",
                    color: "rgba(247, 246, 242, 0.45)",
                    lineHeight: 1.7,
                    maxWidth: 360,
                  }}
                >
                  Зв&apos;яжемося протягом одного робочого дня, щоб обговорити ваш простір.
                </p>
              </div>
            ) : (
              <form onSubmit={onSubmit}>
                <div style={{ marginBottom: 36 }}>
                  <span
                    className="label label--light"
                    style={{ display: "block", marginBottom: 14 }}
                  >
                    Що плануєте
                  </span>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                    {ROOMS.map((item) => (
                      <button
                        key={item.value}
                        type="button"
                        className={`chip${room === item.value ? " on" : ""}`}
                        onClick={() => setRoom(item.value)}
                      >
                        {item.uk}
                      </button>
                    ))}
                  </div>
                </div>

                <div style={{ marginBottom: 28 }}>
                  <textarea
                    rows={4}
                    placeholder="Розкажіть про ваш проєкт…"
                    className="f-line"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                  />
                </div>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "0 28px",
                  }}
                  className="contact-fields"
                >
                  <input
                    placeholder="Ім'я"
                    className="f-line"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    style={{ marginBottom: 24 }}
                    autoComplete="name"
                    required
                  />
                  <input
                    placeholder="Телефон"
                    className="f-line"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    style={{ marginBottom: 24 }}
                    autoComplete="tel"
                    required
                  />
                  <input
                    placeholder="Email"
                    className="f-line"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{ marginBottom: 24 }}
                    autoComplete="email"
                  />
                  <input
                    placeholder="Telegram"
                    className="f-line"
                    value={telegram}
                    onChange={(e) => setTelegram(e.target.value)}
                    style={{ marginBottom: 24 }}
                    autoComplete="off"
                  />
                </div>

                {status === "error" ? (
                  <p
                    style={{
                      fontFamily: "var(--f-sans)",
                      fontSize: "0.875rem",
                      color: "var(--c-oak-pale)",
                      margin: "0 0 16px",
                    }}
                  >
                    {error}
                  </p>
                ) : null}

                <button
                  type="submit"
                  disabled={status === "sending"}
                  style={{
                    marginTop: 8,
                    padding: "16px 40px",
                    background: "var(--c-oak)",
                    color: "var(--c-void)",
                    border: "none",
                    cursor: status === "sending" ? "wait" : "pointer",
                    fontFamily: "var(--f-sans)",
                    fontSize: "0.9375rem",
                    letterSpacing: "0.06em",
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 10,
                    opacity: status === "sending" ? 0.7 : 1,
                  }}
                >
                  {status === "sending" ? "Надсилаємо…" : "Надіслати запит"}
                  <span style={{ fontSize: "1rem" }}>→</span>
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
