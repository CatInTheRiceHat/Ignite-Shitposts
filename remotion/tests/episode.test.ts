import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { assetPaths, durationFrames, parseEpisode } from "../src/episode";

const demo = () =>
  JSON.parse(
    readFileSync(new URL("../../episodes/zipper_demo/edit.json", import.meta.url), "utf8"),
  );
test("the neutral starter is valid without any zipper assets", () => {
  const episode = parseEpisode(JSON.parse(readFileSync(new URL("../../templates/remotion-episode.json", import.meta.url), "utf8")));
  assert.equal(durationFrames(episode), 900);
  assert(episode.shots.every((shot) => shot.scene.type === "layers" && shot.scene.layers.every((layer) => layer.placeholder)));
  assert(assetPaths(episode).every((asset) => !asset.includes("zipper")));
});
test("zipper edit is exactly 600 frames with all five story beats and separate painted layers", () => {
  const episode = parseEpisode(demo());
  assert.equal(durationFrames(episode), 600);
  assert.equal(episode.shots.length, 5);
  assert(
    episode.shots.every(
      (shot) => shot.scene.type === "layers" && shot.scene.layers.length >= 5,
    ),
  );
  assert(assetPaths(episode).includes("art/ignite/sol-full-body.png"));
});
test("another episode can replace a whole shot with a trimmed local MP4 and optional narration", () => {
  const episode = demo();
  episode.id = "episode-two";
  episode.shots[1].scene = {
    type: "video",
    src: "clips/flow-shot.mp4",
    trimBefore: 1,
  };
  episode.voiceover.src = "audio/cub.mp3";
  const parsed = parseEpisode(episode);
  assert.equal(durationFrames(parsed), 600);
  assert(assetPaths(parsed).includes("clips/flow-shot.mp4"));
  assert(assetPaths(parsed).includes("audio/cub.mp3"));
});
test("a layer may use a labeled placeholder without an image path", () => {
  const episode = demo();
  episode.shots[0].scene.layers = [
    { id: "art", placeholder: "REPLACE: jacket and zipper" },
  ];
  assert.doesNotThrow(() => parseEpisode(episode));
});
test("reject invalid durations and out-of-range or overlapping captions", () => {
  for (const mutate of [
    (e: ReturnType<typeof demo>) => {
      e.shots[0].duration = 0.001;
    },
    (e: ReturnType<typeof demo>) => {
      e.captions[0].end = 21;
    },
    (e: ReturnType<typeof demo>) => {
      e.captions[1].start = 1;
    },
    (e: ReturnType<typeof demo>) => {
      e.shots[0].scene.camera.end = 4;
    },
  ]) {
    const episode = demo();
    mutate(episode);
    assert.throws(() => parseEpisode(episode));
  }
});
test("media must stay local and inside public, and shot IDs must be unique", () => {
  for (const src of [
    "../private.png",
    "https://example.com/image.png",
    "/tmp/image.png",
  ]) {
    const episode = demo();
    episode.shots[0].scene.layers[0].src = src;
    assert.throws(() => parseEpisode(episode));
  }
  const episode = demo();
  episode.shots[1].id = episode.shots[0].id;
  assert.throws(() => parseEpisode(episode));
});
