import React from "react";
import { Composition } from "remotion";
import { StatCard1 } from "./StatCard1";
import { StatCard2 } from "./StatCard2";
import { StatCard3 } from "./StatCard3";
import { SpectrumCard } from "./SpectrumCard";
import { PatientInsetCard } from "./PatientInsetCard";
import { PipelineCutaway } from "./PipelineCutaway";
import { CompareCard } from "./CompareCard";
import { SafetyPanel } from "./SafetyPanel";
import { FinalCard } from "./FinalCard";

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="StatCard1"
        component={StatCard1}
        durationInFrames={150}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="StatCard2"
        component={StatCard2}
        durationInFrames={165}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="StatCard3"
        component={StatCard3}
        durationInFrames={180}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="SpectrumCard"
        component={SpectrumCard}
        durationInFrames={180}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="PatientInsetCard"
        component={PatientInsetCard}
        durationInFrames={90}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="PipelineCutaway"
        component={PipelineCutaway}
        durationInFrames={150}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="CompareCard"
        component={CompareCard}
        durationInFrames={150}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="SafetyPanel"
        component={SafetyPanel}
        durationInFrames={150}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="FinalCard"
        component={FinalCard}
        durationInFrames={150}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
