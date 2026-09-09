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
# Tool-specific content extraction:
#   write_file         → use 'content' field directly (full file)
#   apply_diff         → apply SEARCH/REPLACE blocks to current file in a temp copy
#   search_and_replace → apply 'search'→'replace' substitution to current file
#   insert_content     → insert 'content' at 'line' in current file
#
# Non-pom writes exit 0 immediately — zero overhead on other files.
# Exit 2 to block Bob; exit 0 to allow.
#
# Stdin shape (PreToolUse):
#   { "tool_name": "write_file", "tool_input": { "path": "...", "content": "..." } }

# Do NOT use set -e — grep/mvn return non-zero on expected failures
PAYLOAD=$(cat)

# ── Extract tool name and file path ──────────────────────────────────────────
TOOL_NAME=$(echo "$PAYLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('tool_name', ''))
" 2>/dev/null || echo "")

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

# ── Build the post-edit content based on tool type ───────────────────────────
CONTENT=$(echo "$PAYLOAD" | python3 -c "
import sys, json, re

data = json.load(sys.stdin)
inp  = data.get('tool_input', {})
tool = data.get('tool_name', '')
path = inp.get('path', '')

# ── write_file: full replacement content ────────────────────────────────────
if tool == 'write_file':
    print(inp.get('content', ''))
    sys.exit(0)

# ── Read the current file from disk (needed for patch tools) ─────────────────
try:
    with open(path, 'r') as f:
        current = f.read()
except Exception:
    sys.exit(0)   # file doesn't exist yet — nothing to patch against

# ── apply_diff: parse SEARCH/REPLACE blocks and apply them ───────────────────
if tool == 'apply_diff':
    diff = inp.get('diff', '')
    # Split on block boundaries; each block has SEARCH ... ======= ... REPLACE
    blocks = re.split(r'<<<<<<< SEARCH\n', diff)
    result = current
    for block in blocks[1:]:   # skip preamble before first block
        parts = block.split('\n=======\n', 1)
        if len(parts) != 2:
            continue
        search_part = parts[0]
        replace_part = parts[1].split('\n>>>>>>> REPLACE', 1)[0]
        # Strip the optional :start_line: header from the search block
        search_clean = re.sub(r'^:start_line:\d+\n-+\n', '', search_part, flags=re.MULTILINE)
        result = result.replace(search_clean, replace_part, 1)
    print(result)
    sys.exit(0)

# ── search_and_replace: apply regex or literal substitution ──────────────────
if tool == 'search_and_replace':
    search  = inp.get('search', '')
    replace = inp.get('replace', '')
    use_re  = str(inp.get('use_regex', 'false')).lower() == 'true'
    ignore  = str(inp.get('ignore_case', 'false')).lower() == 'true'
    flags   = re.IGNORECASE if ignore else 0
    if use_re:
        result = re.sub(search, replace, current, flags=flags)
    else:
        if ignore:
            result = re.sub(re.escape(search), replace, current, flags=flags)
        else:
            result = current.replace(search, replace)
    print(result)
    sys.exit(0)

# ── insert_content: insert lines at the given line number ────────────────────
if tool == 'insert_content':
    content_to_insert = inp.get('content', '')
    line_num = int(inp.get('line', 0))
    lines = current.splitlines(keepends=True)
    if line_num == 0:
        result = current + content_to_insert
    else:
        insert_at = max(0, line_num - 1)
        lines.insert(insert_at, content_to_insert if content_to_insert.endswith('\n') else content_to_insert + '\n')
        result = ''.join(lines)
    print(result)
    sys.exit(0)

# Fallback — pass through current file
print(current)
" 2>/dev/null || echo "")

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
