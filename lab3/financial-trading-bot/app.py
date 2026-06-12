"""Financial Trading Bot - Flask REST API.

Manages portfolios, executes trades, analyzes markets, and monitors alerts.
"""

import logging
from datetime import datetime, timezone

from flask import Flask, jsonify, request

from config import Config
from database import db, Portfolio, Holding, Trade, PriceHistory, Alert
from exchange_client import exchange
from market_analyzer import generate_signals, get_portfolio_risk_metrics

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


# ── Portfolio CRUD ───────────────────────────────────────────────────────────


@app.route("/api/portfolios", methods=["GET"])
def list_portfolios():
    """List all portfolios."""
    owner = request.args.get("owner")
    query = Portfolio.query
    if owner:
        query = query.filter_by(owner=owner)
    portfolios = query.all()
    return jsonify([p.to_dict() for p in portfolios])


@app.route("/api/portfolios", methods=["POST"])
def create_portfolio():
    """Create a new portfolio."""
    data = request.get_json()
    if not data or not data.get("name") or not data.get("owner"):
        return jsonify({"error": "name and owner are required"}), 400

    portfolio = Portfolio(
        name=data["name"],
        owner=data["owner"],
        description=data.get("description", ""),
        base_currency=data.get("base_currency", "USD"),
    )
    db.session.add(portfolio)
    db.session.commit()

    logger.info("Portfolio created: %s by %s", portfolio.name, portfolio.owner)
    return jsonify(portfolio.to_dict()), 201


@app.route("/api/portfolios/<int:portfolio_id>", methods=["GET"])
def get_portfolio(portfolio_id):
    """Get portfolio details with holdings."""
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404

    result = portfolio.to_dict()
    result["holdings"] = [h.to_dict() for h in portfolio.holdings]
    return jsonify(result)


@app.route("/api/portfolios/<int:portfolio_id>", methods=["DELETE"])
def delete_portfolio(portfolio_id):
    """Delete a portfolio."""
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404

    db.session.delete(portfolio)
    db.session.commit()
    logger.info("Portfolio deleted: %s", portfolio_id)
    return jsonify({"message": "Portfolio deleted"})


# ── Trading ──────────────────────────────────────────────────────────────────


@app.route("/api/portfolios/<int:portfolio_id>/trade", methods=["POST"])
def execute_trade(portfolio_id):
    """Execute a trade for a portfolio."""
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404

    data = request.get_json()
    if (
        not data
        or not data.get("symbol")
        or not data.get("side")
        or not data.get("quantity")
    ):
        return jsonify({"error": "symbol, side, and quantity are required"}), 400

    side = data["side"].lower()
    if side not in ("buy", "sell"):
        return jsonify({"error": "side must be 'buy' or 'sell'"}), 400

    quantity = float(data["quantity"])
    if quantity <= 0:
        return jsonify({"error": "quantity must be positive"}), 400

    # Execute on exchange
    result = exchange.place_order(
        symbol=data["symbol"],
        side=side,
        quantity=quantity,
        price=data.get("price"),
        order_type=data.get("order_type", "market"),
    )

    if result["status"] == "rejected":
        return jsonify(result), 400

    # Record the trade
    trade = Trade(
        portfolio_id=portfolio.id,
        symbol=data["symbol"],
        side=side,
        quantity=quantity,
        price=result["price"],
        total_value=result["total_value"],
        fee=result.get("fee", 0),
        status=result["status"],
        strategy=data.get("strategy"),
        order_id=result.get("order_id"),
        executed_at=datetime.now(timezone.utc),
    )
    db.session.add(trade)

    # Update holdings
    holding = Holding.query.filter_by(
        portfolio_id=portfolio.id, symbol=data["symbol"]
    ).first()

    if side == "buy":
        if holding:
            total_cost = (holding.avg_purchase_price * holding.quantity) + result[
                "total_value"
            ]
            holding.quantity += quantity
            holding.avg_purchase_price = total_cost / holding.quantity
        else:
            holding = Holding(
                portfolio_id=portfolio.id,
                symbol=data["symbol"],
                quantity=quantity,
                avg_purchase_price=result["price"],
                current_price=result["price"],
            )
            db.session.add(holding)
    else:  # sell
        if holding:
            holding.quantity -= quantity
            if holding.quantity <= 0:
                db.session.delete(holding)

    db.session.commit()

    return jsonify(trade.to_dict()), 201


@app.route("/api/portfolios/<int:portfolio_id>/trades", methods=["GET"])
def list_trades(portfolio_id):
    """List trade history for a portfolio."""
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404

    limit = request.args.get("limit", 50, type=int)
    symbol = request.args.get("symbol")

    query = Trade.query.filter_by(portfolio_id=portfolio.id)
    if symbol:
        query = query.filter_by(symbol=symbol)
    trades = query.order_by(Trade.created_at.desc()).limit(limit).all()

    return jsonify([t.to_dict() for t in trades])


# ── Market Data ──────────────────────────────────────────────────────────────


@app.route("/api/market/ticker/<symbol>", methods=["GET"])
def get_ticker(symbol):
    """Get current price for a symbol."""
    ticker = exchange.get_ticker(symbol)
    return jsonify(ticker)


@app.route("/api/market/analysis/<symbol>", methods=["GET"])
def analyze_symbol(symbol):
    """Get technical analysis and signals for a symbol."""
    days = request.args.get("days", 60, type=int)
    analysis = generate_signals(symbol, days=days)
    return jsonify(analysis)


@app.route("/api/market/prices/<symbol>", methods=["GET"])
def get_price_history(symbol):
    """Get historical price data."""
    limit = request.args.get("limit", 100, type=int)
    records = (
        PriceHistory.query.filter_by(symbol=symbol)
        .order_by(PriceHistory.timestamp.desc())
        .limit(limit)
        .all()
    )
    return jsonify([r.to_dict() for r in records])


# ── Alerts ───────────────────────────────────────────────────────────────────


@app.route("/api/alerts", methods=["GET"])
def list_alerts():
    """List all price alerts."""
    active_only = request.args.get("active", "false").lower() == "true"
    query = Alert.query
    if active_only:
        query = query.filter_by(triggered=False)
    alerts = query.order_by(Alert.created_at.desc()).all()
    return jsonify([a.to_dict() for a in alerts])


@app.route("/api/alerts", methods=["POST"])
def create_alert():
    """Create a price alert."""
    data = request.get_json()
    if (
        not data
        or not data.get("symbol")
        or not data.get("condition")
        or data.get("threshold") is None
    ):
        return jsonify({"error": "symbol, condition, and threshold required"}), 400

    if data["condition"] not in ("above", "below", "pct_change"):
        return jsonify({"error": "condition must be above, below, or pct_change"}), 400

    alert = Alert(
        symbol=data["symbol"],
        condition=data["condition"],
        threshold=float(data["threshold"]),
        notification_channel=data.get("notification_channel", "log"),
    )
    db.session.add(alert)
    db.session.commit()

    return jsonify(alert.to_dict()), 201


# ── Risk & Account ───────────────────────────────────────────────────────────


@app.route("/api/account/balance", methods=["GET"])
def get_balance():
    """Get exchange account balance."""
    return jsonify(exchange.get_account_balance())


@app.route("/api/account/verify", methods=["GET"])
def verify_account():
    """Verify exchange API credentials by testing authentication.

    Tests the exchange connection by signing a test request with the
    configured API credentials and returns whether authentication succeeds.

    Returns:
        JSON response with authentication status and details
    """
    logger.info("Verifying exchange credentials")
    result = exchange.verify_credentials()

    # Return appropriate HTTP status code based on authentication result
    status_code = 200 if result["authenticated"] else 401

    return jsonify(result), status_code


@app.route("/api/portfolios/<int:portfolio_id>/risk", methods=["GET"])
def portfolio_risk(portfolio_id):
    """Get risk metrics for a portfolio."""
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404

    metrics = get_portfolio_risk_metrics(portfolio.holdings)
    return jsonify(metrics)


# ── Health ───────────────────────────────────────────────────────────────────


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "financial-trading-bot"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=Config.DEBUG)
