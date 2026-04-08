# SESSION.md — Current State

Overwritten at every session close. Read at every session open.
Last updated: 2026-04-08 · Session focus: Cross-repo skill centralization and audit

## Completed This Session

* [x] **Phase A — my-claude-skills reorganization**
  - Reorganized into `core/`, `personal/`, `style/`, `patterns/`, `scripts/`, `dist/` structure
  - Upgraded context-evaluator to v2.0.0 (info priority, first session, health check, growth mgmt)
  - Merged circuitikz v2.1.0 bidirectionally (canonical components + project additions)
  - Merged JSXGraph into canonical stack-xml-generator
  - Consolidated handover to v2 (§8 patterns, FETCH auto-detect, SESSION.md pre-population)
  - Created shared-patterns.md (10 cross-project rules: P-MSG, P-ENV, P-EXEC)
  - Dropped project-context-manager (absorbed into context-evaluator)
  - Extracted 12 personal skills from .skill ZIPs to folders

* [x] **Phase B — Sync infrastructure**
  - `scripts/sync-to-projects.sh` — hash-based sync with `--dry-run`, Windows Python path handling
  - `scripts/sync-config.json` — maps 5 core skills to 3 project repos with folder name mappings
  - `scripts/build-skills.sh` — generates .skill ZIPs from folders

* [x] **Phase C — EM-AC-STACK-Assessments migration**
  - 7 files synced from canonical
  - CLAUDE.md: shared-patterns loading (step 3), session-close ordering, correction capture, natural trigger phrases
  - PATTERNS.md: cross-cutting rules moved to shared-patterns.md, P-STACK-26–30 added from W14-16 changelog
  - HARD-GATE + rationalization tables on P-STACK-08, P-STACK-09
  - stack-question-validator skill deployed (4-tier post-generation validation)

* [x] **Phase D — EM-CA-Course migration**
  - 6 files synced, CLAUDE.md updated, stale .skill ZIPs deleted

* [x] **Phase E — STACK_XML_Generator deployment**
  - context-evaluator deployed (first context management for this repo)
  - Initial context.md and SESSION.md created

* [x] **Phase F — New skill + enhancements**
  - stack-question-validator created (structure, grading, security, quality tiers)
  - CSO trigger enrichment on all core SKILL.md descriptions
  - Handover updated with SESSION.md pre-population

* [x] **SessionStart hooks** — auto-sync with 45s timeout + fallback warning on all 3 project repos
* [x] **Onboard-project template** — saved to `my-claude-skills/templates/onboard-project.md`
* [x] **Changelog lessons captured** — P-STACK-26 through P-STACK-30 from W14-16 CHANGELOG.md

## Manual Review Items (carried forward)

* [ ] **Exam Q1 V3/V4 PRT grading bug** — pre-existing, needs Moodle testing
* [ ] **Q2 unit checking validation** — needs Moodle import + test
* [ ] **Pre-existing Check 4 failures (5)** — algebraic inputs missing insertstars=1
* [ ] **Pre-existing Check 5 failures (13)** — bare `<` outside CDATA in feedbackvariables
* [ ] **Moodle re-import needed** — all modified XML files

## In Progress (carried forward)

Task: Weeks 10-12 audit fixes (deferred from prior sessions)
Known issues:
  - Week 10 Q4: `{@ans2@}` and `{@ans3@}` in specificfeedback (P-STACK-03)
  - Week 10 Q1: Float literal `1e-7` in questionvariables (P-STACK-06)
  - All weeks 10-12: Missing `<hint>` blocks (15 questions)

Task: Progressive hint unlocking
Last state: Not started
Next step: Research STACK `[[if test="..."]]` conditional blocks

## Open Decisions / Blockers (carried forward)

* [ ] **Exam Q1 V3/V4 correct answer** — needs course content review
* [ ] **Extend units checking** beyond Q2 pilot?
* [ ] **Coverage gaps: weeks 11-12** — missing Q slots

## Patterns Triggered This Session

| Pattern ID | What happened | Action |
|------------|--------------|--------|
| P-EXEC-01 | Large task decomposed into 6 phases (A-F) | Applied — each phase executed sequentially |
| P-EXEC-04 | Hardcoded §N references broke across repos | **New rule added** — route by heading name, not section number |
| P-STACK-26–30 | Changelog design decisions not yet in PATTERNS | **5 new rules added** from W14-16 CHANGELOG |

## §8 — New Patterns for PATTERNS.md

| Category | Title | Status |
|----------|-------|--------|
| P-EXEC-04 | Route by heading name, never by section number | Added to shared-patterns.md |
| P-STACK-26 | Follow-through grading for cascading answers | Added to PATTERNS.md |
| P-STACK-27 | Validate physical model applicability for all parameter sets | Added to PATTERNS.md |
| P-STACK-28 | Guard MCQ error checks against matching correct answer | Added to PATTERNS.md |
| P-STACK-29 | Add conceptual MCQ parts for AI resistance | Added to PATTERNS.md |
| P-STACK-30 | NumRelative on dB values: check magnitude | Added to PATTERNS.md |

## Skills Used This Session

* [x] context-evaluator (session open/close)
* [x] stack-xml-generator (canonical merge)
* [x] circuitikz-circuit-diagrams (canonical merge)
* [x] handover (canonical merge + SESSION.md pre-population)
* [x] stack-question-validator (new — created this session)
