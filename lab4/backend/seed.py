SEED_DATA = [
    {
        "name": "quantum-cache",
        "owner": "axiom-labs",
        "description": "A blazing-fast in-memory cache with probabilistic eviction and TTL support.",
        "language": "Rust",
        "stars": 8_241,
        "url": "https://github.com/axiom-labs/quantum-cache",
    },
    {
        "name": "openform",
        "owner": "formcraft",
        "description": "Open-source form builder with drag-and-drop UI and webhook integrations.",
        "language": "TypeScript",
        "stars": 14_883,
        "url": "https://github.com/formcraft/openform",
    },
    {
        "name": "pylens",
        "owner": "dataviz-io",
        "description": "Lightweight Python library for exploratory data analysis with auto-generated charts.",
        "language": "Python",
        "stars": 6_102,
        "url": "https://github.com/dataviz-io/pylens",
    },
    {
        "name": "meshrouter",
        "owner": "cloudnative-oss",
        "description": "Zero-config service mesh router for Kubernetes with built-in mTLS.",
        "language": "Go",
        "stars": 21_456,
        "url": "https://github.com/cloudnative-oss/meshrouter",
    },
    {
        "name": "logdrop",
        "owner": "telemetry-team",
        "description": "Structured log aggregator that streams to S3, Loki, or stdout with zero dependencies.",
        "language": "Go",
        "stars": 4_788,
        "url": "https://github.com/telemetry-team/logdrop",
    },
    {
        "name": "snapschema",
        "owner": "devtoolsco",
        "description": "Instantly generate JSON Schema, TypeScript types, or Zod validators from sample data.",
        "language": "TypeScript",
        "stars": 9_317,
        "url": "https://github.com/devtoolsco/snapschema",
    },
    {
        "name": "rockettest",
        "owner": "oss-testing",
        "description": "Parallel test runner for Python with live output, retries, and flake detection.",
        "language": "Python",
        "stars": 3_541,
        "url": "https://github.com/oss-testing/rockettest",
    },
    {
        "name": "vaultkey",
        "owner": "securedev-org",
        "description": "CLI tool to manage secrets across .env files, Vault, and AWS Secrets Manager.",
        "language": "Rust",
        "stars": 11_209,
        "url": "https://github.com/securedev-org/vaultkey",
    },
    {
        "name": "chartflow",
        "owner": "vizforge",
        "description": "React charting library built on D3 with composable, accessible chart primitives.",
        "language": "JavaScript",
        "stars": 17_634,
        "url": "https://github.com/vizforge/chartflow",
    },
    {
        "name": "edgedb-sync",
        "owner": "edgecraft",
        "description": "Real-time sync engine that replicates EdgeDB changes to client apps via WebSockets.",
        "language": "TypeScript",
        "stars": 5_922,
        "url": "https://github.com/edgecraft/edgedb-sync",
    },
]


def seed(db, Repo):
    if Repo.query.count() == 0:
        for item in SEED_DATA:
            db.session.add(Repo(**item))
        db.session.commit()
        print(f"Seeded {len(SEED_DATA)} repos.")
    else:
        print("Database already seeded, skipping.")
