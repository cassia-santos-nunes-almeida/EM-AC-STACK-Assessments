# Week 14-16 Question Development Changelog

## Final Validation: 53 PASS, 1 known false-positive FAIL (Q4 CDATA), 0 WARN

## Issues Found and Fixed

### Critical — Physics/Parameter Errors

| # | Question | Issue | Fix |
|---|----------|-------|-----|
| 1 | Q3 (v1) | Sets 3,4,5 had l/lambda > 0.1 — Hertzian dipole model invalid, R_rad formula gives physically wrong answers | Redesigned Q3: ALL variants are invalid, students must recognize invalidity and propose corrected length |
| 2 | Q4 (v1) | Sets 3,4 had l/lambda > 0.1 (set3: 2cm/5GHz=0.333, set4: 3cm/2GHz=0.2) | Fixed parameters: set3→1cm/2GHz=0.067, set4→2cm/1GHz=0.067 |
| 3 | Q2 (v1) | vp1_err check matches correct answer when eps_r1=1 (2 of 5 variants) | Added guard: `if eps_r1 > 1` before error check |

### High — Grading Fairness

| # | Question | Issue | Fix |
|---|----------|-------|-----|
| 4 | Q2 (v1) | Cascading errors: wrong eta → wrong Gamma → wrong power (4/8 pts lost from 1 conceptual error) | Added follow-through method credit in PRT5: if student's Gamma matches their own eta values, award 50% |
| 5 | Q3 (v2) | R_rad/P_rad follow-through needed when student proposes wrong l_max | Added follow-through grading in PRT5/PRT6: correct formula with wrong l_max → 50% credit |

### Medium — Pedagogical / AI Resistance

| # | Question | Issue | Fix |
|---|----------|-------|-----|
| 6 | Q1 (v1→v3) | All parts formula plugging; classification always "good conductor" | **Full restructure:** mix of conductor (3 sets) + low-loss dielectric (2 sets). Conditional α formula, conditional frequency-doubling MCQ. Most AI-resistant question. |
| 7 | Q3 (v1→v2) | Some variants valid, some not — unequal assessment | **Full redesign:** ALL variants invalid, students propose corrected l_max + follow-through grading |
| 8 | Q2 (v1→v3) | Wavenumber k missing from LO1 | Added k = 2π/λ as part (c), shifted remaining parts, 7 PRTs total |

### Low — Validator False Positives

| # | Question | Issue | Status |
|---|----------|-------|--------|
| 8 | Q1, Q4 | Check 5 FAIL: bare `<` in feedbackvariables | Known validator limitation — CDATA wrapping IS correct, but ElementTree strips markers during parsing. Same issue as SESSION.md pre-existing Check 5 failures. No action needed. |

## Design Decisions for Future Questions

1. **Follow-through grading pattern:** When answers cascade (A→B→C), compute expected B from student's A in feedbackvariables and award partial credit for correct method. Use `abs(ans - expected)/abs(expected) < tolerance` flags.

2. **Hertzian dipole parameter validation:** Always verify l/lambda < 0.1 for ALL parameter sets before finalizing. The formula R_rad = 80*pi^2*(l/lambda)^2 gives physically wrong results when l/lambda > 0.1.

3. **MCQ error detection guards:** When checking if student's answer matches an error model value, guard against cases where the error model equals the correct answer (e.g., `if parameter > threshold` before comparing).

4. **Conceptual MCQs for AI resistance:** Add at least one "what happens if X changes" part per question. These test functional understanding (how does Y depend on X?) rather than plugging numbers. Much harder for AI to shortcut.

5. **NumRelative vs NumAbsolute on dB values:** NumRelative works fine on negative dBm values as long as |value| is large (> 10). For values near 0 dBm, use NumAbsolute instead.

## Parameter Verification Table

All parameter sets verified for physical validity:

### Q1 — All good conductors (tan_delta >> 1)
| Set | sigma_c | mu_r | f_MHz | tan_delta | delta_s (um) |
|-----|---------|------|-------|-----------|-------------|
| 1 | 5.8 | 1 | 100 | 1.04e10 | 6.6 |
| 2 | 5.8 | 1 | 900 | 1.16e9 | 2.2 |
| 3 | 3.5 | 1 | 500 | 1.26e9 | 3.8 |
| 4 | 3.5 | 1 | 2400 | 2.62e8 | 1.7 |
| 5 | 1.0 | 200 | 60 | 3.0e9 | 1.5 |

### Q3 — All INVALID (l/lambda > 0.1)
| Set | l_cm | f_GHz | lambda_cm | l/lambda |
|-----|------|-------|-----------|---------|
| 1 | 5 | 1 | 30 | 0.167 |
| 2 | 10 | 2 | 15 | 0.667 |
| 3 | 8 | 5 | 6 | 1.333 |
| 4 | 4 | 2 | 15 | 0.267 |
| 5 | 15 | 0.5 | 60 | 0.250 |

### Q4 — All VALID (l/lambda < 0.1)
| Set | l_cm | f_GHz | lambda_cm | l/lambda |
|-----|------|-------|-----------|---------|
| 1 | 0.5 | 2 | 15 | 0.033 |
| 2 | 1 | 1 | 30 | 0.033 |
| 3 | 1 | 2 | 15 | 0.067 |
| 4 | 2 | 1 | 30 | 0.067 |
