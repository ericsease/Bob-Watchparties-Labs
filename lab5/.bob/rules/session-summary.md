# Session Summary Rule

When the user indicates the session is ending — for example by saying "done", "wrap up",
"end session", "generate summary", or "write a summary" — write a file named
`session-summary.md` to the workspace root.

The file must include the following sections:

## What was assessed
List the files and components Bob reviewed, with a one-line note on each finding.

## What was changed
List every file modified, what was changed, and which Java 17 pattern was applied
(e.g. record, stream, LocalDateTime, var).

## Tests added
List the test files created and what they cover.

## Infrastructure added
List any CI pipelines, Dockerfiles, config changes, or tooling added.

## Security improvements
List any hardcoded secrets removed, credentials externalized, or vulnerabilities addressed.

## What's left to do
A `[ ]` checkbox list of any remaining items from the migration plan that were not completed
in this session.

---

Format the file as clean markdown. Use concise bullet points. Do not include chat transcript
or raw tool output — only a human-readable summary a team member could act on.
