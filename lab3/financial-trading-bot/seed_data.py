"""Seed the database with sample portfolios, holdings, and price history."""

import random
from datetime import datetime, timedelta, timezone

from app import app
from database import db, Portfolio, Holding, Trade, PriceHistory, Alert

SAMPLE_PORTFOLIOS = [
    {
        "name": "Growth Portfolio",
        "owner": "alice.johnson@company-corp.com",
        "description": "Long-term growth equities and crypto",
        "base_currency": "USD",
    },
    {
        "name": "Conservative Fund",
        "owner": "bob.smith@company-corp.com",
        "description": "Blue-chip stocks with low volatility",
        "base_currency": "USD",
    },
    {
        "name": "Crypto Basket",
        "owner": "charlie.dev@company-corp.com",
        "description": "Diversified cryptocurrency holdings",
        "base_currency": "USD",
    },
]

SYMBOLS_CONFIG = {
    "AAPL": {"base_price": 189.50, "volatility": 0.015},
    "GOOGL": {"base_price": 175.30, "volatility": 0.018},
    "MSFT": {"base_price": 415.60, "volatility": 0.012},
    "TSLA": {"base_price": 248.90, "volatility": 0.035},
    "BTC-USD": {"base_price": 67450.25, "volatility": 0.025},
    "ETH-USD": {"base_price": 3520.80, "volatility": 0.030},
}

SAMPLE_HOLDINGS = {
    0: [  # Growth Portfolio
        {"symbol": "AAPL", "quantity": 50, "avg_purchase_price": 175.20},
        {"symbol": "TSLA", "quantity": 30, "avg_purchase_price": 230.00},
        {"symbol": "BTC-USD", "quantity": 0.5, "avg_purchase_price": 58000.00},
        {"symbol": "ETH-USD", "quantity": 10, "avg_purchase_price": 3100.00},
    ],
    1: [  # Conservative Fund
        {"symbol": "AAPL", "quantity": 100, "avg_purchase_price": 165.00},
        {"symbol": "MSFT", "quantity": 80, "avg_purchase_price": 390.00},
        {"symbol": "GOOGL", "quantity": 60, "avg_purchase_price": 160.00},
    ],
    2: [  # Crypto Basket
        {"symbol": "BTC-USD", "quantity": 1.5, "avg_purchase_price": 55000.00},
        {"symbol": "ETH-USD", "quantity": 25, "avg_purchase_price": 2800.00},
    ],
}


def generate_price_history(symbol, config, days=90):
    """Generate realistic OHLCV price data with random walk."""
    records = []
    now = datetime.now(timezone.utc)
    price = config["base_price"] * random.uniform(0.85, 0.95)  # Start lower

    for day in range(days):
        timestamp = now - timedelta(days=days - day)
        daily_return = random.gauss(0.0005, config["volatility"])
        price *= 1 + daily_return

        high = price * (1 + abs(random.gauss(0, config["volatility"] * 0.5)))
        low = price * (1 - abs(random.gauss(0, config["volatility"] * 0.5)))
        open_price = random.uniform(low, high)
        volume = random.uniform(1_000_000, 50_000_000)

        records.append(
            PriceHistory(
                symbol=symbol,
                open_price=round(open_price, 2),
                high_price=round(high, 2),
                low_price=round(low, 2),
                close_price=round(price, 2),
                volume=round(volume, 2),
                timestamp=timestamp,
            )
        )

    return records


def generate_trades(portfolio, holdings, count=10):
    """Generate sample trade history."""
    trades = []
    now = datetime.now(timezone.utc)

    for i in range(count):
        h = random.choice(holdings)
        side = random.choice(["buy", "sell"])
        qty = round(random.uniform(1, 10), 2)
        price = h["avg_purchase_price"] * random.uniform(0.9, 1.1)
        total = round(qty * price, 2)

        trades.append(
            Trade(
                portfolio_id=portfolio.id,
                symbol=h["symbol"],
                side=side,
                quantity=qty,
                price=round(price, 2),
                total_value=total,
                fee=round(total * 0.001, 2),
                status="filled",
                strategy=random.choice(["manual", "sma_crossover", "rsi_signal", None]),
                order_id=f"ORD-SEED-{i:04d}",
                executed_at=now - timedelta(days=random.randint(1, 60)),
            )
        )

    return trades


def seed():
    with app.app_context():
        # Clear existing data
        Trade.query.delete()
        Holding.query.delete()
        Alert.query.delete()
        PriceHistory.query.delete()
        Portfolio.query.delete()

        # Create portfolios
        portfolios = []
        for pdata in SAMPLE_PORTFOLIOS:
            p = Portfolio(**pdata)
            db.session.add(p)
            portfolios.append(p)
        db.session.flush()

        # Create holdings
        for idx, portfolio in enumerate(portfolios):
            holdings_data = SAMPLE_HOLDINGS.get(idx, [])
            for hdata in holdings_data:
                sym_config = SYMBOLS_CONFIG.get(hdata["symbol"], {})
                current_price = sym_config.get("base_price", hdata["avg_purchase_price"])
                holding = Holding(
                    portfolio_id=portfolio.id,
                    symbol=hdata["symbol"],
                    quantity=hdata["quantity"],
                    avg_purchase_price=hdata["avg_purchase_price"],
                    current_price=current_price,
                )
                db.session.add(holding)

            # Generate trade history
            trades = generate_trades(portfolio, holdings_data)
            db.session.add_all(trades)

        # Generate price history for all symbols
        for symbol, config in SYMBOLS_CONFIG.items():
            records = generate_price_history(symbol, config)
            db.session.add_all(records)

        # Create sample alerts
        alerts = [
            Alert(symbol="BTC-USD", condition="above", threshold=70000.0, notification_channel="slack"),
            Alert(symbol="AAPL", condition="below", threshold=170.0, notification_channel="email"),
            Alert(symbol="TSLA", condition="pct_change", threshold=5.0, notification_channel="log"),
        ]
        db.session.add_all(alerts)

        db.session.commit()

        print(f"Seeded {len(portfolios)} portfolios with holdings and trade history")
        print(f"Seeded price history for {len(SYMBOLS_CONFIG)} symbols (90 days)")
        print(f"Seeded {len(alerts)} price alerts")


if __name__ == "__main__":
    seed()
