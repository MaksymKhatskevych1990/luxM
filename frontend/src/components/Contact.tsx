"use client";

import { FormEvent, useRef, useState } from "react";
import { submitLead } from "@/lib/api";
import type { PageSection, RoomType, SiteSettings } from "@/lib/types";

type ContactProps = {
  settings: SiteSettings;
  roomTypes: RoomType[];
  section?: PageSection;
};

export default function Contact({ settings, roomTypes, section }: ContactProps) {
  const rooms = [...roomTypes]
    .filter((item) => item.is_active !== false)
    .sort((a, b) => a.order - b.order);
  const [room, setRoom] = useState(rooms[0]?.value ?? "");
  const [message, setMessage] = useState("");
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [telegram, setTelegram] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");
  const [error, setError] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!name.trim() || !phone.trim()) {
      setStatus("error");
      setError(settings.contact_validation_message);
      return;
    }

    if (file && file.size > 15 * 1024 * 1024) {
      setStatus("error");
      setError("Файл завеликий. Максимум 15 МБ.");
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
        attachment: file,
      });
      setStatus("success");
    } catch (err) {
      setStatus("error");
      setError(err instanceof Error ? err.message : settings.contact_validation_message);
    }
  }

  const rows = [
    { label: settings.contact_label_address, value: settings.address },
    settings.phone
      ? {
          label: settings.contact_label_phone,
          value: settings.phone,
          href: `tel:${settings.phone.replace(/\s/g, "")}`,
        }
      : null,
    settings.email
      ? {
          label: settings.contact_label_email,
          value: settings.email,
          href: `mailto:${settings.email}`,
        }
      : null,
    settings.telegram || settings.telegram_url
      ? {
          label: settings.contact_label_telegram,
          value: settings.telegram || settings.contact_label_telegram,
          href: settings.telegram_url || undefined,
        }
      : null,
    settings.whatsapp || settings.whatsapp_url
      ? {
          label: settings.contact_label_whatsapp,
          value: settings.whatsapp || settings.contact_label_whatsapp,
          href: settings.whatsapp_url || undefined,
        }
      : null,
    settings.instagram_url
      ? {
          label: settings.contact_label_instagram,
          value: settings.contact_label_instagram,
          href: settings.instagram_url,
        }
      : null,
  ].filter((row): row is { label: string; value: string; href?: string } =>
    Boolean(row && row.value)
  );

  return (
    <section
      id={section?.section_id || undefined}
      className="section-pad-lg"
      style={{ background: "var(--c-void)" }}
    >
      <div className="wrap">
        <div className="contact-split" style={{ gap: 100 }}>
          <div>
            <span className="label label--light">{settings.contact_eyebrow}</span>
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
              {settings.contact_title_line1}
              <br />
              {settings.contact_title_line2}
              <br />
              <em style={{ color: "var(--c-oak)" }}>{settings.contact_title_emphasis}</em>
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
              {settings.contact_intro}
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
                      {...(row.href.startsWith("http")
                        ? { target: "_blank", rel: "noopener noreferrer" }
                        : {})}
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
                  {settings.contact_success_eyebrow}
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
                  {settings.contact_success_title}
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
                  {settings.contact_success_body}
                </p>
              </div>
            ) : (
              <form onSubmit={onSubmit}>
                <div style={{ marginBottom: 36 }}>
                  <span
                    className="label label--light"
                    style={{ display: "block", marginBottom: 14 }}
                  >
                    {settings.contact_room_heading}
                  </span>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                    {rooms.map((item) => (
                      <button
                        key={item.value}
                        type="button"
                        className={`chip${room === item.value ? " on" : ""}`}
                        onClick={() => setRoom(item.value)}
                      >
                        {item.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div style={{ marginBottom: 28 }}>
                  <textarea
                    rows={4}
                    placeholder={settings.contact_message_placeholder}
                    className="f-line"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                  />
                </div>

                <div style={{ marginBottom: 28 }}>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/jpeg,image/png,image/webp,image/heic,image/heif,application/pdf"
                    className="contact-file-input"
                    onChange={(e) => {
                      setFile(e.target.files?.[0] ?? null);
                      setError("");
                    }}
                  />
                  <button
                    type="button"
                    className="contact-file"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <span>{file ? file.name : "Додати фото «до» або план"}</span>
                    <span className="contact-file-hint">JPG, PNG, WEBP або PDF · до 15 МБ</span>
                  </button>
                  {file ? (
                    <button
                      type="button"
                      className="contact-file-clear"
                      onClick={() => {
                        setFile(null);
                        if (fileInputRef.current) fileInputRef.current.value = "";
                      }}
                    >
                      Прибрати файл
                    </button>
                  ) : null}
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
                    placeholder={settings.contact_name_placeholder}
                    className="f-line"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    style={{ marginBottom: 24 }}
                    autoComplete="name"
                    required
                  />
                  <input
                    placeholder={settings.contact_phone_placeholder}
                    className="f-line"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    style={{ marginBottom: 24 }}
                    autoComplete="tel"
                    required
                  />
                  <input
                    placeholder={settings.contact_email_placeholder}
                    className="f-line"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{ marginBottom: 24 }}
                    autoComplete="email"
                  />
                  <input
                    placeholder={settings.contact_telegram_placeholder}
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
                  {status === "sending"
                    ? settings.contact_submit_loading
                    : settings.contact_submit_text}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
