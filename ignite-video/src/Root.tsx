import { Composition } from "remotion";
import zipper from "../episodes/zipper.json";
import { IgniteShort } from "./Composition";
import { durationFrames, parseEpisode } from "./episode";
import "./style.css";

const episode = parseEpisode(zipper);

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
