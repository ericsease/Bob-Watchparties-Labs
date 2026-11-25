#!/bin/sh
# log-commands.sh
#
# PostToolUse hook — logs every shell command Bob runs to a local audit file.
# Fires after: execute_command
#
# Bob sends a JSON payload on stdin; the command is tool_input.command.
# Appends a timestamped entry to .bob/hooks/command-log.txt (relative to the
# workspace root, i.e. lab6/). The log is git-ignored and removed on demo reset.

PAYLOAD=$(cat)

COMMAND=$(echo "$PAYLOAD" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('tool_input', {}).get('command', '(unknown)'))
" 2>/dev/null || echo "(parse error)")

LOG_FILE=".bob/hooks/command-log.txt"
mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $COMMAND" >> "$LOG_FILE"

exit 0
