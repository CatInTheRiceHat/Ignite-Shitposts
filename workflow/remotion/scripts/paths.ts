import path from "node:path";
import { fileURLToPath } from "node:url";

export const remotionRoot = fileURLToPath(new URL("../", import.meta.url));
export const workflowRoot = path.resolve(remotionRoot, "..");

// Names are stable from any working directory; explicit paths belong to the caller.
export function resolveEpisodeConfig(value: string, cwd: string): string {
  if (/^[A-Za-z0-9_-]+$/.test(value)) {
    return path.join(workflowRoot, "episodes", value, "edit.json");
  }
  const resolved = path.resolve(cwd, value);
  return path.extname(resolved).toLowerCase() === ".json"
    ? resolved
    : path.join(resolved, "edit.json");
}
