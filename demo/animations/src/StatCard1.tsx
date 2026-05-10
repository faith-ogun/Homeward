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
 * STAT CARD 1 — "67%" of surgery is now outpatient or short-stay.
 *
 * Source: AHRQ HCUP, 2017 (Steiner et al., Statistical Brief #223).
 *
 * Beats:
 *   00–22f: number rises from 0 → 67
 *   22f:    "%" punches in
 *   30f:    label fades up under the number
 *   60f:    eyebrow tag slides in
 *   90f:    accent underline draws
 *   120f+:  hold
 */
export const StatCard1: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Counter: 0 → 67 over the first 22 frames.
  const countProgress = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 90, mass: 0.8 },
  });
  const count = Math.round(67 * countProgress);

  // Percent sign: pop after the count completes.
  const pctScale = spring({
    frame: frame - 22,
    fps,
    config: { damping: 12, stiffness: 180 },
  });

  // Label fade.
  const labelOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelLift = interpolate(frame, [30, 50], [16, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Eyebrow tag.
  const eyebrowOpacity = interpolate(frame, [60, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const eyebrowLift = interpolate(frame, [60, 80], [10, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Underline draw.
  const underline = interpolate(frame, [90, 120], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Source line.
  const sourceOpacity = interpolate(frame, [80, 100], [0, 1], {
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
      {/* Eyebrow tag */}
      <div
        style={{
          display: "inline-block",
          alignSelf: "flex-start",
          fontSize: 18,
          fontWeight: 600,
          letterSpacing: "0.16em",
          textTransform: "uppercase",
          color: theme.accent,
          backgroundColor: theme.accentSoft,
          padding: "10px 20px",
          borderRadius: 999,
          marginBottom: 36,
          opacity: eyebrowOpacity,
          transform: `translateY(${eyebrowLift}px)`,
        }}
      >
        Blind spot one
      </div>

      {/* Number */}
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          gap: 8,
          fontFamily: theme.serif,
          color: theme.ink,
          lineHeight: 0.95,
        }}
      >
        <span
          style={{
            fontSize: 360,
            fontWeight: 500,
            letterSpacing: "-0.04em",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {count}
        </span>
        <span
          style={{
            fontSize: 220,
            fontWeight: 500,
            color: theme.accent,
            transform: `scale(${pctScale})`,
            transformOrigin: "left bottom",
            display: "inline-block",
          }}
        >
          %
        </span>
      </div>

      {/* Underline accent */}
      <div
        style={{
          marginTop: 24,
          height: 6,
          width: 320,
          backgroundColor: theme.accent,
          borderRadius: 3,
          transform: `scaleX(${underline})`,
          transformOrigin: "left center",
        }}
      />

      {/* Label */}
      <div
        style={{
          marginTop: 40,
          fontFamily: theme.serif,
          fontWeight: 500,
          fontSize: 56,
          lineHeight: 1.15,
          letterSpacing: "-0.01em",
          maxWidth: 1100,
          color: theme.ink,
          opacity: labelOpacity,
          transform: `translateY(${labelLift}px)`,
        }}
      >
        of surgery is now performed in <em style={{ color: theme.accent, fontStyle: "italic" }}>outpatient or short-stay</em> settings.
      </div>

      {/* Source */}
      <div
        style={{
          marginTop: 32,
          fontSize: 22,
          color: theme.muted,
          opacity: sourceOpacity,
        }}
      >
        AHRQ HCUP, 2017
      </div>
    </AbsoluteFill>
  );
};
