#!/bin/sh
# validate-pom.sh
#
# PreToolUse hook — validates proposed pom.xml content before it hits disk.
# Fires before: write_file, apply_diff, search_and_replace, insert_content
#
# Two-stage validation:
#   1. Python xml.etree — catches malformed XML instantly (no Maven needed)
#   2. mvn validate    — catches valid XML that's an invalid POM
#                        (missing groupId, bad coordinates, unknown packaging, etc.)
#
# Non-pom writes exit 0 immediately — zero overhead on other files.
# Proposed content is written to a temp dir so the real file is never touched
# if validation fails.
#
# Exit 2 to block Bob; exit 0 to allow.
#
# Stdin shape (PreToolUse):
#   { "tool_name": "write_file", "tool_input": { "path": "...", "content": "..." } }

# Do NOT use set -e — grep/mvn return non-zero on expected failures
PAYLOAD=$(cat)

# ── Extract file path ────────────────────────────────────────────────────────
FILE_PATH=$(echo "$PAYLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('tool_input', {}).get('path', ''))
" 2>/dev/null || echo "")

# Only care about pom.xml writes
case "$FILE_PATH" in
  *pom.xml) ;;
  *) exit 0 ;;
esac

# ── Extract proposed content ─────────────────────────────────────────────────
CONTENT=$(echo "$PAYLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
# write_file sends 'content'; patch tools send 'diff'
val = inp.get('content') or inp.get('diff') or ''
print(val)
" 2>/dev/null || echo "")

# If we couldn't extract content (e.g. apply_diff payload), fall back to the
# file on disk — validates the post-patch state one step behind, but still useful
if [ -z "$CONTENT" ] && [ -f "$FILE_PATH" ]; then
  CONTENT=$(cat "$FILE_PATH")
fi

if [ -z "$CONTENT" ]; then
  exit 0
fi

# ── Stage 1: XML well-formedness ─────────────────────────────────────────────
XML_ERROR=$(echo "$CONTENT" | python3 -c "
import sys, xml.etree.ElementTree as ET
try:
    ET.fromstring(sys.stdin.read())
    print('')
except ET.ParseError as e:
    print(str(e))
" 2>/dev/null)

if [ -n "$XML_ERROR" ]; then
  echo "🔒 HOOK BLOCKED: pom.xml is not valid XML." >&2
  echo "   Parse error: $XML_ERROR" >&2
  echo "" >&2
  echo "   Fix the XML syntax before Bob writes this file." >&2
  exit 2
fi

# ── Stage 2: Maven POM validation ────────────────────────────────────────────
TMPDIR_HOOK=$(mktemp -d)
TMP_POM="$TMPDIR_HOOK/pom.xml"
echo "$CONTENT" > "$TMP_POM"

MVN_OUTPUT=$(mvn validate -f "$TMP_POM" --no-transfer-progress -q 2>&1)
MVN_EXIT=$?

rm -rf "$TMPDIR_HOOK"

if [ $MVN_EXIT -ne 0 ]; then
  echo "🔒 HOOK BLOCKED: pom.xml failed Maven validation." >&2
  echo "" >&2
  echo "$MVN_OUTPUT" | head -20 >&2
  echo "" >&2
  echo "   Bob will read this error and self-correct before retrying." >&2
  exit 2
fi

echo "✅ pom.xml validated successfully (XML + Maven)." >&2
exit 0
