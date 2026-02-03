# Complexity Classification Guide

## Purpose

Complexity classification determines how thorough each EPCV phase should be.
Correct classification prevents over-engineering simple tasks and under-preparing
for complex ones.

## Classification Criteria

### Simple

**Characteristics**:

- Single file affected
- Isolated change (no cross-file dependencies)
- Clear, unambiguous requirements
- Well-understood area of the codebase
- No architectural implications

**Examples**:

- Fix a typo in a string
- Add a CSS class to an element
- Update a configuration value
- Add a simple utility function
- Fix an off-by-one error

**EPCV Approach**: Abbreviated (5-10 minutes total)

---

### Moderate

**Characteristics**:

- 2-5 files affected
- Some dependencies between changed files
- Clear requirements but multiple implementation choices
- Familiar area with some complexity
- No major architectural changes

**Examples**:

- Add a new API endpoint with validation
- Create a new UI component with state
- Refactor a function and update its callers
- Add error handling to an existing flow
- Implement a new feature in an existing module

**EPCV Approach**: Standard (15-30 minutes total)

---

### Complex

**Characteristics**:

- 5+ files affected
- Cross-cutting concerns (multiple modules/layers)
- Requirements may be ambiguous or incomplete
- Unfamiliar or poorly-documented area
- Architectural implications or decisions needed
- Data migration or schema changes
- Security-sensitive changes

**Examples**:

- Implement authentication/authorization system
- Redesign a core data model
- Add a new integration with external service
- Major refactor across multiple modules
- Performance optimization of critical path
- Database schema migration

**EPCV Approach**: Extended (30+ minutes total)

## Classification Decision Tree

```text
Is only 1 file affected?
├── Yes → Are requirements clear and unambiguous?
│         ├── Yes → SIMPLE
│         └── No  → MODERATE (unclear requirements need more planning)
└── No  → Are 5+ files affected OR architectural decisions needed?
          ├── Yes → COMPLEX
          └── No  → MODERATE
```

## Override Rules

Even if the decision tree says "simple", upgrade to moderate if:

- The file is in a security-sensitive area
- The file is in a performance-critical path
- The change affects a public API
- You're unfamiliar with the area

Even if the decision tree says "moderate", upgrade to complex if:

- Requirements are ambiguous and need clarification
- Multiple valid approaches exist with different tradeoffs
- The change could break backward compatibility
- Data migration is involved
