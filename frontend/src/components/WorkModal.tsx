"use client";

import Image from "next/image";
import { useEffect, useMemo, useState } from "react";
import type { SiteSettings, WorkGalleryImage, WorkItem } from "@/lib/types";

type WorkModalProps = {
  item: WorkItem | null;
  settings: SiteSettings;
  onClose: () => void;
};

export default function WorkModal({ item, settings, onClose }: WorkModalProps) {
  const [photoIndex, setPhotoIndex] = useState(0);
  const [lightbox, setLightbox] = useState<string | null>(null);

  const photos = useMemo(() => {
    if (!item) return [] as WorkGalleryImage[];
    const gallery = [...(item.gallery || [])]
      .filter((photo) => photo.url)
      .sort((a, b) => a.order - b.order);
    if (gallery.length > 0) return gallery;
    if (!item.image_url) return [];
    return [
      {
        id: item.id,
        url: item.image_url,
        caption: item.title,
        order: 0,
      },
    ];
  }, [item]);

  useEffect(() => {
    if (!item) return;
    setPhotoIndex(0);
    setLightbox(null);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [item]);

  useEffect(() => {
    if (!item) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        if (lightbox) setLightbox(null);
        else onClose();
        return;
      }
      if (lightbox || photos.length < 2) return;
      if (event.key === "ArrowRight") {
        setPhotoIndex((index) => (index + 1) % photos.length);
      }
      if (event.key === "ArrowLeft") {
        setPhotoIndex((index) => (index - 1 + photos.length) % photos.length);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [item, onClose, lightbox, photos.length]);

  if (!item) return null;

  const photo = photos[photoIndex] ?? photos[0];
  const description = item.description || item.summary;
  const ctaText = settings.detail_cta_text || settings.header_cta_text || "Замовити прорахунок";
  const ctaHref = settings.detail_cta_href || settings.header_cta_href || "#contacts";

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={item.title}
      onClick={onClose}
      className="project-modal-overlay"
    >
      <div onClick={(event) => event.stopPropagation()} className="project-modal-panel">
        <button type="button" onClick={onClose} aria-label="Закрити" className="project-modal-close">
          ×
        </button>

        <div className="wrap project-modal-body">
          <header className="project-modal-header">
            {item.category_name ? <span className="label label--oak">{item.category_name}</span> : null}
            <h2 className="font-serif project-modal-title">{item.title}</h2>
            {item.summary ? <p className="project-modal-lead">{item.summary}</p> : null}
          </header>

          <div className="work-modal-layout">
            <div>
              {photo ? (
                <div className="work-modal-stage">
                  <button
                    type="button"
                    className="work-modal-photo"
                    onClick={() => setLightbox(photo.url)}
                    aria-label={photo.caption || "Відкрити фото"}
                  >
                    <Image
                      src={photo.url}
                      alt={photo.caption || item.title}
                      fill
                      sizes="(max-width: 768px) 100vw, 720px"
                      style={{ objectFit: "cover" }}
                    />
                  </button>
                  {photos.length > 1 ? (
                    <>
                      <button
                        type="button"
                        className="work-modal-nav work-modal-nav--prev"
                        aria-label="Попереднє фото"
                        onClick={() =>
                          setPhotoIndex((index) => (index - 1 + photos.length) % photos.length)
                        }
                      >
                        ‹
                      </button>
                      <button
                        type="button"
                        className="work-modal-nav work-modal-nav--next"
                        aria-label="Наступне фото"
                        onClick={() => setPhotoIndex((index) => (index + 1) % photos.length)}
                      >
                        ›
                      </button>
                      <span className="work-modal-count">
                        {photoIndex + 1} / {photos.length}
                      </span>
                    </>
                  ) : null}
                </div>
              ) : null}

              {photos.length > 1 ? (
                <div className="work-thumbs" role="tablist" aria-label="Фото роботи">
                  {photos.map((thumb, index) => (
                    <button
                      key={thumb.id}
                      type="button"
                      role="tab"
                      aria-selected={index === photoIndex}
                      aria-label={thumb.caption || `Фото ${index + 1}`}
                      className={`work-thumb${index === photoIndex ? " is-active" : ""}`}
                      onClick={() => setPhotoIndex(index)}
                    >
                      <Image
                        src={thumb.url}
                        alt=""
                        fill
                        sizes="96px"
                        style={{ objectFit: "cover" }}
                      />
                    </button>
                  ))}
                </div>
              ) : null}
              {photo?.caption ? <p className="work-caption">{photo.caption}</p> : null}
            </div>

            <aside className="project-modal-aside">
              <span className="label">Тонкощі варіанту</span>
              {description ? <div className="project-modal-description">{description}</div> : null}
              <a href={ctaHref} onClick={onClose} className="cta-invert work-modal-cta">
                {ctaText}
              </a>
            </aside>
          </div>
        </div>
      </div>

      {lightbox ? (
        <div className="project-modal-lightbox" onClick={() => setLightbox(null)}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={lightbox} alt="" className="project-modal-lightbox-img" />
        </div>
      ) : null}
    </div>
  );
}
