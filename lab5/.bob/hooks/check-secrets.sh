#!/bin/sh
# check-secrets.sh
#
# PreToolUse hook — blocks Bob from writing files that contain hardcoded secrets.
# Fires before: write_file, apply_diff, search_and_replace, insert_content
#
# Bob sends a JSON payload on stdin. We extract the file path and scan its
# PROPOSED content for secret patterns. Exit 2 to block; exit 0 to allow.
#
# Stdin shape (PreToolUse):
#   { "tool": "write_file", "input": { "path": "...", "content": "..." } }

# Do NOT use set -e — grep returns 1 on no match, which would cause premature exit

# Parse the incoming JSON payload
PAYLOAD=$(cat)

# Extract the file path
FILE_PATH=$(echo "$PAYLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('input', {}).get('path', ''))
" 2>/dev/null || echo "")

# Extract proposed content (write_file) or fall back to reading the current file
CONTENT=$(echo "$PAYLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('input', {})
# write_file sends 'content'; diff tools send the patch
print(inp.get('content', inp.get('diff', '')))
" 2>/dev/null || echo "")

# Secret patterns to scan for
PATTERNS="password=|passwd=|secret=|api_key=|apikey=|token=|private_key="

# Check proposed content first
if echo "$CONTENT" | grep -qiE "$PATTERNS"; then
  MATCHED=$(echo "$CONTENT" | grep -iE "$PATTERNS" | head -3)
  echo "🔒 HOOK BLOCKED: Hardcoded secret detected in proposed content for: $FILE_PATH" >&2
  echo "   Matched line(s):" >&2
  echo "$MATCHED" | sed 's/^/   /' >&2
  echo "" >&2
  echo "   Action required: move credentials to environment variables or a .env file." >&2
  exit 2
fi

# Also scan the target file if it already exists on disk
if [ -n "$FILE_PATH" ] && [ -f "$FILE_PATH" ]; then
  if grep -qiE "$PATTERNS" "$FILE_PATH" 2>/dev/null; then
    MATCHED=$(grep -iE "$PATTERNS" "$FILE_PATH" | head -3)
    echo "🔒 HOOK WARNING: Existing secrets found in $FILE_PATH" >&2
    echo "   Matched line(s):" >&2
    echo "$MATCHED" | sed 's/^/   /' >&2
    echo "" >&2
    echo "   This file already contains hardcoded credentials. Consider externalizing them." >&2
    # Warning only — don't block on existing file (only block on new writes)
  fi
fi

exit 0
