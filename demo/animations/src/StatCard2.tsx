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
 * STAT CARD 2 — Post-operative complications: 3rd leading cause of death
 * worldwide.
 *
 * Beats:
 *   00f:    eyebrow tag slides in
 *   12f:    "3rd" number scale-pops
 *   30f:    headline lifts in
 *   60f:    bar visualization animates (1st, 2nd, 3rd; 3rd highlighted)
 *   105f:   source line fades up
 *   135f+:  hold
 */
export const StatCard2: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const eyebrowProg = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const numberScale = spring({
    frame: frame - 12,
    fps,
    config: { damping: 14, stiffness: 110 },
  });

  const headlineProg = interpolate(frame, [30, 55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const sourceProg = interpolate(frame, [105, 130], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Bars draw from frame 60 onwards. Each bar staggers in.
  const barProgress = (delay: number) =>
    interpolate(frame, [60 + delay, 95 + delay], [0, 1], {
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
          marginBottom: 32,
          opacity: eyebrowProg,
          transform: `translateY(${(1 - eyebrowProg) * 10}px)`,
        }}
      >
        The post-discharge gap
      </div>

      {/* "3rd" number + headline row */}
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          gap: 56,
        }}
      >
        <div
          style={{
            fontFamily: theme.serif,
            fontSize: 320,
            fontWeight: 500,
            color: theme.accent,
            lineHeight: 0.95,
            letterSpacing: "-0.03em",
            transform: `scale(${numberScale})`,
            transformOrigin: "left top",
          }}
        >
          3<sup style={{ fontSize: 140, top: "-0.5em", marginLeft: 8 }}>rd</sup>
        </div>

        <div
          style={{
            fontFamily: theme.serif,
            fontWeight: 500,
            fontSize: 60,
            lineHeight: 1.1,
            letterSpacing: "-0.01em",
            color: theme.ink,
            maxWidth: 720,
            opacity: headlineProg,
            transform: `translateY(${(1 - headlineProg) * 16}px)`,
            paddingTop: 48,
          }}
        >
          leading cause of death worldwide is{" "}
          <em style={{ color: theme.accent, fontStyle: "italic" }}>
            post-operative complication.
          </em>
        </div>
      </div>

      {/* Bar visualisation */}
      <div
        style={{
          marginTop: 64,
          display: "flex",
          gap: 24,
          alignItems: "flex-end",
          height: 200,
        }}
      >
        {[
          { label: "1st", value: 1.0, highlight: false },
          { label: "2nd", value: 0.85, highlight: false },
          { label: "3rd · post-op", value: 0.72, highlight: true },
        ].map((bar, i) => {
          const p = barProgress(i * 12);
          return (
            <div
              key={bar.label}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 12,
              }}
            >
              <div
                style={{
                  width: 120,
                  height: `${bar.value * 200 * p}px`,
                  backgroundColor: bar.highlight ? theme.accent : theme.line,
                  borderRadius: 8,
                  transition: "all 0.2s",
                }}
              />
              <div
                style={{
                  fontSize: 22,
                  fontWeight: bar.highlight ? 600 : 400,
                  color: bar.highlight ? theme.ink : theme.muted,
                  opacity: p,
                  fontFamily: theme.sans,
                }}
              >
                {bar.label}
              </div>
            </div>
          );
        })}
      </div>

      {/* Source */}
      <div
        style={{
          marginTop: 56,
          fontSize: 22,
          color: theme.muted,
          opacity: sourceProg,
          transform: `translateY(${(1 - sourceProg) * 8}px)`,
        }}
      >
        Nepogodiev et al., The Lancet, 2019
      </div>
    </AbsoluteFill>
  );
};
