---
name: demo-reset
description: Use when resetting any lab demo environment — switches off the current demo branch back to main, resolves a clean working tree, deletes the old demo branch, and runs demo-reset.sh to cut a fresh dated branch. Works for any labN directory. Trigger phrases: "reset the demo", "run demo reset", "get a fresh branch", "delete demo branch", "start over from main", "prep the demo", "reset lab", "reset lab5", "reset lab3".
metadata:
  user-invocable: true
  disable-model-invocation: false
---

# Lab Demo Reset

Resets any lab to its starting state and cuts a fresh demo branch. Follow these steps in order —
each depends on the previous one.

## Step 1 — Identify the lab

If the user specified a lab (e.g. "reset lab5", "prep lab3"), use that directory name.
If not, ask which lab they want to reset before continuing.

## Step 2 — Note the current branch

Run:
```
git rev-parse --abbrev-ref HEAD
```

Save the branch name. If it is already `main`, jump to Step 4.

## Step 3 — Switch to main

Run:
```
git checkout main
```

If this fails because of local modifications, go to Step 3a. Otherwise continue to Step 4.

### Step 3a — Handle uncommitted changes blocking checkout

Check what is dirty:
```
git status --short
```

Apply the appropriate fix for each item:

| Situation | Fix |
|---|---|
| Deleted tracked file | `git checkout -- <file>` to restore it |
| Untracked files (e.g. `command-log.txt`, skill dirs) | Safe to ignore — won't block checkout |
| Modified tracked files from a previous demo run | `git checkout -- <file>` to discard |
| Staged changes to keep | `git stash` |

After resolving, re-run `git checkout main`. Repeat until checkout succeeds.

## Step 4 — Delete the old demo branch

Only if a demo branch for this lab existed. Branch names follow the pattern `demo/<lab-dir>-YYYYMMDD`.

```
git branch -D demo/<lab-dir>-<date>
```

If the branch does not exist, that is fine — continue.

## Step 5 — Verify the working tree is clean

Run:
```
git status --short
```

The reset script will exit early if tracked files are modified. Untracked files are fine.
Fix any remaining dirty tracked files with `git checkout -- <file>`.

## Step 6 — Run the reset script

The root-level script accepts the lab directory as an argument:

```
sh demo-reset.sh <lab-dir>
```

For example: `sh demo-reset.sh lab5` or `sh demo-reset.sh lab3`.

Use `timeout_seconds: 180` when calling `execute_command` — Maven pre-warm can take 60–120 s on
a cold cache. A timeout after the `✅ Created demo branch` line is not a failure; all critical
steps (restore, branch cut, prereq checks) complete before the Maven warm-up.

## Step 7 — Confirm success

The script prints a final checklist. Confirm these lines appeared:

- `✅ On branch: main`
- `✅ Working tree clean`
- `✅ <lab-dir> source files restored to starting state`
- `✅ Created demo branch: demo/<lab-dir>-<date>`
- `✅ Java ...` and `✅ Maven ...` (if applicable)

Report the new branch name to the user.

## Step 8 — Surface any warnings

If the script printed `⚠️` or `❌` lines, explain them:

| Output | Meaning |
|---|---|
| `⚠️ No lab specified — defaulting to '<lab>'` | Script inferred the lab from the most recently modified labN dir |
| `⚠️ Branch demo/... already exists — deleting and recreating` | Normal when re-running the same day |
| `⚠️ Node.js not found` | MCP fetch server won't work — non-blocking for most lab acts |
| `⚠️ MCP fetch server not resolvable via npx` | Run `npx -y mcp-fetch-server --help` manually |
| `⚠️ mvn dependency:resolve failed` | Maven cache not warmed — run `mvn compile -q` in the service dir before demo |
| `❌ mvn compile failed` | Must be fixed before demo — show the Maven error output to the user |

## Known issues

- **Deleted tracked file shows as `D` in git status** — common after a previous demo run (e.g.
  `SecurityConfig.java` in lab5). Restore with `git checkout -- <path>` before switching to main.
  The reset script will remove it again as part of its restore step.
- **Maven pre-warm times out** — not a problem. Manually confirm with
  `cd <lab-dir>/service && mvn compile -q` before starting the demo.
- **Lab has no `.demo-reference` dir** — the script handles this gracefully; it skips the
  reference-file restore and only resets tracked git changes.
