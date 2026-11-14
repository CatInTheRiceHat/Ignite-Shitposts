import {
  access,
  mkdir,
  mkdtemp,
  readFile,
  rename,
  rm,
  writeFile,
} from "node:fs/promises";
import { existsSync, watchFile, unwatchFile } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";
import { spawn, spawnSync } from "node:child_process";
import { bundle } from "@remotion/bundler";
import {
  renderMedia,
  renderStill,
  selectComposition,
} from "@remotion/renderer";
import {
  assetPaths,
  durationFrames,
  parseEpisode,
  type Episode,
} from "../src/episode";

const root = fileURLToPath(new URL("../", import.meta.url));
const sharedModules = path.resolve(root, "../../node_modules");
process.chdir(root);
const { values, positionals } = parseArgs({
  allowPositionals: true,
  options: {
    episode: { type: "string" },
    output: { type: "string" },
    concurrency: { type: "string", default: "4" },
    frame: { type: "string", default: "270" },
    "no-open": { type: "boolean", default: false },
    "browser-executable": { type: "string" },
  },
});
const [command, positionalEpisode, ...extra] = positionals;
if (
  !["dev", "render", "still"].includes(command) ||
  extra.length ||
  (values.episode && positionalEpisode)
)
  throw new Error(
    "Usage: npm run dev|render|still -- [episodes/file.json] [--output out/file.mp4] [--frame 270]",
  );
const episodePath = path.resolve(
  values.episode ?? positionalEpisode ?? "episodes/zipper.json",
);
const readEpisode = async () =>
  parseEpisode(
    JSON.parse((await readFile(episodePath, "utf8")).replace(/^\uFEFF/, "")),
  );
const ffprobe = process.env.FFPROBE_PATH || "ffprobe";
// The current headless-shell build crashes while loading ICU on this Mac.
// Prefer the installed desktop Chrome on macOS; other platforms keep Remotion's
// bundled browser. Both choices still render headlessly in an isolated profile.
const macChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const browserExecutable =
  values["browser-executable"] ??
  process.env.REMOTION_BROWSER_EXECUTABLE ??
  (process.platform === "darwin" && existsSync(macChrome)
    ? macChrome
    : undefined);

function probe(file: string) {
  const result = spawnSync(
    ffprobe,
    ["-v", "error", "-show_streams", "-show_format", "-of", "json", file],
    { encoding: "utf8" },
  );
  if (result.error)
    throw new Error(
      "ffprobe is required. Install with brew install ffmpeg, or set FFPROBE_PATH to its executable.",
    );
  if (result.status !== 0)
    throw new Error(`ffprobe could not read ${file}: ${result.stderr.trim()}`);
  return JSON.parse(result.stdout) as {
    format: { duration: string };
    streams: {
      codec_type: string;
      codec_name: string;
      width: number;
      height: number;
      avg_frame_rate: string;
      nb_frames?: string;
    }[];
  };
}

async function checkAssets(episode: Episode) {
  for (const name of assetPaths(episode)) {
    try {
      await access(path.join(root, "public", name));
    } catch {
      throw new Error(
        `Missing artwork/media: public/${name}. Copy the file there, edit the episode JSON, or run npm run setup-assets for original Ignite art.`,
      );
    }
  }
  for (const shot of episode.shots) {
    if (shot.scene.type !== "video") continue;
    const info = probe(path.join(root, "public", shot.scene.src));
    if (!info.streams.some((stream) => stream.codec_type === "video"))
      throw new Error(`No video stream in shot ${shot.id}`);
    const available =
      (Number(info.format.duration) - shot.scene.trimBefore) /
      shot.scene.playbackRate;
    if (!Number.isFinite(available) || available + 1 / 30 < shot.duration)
      throw new Error(
        `Shot ${shot.id}: local MP4 is too short after trim/playbackRate (${available.toFixed(2)}s for a ${shot.duration}s shot).`,
      );
  }
}

async function main() {
  const episode = await readEpisode();
  await checkAssets(episode);
  const inputProps = { episode };
  console.log(
    `${episode.title} — ${durationFrames(episode)} frames, 1080 × 1920, 30 fps`,
  );
  await mkdir(path.join(root, ".cache"), { recursive: true });
  const scratch = await mkdtemp(path.join(root, ".cache/video-"));
  try {
    if (command === "dev") {
      const propsFile = path.join(scratch, "props.json");
      await writeFile(propsFile, JSON.stringify(inputProps));
      const args = [
        path.join(sharedModules, "@remotion/cli/remotion-cli.js"),
        "studio",
        "src/index.ts",
        "--props",
        propsFile,
      ];
      if (values["no-open"]) args.push("--no-open");
      if (browserExecutable)
        args.push("--browser-executable", browserExecutable);
      const child = spawn(process.execPath, args, {
        cwd: root,
        stdio: "inherit",
      });
      watchFile(episodePath, { interval: 250 }, async () => {
        try {
          const edited = await readEpisode();
          await checkAssets(edited);
          await writeFile(propsFile, JSON.stringify({ episode: edited }));
          console.log(`Reloaded ${path.relative(root, episodePath)}`);
        } catch (error) {
          console.error(
            `Episode edit not applied: ${(error as Error).message}`,
          );
        }
      });
      const stop = () => child.kill("SIGTERM");
      process.on("SIGINT", stop);
      process.on("SIGTERM", stop);
      await new Promise<void>((resolve, reject) => {
        child.on("error", reject);
        child.on("exit", (code, signal) =>
          signal || code === 0
            ? resolve()
            : reject(new Error(`Studio exited ${code}`)),
        );
      });
      unwatchFile(episodePath);
      process.off("SIGINT", stop);
      process.off("SIGTERM", stop);
      return;
    }
    const output = path.resolve(
      values.output ??
        `out/${episode.id}${command === "still" ? "-preview.png" : ".mp4"}`,
    );
    const temporaryOutput = path.join(
      scratch,
      command === "still" ? "preview.png" : "video.mp4",
    );
    const concurrency = Number(values.concurrency);
    if (!Number.isInteger(concurrency) || concurrency < 1)
      throw new Error("--concurrency must be a positive integer");
    console.log("Bundling the composition…");
    if (browserExecutable) console.log(`Render browser: ${browserExecutable}`);
    const serveUrl = await bundle({
      entryPoint: path.join(root, "src/index.ts"),
      outDir: path.join(scratch, "bundle"),
      publicDir: path.join(root, "public"),
      rspack: false,
      enableCaching: true,
    });
    const composition = await selectComposition({
      serveUrl,
      id: "IgniteShort",
      inputProps,
      browserExecutable,
    });
    let verification: unknown;
    if (command === "still") {
      const frame = Number(values.frame);
      if (
        !Number.isInteger(frame) ||
        frame < 0 ||
        frame >= composition.durationInFrames
      )
        throw new Error("--frame must be inside the episode");
      await renderStill({
        serveUrl,
        composition,
        inputProps,
        output: temporaryOutput,
        frame,
        imageFormat: "png",
        browserExecutable,
      });
    } else {
      const toolCheck = spawnSync(ffprobe, ["-version"], { encoding: "utf8" });
      if (toolCheck.error || toolCheck.status !== 0)
        throw new Error(
          "ffprobe is required. Install with brew install ffmpeg, or set FFPROBE_PATH.",
        );
      let lastProgress = -1;
      await renderMedia({
        serveUrl,
        composition,
        inputProps,
        codec: "h264",
        crf: 18,
        pixelFormat: "yuv420p",
        outputLocation: temporaryOutput,
        concurrency,
        imageFormat: "jpeg",
        jpegQuality: 95,
        browserExecutable,
        onProgress: ({ progress }) => {
          const percent = Math.floor(progress * 10) * 10;
          if (percent > lastProgress) {
            console.log(`Rendering ${percent}%`);
            lastProgress = percent;
          }
        },
      });
      const info = probe(temporaryOutput);
      const video = info.streams.find(
        (stream) => stream.codec_type === "video",
      );
      const duration = Number(info.format.duration);
      const [numerator, denominator] = (video?.avg_frame_rate ?? "0/1")
        .split("/")
        .map(Number);
      if (
        !video ||
        video.width !== 1080 ||
        video.height !== 1920 ||
        numerator / denominator !== 30 ||
        !Number.isFinite(duration) ||
        Math.abs(duration - composition.durationInFrames / 30) > 1 / 30
      )
        throw new Error(
          "Rendered video failed dimension/fps/duration verification; existing output preserved.",
        );
      verification = {
        episode: path.relative(root, episodePath),
        width: video.width,
        height: video.height,
        fps: numerator / denominator,
        frames: composition.durationInFrames,
        duration,
        codec: video.codec_name,
      };
    }
    await mkdir(path.dirname(output), { recursive: true });
    const archive = path.join(
      path.dirname(output),
      "archive",
      `${Date.now()}-${path.basename(output)}`,
    );
    try {
      await access(output);
      await mkdir(path.dirname(archive), { recursive: true });
      await rename(output, archive);
      console.log(`Previous output preserved: ${archive}`);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") throw error;
    }
    await rename(temporaryOutput, output);
    if (verification)
      await writeFile(
        output.replace(/\.mp4$/i, "") + ".verification.json",
        JSON.stringify(verification, null, 2) + "\n",
      );
    console.log(`Saved ${output}`);
    if (verification) console.log(`Verified: ${JSON.stringify(verification)}`);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
