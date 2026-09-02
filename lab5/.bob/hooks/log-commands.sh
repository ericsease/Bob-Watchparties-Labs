#!/bin/sh
# log-commands.sh
#
# PostToolUse hook — logs every shell command Bob runs to a local audit file.
# Fires after: execute_command
#
# Non-blocking (PostToolUse cannot exit 2 to block).
# Appends a timestamped entry to .bob/hooks/command-log.txt
#
# Stdin shape (PostToolUse):
#   { "tool": "execute_command", "input": { "command": "..." }, "output": "..." }

PAYLOAD=$(cat)

COMMAND=$(echo "$PAYLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('input', {}).get('command', '(unknown)'))
" 2>/dev/null || echo "(parse error)")

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOG_FILE=".bob/hooks/command-log.txt"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

echo "[$TIMESTAMP] $COMMAND" >> "$LOG_FILE"

exit 0
