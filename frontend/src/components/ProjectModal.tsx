"use client";

import Image from "next/image";
import { useEffect, useMemo, useState } from "react";
import type { Project, ProjectGalleryImage, SiteSettings } from "@/lib/types";

type ProjectModalProps = {
  project: Project | null;
  settings: SiteSettings;
  onClose: () => void;
};

function pad(n: number) {
  return String(n).padStart(2, "0");
}

function uniquePhotos(urls: string[]) {
  const seen = new Set<string>();
  return urls.filter((url) => {
    if (!url || seen.has(url)) return false;
    seen.add(url);
    return true;
  });
}

export default function ProjectModal({
  project,
  settings,
  onClose,
}: ProjectModalProps) {
  const [stageIndex, setStageIndex] = useState(0);
  const [lightbox, setLightbox] = useState<string | null>(null);

  const gallery = useMemo(() => {
    if (!project) return [] as ProjectGalleryImage[];
    return [...(project.gallery || [])].sort((a, b) => a.order - b.order);
  }, [project]);

  const stages = project?.stages || [];
  const hasVideo = Boolean(project?.video_src);

  const photos = useMemo(() => {
    if (!project) return [] as { url: string; caption: string }[];
    if (gallery.length > 0) {
      return gallery.map((g) => ({ url: g.url, caption: g.caption || project.title }));
    }
    return uniquePhotos([project.image_url, project.detail_image_url]).map((url) => ({
      url,
      caption: project.title,
    }));
  }, [project, gallery]);

  // Layout like homepage cards: large media left, tall photo right, pair below left.
  const tallPhoto = photos[0];
  const pairPhotos = photos.slice(1, 3);
  const morePhotos = photos.slice(3);

  useEffect(() => {
    if (!project) return;
    setStageIndex(0);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        if (lightbox) setLightbox(null);
        else onClose();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = prev;
      window.removeEventListener("keydown", onKey);
    };
  }, [project, onClose, lightbox]);

  useEffect(() => {
    if (!project || hasVideo || stages.length < 2) return;
    const id = window.setInterval(() => {
      setStageIndex((i) => (i + 1) % stages.length);
    }, 3200);
    return () => window.clearInterval(id);
  }, [project, hasVideo, stages.length]);

  if (!project) return null;

  const meta = [
    { label: settings.meta_label_area, value: project.area },
    { label: settings.meta_label_materials, value: project.materials_label },
    { label: settings.meta_label_duration, value: project.duration },
    { label: settings.meta_label_year, value: project.year ? String(project.year) : "" },
    { label: settings.meta_label_location, value: project.location },
  ].filter((m) => m.value);

  const description =
    project.description || project.short_description || project.subtitle || "";

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={project.title}
      onClick={onClose}
      className="project-modal-overlay"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="project-modal-panel"
      >
        <button
          type="button"
          onClick={onClose}
          aria-label="Закрити"
          className="project-modal-close"
        >
          ×
        </button>

        <div className="wrap project-modal-body">
          <header className="project-modal-header">
            <span className="label label--oak">
              {settings.detail_eyebrow_prefix} · {pad(project.order || 1)}
            </span>
            <h2 className="font-serif project-modal-title">{project.title}</h2>
            {project.subtitle || project.short_description ? (
              <p className="project-modal-lead">
                {project.subtitle || project.short_description}
              </p>
            ) : null}
          </header>

          {/* Asymmetric media: video/stages left · tall photo right · pair below */}
          <div className="proj-grid-inner project-modal-media">
            <article className="project-modal-hero">
              {hasVideo ? (
                <video
                  key={project.video_src}
                  controls
                  playsInline
                  poster={project.video_poster || tallPhoto?.url || project.image_url}
                  className="project-modal-video"
                >
                  <source src={project.video_src} />
                </video>
              ) : (
                <div className="project-modal-stages">
                  {stages.length > 0 ? (
                    stages.map((stage, i) => (
                      <Image
                        key={stage.id}
                        src={stage.image_url}
                        alt={stage.title}
                        fill
                        sizes="(max-width: 768px) 100vw, 66vw"
                        style={{
                          objectFit: "cover",
                          opacity: i === stageIndex ? 1 : 0,
                          transition: "opacity 0.8s ease",
                        }}
                      />
                    ))
                  ) : project.image_url ? (
                    <Image
                      src={project.image_url}
                      alt={project.title}
                      fill
                      sizes="(max-width: 768px) 100vw, 66vw"
                      style={{ objectFit: "cover" }}
                    />
                  ) : null}

                  {stages.length > 0 ? (
                    <div className="project-modal-stage-tabs">
                      {stages.map((stage, i) => (
                        <button
                          key={stage.id}
                          type="button"
                          className={`stage-tab${i === stageIndex ? " active" : ""}`}
                          onClick={() => setStageIndex(i)}
                          style={{
                            color:
                              i === stageIndex
                                ? "var(--c-oak)"
                                : "rgba(247,246,242,0.45)",
                          }}
                        >
                          {pad(i + 1)} {stage.title}
                        </button>
                      ))}
                    </div>
                  ) : null}

                </div>
              )}
            </article>

            {tallPhoto ? (
              <button
                type="button"
                onClick={() => setLightbox(tallPhoto.url)}
                className="proj-card project-modal-tall"
                aria-label={tallPhoto.caption || "Відкрити фото"}
              >
                <Image
                  src={tallPhoto.url}
                  alt={tallPhoto.caption}
                  fill
                  className="proj-img"
                  sizes="(max-width: 768px) 100vw, 33vw"
                  style={{ objectFit: "cover" }}
                />
              </button>
            ) : null}

            {pairPhotos.length > 0 ? (
              <div className="proj-pair project-modal-pair">
                {pairPhotos.map((photo, idx) => (
                  <button
                    key={`${photo.url}-${idx}`}
                    type="button"
                    className="proj-card"
                    onClick={() => setLightbox(photo.url)}
                    aria-label={photo.caption || "Відкрити фото"}
                    style={{
                      position: "relative",
                      border: "none",
                      padding: 0,
                      cursor: "zoom-in",
                      background: "var(--c-linen)",
                      aspectRatio: "4 / 3",
                      overflow: "hidden",
                    }}
                  >
                    <Image
                      src={photo.url}
                      alt={photo.caption}
                      fill
                      className="proj-img"
                      sizes="(max-width: 768px) 50vw, 33vw"
                      style={{ objectFit: "cover" }}
                    />
                  </button>
                ))}
              </div>
            ) : null}
          </div>

          <div className="detail-split project-modal-content">
            <div>
              <span className="label">Опис проєкту</span>
              <div className="project-modal-description">{description}</div>

              {morePhotos.length > 0 ? (
                <div className="project-modal-gallery">
                  <span className="label">Галерея</span>
                  <div className="project-modal-gallery-grid">
                    {morePhotos.map((photo, idx) => (
                      <button
                        key={`${photo.url}-more-${idx}`}
                        type="button"
                        onClick={() => setLightbox(photo.url)}
                        aria-label={photo.caption || "Відкрити фото"}
                        className="project-modal-gallery-item"
                      >
                        <Image
                          src={photo.url}
                          alt={photo.caption || ""}
                          fill
                          sizes="160px"
                          style={{ objectFit: "cover" }}
                        />
                      </button>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>

            <aside className="project-modal-aside">
              <span className="label label--oak">
                {settings.detail_number_prefix} {pad(project.order || 1)}
                {project.year ? ` · ${project.year}` : ""}
              </span>
              {project.category ? (
                <p className="font-serif project-modal-category">{project.category}</p>
              ) : null}
              <dl className="project-modal-meta">
                {meta.map((item) => (
                  <div key={item.label}>
                    <dt className="label" style={{ marginBottom: 4 }}>
                      {item.label}
                    </dt>
                    <dd style={{ margin: 0, fontSize: "0.95rem" }}>{item.value}</dd>
                  </div>
                ))}
              </dl>
              {settings.detail_cta_text ? (
                <a
                  href={settings.detail_cta_href || "#contacts"}
                  onClick={onClose}
                  className="cta-invert"
                  style={{ marginTop: 28, display: "inline-flex" }}
                >
                  {settings.detail_cta_text}
                </a>
              ) : null}
            </aside>
          </div>
        </div>
      </div>

      {lightbox ? (
        <div
          role="presentation"
          onClick={() => setLightbox(null)}
          className="project-modal-lightbox"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={lightbox} alt="" className="project-modal-lightbox-img" />
        </div>
      ) : null}
    </div>
  );
}
