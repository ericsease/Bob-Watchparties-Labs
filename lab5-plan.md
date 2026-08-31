# Lab 5 Plan — "Bob as Your Java Modernization Partner"

## Top-Level Overview

**Goal:** Build a 30–45 minute presenter-driven lab that pitches Bob to a mixed-skill enterprise audience (SAP developers, Java/Python/full-stack). The lab uses a legacy Java 8 Spring Boot microservice as its starting point and has Bob drive a realistic modernization story across the full SDLC — from assessment through containerization, CI/CD, security hooks, and shipping.

**Narrative:** A fictional legacy `inventory-service` (Java 8, Spring Boot 2.x, no tests, no CI) needs to be brought into the modern world. Bob acts as a senior engineering partner who reads the codebase, produces an assessment, migrates Java idioms to Java 17+, adds tests, wires up a GitHub Actions pipeline, enforces quality via hooks, and ships via PR workflow — all while letting the audience see subagents, a custom mode, a general-purpose MCP, and a skill in action.

**Scope:**
- New `lab5/` directory in the repo (parallel to lab4/)
- A real, runnable Java 8 Spring Boot starting-point app (`lab5/service/`) — starts with `mvn spring-boot:run`, serves JSON on port 8080
- A lightweight Python terminal dashboard (`lab5/dashboard/watch.py`) — live view of inventory API for visual demo impact
- Bob configuration files under `lab5/.bob/`: `settings.json` (hooks), `custom_modes.yaml`, skill, MCP config
- GitHub Actions CI workflow scoped to `lab5/`
- A structured, presenter-focused `lab5/README.md` matching lab4's format — single source of truth
- A separate `lab5-implementation.md` (Agent-mode task list) for building the lab

**Non-goals:**
- Full production-grade Spring Boot (keep it followable on screen)
- Deep Spring Boot or Maven training — Bob is the protagonist, not Spring
- Complex frontend (dashboard is a demo prop, not a feature)

---

## Sub-Task 1 — Create the legacy Java service starting point

**Status:** [ ] pending

**Intent:**
Give participants a realistic but deliberately flawed legacy Java 8 Spring Boot service that *actually runs* so the presenter can show a live terminal and browser hit. The service uses Java 8 idioms (verbose POJOs, raw types, `java.util.Date`, old-style loops), has hardcoded secrets, and is missing tests, CI, and a Dockerfile. This is the "before" state Bob inherits.

**Expected Outcomes:**
- `lab5/service/` is a valid Maven project targeting Java 8 source compatibility, runnable with `mvn spring-boot:run`
- On startup, prints a banner and listens on port 8080
- Seed data: 5 hardcoded inventory items loaded on boot (so `curl localhost:8080/api/inventory` returns real JSON immediately)
- `InventoryController.java` — `GET /api/inventory`, `POST /api/inventory`, `DELETE /api/inventory/{id}`
- `InventoryService.java` — in-memory `ArrayList`, verbose Java 7-style loops, no streams
- `InventoryItem.java` — plain POJO with full getters/setters/toString boilerplate (no records)
- `application.properties` — hardcoded `spring.datasource.password=admin123` (hook trigger)
- No tests, no Dockerfile, no CI — intentionally absent
- `README-legacy.md` inside `lab5/service/` — describes the service for Bob to read during assessment

**Todo List:**
1. Create `lab5/service/pom.xml` — Java 8 source/target, Spring Boot 2.7.18, spring-boot-starter-web, spring-boot-starter-data-jpa, H2 in-memory DB
2. Create `InventoryItem.java` — plain POJO: `id` (Long), `name` (String), `quantity` (int), `price` (double), `lastUpdated` (java.util.Date); full boilerplate getters/setters/toString/equals/hashCode
3. Create `InventoryController.java` — REST controller; uses old-style `for` loops, raw `ArrayList` casts, `new Date()` calls
4. Create `InventoryService.java` — manages items in an `ArrayList<InventoryItem>`; seed 5 items in constructor; verbose non-stream iteration
5. Create `InventoryApplication.java` — `@SpringBootApplication` main class
6. Create `application.properties` — `server.port=8080`, `spring.datasource.password=admin123`, `spring.h2.console.enabled=true`
7. Create `README-legacy.md` — describes the inventory service domain and endpoints

**Relevant Context:**
- Must compile and run with `mvn spring-boot:run` — presenter shows live terminal output and browser
- Use Spring Boot 2.7.18 (last 2.x release — still widely installed in enterprise)
- Hardcoded password in application.properties is the deliberate flaw the hook catches
- Keep Java intentionally verbose so Bob's Java 17 modernization changes are visually dramatic

---

## Sub-Task 1b — Create the live dashboard (demo aid)

**Status:** [ ] pending

**Intent:**
Add a minimal read-only dashboard so the presenter always has something live and visual to show — either a tiny Python script or a single-page React app that polls `GET /api/inventory` and renders the items. This gives the demo the same "something running in the browser" energy as lab4's RepoRadar, without distracting from the Java modernization story.

**Expected Outcomes:**
- `lab5/dashboard/` contains either:
  - Option A (preferred): a single `watch.py` Python script — polls the inventory API every 2 seconds and prints a formatted table to the terminal using `rich` or plain print; requires only `pip install requests rich`
  - Option B (fallback): a minimal Vite + React single-page app (similar to lab4 pattern) that GETs `/api/inventory` and renders a simple table
- `README` setup section documents how to start the dashboard alongside the Java service
- Dashboard is clearly labeled as a "demo aid" — not the subject of modernization

**Todo List:**
1. Decide on dashboard type — **Option A (Python watch script)** is preferred: lower setup friction, reads well in terminal, no Node dependency conflict with dashboard vs service
2. Create `lab5/dashboard/watch.py` — polls `http://localhost:8080/api/inventory`, prints a formatted table every 2 seconds using `rich` (or plain tabular print if rich unavailable)
3. Create `lab5/dashboard/requirements.txt` — `requests`, `rich`
4. Add a one-line startup instruction to the README: `pip install -r dashboard/requirements.txt && python dashboard/watch.py`
5. (Optional) If the audience wants a browser view: create a minimal `index.html` with vanilla JS `fetch` + `setInterval` — no build step needed

**Relevant Context:**
- Lab4 uses React + Vite for a browser UI; lab5 can use a terminal dashboard to feel more "backend/DevOps" which resonates with SAP developers
- The dashboard also makes the "before vs after" migration visible: same JSON, cleaner code
- Keep this sub-task small — the dashboard is a prop, not a feature

---

## Sub-Task 2 — Create the Bob custom mode: "Java Architect"

**Status:** [ ] pending

**Intent:**
Create a `custom_modes.yaml` file in `lab5/.bob/` that defines a "Java Architect" mode. This mode primes Bob with Java 17+ best practices, forbids deprecated patterns, and instructs Bob to always reason about migration impact before making changes. This is a key demo moment — the presenter switches into this mode and the audience sees Bob's persona change instantly.

**Expected Outcomes:**
- `lab5/.bob/custom_modes.yaml` exists with a `java-architect` mode entry
- The mode's `roleDefinition` instructs Bob to: prefer Java records over POJOs, use `var` for local inference, use `LocalDateTime` over `Date`, prefer streams/lambdas over loops, flag deprecated Spring Boot 2.x patterns, always propose a migration plan before editing
- The mode has a `customInstructions` block reinforcing: "never introduce breaking API changes without flagging them"
- Mode is named something presenter-friendly: "☕ Java Architect"

**Todo List:**
1. Create `lab5/.bob/` directory
2. Write `lab5/.bob/custom_modes.yaml` with a single `java-architect` mode entry
3. Set `roleDefinition` to a 3–4 sentence Java 17+ senior architect persona
4. Set `customInstructions` with 5–6 specific Java modernization rules (prefer records, use `var`, use `LocalDateTime`, prefer streams, flag deprecated Spring 2.x APIs, propose plan before editing)
5. Add `groups: ["read", "edit", "command"]` permission set

**Relevant Context:**
- Custom modes live in `.bob/custom_modes.yaml` relative to workspace
- Lab4 has no custom modes — this is net new to the lab series
- The presenter will demo switching modes mid-conversation as a "persona switch" moment
- Keep the YAML clean and well-commented so it reads well on screen during the demo

---

## Sub-Task 3 — Create the Bob hooks configuration

**Status:** [ ] pending

**Intent:**
Define Bob hooks in `lab5/.bob/hooks.yaml` that fire before Bob commits any change. Two hooks: (1) a pre-edit hook that scans for hardcoded secrets in files Bob is about to modify, and (2) a pre-command hook that blocks `git push` unless tests pass. This demonstrates Bob's new safety-net capability and is a natural payoff after the audience sees the hardcoded password in `application.properties`.

**Expected Outcomes:**
- `lab5/.bob/hooks.yaml` (or equivalent Bob hooks config format) is created
- Hook 1: `pre-edit` — runs a grep-style check for patterns like `password=`, `secret=`, `apikey=` in the target file; surfaces a warning to the presenter if found
- Hook 2: `pre-command` — intercepts `git push` and requires confirmation that tests have passed
- Both hooks have human-readable `description` fields that will display in the Bob UI
- README documents the hooks so the presenter can narrate what's happening

**Todo List:**
1. Research the exact Bob hooks config schema (check `.bob/` docs or bob-differentiators.md in the repo)
2. Create `lab5/.bob/hooks.yaml` with the two hooks above
3. Write descriptive `name` and `description` fields for each hook (these appear in the UI)
4. Add a `hooks-explainer.md` inside `lab5/.bob/` explaining what each hook does for the presenter
5. Reference the hooks in the lab README with a dedicated Act section

**Relevant Context:**
- Hooks is described as a "new Bob feature" — confirm exact config format from Bob docs/differentiators
- `bob-differentiators.md` at repo root may contain hooks documentation
- The secret-scanning hook creates a natural narrative bridge from "look at this bad code" to "Bob catches it automatically"

---

## Sub-Task 4 — Create the general-purpose MCP configuration

**Status:** [ ] pending

**Intent:**
Configure a general-purpose MCP server that feels enterprise-useful beyond GitHub. Best candidate: the **filesystem MCP** (reads local files/docs) or a **fetch/web MCP** (queries public APIs or documentation). For the Java story, configuring a MCP that lets Bob query the Spring Boot migration guide or Java release notes in real time is compelling. This shows Bob extending its own knowledge via MCP during the assessment act.

**Expected Outcomes:**
- `lab5/.bob/mcp.json` (or `mcp_settings.json`) configures one MCP server
- Chosen MCP: **fetch MCP** (`@modelcontextprotocol/server-fetch`) — allows Bob to fetch any public URL; presenter uses it to have Bob pull the Spring Boot 3.x migration guide live during the assessment
- Config includes the server name, command, and a human-readable description
- README documents which MCP is used, why, and how to install it (`npx` or `uvx`)
- Lab Act demonstrates Bob calling the MCP to read migration docs and then citing specific guidance in its plan

**Todo List:**
1. Decide on MCP server: `@modelcontextprotocol/server-fetch` (fetch any URL) — no API key needed, universally useful
2. Create `lab5/.bob/mcp.json` with the fetch server config (transport: stdio, command: npx)
3. Document the exact `npx` install command in the README prerequisites section
4. Write the demo prompt: "Use the fetch tool to read https://spring.io/blog/2022/05/24/spring-boot-3-0-m3-available-now and summarize the breaking changes relevant to our service"
5. Add a callout in the README: "💡 This is a general-purpose MCP — not GitHub-specific. Bob can query any public documentation source."

**Relevant Context:**
- MCP-Workaround/ directory in the repo suggests MCP setup has friction — document clearly and provide exact `npx` install command
- The fetch MCP requires Node.js (already a prereq from lab4)
- Keep the MCP demo to 2–3 minutes; it's a supporting feature not the headline act
- Alternative if fetch MCP doesn't resonate: filesystem MCP reading a local `api-docs/` folder of markdown files
- MCP config lives in `.bob/mcp.json` or Bob's global MCP settings — confirm location in implementation

---

## Sub-Task 5 — Create the `java-modernization` skill

**Status:** [ ] pending

**Intent:**
Write a `SKILL.md` for a `java-modernization` skill that Bob can activate. The skill encodes the migration playbook: which Java 8 patterns map to which Java 17+ equivalents, how to handle Spring Boot 2→3 breaking changes, and how to structure a migration PR. The presenter activates this skill explicitly in Act 1 so the audience can see Bob loading specialized knowledge.

**Expected Outcomes:**
- `lab5/.bob/skills/java-modernization/SKILL.md` exists
- Skill covers: Java records (replace POJOs), `var` keyword, `LocalDateTime` (replace `Date`), text blocks, switch expressions, sealed classes (brief mention), Spring Boot 3.x migration checklist
- Skill includes a section: "Migration PR structure" — what to include in the PR description for a Java migration
- Skill has a trigger description that matches phrases like "modernize", "migrate Java", "upgrade to Java 17"
- Skill is short (60–80 lines) — punchy reference, not an essay

**Todo List:**
1. Create `lab5/.bob/skills/java-modernization/` directory
2. Write `SKILL.md` with frontmatter (name, description, trigger phrases)
3. Add Java 8 → 17 pattern mapping table (5–6 key patterns)
4. Add Spring Boot 2 → 3 checklist (5 items: javax→jakarta, Spring Security config, etc.)
5. Add "Migration PR structure" section
6. Keep total file under 80 lines

**Relevant Context:**
- Skill format: SKILL.md with frontmatter + markdown content
- Skills are activated with `use_skill` — the presenter will type "modernize this service" to trigger it
- The skill bridges Act 1 (assessment) to Act 2 (implementation) by giving Bob a concrete playbook

---

## Sub-Task 6 — Create the GitHub Actions CI pipeline and Dockerfile

**Status:** [ ] pending

**Intent:**
Add a `.github/workflows/ci.yml` inside `lab5/` that runs on pull requests. The pipeline: checks out code, sets up Java 17, runs Maven tests, builds a Docker image, and (optionally) runs a trivial secret-scan step. Bob generates this file during Act 3 of the lab — the audience watches Bob write a complete CI pipeline from a single prompt.

**Expected Outcomes:**
- `lab5/.github/workflows/ci.yml` exists (scoped to lab5, not repo root)
- Pipeline triggers on `push` and `pull_request` to `main`
- Jobs: `build-and-test` (Java 17, Maven, `mvn test`), `docker-build` (builds `Dockerfile`)
- `Dockerfile` exists at `lab5/service/Dockerfile` (multi-stage: build with Maven, run with JRE 17-slim)
- Pipeline has clear job names and step names that read well on screen
- README includes the exact Bob prompt that generates this pipeline

**Todo List:**
1. Create `lab5/service/Dockerfile` — multi-stage build (maven:3.9-eclipse-temurin-17 → eclipse-temurin:17-jre-alpine)
2. Create `lab5/.github/workflows/` directory structure
3. Write `ci.yml` with `on: [push, pull_request]` trigger, Java 17 setup, `mvn -B test`, and docker build step
4. Add a `secret-scan` step using `grep -r "password=" --include="*.properties"` as a simple shell check
5. Ensure the workflow file is well-commented (comments show on screen during demo)
6. Document in the README: "Act 3 — Bob adds CI" with the exact prompt the presenter uses

**Relevant Context:**
- GitHub Actions is already known by SAP developers — this will land immediately
- The `secret-scan` step in CI creates a narrative echo of the Bob hook (two layers of protection — "Bob catches it locally, CI catches it in the pipeline")
- Multi-stage Dockerfile is a Java best practice; showing it teaches something real
- The presenter runs `git diff` after Bob creates this file to show the diff before committing
- Scope the workflow trigger to `paths: ['lab5/**']` so it doesn't fire on unrelated lab changes

---

## Sub-Task 7 — Create the subagent personas

**Status:** [ ] pending

**Intent:**
Write two subagent persona definitions that the main Java Architect agent spawns during the lab. Persona 1: "Security Auditor" — scans for hardcoded secrets, insecure configs, and missing input validation. Persona 2: "Test Engineer" — writes JUnit 5 tests for the modernized service. These personas are referenced in the README as explicit demo prompts so the presenter can trigger them on cue.

**Expected Outcomes:**
- `lab5/.bob/personas/security-auditor.md` — persona definition for the security subagent
- `lab5/.bob/personas/test-engineer.md` — persona definition for the test-writing subagent
- Each persona file has: role description, specific responsibilities, output format expectations
- README Act 2 includes: "Bob spawns two subagents simultaneously — watch both workstreams appear"
- The security auditor's output feeds the hooks discussion (natural narrative bridge)

**Todo List:**
1. Create `lab5/.bob/personas/` directory
2. Write `security-auditor.md` — role: "You are a security-focused code reviewer specializing in Java/Spring Boot. Scan for hardcoded credentials, missing input validation, insecure defaults, and unprotected endpoints."
3. Write `test-engineer.md` — role: "You are a test engineer specializing in JUnit 5 and Spring Boot test slices. Write comprehensive unit tests for service classes and integration tests for controllers."
4. Reference both personas in the README with the exact subagent spawn prompts
5. Add a presenter note: "This mirrors how a real team works — security and testing in parallel with development"

**Relevant Context:**
- Lab4 demonstrates subagents for test writing; lab5 elevates this with named personas and a security angle
- Persona files are referenced in prompts, not auto-loaded — they are part of the conversation script
- The parallel subagent moment is one of the strongest audience demo moments; give it its own act beat

---

## Sub-Task 8 — Write the lab5 README (presenter guide) and lab5-implementation.md

**Status:** [ ] pending

**Intent:**
Write the full presenter-focused README following lab4's exact format conventions: emoji section headers, time markers, presenter notes in blockquotes, "what to look for" callouts, success checks, and a troubleshooting table. This is the most important deliverable — the README is what the presenter holds during the demo.

**Expected Outcomes:**
- `lab5/README.md` is 300–400 lines, matching lab4's structure and tone
- Sections: What You'll Learn, Lab Structure (timeline), Setup, Act 1–5, Success Criteria, Troubleshooting, Tips for Presenters, Next Steps
- Every Act has: presenter note, exact prompt to copy-paste, "what to look for" callout, success check
- Act breakdown:
  - Act 1 [0:00–0:07]: Setup — start service (`mvn spring-boot:run`) + dashboard (`python watch.py`) → both running live; switch to Java Architect mode; activate skill
  - Act 2 [0:07–0:17]: Bob assesses legacy code; parallel modernization (Java 17 idioms); dual subagent spawn (Security Auditor + Test Engineer run concurrently)
  - Act 3 [0:17–0:25]: Hooks demo — Bob tries to write `application.properties` → hook fires; GitHub Actions CI pipeline generated; Dockerfile added
  - Act 4 [0:25–0:32]: MCP demo — Bob fetches live Spring migration guide; PR workflow generates description
  - Act 5 [0:32–0:38]: Audience Q&A — 3 pre-scripted "audience questions" the presenter can trigger to show Bob's breadth
- Prerequisites section lists: Java 17 JDK, Maven 3.9, Node.js 18+, Bob IDE, Git, Docker (optional)
- Troubleshooting table covers: Java version mismatch, Maven not found, MCP install issues, hooks not firing

**Todo List:**
1. Write header section (duration 35–45 min, difficulty: intermediate, SAP developer focus note)
2. Write "What You'll Learn" (7 items: custom modes, hooks, subagent personas, MCP, CI pipeline, full SDLC, Java modernization)
3. Write "Lab Structure" timeline table with all 5 acts
4. Write Setup section — start Java service, start dashboard, open Bob, switch mode, install MCP (with exact commands)
5. Write Act 1 through Act 5 with all presenter notes, exact copy-paste prompts, "what to look for" callouts, and success checks
6. Write Success Criteria checklist (8–10 items)
7. Write Troubleshooting table (6 rows: Java version, Maven not found, port 8080 in use, MCP install, hook not firing, Python dashboard errors)
8. Write "Tips for Presenters" with 5 tips specific to SAP audience (mention SAP ABAP-to-Java parallels, BTP, S/4HANA modernization)
9. Write "Next Steps" pointing to bob-differentiators.md and the broader lab series
10. Write `lab5-implementation.md` — the plan-to-build document for Agent mode; mirrors this file's sub-task structure but is self-contained

**Relevant Context:**
- `lab4/README.md` is the direct template — match its format exactly
- Presenter notes use: `> 🎤 **Presenter note:**`
- Callouts use: `> 👤 **What to look for:**`
- Success checks use: `> ✅ **You should see:**`
- Time markers in headers: `[0:07 – 0:17]`
- The README is the *single source of truth* for the lab — not a supplementary guide
- `lab5-plan.md` (this file) is for planning only; `lab5-implementation.md` will be the Agent-mode task list

---

## Feature Coverage Matrix

| Feature | Where Demonstrated | Act |
|---|---|---|
| Custom mode (Java Architect) | Switch mode before first prompt | Act 1 |
| Skill activation (java-modernization) | `use_skill` call in Plan mode | Act 1 |
| Parallel tool calls | Bob reads 5 files simultaneously | Act 1 |
| Subagent persona — Security Auditor | Spawned after assessment | Act 2 |
| Subagent persona — Test Engineer | Spawned in parallel with migration | Act 2 |
| Java 17 modernization | Records, var, streams, LocalDateTime | Act 2 |
| Hooks (secret scan + test gate) | Triggered when editing application.properties | Act 3 |
| GitHub Actions CI pipeline | Bob generates ci.yml from one prompt | Act 3 |
| Dockerfile (multi-stage) | Bob adds containerization | Act 3 |
| MCP — fetch Spring docs | Bob queries live migration guide | Act 4 |
| PR workflow | Bob generates PR description + submits | Act 4 |
| Freestyle / Q&A | Open-ended audience prompts | Act 5 |
