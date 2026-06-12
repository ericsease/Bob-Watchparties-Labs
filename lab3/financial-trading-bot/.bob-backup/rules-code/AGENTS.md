# Code Mode Rules — Financial Trading Bot

## Secrets & Credentials
- NEVER hardcode exchange API keys, secrets, passphrases, or tokens in source code
- ALWAYS use environment variables via `config.py` for sensitive values
- NEVER log credential values — log only that authentication succeeded or failed
- NEVER include real API keys in code comments, docstrings, or error messages
- If a new integration requires credentials, add a placeholder to `.env.example` only

## Secure Coding
- ALWAYS use parameterized queries or ORM methods — NEVER construct SQL with string concatenation or f-strings
- ALWAYS validate and sanitize user input before using it in database queries, file paths, or shell commands
- NEVER use `eval()`, `exec()`, `os.system()`, or `subprocess.shell=True` with user-supplied data
- NEVER use `pickle.loads()` on untrusted data — use JSON serialization for strategy configs
- ALWAYS validate file paths to prevent directory traversal (`../`)

## Financial Data Protection
- NEVER log account balances, portfolio values, or trade details at DEBUG level in production code
- NEVER expose exchange order IDs or internal trade IDs in error responses to API clients
- NEVER include portfolio owner email addresses or personal details in API error messages
- ALWAYS return generic error messages to API clients — log detailed errors server-side only
- Trade execution logs must include order_id and symbol but NEVER include account credentials

## Trade Safety
- ALWAYS enforce `MAX_TRADE_AMOUNT_USD` and `RISK_LIMIT_PERCENT` from Config — NEVER bypass or disable risk limits
- NEVER allow trades without quantity and price validation (positive, non-zero, within bounds)
- NEVER auto-execute trades from external signals without human confirmation
- ALWAYS validate symbol format before using in exchange API calls

## Dependency Management
- ONLY add dependencies listed in `requirements.txt` — do not introduce new packages without explicit approval
- NEVER suggest packages from unknown or unverified sources
- ALWAYS pin dependency versions (e.g., `flask==3.1.0`, not `flask>=3.0`)

## Strategy & Model Integrity
- NEVER modify trading strategy parameters or thresholds without explicit approval
- NEVER alter market analysis calculations (RSI, SMA, volatility) without justification
- NEVER disable or bypass risk checks in the exchange client
