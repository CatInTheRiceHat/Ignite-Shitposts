import { existsSync, readFileSync } from "node:fs";
import { mkdir, mkdtemp, rename, rm, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const episodeDir = fileURLToPath(new URL("../", import.meta.url));
const videoProject = path.resolve(episodeDir, "../../../ignite-video");
const fromVideoProject = createRequire(path.join(videoProject, "package.json"));
const { bundle } = fromVideoProject("@remotion/bundler");
const { renderMedia, selectComposition } =
  fromVideoProject("@remotion/renderer");
const args = process.argv.slice(2);
const compositionOnly = args.includes("--check-composition");
const withAudio = args.includes("--with-audio");
if (
  args.some((arg) => !["--check-composition", "--with-audio"].includes(arg))
) {
  throw new Error(
    "Usage: node render.mjs [--check-composition] [--with-audio]",
  );
}

const clip = path.join(episodeDir, "clips/sol-lantern-kling.mp4");
const audioSettings = JSON.parse(
  readFileSync(path.join(episodeDir, "audio-test.json"), "utf8"),
);
const audioMix = path.join(episodeDir, audioSettings.mix.output);
const output = path.join(
  episodeDir,
  withAudio ? audioSettings.preview : "renders/sol-lantern-preview.mp4",
);
const ffprobe = process.env.FFPROBE_PATH || "ffprobe";
const ffmpeg = process.env.FFMPEG_PATH || "ffmpeg";
const macChrome =
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const browserExecutable =
  process.env.REMOTION_BROWSER_EXECUTABLE ||
  (process.platform === "darwin" && existsSync(macChrome)
    ? macChrome
    : undefined);

function probe(file) {
  const result = spawnSync(
    ffprobe,
    ["-v", "error", "-show_streams", "-show_format", "-of", "json", file],
    { encoding: "utf8" },
  );
  if (result.error || result.status !== 0) {
    throw new Error(
      `ffprobe failed: ${result.error?.message || result.stderr}`,
    );
  }
  return JSON.parse(result.stdout);
}

function rate(stream) {
  const [n, d] = stream.avg_frame_rate.split("/").map(Number);
  return n / d;
}

async function main() {
  if (!compositionOnly && withAudio) {
    if (!existsSync(audioMix)) {
      throw new Error(
        `Missing audio mix: ${audioMix}. Run prepare-audio.py first.`,
      );
    }
    const mix = probe(audioMix);
    if (
      !mix.streams.some((stream) => stream.codec_type === "audio") ||
      Math.abs(Number(mix.format.duration) - 4) > 0.001
    ) {
      throw new Error(
        "The audio mix must contain exactly four seconds of audio.",
      );
    }
  }
  if (!compositionOnly) {
    if (!existsSync(clip)) {
      throw new Error(
        `Missing Kling footage: ${clip}. No preview was rendered.`,
      );
    }
    const source = probe(clip);
    const video = source.streams.find(
      (stream) => stream.codec_type === "video",
    );
    if (!video || video.width !== 720 || video.height !== 1280) {
      throw new Error(
        "Expected a 720 × 1280 Kling clip. Preserve the artwork's framing before rendering.",
      );
    }
    if (
      Math.abs(Number(source.format.duration) - 4) >
      1 / rate(video) + 0.001
    ) {
      throw new Error(
        "Expected four seconds of Kling footage; refusing a speed change or a padded ending.",
      );
    }
  }

  const cache = path.join(episodeDir, ".cache");
  await mkdir(cache, { recursive: true });
  const scratch = await mkdtemp(path.join(cache, "render-"));
  try {
    const serveUrl = await bundle({
      entryPoint: fileURLToPath(new URL("index.tsx", import.meta.url)),
      rootDir: videoProject,
      publicDir: episodeDir,
      // Do not recursively copy renders/cache into the temporary bundle.
      symlinkPublicDir: true,
      outDir: path.join(scratch, "bundle"),
      rspack: false,
      enableCaching: true,
      webpackOverride: (config) => ({
        ...config,
        resolve: {
          ...config.resolve,
          modules: [
            path.join(videoProject, "node_modules"),
            ...(config.resolve?.modules || ["node_modules"]),
          ],
        },
      }),
    });
    const composition = await selectComposition({
      serveUrl,
      id: withAudio ? "SolLanternAudioTest" : "SolLanternTest",
      browserExecutable,
    });
    if (
      composition.width !== 1080 ||
      composition.height !== 1920 ||
      composition.fps !== 30 ||
      composition.durationInFrames !== 120
    ) {
      throw new Error("Composition must be 1080 × 1920, 30 fps, 120 frames.");
    }
    if (compositionOnly) {
      console.log(
        "Verified composition: 1080 × 1920, 30 fps, four seconds. No footage rendered.",
      );
      return;
    }

    const temporaryOutput = path.join(scratch, "preview.mp4");
    let lastProgress = -1;
    await renderMedia({
      serveUrl,
      composition,
      outputLocation: temporaryOutput,
      codec: "h264",
      ...(withAudio ? { audioCodec: "aac", audioBitrate: "192k" } : {}),
      crf: 18,
      pixelFormat: "yuv420p",
      imageFormat: "jpeg",
      jpegQuality: 95,
      concurrency: 2,
      browserExecutable,
      onProgress: ({ progress }) => {
        const percent = Math.floor(progress * 10) * 10;
        if (percent > lastProgress) {
          console.log(`Rendering ${percent}%`);
          lastProgress = percent;
        }
      },
    });
    if (withAudio) {
      // Remotion's copied AAC track includes encoder padding. Mux the original
      // lossless mix with an exact endpoint, preserving the rendered video.
      const exactAudioOutput = path.join(scratch, "preview-exact-audio.mp4");
      const mux = spawnSync(
        ffmpeg,
        [
          "-v",
          "error",
          "-i",
          temporaryOutput,
          "-i",
          audioMix,
          "-map",
          "0:v:0",
          "-map",
          "1:a:0",
          "-c:v",
          "copy",
          "-c:a",
          "aac",
          "-b:a",
          "192k",
          "-t",
          "4",
          "-movflags",
          "+faststart",
          exactAudioOutput,
        ],
        { encoding: "utf8" },
      );
      if (mux.error || mux.status !== 0) {
        throw new Error(
          `Audio mux failed: ${mux.error?.message || mux.stderr}`,
        );
      }
      await rename(exactAudioOutput, temporaryOutput);
    }
    const result = probe(temporaryOutput);
    const video = result.streams.find(
      (stream) => stream.codec_type === "video",
    );
    const audio = result.streams.find(
      (stream) => stream.codec_type === "audio",
    );
    if (
      !video ||
      video.width !== 1080 ||
      video.height !== 1920 ||
      rate(video) !== 30 ||
      Number(video.nb_frames) !== 120 ||
      Math.abs(Number(result.format.duration) - 4) > 0.001 ||
      (withAudio ? !audio || audio.codec_name !== "aac" : Boolean(audio))
    ) {
      const failureDir = path.join(cache, `failed-${Date.now()}`);
      await mkdir(failureDir, { recursive: true });
      await writeFile(
        path.join(failureDir, "ffprobe.json"),
        JSON.stringify(result, null, 2),
      );
      await rename(temporaryOutput, path.join(failureDir, "preview.mp4"));
      throw new Error(
        `Preview failed verification (${video?.width}x${video?.height}, ${video ? rate(video) : "?"} fps, ${video?.nb_frames} frames, ${result.format.duration}s, audio ${audio?.codec_name || "none"}). Inspect ${failureDir}; previous render preserved.`,
      );
    }
    const decode = spawnSync(
      ffmpeg,
      ["-v", "error", "-xerror", "-i", temporaryOutput, "-f", "null", "-"],
      { encoding: "utf8" },
    );
    if (decode.error || decode.status !== 0) {
      throw new Error(
        `Preview decode failed: ${decode.error?.message || decode.stderr}`,
      );
    }

    await mkdir(path.dirname(output), { recursive: true });
    if (existsSync(output)) {
      const archiveDir = path.join(path.dirname(output), "archive");
      await mkdir(archiveDir, { recursive: true });
      await rename(
        output,
        path.join(archiveDir, `${Date.now()}-${path.basename(output)}`),
      );
    }
    await rename(temporaryOutput, output);
    await writeFile(
      output.replace(/\.mp4$/, ".verification.json"),
      JSON.stringify(
        {
          source: clip,
          output,
          width: video.width,
          height: video.height,
          fps: 30,
          frames: 120,
          duration: 4,
          fit: "contain",
          crop: "none",
          audio: withAudio,
          ...(withAudio
            ? { audioSource: audioMix, audioCodec: audio.codec_name }
            : {}),
          captions: false,
          decoded: true,
        },
        null,
        2,
      ) + "\n",
    );
    console.log(`Saved and verified: ${output}`);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
