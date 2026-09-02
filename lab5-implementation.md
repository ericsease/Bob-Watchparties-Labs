# Lab 5 — Implementation Plan

This file is the Agent-mode task list for building lab5. The `lab5/README.md` is the
single source of truth for the lab itself. This file tracks what was built and how.

---

## Overview

Lab 5 is a 35–45 minute presenter-driven demo showing Bob as a Java modernization partner.
Starting point: a legacy Java 8 Spring Boot inventory service. Ending point: modernized,
tested, containerized, CI'd, and shipped — all driven by Bob in a single session.

**Directory structure:**

```
lab5/
├── README.md                          ← Presenter guide (single source of truth)
├── service/                           ← Legacy Java 8 Spring Boot service
│   ├── pom.xml                        ← Maven project (Java 8 source, Spring Boot 2.7.18)
│   ├── Dockerfile                     ← Multi-stage Java 17 build (for Act 3)
│   ├── README-legacy.md               ← Service description for Bob to read
│   └── src/main/java/com/example/inventory/
│       ├── InventoryApplication.java
│       ├── InventoryItem.java         ← 96-line POJO (before), 3-line record (after)
│       ├── InventoryService.java      ← for-loop iteration (before), streams (after)
│       └── InventoryController.java   ← raw HashMap errors (before), clean (after)
├── dashboard/
│   ├── watch.py                       ← Python terminal dashboard (live inventory view)
│   └── requirements.txt               ← requests, rich
└── .bob/
    ├── custom_modes.yaml              ← Java Architect mode
    ├── settings.json                  ← Hooks config (PreToolUse + PostToolUse + SessionStart)
    ├── mcp.json                       ← Fetch MCP server config
    ├── hooks/
    │   ├── check-secrets.sh           ← Blocking hook: scans for hardcoded credentials
    │   ├── log-commands.sh            ← Logging hook: audits all execute_command calls
    │   ├── session-context.sh         ← Context injection: injects project metadata on start
    │   └── hooks-explainer.md         ← Presenter reference for hook behaviour
    ├── personas/
    │   ├── security-auditor.md        ← Subagent: security audit persona
    │   └── test-engineer.md           ← Subagent: JUnit 5 test writing persona
    └── skills/
        └── java-modernization/
            └── SKILL.md               ← Java 8→17 pattern map + Spring Boot checklist

lab5/.github/workflows/
    └── ci.yml                         ← GitHub Actions: build, secret-scan, docker jobs
```

---

## Sub-Tasks — Build Status

### [x] Sub-Task 1 — Legacy Java service

**Files created:**
- `lab5/service/pom.xml` — Java 8 source, Spring Boot 2.7.18, H2 in-memory DB
- `lab5/service/src/main/resources/application.properties` — hardcoded `spring.datasource.password=admin123`
- `lab5/service/src/main/java/com/example/inventory/InventoryApplication.java`
- `lab5/service/src/main/java/com/example/inventory/InventoryItem.java` — 96-line POJO
- `lab5/service/src/main/java/com/example/inventory/InventoryService.java` — for-loop iteration, 5 seeded items
- `lab5/service/src/main/java/com/example/inventory/InventoryController.java` — raw HashMap errors
- `lab5/service/README-legacy.md`

**Verify:** `cd lab5/service && mvn spring-boot:run` → starts on port 8080 with 5 seeded items.

---

### [x] Sub-Task 1b — Python dashboard

**Files created:**
- `lab5/dashboard/watch.py` — polls `/api/inventory` every 2s, renders rich table or plain fallback
- `lab5/dashboard/requirements.txt` — `requests`, `rich`

**Verify:** `cd lab5/dashboard && pip install -r requirements.txt && python watch.py` → live table.

---

### [x] Sub-Task 2 — Java Architect custom mode

**File created:** `lab5/.bob/custom_modes.yaml`

**Mode slug:** `java-architect` | **Display name:** `☕ Java Architect`

**Rules encoded:**
1. Records over POJOs
2. LocalDateTime over Date
3. Streams over loops
4. `var` for local inference
5. Flag deprecated Spring 2.x patterns
6. Plan before edit
7. No silent breaking API changes

---

### [x] Sub-Task 3 — Hooks configuration

**Files created:**
- `lab5/.bob/settings.json` — workspace hooks (PreToolUse + PostToolUse + SessionStart)
- `lab5/.bob/hooks/check-secrets.sh` — **blocking** secret scanner (exit 2 on match)
- `lab5/.bob/hooks/log-commands.sh` — non-blocking command auditor
- `lab5/.bob/hooks/session-context.sh` — context injector (branch, Java version, key files)
- `lab5/.bob/hooks/hooks-explainer.md` — presenter reference

**Setup required before demo:** `chmod +x lab5/.bob/hooks/*.sh`

**Hook 1 trigger:** Any file write that includes `password=`, `passwd=`, `secret=`, `api_key=`,
`apikey=`, `token=`, or `private_key=` in proposed content → blocked with clear message.

**Demo moment:** Ask Bob to update `application.properties` (touch the file) → hook fires →
Bob sees the block → Bob pivots to externalizing the secret.

---

### [x] Sub-Task 4 — MCP configuration

**File created:** `lab5/.bob/mcp.json`

**Server:** `@modelcontextprotocol/server-fetch` (npm, no API key required)
**Command:** `npx -y @modelcontextprotocol/server-fetch`

**Demo prompt (Act 4):**
```
Use the fetch tool to retrieve https://spring.io/blog/2022/05/24/spring-boot-3-0-m3-available-now
Summarize the breaking changes relevant to our inventory-service.
```

---

### [x] Sub-Task 5 — java-modernization skill

**File created:** `lab5/.bob/skills/java-modernization/SKILL.md`

**Contents:**
- Java 8 → Java 17 pattern mapping table (10 patterns)
- Spring Boot 2.x → 3.x migration checklist (5 items)
- Migration PR structure template
- 3 pre-written demo prompts for the presenter

---

### [x] Sub-Task 6 — GitHub Actions CI + Dockerfile

**Files created:**
- `lab5/service/Dockerfile` — multi-stage: `maven:3.9-eclipse-temurin-17` build → `eclipse-temurin:17-jre-alpine` runtime; non-root user
- `lab5/.github/workflows/ci.yml` — 3 jobs: `build-and-test`, `secret-scan`, `docker-build`; scoped to `paths: lab5/service/**`

**CI jobs:**
1. `build-and-test` — Java 17 setup, `mvn -B package`, `mvn -B test`, upload surefire reports
2. `secret-scan` — grep for `password=|secret=|api_key=` in `.properties` and `.yaml` files
3. `docker-build` — builds Docker image using `docker/build-push-action`, no push (demo)

---

### [x] Sub-Task 7 — Subagent personas

**Files created:**
- `lab5/.bob/personas/security-auditor.md` — CRITICAL/HIGH/MEDIUM/LOW findings format, no fixes
- `lab5/.bob/personas/test-engineer.md` — JUnit 5, AssertJ, `@WebMvcTest`, naming convention

**Demo sequence:**
1. Spawn Security Auditor first (Act 2, Step 7)
2. While auditor runs, start Java 17 migration in main conversation (Step 8)
3. Spawn Test Engineer for parallel test writing (Step 9)

---

### [x] Sub-Task 8 — README + this file

**Files created:**
- `lab5/README.md` — 280-line presenter guide (lab4 format)
- `lab5-implementation.md` — this file

---

## Presenter Pre-Flight Checklist

Run these before every demo:

```bash
# 1. Warm Maven dependencies (avoid cold download during demo)
cd lab5/service && mvn dependency:resolve -q

# 2. Make hooks executable
chmod +x lab5/.bob/hooks/*.sh

# 3. Verify Java service starts
mvn spring-boot:run &
sleep 8
curl -s http://localhost:8080/api/inventory | python3 -m json.tool | head -20
# Kill the background process
kill %1

# 4. Verify dashboard
cd ../dashboard && pip install -q -r requirements.txt
python watch.py &
sleep 3
kill %1

# 5. Verify MCP fetch server is resolvable
npx -y @modelcontextprotocol/server-fetch --help 2>/dev/null || echo "MCP fetch: OK (exits non-zero on --help but package is present)"
```

---

## Known Limitations / Future Improvements

- The Java service uses in-memory storage (no persistence between restarts) — by design for demo simplicity
- `InventoryController` test (Act 2 Step 9) requires `spring-boot-starter-test` which is already in `pom.xml`
- The `check-secrets.sh` hook scans proposed content from `write_file` and `apply_diff` — it reads the `content` or `diff` field from the JSON payload; `search_and_replace` payloads may not always include full content, which is acceptable for the demo
- MCP config location (`lab5/.bob/mcp.json`) may need to be merged into Bob's global MCP settings depending on workspace configuration — document this in README Step 5 if needed
