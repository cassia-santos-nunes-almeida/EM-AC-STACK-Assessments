# Claude Code Context Files — Deep Content Audit & Migration Plan

**Date:** 2026-03-22
**Files analyzed:** 10 local + 2 from separate repo (CLAUDE.md, PATTERNS.md, SESSION.md, context.md, context-template.md, personal-preferences.md, context-evaluator/SKILL.md, circuitikz/SKILL.md, 00_prompt_evaluation.md, 01_exam_overview.md, stack-xml-generator/SKILL.md, stack-xml-generator/references/stack-xml-conventions.md)

---

## 1. Complete content map — what lives where

### CLAUDE.md (465 lines) — the heaviest file

| Section | Lines | Unique? | Also exists in |
|---------|-------|---------|----------------|
| §1 Project Identity (owner, courses, textbooks, notation) | 1–21 | **Unique** | — |
| §2 Behavior Defaults (tone, env, confirm intent) | 23–37 | Partial overlap | personal-preferences.md (tone, confirm behavior) |
| §3 Task Decomposition | 39–68 | **Unique** | — |
| §4 Self-Verification | 70–77 | **Unique** | — |
| §5 Session Protocols (open/close) | 79–106 | **Unique** | context-evaluator/SKILL.md references it |
| §6 Cross-Skill Rules (writing, code, files) | 108–127 | Partial overlap | personal-preferences.md (banned words, tone) |
| §7 Skill Index | 129–134 | **Unique but incomplete** | Only lists 2 of 5+ skills |
| Project Overview | 137–148 | **DUPLICATE** | context.md lines 1–11 |
| Repository Structure | 149–185 | **DUPLICATE** (partially stale) | context.md lines 28–52 (also stale) |
| Adding New Content | 187–193 | **DUPLICATE** | context.md lines 54–58 |
| STACK XML Conventions | 194–244 | **DUPLICATE** (see revised_stack_analysis.md) | stack-xml-generator/SKILL.md has same content |
| Maxima CAS Patterns | 245–273 | **Partially unique** — RLC formulas + damping are unique; randomization patterns are duplicated | stack-xml-generator/SKILL.md has generic patterns |
| CircuiTikZ section (pipeline, .tex structure, layout, components, embedding, switches) | 274–370 | **DUPLICATE** | circuitikz/SKILL.md has same content |
| PRT Validation Methodology | 372–398 | **DUPLICATE** (see revised_stack_analysis.md) | stack-xml-generator/SKILL.md has identical checklist |
| Known Issues / Pending Work | 400–406 | **Unique** | SESSION.md has related items |
| Workflow Guidelines | 408–430 | **Partial overlap with §3** | — |
| Visual Style & Diagram Resources | 432–462 | **DUPLICATE** | circuitikz/SKILL.md |

### context.md (144 lines)

| Section | Lines | Unique? | Also exists in |
|---------|-------|---------|----------------|
| Project Overview | 1–11 | DUPLICATE | CLAUDE.md 137–148 |
| Tech Stack table | 13–26 | **More detailed than CLAUDE.md** | CLAUDE.md has partial inline |
| Architecture tree | 28–52 | DUPLICATE (stale — missing week11-13) | CLAUDE.md 149–185 |
| Adding new content | 54–58 | DUPLICATE | CLAUDE.md 187–193 |
| Diagram Embedding Strategy | 60–64 | DUPLICATE | CLAUDE.md 338–344 |
| **Content Summary — Midterm Week 9** | 66–82 | **UNIQUE — would be lost** | — |
| **Content Summary — Week 10** | 84–93 | **UNIQUE — would be lost** (stale: missing weeks 11–13) | — |
| Key Constraints — Technical | 95–104 | Partial overlap | CLAUDE.md has some inline |
| **Key Constraints — Pedagogical** | 106–111 | **UNIQUE — would be lost** | — |
| **Key Constraints — Accessibility** | 113–117 | **UNIQUE — would be lost** | — |
| Quality Assurance | 119–124 | References CLAUDE.md PRT section | — |
| **"Never Suggest" list (11 items)** | 126–137 | **UNIQUE — would be lost** | — |

### personal-preferences.md (58 lines)

| Section | Unique? | Also exists in |
|---------|---------|----------------|
| Communication Style (direct, structured, proactive) | Partial overlap | CLAUDE.md §2 |
| How I Give Instructions | **Unique** | — |
| Coding and Technical Preferences | Partial overlap | CLAUDE.md §2, §6 |
| **Things Claude Gets Wrong** | **UNIQUE — would be lost** | — |
| **Things to Avoid (no emoji, no confirmation loop, no splitting)** | **UNIQUE — would be lost** | CLAUDE.md §2 has some |
| How I Like Problems Flagged | **Unique** | — |
| Formatting preferences | **Unique** | — |

### PATTERNS.md (274 lines) — cleanest file

| Content | Count | Status |
|---------|-------|--------|
| STACK patterns | 20 (P-STACK-01 to P-STACK-20) | Current |
| DIAG patterns | 7 (P-DIAG-01 to P-DIAG-07) | Missing P-DIAG-08 (snapSizeX/Y) |
| MSG patterns | 3 (P-MSG-01 to P-MSG-03) | Current |
| ENV patterns | 3 (P-ENV-01 to P-ENV-03) | Current |
| EXEC patterns | 1 (P-EXEC-01) | Current |
| Template | 1 (audit said duplicate — I found only 1) | Clean |

### decisions-log.md (290 lines)

22 decisions documented (2026-02-22 to 2026-03-10). Missing 12 days of decisions.

### SESSION.md — ephemeral, correct by design

### context-evaluator/SKILL.md — thin routing file (correct)

### circuitikz/SKILL.md — self-contained skill file (good, but duplicated in CLAUDE.md)

### 00_prompt_evaluation.md + 01_exam_overview.md — documentation files, not context files

---

## 2. Duplication inventory

These are information blocks that exist in 2+ files. Each is a risk for drift.

| # | Content | File A | File B | Which is more complete? |
|---|---------|--------|--------|------------------------|
| D1 | Project Overview (what this project is) | CLAUDE.md 137–148 | context.md 1–11 | Nearly identical |
| D2 | Repository tree | CLAUDE.md 149–185 | context.md 28–52 | CLAUDE.md has weeks 11–12; both missing week13 |
| D3 | Adding new content pattern | CLAUDE.md 187–193 | context.md 54–58 | Identical |
| D4 | Diagram embedding strategy | CLAUDE.md 338–344 | context.md 60–64 | context.md slightly more detailed |
| D5 | .tex file structure | CLAUDE.md 290–303 | circuitikz/SKILL.md | Identical |
| D6 | CircuiTikZ components table | CLAUDE.md 316–328 | circuitikz/SKILL.md | Identical |
| D7 | Complex math labels (\dfrac) | CLAUDE.md 329–336 | circuitikz/SKILL.md | Identical |
| D8 | Compilation pipeline commands | CLAUDE.md 280–288 | circuitikz/SKILL.md | Identical |
| D9 | Layout rules | CLAUDE.md 307–312 | circuitikz/SKILL.md | CLAUDE.md slightly expanded |
| D10 | Tone/directness | CLAUDE.md §2 | personal-preferences.md | preferences.md more detailed |
| D11 | Banned words / writing rules | CLAUDE.md §6 | personal-preferences.md + PATTERNS.md P-MSG-* | Split across 3 files |
| D12 | "Confirm before acting" | CLAUDE.md §2, §3 | personal-preferences.md "Things to Avoid" | Slightly different angles |
| D13 | Workflow/task decomposition | CLAUDE.md §3 | CLAUDE.md §Workflow Guidelines (408–430) | **Self-duplication within CLAUDE.md** |
| D14 | Syntax hints table | CLAUDE.md 196–215 | stack-xml-generator/SKILL.md | Identical |
| D15 | Grading (PRT) rules table | CLAUDE.md 226–234 | stack-xml-generator/SKILL.md | Identical |
| D16 | Input configuration table | CLAUDE.md 237–244 | stack-xml-generator/SKILL.md | Identical |
| D17 | PRT Validation checklist (4 tiers) | CLAUDE.md 372–398 | stack-xml-generator/SKILL.md | Identical |
| D18 | Maxima randomization patterns | CLAUDE.md 249–255 | stack-xml-generator/SKILL.md | Identical |
| D19 | Progressive hints spec | CLAUDE.md 217–224 | stack-xml-generator/SKILL.md | Identical |

**Total: 19 duplications. 9 between CLAUDE.md and local files, 6 between CLAUDE.md and the stack-xml-generator skill (separate repo), 4 within CLAUDE.md or across 3+ files.**

---

## 3. Orphaned content — exists in only one file

If that file gets deleted or gutted during reorganization, this content is lost.

| # | Content | Where it lives | Risk level |
|---|---------|----------------|------------|
| O1 | Content Summary tables (Midterm Week 9 + Weekly Week 10) | context.md 66–93 | **HIGH** — only record of question counts, points, topics |
| O2 | Pedagogical Constraints | context.md 106–111 | **HIGH** — "RLC transients excluded from exam" etc. |
| O3 | Accessibility Constraints | context.md 113–117 | MEDIUM |
| O4 | "Never Suggest" list (11 items) | context.md 126–137 | **HIGH** — prevents repeated bad suggestions |
| O5 | Things Claude Gets Wrong | personal-preferences.md | MEDIUM — behavioral guidance |
| O6 | How I Give Instructions | personal-preferences.md | MEDIUM |
| O7 | Problem flagging format | personal-preferences.md | LOW |
| O8 | Multi-switch topology rules (SW1-SW4 pattern) | CLAUDE.md 345–370 | **HIGH** — detailed design pattern |
| O9 | Maxima CAS Patterns (RLC formulas, damping) | CLAUDE.md 245–273 | **HIGH** — critical reference |
| O10 | Input Configuration table | CLAUDE.md 237–244 | LOW — also in stack-xml-generator/SKILL.md |
| O11 | STACK XML Conventions (syntax hints, progressive hints, grading rules) | CLAUDE.md 194–236 | LOW — also in stack-xml-generator/SKILL.md |
| O12 | PRT Validation Methodology (4 tiers) | CLAUDE.md 372–398 | LOW — also in stack-xml-generator/SKILL.md |
| O13 | Progressive Hint Unlocking plan | CLAUDE.md 400–406 | LOW — aspirational |

**Key insight: The truly unique EM&AC-specific content in CLAUDE.md (O8: multi-switch topology, O9: RLC formulas/damping) must stay in CLAUDE.md. The generic STACK content (O10–O12) already exists in stack-xml-generator/SKILL.md and can be removed from CLAUDE.md with a reference. See `revised_stack_analysis.md` for the corrected plan.**

---

## 4. Stale content

| File | What's stale | Impact |
|------|-------------|--------|
| CLAUDE.md header | Says "Testing-Codes" — audit says repo renamed to "EM-AC-STACK-Assessments" | Confusing if repo was actually renamed |
| CLAUDE.md tree | Missing `weekly/week13/` | Claude won't know week13 exists |
| context.md tree | Missing `weekly/week11/`, `week12/`, `week13/` | Worse than CLAUDE.md |
| context.md content summary | Only shows Week 10 | No record of weeks 11–13 question sets |
| context.md status | "Week 10 status: All 5 questions passed" | No status for later weeks |
| context.md Last Updated | 2026-03-07 (15 days) | — |
| decisions-log.md | Last entry 2026-03-10 | Missing weeks 12–13 decisions |
| personal-preferences.md | Last Updated 2026-02-23 (27 days) | Still has `<!-- Review and edit these -->` placeholder |
| SESSION.md | Current session, as expected | Not a real issue |

---

## 5. Structural problems

### 5a. CLAUDE.md is doing too many jobs

Currently CLAUDE.md serves as:
1. **Identity card** (who you are, your courses, your textbooks) — §1
2. **Behavior contract** (how Claude should act) — §2, §3, §4
3. **Session protocol** (open/close workflow) — §5
4. **Cross-skill rules** (writing, code, files) — §6
5. **Skill index** (routing table) — §7
6. **Project overview** (what this repo is) — duplicate of context.md
7. **STACK authoring reference** (XML conventions, Maxima patterns, PRT validation) — generic parts duplicated in stack-xml-generator; only RLC/damping/switch rules are unique
8. **CircuiTikZ reference** — duplicate of circuitikz/SKILL.md
9. **Diagram style guide** — duplicate of circuitikz/SKILL.md
10. **Task workflow guide** — partially duplicates §3

Jobs 1–6 are legitimate for CLAUDE.md. Job 7 should keep only EM&AC-specific STACK content (RLC formulas, damping, multi-switch) and reference the generic skill for everything else. Jobs 8–10 should be delegated.

### 5b. context.md role is confused

It tries to be both:
- A "stable architecture facts" file (which it should be)
- A mirror of CLAUDE.md's project overview (which creates drift)

Its truly unique value is: Content Summary tables, Pedagogical/Accessibility Constraints, and the "Never Suggest" list.

### 5c. CircuiTikZ content exists in both CLAUDE.md and circuitikz/SKILL.md

CLAUDE.md §6 says: "Never duplicate content between CLAUDE.md and a SKILL.md — reference by name."
This rule is currently violated by CLAUDE.md itself (lines 274–462).

### 5d. No JSXGraph skill file

7 fix rounds produced 5 patterns (P-STACK-16 to P-STACK-20) but there's no consolidated authoring guide. The audit flagged this correctly.

### 5e. personal-preferences.md is partially orphaned

context-evaluator/SKILL.md lists it in its file table, but nothing in the session-open protocol explicitly says "read personal-preferences.md." It's loaded only if the context-evaluator skill is activated.

---

## 6. Goals for the reorganized system

Based on your stated needs and the WAT principles worth adopting:

1. **Zero information loss** — every unique content item must survive the migration
2. **One source of truth per topic** — eliminate all 19 duplications
3. **Self-improvement loop** — PATTERNS.md is working; keep it exactly as-is
4. **Regular checking** — session open/close protocol handles this; needs minor refinement
5. **Learn from mistakes** — PATTERNS.md + decisions-log.md cover this; need freshness discipline
6. **Slim CLAUDE.md** — currently 465 lines; target ~200 lines for the "always read" file
7. **No orphaned critical content** — everything must have a clear owner file

---

## 7. Recommended target structure

```
Testing-Codes/  (or EM-AC-STACK-Assessments/ — confirm actual repo name)
├── CLAUDE.md                    # Identity + rules + routing + EM&AC-specific STACK content (~180 lines)
├── PATTERNS.md                  # Mistakes → lessons (keep as-is, clean up)
├── SESSION.md                   # Ephemeral session state (keep as-is)
├── .claude/
│   ├── context.md               # Stable project facts (unique content only)
│   ├── decisions-log.md         # Why decisions were made
│   ├── preferences.md           # Communication + coding style
│   └── skills/
│       ├── context-evaluator/
│       │   └── SKILL.md         # Session management routing
│       └── circuitikz/
│           └── SKILL.md + refs  # Circuit diagram authoring (absorbs CLAUDE.md §CircuiTikZ)

my-claude-skill/ (separate repo — generic reusable skills)
└── stack-xml-generator/
    ├── SKILL.md                 # Generic STACK conventions (already exists, covers generic STACK content)
    ├── references/
    │   ├── stack-xml-conventions.md  # XML reference (already exists)
    │   └── jsxgraph-conventions.md   # NEW: consolidated JSXGraph authoring guide
    └── README.md
```

**NOTE:** The original version of this section proposed creating `stack-authoring/` and `jsxgraph/` as new local skills. This was WRONG — the generic STACK skill already exists in the separate repo. See `revised_stack_analysis.md` for the corrected plan.

### What changes

| Current file | What stays | What moves out | What moves in |
|-------------|-----------|----------------|---------------|
| **CLAUDE.md** | §1–§7 (identity, behavior, task decomp, verification, session protocols, cross-skill rules, skill index) + EM&AC-specific STACK content (RLC formulas, damping, multi-switch) | Remove: Project Overview (→ context.md), Repo Structure (→ context.md), CircuiTikZ section (→ circuitikz/SKILL.md), Diagram Style (→ circuitikz/SKILL.md), generic STACK content (→ already in stack-xml-generator skill), duplicate Workflow section | Add: updated skill index (all skills), reference to stack-xml-generator for generic STACK rules |
| **context.md** | Content Summaries, Pedagogical Constraints, Accessibility Constraints, Never Suggest, Tech Stack table | Remove: Project Overview paragraph, Architecture tree, Adding New Content, Diagram Embedding, QA section (all duplicates of CLAUDE.md) | Add: weeks 11–13 content summaries, keep repo structure as single source of truth |
| **personal-preferences.md** | All current content | — | Add: explicit reference in session-open protocol |
| **PATTERNS.md** | Everything | — | Add: P-DIAG-08 (snapSizeX/Y if confirmed) |
| **decisions-log.md** | Everything | — | Add: catch-up block for weeks 12–13 |
| **circuitikz/SKILL.md** | Everything | — | Absorb: multi-switch topology rules, diagram style rules from CLAUDE.md |
| **stack-xml-generator/SKILL.md** (separate repo) | Everything | — | Add: JSXGraph conventions section + reference file |

### Line count projections

| File | Current | After migration |
|------|---------|----------------|
| CLAUDE.md | 465 | ~180 (removes ~285 lines of duplicates + delegated content, keeps ~42 lines of EM&AC-specific STACK) |
| context.md | 144 | ~110 (removes duplicates, adds weeks 11–13 summaries) |
| circuitikz/SKILL.md | 90 | ~140 (absorbs CLAUDE.md CircuiTikZ content) |
| stack-xml-generator/SKILL.md (separate repo) | 120 | ~150 (adds JSXGraph section) |

---

## 8. Migration checklist — nothing gets lost

Every unique content item mapped to its destination:

| # | Content item | Source | Destination | Status |
|---|-------------|--------|-------------|--------|
| 1 | Project Identity (§1) | CLAUDE.md | CLAUDE.md (stays) | — |
| 2 | Behavior Defaults (§2) | CLAUDE.md | CLAUDE.md (stays) | — |
| 3 | Task Decomposition (§3) | CLAUDE.md | CLAUDE.md (stays, merge with §Workflow) | — |
| 4 | Self-Verification (§4) | CLAUDE.md | CLAUDE.md (stays) | — |
| 5 | Session Protocols (§5) | CLAUDE.md | CLAUDE.md (stays, add preferences.md to read list) | — |
| 6 | Cross-Skill Rules (§6) | CLAUDE.md | CLAUDE.md (stays) | — |
| 7 | Skill Index (§7) | CLAUDE.md | CLAUDE.md (expand to all skills) | — |
| 8 | Project Overview paragraph | CLAUDE.md + context.md | context.md only | — |
| 9 | Repository Structure tree | CLAUDE.md + context.md | context.md only (update with weeks 11–13) | — |
| 10 | Adding New Content | CLAUDE.md + context.md | context.md only | — |
| 11 | Tech Stack table | context.md | context.md (stays) | — |
| 12 | Content Summary — Midterm | context.md | context.md (stays) | — |
| 13 | Content Summary — Weekly | context.md | context.md (stays, add weeks 11–13) | — |
| 14 | Pedagogical Constraints | context.md | context.md (stays) | — |
| 15 | Accessibility Constraints | context.md | context.md (stays) | — |
| 16 | Never Suggest list | context.md | context.md (stays) | — |
| 17 | STACK XML Conventions (generic) | CLAUDE.md + stack-xml-generator | stack-xml-generator ONLY (delete from CLAUDE.md, add reference) | — |
| 18 | Syntax Hints table | CLAUDE.md + stack-xml-generator | stack-xml-generator ONLY (delete from CLAUDE.md) | — |
| 19 | Progressive Hints spec | CLAUDE.md + stack-xml-generator | stack-xml-generator ONLY (delete from CLAUDE.md) | — |
| 20 | Grading (PRT) Rules table | CLAUDE.md + stack-xml-generator | stack-xml-generator ONLY (delete from CLAUDE.md) | — |
| 21 | Input Configuration table | CLAUDE.md + stack-xml-generator | stack-xml-generator ONLY (delete from CLAUDE.md) | — |
| 22 | Maxima CAS Patterns (generic: randomization, syntax) | CLAUDE.md + stack-xml-generator | stack-xml-generator ONLY (delete generic parts from CLAUDE.md) | — |
| 23 | RLC Circuit Formulas table (EM&AC-specific) | CLAUDE.md only | **CLAUDE.md (stays)** — not in generic skill | — |
| 24 | PRT Validation (4 tiers) | CLAUDE.md + stack-xml-generator | stack-xml-generator ONLY (delete from CLAUDE.md) | — |
| 25 | Multi-switch topology rules | CLAUDE.md | circuitikz/SKILL.md (merge) | — |
| 26 | .tex file structure | CLAUDE.md + circuitikz/SKILL.md | circuitikz/SKILL.md only | — |
| 27 | Components table | CLAUDE.md + circuitikz/SKILL.md | circuitikz/SKILL.md only | — |
| 28 | Complex math labels | CLAUDE.md + circuitikz/SKILL.md | circuitikz/SKILL.md only | — |
| 29 | Compilation pipeline | CLAUDE.md + circuitikz/SKILL.md | circuitikz/SKILL.md only | — |
| 30 | Layout rules | CLAUDE.md + circuitikz/SKILL.md | circuitikz/SKILL.md only | — |
| 31 | Diagram Style Rules | CLAUDE.md | circuitikz/SKILL.md (merge) | — |
| 32 | Diagram embedding strategy | CLAUDE.md + context.md | context.md only | — |
| 33 | Known Issues / Pending Work | CLAUDE.md | SESSION.md (move active items) | — |
| 34 | JSXGraph patterns (P-STACK-16–20) | PATTERNS.md | PATTERNS.md (stays) + stack-xml-generator (new JSXGraph section + reference file) | — |
| 35 | Communication Style | personal-preferences.md | preferences.md (stays) | — |
| 36 | Things Claude Gets Wrong | personal-preferences.md | preferences.md (stays) | — |
| 37 | How I Give Instructions | personal-preferences.md | preferences.md (stays) | — |
| 38 | Problem flagging format | personal-preferences.md | preferences.md (stays) | — |
| 39 | Workflow Guidelines (parallel agents) | CLAUDE.md 408–430 | Merge into §3 Task Decomposition | — |

**39 content items tracked. Zero items deleted.**

---

## 9. What to take from the WAT framework

The WAT framework has three principles worth adopting. You already implement all three — just not explicitly named:

| WAT principle | Your equivalent | Status |
|---------------|----------------|--------|
| "Look for existing tools first" | Skill Index §7 + "check PATTERNS.md before starting" | Working, but skill index is incomplete |
| "Learn and adapt when things fail" | PATTERNS.md + session-close protocol | **Your strongest system feature** |
| "Keep workflows current" | decisions-log.md + context.md updates | Needs freshness discipline (12+ days stale) |

What you do NOT need from WAT: the `tools/` + `workflows/` + `.tmp/` directory structure, the Python script execution model, the `.env` credentials pattern. These solve automation problems you don't have in this project.

---

## 10. Execution order

**Phase 0 — Backup (MANDATORY before any edits)**
0. Create a git commit with all current files as-is (message: `chore: snapshot before context file migration`). If there are uncommitted changes, commit them first. This is the rollback point — every file must be recoverable from this commit. Do NOT proceed to Phase 1 until this commit exists.

**Phase 1 — Eliminate duplications (biggest risk reduction)**
1. Remove generic STACK content from CLAUDE.md (syntax hints, PRT rules, input config, validation checklist, Maxima randomization) — these already exist in stack-xml-generator/SKILL.md. Replace with a reference line. Keep EM&AC-specific content (RLC formulas, damping classification, multi-switch topology).
2. Move CircuiTikZ content from CLAUDE.md to circuitikz/SKILL.md
3. Remove duplicate sections from context.md (Project Overview, tree, Adding Content)
4. Remove duplicate sections from CLAUDE.md (Project Overview, tree, Diagram Style)
5. Merge CLAUDE.md §Workflow Guidelines (408–430) into §3 Task Decomposition
6. Verify: every item in the migration checklist has exactly one home

**Phase 2 — Fix staleness**
7. Update repo structure in context.md (add weeks 11–13)
8. Confirm actual repo name (Testing-Codes vs EM-AC-STACK-Assessments)
9. Add weeks 11–13 content summaries to context.md
10. Catch-up block in decisions-log.md for weeks 12–13
11. Clean personal-preferences.md (remove placeholder comment, update date)

**Phase 3 — New content**
12. Add JSXGraph section to stack-xml-generator/SKILL.md + create references/jsxgraph-conventions.md (in separate repo)
13. Update Skill Index in CLAUDE.md (all skills including stack-xml-generator)
14. Add personal-preferences.md to session-open read list in §5

**Phase 4 — Self-Verification (MANDATORY — do not return control until complete)**

Self-verify your work by testing it end to end. Do not return control until you have met the requirements and the result is working as expected and optimized.

15. **Migration checklist audit:** Walk through every row in §8 (39 items). For each item, open the destination file and confirm the content is present and correct. If any item is missing, fix it before continuing.
16. **Duplication check:** For each of the 19 duplications in §2, confirm the content now exists in exactly ONE file (not zero, not two).
17. **Orphan check:** For each of the 13 orphaned items in §3, confirm the content still exists and has not been accidentally deleted.
18. **Cross-reference integrity:** Every skill referenced in CLAUDE.md §7 Skill Index must have a corresponding SKILL.md file. Every file referenced in the session-open protocol (§5) must exist.
19. **Read every modified file end-to-end.** Check for: broken references to deleted sections, stale "Last Updated" dates, placeholder text that should have been removed, and sections that reference content that moved elsewhere.
20. **Run the original audit prompt again** and confirm all scores improved. If any score dropped, diagnose why and fix before returning control.
