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
 * FINAL CARD — closing the loop.
 *
 *   Title:    "Bringing the post-surgical blind spot under one roof."
 *   Subtitle: "Built on A2A, MCP, FHIR, and SHARP."
 *   Wordmark: Homeward
 *
 * Beats:
 *   00f:    background gradient eases up
 *   8f:     wordmark "Homeward" scales in
 *   24f:    headline lifts in
 *   60f:    standards row fades in (A2A · MCP · FHIR · SHARP)
 *   90f:    URL pill fades in
 *   135f+:  hold
 */
export const FinalCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const wordmarkScale = spring({
    frame: frame - 8,
    fps,
    config: { damping: 14, stiffness: 110 },
  });

  const headlineProg = interpolate(frame, [24, 48], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const standardsProg = interpolate(frame, [60, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const urlProg = interpolate(frame, [90, 110], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at center, ${theme.bg2} 0%, ${theme.bg} 70%)`,
        fontFamily: theme.sans,
        color: theme.ink,
        padding: 96,
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
      }}
    >
      {/* Wordmark */}
      <div
        style={{
          fontFamily: theme.serif,
          fontSize: 140,
          fontWeight: 500,
          letterSpacing: "-0.025em",
          color: theme.ink,
          marginBottom: 32,
          transform: `scale(${wordmarkScale})`,
        }}
      >
        <em style={{ fontStyle: "italic", color: theme.accent }}>Home</em>ward
      </div>

      {/* Headline */}
      <div
        style={{
          fontFamily: theme.serif,
          fontSize: 56,
          fontWeight: 400,
          fontStyle: "italic",
          lineHeight: 1.15,
          letterSpacing: "-0.01em",
          color: theme.ink2,
          maxWidth: 1100,
          opacity: headlineProg,
          transform: `translateY(${(1 - headlineProg) * 14}px)`,
        }}
      >
        Bringing the post-surgical blind spot under one roof.
      </div>

      {/* Standards row */}
      <div
        style={{
          marginTop: 72,
          display: "flex",
          gap: 28,
          alignItems: "center",
          opacity: standardsProg,
          transform: `translateY(${(1 - standardsProg) * 10}px)`,
        }}
      >
        {["A2A", "MCP", "FHIR", "SHARP"].map((s, i, arr) => (
          <React.Fragment key={s}>
            <div
              style={{
                fontSize: 22,
                fontWeight: 600,
                letterSpacing: "0.16em",
                color: theme.accent,
              }}
            >
              {s}
            </div>
            {i < arr.length - 1 && (
              <div
                style={{
                  width: 6,
                  height: 6,
                  borderRadius: "50%",
                  background: theme.line,
                }}
              />
            )}
          </React.Fragment>
        ))}
      </div>

      {/* URL pill */}
      <div
        style={{
          marginTop: 56,
          display: "flex",
          gap: 16,
          alignItems: "center",
          padding: "14px 28px",
          background: theme.ink,
          color: theme.bg,
          borderRadius: 999,
          fontSize: 18,
          fontFamily:
            "'SF Mono', 'Menlo', Consolas, monospace",
          opacity: urlProg,
          transform: `translateY(${(1 - urlProg) * 8}px)`,
          letterSpacing: "0.01em",
        }}
      >
        <span
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: "#7BBF8E",
            boxShadow: "0 0 12px #7BBF8E",
          }}
        />
        homeward-434257808344.us-central1.run.app
      </div>
    </AbsoluteFill>
  );
};
