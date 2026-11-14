import { z } from "zod";

// All asset paths are local to public/. No provider, token, or network service.
const asset = z
  .string()
  .min(1)
  .refine(
    (value) =>
      !value.startsWith("/") && !value.includes("..") && !/[:\\?#]/.test(value),
    "Use a relative local path inside public/, such as clips/shot-01.mp4",
  );
const seconds = z.number().finite().nonnegative();
const pose = z.object({
  x: z.number().finite().default(0),
  y: z.number().finite().default(0),
  scale: z.number().positive().default(1),
  rotate: z.number().finite().default(0),
  opacity: z.number().min(0).max(1).default(1),
});
const motion = z
  .object({
    from: pose.default({ x: 0, y: 0, scale: 1, rotate: 0, opacity: 1 }),
    to: pose.default({ x: 0, y: 0, scale: 1, rotate: 0, opacity: 1 }),
    start: seconds.default(0),
    end: seconds,
  })
  .refine(
    (value) => value.end > value.start,
    "Motion end must follow its start",
  );
const cameraPose = z.object({
  x: z.number().finite(),
  y: z.number().finite(),
  scale: z.number().positive(),
});
const layer = z
  .object({
    id: z.string().min(1),
    src: asset.optional(),
    placeholder: z.string().optional(),
    x: z.number().finite().default(0),
    y: z.number().finite().default(0),
    width: z.number().positive().default(1080),
    height: z.number().positive().default(1280),
    motion: motion.optional(),
    tug: z
      .object({
        start: seconds,
        end: seconds,
        amount: z.number().finite().default(14),
      })
      .optional(),
  })
  .refine(
    (value) => Boolean(value.src || value.placeholder),
    "Layer needs src or a labeled placeholder",
  );
const annotation = z.object({
  text: z.string(),
  x: z.number(),
  y: z.number(),
  start: seconds.default(0),
  end: seconds,
});
const scene = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("layers"),
    camera: z.object({
      from: cameraPose,
      to: cameraPose,
      start: seconds.default(0),
      end: seconds,
    }),
    layers: z.array(layer).min(1),
    annotations: z.array(annotation).default([]),
  }),
  z.object({
    type: z.literal("video"),
    src: asset,
    trimBefore: seconds.default(0),
    muted: z.boolean().default(true),
    fit: z.enum(["cover", "contain"]).default("cover"),
    playbackRate: z.number().positive().default(1),
  }),
]);
export const episodeSchema = z
  .object({
    id: z.string().regex(/^[a-z0-9][a-z0-9-]*$/),
    title: z.string().min(1),
    hook: z.string().min(1),
    format: z.object({
      width: z.literal(1080),
      height: z.literal(1920),
      fps: z.literal(30),
    }),
    artNote: z.string().optional(),
    layout: z.enum(["cards", "fullscreen"]).default("cards"),
    captionStyle: z
      .object({
        fontSize: z.number().positive().default(56),
        fill: z.string().default("#FFFFFF"),
        outline: z.string().default("#F07B2A"),
        outlineWidth: z.number().nonnegative().default(6),
        leftPercent: z.number().min(0).max(100).default(10),
        rightPercent: z.number().min(0).max(100).default(16),
        topPercent: z.number().min(0).max(100).default(80),
      })
      .default({
        fontSize: 56,
        fill: "#FFFFFF",
        outline: "#F07B2A",
        outlineWidth: 6,
        leftPercent: 10,
        rightPercent: 16,
        topPercent: 80,
      }),
    timing: z
      .object({ confirmed: z.boolean(), note: z.string().optional() })
      .optional(),
    assets: z.object({ paper: asset, font: asset }),
    palette: z.object({
      paper: z.string(),
      ink: z.string(),
      teal: z.string(),
      orange: z.string(),
    }),
    shots: z
      .array(
        z.object({
          id: z.string().min(1),
          label: z.string().min(1),
          title: z.string().optional(),
          duration: z.number().positive().finite(),
          scene,
        }),
      )
      .min(1),
    captions: z.array(
      z.object({ start: seconds, end: seconds, text: z.string().min(1) }),
    ),
    voiceover: z
      .object({
        src: asset.nullable(),
        script: z.string().optional(),
        start: seconds.default(0),
        volume: z.number().min(0).max(1).default(1),
      })
      .nullable()
      .default(null),
    audioTracks: z
      .array(
        z.object({
          id: z.string().min(1),
          speaker: z.string().min(1),
          src: asset,
          start: seconds,
          trimBefore: seconds.default(0),
          duration: z.number().positive().finite().optional(),
          volume: z.number().min(0).max(2).default(1),
          playbackRate: z.literal(1).default(1),
          source_sha256: z
            .string()
            .regex(/^[a-f0-9]{64}$/)
            .optional(),
        }),
      )
      .default([]),
  })
  .superRefine((episode, context) => {
    const total = episode.shots.reduce((sum, shot) => sum + shot.duration, 0);
    const ids = new Set<string>();
    episode.shots.forEach((shot, index) => {
      if (ids.has(shot.id))
        context.addIssue({
          code: "custom",
          path: ["shots", index, "id"],
          message: "Duplicate shot ID",
        });
      ids.add(shot.id);
      if (Math.abs(shot.duration * 30 - Math.round(shot.duration * 30)) > 1e-6)
        context.addIssue({
          code: "custom",
          path: ["shots", index, "duration"],
          message: "Duration must align to a 30 fps frame",
        });
      if (shot.scene.type === "layers") {
        const timings = [
          shot.scene.camera,
          ...shot.scene.layers.flatMap((item) =>
            item.motion ? [item.motion] : [],
          ),
        ];
        if (
          timings.some(
            (item) => item.end <= item.start || item.end > shot.duration,
          )
        )
          context.addIssue({
            code: "custom",
            path: ["shots", index, "scene"],
            message: "Camera/layer motion must fit within its shot",
          });
        for (const item of [
          ...shot.scene.annotations,
          ...shot.scene.layers.flatMap((l) => (l.tug ? [l.tug] : [])),
        ]) {
          if (item.end <= item.start || item.end > shot.duration)
            context.addIssue({
              code: "custom",
              path: ["shots", index, "scene"],
              message: "Annotation/tug timing must fit within its shot",
            });
        }
      }
    });
    episode.captions.forEach((caption, index) => {
      if (
        caption.end <= caption.start ||
        caption.end > total ||
        (index > 0 && caption.start < episode.captions[index - 1].end)
      )
        context.addIssue({
          code: "custom",
          path: ["captions", index],
          message:
            "Captions must be ordered, nonoverlapping, and inside the episode",
        });
    });
    if (episode.voiceover?.src && episode.voiceover.start >= total)
      context.addIssue({
        code: "custom",
        path: ["voiceover", "start"],
        message: "Voiceover must start inside the episode",
      });
    const audioIds = new Set<string>();
    episode.audioTracks.forEach((track, index) => {
      if (
        audioIds.has(track.id) ||
        track.start >= total ||
        (track.duration !== undefined &&
          track.start + track.duration > total + 1 / 30)
      ) {
        context.addIssue({
          code: "custom",
          path: ["audioTracks", index],
          message:
            "Audio tracks need unique IDs and must fit inside the episode",
        });
      }
      audioIds.add(track.id);
    });
  });

export type Episode = z.infer<typeof episodeSchema>;
export type Shot = Episode["shots"][number];
export type Layer = z.infer<typeof layer>;
export const parseEpisode = (input: unknown): Episode =>
  episodeSchema.parse(input);
export const durationFrames = (episode: Episode) =>
  episode.shots.reduce((sum, shot) => sum + Math.round(shot.duration * 30), 0);
export const assetPaths = (episode: Episode): string[] => [
  ...new Set([
    episode.assets.paper,
    episode.assets.font,
    ...episode.shots.flatMap((shot) =>
      shot.scene.type === "video"
        ? [shot.scene.src]
        : shot.scene.layers.flatMap((l) => (l.src ? [l.src] : [])),
    ),
    ...(episode.voiceover?.src ? [episode.voiceover.src] : []),
    ...episode.audioTracks.map((track) => track.src),
  ]),
];
