#!/bin/sh
# session-context.sh
#
# SessionStart hook — injects project context into Bob's model context at the
# start of every session. Stdout is written to the model as additional context.
#
# This tells Bob upfront: what project this is, which branch we're on,
# and what Java version is available — so it doesn't have to ask.

echo "=== Lab 5 — Java Modernization Session ==="
echo "Project: inventory-service (legacy Java 8 → target Java 17)"
echo "Git branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"
echo "Java version: $(java -version 2>&1 | head -1 || echo 'not found')"
echo "Maven version: $(mvn -version 2>/dev/null | head -1 || echo 'not found')"
echo "Working directory: $PWD"
echo ""
echo "Key files:"
echo "  lab5/service/src/main/java/com/example/inventory/ — legacy Java 8 source"
echo "  lab5/service/src/main/resources/application.properties — ⚠ contains hardcoded secret"
echo "  lab5/.bob/custom_modes.yaml — Java Architect mode"
echo "  lab5/.bob/settings.json — active hooks (secret scan + command log)"
echo ""
echo "Modernization targets: Java 17 records, LocalDateTime, streams, Spring Boot 3.x"

exit 0
