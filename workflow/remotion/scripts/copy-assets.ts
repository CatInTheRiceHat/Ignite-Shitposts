import { copyFile, mkdir, readFile, access } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { resolveEpisodeConfig } from "./paths";

const root = fileURLToPath(new URL("../", import.meta.url));
const [episode, ...extra] = process.argv.slice(2);
if (!episode || extra.length) {
  throw new Error(
    "Usage: npm run setup-assets -- <episode-name|edit.json-path>",
  );
}
const config = resolveEpisodeConfig(
  episode,
  process.env.INIT_CWD || process.cwd(),
);
await access(config);
const publicDir = path.join(path.dirname(config), "public");
const copies = [
  ["sol-full-body.png", "art/ignite/sol-full-body.png"],
  ["calculus-painted-scene.jpg", "art/ignite/painted-style-reference.jpg"],
  ["fonts/Nunito.ttf", "fonts/Nunito.ttf"],
  ["fonts/Nunito-OFL.txt", "fonts/Nunito-OFL.txt"],
  ["fonts/RammettoOne-Regular.ttf", "fonts/RammettoOne-Regular.ttf"],
  ["fonts/RammettoOne-OFL.txt", "fonts/RammettoOne-OFL.txt"],
];
for (const [source, target] of copies) {
  const from = path.resolve(root, "../assets", source);
  const to = path.join(publicDir, target);
  try {
    await access(from);
  } catch {
    throw new Error(`Original Ignite asset missing: ${from}`);
  }
  await mkdir(path.dirname(to), { recursive: true });
  try {
    await copyFile(from, to, 1); // COPYFILE_EXCL: never replace a custom artwork file.
    console.log(`Copied ${target}`);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error;
    const same = (await readFile(from)).equals(await readFile(to));
    console.log(
      same
        ? `Reusing ${target}`
        : `Keeping modified artwork (differs from original): ${to}`,
    );
  }
}
