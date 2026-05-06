import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { theme } from "./theme";

/**
 * SPECTRUM CARD — Same gene (CYP2D6), two opposite catastrophes.
 *
 * Left end:  Poor metabolizer  → no morphine  → no pain relief
 * Right end: Ultra-rapid       → morphine surge → toxicity risk
 *
 * Beats:
 *   00f:    eyebrow tag
 *   12f:    "CYP2D6" label scale-pops
 *   30f:    spectrum track draws left → right
 *   60f:    LEFT enzyme + label fade in
 *   80f:    RIGHT enzyme + label fade in (with red pulse)
 *   120f+:  hold; right enzyme keeps a soft pulse
 */

// Reusable label block under each end of the spectrum.
const EndLabel: React.FC<{
  title: string;
  detail: string;
  align: "left" | "right";
  opacity: number;
  lift: number;
  accentColor: string;
}> = ({ title, detail, align, opacity, lift, accentColor }) => (
  <div
    style={{
      maxWidth: 460,
      textAlign: align,
      opacity,
      transform: `translateY(${lift}px)`,
    }}
  >
    <div
      style={{
        fontSize: 14,
        fontWeight: 700,
        letterSpacing: "0.18em",
        textTransform: "uppercase",
        color: accentColor,
        marginBottom: 12,
      }}
    >
      {title}
    </div>
    <div
      style={{
        fontFamily: theme.serif,
        fontSize: 36,
        lineHeight: 1.2,
        fontWeight: 500,
        color: theme.ink,
        letterSpacing: "-0.01em",
      }}
    >
      {detail}
    </div>
  </div>
);

// Stylised enzyme glyph: a circle with three "active site" notches.
// `active` toggles the visual state (greyed-out vs glowing).
const EnzymeGlyph: React.FC<{
  active: boolean;
  pulse: number;
  size: number;
}> = ({ active, pulse, size }) => {
  const fill = active ? "#C0392B" : theme.line;
  const stroke = active ? "#8B1A0E" : theme.muted;
  const glow = active ? `0 0 ${24 + pulse * 12}px rgba(192,57,43,${0.45 + pulse * 0.25})` : "none";

  return (
    <div
      style={{
        position: "relative",
        width: size,
        height: size,
        boxShadow: glow,
        borderRadius: "50%",
      }}
    >
      <svg width={size} height={size} viewBox="0 0 100 100">
        {/* Body */}
        <circle cx={50} cy={50} r={42} fill={fill} stroke={stroke} strokeWidth={3} />
        {/* Active sites */}
        <circle cx={50} cy={14} r={9} fill={fill} stroke={stroke} strokeWidth={3} />
        <circle cx={84} cy={66} r={9} fill={fill} stroke={stroke} strokeWidth={3} />
        <circle cx={16} cy={66} r={9} fill={fill} stroke={stroke} strokeWidth={3} />
        {active ? (
          // Faint inner heat
          <circle cx={50} cy={50} r={22} fill="#E74C3C" opacity={0.55 + pulse * 0.25} />
        ) : (
          // Slash through
          <line
            x1={26}
            y1={26}
            x2={74}
            y2={74}
            stroke={theme.muted}
            strokeWidth={4}
            strokeLinecap="round"
          />
        )}
      </svg>
    </div>
  );
};

export const SpectrumCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const eyebrowProg = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const geneScale = spring({
    frame: frame - 12,
    fps,
    config: { damping: 14, stiffness: 110 },
  });

  // Track draws left → right.
  const trackProg = interpolate(frame, [30, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Left enzyme + label.
  const leftFade = interpolate(frame, [60, 82], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Right enzyme + label.
  const rightFade = interpolate(frame, [80, 102], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Right-side glow pulse, runs continuously after frame 100.
  const pulse =
    frame > 100
      ? 0.5 + 0.5 * Math.sin((frame - 100) / 6)
      : 0;

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
      {/* Eyebrow */}
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
          transform: `translateY(${(1 - eyebrowProg) * 10}px)`,
        }}
      >
        Same gene, two catastrophes
      </div>

      {/* Gene label */}
      <div
        style={{
          alignSelf: "center",
          fontFamily: theme.serif,
          fontSize: 80,
          fontWeight: 500,
          color: theme.ink,
          letterSpacing: "-0.02em",
          marginBottom: 16,
          transform: `scale(${geneScale})`,
        }}
      >
        CYP2D6
      </div>
      <div
        style={{
          alignSelf: "center",
          fontSize: 20,
          color: theme.muted,
          marginBottom: 56,
          opacity: geneScale,
        }}
      >
        Same drug. Same dose. Two opposite outcomes.
      </div>

      {/* Spectrum track */}
      <div
        style={{
          position: "relative",
          width: "100%",
          height: 6,
          background: theme.line,
          borderRadius: 3,
          marginBottom: 40,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `linear-gradient(90deg, ${theme.muted} 0%, ${theme.accentSoft} 50%, #C0392B 100%)`,
            transform: `scaleX(${trackProg})`,
            transformOrigin: "left center",
          }}
        />
        {/* Center tick */}
        <div
          style={{
            position: "absolute",
            top: -8,
            left: "50%",
            transform: "translateX(-50%)",
            width: 2,
            height: 22,
            background: theme.ink,
            opacity: trackProg * 0.6,
          }}
        />
      </div>
      <div
        style={{
          width: "100%",
          textAlign: "center",
          fontSize: 16,
          color: theme.muted,
          marginTop: -28,
          marginBottom: 56,
          opacity: trackProg * 0.7,
          letterSpacing: "0.04em",
        }}
      >
        normal range
      </div>

      {/* Two ends row */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          gap: 48,
        }}
      >
        {/* LEFT end */}
        <div
          style={{
            display: "flex",
            alignItems: "flex-start",
            gap: 28,
          }}
        >
          <div style={{ opacity: leftFade, transform: `scale(${0.85 + 0.15 * leftFade})` }}>
            <EnzymeGlyph active={false} pulse={0} size={140} />
          </div>
          <EndLabel
            title="Poor metabolizer"
            detail="No morphine conversion. No pain relief."
            align="left"
            opacity={leftFade}
            lift={(1 - leftFade) * 12}
            accentColor={theme.muted}
          />
        </div>

        {/* RIGHT end */}
        <div
          style={{
            display: "flex",
            alignItems: "flex-start",
            gap: 28,
            flexDirection: "row-reverse",
          }}
        >
          <div style={{ opacity: rightFade, transform: `scale(${0.85 + 0.15 * rightFade})` }}>
            <EnzymeGlyph active={true} pulse={pulse} size={140} />
          </div>
          <EndLabel
            title="Ultra-rapid metabolizer"
            detail="Morphine surge. Toxicity risk."
            align="right"
            opacity={rightFade}
            lift={(1 - rightFade) * 12}
            accentColor="#8B1A0E"
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};
