#!/bin/sh
# demo-reset.sh
#
# Run this before any lab demo session.
# Creates a fresh demo branch, restores lab source files, verifies prerequisites,
# and pre-warms Maven (if applicable).
#
# Usage:
#   sh demo-reset.sh <lab-dir>
#
#   <lab-dir>  — the lab directory to reset, e.g. lab5 or lab3
#                Defaults to the most recently modified labN directory if omitted.
#
# What it does:
#   1. Ensures you are on main and it is clean
#   2. Restores any lab source files to their original state
#   3. Cuts a new dated demo branch  (demo/<lab-dir>-YYYYMMDD)
#   4. Pre-warms Maven dependency cache (if a Maven service sub-dir exists)
#   5. Verifies Java, Maven, Node, and Python versions
#   6. Prints a final go/no-go checklist

set -e

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
NC='\033[0m'

ok()   { printf "${GRN}✅  %s${NC}\n" "$1"; }
warn() { printf "${YLW}⚠️   %s${NC}\n" "$1"; }
fail() { printf "${RED}❌  %s${NC}\n" "$1"; exit 1; }

# ── Resolve lab directory ──────────────────────────────────────────────────────
if [ -n "$1" ]; then
  LAB_DIR="$1"
else
  # Default: most recently modified labN directory
  LAB_DIR=$(ls -dt lab[0-9]*/ 2>/dev/null | head -1 | tr -d '/')
  if [ -z "$LAB_DIR" ]; then
    fail "No labN directory found in $(pwd). Pass a lab directory as argument: sh demo-reset.sh lab5"
  fi
  warn "No lab specified — defaulting to '$LAB_DIR'"
fi

if [ ! -d "$LAB_DIR" ]; then
  fail "Lab directory '$LAB_DIR' does not exist."
fi

echo ""
echo "=== demo-reset.sh  [${LAB_DIR}] ==="
echo ""

# ── 1. Must be on main ────────────────────────────────────────────────────────
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
  fail "Not on main (currently on '$BRANCH'). Run: git checkout main"
fi
ok "On branch: main"

# ── 2. Working tree must be clean ─────────────────────────────────────────────
if ! git diff --quiet || ! git diff --cached --quiet; then
  printf "${RED}❌  Uncommitted changes detected. Stash or commit them first.${NC}\n"
  git status --short
  exit 1
fi
ok "Working tree clean"

# ── 3. Restore lab source files to pristine state ─────────────────────────────
# Reset any tracked files under the lab directory that were modified during the demo
git checkout -- "$LAB_DIR/" 2>/dev/null || true

# If the lab ships a .demo-reference directory, apply its overrides.
# Convention: files inside .demo-reference are named <target-filename>.<tag> and
# are copied to their target paths to restore the "legacy" starting state.
#   pom.xml.legacy          → <service-dir>/pom.xml
#   ci.yml.reference        → kept in place (reference only, not copied)
DEMO_REF="$LAB_DIR/.demo-reference"
if [ -d "$DEMO_REF" ]; then
  # Restore legacy pom.xml if present (main carries the modernized version)
  if [ -f "$DEMO_REF/pom.xml.legacy" ]; then
    SERVICE_DIR=$(find "$LAB_DIR" -name "pom.xml" -not -path "*/.demo-reference/*" | head -1 | xargs dirname 2>/dev/null)
    if [ -n "$SERVICE_DIR" ]; then
      cp "$DEMO_REF/pom.xml.legacy" "$SERVICE_DIR/pom.xml"
    fi
  fi
fi

# Remove generated artefacts that should not exist at demo start
# These are repo-root files Bob generates during the session
rm -f migration-plan.md session-summary.md

# Remove any lab-level generated artefacts
rm -f "$LAB_DIR/.github/workflows/ci.yml" 2>/dev/null || true

# Remove generated test directories (Bob writes these during the demo)
find "$LAB_DIR" -type d -name "test" -path "*/src/test" | while read d; do
  rm -rf "$d"
done

# Remove files that are committed to main as reference but must not exist at demo
# start. Convention: list them in <lab-dir>/.demo-reference/remove-on-reset.txt,
# one relative-to-repo-root path per line.
REMOVE_LIST="$DEMO_REF/remove-on-reset.txt"
if [ -f "$REMOVE_LIST" ]; then
  while IFS= read -r fpath || [ -n "$fpath" ]; do
    [ -z "$fpath" ] && continue
    rm -f "$fpath" && warn "Removed (per remove-on-reset.txt): $fpath" || true
  done < "$REMOVE_LIST"
fi

ok "${LAB_DIR} source files restored to starting state"

# ── 4. Cut a fresh demo branch ────────────────────────────────────────────────
DEMO_BRANCH="demo/${LAB_DIR}-$(date +%Y%m%d)"

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
  *) warn "Java 17+ recommended. Found: $JAVA_VER" ;;
esac

# Maven (only relevant if a pom.xml exists in the lab)
if find "$LAB_DIR" -name "pom.xml" -not -path "*/.demo-reference/*" | grep -q .; then
  MVN_VER=$(mvn -version 2>/dev/null | head -1 || echo "not found")
  case "$MVN_VER" in
    *"not found"*) warn "Maven not found. Install: brew install maven" ;;
    *) ok "Maven: $MVN_VER" ;;
  esac
else
  warn "No pom.xml found under $LAB_DIR — skipping Maven check"
fi

# Node (for MCP fetch server)
NODE_VER=$(node --version 2>/dev/null || echo "not found")
case "$NODE_VER" in
  *"not found"*) warn "Node.js not found — MCP fetch server won't work" ;;
  v1[89]*|v2*) ok "Node: $NODE_VER" ;;
  *) warn "Node $NODE_VER found — recommend 18+. MCP may still work." ;;
esac

# Python (for any dashboard/watch scripts)
PY_VER=$(python3 --version 2>/dev/null || echo "not found")
case "$PY_VER" in
  *"not found"*) warn "Python 3 not found — dashboard scripts won't start" ;;
  *) ok "Python: $PY_VER" ;;
esac

# npx mcp-fetch-server resolvable
if npx -y mcp-fetch-server --help > /dev/null 2>&1; then
  ok "MCP fetch server: resolvable"
else
  warn "MCP fetch server not resolvable via npx — run 'npx -y mcp-fetch-server --help' manually"
fi

# ── 6. Pre-warm Maven (if applicable) ─────────────────────────────────────────
SERVICE_POM=$(find "$LAB_DIR" -name "pom.xml" -not -path "*/.demo-reference/*" | head -1)
if [ -n "$SERVICE_POM" ]; then
  SERVICE_DIR=$(dirname "$SERVICE_POM")
  echo ""
  echo "--- Pre-warming Maven dependency cache ---"
  (cd "$SERVICE_DIR" && mvn dependency:resolve -q 2>/dev/null) && ok "Maven cache warm" \
    || warn "mvn dependency:resolve failed — check that Java 17 JDK is on PATH"

  echo ""
  echo "--- Verifying service compiles ---"
  (cd "$SERVICE_DIR" && mvn compile -q 2>/dev/null) && ok "mvn compile passed" \
    || printf "${RED}❌  mvn compile failed — fix before demo${NC}\n"
fi

# ── 7. Final checklist ────────────────────────────────────────────────────────
echo ""
echo "================================================"
echo "  Pre-demo checklist — complete these manually"
echo "================================================"
echo ""
echo "  [ ] Open Bob with repo root (or $LAB_DIR/) as workspace"
echo "  [ ] Confirm the lab mode appears in the mode selector"
echo "  [ ] Enable auto-approve in Bob Settings"
echo "  [ ] Open Settings → MCP, confirm required servers are registered"
if [ -n "$SERVICE_POM" ]; then
  echo "  [ ] Start the service:   cd $SERVICE_DIR && mvn spring-boot:run"
fi
if find "$LAB_DIR" -name "watch.py" | grep -q .; then
  WATCH_DIR=$(find "$LAB_DIR" -name "watch.py" | head -1 | xargs dirname)
  echo "  [ ] Start the dashboard: cd $WATCH_DIR && python3 watch.py"
fi
echo "  [ ] Close/hide this terminal — open clean ones for the demo"
echo ""
echo "  Demo branch: $DEMO_BRANCH"
echo "  After the demo: git checkout main"
echo ""
ok "demo-reset.sh complete — you're ready to go  [${LAB_DIR}]"
echo ""
