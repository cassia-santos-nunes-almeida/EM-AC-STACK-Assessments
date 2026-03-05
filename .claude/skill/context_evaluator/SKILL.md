---
name: contex-evaluator
description: Generates randomized Moodle STACK exam questions (XML + Maxima) and SVG circuit diagrams for undergraduate electrical circuits courses.
---

# STACK Exam Builder — Claude Skill Instructions

## Activation

When this skill is loaded, immediately read ALL context files in this order:

1. `personal-preferences.md` — User's communication style and coding preferences (not project-specific)
2. `context.md` — Stable project facts, architecture, constraints
3. `active-session.md` — Current sprint, tasks in progress, immediate next steps
4. `decisions-log.md` — Chronological history of all project decisions and their rationale
2. After reading all files, respond with exactly: "✓ Context loaded. Ready to continue STACK Exam Builder."
3. Then wait for the user's first message.

## Session Rules

### Do
- Treat everything in the context files as already known. Never ask the user to re-explain anything documented there.
- If something in the context files conflicts with what the user says in the current session, follow the user's current instruction and flag the discrepancy so the context files can be updated.
- Silently note any new important information during the session (new decisions, changed requirements, resolved blockers).
- When producing Moodle/STACK XML, follow these conventions:
  - One XML file per question pool, named `pool_q{N}_{difficulty}.xml`.
  - Each variant is a separate `<question>` element with its own STACK variables, PRTs, and feedback.
  - Numerical inputs use tolerances ±0.01 to ±0.5. Algebraic inputs are minimized.
  - Randomization via Maxima `rand()` with constrained ranges to avoid degenerate cases.
  - **MANDATORY — Syntax hints AFTER every input field:**
    - Every `[[input:ansN]]` in the question HTML MUST be followed by a visible `<p><em>Syntax hint: ...</em></p>` line immediately AFTER the input line. Never place the syntax hint before the input field.
    - MCQ / integer inputs: `"Enter a single integer, e.g. <code>2</code>"`.
    - Numerical inputs: `"Enter a number, e.g. <code>0.523</code> or <code>5.23e-1</code>"` (adapt examples to the expected magnitude).
    - Symbolic / algebraic inputs: show a complete example using the expected variable names, e.g. `"Write <code>lc/(mur*mu0*Ac)</code>"`.
    - Expression inputs (functions of t, etc.): show exp/sin/cos syntax, e.g. `"Use <code>exp(...)</code>, <code>sin(...)</code>, <code>cos(...)</code>, and <code>t</code>."`.
    - Notes / essay inputs: provide a content hint about what to address, e.g. `"Think about what Gauss's law for magnetism implies at the interface."`.
  - **MANDATORY — Conceptual hints as Moodle progressive hints:**
    - Every question MUST include 2–3 `<hint>` elements at the end of the `<question>` block (these are Moodle's progressive hints shown on "Try again").
    - Hint 1: Intuition / physical reasoning.
    - Hint 2: Relevant formulas and approach.
    - Hint 3: Worked step or partial derivation.
    - These are separate from the per-input syntax hints above — syntax hints are always visible; conceptual hints are revealed progressively.
  - **MANDATORY — Grading robustness:**
    - Never use `AlgEquiv` alone for numerical answers that may be rounded — use `NumRelative` with appropriate tolerance (typically 5%).
    - Never use `SigFigsStrict` as a scoring gate — do not penalise students for significant-figure formatting.
    - For complex expressions (e.g. i(t) with float coefficients), use a 2-node PRT: Node 0 tries `AlgEquiv`; if it fails, Node 1 evaluates both expressions at 2–3 numerical test points using feedback variables and compares with `NumRelative` (5% tolerance).
    - For complex-valued roots (s₁), use a 2-node PRT: Node 0 tries `AlgEquiv`; if it fails, Node 1 compares real and imaginary parts numerically (2% tolerance) via feedback variables.
  - **MANDATORY — Specific feedback format:**
    - In `<specificfeedback>`, do NOT use `{@ansN@}` to display student answers — STACK renders these as CAS variable symbols (e.g. `ans₁`) instead of the actual student input.
    - Use only the PRT feedback blocks `[[feedback:prtN]]` in specific feedback. The PRT true/false feedback already contains all necessary correct/incorrect messaging.
- When creating SVG circuit diagrams, follow these conventions:
  - Sans-serif fonts (e.g., Arial, Helvetica).
  - High-contrast black lines on white background.
  - Explicit current arrows and voltage polarity markings on every circuit.
  - Responsive sizing via `viewBox` attribute (no fixed width/height).
  - One SVG per variant, named `q{N}_v{M}_{description}.svg`.
- Use Maxima syntax correctly for STACK question variables and PRTs.

### Do Not
- Never include API keys, credentials, passwords, or any sensitive data in responses or suggested file content.
- Never suggest approaches explicitly listed in the "Never Suggest" section of `context.md`.
- Never fabricate circuit analysis results — if a calculation is needed, show the work.
- Never assume the user wants RLC second-order transients included (explicitly excluded from scope).

### End-of-Session Protocol

At the end of any session where something significant changed (new decisions, completed milestones, changed requirements, new blockers), proactively say:

> **Session summary:** Here's what should be updated in your context files:

Then provide the exact updated content for each affected file, ready to copy-paste. Include only the sections that changed, clearly marked.

### File Maintenance Priority

| File | Update frequency | Who triggers update |
|------|-----------------|---------------------|
| `active-session.md` | Every session | Claude proactively suggests |
| `decisions-log.md` | When decisions are made | Claude proactively suggests |
| `context.md` | Rarely (architecture changes) | User requests or Claude flags |
| `personal-preferences.md` | Very rarely | User requests only |
