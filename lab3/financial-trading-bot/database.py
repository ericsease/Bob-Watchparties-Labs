"""Database models for Financial Trading Bot."""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Portfolio(db.Model):
    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    owner = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    base_currency = db.Column(db.String(10), default="USD")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    holdings = db.relationship("Holding", backref="portfolio", lazy=True)
    trades = db.relationship("Trade", backref="portfolio", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "description": self.description,
            "base_currency": self.base_currency,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Holding(db.Model):
    __tablename__ = "holdings"

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolios.id"), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    avg_purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        unrealized_pnl = None
        if self.current_price is not None:
            unrealized_pnl = round(
                (self.current_price - self.avg_purchase_price) * self.quantity, 2
            )
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "avg_purchase_price": self.avg_purchase_price,
            "current_price": self.current_price,
            "unrealized_pnl": unrealized_pnl,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }


class Trade(db.Model):
    __tablename__ = "trades"

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolios.id"), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    side = db.Column(db.String(4), nullable=False)  # buy, sell
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default="pending")  # pending, filled, cancelled, failed
    strategy = db.Column(db.String(64))
    order_id = db.Column(db.String(128))  # Exchange order reference
    executed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "symbol": self.symbol,
            "side": self.side,
            "quantity": self.quantity,
            "price": self.price,
            "total_value": self.total_value,
            "fee": self.fee,
            "status": self.status,
            "strategy": self.strategy,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PriceHistory(db.Model):
    __tablename__ = "price_history"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False, index=True)
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "open": self.open_price,
            "high": self.high_price,
            "low": self.low_price,
            "close": self.close_price,
            "volume": self.volume,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    condition = db.Column(db.String(20), nullable=False)  # above, below, pct_change
    threshold = db.Column(db.Float, nullable=False)
    triggered = db.Column(db.Boolean, default=False)
    notification_channel = db.Column(db.String(20), default="log")  # log, slack, email
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    triggered_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "condition": self.condition,
            "threshold": self.threshold,
            "triggered": self.triggered,
            "notification_channel": self.notification_channel,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "triggered_at": self.triggered_at.isoformat() if self.triggered_at else None,
        }
