# Lab 6 — Demo Deck Outline

This directory is for the facilitator slide deck. Below is the full slide-by-slide
outline for a ~2-hour workshop delivery.

---

## Slide Structure

### Cover
**Title:** Grocery Inventory Analytics with Bob  
**Sub:** Bobathon Workshop — AI-Assisted Data Analysis  
**Visual:** Bob icon + grocery shelf or inventory spreadsheet image

---

### Slide 1 — The Problem (1 min)
**Headline:** "You have the data. It's in Excel. It's not telling you anything."

- Controllers spend hours reformatting, filtering, manually checking thresholds
- No automatic reorder alerts across all stores
- Event spikes (Volksfest, Weihnachtsmarkt, matchdays) cause reactive stockouts
- Financial summaries are copy-pasted by hand

**Transition:** "In this lab, Bob is your analyst. You bring the business knowledge, Bob brings the code."

---

### Slide 2 — What We'll Build Today (1 min)
**Headline:** "From raw Excel to actionable insight — in plain English"

Four outcomes shown as a pipeline:

```
grocery_inventory.xlsx
      ↓
Stage 1: Data Quality Audit
      ↓
Stage 2: EDA + Reorder Alerts (reorder_alerts.xlsx)
      ↓
Stage 3: Event Demand Model (boost_events)
      ↓
Stage 4: Financial Summary (financial_summary.xlsx + CFO email)
```

---

### Slide 3 — Bob Setup (2 min)
**Headline:** "One custom mode. Seven rules. No configuration needed."

- Show the 📊 Data Analyst Architect mode loading
- Call out Rule 1: "Bob reads the file before writing any code"
- Call out Rule 4: "Every code cell gets a plain-language explanation"
- **Demo step:** Open Bob, confirm mode is active

---

### Slide 4 — Stage 1: Excel Meets Bob (title slide)
**Visual:** Excel file icon → Bob → pandas DataFrame  
Duration callout: **~30 min**

---

### Slide 5 — Stage 1 in action
**Split screen layout:**

Left: Bob prompt  
Right: Bob output (column-by-column description)

Talking point: *"Bob didn't need to be told what columns exist. It read the file."*

---

### Slide 6 — Stage 1: Data Quality Report
**Show the 4 issue categories:**

| Issue | Count | Business impact |
|---|---|---|
| Negative stock | 5 rows | Invalid — masks true stockout risk |
| Below reorder threshold | ~73 rows | Needs immediate reorder |
| Promo with zero sales | 3 rows | Process failure or delisting error |
| Missing sell price | 2 rows | Cannot calculate margin |

Talking point: *"Finding these manually in a 3,000-row spreadsheet: how long?"*

---

### Slide 7 — Stage 2: Notebook Generation (title slide)
**Visual:** Plain English brief → 6 notebook cells + 2 charts  
Duration callout: **~30 min**

---

### Slide 8 — The Analyst Brief
**Show the brief text on screen** (copy from README Stage 2 Act 1)

Talking point: *"This is a job spec for an analyst, written in plain language.
The quality of the output tracks the quality of the brief."*

---

### Slide 9 — Parallel Subagents
**Visual:** Two streams side by side

```
Bob spawns:                     Bob spawns:
┌─────────────────┐             ┌─────────────────────┐
│  EDA Analyst    │             │  Event Crawler      │
│                 │             │                     │
│  Generating 6   │             │  Crawling           │
│  notebook cells │             │  visitduesseldorf.de│
└─────────────────┘             └─────────────────────┘
         ↓                               ↓
   EDA cells ready              Events JSON returned
```

Talking point: *"Two tasks, running at the same time. This is what makes Bob different
from a chatbot."*

---

### Slide 10 — STR-C Outlier (key insight)
**Show the store comparison bar chart**

Highlight STR-C in red.

Talking point: *"One chart, generated from a plain-English prompt, identified a
store with a systematic supply problem. How is STR-C being managed right now?"*

Leave a 30-second pause for the room to react.

---

### Slide 11 — Stage 3: Events as a Demand Signal (title slide)
**Visual:** Calendar event icon + grocery shelf + multiplier arrow  
Duration callout: **~30 min**

---

### Slide 12 — The Concept
**Headline:** "Your spreadsheet doesn't know about Rheinkirmes"

Timeline visual:
```
4 weeks out:  Rheinkirmes announced (50,000 expected)
3 weeks out:  ← This is when you need to adjust your Beer order
2 weeks out:  Supplier lead time window begins
1 week out:   Too late to add stock
Event week:   Shelves empty. Competitor across the street isn't.
```

---

### Slide 13 — The Boost Model
**Show the multiplier table:**

| Attendance | Multiplier |
|---|---|
| < 10,000 | 1.0× |
| 10,000–24,999 | 1.5× |
| 25,000–49,999 | 2.0× |
| ≥ 50,000 | 2.5× |

*"You stated the rule in plain English. Bob encoded it. The model is yours to adjust."*

---

### Slide 14 — Live Crawl Moment
**Headline:** "Bob reads the web so you don't have to"

Show: MCP fetch crawling `visitduesseldorf.de` (falling through to rausgegangen.de if needed)
Show: Raw HTML → structured JSON in one step

Talking point: *"No integration project. No API key. No IT ticket. Just a prompt."*

---

### Slide 15 — Stage 4: Financial Summary (title slide)
**Visual:** 3-tab Excel workbook + email icon  
Duration callout: **~15 min (optional)**

---

### Slide 16 — The CFO Email
**Show the generated email text**

Talking point: *"This started as a 3,000-row Excel file. Forty-five minutes later,
Bob drafted the email to your CFO. How does that change your Monday morning?"*

---

### Slide 17 — What You Built Today
**Headline:** "Four outputs. Zero manual copy-paste."

| Output | Generated in |
|---|---|
| `reorder_alerts.xlsx` | Stage 2 |
| `boost_events()` demand model | Stage 3 |
| `financial_summary.xlsx` (3 tabs) | Stage 4 |
| CFO email draft | Stage 4 |

---

### Slide 18 — What's Next?
**Headline:** "Where do you take this tomorrow?"

- Connect to your real data source (ERP export, SAP CSV, live database)
- Schedule the notebook to run weekly (via cron or simple automation)
- Add more event sources (social media, weather, local news)
- Build a Streamlit dashboard from the notebook output
- Ask Bob to do any of these — in plain English

---

### Slide 19 — Q&A / Freestyle
**Headline:** "Your data. Your questions."

Suggested freestyle prompts (shown on screen):
- *"Which category has the worst margin per unit across all stores?"*
- *"Show me a chart of STR-C vs STR-A head to head over all weeks"*
- *"Write code to send an email alert when any SKU drops below reorder threshold"*
- *"Translate the CFO email into German"*
- *"What would happen to our Beer margin if we raised prices by 10%?"*

---

## Timing Reference

| Segment | Duration |
|---|---|
| Intro + setup (Slides 1–3) | 5 min |
| Stage 1 (Slides 4–6) | 30 min |
| Stage 2 (Slides 7–10) | 30 min |
| Stage 3 (Slides 11–14) | 30 min |
| Stage 4 (Slides 15–16) | 15 min |
| Wrap-up + Q&A (Slides 17–19) | 10 min |
| **Total** | **~2 hours** |

---

## Facilitator Notes for the Deck

- Keep slide transitions instant — no animations that slow down live demos
- Slides 5, 8, 14, 16 are "show Bob's screen" slides — the deck stays in background
- Print Slides 2 and 15 as a one-page handout for participants
- The freestyle prompts on Slide 19 are designed to work with the loaded data —
  each has been tested against the solution notebook
