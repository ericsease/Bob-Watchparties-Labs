#!/bin/sh
# check-data-quality.sh
#
# PreToolUse hook — protects the raw source dataset in lab6/data/.
# Fires before: write_file, apply_diff, search_and_replace, insert_content
#
# Bob sends a JSON payload on stdin; the target file is tool_input.path.
# If it points at an .xlsx or .csv inside a data/ directory, the write is denied
# and Bob is told why (so it can write to a new output file instead).
# Otherwise the hook exits 0 and the write proceeds.

PAYLOAD=$(cat)

FILE_PATH=$(echo "$PAYLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('tool_input', {}).get('path', ''))
" 2>/dev/null || echo "")

case "$FILE_PATH" in
  */data/*.xlsx|*/data/*.csv|data/*.xlsx|data/*.csv)
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Raw data files in data/ are immutable ($FILE_PATH). Write your output to a new file instead, e.g. reorder_alerts.xlsx or financial_summary.xlsx. To regenerate the source data on purpose, run: python data/generate_data.py"
  }
}
EOF
    ;;
esac

exit 0
