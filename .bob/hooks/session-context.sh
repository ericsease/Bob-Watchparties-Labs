#!/bin/sh
# session-context.sh
#
# SessionStart hook — injects project context into Bob's model context at the
# start of every session. Stdout is written to the model as additional context.
#
# The repo root is the Bob workspace for every lab, so the context is chosen
# from the demo branch name (demo/<lab-dir>-YYYYMMDD). Anything that is not a
# lab6 branch gets the original Lab 5 context.

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')

case "$BRANCH" in
  demo/lab6-*|feature/lab6-*)
    echo "=== Lab 6 — Grocery Analytics with Bob ==="
    echo "Project: retail inventory analytics (Excel/CSV → pandas → Jupyter → SQLite), Düsseldorf/NRW context"
    echo "Git branch: $BRANCH"
    echo "Python version: $(python3 --version 2>&1 || echo 'not found')"
    echo "Working directory: $PWD"
    echo ""
    echo "Key files:"
    echo "  lab6/data/ — raw mock dataset (grocery_inventory.xlsx/csv, supplier_prices.csv, promo_calendar.csv, local_events_fallback.json) — treat as immutable"
    echo "  lab6/notebooks/starter.ipynb — participant notebook (4 stages)"
    echo "  lab6/notebooks/solution.ipynb — facilitator reference, do not open for participants"
    echo "  lab6/README.md — facilitator guide with copy-paste prompts"
    echo "  .bob/custom_modes.yaml — 📊 Data Analyst Architect mode (use this mode for Lab 6)"
    echo "  .bob/skills/grocery-analytics/SKILL.md — analytics playbook"
    echo "  .bob/personas/eda-analyst.md, event-crawler.md — Stage 2 subagent personas"
    echo ""
    echo "Run outputs (reorder_alerts.xlsx, financial_summary.xlsx, inventory.db) go in lab6/notebooks/, never in lab6/data/."
    ;;
  *)
    echo "=== Lab 5 — Java Modernization Session ==="
    echo "Project: inventory-service (legacy Java 8 → target Java 17)"
    echo "Git branch: $BRANCH"
    echo "Java version: $(java -version 2>&1 | head -1 || echo 'not found')"
    echo "Maven version: $(mvn -version 2>/dev/null | head -1 || echo 'not found')"
    echo "Working directory: $PWD"
    echo ""
    echo "Key files:"
    echo "  lab5/service/src/main/java/com/example/inventory/ — legacy Java 8 source"
    echo "  lab5/service/src/main/resources/application.properties — ⚠ contains hardcoded password=admin123"
    echo "  lab5/.bob/custom_modes.yaml — Java Architect custom mode"
    echo "  lab5/.bob/settings.json — active hooks (pom validation + command log)"
    echo "  lab5/.bob/rules/session-summary.md — session summary rule (say 'wrap up' to trigger)"
    echo ""
    echo "Modernization targets: Java 17 records, LocalDateTime, streams, Spring Boot 3.x"
    ;;
esac

exit 0
