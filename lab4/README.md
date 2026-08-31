# Lab 4: Bob v2 in Action — The Bookmarks Feature

> **⏱ Duration:** 30 minutes  
> **Difficulty:** Intermediate  
> **Prerequisite:** Basic familiarity with Bob (Plan/Code modes, MCP, approvals)

---

## 🎯 What You'll Learn

By the end of this lab you will have experienced:

- ✅ **Subagents** — spinning off an isolated agent to handle a self-contained task
- ✅ **Parallel tool calling** — Bob reading multiple files simultaneously instead of one by one
- ✅ **Background tasks** — a subagent working while you continue the main conversation
- ✅ **Fewer interruptions, same control** — Bob acts autonomously on safe changes, gates on risky ones
- ✅ **Workflows** — the built-in Create PR workflow (or a plain-text PR description fallback)

---

## 🗺️ Lab Structure

```
[0:00] Setup          — get the app running
[0:05] Act 1 — Plan   — Bob reads the codebase and plans the feature
[0:15] Act 2 — Build  — parallel implementation + background test subagent
[0:23] Act 3 — Review — checkpoints, todo tracking, staying in control
[0:28] Act 4 — Ship   — PR workflow or plain-text description
[0:30] Done!
```

---

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- Node.js 18+
- Bob IDE (any recent version)
- Git

### 0. Enable the fetch MCP *(optional but recommended)*

This lab includes a general-purpose MCP that lets Bob fetch live web content.
It requires Node.js (already a prerequisite) and no API key.

In Bob's MCP settings, point it to the config at `lab4/.bob/mcp.json`, or run
once to pre-install the package:

```bash
npx -y @modelcontextprotocol/server-fetch --version
```

> 🎤 **Presenter note:** *"Before we start — I've added one MCP to this workspace.
> Not a GitHub-specific one. A general-purpose fetch tool that lets Bob reach any
> public URL. We'll use it at the end of the lab to pull live data from GitHub."*

### 1. Open the lab folder in Bob

Open the `lab4/` folder as your workspace in Bob.

### 2. Start the backend

Open a terminal and run:

```bash
cd lab4/backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

You should see:

```
Seeded 10 repos.
 * Running on http://127.0.0.1:5001
```

### 3. Start the frontend

Open a **second terminal** and run:

```bash
cd lab4/frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser. You should see a dark-themed page titled **📡 RepoRadar** with 10 trending repos listed.

> ✅ **Success check:** The app loads, repos appear, no console errors.

### 4. Verify the gap

Look at the app — there's no way to bookmark anything. The [`Sidebar.jsx`](frontend/src/components/Sidebar.jsx) component exists but renders nothing. That's what Bob is about to fix.

---

## 🎬 Act 1 — Orient & Plan `[0:00 – 0:05]`

> 🎤 **Presenter note:** In Bob v1, you'd start a task and Bob would ask 3–4 clarifying questions before doing anything. Bob v2 is different — it reasons through what it knows, then acts. Show this contrast explicitly.

> 🎤 **Presenter note — Rules:** *"One thing I've set up before this session: a custom rule file in `.bob/rules/`. It tells Bob to always use the SQLAlchemy 2.x `db.session.get()` API instead of the deprecated `Model.query.get()` form. Watch — when Bob writes the bookmark endpoints, it will follow that rule automatically without being told. That's the difference between a rule and a comment in code."*

### Step 1 — Switch to Plan mode

Click the mode selector and choose **Plan**.

### Step 2 — Ask Bob to read the codebase and plan the feature

Copy this prompt exactly:

```
Read the RepoRadar codebase — both the Flask backend (lab4/backend/) and the
React frontend (lab4/frontend/src/) — then create a detailed implementation
plan for a Bookmarks feature.

Requirements:
- Users can bookmark any repo by clicking a button on its card
- Bookmarks persist in the SQLite database (survive page refresh)
- Bookmarked repos appear in the Sidebar panel
- Users can remove a bookmark from the sidebar

Output a step-by-step plan covering: database changes, new API endpoints,
frontend state management, component changes, and what tests are needed.
```

> 🎤 **Presenter note:** Watch the tool call trace. Bob reads `app.py`, `models.py`, `RepoCard.jsx`, `App.jsx`, and `Sidebar.jsx` — **simultaneously**, not one at a time. That's parallel tool calling already happening in the planning phase.

> 👤 **What to look for:** In the tool call panel, you'll see multiple file reads firing at the same time rather than sequentially. This is Bob v2's native parallel execution.

> 🎤 **Presenter note:** Bob will produce a plan and a Todo list without asking follow-up questions. In v1 you'd be answering "Should I use REST or GraphQL?" and "Do you want optimistic UI updates?" — none of that here.

---

## ⚡ Act 2 — Parallel Power `[0:05 – 0:15]`

> 🎤 **Presenter note:** This is the heart of the demo. You're about to tell Bob to implement the whole feature. Watch what it does in parallel — and then spawn a subagent for tests while the main conversation keeps moving.

### Step 3 — Switch to Agent (Code) mode

Click the mode selector and choose **Agent**.

### Step 4 — Ask Bob to implement the feature

```
Implement the Bookmarks feature according to the plan you just created.

Work on the backend and frontend in parallel where possible:
- Backend: add a Bookmark model, create /api/bookmarks endpoints (GET, POST, DELETE)
- Frontend: wire up the bookmark button on RepoCard, implement the Sidebar to show bookmarks

Use the existing code style and patterns you see in the codebase.
```

> 🎤 **Presenter note:** Point out what Bob is doing in the tool trace. It will:
> 1. Read `models.py` and `app.py` at the same time (parallel reads)
> 2. Write the backend and plan the frontend edits concurrently
> 3. Make multiple file edits in sequence once it has all the context it needs

> 👤 **What to look for:** Multiple 📖 read icons appearing at the same time in the tool call panel — that's the parallel execution. In v1 this was strictly sequential: read one file → think → read next file → think → etc.

### Step 5 — Spawn a subagent for tests while Bob keeps working

Once Bob has started on the implementation (you don't have to wait for it to finish), send this follow-up:

```
While you continue with the implementation, spawn a subagent to write
unit tests for the new /api/bookmarks endpoints. The tests should cover:
- GET /api/bookmarks returns an empty list initially
- POST /api/bookmarks adds a bookmark and returns 201
- POST /api/bookmarks with an invalid repo_id returns 404
- DELETE /api/bookmarks/<id> removes the bookmark and returns 200

The subagent should write these to lab4/backend/tests/test_bookmarks.py
using pytest and Flask's test client.
```

> 🎤 **Presenter note:** This is the subagent moment. Bob will acknowledge that it's spawning a subagent for the tests and continue the main implementation. Two workstreams are now running. In v1 you'd wait for the whole feature, then ask for tests after.

> 👤 **What to look for:** Bob's response will mention delegating the test writing. The main conversation continues — you can keep chatting, asking questions, reviewing what Bob has done so far — while the tests are being generated independently.

> 🎤 **Presenter note:** While waiting, walk the audience through what's been built so far: the new `Bookmark` model, the `/api/bookmarks` routes, the updated `RepoCard.jsx`. Show the parallel work that already happened.

---

### Step 5.5 — Restart both servers to pick up the changes

Once Bob signals it has finished implementing, the servers need a restart before the new feature is visible in the browser. Flask must re-run `db.create_all()` to create the `bookmarks` table; the browser needs a hard refresh to load the updated components.

**Option A — Ask Bob to do it (recommended)**

```
The implementation looks complete. Please restart both servers for me:
kill the Flask process and restart it from lab4/backend, then confirm
the bookmarks table was created. I'll restart Vite manually.
```

> 🎤 **Presenter note:** Bob will run `pkill`/`kill` on the Flask process and relaunch it — another live example of agentic shell use. Hand Vite the manual restart (Ctrl+C → `npm run dev`) so participants see both paths.

**Option B — Manual restart**

```bash
# Terminal 1 — Flask
pkill -f "python.*app.py"; sleep 1
cd lab4/backend && source venv/bin/activate && python app.py

# Terminal 2 — Vite (Ctrl+C first, then)
cd lab4/frontend && npm run dev
```

Then **hard-refresh** the browser (`Cmd+Shift+R` on macOS / `Ctrl+Shift+R` on Windows).

> ✅ **You should now see:** ⭐ buttons on every repo card and **"No bookmarks yet."** in the sidebar panel. If you see `Error: Failed to fetch bookmarks`, Flask didn't restart cleanly — check Terminal 1.

---

## 🎛️ Act 3 — Control Without Babysitting `[0:15 – 0:23]`

> 🎤 **Presenter note:** The most common concern about AI doing more autonomously is "how do I stay in control?" Show the answer: Bob makes small safe changes freely, but surfaces a gate when something needs a decision.

### Step 6 — Watch the Todo list

Bob maintains a live checklist of what it planned to do vs. what's done. Ask:

```
Show me your current todo list for this feature — what's done, what's in progress,
and what's left?
```

> 👤 **What to look for:** Bob produces an ordered checklist. Each item is marked ✅ done, 🔄 in progress, or ⏳ pending. This is your real-time visibility into what the autonomous agent has actually done — no guessing.

### Step 7 — Trigger a checkpoint intentionally

If Bob hasn't already paused for approval, you can demonstrate the approval pattern manually. Ask Bob to do something that touches shared infrastructure:

```
Update the database.py to add a helper function that wipes all bookmarks
for a given user session. This will be useful for a "clear all" button later.
```

> 🎤 **Presenter note:** Bob will flag this as a change to a shared utility file (`database.py`) that other parts of the app depend on, and ask for your approval before proceeding. This is the "fewer interruptions, same control" principle in practice — Bob doesn't ask permission for adding a model field, but it does pause when touching shared infrastructure.

> 👤 **What to look for:** Bob either (a) asks you to confirm before modifying `database.py`, or (b) explains why the change is safe and proceeds. Either way, the decision surface is clear. Compare this to v1, where Bob might have asked you about safe changes and proceeded silently on risky ones.

### Step 8 — Check the subagent's work

By now the test subagent should have finished. Ask:

```
Has the test subagent completed? Show me what tests were written and
confirm they would pass against the implementation.
```

> 🎤 **Presenter note:** This closes the loop on the background task. The tests were written independently and in parallel with the feature. Real-world equivalent: a second developer wrote tests while you were coding.

### Step 9 — Reload the app and verify

In your browser, hard-refresh **http://localhost:5173**.

> ✅ **You should see:**
> - A ⭐ bookmark button on each repo card
> - Clicking it adds the repo to the Sidebar
> - Refreshing the page keeps your bookmarks (persisted in SQLite)
> - The Sidebar shows a list of saved repos with a remove button

---

## 🚀 Act 4 — Ship It `[0:23 – 0:28]`

> 🎤 **Presenter note:** The code is done. Show how Bob handles the "last mile" of shipping — creating a PR. Two options: the full GitHub workflow (for participants who have a GitHub repo set up), or a plain-text description (for everyone else).

### Option A — Bob's Create PR Workflow *(if you have GitHub configured)*

> 👤 **If you want to use this option:** You'll need a GitHub repo and the GitHub MCP server or git configured. If you're not sure, use Option B instead.

In the Bob chat, type `/` to open the workflow picker and select **Create Pull Request**:

```
/Create Pull Request
```

Bob will:
1. Run `git diff` against your base branch
2. Summarise the changes
3. Generate a PR title and description
4. Show it to you for review and editing
5. Create the PR on GitHub when you confirm

> 🎤 **Presenter note:** Walk through each step as Bob surfaces it. Edit the PR description live to show participants that Bob's output is a starting point — you're always in review. Hit confirm to create the PR.

---

### Option B — Plain-text PR description *(no GitHub required)*

```
We're ready to ship the Bookmarks feature. Write a pull request description
for the changes you just made. Include:
- A one-line summary
- What problem this solves
- A bullet list of all files changed and why
- How a reviewer should test it manually
- Any follow-up work you'd suggest
```

> 🎤 **Presenter note:** Bob reads the actual diff and produces a real PR description — not a template. Show participants the output. This is what you'd paste into GitHub, Bitbucket, or Azure DevOps.

---

### Bonus — Live data with the fetch MCP *(if time permits, ~2 min)*

> 🎤 **Presenter note:** *"Before we wrap — remember that fetch MCP I mentioned at the start?
> Let me show you one thing it enables."*

```
Use the fetch tool to retrieve https://github.com/trending?spoken_language_code=en
and compare the top 5 repos there against the repos currently seeded in RepoRadar.
Suggest 3 repos from the live trending list that would make good additions to our seed data.
```

> 👤 **What to look for:** Bob makes a live HTTP request, reads the page, and reasons over it in context. The audience sees Bob connecting to the real world — not just the local codebase.

> 🎤 **Presenter note:** *"This MCP isn't GitHub-specific. It can hit your internal wiki,
> a Confluence page, a public API spec — anything with a URL. That's the power of
> general-purpose MCP connections."*

---

## 🔮 Going Further — Hooks & Workflows

> 🎤 **Presenter note (voiceover):** *"Everything you've seen today — the parallel execution,
> subagents, approvals, the PR workflow — these are the building blocks. But there are two
> more layers worth knowing about."*

**Lifecycle Hooks** let you attach deterministic shell scripts to Bob's actions:
- A `PreToolUse` hook that scans every file Bob writes for hardcoded secrets — and **blocks** the write if it finds one
- A `SessionStart` hook that injects your git branch, environment info, and project context into Bob automatically at the start of every session
- A `PostToolUse` hook that logs every shell command Bob runs to an audit file

*"Imagine a rule that says: Bob can never write a file outside `src/`. Or: before any commit, run the linter. These are hard guardrails — not prompt suggestions."*

**Custom Workflows** let you define multi-step sequences Bob can execute with a single `/` command:
- The **Create PR** workflow you just saw is a built-in example
- You can author your own: `/deploy-to-staging`, `/run-security-scan`, `/generate-changelog`
- Each workflow is a structured prompt sequence that Bob follows reliably every time

*"The combination is what makes Bob a full SDLC partner. Write code in parallel with subagents, enforce team standards via rules, gate risky actions with hooks, and ship with reproducible workflows. All in one session."*

---

## ✅ Success Criteria

At the end of the lab you should have:

- [ ] The RepoRadar app running locally with the Bookmarks feature working
- [ ] A `Bookmark` model in `models.py` with a new `bookmarks` table in SQLite
- [ ] Three new API endpoints: `GET /api/bookmarks`, `POST /api/bookmarks`, `DELETE /api/bookmarks/<id>`
- [ ] `RepoCard.jsx` updated with a working ⭐ bookmark button
- [ ] `Sidebar.jsx` implemented to display and manage bookmarks
- [ ] Unit tests in `lab4/backend/tests/test_bookmarks.py`
- [ ] A PR description (as a GitHub PR or as text)
- [ ] You witnessed parallel tool calls, a subagent, and a checkpoint gate

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| Backend won't start — `ModuleNotFoundError` | Make sure you activated the venv: `source venv/bin/activate` |
| Frontend shows "Failed to fetch repos" on macOS | macOS AirPlay Receiver occupies port 5000. This project uses port 5001 — confirm Flask started on 5001 |
| Frontend can't reach backend | Confirm Flask is running on port 5001; check `vite.config.js` proxy setting |
| `npm install` fails | Make sure you're on Node 18+: `node --version` |
| Bookmark button appears but doesn't save | Check the browser console for a failed `POST /api/bookmarks` call; confirm Flask is running |
| SQLite file missing | Delete `reporadar.db` if it's corrupted and restart Flask — it will re-seed |
| `LegacyAPIWarning` in Flask terminal | Bob generated `Model.query.get(id)` — ask Bob to replace it with `db.session.get(Model, id)` (SQLAlchemy 2.x API) |
| Bob keeps asking questions instead of acting | Make sure you're in **Agent** mode, not Plan mode, for Act 2 |

---

## 💡 Tips for Presenters

- **Pre-run the app** before your session so the SQLite DB is already seeded
- **Zoom in on the tool call trace** panel — the parallel reads are the visual centrepiece of Act 2
- **Name the contrasts out loud:** "In v1 this was sequential… watch what happens now"
- **Don't rush Act 3** — the approval gate moment is often the most surprising for audiences
- **The subagent running in the background** is most dramatic if you visibly continue chatting in the main thread while it works — show the two conversations side by side if you can

---

## 🚀 Next Steps

- **Extend the feature:** Ask Bob to add a "notes" field to bookmarks, or export bookmarks as JSON
- **Add authentication:** Ask Bob to add a simple user session so different users have different bookmarks
- **Explore Bob Findings:** Ask Bob to run a security and quality scan on the new code it just wrote
- **Try Lab 3:** [`../lab3/README.md`](../lab3/README.md) — security analysis on a vulnerable app

---

*Lab 4 — Bob Watch Parties | Last Updated: July 2025*
