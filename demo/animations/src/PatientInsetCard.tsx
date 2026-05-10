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
 * PATIENT INSET CARD — "Patient 001 — synthetic FHIR bundle, no PHI."
 *
 * Designed to overlay on top of the screen recording in iMovie.
 * Background is transparent-friendly: the card itself is a small
 * pill, with the rest of the frame transparent so it can float
 * over the live UI footage.
 *
 * Use as Picture-in-Picture in iMovie, anchored top-right.
 *
 * Beats:
 *   00f:    card scales in
 *   12f:    label fades in
 *   75f:    card fades out
 *   90f:    end
 */
export const PatientInsetCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cardScale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 140 },
  });

  const labelProg = interpolate(frame, [12, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const fadeOut = interpolate(frame, [75, 90], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        // Transparent-feeling: very pale cream so it cuts cleanly when
        // chroma-keyed, OR you can use it as a full overlay block.
        backgroundColor: "rgba(247, 242, 232, 0)",
        justifyContent: "flex-start",
        alignItems: "flex-end",
        padding: 80,
        opacity: fadeOut,
      }}
    >
      <div
        style={{
          background: theme.bg,
          border: `1.5px solid ${theme.line}`,
          borderRadius: 18,
          padding: "20px 28px",
          display: "flex",
          alignItems: "center",
          gap: 18,
          boxShadow: "0 12px 36px rgba(27,42,32,0.12)",
          fontFamily: theme.sans,
          transform: `scale(${cardScale})`,
          transformOrigin: "top right",
        }}
      >
        {/* Status dot */}
        <div
          style={{
            width: 12,
            height: 12,
            borderRadius: "50%",
            background: theme.accent,
            flexShrink: 0,
            boxShadow: `0 0 0 4px ${theme.accentSoft}`,
          }}
        />

        {/* Text */}
        <div
          style={{
            opacity: labelProg,
            transform: `translateY(${(1 - labelProg) * 4}px)`,
          }}
        >
          <div
            style={{
              fontSize: 13,
              fontWeight: 700,
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              color: theme.accent,
              marginBottom: 4,
            }}
          >
            Patient 001
          </div>
          <div
            style={{
              fontSize: 18,
              color: theme.ink,
              fontWeight: 500,
            }}
          >
            Synthetic FHIR bundle · No PHI
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
