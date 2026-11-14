import { Composition, getInputProps } from "remotion";
import { IgniteShort } from "./Composition";
import { durationFrames, parseEpisode } from "./episode";
import "./style.css";

const episode = parseEpisode(getInputProps().episode);

export const RemotionRoot = () => (
  <Composition
    id="IgniteShort"
    component={IgniteShort}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={durationFrames(episode)}
    defaultProps={{ episode }}
    calculateMetadata={({ props }) => {
      const parsed = parseEpisode(props.episode);
      return {
        width: 1080,
        height: 1920,
        fps: 30,
        durationInFrames: durationFrames(parsed),
        props: { episode: parsed },
      };
    }}
  />
);
