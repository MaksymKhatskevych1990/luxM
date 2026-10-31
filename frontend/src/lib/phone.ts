/** `tel:` href with digits only. Parentheses and spaces break some dialers. */
export function telHref(phone: string | undefined): string {
  const trimmed = (phone || "").trim();
  if (!trimmed) return "";
  const hasPlus = trimmed.startsWith("+");
  const digits = trimmed.replace(/\D/g, "");
  if (!digits) return "";
  return `tel:${hasPlus ? "+" : ""}${digits}`;
}

export function phoneDigits(phone: string): string {
  return phone.replace(/\D/g, "");
}
