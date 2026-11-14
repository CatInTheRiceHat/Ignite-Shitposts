import assert from "node:assert/strict";
import path from "node:path";
import { test } from "node:test";
import { resolveEpisodeConfig, workflowRoot } from "../scripts/paths";

test("episode names select the same edit from any working directory", () => {
  const expected = path.join(workflowRoot, "episodes", "another_short", "edit.json");
  for (const cwd of [workflowRoot, path.dirname(workflowRoot), "/tmp"]) {
    assert.equal(resolveEpisodeConfig("another_short", cwd), expected);
  }
});

test("explicit edits and episode folders resolve from the caller without selecting a demo", () => {
  const caller = path.join(workflowRoot, "episodes", "another_short");
  assert.equal(resolveEpisodeConfig("alternate.json", caller), path.join(caller, "alternate.json"));
  assert.equal(resolveEpisodeConfig("./another_short", path.dirname(caller)), path.join(caller, "edit.json"));
  assert.equal(resolveEpisodeConfig(path.join(caller, "alternate.json"), "/tmp"), path.join(caller, "alternate.json"));
});
