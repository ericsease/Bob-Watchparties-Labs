# Post-trial feedback — action plan

---

## 1. "Bob Settings → MCP, Modes zeigen" *(show in the IDE during setup)*

**What to do:** Add a presenter note to Setup Step 4 and Step 5 in `lab5/README.md`
pointing the presenter to open Bob's Settings UI and walk the audience through the
MCP and Modes panels before typing the first prompt.

**Action:** Add a `> 🎤 **Presenter note:**` block to Setup Step 4 (mode selector) and
Step 5 (MCP) saying: *"Open Settings → Modes to show the Java Architect entry.
Then open Settings → MCP to show the fetch server registered."*

---

## 2. "`.bob` must be in root — otherwise it won't work"

**Answer:** Correct. Bob resolves `.bob/` relative to the workspace root. If someone
opens `lab5/service/` as their workspace instead of the repo root (or `lab5/`), the
custom mode, hooks, skill, and MCP config are all invisible.

**What to do:** Add an explicit callout box in Setup Step 4 warning the presenter:
*"⚠️ Workspace root must be the repo root or `lab5/` — not a subdirectory like
`lab5/service/`. If the mode selector doesn't show ☕ Java Architect, this is why."*

---

## 3. "Can you configure in a rule that Bob should always auto-approve certain things like MCP, but disable others?"

**Answer:** Partially. Auto-approval in Bob is configured in settings, not rules files.
You can set `"autoApprove": true` globally or per tool group in `.bob/settings.json`.
There is no granular "approve MCP calls but block file writes" toggle in the current IDE —
auto-approval is currently all-or-nothing per tool category (read, write, execute, MCP).
Rules files (`*.md` in `.bob/rules/`) can *instruct* Bob to ask before certain actions,
but that's prompt-level guidance — it doesn't enforce at the platform level the way hooks do.
For the demo, the hook (`validate-pom.sh`) is the deterministic gate; auto-approval can be
left on without risk because the hook intercepts bad writes before they land.

**What to do:** Add a short FAQ callout in `hooks-explainer.md` answering this directly
for anyone who asks during the demo.

---

## 4. "Java Architect should create an MD plan file with todos — need to add to instructions"

**Answer:** Rule 6 of the custom mode (`customInstructions`) already says
*"Before modifying any file, output a short migration plan"* — but it only requires Bob to
*output* the plan in chat, not write it to disk.

**What to do:** Add rule 8 to `customInstructions` in **both** `lab5/.bob/custom_modes.yaml`
and `.bob/custom_modes.yaml`:

> 8. **Write a plan file**: When asked to assess or plan a migration, always write the plan to
>    a markdown file (`migration-plan.md` at the workspace root) with a Todo checklist using
>    `[ ]` checkboxes. Update the checklist as tasks complete.

---

## 5. "Include Secure Coder — probably not on short notice"

**Answer:** Agreed, skip for now. Secure Coder is a separate persona/mode that would
need its own setup and demo beat. Flag as a future extension.

**What to do:** Nothing for this iteration. Add a note under 🚀 Next Steps in the README
mentioning it as a possible extension.

---

## 6. "Subagent will only get called if you check auto-permission — need a note in the guide"

**Answer:** Correct. Subagents require the `subagent` permission group in the mode AND
the user must have auto-approve enabled (or manually approve the spawn). Without auto-approve,
Bob will pause and ask the user to confirm the subagent spawn — which breaks the "watch it
work in the background" demo moment.

**What to do:** Add a ⚠️ callout to Setup Step 4 in `lab5/README.md`:
*"For the subagent steps to run without interruption, enable auto-approval in Bob's settings
before the demo. The ☕ Java Architect mode has the `subagent` group enabled — but Bob will
still pause for user confirmation unless auto-approve is on."*

---

## 7. "Bob Findings erwähnen" *(mention Bob Findings)*

**What to do:** Add Bob Findings as a named step (or a callout inside the security audit step)
in Act 2. After the Security Auditor subagent finishes, add a prompt asking Bob to run a
Findings scan on the modernized code. This shows the audience that automated quality gates
exist beyond what the subagent wrote manually.

Suggested placement: new Step 12.5 between the test verification (Step 12) and Act 3.

Suggested prompt to add to the README:
```
Run Bob Findings on the modernized inventory service source files.
Summarise any security, quality, or style findings.
```

---

## 8. "Rule for Session summary"

**Answer:** This can be done with a `SessionStop` (or `PostToolUse` on the last tool) hook,
or more reliably as a rule in `.bob/rules/` that instructs Bob to write a session summary
when the user says something like "done" or "end session". Hook-based approaches are more
reliable because they fire automatically; rule-based approaches depend on the user triggering them.

**What to do:** Add a `session-summary.md` rule file to `lab5/.bob/rules/` with the
instruction:
> When the user indicates the session is ending (e.g. "done", "wrap up", "end session",
> "generate summary"), write a `session-summary.md` file to the workspace root summarising:
> what was assessed, what was changed, what tests were added, what infrastructure was created,
> and what's left to do. Format it as a markdown document with sections and a final todo checklist.

---

## Implementation order

- [x] **2 + 6**: Add workspace root warning + auto-approve note to Setup Step 4 in README
- [x] **1**: Add Settings UI presenter notes to Setup Steps 4 and 5
- [x] **4**: Add rule 8 (plan file) to both custom_modes.yaml files
- [x] **7**: Add Bob Findings step/callout to Act 2 in README
- [x] **8**: Create `lab5/.bob/rules/session-summary.md` rule file
- [x] **3**: ~~Add auto-approve FAQ to `hooks-explainer.md`~~ — cancelled per decision; FAQ added to hooks-explainer.md as reference doc instead (not in README)
- [x] **5**: Add Secure Coder mention to Next Steps in README
- [x] Update `hooks-explainer.md` Hook 1 description (now references `validate-pom.sh`)
