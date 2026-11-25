---
name: grocery-analytics
description: >
  Retail grocery inventory analytics playbook for Bob. Activate when analysing inventory
  data, checking data quality, generating reorder alerts, building demand forecasts, running
  EDA on grocery datasets, joining supplier or promo CSV files, loading data into SQLite,
  or exporting results to Excel.
  Trigger phrases: "analyse inventory", "check data quality", "reorder alert",
  "demand forecast", "event boost", "stock report", "export to Excel", "EDA",
  "weekly trend", "margin analysis", "stockout risk", "boost model",
  "join supplier", "promo calendar", "SQLite", "SQL query", "database", "load to database".
---

# Grocery Analytics Playbook

## 1. Category Taxonomy

| Category     | Typical SKU prefix | Velocity  | Margin profile |
|---|---|---|---|
| Beer/Spirits | BEER-              | Medium    | Medium         |
| Produce      | PROD-              | High      | Low            |
| Dairy        | DAIR-              | High      | Low–Medium     |
| Bakery       | BAKE-              | High      | Medium         |
| Frozen       | FROZ-              | Medium    | Medium–High    |
| HBC          | HBC-               | Low       | High           |

Beer/Spirits shows strong seasonal uplift — expect 40–60% higher sales in summer weeks
and around major local events (Rheinkirmes, Weihnachtsmarkt, Fortuna matchdays).

---

## 2. Standard Column Reference

| Column              | Type    | Notes                                          |
|---|---|---|
| sku                 | string  | Unique product identifier, e.g. BEER-001       |
| product_name        | string  | Human-readable product name in German          |
| category            | string  | One of the 6 categories above                  |
| store_id            | string  | STR-A through STR-E                            |
| week                | date    | ISO date string, Monday of the reporting week  |
| units_sold          | int     | Total units sold that week at that store       |
| stock_level         | int     | End-of-week stock on hand (should be ≥ 0)     |
| reorder_threshold   | int     | Trigger a replenishment order below this value |
| supplier_lead_days  | int     | Days between order and delivery                |
| unit_cost_eur       | float   | Wholesale cost per unit (EUR)                  |
| sell_price_eur      | float   | Retail sell price per unit (EUR, may be NaN)   |
| on_promotion        | bool    | True if item was on promotional price that week|

---

## 3. Data Quality Checklist

Run these checks before any analysis:

```python
# Negative stock (data entry error)
neg_stock = df[df["stock_level"] < 0]

# Below reorder threshold (needs restocking)
below_threshold = df[df["stock_level"] < df["reorder_threshold"]]

# Promo with zero sales (suspicious — possible data entry or delisting)
promo_zero = df[(df["on_promotion"] == True) & (df["units_sold"] == 0)]

# Missing sell price
missing_price = df[df["sell_price_eur"].isna()]
```

---

## 4. Reorder Alert Formula

An item requires a reorder alert when ALL of these are true:
- `stock_level < reorder_threshold`
- `supplier_lead_days > 0` (i.e. not an instant-replenishment item)
- `stock_level >= 0` (exclude data entry errors from alert queue)

```python
reorder_alerts = df[
    (df["stock_level"] < df["reorder_threshold"]) &
    (df["supplier_lead_days"] > 0) &
    (df["stock_level"] >= 0)
][["sku", "product_name", "category", "store_id", "week",
   "stock_level", "reorder_threshold", "supplier_lead_days"]].copy()

reorder_alerts["units_to_order"] = (
    reorder_alerts["reorder_threshold"] - reorder_alerts["stock_level"]
) * 2  # order double the gap as a safety buffer
```

---

## 5. Demand Boost Multipliers (Event Model)

| Expected attendance | Boost multiplier |
|---|---|
| < 10,000            | 1.0× (no boost) |
| 10,000 – 24,999     | 1.5×            |
| 25,000 – 49,999     | 2.0×            |
| ≥ 50,000            | 2.5×            |

Apply only to SKUs whose `category` appears in the event's `category_boosts` list.
Use the most recent week's stock data as the base for boost calculations.

---

## 6. Excel Export Pattern (Multi-Tab)

Always use `pd.ExcelWriter` with `engine="openpyxl"` for multi-tab exports.
Never use `df.to_excel(path)` directly when writing multiple sheets.

```python
with pd.ExcelWriter("output_file.xlsx", engine="openpyxl") as writer:
    df_tab1.to_excel(writer, sheet_name="Tab 1 Name", index=False)
    df_tab2.to_excel(writer, sheet_name="Tab 2 Name", index=False)
    df_tab3.to_excel(writer, sheet_name="Tab 3 Name", index=False)
```

Output files go to the working directory (never overwrite the source `lab6/data/` files).

---

## 7. Preferred Chart Types

| Analysis type         | Chart type        | pandas/matplotlib call            |
|---|---|---|
| Sales by category     | Horizontal bar    | `df.plot(kind="barh")`            |
| Weekly trend          | Line              | `df.plot(kind="line")`            |
| Store comparison      | Grouped bar       | `df.pivot().plot(kind="bar")`     |
| Margin distribution   | Scatter           | `ax.scatter(x, y)`                |
| Stockout risk count   | Vertical bar      | `df.plot(kind="bar")`             |
| Event boost impact    | Stacked bar       | `df.plot(kind="bar", stacked=True)`|

Always call `plt.tight_layout()` before `plt.show()` or `plt.savefig()`.
Always label axes and add a descriptive title.

---

## 8. CSV Join Patterns (Stage 2)

### supplier_prices.csv columns
`sku`, `product_name`, `category`, `supplier_name`, `contract_price_eur`,
`inventory_cost_eur`, `price_mismatch` (bool), `min_order_qty`, `contract_valid_until`

### promo_calendar.csv columns
`sku`, `product_name`, `category`, `week`, `promo_type`, `discount_pct`, `approved_by`

### Standard join pattern

```python
supplier_df = pd.read_csv("../data/supplier_prices.csv")
promo_df    = pd.read_csv("../data/promo_calendar.csv", parse_dates=["week"])

# Join supplier prices onto inventory (SKU-level, left join keeps all inventory rows)
df_enriched = df.merge(
    supplier_df[["sku", "supplier_name", "contract_price_eur", "price_mismatch", "min_order_qty"]],
    on="sku", how="left"
)

# Join promo calendar (SKU + week level)
df_enriched = df_enriched.merge(
    promo_df[["sku", "week", "promo_type", "discount_pct"]],
    on=["sku", "week"], how="left"
)
```

### Price mismatch check (supplier vs inventory)

```python
mismatches = supplier_df[supplier_df["price_mismatch"] == True][
    ["sku", "product_name", "supplier_name", "contract_price_eur", "inventory_cost_eur"]
].copy()
mismatches["gap_eur"]  = (mismatches["contract_price_eur"] - mismatches["inventory_cost_eur"]).round(2)
mismatches["gap_pct"]  = ((mismatches["gap_eur"] / mismatches["inventory_cost_eur"]) * 100).round(1)
```

### Effective margin with promo discount

```python
df_enriched["effective_sell_price"] = df_enriched["sell_price_eur"] * (
    1 - df_enriched["discount_pct"].fillna(0) / 100
)
df_enriched["effective_margin_eur"] = (
    df_enriched["effective_sell_price"] - df_enriched["contract_price_eur"]
)
```

---

## 9. SQLite Database Pattern (Stage 4)

### Schema: 3 tables

| Table             | Source file                  | Key columns         |
|---|---|---|
| inventory         | grocery_inventory.xlsx       | sku, store_id, week |
| supplier_prices   | supplier_prices.csv          | sku                 |
| promo_calendar    | promo_calendar.csv           | sku, week           |

### Create and load

```python
import sqlite3

conn = sqlite3.connect("inventory.db")

df.to_sql("inventory",       conn, if_exists="replace", index=False)
supplier_df.to_sql("supplier_prices", conn, if_exists="replace", index=False)
promo_df.to_sql("promo_calendar",     conn, if_exists="replace", index=False)

conn.close()
print("✅ inventory.db created with 3 tables")
```

### Query pattern (plain-English → SQL → pandas)

```python
conn = sqlite3.connect("inventory.db")

query = """
    SELECT i.sku, i.product_name, i.category,
           s.supplier_name, s.contract_price_eur, i.unit_cost_eur,
           ROUND(s.contract_price_eur - i.unit_cost_eur, 2) AS price_gap_eur
    FROM inventory i
    JOIN supplier_prices s ON i.sku = s.sku
    WHERE s.price_mismatch = 1
    GROUP BY i.sku
    ORDER BY price_gap_eur DESC
"""
result = pd.read_sql(query, conn)
conn.close()
```

Always close the connection after each query block.
Never run DELETE or DROP in a workshop setting — read-only queries only.

---

## 10. KPI Reference (Stage 4)

| KPI                        | Formula                                              |
|---|---|
| Total inventory value      | `sum(stock_level × contract_price_eur)`             |
| Gross margin %             | `(effective_sell_price - contract_price_eur) / effective_sell_price × 100` |
| SKUs at stockout risk      | Count where `stock_level < reorder_threshold` (latest week) |
| Revenue at risk            | `sum(units_sold_avg × sell_price_eur)` for zero-stock SKUs |
| Reorder cost projection    | `sum(units_to_order × contract_price_eur)`          |
| Supplier price exposure    | `sum(gap_eur × units_to_order)` for mismatched SKUs |
