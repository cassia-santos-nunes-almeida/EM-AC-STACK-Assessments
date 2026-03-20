---
name: context-evaluator
description: Manages session context and project state for STACK Exam & Practice Question Builder.
---

# Context Evaluator — Session Management Skill

## Activation

On load, follow the **Session Open** protocol in CLAUDE.md §4.

Read files in order:
1. `CLAUDE.md` — global rules and repo-specific conventions
2. `PATTERNS.md` — accumulated corrections (hard constraints)
3. `SESSION.md` — current session state
4. `context.md` (this directory) — stable architecture facts
5. `decisions-log.md` (this directory) — chronological decision history

Then confirm readiness per CLAUDE.md §4.

## Skill-Specific Files

| File | Purpose | Update frequency |
|------|---------|-----------------|
| `context.md` | Architecture, tech stack, constraints | Rarely (architecture changes) |
| `decisions-log.md` | Chronological decisions with rationale | When decisions are made |
| `personal-preferences.md` | User communication & coding style | Very rarely |

## Session Close

Follow the **Session Close** protocol in CLAUDE.md §4.

## Rules

All session rules, behavior defaults, and cross-skill rules are in CLAUDE.md §§2-5.
All STACK XML conventions, Maxima patterns, and PRT rules are in CLAUDE.md (repo-specific sections).
All accumulated corrections are in PATTERNS.md.
Do not duplicate rules from those files here.
