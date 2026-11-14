import React from "react";
import audioTest from "../audio-test.json";
import {
  AbsoluteFill,
  Audio,
  Composition,
  OffthreadVideo,
  registerRoot,
  staticFile,
} from "remotion";

// Replace this asset to review another Kling pass without changing the edit.
const SolLanternTest: React.FC<{ audioSrc: string | null }> = ({
  audioSrc,
}) => (
  <AbsoluteFill style={{ backgroundColor: "#FFF8F0" }}>
    <OffthreadVideo
      src={staticFile("clips/sol-lantern-kling.mp4")}
      muted
      playbackRate={1}
      style={{
        width: "100%",
        height: "100%",
        objectFit: "contain",
        objectPosition: "center",
      }}
    />
    {audioSrc && <Audio src={staticFile(audioSrc)} playbackRate={1} />}
  </AbsoluteFill>
);

const RemotionRoot = () => (
  <>
    <Composition
      id="SolLanternTest"
      component={SolLanternTest}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={120}
      defaultProps={{ audioSrc: null }}
    />
    <Composition
      id="SolLanternAudioTest"
      component={SolLanternTest}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={120}
      defaultProps={{ audioSrc: audioTest.mix.output }}
    />
  </>
);

registerRoot(RemotionRoot);
