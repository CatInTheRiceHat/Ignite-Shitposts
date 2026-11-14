import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { Episode, Layer, Shot } from "./episode";

const smooth = (
  frame: number,
  start: number,
  end: number,
  from: number,
  to: number,
  fps: number,
) =>
  interpolate(frame, [start * fps, end * fps], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });

const PaintedLayer: React.FC<{ layer: Layer }> = ({ layer }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const motion = layer.motion;
  const value = (
    key: "x" | "y" | "scale" | "rotate" | "opacity",
    fallback: number,
  ) =>
    motion
      ? smooth(
          frame,
          motion.start,
          motion.end,
          motion.from[key],
          motion.to[key],
          fps,
        )
      : fallback;
  const tug = layer.tug;
  const stepped = Math.floor(frame / 3) * 3;
  const tugY =
    tug && frame >= tug.start * fps && frame < tug.end * fps
      ? Math.sin((stepped - tug.start * fps) / 7) * tug.amount
      : 0;
  return (
    <div
      style={{
        position: "absolute",
        left: layer.x,
        top: layer.y,
        width: layer.width,
        height: layer.height,
        opacity: value("opacity", 1),
        transform: `translate(${value("x", 0)}px, ${value("y", 0) + tugY}px) rotate(${value("rotate", 0)}deg) scale(${value("scale", 1)})`,
      }}
    >
      {layer.src ? (
        <Img
          src={staticFile(layer.src)}
          style={{ width: "100%", height: "100%", objectFit: "contain" }}
        />
      ) : (
        <div className="art-placeholder">{layer.placeholder}</div>
      )}
    </div>
  );
};

const ShotScene: React.FC<{ shot: Shot }> = ({ shot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { scene } = shot;
  if (scene.type === "video")
    return (
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <OffthreadVideo
          src={staticFile(scene.src)}
          trimBefore={Math.round(scene.trimBefore * fps)}
          muted={scene.muted}
          playbackRate={scene.playbackRate}
          style={{ width: "100%", height: "100%", objectFit: scene.fit }}
        />
      </AbsoluteFill>
    );
  const { camera } = scene;
  const x = smooth(
    frame,
    camera.start,
    camera.end,
    camera.from.x,
    camera.to.x,
    fps,
  );
  const y = smooth(
    frame,
    camera.start,
    camera.end,
    camera.from.y,
    camera.to.y,
    fps,
  );
  const scale = smooth(
    frame,
    camera.start,
    camera.end,
    camera.from.scale,
    camera.to.scale,
    fps,
  );
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          width: 1080,
          height: 1280,
          transformOrigin: "0 0",
          transform: `translate(540px, 640px) scale(${scale}) translate(${-x}px, ${-y}px)`,
        }}
      >
        {scene.layers.map((layer) => (
          <PaintedLayer key={layer.id} layer={layer} />
        ))}
        {scene.annotations.map((annotation, index) =>
          frame >= annotation.start * fps && frame < annotation.end * fps ? (
            <div
              key={index}
              className="annotation"
              style={{ left: annotation.x, top: annotation.y }}
            >
              {annotation.text}
            </div>
          ) : null,
        )}
      </div>
    </AbsoluteFill>
  );
};

const ShotCard: React.FC<{ shot: Shot; index: number; hook: string }> = ({
  shot,
  index,
  hook,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = smooth(frame, 0, 0.25, 22, 0, fps);
  return (
    <AbsoluteFill>
      <div className="chapter">
        {String(index + 1).padStart(2, "0")} <span>/</span> {shot.label}
      </div>
      <div className="headline" style={{ transform: `translateY(${enter}px)` }}>
        {index === 0 ? hook : shot.title}
      </div>
      <div className="scene">
        <ShotScene shot={shot} />
      </div>
    </AbsoluteFill>
  );
};

export const IgniteShort: React.FC<{ episode: Episode }> = ({ episode }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const caption = episode.captions.find(
    (cue) =>
      frame >= Math.round(cue.start * fps) && frame < Math.round(cue.end * fps),
  );
  let offset = 0;
  return (
    <AbsoluteFill
      className="ignite-short"
      style={
        {
          background: episode.palette.paper,
          color: episode.palette.ink,
          "--ink": episode.palette.ink,
          "--teal": episode.palette.teal,
          "--orange": episode.palette.orange,
        } as React.CSSProperties
      }
    >
      <style>{`@font-face {font-family: Ignite; src: url("${staticFile(episode.assets.font)}") format("truetype"); font-weight: 100 900;}`}</style>
      <Img className="paper" src={staticFile(episode.assets.paper)} />
      <div className="brand">
        <span className="brand-flame">✦</span> IGNITE{" "}
        <span className="brand-series">LITTLE THINGS, EXPLAINED.</span>
      </div>
      {episode.shots.map((shot, index) => {
        const from = offset;
        const duration = Math.round(shot.duration * fps);
        offset += duration;
        return (
          <Sequence
            key={shot.id}
            name={shot.label}
            from={from}
            durationInFrames={duration}
          >
            <ShotCard shot={shot} index={index} hook={episode.hook} />
          </Sequence>
        );
      })}
      {caption && (
        <div className="caption">
          <span>{caption.text}</span>
        </div>
      )}
      <div className="footer">
        <span>{episode.artNote ?? "FIND YOUR FIRE."}</span>
        <span>{episode.id.toUpperCase()}</span>
      </div>
      <div
        className="progress"
        style={{ width: `${(100 * (frame + 1)) / durationInFrames}%` }}
      />
      {episode.voiceover?.src && (
        <Sequence from={Math.round(episode.voiceover.start * fps)}>
          <Audio
            src={staticFile(episode.voiceover.src)}
            volume={episode.voiceover.volume}
          />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};
