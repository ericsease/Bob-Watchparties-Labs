# Hooks Explainer — for the presenter

This directory contains Bob lifecycle hook scripts for the Java Modernization lab.

## What's configured

Hooks are defined in `lab5/.bob/settings.json` and apply to this workspace.

### Hook 1 — `validate-pom.sh` (blocking)

**Type:** `PreToolUse`
**Fires before:** `write_file`, `apply_diff`, `search_and_replace`, `insert_content`
**Effect:** **Blocks** Bob from writing `pom.xml` until the proposed content passes
Maven validation. Two-stage check: XML well-formedness (instant, no Maven needed),
then `mvn validate` in a temp directory — the real file is never touched if validation fails.

**Demo moment:** During Act 3, ask Bob to bump the Spring Boot version. Bob writes
`pom.xml`, the hook fires, runs `mvn validate` against the proposed content, and either
passes (`✅ pom.xml validated successfully.`) or blocks with the Maven error in chat.
If blocked, Bob reads the error and self-corrects — the **self-correction loop**.

**What the audience sees:** Bob stops mid-action, reads a compiler error, fixes itself,
and retries. This is the "AI + deterministic code" combination moment — behaviour you
cannot get from prompt engineering alone.

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

---

## Setup

Make scripts executable before the demo:

```bash
chmod +x lab5/.bob/hooks/*.sh
```

The `settings.json` is workspace-scoped — it only applies when Bob is opened with
`lab5/` (or the repo root) as the workspace.

---

## FAQ

**Q: Can you configure Bob to auto-approve some tool types but not others?**

Auto-approval in Bob is currently all-or-nothing — it's a global setting in Bob's UI,
not a per-tool-category toggle. You can't say "approve MCP calls but gate file writes"
through the settings panel.

Rules files (`.bob/rules/*.md`) can *instruct* Bob to ask before certain actions, but
that's prompt-level guidance — Bob may follow it, but it isn't enforced at the platform
level the way hooks are.

For this demo, the safest approach is: **enable auto-approve globally, rely on the hook
as the deterministic gate.** The `validate-pom.sh` hook will block any bad `pom.xml`
write regardless of auto-approve state — so there's no risk in leaving auto-approve on.
