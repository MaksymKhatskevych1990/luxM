type FloorPlanProps = {
  idPrefix?: string;
};

export default function FloorPlan({ idPrefix = "fp" }: FloorPlanProps) {
  const a1 = `${idPrefix}-a1`;
  const a2 = `${idPrefix}-a2`;

  return (
    <svg
      viewBox="0 0 560 400"
      aria-label="Технічне креслення"
      style={{ width: "100%", height: "auto", display: "block" }}
    >
      <defs>
        <marker
          id={a1}
          markerWidth="5"
          markerHeight="5"
          refX="2.5"
          refY="2.5"
          orient="auto"
        >
          <path d="M0,0 L5,2.5 L0,5 Z" fill="#9A7E55" />
        </marker>
        <marker
          id={a2}
          markerWidth="5"
          markerHeight="5"
          refX="2.5"
          refY="2.5"
          orient="auto-start-reverse"
        >
          <path d="M0,0 L5,2.5 L0,5 Z" fill="#9A7E55" />
        </marker>
      </defs>
      <text
        x="20"
        y="16"
        fill="#B89B72"
        fontSize="7.5"
        fontFamily="'DM Mono'"
        letterSpacing="0.13em"
      >
        ФОРМА STUDIO · КУХНЯ-ОСТРІВ · ПЛ.001 · М 1:25
      </text>
      <line x1="20" y1="22" x2="540" y2="22" stroke="#B89B72" strokeWidth="0.4" />
      <rect
        x="28"
        y="38"
        width="500"
        height="320"
        fill="none"
        stroke="#252525"
        strokeWidth="1.5"
      />
      <rect
        x="28"
        y="38"
        width="310"
        height="52"
        fill="rgba(184,155,114,0.06)"
        stroke="#252525"
        strokeWidth="0.75"
      />
      <line
        x1="28"
        y1="64"
        x2="338"
        y2="64"
        stroke="#252525"
        strokeWidth="0.4"
        strokeDasharray="6 3"
      />
      <line x1="80" y1="38" x2="80" y2="90" stroke="#252525" strokeWidth="0.4" />
      <line x1="130" y1="38" x2="130" y2="90" stroke="#252525" strokeWidth="0.4" />
      <line x1="180" y1="38" x2="180" y2="90" stroke="#252525" strokeWidth="0.4" />
      <line x1="230" y1="38" x2="230" y2="90" stroke="#252525" strokeWidth="0.4" />
      <line x1="280" y1="38" x2="280" y2="90" stroke="#252525" strokeWidth="0.4" />
      <line x1="54" y1="52" x2="66" y2="52" stroke="#252525" strokeWidth="1.2" />
      <line x1="104" y1="52" x2="116" y2="52" stroke="#252525" strokeWidth="1.2" />
      <line x1="154" y1="52" x2="166" y2="52" stroke="#252525" strokeWidth="1.2" />
      <line x1="204" y1="52" x2="216" y2="52" stroke="#252525" strokeWidth="1.2" />
      <line x1="254" y1="52" x2="266" y2="52" stroke="#252525" strokeWidth="1.2" />
      <rect
        x="28"
        y="38"
        width="52"
        height="220"
        fill="rgba(184,155,114,0.06)"
        stroke="#252525"
        strokeWidth="0.75"
      />
      <line
        x1="28"
        y1="90"
        x2="80"
        y2="90"
        stroke="#252525"
        strokeWidth="0.4"
        strokeDasharray="4 2"
      />
      <line
        x1="28"
        y1="140"
        x2="80"
        y2="140"
        stroke="#252525"
        strokeWidth="0.4"
        strokeDasharray="4 2"
      />
      <line
        x1="28"
        y1="190"
        x2="80"
        y2="190"
        stroke="#252525"
        strokeWidth="0.4"
        strokeDasharray="4 2"
      />
      <line
        x1="28"
        y1="220"
        x2="80"
        y2="220"
        stroke="#252525"
        strokeWidth="0.4"
        strokeDasharray="4 2"
      />
      <rect
        x="148"
        y="168"
        width="260"
        height="132"
        fill="rgba(247,246,242,0.5)"
        stroke="#252525"
        strokeWidth="1.2"
      />
      <rect
        x="152"
        y="172"
        width="252"
        height="124"
        fill="none"
        stroke="#252525"
        strokeWidth="0.4"
        strokeDasharray="5 3"
      />
      <circle cx="200" cy="232" r="20" fill="none" stroke="#252525" strokeWidth="0.65" />
      <circle cx="248" cy="232" r="20" fill="none" stroke="#252525" strokeWidth="0.65" />
      <circle cx="308" cy="232" r="20" fill="none" stroke="#252525" strokeWidth="0.65" />
      <circle cx="356" cy="232" r="20" fill="none" stroke="#252525" strokeWidth="0.65" />
      <text
        x="278"
        y="345"
        textAnchor="middle"
        fill="#77736C"
        fontSize="7"
        fontFamily="'DM Mono'"
        letterSpacing="0.1em"
      >
        ОСТРІВ · ДУБ / КАМІНЬ
      </text>
      <rect
        x="400"
        y="38"
        width="72"
        height="88"
        fill="rgba(239,237,231,0.6)"
        stroke="#252525"
        strokeWidth="0.75"
      />
      <line x1="436" y1="38" x2="436" y2="126" stroke="#252525" strokeWidth="0.4" />
      <text
        x="418"
        y="86"
        fill="#77736C"
        fontSize="6.5"
        fontFamily="'DM Mono'"
        textAnchor="middle"
        letterSpacing="0.06em"
      >
        Хол.
      </text>
      <rect
        x="158"
        y="46"
        width="72"
        height="32"
        fill="none"
        stroke="#252525"
        strokeWidth="0.6"
      />
      <circle cx="194" cy="62" r="11" fill="none" stroke="#252525" strokeWidth="0.5" />
      <circle cx="194" cy="62" r="3" fill="#252525" />
      <line
        x1="28"
        y1="378"
        x2="528"
        y2="378"
        stroke="#9A7E55"
        strokeWidth="0.5"
        markerEnd={`url(#${a1})`}
        markerStart={`url(#${a2})`}
      />
      <text
        x="278"
        y="390"
        textAnchor="middle"
        fill="#9A7E55"
        fontSize="7.5"
        fontFamily="'DM Mono'"
        letterSpacing="0.1em"
      >
        4 200 мм
      </text>
      <line
        x1="548"
        y1="38"
        x2="548"
        y2="358"
        stroke="#9A7E55"
        strokeWidth="0.5"
        markerEnd={`url(#${a1})`}
        markerStart={`url(#${a2})`}
      />
      <text
        x="556"
        y="200"
        textAnchor="middle"
        fill="#9A7E55"
        fontSize="7.5"
        fontFamily="'DM Mono'"
        letterSpacing="0.1em"
        transform="rotate(90,556,200)"
      >
        2 900 мм
      </text>
      <line x1="194" y1="62" x2="300" y2="26" stroke="#B89B72" strokeWidth="0.45" />
      <text
        x="303"
        y="24"
        fill="#B89B72"
        fontSize="7"
        fontFamily="'DM Mono'"
        letterSpacing="0.08em"
      >
        Мийка — нерж. сталь
      </text>
      <line x1="278" y1="168" x2="360" y2="140" stroke="#B89B72" strokeWidth="0.45" />
      <text
        x="363"
        y="138"
        fill="#B89B72"
        fontSize="7"
        fontFamily="'DM Mono'"
        letterSpacing="0.08em"
      >
        Острів 2600×1100
      </text>
    </svg>
  );
}
