# Workspace organization — 2026-11-13

All active production material now lives under `workflow/`.

| Previous location | Canonical location |
| --- | --- |
| `guidlines/` | `workflow/guidelines/` |
| `graphics/` | `workflow/assets/reference-art/` |
| `music/` | `workflow/assets/music/` |
| `ignite-video/` | `workflow/remotion/` |
| `zack-d-films-ai-video-generator/` | `workflow/vendor/zack-d-films-ai-video-generator/` |

The root `music/` and `zack-d-films-ai-video-generator/` paths are relative
compatibility symlinks. New work uses the canonical destinations.

`moves.json` records the relocations. `before.json` records SHA-256 hashes
and symlink targets before moving files, including local episode media.
Dependencies, caches, environment files, OS metadata and compiled Python
files are excluded from the hash inventory; whole-directory renames preserve
them on disk. No destination existed before these moves.

`original-text/` preserves the documents and source files whose references
or instructions needed updating. Creative edits, recordings, downloaded
clips, existing renders, provider history and older migration records remain
preserved. Episode metadata changes only repair file references.

The guide updates distinguish shared 30-second defaults from existing
episode durations and distinguish Python's 720p output from Remotion's 1080p
output. Existing episode settings and render behavior are retained.

Checking the restored legacy entry point exposed an existing Python renderer
startup bug: a loop variable named `settings` shadowed the imported settings
function, raising `UnboundLocalError` before argument parsing. The loop variable
is now `clip_settings`, with a CLI startup regression test.

See `verification.json` for preservation and local verification results.
