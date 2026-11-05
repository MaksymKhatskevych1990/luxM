type SiteLogoProps = {
  src?: string;
  alt: string;
  size?: number;
};

export default function SiteLogo({ src, alt, size = 28 }: SiteLogoProps) {
  if (src) {
    return (
      // CMS logos can be local media or an external URL, so keep the original source.
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={src}
        alt={alt}
        width={size * 5}
        height={size}
        className="site-logo"
        style={{ height: size, width: "auto", maxWidth: size * 5 }}
      />
    );
  }

  return (
    <div
      className="logo-mark"
      aria-hidden="true"
      style={{ width: size, height: size }}
    >
      <span />
      <span />
      <span />
      <span />
    </div>
  );
}
