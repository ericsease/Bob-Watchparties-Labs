# Hooks Explainer — for the presenter

This directory contains Bob lifecycle hook scripts for the Java Modernization lab.

## What's configured

Hooks are defined in `lab5/.bob/settings.json` and apply to this workspace.

### Hook 1 — `check-secrets.sh` (blocking)

**Type:** `PreToolUse`
**Fires before:** `write_file`, `apply_diff`, `search_and_replace`, `insert_content`
**Effect:** **Blocks** Bob from writing any file that contains hardcoded credentials.

**Demo moment:** During Act 3, ask Bob to update `application.properties`. Bob will try
to write the file, the hook fires, Bob sees the block message, and then Bob pivots to
externalizing the secret to an environment variable instead.

**What the audience sees:** Bob stops mid-action and explains why — not because you told
it to, but because a deterministic guard caught it. This is the "AI + deterministic code"
combination moment.

### Hook 2 — `log-commands.sh` (non-blocking)

**Type:** `PostToolUse`
**Fires after:** `execute_command`
**Effect:** Appends every shell command Bob runs to `.bob/hooks/command-log.txt`.

**Demo moment:** After running `mvn test`, show the audience the log file. Say:
"Every command Bob ran is audited here. You have a full record."

### Hook 3 — `session-context.sh` (context injection)

**Type:** `SessionStart`
**Fires:** Once when Bob opens the workspace.
**Effect:** Injects project metadata (branch, Java version, key files) into Bob's context
so it starts the session already knowing what it's working with.

**Demo moment:** Show that Bob's first response already mentions the correct Java version
and key files without being told — because the hook seeded the context.

## Setup

Make scripts executable before the demo:

```bash
chmod +x lab5/.bob/hooks/*.sh
```

The `settings.json` is workspace-scoped — it only applies when Bob is opened with
`lab5/` (or the repo root) as the workspace.
