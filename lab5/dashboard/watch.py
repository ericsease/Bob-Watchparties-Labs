#!/usr/bin/env python3
"""
Inventory Dashboard — live terminal view of the inventory service.

Polls GET /api/inventory every 2 seconds and renders a formatted table.
This is a demo aid — start it in a second terminal alongside the Java service.

Usage:
    pip install requests rich
    python watch.py
"""

import time
import sys

try:
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.text import Text
    USE_RICH = True
except ImportError:
    USE_RICH = False

API_URL = "http://localhost:8080/api/inventory"
POLL_INTERVAL = 2  # seconds


def fetch_items():
    """Fetch inventory items from the Java service."""
    try:
        resp = requests.get(API_URL, timeout=3)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.ConnectionError:
        return None, "⚠  Cannot reach http://localhost:8080 — is the Java service running?"
    except Exception as e:
        return None, f"Error: {e}"


def build_table(items):
    """Build a rich table from inventory items."""
    table = Table(title="📦 Inventory Service — Live View", border_style="blue")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Name", style="bold white", min_width=24)
    table.add_column("Qty", justify="right", style="cyan")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Last Updated", style="dim")

    for item in items:
        table.add_row(
            str(item.get("id", "")),
            item.get("name", ""),
            str(item.get("quantity", "")),
            f"${item.get('price', 0):.2f}",
            str(item.get("lastUpdated", ""))[:24],
        )
    return table


def plain_print(items, error):
    """Fallback plain-text renderer when rich is not installed."""
    print("\033[2J\033[H", end="")  # clear screen
    print("=" * 60)
    print("  📦  Inventory Service — Live View")
    print("=" * 60)
    if error:
        print(f"\n  {error}\n")
        return
    fmt = "  {:<4} {:<28} {:>6} {:>10}"
    print(fmt.format("ID", "Name", "Qty", "Price"))
    print("  " + "-" * 56)
    for item in items:
        print(fmt.format(
            item.get("id", ""),
            item.get("name", "")[:28],
            item.get("quantity", ""),
            f"${item.get('price', 0):.2f}",
        ))
    print(f"\n  {len(items)} items  |  polling every {POLL_INTERVAL}s  |  Ctrl+C to stop")


def run_rich():
    console = Console()
    with Live(console=console, refresh_per_second=1) as live:
        while True:
            items, error = fetch_items()
            if error:
                live.update(Text(error, style="bold red"))
            else:
                live.update(build_table(items))
            time.sleep(POLL_INTERVAL)


def run_plain():
    while True:
        items, error = fetch_items()
        plain_print(items or [], error)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    print(f"Connecting to {API_URL} ...")
    try:
        if USE_RICH:
            run_rich()
        else:
            print("Tip: pip install rich  for a prettier view")
            run_plain()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
        sys.exit(0)
