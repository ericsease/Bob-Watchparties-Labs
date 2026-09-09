# Lab 5 — Bob as Your Java Modernization Partner

**Duration:** 45–55 minutes | **Difficulty:** Intermediate | **Audience:** Enterprise Java developers

> 🎯 **Presenter context:** This lab is aimed at developers who work with legacy Java services
> and want to see Bob as a *senior engineering partner* across the **full SDLC**, not just a
> code autocomplete tool. Every act demonstrates a capability that enterprise Java teams wish
> they had last week.

---

## 🎯 What You'll Learn

1. **Plan mode first** — use Bob's standard Plan mode to orient before activating any specialist tooling
2. **Custom modes** — switch Bob's persona to a "Java Architect" who enforces Java 17+ best practices and see the difference it makes
3. **Skills** — walk through a `java-modernization` playbook and watch Bob apply its rules automatically
4. **Parallel subagents** — spawn a Security Auditor and a Test Engineer running simultaneously
5. **Security hardening** — Bob reads the audit findings and remediates a hardcoded credential + adds Spring Security in one pass
6. **GitHub Actions CI** — Bob generates a complete pipeline from a single prompt
7. **General-purpose MCP** — Bob fetches live Spring Boot migration docs from the web
8. **Full SDLC** — assessment → migration → verify → CI/CD → containerization → PR in one session

---

## 🗺️ Lab Structure

| Act | Time | Focus | Key Bob Feature |
|-----|------|-------|-----------------|
| Setup | 0:00 – 0:07 | Start services, configure Bob | Mode switching, skill setup |
| Act 1 | 0:07 – 0:17 | Plan mode orient → expert mode assess | Before/after custom mode contrast |
| Act 2 | 0:17 – 0:28 | Modernize Java 8 → 17 + verify | Parallel subagents, test loop |
| Act 3 | 0:28 – 0:37 | Security hardening + CI pipeline | Credential remediation, GitHub Actions generation |
| Act 4 | 0:37 – 0:44 | MCP + ship via PR | Fetch MCP, PR workflow |
| Act 5 | 0:44 – 0:50 | Freestyle / audience Q&A | Open demo |

---

## 🛠️ Setup

### Prerequisites

- **Java 17 JDK** — `java -version` should show 17+
- **Maven 3.9+** — `mvn -version`
- **Python 3.8+** — `python3 --version`
- **Node.js 18+** — `node --version` (for MCP fetch server)
- **Bob IDE** — v2.x or later
- **Git** — configured with your credentials
- **Docker** *(optional)* — for the Dockerfile demo in Act 3

### Step 1 — Start the Java service

Open a terminal and run:

```bash
cd lab5/service
mvn spring-boot:run
```

Wait for the banner:
```
===========================================
  Inventory Service (Legacy Java 8 build)
  http://localhost:8080/api/inventory
===========================================
```

> ✅ **Verify:** `curl http://localhost:8080/api/inventory` returns a JSON array of 5 items.

### Step 2 — Start the live dashboard

Open a **second terminal**:

```bash
cd lab5/dashboard
pip install -r requirements.txt
python watch.py
```

> ✅ **You should see:** A live table refreshing every 2 seconds showing all 5 inventory items.
> Leave this terminal visible throughout the demo — it's your "live system" prop.

### Step 3 — Make hook scripts executable

```bash
chmod +x lab5/.bob/hooks/*.sh
```

### Step 4 — Open Bob in Plan mode *(do NOT switch to Java Architect yet)*

1. Open the `lab5/` directory (or **repo root**) in Bob
2. Make sure you are in **Plan** mode — the contrast with Java Architect mode in Act 1 is the point
3. Confirm the mode badge shows Plan

> ⚠️ **Workspace root matters:** Bob resolves `.bob/` relative to the workspace root.
> Open `lab5/` or the repo root — **not** a subdirectory like `lab5/service/`.
> If the **☕ Java Architect** mode doesn't appear in the mode selector, this is the reason.

> 🎤 **Presenter note:** *"We're starting in plain Plan mode — no custom persona, no specialist
> skill loaded. I want to show you what Bob gives you out of the box, and then what changes
> when we give it the right context."*

> 🎤 **Presenter note — show the Settings UI:** Open **Settings → Modes** to show the Java
> Architect entry to the audience. Then open **Settings → Extensions** (or MCP panel) to show
> the fetch server registered. This is a good 30-second orientation before the first prompt.

> ⚠️ **Auto-approve required for subagents:** The subagent steps (Steps 9 and 11) require
> auto-approval to run without interruption. Enable it now in **Settings → Auto-approve** before
> the demo starts. Without it, Bob will pause and ask permission at each subagent spawn —
> which breaks the "three workstreams in parallel" moment.

### Step 5 — Install and enable the fetch MCP

In Bob's MCP settings, add the fetch server from `lab5/.bob/mcp.json`:

```bash
# Verify Node.js can resolve the package
npx -y mcp-fetch-server --help
```

> 🎤 **Presenter note — show the MCP panel:** *"Before I type anything, let me show you what's
> configured. Open Settings → MCP — you'll see a 'fetch' server registered. This is a
> general-purpose tool, not tied to any specific platform. It lets Bob fetch any public URL.
> In Act 4, we'll use it to pull the live Spring Boot migration guide directly into context."*

---

## 🔍 Act 1 — Orient & Assess [0:07 – 0:17]

> 🎤 **Presenter note:** *"The legacy service is running — the dashboard is showing live data.
> I'm going to ask Bob to tell me what's wrong with this codebase. But first, I'm going to do
> it in plain Plan mode — no specialist context. Then I'll activate the Java Architect mode and
> the java-modernization skill, and we'll see exactly what changes."*

### Step 6 — First pass: plain Plan mode assessment

In **Plan mode**, type:

```
Read the inventory service source files in lab5/service/src/main/java/com/example/inventory/
and lab5/service/src/main/resources/application.properties.
Tell me what you'd want to improve in this codebase.
```

> 👤 **What to look for:**
> - Bob reads the files and gives a reasonable but generic response
> - It may mention Java version, tests, or hardcoded values — but without a structured
>   severity model or specific migration patterns
> - The output reads like a knowledgeable generalist, not a specialist

> 🎤 **Presenter note:** *"That's a solid response. But notice it's general advice —
> 'consider adding tests', 'update the Java version'. It doesn't have a framework for
> Java 8 → 17 migration specifically. Let me change that."*

---

### Step 7 — Switch to Java Architect mode and open the skill

1. Click the mode selector and choose **☕ Java Architect**
2. Open `.bob/skills/java-modernization/SKILL.md` in the editor and spend 60 seconds reading it aloud with the audience

> 🎤 **Presenter note:** *"This is the skill file. It's a markdown document — not code.
> It defines seven rules: records over POJOs, LocalDateTime over Date, streams over loops,
> and so on. When I activate this skill, Bob loads these rules into its context before
> touching a single file. Watch what the same question produces now."*

### Step 8 — Second pass: expert mode + skill assessment

In the Bob chat, type:

```
use the java-modernization skill and then assess the inventory service.
Read all source files in lab5/service/src/main/java/com/example/inventory/
and lab5/service/src/main/resources/application.properties.
Produce a prioritised modernization plan covering: language idioms,
security issues, missing infrastructure, and testability gaps.
```

> 👤 **What to look for:**
> - Bob reads **all 5 files simultaneously** (parallel tool calls) — not one at a time
> - The output is now a structured plan with CRITICAL / HIGH / MEDIUM severity categories
> - Bob specifically calls out `InventoryItem` as a record candidate, `java.util.Date` → `LocalDateTime`, for-loops → streams
> - Bob calls out the hardcoded `spring.datasource.password=admin123` as a CRITICAL security finding
> - Missing tests, Dockerfile, and CI are listed as infrastructure gaps

> 🎤 **Presenter note:** *"Same question, different answer. The custom mode gave Bob a frame —
> 'you are a Java architect, here are the rules you enforce'. The skill gave it the specific
> pattern map. Now it reads five files in parallel and produces a severity-ranked plan.
> That's the difference between a generalist and a specialist."*

> ✅ **Success check:** Bob's plan includes at minimum:
> - Migration of `InventoryItem` to a record
> - Replace `java.util.Date` with `LocalDateTime`
> - Replace for-loops with streams
> - Flag hardcoded password as CRITICAL
> - Missing tests, Dockerfile, CI as infrastructure gaps

---

## ⚡ Act 2 — Modernize + Verify [0:17 – 0:28]

> 🎤 **Presenter note:** *"We have the plan. Now I'm going to use subagents for the security
> audit and the tests. A subagent is Bob delegating a self-contained task to an isolated
> context — it keeps the work out of our main conversation so it doesn't pollute the context
> window, and it comes back with just the summary we need. Think of it as handing a task to
> a specialist so the main conversation stays focused."*

> ⚠️ **Important:** A subagent completes its task and returns — it is **not** a background
> process you can interrupt. Do **not** type a new prompt while the subagent is running or
> it will be cancelled. Wait for Bob to return control before continuing.

### Step 9 — Spawn the Security Auditor subagent

```
Spawn a subagent for the security audit. The subagent should:
- Read lab5/.bob/personas/security-auditor.md and adopt that persona
- Perform a full security audit of the inventory service source files
- Produce a structured findings report as its output

Do not do this work yourself — delegate it to a subagent to keep the audit
out of our main conversation context.
```

> 👀 **Watch for:** Bob using the `spawn_subagent` tool. The subagent runs, completes,
> and Bob returns a summary to the main conversation.
> If Bob does the audit inline instead of spawning, redirect:
> *"Please delegate that to a subagent — I want to keep this context clean."*

### Step 10 — Modernize the service files

```
Now modernize the inventory service in this conversation:

1. Convert InventoryItem.java to a Java record — replace all boilerplate with a single record declaration. Use LocalDateTime instead of Date.
2. Refactor InventoryService.java — replace all for-loops with Stream API. Replace new Date() with LocalDateTime.now().
3. Update InventoryController.java — remove raw HashMap error responses, use a proper Map<String, String> with var for local inference.

Apply changes in parallel where files are independent.
```

> 👤 **What to look for:**
> - Bob edits multiple files in parallel — watch the tool calls fire simultaneously
> - Java goes from 80-line POJO to a 3-line record — point this out explicitly

> 🎤 **Presenter note:** *"Look at InventoryItem.java. It went from 96 lines of boilerplate
> to 3 lines — a Java record. Same data, zero noise. Now imagine doing this across hundreds
> of classes in a large legacy service. Bob can batch this."*

### Step 11 — Spawn the Test Engineer subagent

```
Spawn a subagent to write the test suite. The subagent should:
- Read lab5/.bob/personas/test-engineer.md and adopt that persona
- Write JUnit 5 unit tests for InventoryService
- Write @WebMvcTest controller tests for InventoryController
- Place tests in lab5/service/src/test/java/com/example/inventory/

Do not write the tests yourself — delegate to a subagent to keep test generation
out of the main conversation context.
```

> 👀 **Watch for:** Bob using `spawn_subagent` again. The subagent runs, writes the files,
> and returns a summary. Bob then resumes in this conversation.
> If Bob starts writing tests inline, redirect: *"Please spawn a subagent for that."*

> 🎤 **Presenter note:** *"Two subagents used so far — one for the audit, one for the tests.
> Each ran in its own isolated context so the findings and the test boilerplate didn't
> pollute our migration conversation. That's the point: clean context, specialist output,
> summary returned here."*

### Step 12 — Run the tests and verify

Once the Test Engineer subagent has finished, type:

```
Run the tests that were just written. From lab5/service, run mvn test and report the results.
```

> 👤 **What to look for:**
> - Bob runs `mvn test` in the terminal
> - Tests pass (or Bob identifies and fixes any failures from the migration)
> - The "did it actually work?" question is answered live

> 🎤 **Presenter note:** *"This closes the loop. Bob didn't just migrate the code — we verified
> it. The tests the subagent wrote are passing against the modernized implementation. That's
> the full dev cycle: write, test, confirm."*

### Step 12b — Bob Findings *(mention only, no prompt needed)*

> 🎤 **Presenter note:** *"While all this has been happening, Bob Findings has been running
> in the background automatically — no trigger needed. It's a continuous static analysis
> engine that scans every open file for code quality issues: cyclomatic complexity,
> maintainability index, overly long functions. When something crosses a threshold it
> appears in the Bob Findings panel with a purple underline in the editor.*
>
> *You might notice it's not surfacing anything on this codebase right now — and that's
> actually the point. Bob wrote clean, well-structured code. The legacy source is simple
> enough that none of the quality thresholds are tripped. Bob Findings would light up if
> you had deeply nested conditionals or 200-line functions — the kind of thing that arrives
> in a real migration from a large legacy codebase."*

> 👤 **What to show:** Open the **Bob Findings panel** in the sidebar and point it out.
> Show the empty or clean state as a positive signal, not a gap. Mention that on a real
> enterprise codebase with complex business logic, this panel would surface actionable issues automatically.

---

## 🔒 Act 3 — Security Hardening + CI Pipeline [0:28 – 0:37]

> 🎤 **Presenter note:** *"The security audit flagged two things: a missing authentication
> layer and a hardcoded credential. Let's fix both, then build a CI pipeline that enforces
> the same checks on every future commit."*

### Step 13 — Fix the hardcoded credential and add Spring Security

```
The security audit flagged two issues in application.properties and the POM:

1. application.properties has a hardcoded password (spring.datasource.password=admin123).
   Externalize it to an environment variable reference: ${DB_PASSWORD:changeme}

2. The POM is missing Spring Security. Add spring-boot-starter-security and
   update the parent version to 3.2.0 and java.version to 17.
```

> 🎤 **Presenter note:** *"Bob is going to fix the credential leak and upgrade Spring Boot
> in one pass. Watch the tool calls — it reads both files, plans the changes, then writes them.
> This is the same pattern as Act 2 but now it's security-driven remediation."*

> 👤 **What to look for:**
> - Bob reads `application.properties` and `pom.xml` in parallel
> - Replaces the hardcoded `admin123` with `${DB_PASSWORD:changeme}` — externalised, safe to commit
> - Updates `pom.xml` with Spring Boot 3.2.0, Java 17, and `spring-boot-starter-security`
> - Uses its todo list to track both changes without losing either one

### Step 14 — Configure Spring Security and restore the dashboard

Adding Spring Security to the POM locked down all endpoints by default — including the GET route the Python dashboard uses. Add a `SecurityFilterChain` to allow public read access while keeping mutations authenticated:

```
Spring Security is now on the classpath but has no configuration, so it locks
down all endpoints including GET /api/inventory — which breaks the dashboard.

Add a SecurityConfig class that:
- Permits GET /api/inventory and GET /api/inventory/** without authentication
- Requires authentication for all other requests
- Disables CSRF (stateless API)
- Keeps HTTP Basic enabled for authenticated endpoints
```

> 👤 **What to look for:** Bob writes `SecurityConfig.java` in the inventory package.
> The dashboard terminal should recover and show live data again once the service restarts.

> 🎤 **Presenter note:** *"Adding Spring Security without a configuration locks everything down
> by default — which broke our read-only dashboard. This is the realistic next step after adding
> the dependency: configuring the security posture intentionally. Public GET access for the
> read API, authentication required for mutations. That's a sensible production default."*

Then restart the service and verify:

```
Run mvn spring-boot:run from lab5/service and confirm the service starts cleanly.
Check that curl http://localhost:8080/api/inventory returns data without credentials.
```

> ✅ **You should see:** Service starts, dashboard recovers and shows live inventory data again.

### Step 15 — Bob generates the GitHub Actions CI pipeline

```
Add a GitHub Actions CI pipeline for the inventory service.
Requirements:
- Trigger on push and pull_request to main, scoped to lab5/service/** changes
- Job 1: Build and test with Java 17 and Maven
- Job 2: Scan for hardcoded secrets in .properties and .yaml files
- Job 3: Build the Docker image (multi-stage, Java 17 JRE Alpine target)
Place the workflow at lab5/.github/workflows/ci.yml
```

> 👤 **What to look for:** Bob generates a complete, well-structured YAML workflow.
> Point out the three jobs — build, scan, docker — and note that Job 2 enforces the same
> credential check we just fixed manually: now it's automatic on every PR.

> 🎤 **Presenter note:** *"Notice Job 2 — the secret scan in CI. It catches the same pattern
> we just fixed: hardcoded `password=` in config files. We fixed it manually this session;
> the pipeline ensures no future commit sneaks one back in. Two layers — developer remediation
> now, automated gate forever."*

### Step 16 — Verify the Dockerfile

```
Show me the Dockerfile for the inventory service and explain the multi-stage build.
```

> 👤 **What to look for:** Bob reads `lab5/service/Dockerfile` and explains: build stage
> uses Maven + JDK 17, runtime stage uses JRE Alpine (smaller image), non-root user for security.

---

## 🌐 Act 4 — MCP + Ship [0:37 – 0:44]

> 🎤 **Presenter note:** *"One more thing before we ship. The fetch MCP lets Bob reach out to
> any public URL. Watch it pull the official Spring Boot 3.x migration guide live and map the
> breaking changes directly to our codebase."*

### Step 17 — Use the fetch MCP to query live migration docs

```
Use the fetch tool to retrieve https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide
Summarize the breaking changes that are relevant to our inventory-service.
Which changes should we address before upgrading from Spring Boot 2.7 to 3.x?
```

> 👤 **What to look for:**
> - Bob makes a live HTTP request via the MCP
> - Bob cites specific content from the page (javax→jakarta, Spring Security changes)
> - Bob maps findings back to our specific codebase

> 🎤 **Presenter note:** *"Bob just read a live web page and applied it to our code. No
> copy-paste, no context switching. Any public documentation — framework docs, RFC specs,
> your team's internal wiki — Bob can pull and reason over it in real time."*

### Step 18 — Generate the PR description

```
Generate a pull request description for the modernization work we've done.
Include: what changed, Java 17 features used, security improvements, infrastructure added.
Format it as a GitHub PR body.
```

> 👤 **What to look for:** Bob produces a structured PR description covering all changes.
> If GitHub is configured, use the Create PR workflow. Otherwise, copy-paste the output.

> 🎤 **Presenter note:** *"From legacy Java 8 service to modernized, tested, containerized,
> and CI'd codebase — assessed, built, verified, and shipped in one Bob session."*

---

## 🎙️ Act 5 — Freestyle / Audience Q&A [0:44 – 0:50]

> 🎤 **Presenter note:** *"The floor is open. Here are three prompts I keep in my back pocket
> for when the audience asks 'but can Bob do X?' — feel free to use these or take live questions."*

### Pre-scripted audience prompts

**Prompt A — "Can Bob review code like a senior engineer?"**
```
Review InventoryController.java as a senior Java engineer.
What would you flag in a code review? Be specific and cite line numbers.
```

**Prompt B — "Can Bob explain a complex migration risk?"**
```
Explain the risk of migrating from javax.validation to jakarta.validation
in a Spring Boot 3.x upgrade. What could break at runtime, and how do we test for it?
```

**Prompt C — "Can Bob help plan a cloud deployment?"**
```
This inventory service needs to be deployed to a cloud platform.
What additional considerations should we address?
Think about: health endpoints, externalized configuration, logging standards, container sizing.
```

> 🎤 **Presenter note:** *"Notice Bob doesn't just answer the question — it reasons through
> the risk, proposes a mitigation, and offers to implement it. That's what makes it a partner,
> not just a search engine."*

---

## ✅ Success Criteria

By the end of the lab, the presenter should have demonstrated:

- [ ] Java service running live at `http://localhost:8080/api/inventory`
- [ ] Python dashboard showing live inventory data in the terminal
- [ ] Plain Plan mode assessment completed (Step 6) — shows Bob's baseline
- [ ] Bob switched to **☕ Java Architect** mode with `java-modernization` skill active
- [ ] Before/after contrast between Plan mode and Java Architect mode outputs visible
- [ ] `InventoryItem.java` modernized from 96-line POJO to a Java record
- [ ] `InventoryService.java` refactored from for-loops to Stream API
- [ ] Test suite written by subagent and verified passing with `mvn test`
- [ ] Hardcoded `admin123` credential externalized to `${DB_PASSWORD:changeme}` in `application.properties`
- [ ] Spring Boot upgraded to 3.2.0, Java 17, `spring-boot-starter-security` added to POM
- [ ] GitHub Actions `ci.yml` generated with 3 jobs (build, scan, docker)
- [ ] Fetch MCP used to retrieve live Spring Boot migration docs
- [ ] PR description generated covering all changes
- [ ] Security Auditor and Test Engineer subagents spawned in parallel

---

## 🔧 Troubleshooting

| Problem | Symptom | Fix |
|---------|---------|-----|
| Java version mismatch | `mvn spring-boot:run` fails with `source 8 not supported` | Run with `JAVA_HOME` pointing to a JDK that supports `--release 8` (JDK 17 is fine — it supports source 8) |
| Maven not found | `command not found: mvn` | Install Maven 3.9: `brew install maven` or download from maven.apache.org |
| Port 8080 in use | `Web server failed to start. Port 8080 was already in use` | `lsof -i :8080` then `kill -9 <PID>`, or add `server.port=8081` temporarily |
| MCP fetch error | Bob says "fetch tool not available" | Run `npx -y mcp-fetch-server --help` once to install, then restart Bob |
| Dashboard connection error | `⚠ Cannot reach http://localhost:8080` | Java service isn't running — go to the service terminal and run `mvn spring-boot:run` |
| Tests fail after migration | `mvn test` reports compilation errors | The record migration may have broken a constructor call — ask Bob to read the error and fix it |

---

## 🎬 Before Every Demo Session

Run this once from the repo root before the audience arrives:

```bash
sh lab5/demo-reset.sh
```

The script will:
1. Verify you are on `main` with a clean working tree
2. Restore all `lab5/service/` source files to their pristine legacy state (removes any artefacts from a previous run)
3. Cut a fresh dated branch — `demo/lab5-YYYYMMDD` — so the PR workflow has a real diff to show
4. Pre-warm the Maven dependency cache (avoids cold downloads during the demo)
5. Verify Java, Maven, Node, and Python are available
6. Print a final manual checklist

**After the script completes, finish the checklist it prints:**
- Open Bob with the repo root (or `lab5/`) as workspace
- Confirm **☕ Java Architect** appears in the mode selector
- Enable auto-approve in Bob Settings
- Open Settings → MCP and confirm the `fetch` server is registered
- Start the Java service: `cd lab5/service && mvn spring-boot:run`
- Start the dashboard: `cd lab5/dashboard && python3 watch.py`
- Verify the dashboard shows 5 items at `http://localhost:8080/api/inventory`

**After the demo:**
```bash
git checkout main
```
The demo branch (`demo/lab5-YYYYMMDD`) can be left for reference or deleted:
```bash
git branch -D demo/lab5-YYYYMMDD
```

---

## 💡 Tips for Presenters

1. **Lead with the legacy problem.** In your opening 60 seconds, ask the audience: *"How many
   of you have a Java 8 service somewhere that needs to move to 17?"* Make it personal before
   the first prompt lands.

2. **Don't skip Step 6.** The plain Plan mode assessment is the anchor for everything that follows.
   If you jump straight to Java Architect mode, the audience has no baseline to compare against.

3. **Run everything before the audience arrives.** Have both terminals open and running.
   Cold Maven downloads kill demo energy. Pre-warm: `cd lab5/service && mvn dependency:resolve`.

4. **The credential fix is a talking point.** When Bob externalizes `admin123` to an env var,
   say: *"This is what a security-aware code review looks like at AI speed. It found it,
   fixed it, and moved on — in the same pass as the Spring Boot upgrade."*

5. **The parallel subagent moment is your headline.** When Security Auditor + Test Engineer
   are both running while the main migration continues, say: *"Three engineers working
   simultaneously. How long would this take your team to do sequentially?"*

6. **Use the freestyle act for the skeptic in the room.** There's always someone who asks
   "yeah but what about X?" The pre-scripted prompts are your safety net.

---

## 🚀 Next Steps

- Explore Bob's full capability set: [`bob-differentiators.md`](../bob-differentiators.md)
- Try Lab 4 for Bob's subagent + PR workflow demo with a React/Flask full-stack app: [`lab4/README.md`](../lab4/README.md)
- Read the hooks documentation: [`Hooks.md`](../Hooks.md)
- Explore the `java-modernization` skill: [`lab5/.bob/skills/java-modernization/SKILL.md`](.bob/skills/java-modernization/SKILL.md)
- Understand the subagent personas: [`lab5/.bob/personas/`](.bob/personas/)
- **Future extension:** Add a **Secure Coder** custom mode persona that enforces OWASP patterns,
  flags injection risks, and gates any write that introduces a new HTTP endpoint without input
  validation. Could replace or complement the Security Auditor subagent as a resident mode.

---

*Last Updated: July 2025*
