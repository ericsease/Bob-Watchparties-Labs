# Lab 6 — Grocery Analytics with Bob
## Plan Document

**Goal:** Design and build a 2-hour Bobathon lab for retail IT/inventory controllers at a
grocery chain. The lab demonstrates Bob as an AI pair for data analysis workflows: reading
Excel files, generating Jupyter notebook code, integrating live web event data as a demand
signal, and producing actionable reorder/forecast outputs — without touching the Lab 5
Java service.

**Audience:** Grocery/retail IT and inventory controllers. Heavy Excel users. Not
necessarily developers. Düsseldorf / NRW region context. No client name in materials.

**Live crawl targets (try in order):**
1. `https://www.visitduesseldorf.de/erleben/veranstaltungen/veranstaltungskalender#/event`
2. `https://rausgegangen.de/duesseldorf/`

**Target duration:** ~2 hours (3 stages × ~30 min + 1 optional bonus stage ~15 min).
Each stage is self-contained so a facilitator can cut Stage 4 if time runs short.

**Bob features demonstrated across the lab:**
- Excel file reading + pandas code generation
- Jupyter notebook generation from a plain-English brief
- Anomaly/alert detection via data analysis
- MCP fetch for live web data (local events as demand signal)
- Multi-step agentic reasoning across notebook cells
- Skill loading (grocery-analytics playbook)
- Custom mode (Data Analyst Architect)
- Hooks (data quality gate on file writes)
- Subagent parallelism (EDA subagent + event-crawler subagent running together)

---

## Repository Layout

All lab files live under `lab6/`. The structure mirrors Lab 5 conventions:

```
lab6/
├── README.md                          — facilitator + participant guide
├── data/
│   ├── grocery_inventory.xlsx         — rich mock dataset (primary artifact)
│   ├── grocery_inventory.csv          — CSV export of same data (fallback)
│   └── local_events_fallback.json     — curated mock event data for offline use
├── notebooks/
│   ├── starter.ipynb                  — stub notebook (imports + data load cell only)
│   └── solution.ipynb                 — completed reference notebook (facilitator only)
├── requirements.txt                   — pandas, matplotlib, openpyxl, notebook, requests
├── .bob/
│   ├── custom_modes.yaml              — 📊 Data Analyst Architect mode
│   ├── settings.json                  — hooks (data quality gate, command log)
│   ├── mcp.json                       — fetch server for event crawling
│   ├── hooks/
│   │   ├── check-data-quality.sh      — PreToolUse: warn if writing over raw data file
│   │   └── log-commands.sh            — PostToolUse: log executed commands
│   ├── skills/
│   │   └── grocery-analytics/
│   │       └── SKILL.md               — analytics playbook (trigger phrases, patterns)
│   └── personas/
│       ├── eda-analyst.md             — EDA subagent persona
│       └── event-crawler.md           — event data subagent persona
└── demo-deck/                         — facilitator slide deck (PPTX)
```

---

## Dataset Specification

**File:** `lab6/data/grocery_inventory.xlsx`

**Size:** ~300 rows, 1 worksheet named "Inventory"

**Columns:**

| Column | Type | Description |
|---|---|---|
| sku | string | e.g. `BEER-001`, `PROD-012` |
| product_name | string | e.g. "Pilsner Lager 500ml 6-pack" |
| category | string | One of: Beer/Spirits, Produce, Dairy, Bakery, Frozen, HBC |
| store_id | string | One of 5 store codes: `STR-A` – `STR-E` |
| week | date | ISO week start date, 12 weeks of history |
| units_sold | int | Weekly units sold (realistic seasonal variation) |
| stock_level | int | End-of-week stock on hand |
| reorder_threshold | int | When stock_level falls below this, reorder triggered |
| supplier_lead_days | int | Days until replenishment arrives |
| unit_cost_eur | float | Cost per unit in EUR |
| sell_price_eur | float | Retail sell price per unit |
| on_promotion | bool | Whether item was on promo that week |

**Data quality issues intentionally seeded (teaching moments):**
- ~5 rows with `stock_level < 0` (data entry errors)
- ~8 rows where `stock_level < reorder_threshold` but no flag set (alert candidates)
- ~3 rows with `units_sold = 0` and `on_promotion = True` (suspicious anomaly)
- ~2 rows with missing `sell_price_eur` (NULL / NaN)
- Beer/Spirits category shows clear sales spikes in summer weeks (seasonal signal)
- Store STR-C has consistently higher stockouts than others (outlier store)

**Scope of categories:**
- Beer/Spirits: 8 SKUs (lager, wheat beer, wine, prosecco, spirits)
- Produce: 12 SKUs (seasonal veg, fruit, herbs)
- Dairy: 10 SKUs (milk, yogurt, cheese, butter)
- Bakery: 8 SKUs (bread, rolls, pastries)
- Frozen: 8 SKUs (pizza, veg, ice cream)
- HBC: 4 SKUs (health/beauty/cleaning — low velocity, high margin)

**`local_events_fallback.json` structure:**
```json
[
  { "date": "2026-07-12", "name": "Rheinkirmes", "city": "Düsseldorf",
    "expected_attendance": 50000, "category_boosts": ["Beer/Spirits", "Bakery", "Produce"] },
  { "date": "2026-11-22", "name": "Fortuna Düsseldorf vs FC Köln", "city": "Düsseldorf",
    "expected_attendance": 55000, "category_boosts": ["Beer/Spirits", "HBC"] },
  { "date": "2026-12-05", "name": "Düsseldorfer Weihnachtsmarkt", "city": "Düsseldorf",
    "expected_attendance": 30000, "category_boosts": ["Beer/Spirits", "Bakery"] },
  { "date": "2026-02-28", "name": "Karneval Düsseldorf", "city": "Düsseldorf",
    "expected_attendance": 40000, "category_boosts": ["Beer/Spirits", "Bakery"] },
  { "date": "2026-09-05", "name": "Düsseldorfer Weinfest", "city": "Düsseldorf",
    "expected_attendance": 20000, "category_boosts": ["Beer/Spirits", "Produce"] },
  { "date": "2026-04-26", "name": "Düsseldorf Marathon", "city": "Düsseldorf",
    "expected_attendance": 15000, "category_boosts": ["Produce", "Dairy", "HBC"] },
  { "date": "2026-10-15", "name": "Tonhalle Konzert", "city": "Düsseldorf",
    "expected_attendance": 10000, "category_boosts": ["Beer/Spirits", "HBC"] },
  { "date": "2026-12-18", "name": "Oberhausen Weihnachtsmarkt", "city": "Oberhausen",
    "expected_attendance": 8000, "category_boosts": ["Bakery", "Dairy"] }
]
```

---

## Stage Breakdown

---

### Stage 1 — Excel Meets Bob (Data Onboarding)
**Status:** [ ] pending

#### Intent
Show controllers how Bob can read their existing Excel file, describe what it contains,
identify data quality issues, and generate clean pandas loading code — all from plain
English prompts. This is the "aha" moment for heavy Excel users: Bob bridges the gap
between spreadsheet and automation.

#### Bob Features Demonstrated
- File reading (office_read on .xlsx)
- Code generation (pandas DataFrame, dtype coercion, NaN handling)
- Anomaly detection prompted in plain English
- Custom mode: 📊 Data Analyst Architect (loaded at session start)
- Skill: `grocery-analytics` (loaded mid-stage to show the pattern)

#### Expected Outcomes
- Participant can ask Bob to describe the Excel file and get back a column-by-column summary
- Bob generates a working pandas cell that loads the file with correct dtypes
- Bob identifies the 3 categories of data quality issues (negative stock, missing prices, promo anomaly)
- Bob generates a `data_quality_report()` function that surfaces all issues as a printed summary
- Participant understands: Bob does not need them to write code first

#### Stage Flow (facilitator guide)
1. **Setup** (5 min): Open Bob in Plan mode. Show `lab6/` directory. Run
   `pip install -r requirements.txt`. Open `notebooks/starter.ipynb`.
2. **Act 1 — Describe the data** (7 min):
   Prompt: *"Read grocery_inventory.xlsx and tell me what data we have, column by column."*
   Bob uses `office_read` → returns schema + sample values + column descriptions.
3. **Act 2 — Generate load code** (8 min):
   Prompt: *"Write me a pandas cell that loads this file cleanly, sets correct types for
   dates and booleans, and prints shape and dtypes."*
   Bob writes cell → participant pastes into notebook → runs it → succeeds.
4. **Act 3 — Spot the problems** (10 min):
   Load `grocery-analytics` skill. Prompt: *"Check this dataset for data quality issues.
   I specifically care about stock levels, prices, and promotions."*
   Bob finds all 3 seeded issue categories. Generates `data_quality_report()`.

#### Relevant Files
- `lab6/data/grocery_inventory.xlsx` — primary data artifact
- `lab6/notebooks/starter.ipynb` — participant's working file
- `lab6/.bob/custom_modes.yaml` — Data Analyst Architect mode
- `lab6/.bob/skills/grocery-analytics/SKILL.md` — analytics playbook

#### Todo List
- [ ] Create `lab6/data/grocery_inventory.xlsx` with 300-row dataset per spec above
- [ ] Create `lab6/data/grocery_inventory.csv` as a CSV export of same data
- [ ] Create `lab6/notebooks/starter.ipynb` with only: markdown title cell + imports cell + empty "Load Data" cell
- [ ] Create `lab6/requirements.txt` (pandas, matplotlib, openpyxl, notebook, requests)
- [ ] Create `lab6/.bob/custom_modes.yaml` — Data Analyst Architect mode
- [ ] Create `lab6/.bob/skills/grocery-analytics/SKILL.md` — analytics playbook
- [ ] Create `lab6/.bob/settings.json` — hooks config
- [ ] Create `lab6/.bob/mcp.json` — fetch server registration
- [ ] Create `lab6/.bob/hooks/check-data-quality.sh` — warn on raw data overwrite
- [ ] Create `lab6/.bob/hooks/log-commands.sh` — command log (copy from lab5 pattern)
- [ ] Write Stage 1 section of `lab6/README.md`

---

### Stage 2 — Notebook Generation and EDA
**Status:** [ ] pending

#### Intent
Bob generates a full exploratory data analysis (EDA) notebook section from a plain-English
analyst brief. Participants see Bob reason across multiple steps: choosing the right charts,
writing grouped aggregations, generating reorder alerts, and exporting a summary to Excel.
Two subagents run in parallel — one for EDA, one scoping the event-demand connection (sets
up Stage 3). This is the "code generation at scale" moment.

#### Bob Features Demonstrated
- Multi-cell notebook generation from a brief
- Parallel subagents (EDA analyst + event crawler scoping in background)
- Grouped pandas aggregations, matplotlib visualisation
- Reorder alert logic (stock_level < reorder_threshold)
- Export to Excel (`.to_excel()`)
- Plan mode → Agent mode switch to show the plan-then-execute discipline

#### Expected Outcomes
- Bob produces a 6–8 cell EDA section covering: category sales distribution, weekly trend
  per category, top 10 stockout-risk SKUs, store-level comparison (STR-C outlier visible),
  margin analysis (sell_price - unit_cost), and a reorder alert table
- A `reorder_alerts.xlsx` file is generated by the notebook
- Participants understand: writing the brief well matters; Bob's output quality follows brief quality
- The event-crawler subagent returns a JSON list of upcoming events (from fallback file or live),
  priming Stage 3

#### Stage Flow (facilitator guide)
1. **Setup** (3 min): Switch Bob to Agent mode. Brief the room on what a "notebook brief" is.
2. **Act 1 — Write the brief** (5 min):
   Facilitator + room co-write a plain-English brief on the whiteboard/slide:
   *"I need an EDA notebook for our grocery inventory data. Show sales by category,
   weekly trend for Beer/Spirits, highlight stores with stockouts, calculate margin
   per SKU, and flag everything below reorder threshold. Export the alert table to Excel."*
3. **Act 2 — Launch parallel subagents** (15 min):
   Prompt: *"Use the eda-analyst persona to generate the EDA notebook cells from this brief.
   At the same time, use the event-crawler persona to find upcoming public events in the
   Düsseldorf region this month and return which grocery categories they will boost."*
   Bob spawns both subagents. Audience watches dual streams. EDA cells appear first.
   Event list returns (from MCP fetch or fallback JSON). Both complete.
4. **Act 3 — Run and verify** (7 min):
   Paste generated cells into notebook. Run all. Charts render. Reorder alert table prints.
   `reorder_alerts.xlsx` created. Facilitator highlights STR-C outlier in the store chart.

#### Relevant Files
- `lab6/.bob/personas/eda-analyst.md` — EDA subagent persona
- `lab6/.bob/personas/event-crawler.md` — event crawler persona
- `lab6/.bob/mcp.json` — fetch server for live event crawling
- `lab6/data/local_events_fallback.json` — offline fallback event data
- `lab6/notebooks/starter.ipynb` — participant's working file

#### Todo List
- [ ] Create `lab6/.bob/personas/eda-analyst.md`
- [ ] Create `lab6/.bob/personas/event-crawler.md`
- [ ] Create `lab6/data/local_events_fallback.json` with 6–8 realistic Düsseldorf/NRW events
- [ ] Write Stage 2 section of `lab6/README.md`
- [ ] Write the "analyst brief" as a pre-formatted prompt block in README for facilitator copy-paste

---

### Stage 3 — Local Events as a Demand Signal
**Status:** [ ] pending

#### Intent
The event crawler's output from Stage 2 feeds into a demand-boost model. Bob writes a
notebook section that joins the events list against inventory SKUs, calculates how many
extra units to pre-order, and flags the affected SKUs with a boost recommendation. This
is the "data layer use case" the customer envisioned — connecting external signals to
inventory decisions without building a custom integration.

#### Bob Features Demonstrated
- MCP fetch (live web crawl of a public event/festival listing)
- Joining external signal data to internal inventory data in pandas
- Parameterised demand boost logic written by Bob
- Plain-English → business logic translation ("if attendance > 10,000 and category is
  Beer/Spirits, multiply reorder quantity by 1.5")
- Annotated notebook cells with markdown explanations (Bob documents its own code)

#### Expected Outcomes
- A `boost_events()` function that takes events JSON + inventory DataFrame, returns a
  boosted reorder table
- At least 3 Beer/Spirits SKUs and 2 Bakery SKUs flagged for the Weihnachtsmarkt event
- A formatted markdown cell explaining the boost logic in plain language (auto-generated)
- Participants see: Bob can be the integration layer between a spreadsheet and the internet
  without any custom ETL pipeline

#### Stage Flow (facilitator guide)
1. **Setup** (3 min): Show the event JSON output from Stage 2 (or load fallback).
   Show that it has `category_boosts` mapped to our category names.
2. **Act 1 — Describe the business rule** (5 min):
   Prompt: *"I have a list of upcoming local events with expected attendance and the grocery
   categories they affect. Write a function that boosts reorder quantities for affected SKUs
   based on event attendance. For attendance over 10,000 apply a 1.5× multiplier; over
   25,000 use 2×. Show me the result as a table sorted by boost magnitude."*
3. **Act 2 — Live event crawl demo** (10 min):
   If wifi is reliable: use MCP fetch, trying these URLs in order:
   1. `https://www.visitduesseldorf.de/erleben/veranstaltungen/veranstaltungskalender#/event`
   2. `https://rausgegangen.de/duesseldorf/`
   Bob extracts event names, dates, attendance estimates. Formats into the same JSON
   structure as the fallback.
   If both fail: load `local_events_fallback.json` directly, explain the pattern.
4. **Act 3 — Run the boost model** (10 min):
   Paste `boost_events()` into notebook. Call it with the events data. Table renders.
   Facilitator points to Rheinkirmes row — Beer SKUs flagged. Ask room: "Would you
   have caught this manually?" Pause for discussion.
5. **Act 4 — Bob documents** (2 min):
   Prompt: *"Add a markdown cell above the boost function explaining to a non-technical
   store manager what this model does and when to use it."*
   Bob writes plain-language documentation cell.

#### Relevant Files
- `lab6/data/local_events_fallback.json` — fallback event data
- `lab6/.bob/mcp.json` — fetch server
- `lab6/notebooks/starter.ipynb` — participant's working file

#### Todo List
- [ ] Verify `local_events_fallback.json` has enough variety (seasonal + sport + cultural events)
- [ ] Add Düsseldorf event URLs to README as facilitator reference:
  1. `https://www.visitduesseldorf.de/erleben/veranstaltungen/veranstaltungskalender#/event`
  2. `https://rausgegangen.de/duesseldorf/`
- [ ] Write Stage 3 section of `lab6/README.md`
- [ ] Write the "boost rule" prompt block in README for facilitator copy-paste

---

### Stage 4 — Financial Summary Report
**Status:** [ ] pending

#### Intent
The optional final stage targets the "financial planning" angle. Bob takes the complete
notebook analysis and generates a board-ready financial summary: a formatted multi-tab
Excel workbook with a KPI dashboard tab, a reorder cost projection tab, and a margin
analysis tab. This closes the loop — the analysis that started in Excel ends as a
polished Excel deliverable, generated by Bob without manual copy-pasting.

#### Bob Features Demonstrated
- Multi-tab Excel export via openpyxl/pandas (`.ExcelWriter` pattern)
- Financial KPI calculation (total reorder cost, gross margin %, stockout cost estimate)
- Bob narrating what it is doing step-by-step (chain of thought in output)
- "Explain this to my CFO" prompt pattern — plain-language executive summary generated
  alongside the workbook

#### Expected Outcomes
- A `financial_summary.xlsx` with 3 tabs: KPI Dashboard, Reorder Cost Projection, Margin Analysis
- KPI Dashboard tab includes: total inventory value, avg gross margin %, stores below reorder
  SLA count, estimated stockout revenue loss (units × sell price for items at 0 stock)
- Bob generates a 3-paragraph executive summary text the controller can paste into an email
- Participants see: the full loop from raw data → insight → formatted deliverable, all prompted
  in plain English

#### Stage Flow (facilitator guide)
1. **Setup** (2 min): Confirm notebook is running cleanly from Stage 3.
2. **Act 1 — Define the KPIs** (5 min):
   Prompt: *"Based on our analysis, calculate these KPIs from the data: total current inventory
   value, average gross margin per category, number of SKUs at stockout risk this week,
   and estimated revenue at risk from stockouts. Show as a summary table."*
3. **Act 2 — Generate the workbook** (10 min):
   Prompt: *"Now write code to export these results to a multi-tab Excel file called
   financial_summary.xlsx. Tab 1: KPI Dashboard. Tab 2: Reorder Cost Projection (SKU list
   with reorder qty × unit cost). Tab 3: Margin Analysis by category. Use pandas ExcelWriter."*
4. **Act 3 — Write the CFO summary** (5 min):
   Prompt: *"Write a 3-paragraph email summary of this analysis for a CFO who doesn't look
   at spreadsheets. Focus on risks, the event demand opportunity, and the one store needing
   attention."*
   Bob generates the text. Facilitator reads it aloud. Room reacts.

#### Relevant Files
- `lab6/notebooks/starter.ipynb` — participant's working file (by now substantially complete)
- `lab6/data/grocery_inventory.xlsx` — source data

#### Todo List
- [ ] Write Stage 4 section of `lab6/README.md`
- [ ] Add the KPI prompt and CFO summary prompt as pre-formatted blocks in README
- [ ] Ensure `solution.ipynb` includes all 4 stages completed as facilitator reference

---

## Bob Configuration Details

### Custom Mode: 📊 Data Analyst Architect

**File:** `lab6/.bob/custom_modes.yaml`

**Slug:** `data-analyst-architect`

**Role:** An expert data analyst and Python engineer specialising in retail/grocery inventory
analytics. Fluent in pandas, matplotlib, openpyxl, and Jupyter notebooks. Always explains
what it is doing before writing code. Surfaces data quality issues proactively.

**Inline rules (customInstructions):**
1. Always read the data file before writing analysis code — never assume column names
2. Flag data quality issues (nulls, negatives, anomalies) before proceeding to analysis
3. Prefer readable pandas over clever one-liners — controllers need to understand the code
4. Always annotate generated notebook cells with a markdown cell explaining the output
5. When writing Excel exports, use multi-tab ExcelWriter pattern — never overwrite input files
6. For demand forecasting, always ask for the business rule first, then encode it
7. Plan the full notebook structure before writing any cell

### Skill: grocery-analytics

**File:** `lab6/.bob/skills/grocery-analytics/SKILL.md`

**Trigger phrases:** "analyse inventory", "check data quality", "reorder alert",
"demand forecast", "event boost", "stock report", "export to Excel", "EDA"

**Contents:**
- Grocery category taxonomy (Beer/Spirits, Produce, Dairy, Bakery, Frozen, HBC)
- Standard column name map (sku, stock_level, reorder_threshold, etc.)
- Pattern table: common pandas idioms for inventory analysis
- Reorder alert formula: `stock_level < reorder_threshold AND supplier_lead_days > 0`
- Demand boost multiplier table (attendance tiers → multiplier)
- Excel export pattern (multi-tab ExcelWriter boilerplate)
- Preferred chart types per analysis (bar for category, line for trend, scatter for margin)

### Personas

**`eda-analyst.md`**
- Role: Senior retail data analyst, 10 years grocery sector
- Responsibilities: EDA only — describe, aggregate, visualise, flag anomalies
- Output format: numbered list of findings, then code cells (one cell per finding)
- Constraints: Does not make business recommendations, only surfaces what the data shows

**`event-crawler.md`**
- Role: External data specialist
- Responsibilities: Find upcoming public events, estimate attendance, map to grocery categories
- Output format: JSON array matching `local_events_fallback.json` schema
- Constraints: If live crawl fails, say so and load the fallback file; never invent events

### Hooks

**`check-data-quality.sh` (PreToolUse)**
- Matcher: `write_file|apply_diff` targeting `*.xlsx` or `*.csv` in the `data/` directory
- Behaviour: Prints a warning — "You are about to modify a raw data file. Are you sure?
  Consider writing to a new file instead."
- Purpose: Teaches data engineering discipline — raw data is immutable

**`log-commands.sh` (PostToolUse)**
- Same pattern as Lab 5 — logs all `execute_command` calls with timestamp
- File: `lab6/.bob/hooks/command-log.txt`

### MCP Configuration

**`lab6/.bob/mcp.json`**
```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```
Used in Stage 3 to crawl a live public events page. The fallback JSON covers offline runs.

---

## README Structure

`lab6/README.md` must include:

1. **Lab overview** — goal, audience, duration, prerequisites
2. **Prerequisites** — Python 3.10+, Node.js (for MCP fetch), pip, Jupyter
3. **Setup instructions** — clone, `pip install -r requirements.txt`, open notebook
4. **Bob setup** — open lab6/ in Bob, confirm Data Analyst Architect mode loads
5. **Stage 1 guide** — facilitator script + copy-paste prompts
6. **Stage 2 guide** — facilitator script + analyst brief text + parallel subagent prompt
7. **Stage 3 guide** — facilitator script + boost rule prompt + live crawl URL list + fallback instruction
8. **Stage 4 guide** — facilitator script + KPI prompt + CFO summary prompt
9. **Facilitator tips** — what to do if wifi fails, if notebook kernel crashes, if Bob generates wrong column names
10. **Dataset reference** — column descriptions, seeded data quality issues (so facilitator can point them out)
11. **Solution reference** — pointer to `solution.ipynb`

---

## Implementation Order

Sub-tasks should be executed in this sequence to avoid dependencies:

1. **Sub-task 1:** Generate dataset (`grocery_inventory.xlsx` + `.csv` + `local_events_fallback.json`)
2. **Sub-task 2:** Create Bob configuration files (custom mode, skill, personas, hooks, mcp.json)
3. **Sub-task 3:** Create the starter notebook and requirements.txt
4. **Sub-task 4:** Write `lab6/README.md` (all stages)
5. **Sub-task 5:** Create the solution notebook (`solution.ipynb`) as facilitator reference
6. **Sub-task 6:** Create the demo deck outline in `lab6/demo-deck/`

Each sub-task is independently verifiable and produces concrete file artifacts.
