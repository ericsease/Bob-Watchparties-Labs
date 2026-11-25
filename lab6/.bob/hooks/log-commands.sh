#!/usr/bin/env bash
# PostToolUse hook — logs executed shell commands with a timestamp.

COMMAND="${1:-unknown}"
LOG_FILE="lab6/.bob/hooks/command-log.txt"

mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $COMMAND" >> "$LOG_FILE"

exit 0
