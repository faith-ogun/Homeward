import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
} from "remotion";
import { theme } from "./theme";

/**
 * SAFETY PANEL — three icons fading in.
 *
 *   1. Synthetic data only — no PHI
 *   2. CPIC-cited evidence — deterministic
 *   3. Clinician approves every draft
 *
 * Beats:
 *   00f:    eyebrow tag
 *   12f:    headline lifts in
 *   30f:    icon 1 fades up
 *   48f:    icon 2 fades up
 *   66f:    icon 3 fades up
 *   90f:    closing line fades up
 *   120f+:  hold
 */

const ICONS = [
  {
    glyph: "shield",
    title: "Synthetic data only",
    detail: "No PHI ever touches the system. Four hand-built FHIR bundles for the demo.",
  },
  {
    glyph: "book",
    title: "CPIC-cited evidence",
    detail: "Every drug-gene flag carries a citation. Deterministic lookup; no fabrication.",
  },
  {
    glyph: "check",
    title: "Clinician approves",
    detail: "Drafts are status='draft', intent='proposal'. Nothing reaches the EHR without review.",
  },
] as const;

const Icon: React.FC<{ glyph: (typeof ICONS)[number]["glyph"] }> = ({ glyph }) => {
  const stroke = theme.accent;
  const w = 56;
  switch (glyph) {
    case "shield":
      return (
        <svg width={w} height={w} viewBox="0 0 24 24" fill="none">
          <path
            d="M12 3l8 3v6c0 4.5-3.5 8.5-8 9-4.5-.5-8-4.5-8-9V6l8-3z"
            stroke={stroke}
            strokeWidth={1.8}
            fill={theme.accentSoft}
          />
          <path
            d="M9 12l2.2 2.2L15.5 10"
            stroke={stroke}
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
        </svg>
      );
    case "book":
      return (
        <svg width={w} height={w} viewBox="0 0 24 24" fill="none">
          <path
            d="M4 5a2 2 0 012-2h13v17H6a2 2 0 01-2-2V5z"
            stroke={stroke}
            strokeWidth={1.8}
            fill={theme.accentSoft}
          />
          <path
            d="M4 18a2 2 0 012-2h13"
            stroke={stroke}
            strokeWidth={1.8}
            fill="none"
          />
          <path
            d="M8 8h7M8 11h7"
            stroke={stroke}
            strokeWidth={1.6}
            strokeLinecap="round"
          />
        </svg>
      );
    case "check":
      return (
        <svg width={w} height={w} viewBox="0 0 24 24" fill="none">
          <circle
            cx={12}
            cy={12}
            r={10}
            stroke={stroke}
            strokeWidth={1.8}
            fill={theme.accentSoft}
          />
          <path
            d="M7.5 12.5l3 3 6-6.5"
            stroke={stroke}
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
        </svg>
      );
  }
};

export const SafetyPanel: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrowProg = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const headlineProg = interpolate(frame, [12, 36], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const iconProg = (i: number) => {
    const start = 30 + i * 18;
    return interpolate(frame, [start, start + 18], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  };

  const closingProg = interpolate(frame, [90, 110], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.bg,
        fontFamily: theme.sans,
        color: theme.ink,
        padding: 96,
        justifyContent: "center",
      }}
    >
      <div
        style={{
          alignSelf: "flex-start",
          fontSize: 18,
          fontWeight: 600,
          letterSpacing: "0.16em",
          textTransform: "uppercase",
          color: theme.accent,
          backgroundColor: theme.accentSoft,
          padding: "10px 20px",
          borderRadius: 999,
          marginBottom: 28,
          opacity: eyebrowProg,
        }}
      >
        Decision support, not autonomous prescribing
      </div>

      <div
        style={{
          fontFamily: theme.serif,
          fontSize: 60,
          fontWeight: 500,
          lineHeight: 1.1,
          letterSpacing: "-0.015em",
          color: theme.ink,
          marginBottom: 64,
          maxWidth: 1200,
          opacity: headlineProg,
          transform: `translateY(${(1 - headlineProg) * 14}px)`,
        }}
      >
        Three guardrails. <em style={{ color: theme.accent, fontStyle: "italic" }}>No exceptions.</em>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gap: 28,
        }}
      >
        {ICONS.map((icon, i) => {
          const p = iconProg(i);
          return (
            <div
              key={icon.title}
              style={{
                background: theme.bg2,
                border: `1.5px solid ${theme.line}`,
                borderRadius: 20,
                padding: 36,
                opacity: p,
                transform: `translateY(${(1 - p) * 18}px)`,
              }}
            >
              <div style={{ marginBottom: 20 }}>
                <Icon glyph={icon.glyph} />
              </div>
              <div
                style={{
                  fontFamily: theme.serif,
                  fontSize: 28,
                  fontWeight: 500,
                  lineHeight: 1.2,
                  color: theme.ink,
                  marginBottom: 12,
                  letterSpacing: "-0.01em",
                }}
              >
                {icon.title}
              </div>
              <div
                style={{
                  fontSize: 16,
                  lineHeight: 1.5,
                  color: theme.ink2,
                }}
              >
                {icon.detail}
              </div>
            </div>
          );
        })}
      </div>

      <div
        style={{
          marginTop: 40,
          fontSize: 18,
          color: theme.muted,
          opacity: closingProg,
          alignSelf: "flex-end",
        }}
      >
        HIPAA- and GDPR-compatible by construction.
      </div>
    </AbsoluteFill>
  );
};
