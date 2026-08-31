---
name: java-modernization
description: >
  Java 8 to Java 17+ modernization playbook. Use when modernizing legacy Java code,
  migrating Spring Boot 2.x to 3.x, or applying modern Java idioms (records, var,
  LocalDateTime, streams, sealed classes). Trigger phrases: "modernize", "migrate Java",
  "upgrade to Java 17", "Java modernization", "legacy Java".
---

# Java Modernization Skill

Activated when modernizing Java 8 codebases to Java 17+.

---

## Java 8 → Java 17 Pattern Map

| Java 8 Pattern | Java 17+ Replacement | Notes |
|---|---|---|
| Plain POJO class | `record` | Records are immutable, auto-generate equals/hashCode/toString |
| `java.util.Date` | `java.time.LocalDateTime` | Use `Instant` for timestamps with timezone |
| `new ArrayList<Type>()` | `List.of(...)` / `List.copyOf(...)` | Prefer immutable collections |
| `for (T x : list)` loop | `list.stream().filter().map()...` | Use streams; `removeIf` for deletions |
| `if (x == null)` checks | `Optional<T>` | Return `Optional.empty()` instead of null |
| Raw type `HashMap` | `Map<K,V>` with diamond `<>` | Always parameterize generics |
| `instanceof` + cast | Pattern matching: `if (x instanceof Foo f)` | Java 16+ |
| Multi-line String concat | Text blocks `"""..."""` | Java 15+ |
| `switch` statement | `switch` expression with `->` | Java 14+ |
| `var` missing | `var` for local inference | Java 10+; never use for fields |

---

## Spring Boot 2.x → 3.x Migration Checklist

- [ ] **javax → jakarta**: All `javax.*` imports become `jakarta.*` (Servlet, Persistence, Validation)
- [ ] **Spring Security**: `WebSecurityConfigurerAdapter` removed — use `SecurityFilterChain` bean
- [ ] **Spring Data**: `CrudRepository.findById()` returns `Optional<T>` — update null checks
- [ ] **Actuator**: `/actuator/health` endpoint format changed — update monitoring configs
- [ ] **Parent POM**: Bump `spring-boot-starter-parent` to `3.x.x`; Java baseline is now 17

---

## Migration PR Structure

A well-formed Java modernization PR should include:

**Title:** `feat: modernize inventory-service to Java 17 + Spring Boot 3.x`

**Description sections:**
1. **What changed** — bullet list of files modified and why
2. **Migration highlights** — specific Java 17 features used (records, streams, LocalDateTime)
3. **Breaking changes** — any API contract changes (none if backwards-compatible)
4. **Testing** — test coverage before/after; `mvn test` output
5. **Security** — confirm no hardcoded secrets; credentials moved to environment variables

---

## Key Modernization Prompts (for the presenter)

```
Assess the legacy inventory-service and produce a modernization plan.
Identify all Java 8 anti-patterns, hardcoded secrets, and missing infrastructure.
```

```
Modernize InventoryItem.java to use a Java record.
Modernize InventoryService.java to use streams and LocalDateTime.
Run both changes in parallel.
```

```
Add JUnit 5 unit tests for InventoryService covering: findAll, findById (found),
findById (not found), create, and delete.
```
