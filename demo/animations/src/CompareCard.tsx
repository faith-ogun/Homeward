import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
} from "remotion";
import { theme } from "./theme";

/**
 * COMPARE CARD — Generic recovery agent vs Homeward.
 *
 * Beats:
 *   00f:    eyebrow tag + "vs" pivot fade in
 *   12f:    LEFT card slides in from the left
 *   30f:    LEFT verdict appears (greyed)
 *   42f:    RIGHT card slides in from the right
 *   60f:    RIGHT verdict appears (accent)
 *   78f:    accent ring around RIGHT card pulses once
 *   135f+:  hold
 */

const Card: React.FC<{
  title: string;
  verdict: string;
  reasoning: string;
  variant: "muted" | "accent";
  enterProg: number; // 0..1 slide-in
  verdictProg: number; // 0..1 verdict reveal
  ringPulse?: number; // 0..1
}> = ({ title, verdict, reasoning, variant, enterProg, verdictProg, ringPulse = 0 }) => {
  const isAccent = variant === "accent";
  const slideX =
    variant === "muted" ? (1 - enterProg) * -60 : (1 - enterProg) * 60;

  const ringWidth = 3 + ringPulse * 6;
  const ringOpacity = 0.5 + ringPulse * 0.5;

  return (
    <div
      style={{
        flex: 1,
        background: isAccent ? theme.bg2 : theme.bg2,
        border: `${ringWidth}px solid ${
          isAccent ? `rgba(47,92,62,${ringOpacity})` : theme.line
        }`,
        borderRadius: 24,
        padding: 44,
        opacity: enterProg,
        transform: `translateX(${slideX}px)`,
        position: "relative",
      }}
    >
      <div
        style={{
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: "0.18em",
          textTransform: "uppercase",
          color: isAccent ? theme.accent : theme.muted,
          marginBottom: 18,
        }}
      >
        {title}
      </div>

      <div
        style={{
          fontFamily: theme.serif,
          fontSize: 38,
          fontWeight: 500,
          lineHeight: 1.2,
          letterSpacing: "-0.01em",
          color: isAccent ? theme.ink : theme.muted,
          marginBottom: 24,
          opacity: verdictProg,
          transform: `translateY(${(1 - verdictProg) * 10}px)`,
        }}
      >
        {verdict}
      </div>

      <div
        style={{
          fontSize: 20,
          lineHeight: 1.5,
          color: isAccent ? theme.ink2 : theme.muted,
          opacity: verdictProg * 0.85,
        }}
      >
        {reasoning}
      </div>
    </div>
  );
};

export const CompareCard: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrowProg = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const leftEnter = interpolate(frame, [12, 32], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const leftVerdict = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const rightEnter = interpolate(frame, [42, 62], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const rightVerdict = interpolate(frame, [60, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // One soft pulse on the right card around frame 78–98
  const ringPulse =
    frame > 78 && frame < 110
      ? Math.max(0, Math.sin(((frame - 78) / 32) * Math.PI))
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
          marginBottom: 16,
          opacity: eyebrowProg,
        }}
      >
        Same patient, two agents
      </div>

      <div
        style={{
          fontFamily: theme.serif,
          fontSize: 44,
          fontWeight: 500,
          lineHeight: 1.1,
          letterSpacing: "-0.015em",
          marginBottom: 56,
          color: theme.ink,
          opacity: eyebrowProg,
        }}
      >
        Pain 7/10, day 4 post-op.
      </div>

      <div style={{ display: "flex", gap: 32, alignItems: "stretch" }}>
        <Card
          title="Generic recovery agent"
          verdict="Pain above expected. Escalate."
          reasoning="Flags the deviation. Has no idea why."
          variant="muted"
          enterProg={leftEnter}
          verdictProg={leftVerdict}
        />

        {/* Center pivot */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            opacity: eyebrowProg,
          }}
        >
          <div
            style={{
              fontFamily: theme.serif,
              fontStyle: "italic",
              fontSize: 36,
              color: theme.muted,
              letterSpacing: "-0.01em",
            }}
          >
            vs
          </div>
        </div>

        <Card
          title="Homeward"
          verdict="CYP2D6 *4/*4. Codeine inert. Switch analgesic."
          reasoning="The complication is the drug, not the surgery. CPIC-cited oxycodone alternative drafted as FHIR MedicationRequest for clinician approval."
          variant="accent"
          enterProg={rightEnter}
          verdictProg={rightVerdict}
          ringPulse={ringPulse}
        />
      </div>
    </AbsoluteFill>
  );
};
