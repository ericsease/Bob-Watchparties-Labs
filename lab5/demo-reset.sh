#!/bin/sh
# demo-reset.sh
#
# Run this before every Lab 5 demo session.
# Creates a fresh demo branch, verifies all prerequisites, and pre-warms Maven.
#
# Usage:
#   sh lab5/demo-reset.sh
#
# What it does:
#   1. Ensures you are on main and it is clean
#   2. Restores any lab5 source files to their original legacy state
#   3. Cuts a new dated demo branch
#   4. Pre-warms Maven dependency cache
#   5. Verifies Java, Maven, Node, and Python versions
#   6. Prints a final go/no-go checklist

set -e

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
NC='\033[0m'

ok()   { printf "${GRN}✅  %s${NC}\n" "$1"; }
warn() { printf "${YLW}⚠️   %s${NC}\n" "$1"; }
fail() { printf "${RED}❌  %s${NC}\n" "$1"; }

echo ""
echo "=== Lab 5 demo-reset.sh ==="
echo ""

# ── 1. Must be on main ────────────────────────────────────────────────────────
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
  fail "Not on main (currently on '$BRANCH'). Run: git checkout main"
  exit 1
fi
ok "On branch: main"

# ── 2. Working tree must be clean ─────────────────────────────────────────────
if ! git diff --quiet || ! git diff --cached --quiet; then
  fail "Uncommitted changes detected. Stash or commit them first."
  git status --short
  exit 1
fi
ok "Working tree clean"

# ── 3. Restore legacy source files to pristine state ─────────────────────────
# (resets any changes from a previous demo run)
git checkout -- lab5/service/src/ lab5/service/pom.xml \
                lab5/service/src/main/resources/application.properties 2>/dev/null || true

# Remove any generated artefacts from the previous session
# NOTE: lab5/demo-issues.md is intentionally NOT removed — it persists across runs
rm -f migration-plan.md session-summary.md
rm -f lab5/.github/workflows/ci.yml 2>/dev/null || true
rm -rf lab5/service/src/test/ 2>/dev/null || true
# SecurityConfig.java is committed to main (for reference) but must not exist at demo
# start — Bob adds it in Step 14 as part of the Spring Security configuration demo
rm -f lab5/service/src/main/java/com/example/inventory/SecurityConfig.java

ok "Lab5 source files restored to legacy state"

# ── 4. Cut a fresh demo branch ────────────────────────────────────────────────
DEMO_BRANCH="demo/lab5-$(date +%Y%m%d)"

# If branch already exists (re-running same day), delete and recreate
if git rev-parse --verify "$DEMO_BRANCH" > /dev/null 2>&1; then
  warn "Branch $DEMO_BRANCH already exists — deleting and recreating"
  git branch -D "$DEMO_BRANCH"
fi

git checkout -b "$DEMO_BRANCH"
ok "Created demo branch: $DEMO_BRANCH"

# ── 5. Verify prerequisites ───────────────────────────────────────────────────
echo ""
echo "--- Checking prerequisites ---"

# Java 17+
JAVA_VER=$(java -version 2>&1 | head -1)
case "$JAVA_VER" in
  *17*|*21*|*23*|*24*) ok "Java: $JAVA_VER" ;;
  *) fail "Java 17+ required. Found: $JAVA_VER" ;;
esac

# Maven
MVN_VER=$(mvn -version 2>/dev/null | head -1 || echo "not found")
case "$MVN_VER" in
  *"not found"*) fail "Maven not found. Install: brew install maven" ;;
  *) ok "Maven: $MVN_VER" ;;
esac

# Node (for MCP fetch server)
NODE_VER=$(node --version 2>/dev/null || echo "not found")
case "$NODE_VER" in
  *"not found"*) warn "Node.js not found — MCP fetch server won't work (Act 4 only)" ;;
  v1[89]*|v2*) ok "Node: $NODE_VER" ;;
  *) warn "Node $NODE_VER found — recommend 18+. MCP may still work." ;;
esac

# Python (for dashboard)
PY_VER=$(python3 --version 2>/dev/null || echo "not found")
case "$PY_VER" in
  *"not found"*) fail "Python 3 not found — dashboard won't start" ;;
  *) ok "Python: $PY_VER" ;;
esac

# npx mcp-fetch-server resolvable
if npx -y mcp-fetch-server --help > /dev/null 2>&1; then
  ok "MCP fetch server: resolvable"
else
  warn "MCP fetch server not resolvable via npx — run 'npx -y mcp-fetch-server --help' manually"
fi

# ── 6. Pre-warm Maven ─────────────────────────────────────────────────────────
echo ""
echo "--- Pre-warming Maven dependency cache (avoids cold-download during demo) ---"
(cd lab5/service && mvn dependency:resolve -q 2>/dev/null) && ok "Maven cache warm" \
  || warn "mvn dependency:resolve failed — check that Java 17 JDK is on PATH"

# ── 7. Verify service starts (quick check) ────────────────────────────────────
echo ""
echo "--- Verifying service compiles ---"
(cd lab5/service && mvn compile -q 2>/dev/null) && ok "mvn compile passed" \
  || fail "mvn compile failed — fix before demo"

# ── 8. Final checklist ────────────────────────────────────────────────────────
echo ""
echo "================================================"
echo "  Pre-demo checklist — complete these manually"
echo "================================================"
echo ""
echo "  [ ] Open Bob with repo root (or lab5/) as workspace"
echo "  [ ] Confirm ☕ Java Architect appears in mode selector"
echo "  [ ] Enable auto-approve in Bob Settings"
echo "  [ ] Open Settings → MCP, confirm 'fetch' server is registered"
echo "  [ ] Start the Java service:   cd lab5/service && mvn spring-boot:run"
echo "  [ ] Start the dashboard:      cd lab5/dashboard && python3 watch.py"
echo "  [ ] Verify dashboard shows 5 items at http://localhost:8080/api/inventory"
echo "  [ ] Close/hide this terminal — open two clean ones for the demo"
echo ""
echo "  Demo branch: $DEMO_BRANCH"
echo "  After the demo: git checkout main"
echo ""
ok "demo-reset.sh complete — you're ready to go"
echo ""
