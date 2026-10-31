"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { submitLead } from "@/lib/api";
import { trackEvent, trackHref } from "@/lib/analytics";
import { formatOpeningHours } from "@/lib/hours";
import { phoneDigits, telHref } from "@/lib/phone";
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
  const [hpField, setHpField] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const sendingRef = useRef(false);
  const successRef = useRef<HTMLHeadingElement>(null);
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");
  const [error, setError] = useState("");

  useEffect(() => {
    if (status === "success") successRef.current?.focus();
  }, [status]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (sendingRef.current) return;
    if (!name.trim() || !phone.trim()) {
      setStatus("error");
      setError(settings.contact_validation_message);
      return;
    }

    const digits = phoneDigits(phone);
    if (digits.length < 10 || digits.length > 15) {
      setStatus("error");
      setError("Вкажіть коректний телефон: щонайменше 10 цифр.");
      return;
    }

    if (file) {
      const extension = file.name.split(".").pop()?.toLowerCase() ?? "";
      const allowedExtensions = ["jpg", "jpeg", "png", "webp", "heic", "heif", "pdf"];
      const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/heic",
        "image/heif",
        "application/pdf",
        "",
      ];
      if (!allowedExtensions.includes(extension) || !allowedTypes.includes(file.type)) {
        setStatus("error");
        setError("Надішліть фото (JPG, PNG, WEBP, HEIC) або PDF.");
        return;
      }
      if (file.size > 15 * 1024 * 1024) {
        setStatus("error");
        setError("Файл завеликий. Максимум 15 МБ.");
        return;
      }
    }

    sendingRef.current = true;
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
        hp_field: hpField,
      });
      setStatus("success");
      if (!hpField.trim()) {
        trackEvent("generate_lead", { form_id: "enquiry", room_type: room });
      }
    } catch (err) {
      sendingRef.current = false;
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
          href: telHref(settings.phone),
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
    settings.jsonld_opening_hours
      ? {
          label: "Графік",
          value: formatOpeningHours(settings.jsonld_opening_hours),
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
        <div className="contact-split">
          <div className="contact-copy">
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
                color: "rgba(247, 246, 242, 0.82)",
                lineHeight: 1.75,
                margin: "32px 0 0",
                maxWidth: 380,
              }}
            >
              {settings.contact_intro}
            </p>
          </div>
          <div className="contact-list">
              {rows.map((row) => (
                <div key={row.label} className="contact-row">
                  <span className="label label--light" style={{ minWidth: 72 }}>
                    {row.label}
                  </span>
                  {row.href ? (
                    <a
                      href={row.href}
                      {...(row.href.startsWith("http")
                        ? { target: "_blank", rel: "noopener noreferrer" }
                        : {})}
                      onClick={() => trackHref(row.href || "", "contact")}
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

          {status === "success" ? (
              <div className="contact-success">
                <span className="label label--oak" style={{ display: "block", marginBottom: 16 }}>
                  {settings.contact_success_eyebrow}
                </span>
                <h3
                  ref={successRef}
                  tabIndex={-1}
                  className="font-serif"
                  style={{
                    fontSize: "clamp(1.75rem, 3vw, 2.5rem)",
                    color: "var(--c-parchment)",
                    margin: "0 0 16px",
                    lineHeight: 1.2,
                    outline: "none",
                  }}
                >
                  {settings.contact_success_title}
                </h3>
                <p
                  style={{
                    fontFamily: "var(--f-sans)",
                    fontSize: "1rem",
                    color: "rgba(247, 246, 242, 0.82)",
                    lineHeight: 1.7,
                    maxWidth: 360,
                  }}
                >
                  {settings.contact_success_body}
                </p>
              </div>
            ) : (
              <form className="contact-form" onSubmit={onSubmit} noValidate aria-busy={status === "sending"}>
                <div className="contact-form-lead">
                <fieldset className="contact-rooms">
                  <legend className="label label--light">{settings.contact_room_heading}</legend>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                    {rooms.map((item) => (
                      <button
                        key={item.value}
                        type="button"
                        className={`chip${room === item.value ? " on" : ""}`}
                        aria-pressed={room === item.value}
                        onClick={() => setRoom(item.value)}
                      >
                        {item.label}
                      </button>
                    ))}
                  </div>
                </fieldset>

                <div style={{ marginBottom: 28 }}>
                  <label className="sr-only" htmlFor="enquiry-message">
                    {settings.contact_message_placeholder}
                  </label>
                  <textarea
                    id="enquiry-message"
                    name="message"
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
                    id="enquiry-file"
                    name="attachment"
                    type="file"
                    accept="image/jpeg,image/png,image/webp,image/heic,image/heif,application/pdf,.jpg,.jpeg,.png,.webp,.heic,.heif,.pdf"
                    className="contact-file-input"
                    aria-describedby="enquiry-file-hint"
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
                    <span>{file ? file.name : "Додати фото ніші або ескіз"}</span>
                    <span id="enquiry-file-hint" className="contact-file-hint">
                      JPG, PNG, WEBP, HEIC або PDF · до 15 МБ
                    </span>
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
                </div>

                <div className="contact-form-fields">
                <div className="contact-fields">
                  <div>
                    <label className="sr-only" htmlFor="enquiry-name">
                      {settings.contact_name_placeholder}
                    </label>
                    <input
                      id="enquiry-name"
                      name="name"
                      placeholder={settings.contact_name_placeholder}
                      className="f-line"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      autoComplete="name"
                      required
                      aria-invalid={status === "error" && !name.trim()}
                      aria-describedby={status === "error" ? "enquiry-error" : undefined}
                    />
                  </div>
                  <div>
                    <label className="sr-only" htmlFor="enquiry-phone">
                      {settings.contact_phone_placeholder}
                    </label>
                    <input
                      id="enquiry-phone"
                      name="phone"
                      type="tel"
                      inputMode="tel"
                      placeholder={settings.contact_phone_placeholder}
                      className="f-line"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      autoComplete="tel"
                      required
                      aria-invalid={status === "error" && phoneDigits(phone).length < 10}
                      aria-describedby={status === "error" ? "enquiry-error" : undefined}
                    />
                  </div>
                  <div>
                    <label className="sr-only" htmlFor="enquiry-email">
                      {settings.contact_email_placeholder}
                    </label>
                    <input
                      id="enquiry-email"
                      name="email"
                      placeholder={settings.contact_email_placeholder}
                      className="f-line"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      autoComplete="email"
                    />
                  </div>
                  <div>
                    <label className="sr-only" htmlFor="enquiry-telegram">
                      {settings.contact_telegram_placeholder}
                    </label>
                    <input
                      id="enquiry-telegram"
                      name="telegram"
                      placeholder={settings.contact_telegram_placeholder}
                      className="f-line"
                      value={telegram}
                      onChange={(e) => setTelegram(e.target.value)}
                      autoComplete="off"
                    />
                  </div>
                </div>

                <div className="hp-field" aria-hidden="true" inert>
                  <label htmlFor="enquiry-hp">Company</label>
                  <input
                    id="enquiry-hp"
                    name="hp_field"
                    tabIndex={-1}
                    autoComplete="off"
                    value={hpField}
                    onChange={(e) => setHpField(e.target.value)}
                  />
                </div>

                {status === "error" ? (
                  <p id="enquiry-error" role="alert">
                    {error}
                  </p>
                ) : null}

                <button
                  type="submit"
                  disabled={status === "sending"}
                  className="contact-submit"
                >
                  {status === "sending"
                    ? settings.contact_submit_loading
                    : settings.contact_submit_text}
                </button>
                </div>
              </form>
            )}
        </div>
      </div>
    </section>
  );
}
