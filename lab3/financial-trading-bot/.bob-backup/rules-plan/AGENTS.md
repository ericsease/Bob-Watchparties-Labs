# Plan Mode Rules — Financial Trading Bot

## Architecture Constraints
- Flask REST API with SQLAlchemy ORM — no raw SQL
- Configuration via python-dotenv and `config.py` — no hardcoded values
- Exchange interaction through `exchange_client.py` — all trades go through this client
- Market analysis in `market_analyzer.py` using pandas and numpy
- SQLite for development — no additional database services required

## Security Planning
- All new features must include a security consideration section
- New API endpoints must specify what data they expose and whether authentication is needed
- Any feature that touches exchange credentials must include a threat model
- Data flow changes must document what financial data passes through each component
- NEVER plan features that bypass trade risk limits or auto-execute without confirmation

## Approved Dependencies
- Only these packages are approved: flask, flask-sqlalchemy, requests, python-dotenv, cryptography, apscheduler, numpy, pandas
- Any additional dependency requires explicit justification and approval

## File Access Boundaries
- Code changes must not read or modify files outside the project directory
- The `.env` file must never be read or displayed by the IDE
- Strategy files (`.json`) and model files (`.pkl`) are protected — do not modify without approval
- Market data exports (`.csv`) are read-only reference data

## Regulatory Awareness
- Features must not facilitate wash trading, spoofing, or market manipulation
- Automated trading features must include kill-switch or circuit-breaker mechanisms
- All trade actions must be auditable (logged with timestamps and order IDs)
