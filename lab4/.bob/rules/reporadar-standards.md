# RepoRadar — Flask & React coding standards

These rules apply whenever Bob edits code in this project.

## SQLAlchemy 2.x API

Always use `db.session.get(Model, id)` for primary-key lookups.
Never use the deprecated `Model.query.get(id)` form — it raises a
`LegacyAPIWarning` in SQLAlchemy 2.x and will be removed in a future release.

```python
# ✅ correct
item = db.session.get(Repo, repo_id)

# ❌ deprecated — do not generate this
item = Repo.query.get(repo_id)
```

## Flask response patterns

Always return explicit HTTP status codes on non-200 responses.
Use `jsonify()` for all JSON responses — never return a plain dict.

```python
# ✅ correct
return jsonify({"error": "Not found"}), 404

# ❌ wrong — missing status code, missing jsonify
return {"error": "Not found"}
```

## Python style

- Use f-strings, not `.format()` or `%` formatting.
- Keep route handler functions focused — delegate business logic to a service layer or directly to SQLAlchemy; don't put queries inline in complex conditionals.
- All new Flask routes must have a docstring describing the endpoint's purpose.
