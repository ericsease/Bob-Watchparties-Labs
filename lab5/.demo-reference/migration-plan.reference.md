# Inventory Service — Java 17 Modernization Plan

**Source:** `lab5/service/src/main/java/com/example/inventory/`
**Target:** Java 17 + Spring Boot 3.x
**Approach:** Incremental, one sub-task at a time. Each task is independently reviewable.

---

## Priority Tiers

| Priority | Category | Rationale |
|---|---|---|
| P0 | Security | Hardcoded secret committed to source — fix before any other change |
| P1 | Language idioms | Core Java 17 modernization; reduces boilerplate, improves correctness |
| P2 | Missing infrastructure | Replace in-memory store with JPA; add error handling |
| P3 | Testability gaps | No tests exist; required before any production use |

---

## Sub-Tasks

---

### Task 1 — Externalize hardcoded datasource password
**Status:** `[ ] pending`
**Priority:** P0 — Security

**Intent**
Remove the plaintext `admin123` password from `application.properties`. A secret committed to source is visible in every git clone, log, and CI artifact.

**Expected Outcomes**
- `application.properties` contains `spring.datasource.password=${DB_PASSWORD:}` (env-var placeholder with empty default)
- No literal password string remains in any tracked file
- A `.env.example` file documents the required variable for local development

**Todo**
1. Replace `spring.datasource.password=admin123` with `spring.datasource.password=${DB_PASSWORD:}`
2. Create `lab5/service/.env.example` containing `DB_PASSWORD=<your-password-here>`
3. Confirm `.env` is listed in `.gitignore`

**Relevant Files**
- `lab5/service/src/main/resources/application.properties:7`

---

### Task 2 — Replace `InventoryItem` POJO with a Java `record`
**Status:** `[ ] pending`
**Priority:** P1 — Language idiom

**Intent**
`InventoryItem` is a pure data carrier: 5 fields and 80+ lines of hand-written getters, setters, `equals`, `hashCode`, and `toString`. A Java 16+ `record` eliminates all of that in a single declaration and is immutable by default.

**Expected Outcomes**
- `InventoryItem.java` is replaced by a `record` with 5 components: `id`, `name`, `quantity`, `price`, `lastUpdated`
- `lastUpdated` type changes from `java.util.Date` to `java.time.LocalDateTime`
- All call sites in `InventoryService` and `InventoryController` compile against the record's accessor methods (`.id()`, `.name()`, etc.)
- No `setters` remain (record components are final)

**API contract note**
Records serialize to the same JSON field names via Jackson — no REST contract change.

**Todo**
1. Replace `InventoryItem.java` with a `record` declaration
2. Change `Date lastUpdated` component to `LocalDateTime lastUpdated`
3. Remove `java.util.Date` import; add `java.time.LocalDateTime` import
4. Update `InventoryService` constructor calls and any setter calls to use `with`-style construction or record canonical constructor

**Relevant Files**
- `lab5/service/src/main/java/com/example/inventory/InventoryItem.java`
- `lab5/service/src/main/java/com/example/inventory/InventoryService.java` (call sites)

---

### Task 3 — Modernize `InventoryService` with streams, `Optional`, and `LocalDateTime`
**Status:** `[ ] pending`
**Priority:** P1 — Language idiom

**Intent**
Three methods in `InventoryService` use index-based `for` loops that Java streams replace with concise, readable one-liners. `findById` returns `null` where `Optional<InventoryItem>` is the correct Java 8+ contract. `new Date()` must be replaced with `LocalDateTime.now()`.

**Expected Outcomes**
- `findAll()` returns `List.copyOf(items)` — defensive immutable copy, no loop
- `findById(Long id)` returns `Optional<InventoryItem>` using `stream().filter().findFirst()`
- `create()` stamps `LocalDateTime.now()` instead of `new Date()`
- `delete()` uses `items.removeIf(...)` — no index manipulation
- `InventoryController` updated to unwrap `Optional` and return 404 on `empty()`
- `var` used for local variable declarations where type is obvious

**Todo**
1. Refactor `findAll()` to `return List.copyOf(items)`
2. Refactor `findById()` to use stream + `Optional<InventoryItem>` return type
3. Replace `new Date()` in `create()` with `LocalDateTime.now()`
4. Refactor `delete()` to use `removeIf`
5. Update `InventoryController.deleteItem()` to call `Optional`-returning `findById` pattern (or keep boolean delete — confirm which)
6. Replace raw `new ArrayList<InventoryItem>()` with diamond `new ArrayList<>()`

**Relevant Files**
- `lab5/service/src/main/java/com/example/inventory/InventoryService.java`
- `lab5/service/src/main/java/com/example/inventory/InventoryController.java`

---

### Task 4 — Add typed error response and `@ControllerAdvice` handler
**Status:** `[ ] pending`
**Priority:** P2 — Missing infrastructure

**Intent**
Both controller error paths return raw `HashMap<String, String>`, producing `ResponseEntity<?>` wildcards. Every API error should have the same shape. A small `ErrorResponse` record plus a `@ControllerAdvice` centralises this and removes the inline map construction.

**Expected Outcomes**
- New `ErrorResponse` record: `record ErrorResponse(String error) {}`
- New `GlobalExceptionHandler` class annotated `@ControllerAdvice`
- Controller methods return `ResponseEntity<InventoryItem>` (typed, not wildcard)
- Error cases throw a typed exception (e.g., `ItemNotFoundException`) caught by the advice

**Todo**
1. Create `ErrorResponse.java` as a `record`
2. Create `ItemNotFoundException.java` extending `RuntimeException`
3. Create `GlobalExceptionHandler.java` with `@ExceptionHandler(ItemNotFoundException.class)` returning 404
4. Refactor `InventoryController` to throw instead of building error maps inline
5. Remove all `HashMap` error construction from controller methods

**Relevant Files**
- `lab5/service/src/main/java/com/example/inventory/InventoryController.java`

---

### Task 5 — Add `GET /api/inventory/{id}` endpoint
**Status:** `[ ] pending`
**Priority:** P2 — Missing infrastructure

**Intent**
The REST interface is missing a single-item retrieval endpoint. `GET /api/inventory` (list all) and `DELETE /{id}` exist, but there is no `GET /{id}`. This is a standard REST gap.

**Expected Outcomes**
- New `@GetMapping("/{id}")` handler in `InventoryController`
- Returns `200 OK` with the item body when found
- Returns `404 Not Found` with `ErrorResponse` when not found (via `ItemNotFoundException` from Task 4)

**Todo**
1. Add `getItemById(@PathVariable Long id)` method to `InventoryController`
2. Delegate to `inventoryService.findById(id)` and map `Optional.empty()` to `ItemNotFoundException`

**Relevant Files**
- `lab5/service/src/main/java/com/example/inventory/InventoryController.java`

---

### Task 6 — Add Bean Validation to `InventoryItem` and controller
**Status:** `[ ] pending`
**Priority:** P2 — Missing infrastructure

**Intent**
Validation logic is hand-rolled in the controller with `if` checks. Bean Validation (`@NotBlank`, `@Min`) on the model and `@Valid` on the controller parameter lets Spring handle this declaratively and produces consistent 400 responses.

**Expected Outcomes**
- `InventoryItem` record components annotated with `@NotBlank(message="Name is required")` and `@Min(value=0, message="Quantity cannot be negative")`
- `createItem(@Valid @RequestBody InventoryItem item)` — manual null/range checks removed
- `GlobalExceptionHandler` handles `MethodArgumentNotValidException` and returns `400` with `ErrorResponse`

**Todo**
1. Add `spring-boot-starter-validation` dependency to `pom.xml` if not present
2. Annotate `InventoryItem` record components with JSR-380 constraints
3. Add `@Valid` to `createItem` parameter
4. Remove manual `if` validation blocks from controller
5. Add `@ExceptionHandler(MethodArgumentNotValidException.class)` to `GlobalExceptionHandler`

**Relevant Files**
- `lab5/service/src/main/java/com/example/inventory/InventoryItem.java`
- `lab5/service/src/main/java/com/example/inventory/InventoryController.java`
- `lab5/service/pom.xml`

---

### Task 7 — Add JUnit 5 unit tests for `InventoryService`
**Status:** `[ ] pending`
**Priority:** P3 — Testability

**Intent**
There are zero tests in this project. `InventoryService` is pure in-memory logic — it can be fully unit-tested with no mocking framework. Tests must be in place before any refactored code can be trusted.

**Expected Outcomes**
- `InventoryServiceTest.java` under `src/test/java/com/example/inventory/`
- Test cases: `findAll_returnsAllItems`, `findById_found`, `findById_notFound`, `create_assignsIdAndTimestamp`, `delete_existingItem`, `delete_nonExistentItem`
- `mvn test` passes with all 6 tests green

**Todo**
1. Create `src/test/java/com/example/inventory/InventoryServiceTest.java`
2. Use JUnit 5 (`@Test`, `assertThat` from AssertJ, already on Spring Boot test classpath)
3. Instantiate `InventoryService` directly — no Spring context needed
4. Cover all 4 public methods: `findAll`, `findById`, `create`, `delete`

**Relevant Files**
- New file: `lab5/service/src/test/java/com/example/inventory/InventoryServiceTest.java`
- `lab5/service/pom.xml` (verify `spring-boot-starter-test` is present)

---

### Task 8 — Add Spring Boot integration test for `InventoryController`
**Status:** `[ ] pending`
**Priority:** P3 — Testability

**Intent**
Unit tests cover service logic; a `@WebMvcTest` slice test covers the HTTP layer: routing, serialization, HTTP status codes, and validation rejection.

**Expected Outcomes**
- `InventoryControllerTest.java` using `@WebMvcTest(InventoryController.class)`
- `MockMvc` tests for: `GET /api/inventory` returns 200, `POST` with valid body returns 201, `POST` with blank name returns 400, `DELETE /{id}` returns 204, `DELETE` unknown id returns 404
- `mvn test` passes

**Todo**
1. Create `src/test/java/com/example/inventory/InventoryControllerTest.java`
2. Mock `InventoryService` with `@MockBean`
3. Write `MockMvc` test cases for each HTTP scenario above

**Relevant Files**
- New file: `lab5/service/src/test/java/com/example/inventory/InventoryControllerTest.java`

---

## Completion Checklist

- [ ] Task 1 — Externalize hardcoded password (P0)
- [ ] Task 2 — `InventoryItem` → Java `record` + `LocalDateTime` (P1)
- [ ] Task 3 — `InventoryService` streams + `Optional` + `LocalDateTime` (P1)
- [ ] Task 4 — `ErrorResponse` record + `@ControllerAdvice` (P2)
- [ ] Task 5 — `GET /api/inventory/{id}` endpoint (P2)
- [ ] Task 6 — Bean Validation with `@Valid` (P2)
- [ ] Task 7 — JUnit 5 unit tests for `InventoryService` (P3)
- [ ] Task 8 — `@WebMvcTest` integration tests for `InventoryController` (P3)
