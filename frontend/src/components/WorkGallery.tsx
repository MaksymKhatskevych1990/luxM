"use client";

import { useState } from "react";
import type { WorkGalleryImage } from "@/lib/types";

type WorkGalleryProps = {
  photos: WorkGalleryImage[];
  title: string;
};

export default function WorkGallery({ photos, title }: WorkGalleryProps) {
  const [index, setIndex] = useState(0);
  const photo = photos[index] ?? photos[0];
  if (!photo) return null;

  const showStrip = photos.length > 1;

  const select = (next: number) => {
    const count = photos.length;
    setIndex((next + count) % count);
  };

  return (
    <div className="work-gallery">
      <figure className="work-gallery-stage">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={photo.url}
          alt={photo.caption || title}
          decoding="async"
          fetchPriority="high"
        />
        {showStrip ? (
          <>
            <button
              type="button"
              className="work-modal-nav work-modal-nav--prev"
              aria-label="Попереднє фото"
              onClick={() => select(index - 1)}
            >
              ‹
            </button>
            <button
              type="button"
              className="work-modal-nav work-modal-nav--next"
              aria-label="Наступне фото"
              onClick={() => select(index + 1)}
            >
              ›
            </button>
          </>
        ) : null}
        {photo.caption ? <figcaption>{photo.caption}</figcaption> : null}
      </figure>

      {showStrip ? (
        <div className="work-gallery-thumbs" role="tablist" aria-label="Фото роботи">
          {photos.map((thumb, thumbIndex) => {
            const selected = thumbIndex === index;
            return (
              <button
                key={thumb.id}
                type="button"
                role="tab"
                aria-selected={selected}
                aria-label={thumb.caption || `Фото ${thumbIndex + 1}`}
                className={`work-gallery-thumb${selected ? " is-active" : ""}`}
                onClick={() => select(thumbIndex)}
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={thumb.url} alt="" />
              </button>
            );
          })}
        </div>
      ) : null}
    </div>
  );
}
