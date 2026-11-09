/**
 * Plan of the kitchen in /works/2024-10-08-a.jpg, in the same 16:10 frame
 * the photo uses (object-fit: cover). 160×100 matches that frame.
 */
export default function FloorPlan() {
  const ink = "#252525";
  const oak = "#9A7E55";
  const wash = "rgba(184,155,114,0.08)";

  return (
    <svg
      viewBox="0 0 160 100"
      preserveAspectRatio="xMidYMid meet"
      aria-label="Креслення кутової кухні: пенал, духовки, мийка, вітрина і стіл"
      style={{ width: "100%", height: "100%", display: "block" }}
    >
      <text
        x="4"
        y="5.5"
        fill="#B89B72"
        fontSize="2.1"
        fontFamily="'DM Mono', ui-monospace, monospace"
        letterSpacing="0.12em"
      >
        PROPROSTIR · КУХНЯ КУТОВА · ПЛ.001 · М 1:25
      </text>
      <line x1="4" y1="7.2" x2="156" y2="7.2" stroke="#B89B72" strokeWidth="0.25" />

      <rect x="8" y="24" width="32" height="64" fill={wash} stroke={ink} strokeWidth="0.45" />
      <line x1="26" y1="24" x2="26" y2="88" stroke={ink} strokeWidth="0.3" />
      <line x1="8" y1="42" x2="26" y2="42" stroke={ink} strokeWidth="0.25" strokeDasharray="1.4 0.8" />
      <line x1="8" y1="58" x2="26" y2="58" stroke={ink} strokeWidth="0.25" strokeDasharray="1.4 0.8" />
      <line x1="8" y1="74" x2="26" y2="74" stroke={ink} strokeWidth="0.25" strokeDasharray="1.4 0.8" />
      <text
        x="17"
        y="36"
        fill="#77736C"
        fontSize="1.7"
        fontFamily="'DM Mono', ui-monospace, monospace"
        textAnchor="middle"
        letterSpacing="0.08em"
      >
        Пенал
      </text>

      <rect x="28" y="47" width="10" height="9" fill="rgba(247,246,242,0.55)" stroke={ink} strokeWidth="0.35" />
      <rect x="28" y="58" width="10" height="9" fill="rgba(247,246,242,0.55)" stroke={ink} strokeWidth="0.35" />
      <line x1="29.2" y1="51.5" x2="36.8" y2="51.5" stroke={ink} strokeWidth="0.25" />
      <line x1="29.2" y1="62.5" x2="36.8" y2="62.5" stroke={ink} strokeWidth="0.25" />

      <rect x="40" y="30" width="72" height="20" fill={wash} stroke={ink} strokeWidth="0.4" />
      <line x1="40" y1="40" x2="112" y2="40" stroke={ink} strokeWidth="0.22" strokeDasharray="2 1" />
      <line x1="58" y1="30" x2="58" y2="50" stroke={ink} strokeWidth="0.22" />
      <line x1="76" y1="30" x2="76" y2="50" stroke={ink} strokeWidth="0.22" />
      <line x1="94" y1="30" x2="94" y2="50" stroke={ink} strokeWidth="0.22" />

      <rect x="40" y="61" width="72" height="8" fill="rgba(247,246,242,0.35)" stroke={ink} strokeWidth="0.4" />
      <rect x="70" y="62.4" width="16" height="5.2" fill="none" stroke={ink} strokeWidth="0.35" />
      <circle cx="78" cy="65" r="1.5" fill="none" stroke={ink} strokeWidth="0.3" />
      <circle cx="78" cy="65" r="0.45" fill={ink} />

      <rect x="72" y="68" width="40" height="22" fill={wash} stroke={ink} strokeWidth="0.4" />
      <line x1="72" y1="76" x2="112" y2="76" stroke={ink} strokeWidth="0.22" strokeDasharray="1.6 0.9" />
      <line x1="72" y1="84" x2="112" y2="84" stroke={ink} strokeWidth="0.22" strokeDasharray="1.6 0.9" />

      <rect x="114" y="12" width="18" height="80" fill="rgba(239,237,231,0.45)" stroke={ink} strokeWidth="0.45" />
      <line x1="123" y1="12" x2="123" y2="92" stroke={ink} strokeWidth="0.25" />
      {[24, 36, 48, 60, 72, 84].map((y) => (
        <line key={y} x1="114" y1={y} x2="132" y2={y} stroke={ink} strokeWidth="0.2" />
      ))}
      <text
        x="123"
        y="18"
        fill="#77736C"
        fontSize="1.7"
        fontFamily="'DM Mono', ui-monospace, monospace"
        textAnchor="middle"
        letterSpacing="0.08em"
      >
        Вітрина
      </text>

      <rect x="42" y="73" width="32" height="7" fill="rgba(247,246,242,0.72)" stroke={ink} strokeWidth="0.5" />
      <rect
        x="50"
        y="81"
        width="16"
        height="13"
        rx="3"
        fill="rgba(247,246,242,0.72)"
        stroke={ink}
        strokeWidth="0.4"
      />
      <path d="M52 85 H64" stroke={ink} strokeWidth="0.25" />

      <line x1="78" y1="62.4" x2="100" y2="22" stroke={oak} strokeWidth="0.28" />
      <text
        x="101"
        y="21"
        fill={oak}
        fontSize="1.8"
        fontFamily="'DM Mono', ui-monospace, monospace"
        letterSpacing="0.06em"
      >
        Мийка
      </text>
      <line x1="33" y1="52" x2="48" y2="24" stroke={oak} strokeWidth="0.28" />
      <text
        x="49"
        y="23"
        fill={oak}
        fontSize="1.8"
        fontFamily="'DM Mono', ui-monospace, monospace"
        letterSpacing="0.06em"
      >
        Духовки
      </text>
      <line x1="58" y1="76" x2="78" y2="56" stroke={oak} strokeWidth="0.28" />
      <text
        x="79"
        y="55.5"
        fill={oak}
        fontSize="1.8"
        fontFamily="'DM Mono', ui-monospace, monospace"
        letterSpacing="0.06em"
      >
        Обідній стіл
      </text>
      <text
        x="61"
        y="97"
        textAnchor="middle"
        fill="#77736C"
        fontSize="1.7"
        fontFamily="'DM Mono', ui-monospace, monospace"
        letterSpacing="0.08em"
      >
        ГОРІХ · КАМІНЬ · ОДНЕ КРІСЛО
      </text>
    </svg>
  );
}
