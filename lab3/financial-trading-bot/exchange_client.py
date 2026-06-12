"""Exchange API client for placing and managing trades."""

import hashlib
import hmac
import json
import logging
import time
from datetime import datetime, timezone

from config import Config

logger = logging.getLogger(__name__)


class ExchangeClient:
    """Simulated exchange client with realistic API patterns.

    In production this would connect to a real exchange (Coinbase, Binance, etc.).
    This simulation mirrors the authentication and order flow patterns.
    """

    BASE_URL = "https://api.exchange-sim.example.com"

    def __init__(self):
        self.api_key = Config.EXCHANGE_API_KEY
        self.api_secret = Config.EXCHANGE_API_SECRET
        self.passphrase = Config.EXCHANGE_PASSPHRASE
        self._simulated_balance = {
            "USD": 100000.0,
            "BTC": 2.5,
            "ETH": 30.0,
            "AAPL": 100,
        }

    def _sign_request(self, method, path, body=""):
        """Generate HMAC signature for authenticated requests."""
        timestamp = str(int(time.time()))
        message = timestamp + method.upper() + path + body
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return {
            "X-API-Key": self.api_key,
            "X-API-Sign": signature,
            "X-API-Timestamp": timestamp,
            "X-API-Passphrase": self.passphrase,
        }

    def get_account_balance(self):
        """Retrieve account balances."""
        logger.info("Fetching account balance")
        return {
            "balances": [
                {"currency": k, "available": v, "hold": 0.0}
                for k, v in self._simulated_balance.items()
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def get_ticker(self, symbol):
        """Get current price for a symbol."""
        # Simulated prices
        prices = {
            "BTC-USD": 67450.25,
            "ETH-USD": 3520.80,
            "AAPL": 189.50,
            "GOOGL": 175.30,
            "MSFT": 415.60,
            "TSLA": 248.90,
        }
        price = prices.get(symbol, 100.0)
        return {
            "symbol": symbol,
            "price": price,
            "bid": round(price * 0.999, 2),
            "ask": round(price * 1.001, 2),
            "volume_24h": 15234567.89,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def place_order(self, symbol, side, quantity, price=None, order_type="market"):
        """Place a trade order."""
        ticker = self.get_ticker(symbol)
        exec_price = price if price else ticker["price"]
        total_value = exec_price * quantity

        # Risk checks
        if total_value > Config.MAX_TRADE_AMOUNT_USD:
            logger.warning(
                "Order rejected: value $%.2f exceeds max $%.2f",
                total_value,
                Config.MAX_TRADE_AMOUNT_USD,
            )
            return {
                "status": "rejected",
                "reason": f"Order value ${total_value:.2f} exceeds maximum ${Config.MAX_TRADE_AMOUNT_USD:.2f}",
            }

        order_id = f"ORD-{int(time.time())}-{symbol.replace('-', '')}"

        # Simulate fill
        if side == "buy":
            base = symbol.split("-")[0] if "-" in symbol else symbol
            self._simulated_balance["USD"] -= total_value
            self._simulated_balance[base] = (
                self._simulated_balance.get(base, 0) + quantity
            )
        else:
            base = symbol.split("-")[0] if "-" in symbol else symbol
            self._simulated_balance[base] = (
                self._simulated_balance.get(base, 0) - quantity
            )
            self._simulated_balance["USD"] += total_value

        fee = round(total_value * 0.001, 2)  # 0.1% fee

        logger.info(
            "Order filled: %s %s %.4f %s @ $%.2f (total: $%.2f, fee: $%.2f)",
            order_id,
            side,
            quantity,
            symbol,
            exec_price,
            total_value,
            fee,
        )

        return {
            "order_id": order_id,
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": exec_price,
            "total_value": total_value,
            "fee": fee,
            "status": "filled",
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }

    def verify_credentials(self):
        """Verify API credentials by signing a test request.

        Returns a dict with:
        - authenticated: bool indicating if credentials are valid
        - message: str describing the result
        - signature_valid: bool indicating if signature generation works
        - credentials_present: bool indicating if all required credentials exist
        """
        # Check if credentials are present
        credentials_present = bool(self.api_key and self.api_secret and self.passphrase)

        if not credentials_present:
            logger.warning("Credential verification failed: missing credentials")
            return {
                "authenticated": False,
                "message": "Missing API credentials (key, secret, or passphrase)",
                "signature_valid": False,
                "credentials_present": False,
            }

        try:
            # Sign a test request to verify signature generation works
            test_path = "/api/v1/account"
            test_method = "GET"
            headers = self._sign_request(test_method, test_path)

            # Verify signature was generated
            signature_valid = bool(headers.get("X-API-Sign"))

            # In a real implementation, this would make an actual API call
            # to the exchange to verify the credentials work
            # For this simulation, we verify the signature generation works

            if signature_valid:
                logger.info("Credential verification successful")
                return {
                    "authenticated": True,
                    "message": "API credentials verified successfully",
                    "signature_valid": True,
                    "credentials_present": True,
                    "api_key": self.api_key[:8] + "..."
                    if len(self.api_key) > 8
                    else "***",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            else:
                logger.warning(
                    "Credential verification failed: signature generation error"
                )
                return {
                    "authenticated": False,
                    "message": "Failed to generate request signature",
                    "signature_valid": False,
                    "credentials_present": True,
                }

        except Exception as e:
            logger.error("Credential verification error: %s", str(e))
            return {
                "authenticated": False,
                "message": f"Verification error: {str(e)}",
                "signature_valid": False,
                "credentials_present": credentials_present,
            }

    def cancel_order(self, order_id):
        """Cancel a pending order."""
        logger.info("Order cancelled: %s", order_id)
        return {"order_id": order_id, "status": "cancelled"}


exchange = ExchangeClient()
