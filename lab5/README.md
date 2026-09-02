# Lab 5 — Bob as Your Java Modernization Partner

**Duration:** 35–45 minutes | **Difficulty:** Intermediate | **Audience:** Enterprise Java / SAP developers

> 🎯 **Presenter context:** This lab is pitched at developers who live in enterprise Java daily —
> SAP BTP extensions, S/4HANA integrations, Spring Boot microservices. They've seen AI demos before.
> The goal is to show Bob as a *senior engineering partner* across the **full SDLC**, not just a
> code autocomplete tool. Every act demonstrates a capability SAP developers wish they had last week.

---

## 🎯 What You'll Learn

1. **Custom modes** — switch Bob's persona to a "Java Architect" who enforces Java 17+ best practices
2. **Skills** — load a `java-modernization` playbook so Bob knows migration patterns before touching code
3. **Parallel subagents** — spawn a Security Auditor and a Test Engineer running simultaneously
4. **Lifecycle hooks** — deterministic guards that block Bob from writing hardcoded secrets
5. **GitHub Actions CI** — Bob generates a complete pipeline from a single prompt
6. **General-purpose MCP** — Bob fetches live Spring Boot migration docs from the web
7. **Full SDLC** — assessment → migration → tests → CI/CD → containerization → PR in one session

---

## 🗺️ Lab Structure

| Act | Time | Focus | Key Bob Feature |
|-----|------|-------|-----------------|
| Setup | 0:00 – 0:07 | Start services, configure Bob | Custom mode + skill activation |
| Act 1 | 0:07 – 0:15 | Assess legacy codebase | Parallel reads, assessment plan |
| Act 2 | 0:15 – 0:25 | Modernize Java 8 → 17 | Parallel subagents, hooks |
| Act 3 | 0:25 – 0:33 | Add CI pipeline + Dockerfile | GitHub Actions generation |
| Act 4 | 0:33 – 0:40 | MCP + ship via PR | Fetch MCP, PR workflow |
| Act 5 | 0:40 – 0:45 | Freestyle / audience Q&A | Open demo |

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

### Step 4 — Open Bob and switch to Java Architect mode

1. Open the `lab5/` directory (or repo root) in Bob
2. Click the mode selector → choose **☕ Java Architect**
3. Confirm the mode badge changes in the UI

> 🎤 **Presenter note:** Say — *"Before I even type a prompt, I've switched Bob into a specialised
> persona. Java Architect mode primes Bob with Java 17 best practices and tells it to always propose
> a migration plan before touching code. It's like assigning a senior architect to your team."*

### Step 5 — Install and enable the fetch MCP

In Bob's MCP settings, add the fetch server from `lab5/.bob/mcp.json`:

```bash
# Verify Node.js can resolve the package
npx -y mcp-fetch-server --help
```

> 🎤 **Presenter note:** *"We've also added a general-purpose MCP — not GitHub-specific.
> This one lets Bob fetch any public URL. In Act 4, we'll use it to pull the Spring Boot
> migration guide live from spring.io."*

---

## 🔍 Act 1 — Orient & Assess [0:07 – 0:15]

> 🎤 **Presenter note:** *"The legacy service is running — the dashboard shows live data.
> Now I'm going to ask Bob to read this codebase and tell me what's wrong with it.
> Watch how many files it reads simultaneously."*

### Step 6 — Activate the java-modernization skill

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
> - The skill is activated; Bob references the Java 8 → 17 pattern map
> - Bob calls out the hardcoded `spring.datasource.password=admin123` as a security finding
> - Output is a structured plan with CRITICAL / HIGH / MEDIUM categories

> 🎤 **Presenter note:** *"Notice Bob read five files at the same time. v1 would have done
> them sequentially — one by one. v2 parallelises reads. This is the difference between
> a junior who works linearly and a senior who can process multiple things at once."*

> ✅ **Success check:** Bob's plan includes at minimum:
> - Migration of `InventoryItem` to a record
> - Replace `java.util.Date` with `LocalDateTime`
> - Replace for-loops with streams
> - Flag hardcoded password as CRITICAL
> - Missing tests, Dockerfile, CI as infrastructure gaps

---

## ⚡ Act 2 — Modernize + Parallel Subagents [0:15 – 0:25]

> 🎤 **Presenter note:** *"Now for the part SAP shops dream about. I'm going to ask Bob to
> start the migration AND spawn two specialist subagents at the same time — one doing a security
> audit, one writing tests. Three workstreams running in parallel."*

### Step 7 — Spawn the Security Auditor subagent

```
Read lab5/.bob/personas/security-auditor.md and take on that role as a subagent.
Perform a full security audit of the inventory service and produce a findings report.
```

> 👤 **What to look for:** Bob spawns a background subagent. The main conversation continues
> while the subagent works independently. You'll see two active workstreams in the UI.

### Step 8 — Simultaneously: modernize InventoryItem and InventoryService

In the **main conversation** (not the subagent), type:

```
While the security audit runs in the background, modernize the inventory service:

1. Convert InventoryItem.java to a Java record — replace all boilerplate with a single record declaration. Use LocalDateTime instead of Date.
2. Refactor InventoryService.java — replace all for-loops with Stream API. Replace new Date() with LocalDateTime.now().
3. Update InventoryController.java — remove raw HashMap error responses, use a proper Map<String, String> with var for local inference.

Apply changes in parallel where files are independent.
```

> 👤 **What to look for:**
> - Bob edits multiple files in parallel — watch the tool calls fire simultaneously
> - The **hook fires** when Bob tries to write `application.properties` (if it touches it during refactor)
> - Java goes from 80-line POJO to a 3-line record — point this out explicitly

> 🎤 **Presenter note:** *"Look at InventoryItem.java. It went from 96 lines of boilerplate to
> 3 lines — a Java record. That's the same data, zero noise. Now imagine doing this across
> 400 classes in an SAP extension. Bob can batch this."*

### Step 9 — Spawn the Test Engineer subagent

```
Read lab5/.bob/personas/test-engineer.md and take on that role as a subagent.
Write JUnit 5 unit tests for InventoryService and @WebMvcTest controller tests
for InventoryController. Place tests in lab5/service/src/test/java/com/example/inventory/.
```

> 👤 **What to look for:** A second subagent spawns. Now you have: main agent (migration) +
> Security Auditor + Test Engineer — three concurrent workstreams.

> 🎤 **Presenter note:** *"This is how a real senior engineer works. They don't do one thing
> at a time. Bob is now simultaneously finishing the migration, auditing for security, and
> writing tests. Each subagent has a clear persona and scope."*

---

## 🔒 Act 3 — Hooks + CI Pipeline [0:25 – 0:33]

> 🎤 **Presenter note:** *"Before we add CI, let me show you something that just happened.
> Bob tried to write application.properties earlier. Let me trigger the hook deliberately
> so you can see what deterministic guards look like in practice."*

### Step 10 — Trigger the secret-scanning hook

```
Update application.properties to change the H2 console path to /admin/h2-console.
Keep all other values the same.
```

> 👤 **What to look for:**
> - Bob tries to use a write tool on `application.properties`
> - The `check-secrets.sh` hook fires **before** the write completes
> - Bob sees the hook's block message (exit 2) and reports it in chat
> - Bob automatically pivots: "I notice there's a hardcoded password in this file.
>   Let me externalize it to an environment variable first."

> 🎤 **Presenter note:** *"The hook didn't just warn — it blocked. Bob couldn't write that
> file until the secret was gone. This is deterministic code running inside an AI workflow.
> No prompt engineering required. It's a hard rule."*

> 🎤 **Presenter note for SAP audience:** *"Think about what this means for SAP BTP deployments.
> Every time someone asks Bob to touch a config file, your credential policy enforces itself.
> Automatically."*

### Step 11 — Fix the secret properly

```
Externalize spring.datasource.password to an environment variable.
Update application.properties to use ${DB_PASSWORD:changeme} as the value.
Create a .env.example file showing how to set DB_PASSWORD.
```

> ✅ **You should see:** Bob writes the file successfully this time — no hook block.
> The command log at `.bob/hooks/command-log.txt` shows the command audit trail.

### Step 12 — Bob generates the GitHub Actions CI pipeline

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
> Point out the three jobs — build, scan, docker — and note that the secret scan in CI
> *echoes* the Bob hook: two layers of protection.

> 🎤 **Presenter note:** *"The CI pipeline has the same secret scan as the Bob hook.
> Local guard catches it before commit. Pipeline guard catches it before merge.
> Defence in depth — Bob built both layers."*

### Step 13 — Verify the Dockerfile

```
Show me the Dockerfile for the inventory service and explain the multi-stage build.
```

> 👤 **What to look for:** Bob reads `lab5/service/Dockerfile` and explains: build stage
> uses Maven + JDK 17, runtime stage uses JRE Alpine (smaller image), non-root user for security.

---

## 🌐 Act 4 — MCP + Ship [0:33 – 0:40]

> 🎤 **Presenter note:** *"One more thing before we ship. I want to show you a general-purpose
> MCP — the fetch server. This isn't GitHub-specific. It lets Bob reach out to any public URL.
> Watch Bob pull the Spring Boot 3.x migration guide live and use it to give us advice."*

### Step 14 — Use the fetch MCP to query live migration docs

```
Use the fetch tool to retrieve https://spring.io/blog/2022/05/24/spring-boot-3-0-m3-available-now
Summarize the breaking changes that are relevant to our inventory-service.
Which changes should we address before upgrading from Spring Boot 2.7 to 3.x?
```

> 👤 **What to look for:**
> - Bob makes a live HTTP request via the MCP
> - Bob cites specific content from the page (javax→jakarta, Spring Security changes)
> - Bob maps findings back to our specific codebase

> 🎤 **Presenter note:** *"Bob just read a live web page and applied it to our code. No copy-paste,
> no context switching. Any public documentation — Spring docs, RFC specs, your internal wiki if
> it's public — Bob can pull and reason over it in real time."*

### Step 15 — Generate the PR description

```
Generate a pull request description for the modernization work we've done.
Include: what changed, Java 17 features used, security improvements, infrastructure added.
Format it as a GitHub PR body.
```

> 👤 **What to look for:** Bob produces a structured PR description covering all changes.
> If GitHub is configured, use the Create PR workflow. Otherwise, copy-paste the output.

> 🎤 **Presenter note:** *"From legacy Java 8 service to modernized, containerized, tested,
> and CI'd codebase — assessed, built, secured, and shipped in one Bob session."*

---

## 🎙️ Act 5 — Freestyle / Audience Q&A [0:40 – 0:45]

> 🎤 **Presenter note:** *"The floor is open. Here are three prompts I keep in my back pocket
> for when the audience asks 'but can Bob do X?' — feel free to use these or take live questions."*

### Pre-scripted audience prompts

**Prompt A — "Can Bob review code like a senior engineer?"**
```
Review InventoryController.java as a senior Java engineer.
What would you flag in a code review? Be specific and cite line numbers.
```

**Prompt B — "Can Bob help with SAP-specific patterns?"**
```
This inventory service will be deployed as an SAP BTP extension.
What additional considerations should we address for BTP deployment?
Think about: multi-tenancy, service binding, logging, health endpoints.
```

**Prompt C — "Can Bob explain a complex migration risk?"**
```
Explain the risk of migrating from javax.validation to jakarta.validation
in a Spring Boot 3.x upgrade. What could break at runtime, and how do we test for it?
```

> 🎤 **Presenter note:** *"Notice Bob doesn't just answer the question — it reasons through the
> risk, proposes a mitigation, and offers to implement it. That's what makes it a partner,
> not just a search engine."*

---

## ✅ Success Criteria

By the end of the lab, the presenter should have demonstrated:

- [ ] Java service running live at `http://localhost:8080/api/inventory`
- [ ] Python dashboard showing live inventory data in the terminal
- [ ] Bob operating in **☕ Java Architect** mode with `java-modernization` skill active
- [ ] `InventoryItem.java` modernized from 96-line POJO to a Java record
- [ ] `InventoryService.java` refactored from for-loops to Stream API
- [ ] Secret-scanning hook **blocked** Bob from writing a file with `password=` in it
- [ ] `application.properties` updated to use `${DB_PASSWORD}` environment variable
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
| Hook not firing | Bob writes files without triggering secret scan | Verify `chmod +x lab5/.bob/hooks/*.sh` and that Bob's workspace root is the repo root (not a subdirectory) |
| MCP fetch error | Bob says "fetch tool not available" | Run `npx -y @modelcontextprotocol/server-fetch` once to install, then restart Bob |
| Dashboard connection error | `⚠ Cannot reach http://localhost:8080` | Java service isn't running — go to the service terminal and run `mvn spring-boot:run` |

---

## 💡 Tips for Presenters

1. **Lead with the SAP angle early.** In your opening 60 seconds, say: *"How many of you have
   a legacy Java 8 service somewhere in your SAP landscape that needs to move to BTP?"*
   Every hand goes up. You've just made it personal.

2. **Run everything before the audience arrives.** Have both terminals open and running.
   Cold Maven downloads kill demo energy. Pre-warm: `cd lab5/service && mvn dependency:resolve`.

3. **Let the hook moment breathe.** When the secret-scanning hook blocks Bob, pause.
   Let the audience read the error. Then say: *"Bob didn't just warn — it was stopped.
   That's deterministic code enforcing a policy inside an AI session."*

4. **The parallel subagent moment is your headline.** When Security Auditor + Test Engineer
   are both running while the main migration continues, say: *"Three engineers working
   simultaneously. How long would this take your team to do sequentially?"*

5. **Use the freestyle act for the skeptic in the room.** There's always someone who asks
   "yeah but what about X?" The pre-scripted prompts are your safety net. The BTP extension
   prompt (Prompt B) almost always gets a strong reaction from SAP audiences.

---

## 🚀 Next Steps

- Explore Bob's full capability set: [`bob-differentiators.md`](../bob-differentiators.md)
- Try Lab 4 for Bob's subagent + PR workflow demo with a React/Flask full-stack app: [`lab4/README.md`](../lab4/README.md)
- Read the hooks documentation: [`Hooks.md`](../Hooks.md)
- Explore the `java-modernization` skill: [`lab5/.bob/skills/java-modernization/SKILL.md`](.bob/skills/java-modernization/SKILL.md)
- Understand the subagent personas: [`lab5/.bob/personas/`](.bob/personas/)

---

*Last Updated: July 2025*
