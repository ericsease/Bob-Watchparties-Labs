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
 * Running on http://127.0.0.1:5000
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
| Frontend can't reach backend | Confirm Flask is running on port 5000; check `vite.config.js` proxy setting |
| `npm install` fails | Make sure you're on Node 18+: `node --version` |
| Bookmark button appears but doesn't save | Check the browser console for a failed `POST /api/bookmarks` call; confirm Flask is running |
| SQLite file missing | Delete `reporadar.db` if it's corrupted and restart Flask — it will re-seed |
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
