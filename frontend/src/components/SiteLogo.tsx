type SiteLogoProps = {
  src?: string;
  alt: string;
  size?: number;
};

export default function SiteLogo({ src, alt, size = 28 }: SiteLogoProps) {
  if (src) {
    return (
      <img
        src={src}
        alt={alt}
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
