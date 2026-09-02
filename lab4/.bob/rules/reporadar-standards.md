# RepoRadar — Flask & React coding standards

These rules apply whenever Bob edits code in this project.

---

## SQLAlchemy 2.x API

Always use `db.session.get(Model, id)` for primary-key lookups.
Never use the deprecated `Model.query.get(id)` form — it raises a
`LegacyAPIWarning` in SQLAlchemy 2.x and will be removed in a future release.

Note: `flask-sqlalchemy==3.1.1` is installed (see `requirements.txt`), which
ships SQLAlchemy 2.x under the hood — the warning is live right now.

```python
# ✅ correct
item = db.session.get(Repo, repo_id)

# ❌ deprecated — do not generate this
item = Repo.query.get(repo_id)
```

---

## Flask response patterns

Always return explicit HTTP status codes on non-200 responses.
Use `jsonify()` for all JSON responses — never return a plain dict.

```python
# ✅ correct
return jsonify({"error": "Not found"}), 404

# ❌ wrong — missing status code, missing jsonify
return {"error": "Not found"}
```

---

## Python style

- Use f-strings, not `.format()` or `%` formatting.
- Keep route handler functions focused — delegate business logic directly to
  SQLAlchemy; don't put queries inline in complex conditionals. (There is no
  service layer in this project — keep it that way unless scope grows.)
- All new Flask routes must have a docstring describing the endpoint's purpose.
- The existing `get_repos()` route has no docstring; add one when touching that
  function.

---

## SQLite schema drift — MANDATORY cleanup step

**This is the single most common reason a feature "works" in code but fails silently in the browser during demos.**

### Why it happens

`db.create_all()` is **additive-only**. It creates tables that don't exist yet,
but it **never alters existing tables** — it will not add a new column (or a new
table like `bookmarks`) to a database file that was created by a previous run.

If `instance/reporadar.db` already exists from a prior session where this feature
was partially or fully implemented, the new schema changes will be invisible to the
running app. The first request that touches the new table or column crashes with:

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: bookmarks.<column>
```

This surfaces in the browser as a generic **500**, which looks like a frontend,
CORS, or server startup problem — masking the real cause entirely.

### The rule

**Whenever a `db.Column` or a new `db.Model` table is added in this project, Bob
must delete `instance/reporadar.db` as part of the same implementation step —
before signalling that the implementation is complete.**

Do not wait for the user to hit a 500. After writing the model change, immediately run:

```bash
rm -f lab4/backend/instance/reporadar.db
# Verify it's gone before restarting
ls lab4/backend/instance/
```

Then confirm to the user:

> "I've deleted `instance/reporadar.db` so `db.create_all()` will rebuild the
> schema cleanly (including the new `bookmarks` table) on next startup. The seed
> data will be re-populated automatically."

### How to detect a stale database

All four of these will be true at the same time:

1. A new `db.Column` or `db.Model` was added or renamed in `models.py`.
2. The project uses `db.create_all()` at startup (no Alembic/Flask-Migrate).
3. `instance/reporadar.db` already exists on disk.
4. *(Optional signal)* The user reports a 500 error, a fetch failure, or an `OperationalError`.

If signals 1–3 are present, **act without waiting for signal 4.**

### Codebase fingerprint for this rule

```
lab4/backend/models.py    — Repo (and future Bookmark) db.Model subclasses
lab4/backend/database.py  — exports db = SQLAlchemy() singleton; init_db() calls db.create_all()
lab4/backend/app.py       — calls init_db(app) at startup; no Flask-Migrate present
lab4/backend/instance/    — reporadar.db lives here (Flask default for named apps)
lab4/backend/requirements.txt — flask-sqlalchemy==3.1.1, no flask-migrate entry
```

### Longer-term recommendation

For any project that will evolve its schema beyond initial prototyping, suggest
adding **Flask-Migrate** (Alembic-backed migrations):

```bash
pip install Flask-Migrate
```

```python
# app.py
from flask_migrate import Migrate

migrate = Migrate(app, db)
```

```bash
flask db init       # one-time setup
flask db migrate    # generate migration after each model change
flask db upgrade    # apply migration to the live db
```

This eliminates schema drift entirely and is safe to use in dev and production.
