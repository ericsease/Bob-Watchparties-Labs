# Security Audit — inventory-service

**Auditor role:** security-auditor persona (`lab5/.bob/personas/security-auditor.md`)
**Date:** 2026-09-09
**Scope:** All Java source files, `application.properties`, `pom.xml`

---

## CRITICAL

### [CRED-001] Hardcoded datasource password
**File:** `lab5/service/src/main/resources/application.properties`, line 7
**Evidence:** `spring.datasource.password=admin123`
**Risk:** Any developer with repository access, any CI log, or any image layer dump exposes the credential in plaintext. Even for a demo H2 database the pattern will be copied verbatim to production configs.
**Fix:** Replace with `spring.datasource.password=${DB_PASSWORD:}` and supply the value via environment variable or a secrets manager. Add a `.env.example` documenting the required variable.

---

## HIGH

### [AUTH-001] No authentication or authorisation on any endpoint
**File:** `lab5/service/src/main/java/com/example/inventory/InventoryController.java`, lines 36–68
**Evidence:** Spring Security is absent from `pom.xml` entirely. All three endpoints (`GET /api/inventory`, `POST /api/inventory`, `DELETE /api/inventory/{id}`) are publicly accessible with no token, session, or basic-auth check.
**Fix:** Add `spring-boot-starter-security` to `pom.xml`. Configure a `SecurityFilterChain` bean that requires authentication for all `/api/**` routes. For Spring Boot 3.x use the `SecurityFilterChain` pattern — `WebSecurityConfigurerAdapter` is removed.

### [DEP-001] Spring Boot 2.7.18 — end-of-life, `javax.*` namespace
**File:** `lab5/service/pom.xml`, line 10
**Evidence:** `spring-boot-starter-parent` version `2.7.18`. Spring Boot 2.7.x reached end-of-life on **24 November 2023** and receives no further security patches. The `spring-boot-starter-validation` dependency at this version pulls `javax.validation` (not `jakarta.validation`), which is incompatible with the Spring Boot 3.x migration target.
**Fix:** Bump parent to `3.3.x` (current stable). Update all `javax.*` imports to `jakarta.*`. Set `<java.version>17</java.version>`.

### [VAL-001] No `@Valid` on `POST /api/inventory` request body
**File:** `lab5/service/src/main/java/com/example/inventory/InventoryController.java`, line 38
**Evidence:** `createItem(@RequestBody InventoryItem item)` — no `@Valid` annotation. Bean Validation constraints on the model are not enforced by the framework; only two hand-rolled `if` checks guard the input. Any field not explicitly checked (e.g. `price`, `lastUpdated`) is completely unvalidated and can receive arbitrary values.
**Fix:** Add `@Valid` to the `@RequestBody` parameter. Annotate `InventoryItem` record components with `@NotBlank`, `@Min(0)`, etc. Handle `MethodArgumentNotValidException` in a `@ControllerAdvice`.

---

## MEDIUM

### [SEC-001] H2 console enabled — no scope restriction
**File:** `lab5/service/src/main/resources/application.properties`, lines 9–10
**Evidence:**
```
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
```
The H2 web console at `/h2-console` provides a full SQL interface to the in-memory database with no authentication (Spring Security is absent — see AUTH-001). An attacker on the same network can read, modify, or drop all data via the browser UI.
**Fix:** Set `spring.h2.console.enabled=false` in any profile that could reach a network. If needed for local development, gate it behind a `dev` profile and require Spring Security's `h2-console` frame-options permit.

### [VAL-002] Path variable `{id}` has no bounds or type validation beyond implicit Long parsing
**File:** `lab5/service/src/main/java/com/example/inventory/InventoryController.java`, line 59
**Evidence:** `@PathVariable Long id` — Spring will throw a `MethodArgumentTypeMismatchException` for non-numeric input, but there is no explicit positive-value constraint. A value of `0` or `-1` is accepted and silently returns "not found" rather than a 400 Bad Request.
**Fix:** Add `@Positive` constraint via `@PathVariable @Positive Long id` (requires `@Validated` on the controller class and `spring-boot-starter-validation`).

### [ERR-001] No global exception handler — unhandled exceptions may expose stack traces
**File:** `lab5/service/src/main/java/com/example/inventory/InventoryController.java`
**Evidence:** There is no `@ControllerAdvice` class. Spring Boot's default error handling (`BasicErrorController`) includes exception class names and, in some configurations, full stack traces in the response body (`server.error.include-stacktrace=always` is the default in some Boot 2.x setups). This is an information disclosure risk.
**Fix:** Add a `@ControllerAdvice` `GlobalExceptionHandler`. Set `server.error.include-stacktrace=never` and `server.error.include-message=never` in `application.properties`.

### [DEP-002] H2 database dependency has no explicit version pin
**File:** `lab5/service/pom.xml`, line 35–38
**Evidence:** `<artifactId>h2</artifactId>` with no `<version>` tag — version is delegated to the Spring Boot BOM. While BOM management is standard, the H2 version in use is not visible in this file. H2 has had critical CVEs (e.g. CVE-2021-42392, CVE-2022-23221) in versions below 2.1.x.
**Fix:** Confirm the BOM-resolved H2 version with `mvn dependency:tree`. If below `2.2.x`, pin it explicitly: `<version>2.2.224</version>`.

---

## LOW / INFORMATIONAL

### [INF-001] `System.out.println` used for startup banner — not a logger
**File:** `lab5/service/src/main/java/com/example/inventory/InventoryApplication.java`, lines 10–13
**Evidence:** Four `System.out.println` calls output a startup banner. While not a direct security risk, stdout output bypasses log-level filtering and log-aggregation pipelines, which means it cannot be silenced or redirected in production environments. In some frameworks stdout is captured in ways that could intermix with sensitive log data.
**Fix:** Replace with `log.info(...)` using SLF4J, or use Spring Boot's built-in `spring.banner.location` mechanism.

### [INF-002] `spring.jpa.show-sql=false` — confirm this is not overridden in profiles
**File:** `lab5/service/src/main/resources/application.properties`, line 12
**Evidence:** SQL logging is currently disabled, which is correct for production. However, there are no profile-specific property files (`application-dev.properties`, `application-prod.properties`) to prevent accidental re-enabling. If a developer adds `show-sql=true` to a shared config it would expose query structure and data shapes in logs.
**Fix:** Introduce `application-dev.properties` and `application-prod.properties` and explicitly set `spring.jpa.show-sql=false` in the prod profile as a permanent guard.

### [INF-003] No CORS configuration present
**File:** `lab5/service/src/main/java/com/example/inventory/InventoryController.java`
**Evidence:** No `@CrossOrigin` annotation and no `CorsConfigurationSource` bean. Spring Boot's default in the absence of Spring Security is to allow all origins for `@RestController` endpoints. This means any browser origin can call the API.
**Fix:** Define an explicit `CorsConfigurationSource` bean that whitelists known origins. Do not use `allowedOrigins("*")` in production.

---

## Summary

| Severity | Count | Finding IDs |
|---|---|---|
| CRITICAL | 1 | CRED-001 |
| HIGH | 3 | AUTH-001, DEP-001, VAL-001 |
| MEDIUM | 3 | SEC-001, VAL-002, ERR-001, DEP-002 |
| LOW / INFO | 3 | INF-001, INF-002, INF-003 |

**Total findings: 10**

### Recommended remediation order

1. **CRED-001** — externalize password immediately (30 min)
2. **DEP-001** — upgrade to Spring Boot 3.3.x; migrate `javax` → `jakarta` (2–3 hrs)
3. **AUTH-001** — add Spring Security with `SecurityFilterChain` (2 hrs)
4. **VAL-001 + ERR-001** — add `@Valid`, `@ControllerAdvice`, and `server.error` properties (1 hr)
5. **SEC-001** — disable H2 console outside dev profile (15 min)
6. **VAL-002 + DEP-002 + INF-001–3** — remaining hardening (1–2 hrs)

**Estimated total remediation: 7–9 hours**
