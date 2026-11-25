"""
Lab 6 — Grocery Analytics with Bob
Dataset generator: produces grocery_inventory.xlsx, grocery_inventory.csv,
local_events_fallback.json, supplier_prices.csv, and promo_calendar.csv
for the Düsseldorf / North Rhine-Westphalia region.

Run once to (re-)create all data artifacts:
    python generate_data.py
"""

import json
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)

# ---------------------------------------------------------------------------
# 1. SKU catalogue
# ---------------------------------------------------------------------------

SKUS = [
    # Beer/Spirits (8 SKUs)
    ("BEER-001", "Pilsner Lager 500ml 6-pack",        "Beer/Spirits", 4.20,  5.99),
    ("BEER-002", "Weizenbier 500ml 6-pack",            "Beer/Spirits", 4.80,  6.49),
    ("BEER-003", "Alkoholfrei Lager 330ml 12-pack",    "Beer/Spirits", 6.50,  9.99),
    ("BEER-004", "Rotwein Dornfelder 0.75l",           "Beer/Spirits", 3.80,  6.49),
    ("BEER-005", "Weißwein Riesling 0.75l",            "Beer/Spirits", 4.20,  7.49),
    ("BEER-006", "Prosecco 0.75l",                     "Beer/Spirits", 4.90,  7.99),
    ("BEER-007", "Whisky Blend 0.7l",                  "Beer/Spirits", 14.50, 22.99),
    ("BEER-008", "Sekt Brut 0.75l",                    "Beer/Spirits", 3.90,  5.99),

    # Produce (12 SKUs)
    ("PROD-001", "Tomaten Rispentomaten 500g",          "Produce",      0.80,  1.49),
    ("PROD-002", "Kartoffeln festkochend 2.5kg",        "Produce",      1.20,  2.29),
    ("PROD-003", "Äpfel Elstar 1kg",                    "Produce",      1.10,  1.99),
    ("PROD-004", "Bananen 1kg",                         "Produce",      0.90,  1.59),
    ("PROD-005", "Gurken Salatgurke Stück",             "Produce",      0.40,  0.79),
    ("PROD-006", "Paprika Rot 3-Pack",                  "Produce",      1.30,  2.49),
    ("PROD-007", "Zwiebeln 1kg",                        "Produce",      0.60,  1.09),
    ("PROD-008", "Karotten 1kg",                        "Produce",      0.70,  1.29),
    ("PROD-009", "Salat Eisberg Kopf",                  "Produce",      0.50,  0.99),
    ("PROD-010", "Zucchini 500g",                       "Produce",      0.90,  1.69),
    ("PROD-011", "Erdbeeren 500g",                      "Produce",      1.80,  3.29),
    ("PROD-012", "Trauben kernlos 500g",                "Produce",      2.10,  3.79),

    # Dairy (10 SKUs)
    ("DAIR-001", "Vollmilch 3.5% 1L",                  "Dairy",        0.85,  1.29),
    ("DAIR-002", "Fettarme Milch 1.5% 1L",             "Dairy",        0.80,  1.19),
    ("DAIR-003", "Naturjoghurt 500g",                   "Dairy",        0.70,  1.09),
    ("DAIR-004", "Fruchtjoghurt Erdbeere 150g 4-Pack",  "Dairy",        1.20,  1.99),
    ("DAIR-005", "Gouda Scheiben 400g",                 "Dairy",        2.40,  3.79),
    ("DAIR-006", "Camembert 125g",                      "Dairy",        1.10,  1.89),
    ("DAIR-007", "Butter 250g",                         "Dairy",        1.80,  2.69),
    ("DAIR-008", "Sahne 200ml",                         "Dairy",        0.90,  1.49),
    ("DAIR-009", "Quark Magerquark 500g",               "Dairy",        0.80,  1.29),
    ("DAIR-010", "Mozzarella 125g",                     "Dairy",        0.95,  1.69),

    # Bakery (8 SKUs)
    ("BAKE-001", "Vollkornbrot 500g",                   "Bakery",       1.20,  2.19),
    ("BAKE-002", "Brötchen 6-Pack",                     "Bakery",       0.90,  1.49),
    ("BAKE-003", "Laugenbrezel groß Stück",             "Bakery",       0.50,  0.89),
    ("BAKE-004", "Toastbrot 750g",                      "Bakery",       0.95,  1.59),
    ("BAKE-005", "Croissant Butter 2-Pack",             "Bakery",       1.30,  2.29),
    ("BAKE-006", "Marmorkuchen 400g",                   "Bakery",       1.80,  3.19),
    ("BAKE-007", "Schwarzbrot 500g",                    "Bakery",       1.10,  1.99),
    ("BAKE-008", "Zimtschnecke 2-Pack",                 "Bakery",       1.60,  2.79),

    # Frozen (8 SKUs)
    ("FROZ-001", "Tiefkühlpizza Margherita 400g",       "Frozen",       1.80,  3.29),
    ("FROZ-002", "Pommes Frites 750g",                  "Frozen",       1.20,  2.19),
    ("FROZ-003", "Tiefkühlerbsen 450g",                 "Frozen",       0.90,  1.59),
    ("FROZ-004", "Schnitzel paniert 2-Pack",            "Frozen",       3.20,  5.49),
    ("FROZ-005", "Vanilleeis 500ml",                    "Frozen",       1.90,  3.49),
    ("FROZ-006", "Fischstäbchen 400g",                  "Frozen",       2.10,  3.79),
    ("FROZ-007", "Spinat gehackt 450g",                 "Frozen",       0.85,  1.49),
    ("FROZ-008", "Schokoladeneis Stieleis 6-Pack",      "Frozen",       2.40,  4.29),

    # HBC (4 SKUs — Health/Beauty/Cleaning)
    ("HBC-001",  "Waschmittel Flüssig 1.5L",            "HBC",          4.50,  7.99),
    ("HBC-002",  "Zahncreme 75ml",                       "HBC",          0.90,  1.79),
    ("HBC-003",  "Shampoo 300ml",                        "HBC",          1.80,  3.49),
    ("HBC-004",  "Duschgel 250ml",                       "HBC",          1.20,  2.29),
]

STORES = ["STR-A", "STR-B", "STR-C", "STR-D", "STR-E"]

# 12 weeks of history ending on a recent Monday
WEEK_END = date(2026, 11, 17)  # most recent Monday
WEEKS = [WEEK_END - timedelta(weeks=i) for i in reversed(range(12))]

# Reorder thresholds per category (units)
REORDER = {
    "Beer/Spirits": 30,
    "Produce":       40,
    "Dairy":         50,
    "Bakery":        35,
    "Frozen":        25,
    "HBC":           15,
}

# Supplier lead days per category
LEAD_DAYS = {
    "Beer/Spirits": 3,
    "Produce":       1,
    "Dairy":         2,
    "Bakery":        1,
    "Frozen":        5,
    "HBC":           7,
}

# Base weekly sales per category (avg units per SKU per store per week)
BASE_SALES = {
    "Beer/Spirits": 18,
    "Produce":       55,
    "Dairy":         60,
    "Bakery":        45,
    "Frozen":        22,
    "HBC":           8,
}

# Summer week indices (weeks 2–7 = mid-year) boost Beer/Spirits
SUMMER_WEEKS = {2, 3, 4, 5, 6, 7}

# STR-C stockout multiplier — this store undersells and overdraws stock
STR_C_DEMAND_BOOST = 1.4  # higher demand, same replenishment → more stockouts


def beer_seasonal(week_idx: int) -> float:
    """Return sales multiplier for Beer/Spirits based on week index."""
    if week_idx in SUMMER_WEEKS:
        return 1.6
    if week_idx in {0, 1, 8}:
        return 1.2  # mild spring / autumn
    return 1.0


rows = []

for sku, name, category, cost, price in SKUS:
    for store in STORES:
        stock = random.randint(60, 120)  # opening stock for first week
        for w_idx, week in enumerate(WEEKS):
            # --- base demand ---
            base = BASE_SALES[category]
            multiplier = 1.0
            if category == "Beer/Spirits":
                multiplier *= beer_seasonal(w_idx)
            if store == "STR-C":
                multiplier *= STR_C_DEMAND_BOOST
            on_promo = random.random() < 0.08  # 8% promo chance
            if on_promo:
                multiplier *= 1.3

            sold = max(0, int(random.gauss(base * multiplier, base * 0.2)))
            sold = min(sold, stock)  # can't sell more than stock

            end_stock = stock - sold
            reorder_qty = random.randint(40, 80)
            if end_stock < REORDER[category]:
                # Replenish (arrives next week — simulate by adding to next opening)
                end_stock += reorder_qty

            rows.append({
                "sku":                sku,
                "product_name":       name,
                "category":           category,
                "store_id":           store,
                "week":               week.isoformat(),
                "units_sold":         sold,
                "stock_level":        end_stock,
                "reorder_threshold":  REORDER[category],
                "supplier_lead_days": LEAD_DAYS[category],
                "unit_cost_eur":      cost,
                "sell_price_eur":     price,
                "on_promotion":       on_promo,
            })
            stock = end_stock  # carry forward


df = pd.DataFrame(rows)

# ---------------------------------------------------------------------------
# 2. Seed intentional data quality issues
# ---------------------------------------------------------------------------

# Issue A: ~5 rows with negative stock_level (data entry errors)
neg_idx = df.sample(5, random_state=1).index
df.loc[neg_idx, "stock_level"] = [-3, -7, -1, -12, -5]

# Issue B: ~8 rows where stock_level < reorder_threshold but we won't trigger an alert
# (already naturally occurs; just ensure some are present by forcing them)
low_idx = df[df["stock_level"] > df["reorder_threshold"]].sample(8, random_state=2).index
df.loc[low_idx, "stock_level"] = df.loc[low_idx, "reorder_threshold"] - random.randint(1, 10)

# Issue C: ~3 rows with units_sold = 0 AND on_promotion = True (suspicious)
promo_idx = df[df["on_promotion"] == True].sample(3, random_state=3).index
df.loc[promo_idx, "units_sold"] = 0

# Issue D: ~2 rows with missing sell_price_eur
null_idx = df.sample(2, random_state=4).index
df.loc[null_idx, "sell_price_eur"] = None

# ---------------------------------------------------------------------------
# 3. Write output files
# ---------------------------------------------------------------------------

out_dir = Path(__file__).parent
xlsx_path = out_dir / "grocery_inventory.xlsx"
csv_path  = out_dir / "grocery_inventory.csv"

# Sort for readability
df = df.sort_values(["category", "sku", "store_id", "week"]).reset_index(drop=True)

df.to_excel(xlsx_path, sheet_name="Inventory", index=False)
df.to_csv(csv_path, index=False)

print(f"✅  Written {len(df)} rows to:")
print(f"   {xlsx_path}")
print(f"   {csv_path}")
print(f"\nDataset shape: {df.shape}")
print(f"Categories:    {df['category'].unique().tolist()}")
print(f"Stores:        {df['store_id'].unique().tolist()}")
print(f"Weeks:         {df['week'].min()} → {df['week'].max()}")
print(f"\nSeeded issues:")
print(f"  Negative stock rows:              {(df['stock_level'] < 0).sum()}")
print(f"  Stock below reorder threshold:    {(df['stock_level'] < df['reorder_threshold']).sum()}")
print(f"  Promo with zero sales:            {((df['on_promotion']) & (df['units_sold'] == 0)).sum()}")
print(f"  Missing sell_price_eur:           {df['sell_price_eur'].isna().sum()}")

# ---------------------------------------------------------------------------
# 4. local_events_fallback.json
# ---------------------------------------------------------------------------

events = [
    {
        "date": "2026-11-29",
        "name": "Fortuna Düsseldorf vs Hamburger SV",
        "city": "Düsseldorf",
        "venue": "MERKUR SPIEL-ARENA",
        "expected_attendance": 55000,
        "category_boosts": ["Beer/Spirits", "HBC"]
    },
    {
        "date": "2026-07-11",
        "name": "Rheinkirmes Düsseldorf",
        "city": "Düsseldorf",
        "venue": "Oberkasseler Rheinwiesen",
        "expected_attendance": 50000,
        "category_boosts": ["Beer/Spirits", "Bakery", "Produce"]
    },
    {
        "date": "2026-02-14",
        "name": "Karneval Rosenmontagszug Düsseldorf",
        "city": "Düsseldorf",
        "venue": "Innenstadt Düsseldorf",
        "expected_attendance": 40000,
        "category_boosts": ["Beer/Spirits", "Bakery", "HBC"]
    },
    {
        "date": "2026-12-05",
        "name": "Düsseldorfer Weihnachtsmarkt",
        "city": "Düsseldorf",
        "venue": "Marktplatz Düsseldorf",
        "expected_attendance": 30000,
        "category_boosts": ["Beer/Spirits", "Bakery"]
    },
    {
        "date": "2026-08-22",
        "name": "Alt-Düsseldorf Weinfest",
        "city": "Düsseldorf",
        "venue": "Burgplatz Düsseldorf",
        "expected_attendance": 20000,
        "category_boosts": ["Beer/Spirits", "Produce"]
    },
    {
        "date": "2026-10-04",
        "name": "Düsseldorf Marathon",
        "city": "Düsseldorf",
        "venue": "Rheinuferpromenade",
        "expected_attendance": 15000,
        "category_boosts": ["Produce", "Dairy", "HBC"]
    },
    {
        "date": "2026-06-20",
        "name": "Open-Air Konzert Tonhalle",
        "city": "Düsseldorf",
        "venue": "Ehrenhof Düsseldorf",
        "expected_attendance": 10000,
        "category_boosts": ["Beer/Spirits", "HBC"]
    },
    {
        "date": "2026-12-19",
        "name": "Weihnachtsmarkt Oberhausen",
        "city": "Oberhausen",
        "venue": "Altmarkt Oberhausen",
        "expected_attendance": 8000,
        "category_boosts": ["Bakery", "Dairy"]
    }
]

events_path = out_dir / "local_events_fallback.json"
with open(events_path, "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print(f"\n✅  Written {len(events)} events to:")
print(f"   {events_path}")

# ---------------------------------------------------------------------------
# 5. supplier_prices.csv
# ---------------------------------------------------------------------------
# One row per SKU. Supplier contract prices deliberately diverge from the
# unit_cost_eur in the inventory data for ~15% of SKUs — a teaching moment:
# price changes from suppliers haven't been updated in the main system yet.

SUPPLIERS = {
    "Beer/Spirits": "Getränke Hoffmann GmbH",
    "Produce":       "Frischmarkt Bayern KG",
    "Dairy":         "Molkerei Allgäu AG",
    "Bakery":        "Bäckerei Zulieferer Süd",
    "Frozen":        "TK-Logistik Rheinland",
    "HBC":           "Drogeriehandel Nord GmbH",
}

supplier_rows = []
random.seed(99)
for sku, name, category, cost, price in SKUS:
    # ~15% of SKUs have a supplier price that differs from inventory unit_cost
    if random.random() < 0.15:
        # Supplier raised price by 5–18% but inventory not updated yet
        contract_price = round(cost * random.uniform(1.05, 1.18), 2)
        price_mismatch = True
    else:
        contract_price = cost
        price_mismatch = False

    supplier_rows.append({
        "sku":                  sku,
        "product_name":         name,
        "category":             category,
        "supplier_name":        SUPPLIERS[category],
        "contract_price_eur":   contract_price,
        "inventory_cost_eur":   cost,
        "price_mismatch":       price_mismatch,
        "min_order_qty":        random.choice([6, 12, 24, 48]),
        "contract_valid_until": "2027-03-31",
    })

supplier_df = pd.DataFrame(supplier_rows)
supplier_path = out_dir / "supplier_prices.csv"
supplier_df.to_csv(supplier_path, index=False)

mismatches = supplier_df["price_mismatch"].sum()
print(f"\n✅  Written {len(supplier_df)} rows to:")
print(f"   {supplier_path}")
print(f"   Price mismatches (supplier raised price, inventory not updated): {mismatches}")

# ---------------------------------------------------------------------------
# 6. promo_calendar.csv
# ---------------------------------------------------------------------------
# One row per SKU per week with richer promo metadata than the boolean
# on_promotion flag in the inventory data. ~12% of SKU-weeks are on promo.
# Intentional issue: 4 promos have discount_pct = 0 (data entry error).

PROMO_TYPES = ["2-for-1", "Loyalty Card", "Weekend Special", "Clearance", "New Listing"]

promo_rows = []
random.seed(77)
for sku, name, category, cost, price in SKUS:
    for week in WEEKS:
        if random.random() < 0.12:
            promo_type = random.choice(PROMO_TYPES)
            discount_pct = random.choice([5, 10, 15, 20, 25, 30])
            promo_rows.append({
                "sku":           sku,
                "product_name":  name,
                "category":      category,
                "week":          week.isoformat(),
                "promo_type":    promo_type,
                "discount_pct":  discount_pct,
                "approved_by":   random.choice(["regional_mgr", "category_mgr", "auto"]),
            })

promo_df = pd.DataFrame(promo_rows)

# Seed issue: 4 promos with discount_pct = 0 (forgot to fill in the discount)
zero_idx = promo_df.sample(4, random_state=5).index
promo_df.loc[zero_idx, "discount_pct"] = 0

promo_path = out_dir / "promo_calendar.csv"
promo_df.to_csv(promo_path, index=False)

print(f"\n✅  Written {len(promo_df)} rows to:")
print(f"   {promo_path}")
print(f"   Promo weeks total: {len(promo_df)}")
print(f"   Promos with discount_pct = 0 (data issue): {(promo_df['discount_pct'] == 0).sum()}")
