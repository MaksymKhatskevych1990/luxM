export function isEnquiryHref(href: string | undefined): boolean {
  const value = (href || "").trim().toLowerCase();
  if (!value) return false;
  return (
    value.includes("contact") ||
    value.startsWith("tel:") ||
    value.startsWith("mailto:") ||
    value.includes("wa.me") ||
    value.includes("t.me/")
  );
}
