# EM-AC-STACK-Assessments

## 1. Project Identity

Owner: Cássia Almeida (she/her), Associate Professor, LUT University (Finland)
Languages: English (primary for technical work), Finnish (institutional), Portuguese (personal)
Expertise level: Senior — skip fundamentals unless asked. Precision over completeness.
Role context: Engineering educator building AI-integrated teaching tools, assessment systems, and interactive web applications for electromagnetic theory and circuit analysis students.

Active courses:
* BL30A0350 — Electromagnetism and Circuit Analysis (EM&AC)
* LES10A020 — Engineering Physics (EP, co-taught with Mikko Äijälä and Ayesha Sadiqa)

Reference textbooks:
* Ulaby — Fundamentals of Applied Electromagnetics
* Ida — Engineering Electromagnetics
* Nilsson & Riedel — Electric Circuits

Notation conflict (known): Cross-sectional area: A (Nilsson) vs. S (Ulaby). Flux linkage: λ (Nilsson) vs. Λ (Ulaby). Always use the convention of the course being worked on — ask if unclear.

## 2. Behavior Defaults

* Architecture-first: explain structure before writing code.
* Confirm intent before writing code for any non-trivial task.
* Flag risks, edge cases, and conflicts proactively — do not wait to be asked.
* Only modify explicitly requested parts. Leave everything else untouched.
* When multiple options exist, present them with tradeoffs — let Cássia decide.
* Never add new ideas to messages or documents. Never remove existing ones. Only adjust what is asked.

Tone: Professional, direct, warm, natural. No flattery. No filler.

Environment:
* OS: Windows / PowerShell
* Python: use python — not python3 (not on PATH)
* Claude Code active — use session teleport when needed; re-authenticate with /login if token expired

## 3. Task Decomposition and Execution Strategy

Before starting any non-trivial task, assess scope:

**Step 1 — Size check**
If a task has more than 3 distinct deliverables, affects more than 2 files,
or requires more than one skill — it is too large to execute as one unit.
Decompose it before starting. Never attempt a large task as a single block.

**Step 2 — Dependency map**
For each subtask, determine:
- Does it depend on the output of another subtask? → sequential
- Can it proceed independently? → parallel candidate

**Step 3 — Execution order**
Sequential: use when subtask B needs output from A.
  Example: generate Maxima CAS code → then build XML wrapper around it.
Parallel: use when subtasks share no inputs/outputs.
  Example: draft 3 STACK questions on different topics simultaneously.
Batched parallel: group independent subtasks, execute the batch, then proceed.
  Example: generate all randomization blocks → then all PRT trees → then all XML wrappers.

**Step 4 — Confirm before executing**
Present the subtask list and proposed execution order BEFORE starting work.
Wait for confirmation unless the task is clearly routine.

**Step 5 — Report at each boundary**
At the end of each subtask or batch: report what was completed, what comes
next, and any blocker or decision needed before proceeding.
Do not silently chain subtasks without a checkpoint.

## 4. Self-Verification (applies to all tasks)

Before returning any output:
1. Goal analysis — State the explicit and implicit goals. What does success look like?
2. Assumption audit — List every inference made that was not directly stated in the input. For each: what was the basis, and what would change if the assumption is wrong?
3. Gap identification — What is missing, ambiguous, or likely to fall short?
4. End-to-end self-test — Test output against all stated goals and identified risks. Iterate until requirements are met and output is optimized. Do not return control until this is complete.
5. Pattern check — Before finalizing, check PATTERNS.md. If the output would trigger a known pattern, apply the documented fix automatically.

## 5. Session Protocols

### Session Open
At the start of every session, before any task work:
1. Read CLAUDE.md (this file) — confirm active constraints and project identity.
2. Read PATTERNS.md — load all accumulated corrections and rules. Treat every entry as a hard constraint, not a suggestion.
3. Read `.claude/skill/context_evaluator/shared-patterns.md` — cross-project rules (synced from my-claude-skills). When a rule here conflicts with a project-specific PATTERNS.md entry, the project-specific rule wins.
4. Read SESSION.md if present — resume from last known state.
5. Read `.claude/skill/context_evaluator/context.md` — stable architecture facts.
6. Read `.claude/skill/context_evaluator/personal-preferences.md` — communication and coding style.
7. Confirm readiness: state which skills are relevant to today's work and flag any conflict between loaded files.

Do not begin task work until these steps are confirmed.
To trigger: **open session**, **load context**, **new session**, **let's start**, **let's start the day**, **where did we stop**, **good morning**, or similar.

### Session Close
At the end of every session, before returning control:
1. Review the full session for recurring corrections or repeated assumptions — anything said more than once, or any mistake that appeared in more than one place.
2. For each pattern found:
   - Produce a concrete rule in plain language.
   - Add it to PATTERNS.md under the relevant category.
   - State: "Pattern detected: [X]. Rule added: [Y]."
3. Write SESSION.md:
   - What was completed (with file names and locations).
   - What is in progress (enough context to resume cold).
   - Open decisions or blockers.
   - Which PATTERNS.md entries were triggered today.
4. If any SKILL.md should be updated based on today's work, state the proposed change explicitly and ask for confirmation before writing.
5. **Handover (optional):** If ending work for today, ask once: "Do you want me to save a handover to Notion before we close?" If yes, invoke the handover skill. Context-evaluator writes local state first, handover reads it second.

To trigger: **wrap up**, **close session**, **let's call it a day**, **close the work**, **finish this session**, **I'm done for now**, **that's all for today**, or similar.

### Session Boundary Protocol (summary)

At **session end**, run both protocols in order:
1. **context_evaluator** -- writes `SESSION.md` + `PATTERNS.md` (local project state)
2. **handover** -- saves structured handover to Notion (cross-chat continuity)

At **session start**, context_evaluator loads local files automatically. Use handover **FETCH** only when resuming in a brand-new chat that lacks prior context.

### Correction Capture (during session)
When the user corrects an error or overrides a default behavior, assess: is this a one-time adjustment or a repeatable rule? If unclear, ask: "Should this become a permanent rule in PATTERNS.md?" If yes, draft the entry immediately.

## 6. Cross-Skill Rules

These apply to all skills. Skills do not repeat them.

### Writing and communication
* Never use: "flagging", "thanks for flagging" — use "thanks for the heads-up" or "thanks for pointing that out"
* Email sign-off: "Best regards," — never "Best,"
* Sign as: "Cássia" — never full name in sign-off
* Anti-AI banned words: "crucial", "vital", "leverage", "delve", "navigate", "landscape", "groundbreaking", "game-changer", "it's worth noting", "at the end of the day", "in conclusion"

### Code
* Confirm intent before writing non-trivial code
* Explain architectural choices when making decisions that affect structure
* Flag performance and edge cases proactively

### Files and structure
* Check PATTERNS.md before starting any task in a known domain
* Session state lives in SESSION.md — write it at close, read it at open
* Never duplicate content between CLAUDE.md and a SKILL.md — reference by name

## 7. Skills

| Skill | Purpose | Location |
|-------|---------|----------|
| context-evaluator | Session lifecycle, context loading, correction capture | `.claude/skill/context_evaluator/SKILL.md` |
| circuitikz-circuit-diagrams | LaTeX circuit diagram generation | `.claude/skill/circuitikz-latex-circuit-diagrams/SKILL.md` |
| stack-xml-generator | STACK XML authoring, Maxima CAS, PRT validation | `.claude/skill/stack-xml-generator/SKILL.md` |
| stack-question-validator | Post-generation quality check, PATTERNS compliance | `.claude/skill/stack-question-validator/SKILL.md` |

## Reference

| Topic | File |
|-------|------|
| Architecture, tech stack, constraints | `.claude/skill/context_evaluator/context.md` |
| Current session state, pending tasks, blockers | `.claude/skill/context_evaluator/SESSION.md` |
| Accumulated corrections and hard constraints | `PATTERNS.md` |
| All design decisions with rationale | `.claude/skill/context_evaluator/decisions-log.md` |
| Communication and coding preferences | `.claude/skill/context_evaluator/personal-preferences.md` |
| Cross-project rules (synced from my-claude-skills) | `.claude/skill/context_evaluator/shared-patterns.md` |

## STACK XML Conventions

All generic STACK XML rules (syntax hints, progressive hints, grading/PRT rules, input configuration, Maxima randomization patterns, PRT validation checklist) → see **stack-xml-generator skill** (`.claude/skill/stack-xml-generator/SKILL.md`).

PATTERNS.md entries P-STACK-01 through P-STACK-23 are hard constraints that override any skill defaults.

### EM&AC-Specific: RLC Circuit Formulas

| Circuit | alpha | omega0 | dv/dt(0+) or di/dt(0+) |
|---------|-------|--------|-------------------------|
| Parallel RLC | `1/(2*R*C)` | `1/sqrt(L*C)` | `dv/dt(0+) = -(1/C)*(V0/R + I0)` from KCL |
| Series RLC | `R/(2*L)` | `1/sqrt(L*C)` | `di/dt(0+) = (1/L)*(V0 - R*I0)` |

### Key Patterns

- **Natural response:** No forced term. `v_final = 0` (all exponentials decay to zero).
- **Step response:** Has forced term. `v_final = V_source * (voltage divider)`.
- **Pre-switch DC analysis:** Inductor = short circuit, capacitor = open circuit.
- **Damping classification:**
  - `alpha > omega0` → overdamped (two real roots)
  - `alpha < omega0` → underdamped (complex conjugate roots)
  - `alpha = omega0` → critically damped (repeated root)

## CircuiTikZ / TikZ Circuit Diagrams

All diagram authoring rules, components, compilation pipeline, layout conventions, multi-switch topology patterns, and embedding strategies → see **circuitikz-circuit-diagrams skill** (`.claude/skill/circuitikz-latex-circuit-diagrams/SKILL.md`).

Before creating any diagram, also read:
- `.claude/skill/circuitikz-latex-circuit-diagrams/references/circuit-patterns.md` — 8 standard topology templates
- `shared/templates/circuitikz_template.tex` — starter template

### Task Granularity

- **1–2 questions per agent**, **1 diagram per agent** — validate independently before bundling
- Separate concerns: randomization → solution derivation → PRT structure → grading code

## 8. Question Design Protocol

### Pre-XML Spec Gate (all new questions)

Do not generate STACK XML until all five spec items are produced and confirmed.

**Spec 1 — Learning objective:**
"Students will be able to [Bloom's verb] [topic] given [context]."
Permitted verbs — Easy: recall, identify, apply. Medium: analyze, calculate, convert, interpret. Difficult: synthesize, evaluate, design.

**Spec 2 — Error model:** 2–4 specific errors with the answer each produces. These drive PRT feedback branches.

**Spec 3 — PRT logic tree (text form):** Full tree before XML. Every branch terminates. Every feedback addresses an error model from Spec 2.

**Spec 4 — Parameter specification:** Per randomized parameter: name, type, units, bounds/values, degenerate exclusions, total variants.

**Spec 5 — Coverage check:** Difficulty tier, which week's objectives, whether already assessed this week.

### Exam Companion Decision Gate

Before generating exam question XML, ask once per session:
"Will students need to show handwritten working? If yes, which questions need companion handwritten notes questions?"
If yes, generate companion `_handwritten_notes` essay questions in the same XML export.

## Last Updated

2026-04-07 (Session 1: added §8 Question Design Protocol, MCQ shuffle fix, PRT validator)
