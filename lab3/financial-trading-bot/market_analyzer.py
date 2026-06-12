"""Market analysis and trading signal generation."""

import logging
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

from database import db, PriceHistory

logger = logging.getLogger(__name__)


def get_price_dataframe(symbol, days=30):
    """Load price history into a pandas DataFrame."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    records = (
        PriceHistory.query.filter_by(symbol=symbol)
        .filter(PriceHistory.timestamp >= cutoff)
        .order_by(PriceHistory.timestamp.asc())
        .all()
    )

    if not records:
        return None

    data = [
        {
            "timestamp": r.timestamp,
            "open": r.open_price,
            "high": r.high_price,
            "low": r.low_price,
            "close": r.close_price,
            "volume": r.volume,
        }
        for r in records
    ]
    df = pd.DataFrame(data)
    df.set_index("timestamp", inplace=True)
    return df


def calculate_moving_averages(df, short_window=10, long_window=30):
    """Calculate short and long moving averages."""
    df["sma_short"] = df["close"].rolling(window=short_window).mean()
    df["sma_long"] = df["close"].rolling(window=long_window).mean()
    return df


def calculate_rsi(df, period=14):
    """Calculate Relative Strength Index."""
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))
    return df


def calculate_volatility(df, window=20):
    """Calculate rolling volatility (annualized standard deviation of returns)."""
    returns = df["close"].pct_change()
    df["volatility"] = returns.rolling(window=window).std() * np.sqrt(252)
    return df


def generate_signals(symbol, days=60):
    """Generate trading signals based on technical indicators."""
    df = get_price_dataframe(symbol, days=days)
    if df is None or len(df) < 30:
        return {"symbol": symbol, "error": "Insufficient price data"}

    df = calculate_moving_averages(df)
    df = calculate_rsi(df)
    df = calculate_volatility(df)

    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else latest

    signals = []

    # Moving average crossover
    if latest["sma_short"] > latest["sma_long"] and prev["sma_short"] <= prev["sma_long"]:
        signals.append({"type": "sma_crossover", "direction": "bullish", "strength": "strong"})
    elif latest["sma_short"] < latest["sma_long"] and prev["sma_short"] >= prev["sma_long"]:
        signals.append({"type": "sma_crossover", "direction": "bearish", "strength": "strong"})

    # RSI signals
    rsi_val = latest.get("rsi")
    if rsi_val is not None and not np.isnan(rsi_val):
        if rsi_val < 30:
            signals.append({"type": "rsi_oversold", "value": round(rsi_val, 2), "direction": "bullish"})
        elif rsi_val > 70:
            signals.append({"type": "rsi_overbought", "value": round(rsi_val, 2), "direction": "bearish"})

    # Volatility alert
    vol = latest.get("volatility")
    if vol is not None and not np.isnan(vol) and vol > 0.4:
        signals.append({"type": "high_volatility", "value": round(vol, 4), "severity": "warning"})

    return {
        "symbol": symbol,
        "latest_price": round(latest["close"], 2),
        "sma_short": round(latest["sma_short"], 2) if not np.isnan(latest["sma_short"]) else None,
        "sma_long": round(latest["sma_long"], 2) if not np.isnan(latest["sma_long"]) else None,
        "rsi": round(rsi_val, 2) if rsi_val is not None and not np.isnan(rsi_val) else None,
        "volatility": round(vol, 4) if vol is not None and not np.isnan(vol) else None,
        "signals": signals,
        "data_points": len(df),
    }


def get_portfolio_risk_metrics(holdings):
    """Calculate portfolio-level risk metrics."""
    if not holdings:
        return {"error": "No holdings to analyze"}

    total_value = sum(
        h.quantity * (h.current_price or h.avg_purchase_price) for h in holdings
    )

    positions = []
    for h in holdings:
        price = h.current_price or h.avg_purchase_price
        position_value = h.quantity * price
        weight = position_value / total_value if total_value > 0 else 0
        positions.append({
            "symbol": h.symbol,
            "value": round(position_value, 2),
            "weight": round(weight * 100, 2),
            "pnl_pct": round(((price - h.avg_purchase_price) / h.avg_purchase_price) * 100, 2),
        })

    # Concentration risk: largest single position
    max_weight = max(p["weight"] for p in positions) if positions else 0

    return {
        "total_value": round(total_value, 2),
        "positions": positions,
        "num_positions": len(positions),
        "max_concentration_pct": max_weight,
        "concentration_warning": max_weight > 30,
    }
