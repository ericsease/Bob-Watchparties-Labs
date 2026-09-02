# Inventory Service — Legacy Codebase

This is the **pre-modernization** version of the Inventory Service.
Bob will use this as the starting point for the Java modernization demo.

## What it does

A simple REST microservice that manages a product inventory for a fictional enterprise warehouse.
Stores items in memory (no persistence between restarts).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/inventory` | List all inventory items |
| POST | `/api/inventory` | Add a new item |
| DELETE | `/api/inventory/{id}` | Remove an item by ID |

## Known issues (intentional — for the demo)

- **Java 8** — uses `java.util.Date`, raw types, verbose for-loops, plain POJOs
- **No tests** — zero test coverage
- **Hardcoded credentials** — `application.properties` has `spring.datasource.password=admin123`
- **No Dockerfile** — cannot be containerized without manual work
- **No CI/CD** — no pipeline, no automated quality gates
- **No input validation** — manual null checks instead of `@Valid`
- **No exception handling** — no `@ControllerAdvice`, raw HashMap error responses

## Starting the service

```bash
cd lab5/service
mvn spring-boot:run
```

Then verify:
```bash
curl http://localhost:8080/api/inventory
```

You should see 5 seeded inventory items as JSON.
