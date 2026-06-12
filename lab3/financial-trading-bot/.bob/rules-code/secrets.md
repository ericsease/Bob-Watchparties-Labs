# Secret Handling Rules
- NEVER hardcode exchange API keys, secrets, passphrases, or tokens in source code
- ALWAYS use environment variables via `config.py` for sensitive values
- NEVER log credential values — log only that authentication succeeded or failed
- NEVER include real API keys in code comments, docstrings, or error messages
- If a new integration requires credentials, add a placeholder to `.env.example` only