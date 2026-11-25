# Lab 6 — Grocery Analytics with Bob — Session Summary

## What was assessed

| File / Component | Finding |
|---|---|
| `lab6/` directory structure | Built from scratch — no prior Lab 6 existed |
| Lab 5 Java service | Confirmed out of scope — Lab 6 is fully standalone |
| Stuttgart vs Düsseldorf region | All materials initially generated with Stuttgart context; full rebrand to Düsseldorf / NRW completed in second session |
| `lab6/data/supplier_prices.csv` | Supplier `TK-Logistik Stuttgart` identified as city-branded — renamed to `TK-Logistik Rheinland` |
| `lab6/notebooks/starter.ipynb` | One Stuttgart URL in a Stage 3 prompt hint — corrected |
| `lab6/data/local_events_fallback.json` | Originally contained Stuttgart events; regenerated with 8 Düsseldorf/NRW events |

---

## What was changed

### Region rebrand (Stuttgart → Düsseldorf / NRW)

| File | What changed |
|---|---|
| `.bob/personas/event-crawler.md` | Crawl targets replaced: 3 Stuttgart URLs → 2 Düsseldorf URLs; constraint text updated ("three" → "both") |
| `.bob/skills/grocery-analytics/SKILL.md` | Seasonal event examples updated: Volksfest/matchdays → Rheinkirmes/Fortuna matchdays |
| `lab6/README.md` | 20 Stuttgart references replaced: URL table, event table, Stage 2 subagent prompt, Stage 3 crawl prompt, Act 3 expected output, facilitator tips, section heading |
| `lab6/demo-deck/README.md` | Slide 9 crawler diagram, Slide 12 headline + timeline, Slide 14 live crawl URL, Stage 4 "optional" label removed |
| `lab6-plan.md` | Region context line, live crawl URL list, fallback JSON sample block, all stage flow descriptions, todo list items |
| `lab6/notebooks/starter.ipynb` | Stage 3 prompt hint updated to Düsseldorf primary crawl URL |
| `lab6/data/generate_data.py` | `TK-Logistik Stuttgart` → `TK-Logistik Rheinland` in supplier name map |
| `lab6/data/supplier_prices.csv` | Regenerated from updated generator — supplier name corrected, all 4 seeded data quality issues preserved |
| `lab6/data/local_events_fallback.json` | Regenerated: 8 Düsseldorf events (Rheinkirmes, Fortuna match, Karneval, Weihnachtsmarkt, Weinfest, Marathon, Tonhalle Konzert, Oberhausen Weihnachtsmarkt) |

### New files created (full Lab 6 build)

| File | Purpose |
|---|---|
| `lab6/data/grocery_inventory.xlsx` | 3,000-row mock inventory — 50 SKUs, 5 stores, 12 weeks, 4 seeded data quality issues |
| `lab6/data/grocery_inventory.csv` | CSV export of the same dataset |
| `lab6/data/supplier_prices.csv` | 50 rows — one per SKU, 6 price-mismatch rows for Stage 2 join exercise |
| `lab6/data/promo_calendar.csv` | ~78 rows — SKU × week promo entries, 4 zero-discount rows as data quality trap |
| `lab6/data/generate_data.py` | Reproducible data generator — re-run to reset all source files |
| `lab6/requirements.txt` | Python dependencies: pandas, openpyxl, matplotlib, notebook |
| `lab6/notebooks/starter.ipynb` | Participant notebook — 4-stage stubs with copy-paste prompt hints |
| `lab6/notebooks/solution.ipynb` | Fully working reference notebook — facilitator only, executes end-to-end cleanly |
| `.bob/custom_modes.yaml` | 📊 Data Analyst Architect custom mode — 7 rules including read-before-code and explain-every-cell |
| `.bob/skills/grocery-analytics/SKILL.md` | Full analytics playbook: column reference, reorder formula, boost multipliers, CSV join patterns, SQLite patterns, KPI reference |
| `.bob/personas/eda-analyst.md` | EDA subagent persona — generates 6-cell notebook from plain-English brief |
| `.bob/personas/event-crawler.md` | Event crawler subagent — crawls Düsseldorf URLs, returns structured JSON |
| `.bob/mcp.json` | MCP fetch server config for Stage 3 live crawl |
| `.bob/settings.json` | Hooks: data quality gate on file writes + command log |
| `.bob/hooks/check-data-quality.sh` | Pre-write hook — checks for negative stock and missing prices |
| `.bob/hooks/log-commands.sh` | Logs all Bob-generated shell commands to `hooks/command-log.txt` |
| `lab6/README.md` | Full facilitator guide — stage-by-stage script, copy-paste prompts, fallback tips, dataset reference |
| `lab6/demo-deck/README.md` | 19-slide deck outline with timing, talking points, and facilitator notes |
| `lab6-plan.md` | Planning document — design decisions, stage breakdown, todo lists |

---

## Tests added

None. This is a workshop lab (not a software project). The solution notebook (`notebooks/solution.ipynb`) serves as the functional validation — it executes end-to-end cleanly against the generated dataset.

---

## Infrastructure added

| Item | Detail |
|---|---|
| `.bob/mcp.json` | Registers the MCP fetch server so Bob can crawl live event URLs in Stage 3 |
| `.bob/settings.json` | Pre-write hook (`check-data-quality.sh`) and command-log hook (`log-commands.sh`) |
| `.bob/custom_modes.yaml` | Custom Bob mode scoped to the lab6 directory |
| `lab6/data/generate_data.py` | Standalone data generator — reproducible dataset reset at any time via `python lab6/data/generate_data.py` |

---

## Security improvements

None applicable — this is a mock dataset workshop. No real credentials or secrets are present in Lab 6 materials.

---

## What's left to do

- [ ] Test the live crawl URLs against the actual Düsseldorf event sites before the workshop to confirm MCP fetch can parse their HTML structure
- [ ] Verify `solution.ipynb` Stage 3 runs cleanly with the Düsseldorf fallback events (boost output references were updated but notebook execution against new event names was not re-verified)
- [ ] Consider translating the CFO email draft prompt (Stage 4) into German for the Düsseldorf audience
- [ ] Print Slides 2 and 15 of the demo deck as a one-page participant handout before the workshop
- [ ] Confirm Python environment with `pip install -r lab6/requirements.txt` on the demo machine ahead of time
