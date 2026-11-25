#!/usr/bin/env bash
# PreToolUse hook — warns before any write operation targets raw data files.
# Keeps participants from accidentally overwriting the source dataset.

TOOL_PATH="${1:-}"

# Check if the target path is inside a data/ directory and is .xlsx or .csv
if [[ "$TOOL_PATH" == *"/data/"* && ( "$TOOL_PATH" == *.xlsx || "$TOOL_PATH" == *.csv ) ]]; then
  echo ""
  echo "⚠️  DATA FILE PROTECTION WARNING"
  echo "   You are about to write to a raw data file:"
  echo "   $TOOL_PATH"
  echo ""
  echo "   Raw data files in data/ should be treated as immutable."
  echo "   Consider writing your output to a new file instead, e.g.:"
  echo "     reorder_alerts.xlsx"
  echo "     financial_summary.xlsx"
  echo ""
  echo "   If you intentionally want to regenerate the source data,"
  echo "   run: python lab6/data/generate_data.py"
  echo ""
fi

exit 0
