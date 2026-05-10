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
 * PIPELINE CUTAWAY — five nodes lighting up in sequence as Homeward
 * processes the consult.
 *
 *   FHIR fetch → Discharge interpretation → PGx review → Recovery
 *   assessment → Escalation
 *
 * Beats:
 *   00f:    eyebrow fades in, all nodes drawn dim
 *   12f:    node 1 lights up + connector to 2 draws
 *   30f:    node 2 lights up + connector to 3 draws
 *   48f:    node 3 lights up + connector to 4 draws
 *   66f:    node 4 lights up + connector to 5 draws
 *   84f:    node 5 lights up
 *   105f:   final "AMBER" badge pops in
 *   135f+:  hold
 */

type Node = {
  label: string;
  detail: string;
};

const NODES: Node[] = [
  { label: "FHIR Fetch", detail: "Procedure · Meds · PGx panel" },
  { label: "Discharge", detail: "Note → structured timeline" },
  { label: "PGx Review", detail: "CPIC + ClinVar lookup" },
  { label: "Recovery", detail: "Symptom vs. expected curve" },
  { label: "Escalation", detail: "GREEN · AMBER · RED" },
];

const NODE_LIGHT_DELAY = 18;
const FIRST_NODE_FRAME = 12;

export const PipelineCutaway: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const eyebrowProg = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Light progress per node: 0 dim → 1 fully lit
  const nodeLight = (i: number) => {
    const start = FIRST_NODE_FRAME + i * NODE_LIGHT_DELAY;
    return interpolate(frame, [start, start + 12], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  };

  // Connector fill between i and i+1
  const connectorFill = (i: number) => {
    const start = FIRST_NODE_FRAME + i * NODE_LIGHT_DELAY + 6;
    return interpolate(frame, [start, start + 14], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  };

  // Final AMBER badge
  const badgeScale = spring({
    frame: frame - 105,
    fps,
    config: { damping: 14, stiffness: 140 },
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
          marginBottom: 56,
          opacity: eyebrowProg,
        }}
      >
        Inside the consult
      </div>

      {/* Pipeline */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 0,
          marginBottom: 64,
        }}
      >
        {NODES.map((node, i) => {
          const light = nodeLight(i);
          const dim = 0.25 + 0.75 * light;
          return (
            <React.Fragment key={node.label}>
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 14,
                  flexShrink: 0,
                  width: 220,
                }}
              >
                {/* Node circle */}
                <div
                  style={{
                    width: 80,
                    height: 80,
                    borderRadius: "50%",
                    background:
                      light > 0.4 ? theme.accent : theme.line,
                    border: `3px solid ${
                      light > 0.4 ? theme.ink : theme.muted
                    }`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontFamily: theme.serif,
                    fontSize: 28,
                    fontWeight: 600,
                    color:
                      light > 0.4 ? theme.bg : theme.muted,
                    boxShadow:
                      light > 0.6
                        ? `0 0 ${24 + light * 24}px ${theme.accent}66`
                        : "none",
                    transition: "all 0.05s",
                  }}
                >
                  {String(i + 1).padStart(2, "0")}
                </div>

                {/* Label */}
                <div
                  style={{
                    textAlign: "center",
                    opacity: dim,
                  }}
                >
                  <div
                    style={{
                      fontFamily: theme.serif,
                      fontSize: 22,
                      fontWeight: 500,
                      color: theme.ink,
                      marginBottom: 4,
                    }}
                  >
                    {node.label}
                  </div>
                  <div
                    style={{
                      fontSize: 14,
                      color: theme.muted,
                      lineHeight: 1.35,
                    }}
                  >
                    {node.detail}
                  </div>
                </div>
              </div>

              {/* Connector */}
              {i < NODES.length - 1 && (
                <div
                  style={{
                    flex: 1,
                    height: 4,
                    background: theme.line,
                    borderRadius: 2,
                    position: "relative",
                    overflow: "hidden",
                    marginTop: -54, // align with node center
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      inset: 0,
                      background: theme.accent,
                      transform: `scaleX(${connectorFill(i)})`,
                      transformOrigin: "left center",
                    }}
                  />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* AMBER outcome badge */}
      <div
        style={{
          alignSelf: "center",
          transform: `scale(${badgeScale})`,
          display: "flex",
          alignItems: "center",
          gap: 18,
          padding: "20px 36px",
          borderRadius: 999,
          background: "#E8A93D",
          color: theme.ink,
          fontFamily: theme.serif,
          fontSize: 36,
          fontWeight: 600,
          letterSpacing: "0.04em",
          boxShadow: "0 12px 36px rgba(232,169,61,0.35)",
        }}
      >
        <span style={{ fontSize: 28 }}>●</span>
        AMBER · Recovery deviation detected
      </div>
    </AbsoluteFill>
  );
};
