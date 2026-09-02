# /health-check

**Description:** Pre-merge quality gate for the RepoRadar Lab 4 Bookmarks feature.
Runs the test suite, checks rule compliance, detects schema drift, and smoke-tests
the live API — then produces a single ✅ / ❌ verdict.

---

## When to use

Type `/health-check` after completing Lab 4's implementation step, before
creating a pull request. It catches the three most common failure modes:
a broken test, a rule violation Bob introduced, and a stale SQLite schema.

---

## Steps

Run all five steps sequentially. Narrate each one as you go ("Running tests…",
"Checking rule compliance…") rather than printing results silently at the end.
Collect all results and display the final report only after all steps complete.

---

### Step 1 — Run the test suite

Run:
```bash
cd lab4/backend && source venv/bin/activate && python -m pytest tests/test_bookmarks.py -v
```

- All tests pass → mark ✅, note count (e.g. "8 passed")
- Any failure → mark ❌, include the failure lines in the report
- **Continue to Step 2 regardless** — do not stop on test failure

---

### Step 2 — Check rule compliance

Read these files directly (no shell command):
- `lab4/backend/app.py`
- `lab4/backend/models.py`

Apply the following checklist from `lab4/.bob/rules/reporadar-standards.md`:

1. **Deprecated API** — flag any occurrence of `Model.query.get(` (e.g. `Repo.query.get(`,
   `Bookmark.query.get(`). The correct form is `db.session.get(Model, id)`.
2. **Missing docstrings** — flag any `@app.route` function whose body does not
   begin with a docstring string literal.
3. **Bare dict returns** — flag any `return {` or `return ({` that is not wrapped
   in `jsonify()`.

Report each violation as a separate line item. If none found → mark ✅ "No violations found".

---

### Step 3 — Check for schema drift risk

Run:
```bash
ls lab4/backend/instance/reporadar.db 2>/dev/null && echo "EXISTS" || echo "CLEAN"
```

- Output is `CLEAN` → mark ✅ "`instance/` is clean"
- Output is `EXISTS` → mark ❌ with the message:
  "Delete `instance/reporadar.db` before restarting Flask — `db.create_all()` is
  additive-only and will not add new columns to the existing stale table."

---

### Step 4 — Smoke-test the live API

Run each command in sequence. Capture both the HTTP status code and response body.
If Flask is not running (connection refused), report "Flask is not running on
port 5001 — start it with `python app.py` before re-running this check" and mark
the entire step ❌ without running the remaining curl commands.

```bash
# 1. GET /api/bookmarks — expect 200
curl -s -o /tmp/get_resp.json -w "%{http_code}" http://127.0.0.1:5001/api/bookmarks

# 2. POST /api/bookmarks — expect 201
curl -s -o /tmp/post_resp.json -w "%{http_code}" \
  -X POST http://127.0.0.1:5001/api/bookmarks \
  -H "Content-Type: application/json" \
  -d '{"repo_id": 1}'

# 3. DELETE the bookmark just created — expect 204
BOOKMARK_ID=$(python3 -c "import json; print(json.load(open('/tmp/post_resp.json'))['id'])")
curl -s -o /tmp/del_resp.json -w "%{http_code}" \
  -X DELETE http://127.0.0.1:5001/api/bookmarks/$BOOKMARK_ID
```

Expected status codes: **200, 201, 204**.

- All three match expectations → mark ✅, note all three codes
- Any mismatch → mark ❌, note which call failed and the actual code returned

---

### Step 5 — Produce the final report

Print the following table with real values filled in, then the verdict line:

```
## RepoRadar Health Check

| Check               | Status | Notes                                        |
|---------------------|--------|----------------------------------------------|
| Test suite          | ✅ / ❌ | e.g. "8 passed" or "2 failed (see above)"    |
| Rule compliance     | ✅ / ❌ | e.g. "No violations" or list each violation  |
| Schema drift        | ✅ / ❌ | e.g. "instance/ is clean" or delete warning  |
| API smoke tests     | ✅ / ❌ | e.g. "GET 200, POST 201, DELETE 204"         |

**Verdict: Ready to ship ✅**
```

If any row is ❌, replace the verdict with:

```
**Verdict: X issue(s) need fixing before merge ❌**
```

where X is the count of failed checks.
