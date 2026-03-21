# PATTERNS.md — Accumulated Corrections and Rules

Living memory. Updated at every session close. Read at every session open.
Every entry is a hard constraint — not a suggestion.

---

## How to Read This File

Each entry follows this format:

```
### P-[CATEGORY]-[NN] — [Short descriptive title]
**Pattern:** What kept happening — describe concretely.
**Rule:** The concrete fix. Imperative, unambiguous.
**Scope:** Which skill(s) or context(s).
**First seen:** Session date or task name.
```

**Categories:**
- **STACK** — Moodle XML, STACK grading (PRT), Maxima/CAS, input configuration.
- **DIAG** — CircuiTikZ diagrams, LaTeX compilation, SVG embedding.
- **MSG** — Writing style, email tone, word choice (message-coach).
- **ENV** — Environment quirks, CLI tools, authentication, file systems.

Entries are numbered sequentially within each category and never renumbered.
When a rule is superseded, mark it `[RETIRED]` but keep it in place.

---

## STACK / Moodle XML

### P-STACK-01 — Full `<name>` tag, never abbreviated
**Pattern:** Question names were shortened or abbreviated in XML, making them hard to locate in the Moodle question bank.
**Rule:** Always write the complete, descriptive `<name><text>` value exactly as specified in the question plan. Never abbreviate, truncate, or paraphrase question names.
**Scope:** All STACK XML authoring.
**First seen:** Project convention (pre-session).

### P-STACK-02 — NumAbsolute for zero, NumRelative for nonzero
**Pattern:** PRT nodes used `NumRelative` when the reference answer was 0, causing division-by-zero failures in grading. Conversely, `NumAbsolute` on large-magnitude answers accepted wildly wrong values.
**Rule:** When the expected value is exactly 0, use `NumAbsolute` with tolerance 0.01. When the expected value is nonzero, use `NumRelative` with 0.05 (5%) tolerance. When a PRT uses `AlgEquiv` on an expression that evaluates to a number (possibly containing `%pi`), add a fallback node with `NumRelative` (5%) against `float()` to catch decimal approximations.
**Scope:** All PRT answer tests for numerical results.
**First seen:** Sessions 1-3 (CM#1).

### P-STACK-03 — No `{@ansN@}` in `<specificfeedback>`
**Pattern:** `{@ans1@}` placed inside `<specificfeedback>` rendered as a raw CAS variable symbol instead of the student's input.
**Rule:** Never use `{@ansN@}` inside `<specificfeedback>`. Use only `[[feedback:prtN]]` tags in that block. If you need to display the student's input in feedback, do so inside the PRT node feedback text, not in `<specificfeedback>` directly.
**Scope:** STACK XML `<specificfeedback>` elements.
**First seen:** Sessions 1-3 (CM#3).

### P-STACK-04 — CDATA wrapping for `<` in feedbackvariables
**Pattern:** Bare `<` characters in `<feedbackvariables>` broke the XML parser, which interpreted them as tag openers.
**Rule:** Always wrap `<feedbackvariables>` content in `<![CDATA[ ... ]]>` if it contains any `<` comparisons or inequalities. Apply the same treatment to `<questionvariables>` when in doubt.
**Scope:** All STACK XML with Maxima code containing `<`.
**First seen:** Sessions 1-3 (CM#4).

### P-STACK-05 — NumRelative 5% for nonzero numerical answers (not NumSigFigs)
**Pattern:** Early drafts used `NumSigFigs(3)` for non-zero numerical grading. This does not match the project convention — the repo standard is `NumRelative` with 5% tolerance for nonzero values.
**Rule:** For non-zero numerical answers, use `NumRelative` with tolerance `0.05` (5%). Do not use `NumSigFigs` as the primary answer test. Reserve `NumAbsolute` for zero-valued answers only (see P-STACK-02).
**Scope:** All PRT answer tests for nonzero numerical results.
**First seen:** Project convention (confirmed against repo practice).

### P-STACK-06 — Exact arithmetic for symbolic constants
**Pattern:** Floats like `4*%pi*1e-7` caused `AlgEquiv` failures because Maxima treated them as approximate, producing mismatches on expressions like `0.2*%pi`.
**Rule:** Write exact rational arithmetic for all symbolic constants: `mu0: 4*%pi/10^7;` — never `1e-7` or other float literals. Keep everything in exact form until the final numerical comparison node (if any).
**Scope:** Maxima `questionvariables` and `feedbackvariables`.
**First seen:** Sessions 1-3 (CM#6).

### P-STACK-07 — No SigFigsStrict as a scoring gate
**Pattern:** Using `SigFigsStrict` as a grading criterion penalized students for formatting choices (e.g., trailing zeros) rather than conceptual understanding.
**Rule:** Never use `SigFigsStrict` as a pass/fail scoring gate. If significant-figure formatting matters, handle it in a separate advisory feedback node that does not affect the score.
**Scope:** PRT answer test selection.
**First seen:** Sessions 1-3 (CM#2).

### P-STACK-08 — Validate PRT node chains before committing
**Pattern:** A single broken `truenextnode` or `falsenextnode` reference silently skipped grading nodes, causing students to receive incorrect marks with no error visible to instructors.
**Rule:** Before finalizing any question XML, trace every PRT node chain from the root to all terminal nodes. Verify that every `truenextnode` and `falsenextnode` value either points to a valid node index or is `-1` (stop). Use the multi-tiered validation methodology documented in CLAUDE.md.
**Scope:** All PRT definitions.
**First seen:** Sessions 1-3 (CM#5).

### P-STACK-09 — Verify all parameter set variants
**Pattern:** A question with randomized parameters worked for most variants but produced wrong answers or degenerate cases for untested combinations (e.g., `alpha` vs `omega0` yielding unexpected damping regimes).
**Rule:** For every question with `rand()` or parameter sets, enumerate all distinct variants and verify that each produces a valid, non-degenerate answer. Test edge cases: zero crossings, sign flips, division by near-zero values.
**Scope:** Randomized STACK questions.
**First seen:** Sessions 1-3 (CM#7).

### P-STACK-10 — insertstars=1 on all algebraic inputs
**Pattern:** Students typed `2t` expecting multiplication but STACK rejected the input because implicit multiplication was disabled.
**Rule:** Set `insertstars="1"` on every `<input>` element that accepts algebraic expressions. This makes `2t` parse as `2*t`.
**Scope:** STACK XML `<input>` elements of type `algebraic`.
**First seen:** Sessions 1-3 (CM#8).

### P-STACK-11 — Syntax hints must define aliases and explain every symbol
**Pattern:** Syntax hints told students to type `N`, `l1`, `mur`, etc., but `questionvariables` had no matching aliases, so student input was rejected or misinterpreted.
**Rule:** If a syntax hint references a variable name, `questionvariables` must define a matching alias (e.g., `N: N_val;`). Every hint must state how to type special symbols: `mu0` for mu-sub-0, `mur` for mu-sub-r, `%pi` for pi, `j` for imaginary unit, `exp()`/`sin()`/`cos()` for functions. Include a complete typed example expression.
**Scope:** STACK `<input>` syntax hints and `questionvariables`.
**First seen:** Sessions 1-3 (CM#9).

### P-STACK-12 — Do not leak answers via hints or placeholders
**Pattern:** Syntax hints, textarea placeholder text, or overly specific hint content effectively revealed the answer structure, defeating the purpose of unsupervised assessment.
**Rule:** Never place answer-revealing content in `syntaxhint`, placeholder text, or feedback hints. In unsupervised exams, even structural hints (e.g., showing the form of the expected expression) narrow the solution space unacceptably.
**Scope:** All STACK inputs, especially for exam-mode questions.
**First seen:** Sessions 1-3 (CM#10).

### P-STACK-13 — Match MCQ type to option length
**Pattern:** Long descriptive options were placed in a dropdown, where they were truncated and unreadable.
**Rule:** Use `type="dropdown"` only for short classification labels (e.g., damping regime names, approximately 40 characters or fewer). Use `type="radio"` for longer descriptive options that would be truncated in a dropdown.
**Scope:** STACK MCQ / multiple-choice inputs.
**First seen:** Sessions 1-3 (CM#11).

### P-STACK-14 — No dependent sources in Easy questions
**Pattern:** Dependent sources appeared in Easy-tier questions, introducing complexity inappropriate for that difficulty level.
**Rule:** Reserve dependent sources (VCVS, CCCS, etc.) for Difficult-tier questions (Q4) only. Easy and Medium questions must use only independent sources.
**Scope:** Circuit analysis question design, difficulty tiering.
**First seen:** Sessions 1-3 (CM#12).

### P-STACK-15 — No base64 in exam XMLs
**Pattern:** Base64-encoded images embedded in exam XML were stripped by Moodle's HTML sanitizer, leaving broken image placeholders.
**Rule:** Never embed base64 data URIs in exam-mode question XML. Use text placeholders or Moodle-hosted file references for exams. Base64 embedding is acceptable only for weekly practice questions (non-exam).
**Scope:** Exam vs. practice question XML.
**First seen:** Sessions 1-3 (CM#13).

---

## CircuiTikZ / Diagrams

### P-DIAG-01 — Switch element name = action at t=0
**Pattern:** Authors confused the CircuiTikZ element name with the switch state *before* t=0. For example, they used `closing switch` for a switch that was already closed.
**Rule:** `opening switch` means the switch was closed and is now opening (breaking contact) at t=0. `closing switch` means the switch was open and is now closing (making contact) at t=0. The element name describes the *transition*, not the prior state.
**Scope:** CircuiTikZ switch elements.
**First seen:** Sessions 1-3 (CM#14).

### P-DIAG-02 — Name every switch; use open/closed for SPST
**Pattern:** Switches were left unnamed or labeled with abstract "position a/b" terminology that only applies to SPDT switches, confusing students.
**Rule:** Assign every switch a name: SW1, SW2, etc. Use these names consistently in the diagram and all XML text. For SPST switches, describe state as "open" or "closed" — never "position a/b" (that terminology is reserved for SPDT).
**Scope:** CircuiTikZ diagrams and corresponding question text.
**First seen:** Sessions 1-3 (CM#15).

### P-DIAG-03 — Keep diagram labels and XML text in sync
**Pattern:** The diagram showed SW1-SW4 but the question text, general feedback, or hints used different names or omitted some switches.
**Rule:** Every label visible in the diagram (component names, node labels, switch identifiers) must appear identically in the `<questiontext>`, `<generalfeedback>`, and all `<hint>` elements. Audit label consistency before finalizing.
**Scope:** All questions with embedded diagrams.
**First seen:** Sessions 1-3 (CM#16).

### P-DIAG-04 — No `\dfrac` inside CircuiTikZ `l=` labels
**Pattern:** Using `\dfrac` inside a CircuiTikZ `l=` label caused "Extra \endgroup" compilation errors.
**Rule:** Never use `\dfrac` (or `\displaystyle\frac`) inside CircuiTikZ `l=` labels. If a complex math label is needed, place it in a separate `\node` element positioned near the component.
**Scope:** CircuiTikZ component labels.
**First seen:** Sessions 1-3 (CM#17).

### P-DIAG-05 — Leave adequate spacing between adjacent vertical components
**Pattern:** Voltage and polarity labels on vertically stacked components overlapped or collided, making the diagram unreadable.
**Rule:** When placing components vertically, leave enough coordinate spacing (typically 2-3 units minimum) so that voltage labels, polarity marks, and current arrows do not overlap with neighboring components.
**Scope:** CircuiTikZ layout and spacing.
**First seen:** Sessions 1-3 (CM#18).

### P-DIAG-06 — Do not mix diagram tools in the same content set
**Pattern:** Some questions used CircuiTikZ while others in the same set used Schemdraw, creating visual inconsistency.
**Rule:** Use CircuiTikZ for all new diagram content. Never mix CircuiTikZ and Schemdraw (or other tools) within the same question set. Legacy Schemdraw files are preserved with a `_schemdraw` suffix but are not used in new content.
**Scope:** Diagram tool selection across question sets.
**First seen:** Sessions 1-3 (CM#19).

### P-DIAG-07 — Test compilation; use standalone with border=10pt
**Pattern:** Diagrams looked correct in the LaTeX source but had clipped labels and arrows after SVG conversion because no border was specified.
**Rule:** Always compile `.tex` to SVG and visually inspect before base64-encoding or embedding. Use the `standalone` document class with `border=10pt` to prevent clipping at SVG edges.
**Scope:** LaTeX-to-SVG diagram pipeline.
**First seen:** Sessions 1-3 (CM#20).

---

## Writing and Communication (message-coach)

### P-MSG-01 — "Flagging" is banned
**Pattern:** Drafts included the word "flagging" (e.g., "I'm flagging this issue"), which reads as passive-aggressive or bureaucratic in professional communication.
**Rule:** Never use the word "flagging" in any message draft. Replace with direct alternatives: "noting," "raising," "highlighting," or simply state the issue directly.
**Scope:** All written communication (emails, Slack, comments).
**First seen:** Message-coach convention.

### P-MSG-02 — Sign-off is "Best regards,"
**Pattern:** Inconsistent sign-offs across messages (Cheers, Thanks, Best, etc.).
**Rule:** Use "Best regards," as the standard email sign-off unless the user specifies otherwise.
**Scope:** Email drafts.
**First seen:** Message-coach convention.

### P-MSG-03 — Anti-AI banned words check
**Pattern:** Drafts contained words that signal AI-generated text (e.g., "delve," "leverage," "synergy," "utilize," "facilitate"), undermining authenticity.
**Rule:** Before finalizing any message, scan for and remove common AI-tell words. Replace with plain, direct language. Maintain a banned-words list and check against it.
**Scope:** All written communication.
**First seen:** Message-coach convention.

---

## Environment and Tooling

### P-ENV-01 — Use `python` not `python3`
**Pattern:** Commands using `python3` failed because the environment aliases only `python`.
**Rule:** Always invoke `python`, never `python3`. If a script has a `#!/usr/bin/env python3` shebang, update it to `python`.
**Scope:** All CLI Python invocations.
**First seen:** Environment setup.

### P-ENV-02 — Google Drive search unreliable for .pptx
**Pattern:** Google Drive search returned incomplete or no results when searching for `.pptx` files by name or content.
**Rule:** Do not rely on Google Drive search to locate `.pptx` files. Instead, navigate the folder hierarchy manually or use known file paths. If search is required, try multiple query variations and verify results.
**Scope:** Google Drive file retrieval.
**First seen:** Environment discovery.

### P-ENV-03 — NotebookLM auth tokens expire
**Pattern:** NotebookLM authentication tokens expired mid-session, causing silent failures in API calls.
**Rule:** Assume NotebookLM auth tokens may expire at any time. Check for auth errors before retrying content operations. Re-authenticate proactively if a session runs long.
**Scope:** NotebookLM integration.
**First seen:** Environment discovery.

---

## Execution

### P-EXEC-01 — Large tasks must be decomposed before starting

**Pattern:** Large tasks attempted as a single block produced incomplete or
inconsistent output requiring full rework.
**Rule:** Any task with 3+ deliverables, 2+ files, or 2+ skills required must
be decomposed into subtasks with an explicit dependency map before any work
begins. Present the plan and wait for confirmation. Never start without this step.
**Scope:** All sessions, all skills.
**First seen:** Workflow optimization session, March 2026.

---

## Template for New Entries

```markdown
### P-[CATEGORY]-[NN] — [Short descriptive title]
**Pattern:** What kept happening — describe concretely.
**Rule:** The concrete fix. Imperative, unambiguous.
**Scope:** Which skill(s) or context(s).
**First seen:** Session date or task name.
```

To add a new entry:
1. Pick the correct category (STACK, DIAG, MSG, ENV) or create a new one.
2. Use the next available number in that category.
3. Fill in all four fields. Be concrete — avoid vague language.
4. Never renumber existing entries. If an entry is retired, mark it `[RETIRED]`.
