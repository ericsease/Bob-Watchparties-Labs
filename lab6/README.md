# Lab 6 — Grocery Inventory Analytics with Bob

> **Bobathon Workshop** | Duration: ~2 hours | Level: No coding experience required

Bob as an AI pair for data analysis. Starting from an Excel file, participants
use Bob to onboard data, join external CSVs, run exploratory analysis, build an
event-driven demand model, load everything into a SQLite database, and produce a
board-ready financial summary — all through plain-English prompts.

---

## Overview

| Stage | Title | Duration | Bob feature highlight |
|---|---|---|---|
| 1 | Excel Meets Bob | ~30 min | `office_read`, data quality audit, pandas codegen |
| 2 | EDA & External Data Join | ~30 min | CSV joins, supplier price gap, enriched margins, parallel subagents |
| 3 | Events as a Demand Signal | ~30 min | MCP fetch (live web crawl), boost model |
| 4 | SQLite Database & Financial Summary | ~30 min | SQLite schema, SQL queries, 4-tab Excel export |

**Bob mode used:** 📊 Data Analyst Architect
**Skill loaded mid-lab:** `grocery-analytics`
**Datasets:** `grocery_inventory.xlsx` · `supplier_prices.csv` · `promo_calendar.csv` · `local_events_fallback.json`

---

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) — needed for MCP fetch in Stage 3 |
| pip | any | bundled with Python |
| Bob | latest | — |

---

## Setup

```bash
# 1. Install Python dependencies
pip install -r lab6/requirements.txt

# 2. Open the starter notebook
jupyter notebook lab6/notebooks/starter.ipynb
```

**Bob setup:**

1. Open Bob with the `lab6/` directory as workspace root
2. At session start, Bob will load the **📊 Data Analyst Architect** custom mode
   automatically from `lab6/.bob/custom_modes.yaml`
3. Keep the starter notebook open alongside Bob

---

## Stage 1 — Excel Meets Bob (~30 min)

**Goal:** Bob reads the Excel file, describes the data, generates clean loading code,
and runs a data quality audit.

### Setup (5 min)

- Open Bob. Confirm the mode indicator shows **📊 Data Analyst Architect**
- Open `lab6/notebooks/starter.ipynb` in Jupyter
- Run the **Imports** cell (Cell 2) — confirm `✅ Imports OK`

---

### Act 1 — Describe the data (7 min)

**Copy-paste prompt:**

```
Read lab6/data/grocery_inventory.xlsx and tell me what data we have, column by column.
Describe the data type, what it represents, and give me a sample value for each column.
```

Bob will use `office_read` on the file and return a column-by-column summary with
sample values. **Watch for:** Bob reading the file before making any assumptions — this
is Rule 1 of the Data Analyst Architect mode.

---

### Act 2 — Generate the load cell (8 min)

**Copy-paste prompt:**

```
Write me a pandas cell that loads lab6/data/grocery_inventory.xlsx cleanly:
- Sheet name: Inventory
- Parse the 'week' column as a date
- Cast 'on_promotion' as boolean
- Print the DataFrame shape and dtypes when done
```

Paste Bob's output into the **Load Data** cell in the notebook and run it.
Expected output: `(3000, 12)` and correct dtypes (`week` as datetime64, `on_promotion` as bool).

---

### Act 3 — Spot the problems (10 min)

First, load the skill:

**Copy-paste prompt:**

```
Load the grocery-analytics skill.
```

Then:

**Copy-paste prompt:**

```
Check this dataset for data quality issues.
I specifically care about stock levels, prices, and promotions.
Generate a data_quality_report() function that surfaces all issues
as a printed summary with row counts and example values.
```

Bob will find all four seeded issues (see [Dataset Reference](#dataset-reference) below).
Paste the generated function into the **Data Quality Report** cell and run it.

**Discussion point:** Ask the room — *"How long would this have taken in Excel?"*

---

## Stage 2 — EDA & External Data Join (~30 min)

**Goal:** Bob generates an EDA notebook section from a plain-English brief, then loads
and joins two external CSVs — a supplier price list and a promotional calendar — to
enrich the analysis. Two subagents run in parallel: one for EDA, one scoping events for Stage 3.

### Setup (3 min)

Switch Bob to **Agent** mode. Brief the room:

> *"We're going to write a brief — like a job spec for an analyst — and Bob will generate
> the analysis code from it. Then we'll bring in two more data sources Bob hasn't seen yet."*

---

### Act 1 — Co-write the brief (5 min)

**Analyst brief (copy-paste prompt):**

```
I need an EDA section for our grocery inventory notebook. Use the eda-analyst persona.

Cover these points:
1. Total units sold by category (horizontal bar chart)
2. Weekly sales trend for Beer/Spirits across all stores (line chart)
3. Store comparison: which store has the most SKUs below reorder threshold? (bar chart)
4. Reorder alert table: all SKUs currently below threshold, with units_to_order calculated
5. Export the reorder alert table to reorder_alerts.xlsx

Generate a numbered outline of the cells you will produce first, then wait for my OK.
```

Bob returns the outline. Confirm it, then say `OK, generate the cells.`

---

### Act 2 — Launch parallel subagents (10 min)

**Copy-paste prompt:**

```
Now run two tasks in parallel:

Task A: Generate the EDA notebook cells from the brief above using the eda-analyst persona.

Task B: Using the event-crawler persona, find upcoming public events in the Düsseldorf
region this month. Try these URLs in order:
1. https://www.visitduesseldorf.de/erleben/veranstaltungen/veranstaltungskalender#/event
2. https://rausgegangen.de/duesseldorf/
Return the results as JSON matching the local_events_fallback.json schema.
If both crawls fail, load lab6/data/local_events_fallback.json instead.
```

Both subagents run simultaneously. EDA cells return first (~60 sec), event list follows.

---

### Act 3 — Run EDA + highlight STR-C (5 min)

Paste the generated cells. Run all. Expected results:

- Cell 1: Horizontal bar chart — Dairy and Produce highest volume
- Cell 2: Line chart — Beer/Spirits trend over 12 weeks
- Cell 3: Bar chart — **STR-C clearly highest stockout rate** (facilitator highlight)
- Cell 4: Reorder alert DataFrame (60–80 rows), `reorder_alerts.xlsx` created

**Facilitator call-out:** Point to the STR-C bar. *"This store has a supply problem.
How many weeks would it have taken to notice this in a spreadsheet?"*

---

### Act 4 — Join the external CSVs (12 min)

**Copy-paste prompt:**

```
Now load two more data files and join them onto the inventory DataFrame:

1. Load data/supplier_prices.csv — this is our supplier contract price list.
   Join it onto the inventory data on 'sku'.
2. Load data/promo_calendar.csv — this is our promotional calendar with discount %.
   Join it onto the inventory data on 'sku' and 'week'.

After joining:
- Show me which SKUs have a price mismatch: the supplier's current contract price
  is higher than what we have recorded in our inventory system.
  Show the gap in EUR and %, sorted highest gap first.
- Recalculate gross margin using the contract price and the actual promo discount.
  Show average effective margin % per category.
```

Bob loads both CSVs, performs the joins, and surfaces the price mismatches.
Expected: 6 SKUs with price gaps. HBC and Beer/Spirits will show the largest absolute gaps.

**Discussion point:** *"Our inventory system shows a cost of €X for this SKU.
The supplier's current contract says €Y. That gap is hidden in every reorder we place.
Bob found it in 30 seconds."*

---

## Stage 3 — Events as a Demand Signal (~30 min)

**Goal:** The event list from Stage 2 feeds a demand-boost model. Bob writes the logic
from a spoken business rule. Live web crawl of `visitduesseldorf.de` (with one backup).

### Setup (3 min)

Show the event JSON output from Stage 2 (or the fallback file contents in the notebook).
Point out the structure: `name`, `expected_attendance`, `category_boosts`.

> *"This is the bridge between the internet and your spreadsheet. No ETL pipeline,
> no integration project — just Bob and a prompt."*

---

### Act 1 — State the business rule (5 min)

**Copy-paste prompt:**

```
I have a list of upcoming local events, each with expected_attendance and
a list of category_boosts (grocery categories affected by the event).

Write a boost_events(events, df) function that:
- Takes the events JSON list and the inventory DataFrame
- Filters the DataFrame to the most recent week only
- For each event, identifies SKUs in the affected categories
- Applies a boost multiplier to their reorder quantities:
    attendance < 10,000  → 1.0× (no change)
    attendance 10–24,999 → 1.5×
    attendance 25–49,999 → 2.0×
    attendance >= 50,000  → 2.5×
- Returns a DataFrame sorted by boost magnitude (highest first)
- Columns: sku, product_name, category, event_name, attendance, multiplier, boosted_reorder_qty
```

Paste into the **boost_events() function** cell.

---

### Act 2 — Live event crawl (10 min)

**Copy-paste prompt:**

```
Using the event-crawler persona and the MCP fetch tool,
try these URLs in order until one returns usable event data:
1. https://www.visitduesseldorf.de/erleben/veranstaltungen/veranstaltungskalender#/event
2. https://rausgegangen.de/duesseldorf/
Extract upcoming events, estimate attendance, map to our grocery categories,
and return as JSON matching local_events_fallback.json schema.
```

**If wifi is reliable:** Bob fetches one of the URLs live and returns structured JSON.
Show the raw page content Bob retrieved, then the structured output — this is the
"data layer" moment.

**If all crawls fail or return nothing useful:**

```
The crawls didn't return useful data. Load lab6/data/local_events_fallback.json
and use that as our events list.
```

---

### Act 3 — Run the boost model (10 min)

Paste the `boost_events()` function and the call cell into the notebook. Run it.

Expected output: table with Fortuna Düsseldorf match (55,000 attendance, 2.5×) and
Rheinkirmes (50,000 attendance, 2.5×) at the top, Beer/Spirits SKUs
flagged across both events.

**Facilitator question to the room:**
> *"The Rheinkirmes shows 50,000 expected attendance. That's a 2.5× multiplier
> on Beer/Spirits reorder quantities. Would this have appeared on anyone's radar before
> the week it happened?"* Pause for discussion.

---

### Act 4 — Bob documents (2 min)

**Copy-paste prompt:**

```
Add a markdown cell above the boost_events function that explains in plain language
— for a non-technical store manager — what this model does, what the input data is,
and when to run it before placing a weekly order.
```

Bob writes the explanation cell. Read it aloud. It should be fully plain language,
no code references.

---

## Stage 4 — SQLite Database & Financial Summary (~30 min)

**Goal:** Everything we've loaded and analysed goes into a proper database. Bob creates
the schema, loads the three tables, and translates plain-English business questions into
SQL queries. The stage closes with a 4-tab financial workbook and a CFO email.

### Setup (2 min)

Confirm the notebook is running cleanly. `df_enriched`, `supplier_df`, and `promo_df`
must all be in memory from Stage 2.

---

### Act 1 — Create the database (8 min)

**Copy-paste prompt:**

```
Create an SQLite database called inventory.db in the current directory.
Load three tables into it:
- inventory: the full enriched inventory DataFrame (df_enriched)
- supplier_prices: the supplier price list
- promo_calendar: the promotional calendar

After loading, print the row count for each table to confirm it worked.
```

Bob writes the `sqlite3.connect()` and `to_sql()` code. Run it.
Expected output: `inventory: 3,000 rows`, `supplier_prices: 50 rows`, `promo_calendar: ~78 rows`.

**Facilitator point:** *"Three separate files. Now one database. Query it like any SQL system."*

---

### Act 2 — Ask business questions in plain English (12 min)

**Copy-paste prompt 1:**

```
Using pd.read_sql() against inventory.db, write a SQL query that answers:
"Which suppliers have raised their contract price above what's in our inventory system?
Show the SKU, supplier name, both prices, the gap in EUR, and the gap as a percentage.
Sort by largest gap first."
```

**Copy-paste prompt 2:**

```
Now write a SQL query that answers:
"Which promotion types generate the most units sold on average?
Join the promo_calendar and inventory tables on sku and week.
Exclude promos with discount_pct = 0 (data entry errors).
Show promo_type, number of promo weeks, average units sold, average discount %."
```

Both queries run via `pd.read_sql()`. Results display as DataFrames in the notebook.

**Discussion point on query 2:** *"Four promos in our data have discount_pct = 0 — that's
a data entry error in the promo_calendar.csv. Bob filtered them out automatically because
we told it to. What would have happened to those rows in an Excel VLOOKUP?"*

---

### Act 3 — KPIs and financial export (10 min)

**Copy-paste prompt:**

```
Calculate these KPIs using the enriched data (use contract prices, not stale inventory costs,
and account for promo discounts in the margin calculation):

1. Total inventory value (stock_level × contract_price_eur, latest week)
2. Average effective gross margin % per category
3. Number of SKUs at stockout risk (latest week)
4. Estimated revenue at risk (zero-stock SKUs × avg weekly units_sold × sell_price_eur)
5. Supplier price gap exposure: for SKUs with price mismatches, sum of (units_to_order × gap_eur)

Then export to financial_summary.xlsx with 4 tabs:
Tab 1 — KPI Dashboard
Tab 2 — Reorder Cost Projection (using contract prices)
Tab 3 — Margin Analysis by category (effective margins after promo discounts)
Tab 4 — Supplier Price Gaps (the action list for the buying team)
```

Run the cell. Open `financial_summary.xlsx`. Point to the **Supplier Price Gaps** tab.

**Closing discussion:** *"This tab didn't exist before this workshop. It's the hidden cost
in every reorder your buying team places. Bob surfaced it from two CSV files in 90 minutes.
What would you do with this list on Monday morning?"*

---

## Facilitator Tips

### If wifi fails during Stage 3
Use the fallback file directly:
```
Load lab6/data/local_events_fallback.json as the events data and proceed.
```
The fallback has 8 Düsseldorf-area events covering all major categories and attendance tiers.

### If Bob generates wrong column names
Bob reads the file before generating code (Rule 1 of the custom mode), so this should not
happen. If it does, ask:
```
You used column name X but the actual column is Y. Please correct the code.
```

### If the notebook kernel crashes
Restart the kernel, re-run the Imports cell, then re-run the Load Data cell.
All subsequent cells depend on the `df` DataFrame being loaded.

### If a generated cell throws an error
Paste the error back to Bob:
```
Running that cell gave this error: [paste error here]
Please fix it.
```

### If Stage 3 or 4 runs long
Stage 3 Act 4 (Bob documents) can be skipped to save 2 min.
Stage 4 Act 3 (financial export) can be demo'd without participants doing it themselves.
The non-negotiable payoff moments are: data quality audit (Stage 1), CSV price mismatch
(Stage 2 Act 4), STR-C outlier chart (Stage 2 Act 3), Volksfest boost table (Stage 3 Act 3),
and the Supplier Price Gaps tab (Stage 4 Act 3).

---

## Dataset Reference

**File:** `data/grocery_inventory.xlsx` (sheet: Inventory)  
**Rows:** 3,000 | **SKUs:** 50 | **Stores:** 5 (STR-A to STR-E) | **Weeks:** 12

| Column | Type | Description |
|---|---|---|
| sku | string | Product identifier, e.g. BEER-001 |
| product_name | string | German product name |
| category | string | Beer/Spirits, Produce, Dairy, Bakery, Frozen, HBC |
| store_id | string | STR-A through STR-E |
| week | date | Monday of the reporting week (ISO format) |
| units_sold | int | Weekly units sold at that store |
| stock_level | int | End-of-week stock on hand |
| reorder_threshold | int | Reorder trigger level |
| supplier_lead_days | int | Days until replenishment arrives |
| unit_cost_eur | float | Wholesale cost per unit (EUR) |
| sell_price_eur | float | Retail price per unit (EUR) |
| on_promotion | bool | True if item was on promo that week |

### Seeded data quality issues — grocery_inventory.xlsx (for facilitator reference)

| Issue | Count | Description |
|---|---|---|
| Negative stock | 5 rows | Values: -1, -3, -5, -7, -12 — data entry errors |
| Below reorder threshold | ~73 rows | Stock < threshold, no alert raised |
| Promo with zero sales | 3 rows | on_promotion=True, units_sold=0 — suspicious |
| Missing sell price | 2 rows | sell_price_eur is NaN |

**STR-C outlier:** Store C has a 1.4× demand boost in data generation → consistently
higher stockout rates. Visibly apparent in the store comparison bar chart in Stage 2.

**Beer/Spirits seasonality:** Dataset covers September–November 2026. Autumn window —
no strong summer spike visible, but Volksfest event (50,000 attendance) demonstrates
the event demand concept clearly.

### supplier_prices.csv (50 rows — one per SKU)

| Column | Description |
|---|---|
| sku | Product identifier |
| supplier_name | Supplier company name (6 suppliers, one per category) |
| contract_price_eur | Current contract price from supplier |
| inventory_cost_eur | Price recorded in inventory system |
| price_mismatch | True if contract price > inventory price |
| min_order_qty | Minimum units per order |
| contract_valid_until | Contract expiry date |

**Seeded issue:** 6 SKUs have `price_mismatch = True` — the supplier raised prices 5–18%
but the inventory system wasn't updated. These are the hidden reorder cost underestimates
Bob surfaces in Stage 2 Act 4.

### promo_calendar.csv (~78 rows — SKU × week entries where promo ran)

| Column | Description |
|---|---|
| sku | Product identifier |
| week | ISO date of the promo week |
| promo_type | One of: 2-for-1, Loyalty Card, Weekend Special, Clearance, New Listing |
| discount_pct | Discount percentage applied |
| approved_by | Who approved the promo: regional_mgr / category_mgr / auto |

**Seeded issue:** 4 rows have `discount_pct = 0` — a promo was entered but the discount
was never filled in. Bob's SQL query in Stage 4 filters these out explicitly, which is
itself a teaching moment about data entry discipline.

---

## Düsseldorf Event URLs (Stage 3)

| URL | Use |
|---|---|
| `https://www.visitduesseldorf.de/erleben/veranstaltungen/veranstaltungskalender#/event` | Primary live crawl target |
| `https://rausgegangen.de/duesseldorf/` | Backup |
| `lab6/data/local_events_fallback.json` | Offline fallback — always works |

**Fallback events included:**

| Event | Attendance | Category boosts |
|---|---|---|
| Fortuna Düsseldorf vs FC Köln | 55,000 | Beer/Spirits, HBC |
| Rheinkirmes | 50,000 | Beer/Spirits, Bakery, Produce |
| Karneval Düsseldorf | 40,000 | Beer/Spirits, Bakery |
| Düsseldorfer Weihnachtsmarkt | 30,000 | Beer/Spirits, Bakery |
| Düsseldorfer Weinfest | 20,000 | Beer/Spirits, Produce |
| Düsseldorf Marathon | 15,000 | Produce, Dairy, HBC |
| Tonhalle Konzert | 10,000 | Beer/Spirits, HBC |
| Oberhausen Weihnachtsmarkt | 8,000 | Bakery, Dairy |

---

## Solution Reference

A fully completed reference notebook is at `notebooks/solution.ipynb`.  
**Keep this file for the facilitator only** — do not share with participants before the lab.

To regenerate the source dataset at any time:

```bash
python lab6/data/generate_data.py
```
