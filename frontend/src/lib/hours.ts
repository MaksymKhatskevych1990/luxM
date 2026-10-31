const DAYS: Record<string, string> = {
  Mo: "Пн",
  Tu: "Вт",
  We: "Ср",
  Th: "Чт",
  Fr: "Пт",
  Sa: "Сб",
  Su: "Нд",
};

/** Schema.org day codes from the CMS, shown in Ukrainian. Unknown text is kept. */
export function formatOpeningHours(value: string | undefined): string {
  const raw = (value || "").trim();
  if (!raw) return "";
  return raw.replace(
    /\b(Mo|Tu|We|Th|Fr|Sa|Su)(?:\s*-\s*(Mo|Tu|We|Th|Fr|Sa|Su))?/g,
    (_match, start: string, end?: string) =>
      end ? `${DAYS[start]}–${DAYS[end]}` : DAYS[start],
  );
}
