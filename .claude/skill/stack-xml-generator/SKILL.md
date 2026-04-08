---
name: stack-xml-generator
version: 1.0.0
description: >
  Use when: generating STACK XML, creating Moodle questions, writing
  Maxima CAS code, building PRT grading trees, setting up randomization,
  creating MCQ questions, building exam question banks, adding JSXGraph
  interactive elements, "create a question", "generate XML", "STACK
  question", "randomized assessment", "PRT validation".
---

# STACK XML Generator

This skill generates Moodle STACK assessment questions with randomized parameters, Potential Response Trees (PRTs), and Maxima CAS code. It produces well-structured XML ready for Moodle import.

## When to Use This Skill

- User asks to create Moodle STACK questions
- User needs randomized exam or practice questions with Maxima CAS
- User wants to build PRT grading trees for numerical or algebraic answers
- User needs to convert a problem set into STACK XML format

## Output Format

- One XML file per question pool, named `pool_q{N}_{difficulty}.xml` (exams) or `Q{N}_{TopicDescription}.xml` (practice)
- Each variant is a separate `<question>` element with its own STACK variables, PRTs, and feedback

## Mandatory Conventions

### Syntax Hints

Every `[[input:ansN]]` in the question HTML MUST be followed by a visible syntax hint line immediately AFTER the input field. Never place the syntax hint before the input.

```html
[[input:ansN]]
<p><em>Syntax hint: Enter a number, e.g. <code>0.523</code> or <code>5.23e-1</code></em></p>
```

Type-specific hint text:

| Input type | Hint text |
|------------|-----------|
| MCQ / integer | `Enter a single integer, e.g. <code>2</code>` |
| Numerical | `Enter a number, e.g. <code>0.523</code> or <code>5.23e-1</code>` (adapt to expected magnitude) |
| Numerical (may contain pi) | Add: `You may also use <code>%pi</code> for pi, e.g. <code>0.2*%pi</code>.` |
| Symbolic / algebraic | Show complete example with expected variables, e.g. `Write <code>lc/(mur*mu0*Ac)</code>`. Always state how to type special symbols. |
| Expression (function of t) | `Use <code>exp(...)</code>, <code>sin(...)</code>, <code>cos(...)</code>, and <code>t</code>.` Include a complete example. |
| Complex roots (with j) | `For complex roots use <code>j</code> for the imaginary unit, e.g. <code>-2800+9600*j</code>` |
| Notes / essay | Content hint about what to address |

### Progressive Hints

Every question MUST include 2-3 `<hint>` elements at the end of the `<question>` block (Moodle's progressive hints shown on "Try again"):

1. **Hint 1:** Intuition / physical reasoning
2. **Hint 2:** Relevant formulas and approach
3. **Hint 3:** Worked step or partial derivation

These are separate from the per-input syntax hints — syntax hints are always visible; conceptual hints are revealed progressively.

### Grading (PRT) Rules

| Rule | Details |
|------|---------|
| Numerical answers | Use `NumRelative` with appropriate tolerance (typically 5%). Never `AlgEquiv` alone for rounded values. |
| Answer is 0 | Use `NumAbsolute` with tolerance 0.01. `NumRelative` divides by zero. |
| Complex expressions | 2-node PRT: Node 0 = `AlgEquiv`; Node 1 fallback = evaluate at 2-3 test points with `NumRelative` (5%). |
| Complex-valued roots | 2-node PRT: Node 0 = `AlgEquiv`; Node 1 = compare `realpart()`/`imagpart()` with `NumRelative` (2%). |
| `SigFigsStrict` | Never use as a scoring gate — do not penalize students for significant-figure formatting. |
| Specific feedback | Never use `{@ansN@}` in `<specificfeedback>` — STACK renders these as CAS variable symbols. Use `[[feedback:prtN]]` only. |

### Input Configuration

| Setting | Value | Reason |
|---------|-------|--------|
| `insertstars` | `1` | Required for algebraic expression inputs (e.g. `2*exp(-3*t)`) |
| Classification MCQs (short labels) | `type="dropdown"` | Compact for single-word/short-phrase options |
| Reasoning MCQs (long text) | `type="radio"` | Full option text always visible; dropdowns truncate |
| MCQ option format | `[[value, bool, "text"]]` | STACK 4.x Maxima list format in `questionvariables` |

### Randomization

- Use Maxima `rand()` or `rand_with_step()` with constrained ranges to avoid degenerate cases
- Numerical inputs use tolerances +/-0.01 to +/-0.5
- Algebraic inputs are minimized in favor of numerical inputs

## PRT Validation Checklist

Before finalizing any STACK XML, validate every PRT:

### Tier 1 — Structural Integrity
- [ ] Every `truenextnode` / `falsenextnode` points to an existing node or `-1` (exit)
- [ ] Every node is reachable from node 0 (root)
- [ ] All variables in PRT node tests are defined in `<feedbackvariables>` or `<questionvariables>`

### Tier 2 — Grading Correctness
- [ ] `NumAbsolute` for zero-valued answers (tolerance 0.01)
- [ ] `NumRelative` fallback on symbolic PRTs against `float()`
- [ ] Score consistency: 1.0 (exact/5%), 0.7 (close/15%), 0.3 (order-of-magnitude), 0.0 (wrong)
- [ ] No `SigFigsStrict` as scoring gate
- [ ] No `{@ansN@}` in specificfeedback

### Tier 3 — XML/CAS Safety
- [ ] `<feedbackvariables>` containing `<` operators are wrapped in `<![CDATA[...]]>`
- [ ] Penalty settings are intentional (0 for practice, >0 for exams)
- [ ] `insertstars=1` on all algebraic inputs
- [ ] Exact arithmetic for symbolic constants (e.g. `4*%pi/10^7`, not `4*%pi*1e-7`)

### Tier 4 — Pedagogical Quality
- [ ] Syntax hints present after every `[[input:ansN]]`
- [ ] Progressive hints (2-3 `<hint>` elements) per question
- [ ] No answer leaks via `syntaxhint`, placeholder text, or hint content

## Maxima CAS Patterns

### Parameter Randomization

```maxima
/* Use rand_with_step for constrained random values */
R1: rand_with_step(2, 8, 2);    /* 2, 4, 6, or 8 */

/* Verify parameter combinations produce valid problems */
```

### Key Syntax

- `float()` — convert exact to decimal
- `realpart()` / `imagpart()` — extract complex number components
- `%pi` — the constant pi
- `%e` — Euler's number
- `%i` or `j` — imaginary unit (configure per question)

## Common Mistakes to Avoid

1. **`NumAbsolute` for zero, `NumRelative` for nonzero** — `NumRelative` divides by the reference value; if it's 0, grading fails silently.
2. **Exact arithmetic** — write `4*%pi/10^7` not `4*%pi*1e-7`. Floats cause `AlgEquiv` failures on symbolic expressions.
3. **CDATA wrapping** — XML parsers interpret bare `<` as tag openers inside `<feedbackvariables>`.
4. **Syntax hints define aliases** — if a hint tells students to type `mur`, ensure `questionvariables` defines a matching alias.
5. **Don't leak answers** via `syntaxhint`, textarea placeholders, or overly specific hints.
6. **Match MCQ type to option length** — `dropdown` for short labels, `radio` for long descriptions.
7. **Test all parameter variants** — a single untested variant can produce wrong answers or degenerate cases.

## JSXGraph Integration

STACK supports interactive JSXGraph elements inside `[[jsxgraph]]...[[/jsxgraph]]` blocks. These run in **sandboxed iframes** — this has critical implications for how you bind inputs and access the DOM.

### Key Rules

1. **Use `{#var#}` not `{@var@}` inside JSXGraph blocks.** The `{@var@}` syntax renders LaTeX delimiters (`\(...\)`) which produce invalid JavaScript. `{#var#}` gives raw Maxima values.

2. **JSXGraph runs in a sandboxed iframe.** `document.getElementById()` cannot reach elements in the parent page (STACK inputs, HTML tables). Create display elements dynamically inside the JSXGraph block.

3. **Use `stack_jxg.custom_bind()` for input binding.** This is the official STACK-JS mechanism for serializing graph state to a hidden input across the iframe boundary.

4. **Dispatch change events** when writing to inputs manually (if not using `custom_bind`). Otherwise STACK won't detect the value change.

5. **Declare `input-ref-X` attributes** on the `[[jsxgraph]]` tag to get references to STACK inputs.

### Recommended Pattern for Point Collection

```javascript
[[jsxgraph input-ref-ans6="ans6Ref" width="680px" height="440px"]]
var board = JXG.JSXGraph.initBoard(divid, { ... });

/* Hidden anchor for custom_bind watch */
var syncAnchor = board.create('point', [0,0], {visible: false, fixed: true});

/* Use snapSizeX/Y instead of snapToGrid (which snaps to integers only) */
var p = board.create('point', [x, y], {
    snapSizeX: 1,
    snapSizeY: 0.25
});

/* Bind with serializer/deserializer */
stack_jxg.custom_bind(ans6Ref, serializeFn, deserializeFn, [syncAnchor]);
stack_jxg.clear_initial(syncAnchor);
[[/jsxgraph]]
```

### Hidden Input Configuration for JSXGraph

```xml
<input>
    <name>ans6</name>
    <type>algebraic</type>
    <tans>correct_points</tans>
    <mustverify>0</mustverify>
    <showvalidation>0</showvalidation>
    <options>hideanswer</options>
</input>
```

### Grading JSXGraph Points in PRT

Maxima parses `[[x1,y1],[x2,y2]]` as a **matrix**, not a nested list. Convert with `args()`:
```maxima
student_pts: if matrixp(ans6) then args(ans6) else ans6;
```

Then use nearest-point matching with separate x/y tolerances for order-independent grading.

See `references/jsxgraph-conventions.md` for the complete authoring guide.

## Reference Files

- `references/stack-xml-conventions.md` — Complete XML structure reference with examples
- `references/jsxgraph-conventions.md` — JSXGraph authoring guide (binding, snapping, grading)
