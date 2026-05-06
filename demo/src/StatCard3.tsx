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
 * STAT CARD 3 — "99%" of people carry an actionable pharmacogenomic variant.
 *
 * Source: PREPARE study (Swen et al., Lancet 2023);
 * supporting reference: Van Driest et al., 2014.
 *
 * Beats:
 *   00f:    eyebrow + DNA helix start drawing in
 *   12–32f: helix rungs draw in over time
 *   30f:    "99%" number scale-pops on the right
 *   55f:    headline lifts up
 *   95f:    source line fades up
 *   135f+:  helix continues to rotate slowly through the hold
 */

const HELIX_NODES = 14; // pairs of base nodes
const HELIX_HEIGHT = 720;
const HELIX_WIDTH = 220;

const Helix: React.FC<{ frame: number; fps: number }> = ({ frame }) => {
  const phase = (frame / 120) * Math.PI * 2; // slow rotation
  const drawIn = (i: number) =>
    interpolate(frame, [12 + i * 1.4, 28 + i * 1.4], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  const cx = HELIX_WIDTH / 2;

  const nodes = Array.from({ length: HELIX_NODES }).map((_, i) => {
    const t = (i / (HELIX_NODES - 1)) * Math.PI * 2.4; // wraps ~1.2 turns
    const xLeft = cx + Math.sin(t + phase) * (HELIX_WIDTH / 2 - 14);
    const xRight = cx + Math.sin(t + phase + Math.PI) * (HELIX_WIDTH / 2 - 14);
    const y = (i / (HELIX_NODES - 1)) * (HELIX_HEIGHT - 28) + 14;

    // Depth cue: scale + opacity based on which strand is "in front"
    const zLeft = Math.cos(t + phase);
    const zRight = Math.cos(t + phase + Math.PI);
    const opacityLeft = 0.45 + 0.55 * ((zLeft + 1) / 2);
    const opacityRight = 0.45 + 0.55 * ((zRight + 1) / 2);
    const scaleLeft = 0.7 + 0.3 * ((zLeft + 1) / 2);
    const scaleRight = 0.7 + 0.3 * ((zRight + 1) / 2);

    const draw = drawIn(i);

    return {
      i,
      xLeft,
      xRight,
      y,
      opacityLeft,
      opacityRight,
      scaleLeft,
      scaleRight,
      draw,
    };
  });

  return (
    <svg
      width={HELIX_WIDTH}
      height={HELIX_HEIGHT}
      viewBox={`0 0 ${HELIX_WIDTH} ${HELIX_HEIGHT}`}
      style={{ overflow: "visible" }}
    >
      {/* Rungs (rendered first so circles sit above) */}
      {nodes.map((n) => (
        <line
          key={`rung-${n.i}`}
          x1={n.xLeft}
          y1={n.y}
          x2={n.xRight}
          y2={n.y}
          stroke={theme.accent}
          strokeWidth={2.5}
          strokeOpacity={0.45 * n.draw}
        />
      ))}

      {/* Strand A */}
      {nodes.map((n) => (
        <circle
          key={`a-${n.i}`}
          cx={n.xLeft}
          cy={n.y}
          r={9 * n.scaleLeft}
          fill={theme.ink}
          opacity={n.opacityLeft * n.draw}
        />
      ))}

      {/* Strand B */}
      {nodes.map((n) => (
        <circle
          key={`b-${n.i}`}
          cx={n.xRight}
          cy={n.y}
          r={9 * n.scaleRight}
          fill={theme.accent}
          opacity={n.opacityRight * n.draw}
        />
      ))}
    </svg>
  );
};

export const StatCard3: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const eyebrowProg = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const numberScale = spring({
    frame: frame - 30,
    fps,
    config: { damping: 14, stiffness: 110 },
  });

  const headlineProg = interpolate(frame, [55, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const sourceProg = interpolate(frame, [95, 120], [0, 1], {
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
          marginBottom: 32,
          opacity: eyebrowProg,
          transform: `translateY(${(1 - eyebrowProg) * 10}px)`,
        }}
      >
        Blind spot two
      </div>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 80,
        }}
      >
        {/* DNA Helix */}
        <div style={{ flexShrink: 0 }}>
          <Helix frame={frame} fps={fps} />
        </div>

        {/* Number + headline */}
        <div style={{ display: "flex", flexDirection: "column" }}>
          <div
            style={{
              display: "flex",
              alignItems: "baseline",
              gap: 4,
              fontFamily: theme.serif,
              lineHeight: 0.95,
              transform: `scale(${numberScale})`,
              transformOrigin: "left bottom",
            }}
          >
            <span
              style={{
                fontSize: 320,
                fontWeight: 500,
                color: theme.ink,
                letterSpacing: "-0.04em",
                fontVariantNumeric: "tabular-nums",
              }}
            >
              99
            </span>
            <span
              style={{
                fontSize: 180,
                fontWeight: 500,
                color: theme.accent,
              }}
            >
              %
            </span>
          </div>

          <div
            style={{
              marginTop: 32,
              fontFamily: theme.serif,
              fontWeight: 500,
              fontSize: 52,
              lineHeight: 1.15,
              letterSpacing: "-0.01em",
              maxWidth: 820,
              color: theme.ink,
              opacity: headlineProg,
              transform: `translateY(${(1 - headlineProg) * 16}px)`,
            }}
          >
            of people carry at least one{" "}
            <em style={{ color: theme.accent, fontStyle: "italic" }}>
              actionable pharmacogenomic
            </em>{" "}
            variant.
          </div>

          <div
            style={{
              marginTop: 28,
              fontSize: 22,
              color: theme.muted,
              opacity: sourceProg,
              transform: `translateY(${(1 - sourceProg) * 8}px)`,
            }}
          >
            PREPARE study, Swen et al., The Lancet, 2023
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
