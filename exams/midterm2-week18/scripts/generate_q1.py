#!/usr/bin/env python
"""
Generate pool_q1_medium.xml — Magnetic Circuit + Faraday Induction
Midterm 2, Q1 (Medium, 9 pts), 4 variants + companion essay

Textbook: Ulaby Ch.5 (toroid+gap) + Nilsson Ch.6 (mutual inductance)
"""

import math
import os

# ─── Variant definitions ────────────────────────────────────────────
VARIANTS = [
    {
        "id": "V1", "name": "E-core with Center-Limb Air Gap",
        "N1": 200, "N2": 100, "mu_r": 2000,
        "lc": 0.4, "lg": 0.002, "Ac": 4e-4,
        "I0": 2, "f": 50,
        "core_desc": (
            "An <strong>E-core</strong> electromagnet has a ferromagnetic core shaped like the letter E. "
            "Two coils are wound on the outer limbs. A single <strong>air gap</strong> of length "
            "\\(\\ell_g\\) exists in the <strong>center limb</strong>. "
            "The mean magnetic path length through the core (excluding the gap) is \\(\\ell_c\\)."
        ),
        "ascii_diagram": (
            "       ┌────────┬────────┬────────┐\n"
            "       │  Coil 1│  GAP   │ Coil 2 │\n"
            "       │ (N₁)   │ (ℓ_g)  │ (N₂)   │\n"
            "       │        │        │        │\n"
            "       └────────┴────────┴────────┘\n"
            "         Ferromagnetic core (μ_r·μ₀)\n"
            "         Mean path ℓ_c, cross-section A_c"
        ),
        "debug_errors": [2, 4],  # indices of TRUE errors (1-based)
        "debug_options": [
            ("The formula R_core = ℓ_c/(μ_r·μ₀·A_c) was applied incorrectly", False),
            ("The air gap reluctance was not included in the total reluctance", True),
            ("The number of turns N₂ was correctly used in Faraday's law", False),
            ("The derivative of sin(ωt) is missing the factor ω", True),
            ("The cross-sectional area A_c was used correctly throughout", False),
        ],
        "worked_solution_errors": (
            "A student wrote the following solution:\n"
            "\\[ \\mathcal{R}_{\\text{total}} = \\frac{\\ell_c}{\\mu_r \\mu_0 A_c} \\]\n"
            "(Note: the student did <em>not</em> add an air gap term.)\n"
            "Then: \\(\\Phi_{\\max} = \\frac{N_1 I_0}{\\mathcal{R}_{\\text{total}}}\\)\n"
            "Finally: \\(\\text{EMF}_{2,\\text{peak}} = N_2 \\cdot \\Phi_{\\max}\\)\n"
            "(Note: the student wrote \\(N_2 \\cdot \\Phi_{\\max}\\) without the \\(\\omega\\) factor.)"
        ),
    },
    {
        "id": "V2", "name": "C-core with Single Air Gap",
        "N1": 300, "N2": 150, "mu_r": 1500,
        "lc": 0.3, "lg": 0.001, "Ac": 6e-4,
        "I0": 1.5, "f": 60,
        "core_desc": (
            "A <strong>C-core</strong> electromagnet has a U-shaped ferromagnetic core with a single "
            "<strong>air gap</strong> at the top. "
            "Coil 1 (primary, \\(N_1\\) turns) is wound on the left arm and "
            "Coil 2 (secondary, \\(N_2\\) turns) on the right arm."
        ),
        "ascii_diagram": (
            "       ┌──────────────────────┐\n"
            "       │   Ferromagnetic core  │\n"
            "  Coil 1    (μ_r·μ₀)     Coil 2\n"
            "  (N₁)  │              │  (N₂)\n"
            "       └──────┐  ┌──────┘\n"
            "              │  │  ← Air gap (ℓ_g)\n"
            "              └──┘"
        ),
        "debug_errors": [1, 5],
        "debug_options": [
            ("The student used N₁ instead of N₂ in the Faraday's law step", True),
            ("The total reluctance correctly includes both core and gap", False),
            ("The derivative d(sin ωt)/dt = ω cos(ωt) was applied correctly", False),
            ("The core permeability μ_r was omitted from the reluctance formula", False),
            ("The sign of the induced EMF violates Lenz's law", True),
        ],
        "worked_solution_errors": (
            "A student wrote:\n"
            "\\(\\mathcal{R}_{\\text{total}} = \\frac{\\ell_c}{\\mu_r \\mu_0 A_c} + "
            "\\frac{\\ell_g}{\\mu_0 A_c}\\) (correct)\n"
            "\\(\\Phi_{\\max} = \\frac{N_1 I_0}{\\mathcal{R}_{\\text{total}}}\\) (correct)\n"
            "\\(\\text{EMF}_{2,\\text{peak}} = -N_1 \\cdot \\omega \\cdot \\Phi_{\\max}\\)\n"
            "(Error: used \\(N_1\\) instead of \\(N_2\\), and the sign is wrong by Lenz's law convention.)"
        ),
    },
    {
        "id": "V3", "name": "Toroid with Cut (Air Gap)",
        "N1": 500, "N2": 250, "mu_r": 3000,
        "lc": 0.5, "lg": 0.0015, "Ac": 3e-4,
        "I0": 1, "f": 50,
        "core_desc": (
            "A <strong>toroidal</strong> core made of ferromagnetic material has a narrow "
            "<strong>cut</strong> (air gap) of length \\(\\ell_g\\). "
            "Coil 1 (\\(N_1\\) turns) is wound on one half of the toroid, "
            "Coil 2 (\\(N_2\\) turns) on the other half."
        ),
        "ascii_diagram": (
            "          ╭──── Coil 1 (N₁) ────╮\n"
            "         ╱                        ╲\n"
            "        │    Toroidal core         │\n"
            "        │    (μ_r·μ₀)              │\n"
            "         ╲                        ╱\n"
            "          ╰── Coil 2 (N₂) ──╮╭──╯\n"
            "                            ││ ← Gap (ℓ_g)\n"
            "                            ╰╯"
        ),
        "debug_errors": [2, 3],
        "debug_options": [
            ("The ω factor in the Faraday's law derivative was applied correctly", False),
            ("The air gap reluctance was not included in R_total", True),
            ("The student used N₁ instead of N₂ in the EMF calculation", True),
            ("The cross-sectional area was doubled incorrectly", False),
            ("The core reluctance formula is correct", False),
        ],
        "worked_solution_errors": (
            "A student wrote:\n"
            "\\(\\mathcal{R}_{\\text{total}} = \\frac{\\ell_c}{\\mu_r \\mu_0 A_c}\\)\n"
            "(Error: did not include air gap reluctance.)\n"
            "\\(\\Phi_{\\max} = \\frac{N_1 I_0}{\\mathcal{R}_{\\text{total}}}\\)\n"
            "\\(\\text{EMF}_{2,\\text{peak}} = N_1 \\cdot \\omega \\cdot \\Phi_{\\max}\\)\n"
            "(Error: used \\(N_1\\) instead of \\(N_2\\).)"
        ),
    },
    {
        "id": "V4", "name": "Rectangular Core with Two Series Air Gaps",
        "N1": 400, "N2": 200, "mu_r": 2500,
        "lc": 0.6, "lg": 0.002,  # total gap = 2 × 0.001
        "Ac": 5e-4,
        "I0": 1.8, "f": 60,
        "core_desc": (
            "A <strong>rectangular</strong> ferromagnetic core has <strong>two air gaps</strong> "
            "of equal length \\(\\ell_{g}/2\\) each (total gap length \\(\\ell_g\\)). "
            "Coil 1 (\\(N_1\\) turns) is wound on the top section, "
            "Coil 2 (\\(N_2\\) turns) on the bottom section."
        ),
        "ascii_diagram": (
            "       ┌───── Coil 1 (N₁) ─────┐\n"
            "       │                         │\n"
            "  Gap 1 ┤                         ├ Gap 2\n"
            "  (ℓ_g/2)                       (ℓ_g/2)\n"
            "       │                         │\n"
            "       └───── Coil 2 (N₂) ─────┘\n"
            "         Rectangular core (μ_r·μ₀)\n"
            "         ℓ_c = total core path, A_c = cross-section"
        ),
        "debug_errors": [3, 5],
        "debug_options": [
            ("The total reluctance correctly includes core and both gaps", False),
            ("N₂ was correctly used in Faraday's law", False),
            ("The derivative of sin(ωt) is missing the factor ω", True),
            ("The core permeability was correctly included", False),
            ("The sign of the EMF contradicts Lenz's law", True),
        ],
        "worked_solution_errors": (
            "A student wrote:\n"
            "\\(\\mathcal{R}_{\\text{total}} = \\frac{\\ell_c}{\\mu_r \\mu_0 A_c} + "
            "\\frac{\\ell_g}{\\mu_0 A_c}\\) (correct)\n"
            "\\(\\Phi_{\\max} = \\frac{N_1 I_0}{\\mathcal{R}_{\\text{total}}}\\) (correct)\n"
            "\\(\\text{EMF}_{2,\\text{peak}} = -N_2 \\cdot \\Phi_{\\max}\\)\n"
            "(Error: forgot \\(\\omega\\) from the derivative, and wrong sign.)"
        ),
    },
]

MU0 = 4 * math.pi * 1e-7


def compute_values(v):
    """Compute all derived values for a variant."""
    mu0 = MU0
    R_core = v["lc"] / (v["mu_r"] * mu0 * v["Ac"])
    R_gap = v["lg"] / (mu0 * v["Ac"])
    R_total = R_core + R_gap
    omega = 2 * math.pi * v["f"]
    Phi_max = v["N1"] * v["I0"] / R_total
    emf_peak = v["N2"] * omega * Phi_max

    # Error values
    Phi_no_gap = v["N1"] * v["I0"] / R_core
    emf_no_omega = v["N2"] * Phi_max
    emf_wrong_N = v["N1"] * omega * Phi_max

    return {
        "R_core": R_core, "R_gap": R_gap, "R_total": R_total,
        "omega": omega, "Phi_max": Phi_max, "emf_peak": emf_peak,
        "Phi_no_gap": Phi_no_gap, "emf_no_omega": emf_no_omega,
        "emf_wrong_N": emf_wrong_N,
    }


def gen_questionvariables(v, vals):
    """Generate Maxima questionvariables code."""
    # Build correct error set
    correct_set = "{" + ",".join(str(i) for i in v["debug_errors"]) + "}"

    # Build debug options list (Maxima format for checkbox)
    opts = []
    for i, (text, is_err) in enumerate(v["debug_options"], 1):
        bval = "true" if is_err else "false"
        opts.append(f'[{i}, {bval}, "{text}"]')
    opts_str = "[" + ", ".join(opts) + "]"

    return f"""/* {v['id']}: {v['name']} */
/* Physical parameters */
mu0: 4*%pi/10^7;
N1_val: {v['N1']};
N2_val: {v['N2']};
mur_val: {v['mu_r']};
lc_val: {v['lc']};
lg_val: {v['lg']};
Ac_val: {v['Ac']};
I0_val: {v['I0']};
f_val: {v['f']};

/* Derived quantities — exact arithmetic */
omega_val: 2*%pi*f_val;
R_core: lc_val/(mur_val*mu0*Ac_val);
R_gap: lg_val/(mu0*Ac_val);
R_total: R_core + R_gap;

Phi_max: N1_val*I0_val/R_total;
emf_peak: N2_val*omega_val*Phi_max;

/* Error model values */
Phi_no_gap: N1_val*I0_val/R_core;
emf_no_omega: N2_val*Phi_max;
emf_wrong_N: N1_val*omega_val*Phi_max;

/* Numerical versions for display */
R_total_num: float(R_total);
Phi_max_num: float(Phi_max);
emf_peak_num: float(emf_peak);

/* Debug MCQ-MA options (checkbox) */
debug_opts: random_permutation({opts_str});
correct_errors: {correct_set};

/* Teacher answers */
ta_reluctance: float(R_total);
ta_flux: float(Phi_max);
ta_emf: float(emf_peak);
ta_debug: correct_errors;"""


def gen_questiontext(v, vals):
    """Generate the question HTML."""
    # Format numbers for display
    R_t = vals["R_total"]
    Phi = vals["Phi_max"]
    emf = vals["emf_peak"]

    return f"""<h3>Midterm 2 &ndash; Q1{v['id']}: Magnetic Circuit with Faraday Induction ({v['name']})</h3>
<p><em>Electromagnetism and Circuit Analysis &mdash; LUT University, Finland</em></p>
<p><strong>Total: 9 points | Penalty per wrong attempt: 10%</strong></p>
<p><em>Inspired by Ulaby Ch.5 Example 5-6 and Nilsson Ch.6 Problems 6.1&ndash;6.5.</em></p>
<hr />

<h4>Scenario</h4>
<p>{v['core_desc']}</p>

<p>[DIAGRAM: {v['name']} &mdash; will be replaced with CircuiTikZ SVG after compilation]</p>
<pre>{v['ascii_diagram']}</pre>

<h4>Given Data</h4>
<ul>
  <li>Primary coil: \\(N_1 = {{@N1_val@}}\\) turns</li>
  <li>Secondary coil: \\(N_2 = {{@N2_val@}}\\) turns</li>
  <li>Core relative permeability: \\(\\mu_r = {{@mur_val@}}\\)</li>
  <li>Mean core path length: \\(\\ell_c = {{@lc_val@}}\\;\\text{{m}}\\)</li>
  <li>Air gap length: \\(\\ell_g = {{@lg_val@}}\\;\\text{{m}}\\)</li>
  <li>Core cross-sectional area: \\(A_c = {{@Ac_val@}}\\;\\text{{m}}^2\\)</li>
  <li>Primary current: \\(i_1(t) = I_0 \\sin(\\omega t)\\) with \\(I_0 = {{@I0_val@}}\\;\\text{{A}}\\) and \\(f = {{@f_val@}}\\;\\text{{Hz}}\\)</li>
  <li>Permeability of free space: \\(\\mu_0 = 4\\pi \\times 10^{{-7}}\\;\\text{{H/m}}\\)</li>
</ul>

<hr />

<h4>Part (a) &mdash; Total Reluctance (2 points)</h4>
<p>Calculate the <strong>total reluctance</strong> \\(\\mathcal{{R}}_{{\\text{{total}}}}\\) of the magnetic circuit (core + air gap).</p>
<p>\\(\\mathcal{{R}}_{{\\text{{total}}}} = \\) [[input:ans1]] \\(\\text{{A-turns/Wb}}\\)</p>
<p>[[validation:ans1]]</p>
<p><em>Enter a number, e.g. <code>1.23e5</code> or <code>123000</code></em></p>

<h4>Part (b) &mdash; Peak Magnetic Flux (2 points)</h4>
<p>Given the sinusoidal primary current, calculate the <strong>peak magnetic flux</strong> \\(\\Phi_{{\\max}}\\) in the core.</p>
<p>\\(\\Phi_{{\\max}} = \\) [[input:ans2]] \\(\\text{{Wb}}\\)</p>
<p>[[validation:ans2]]</p>
<p><em>Enter a number, e.g. <code>4.56e-4</code> or <code>0.000456</code></em></p>

<h4>Part (c) &mdash; Peak Induced EMF (1 point)</h4>
<p>Using Faraday&rsquo;s law, calculate the <strong>peak induced EMF</strong> in the secondary coil (Coil 2).</p>
<p>Recall: \\(\\text{{emf}}_2(t) = -N_2 \\frac{{d\\Phi}}{{dt}}\\), so \\(|\\text{{EMF}}_{{2,\\text{{peak}}}}| = N_2 \\cdot \\omega \\cdot \\Phi_{{\\max}}\\).</p>
<p>\\(|\\text{{EMF}}_{{2,\\text{{peak}}}}| = \\) [[input:ans3]] \\(\\text{{V}}\\)</p>
<p>[[validation:ans3]]</p>
<p><em>Enter a number, e.g. <code>0.567</code></em></p>

<h4>Part (d) &mdash; Error Identification (1 point)</h4>
<p>A student attempted this problem and made <strong>two errors</strong>. Their work is shown below:</p>
<blockquote>
{v['worked_solution_errors']}
</blockquote>
<p><strong>Select ALL statements that identify actual errors in the student&rsquo;s work:</strong></p>
<p>[[input:ans4]]</p>
<p>[[validation:ans4]]</p>

<h4>Part (e) &mdash; Qualitative Analysis (3 points, manually graded)</h4>
<p>Suppose the air gap length is <strong>doubled</strong> (from \\(\\ell_g\\) to \\(2\\ell_g\\)).</p>
<p>Explain qualitatively what happens to:</p>
<ol>
  <li>The total reluctance \\(\\mathcal{{R}}_{{\\text{{total}}}}\\)</li>
  <li>The peak flux \\(\\Phi_{{\\max}}\\)</li>
  <li>The peak induced EMF \\(|\\text{{EMF}}_{{2,\\text{{peak}}}}|\\)</li>
</ol>
<p>Does the EMF increase or decrease? By approximately what factor? Justify your reasoning.</p>
<p>[[input:ans5]]</p>
<p>[[validation:ans5]]</p>"""


def gen_generalfeedback(v, vals):
    """Generate solution feedback."""
    return f"""<h4>Solution for {v['id']} ({v['name']})</h4>
<p><strong>Part (a):</strong></p>
<p>\\(\\mathcal{{R}}_{{\\text{{core}}}} = \\frac{{\\ell_c}}{{\\mu_r \\mu_0 A_c}} = {{@float(R_core)@}}\\;\\text{{A-turns/Wb}}\\)</p>
<p>\\(\\mathcal{{R}}_{{\\text{{gap}}}} = \\frac{{\\ell_g}}{{\\mu_0 A_c}} = {{@float(R_gap)@}}\\;\\text{{A-turns/Wb}}\\)</p>
<p>\\(\\mathcal{{R}}_{{\\text{{total}}}} = {{@R_total_num@}}\\;\\text{{A-turns/Wb}}\\)</p>

<p><strong>Part (b):</strong></p>
<p>\\(\\Phi_{{\\max}} = \\frac{{N_1 I_0}}{{\\mathcal{{R}}_{{\\text{{total}}}}}} = {{@Phi_max_num@}}\\;\\text{{Wb}}\\)</p>

<p><strong>Part (c):</strong></p>
<p>\\(\\omega = 2\\pi f = {{@float(omega_val)@}}\\;\\text{{rad/s}}\\)</p>
<p>\\(|\\text{{EMF}}_{{2,\\text{{peak}}}}| = N_2 \\cdot \\omega \\cdot \\Phi_{{\\max}} = {{@emf_peak_num@}}\\;\\text{{V}}\\)</p>

<p><strong>Part (d):</strong> The errors in the worked solution are statements {{@correct_errors@}}.</p>

<p><strong>Part (e):</strong> If \\(\\ell_g\\) doubles:</p>
<ul>
  <li>\\(\\mathcal{{R}}_{{\\text{{gap}}}}\\) roughly doubles (since \\(\\mathcal{{R}}_{{\\text{{gap}}}} \\propto \\ell_g\\))</li>
  <li>\\(\\mathcal{{R}}_{{\\text{{total}}}}\\) increases (but not by 2&times; because the core reluctance is unchanged)</li>
  <li>\\(\\Phi_{{\\max}}\\) decreases (inversely proportional to \\(\\mathcal{{R}}_{{\\text{{total}}}}\\))</li>
  <li>\\(|\\text{{EMF}}_{{2,\\text{{peak}}}}|\\) decreases by the same factor as \\(\\Phi_{{\\max}}\\)</li>
</ul>"""


def gen_prt_reluctance():
    """PRT for ans1 (reluctance), 2 points."""
    return """    <prt>
      <name>prt_reluctance</name>
      <value>2.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans1</sans>
        <tans>ta_reluctance</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_reluctance-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct total reluctance.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>1</falsenextnode>
        <falseanswernote>prt_reluctance-1-F</falseanswernote>
        <falsefeedback format="html"><text></text></falsefeedback>
      </node>
      <node>
        <name>1</name>
        <answertest>NumRelative</answertest>
        <sans>ans1</sans>
        <tans>float(R_core)</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>0.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_reluctance-2-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>You calculated the core reluctance only. You must add the air gap reluctance: \\(\\mathcal{R}_{\\text{gap}} = \\frac{\\ell_g}{\\mu_0 A_c}\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_reluctance-2-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(\\mathcal{R}_{\\text{total}} = \\frac{\\ell_c}{\\mu_r \\mu_0 A_c} + \\frac{\\ell_g}{\\mu_0 A_c}\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_prt_flux():
    """PRT for ans2 (flux), 2 points."""
    return """    <prt>
      <name>prt_flux</name>
      <value>2.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans2</sans>
        <tans>ta_flux</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_flux-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct peak flux.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>1</falsenextnode>
        <falseanswernote>prt_flux-1-F</falseanswernote>
        <falsefeedback format="html"><text></text></falsefeedback>
      </node>
      <node>
        <name>1</name>
        <answertest>NumRelative</answertest>
        <sans>ans2</sans>
        <tans>float(Phi_no_gap)</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>0.3000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_flux-2-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>This flux value ignores the air gap. You must use the total reluctance (core + gap) in \\(\\Phi_{\\max} = \\frac{N_1 I_0}{\\mathcal{R}_{\\text{total}}}\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_flux-2-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(\\Phi_{\\max} = \\frac{N_1 I_0}{\\mathcal{R}_{\\text{total}}}\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_prt_emf():
    """PRT for ans3 (EMF), 1 point."""
    return """    <prt>
      <name>prt_emf</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans3</sans>
        <tans>ta_emf</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_emf-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct peak induced EMF.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>1</falsenextnode>
        <falseanswernote>prt_emf-1-F</falseanswernote>
        <falsefeedback format="html"><text></text></falsefeedback>
      </node>
      <node>
        <name>1</name>
        <answertest>NumRelative</answertest>
        <sans>ans3</sans>
        <tans>float(emf_no_omega)</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>0.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_emf-2-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>You forgot the \\(\\omega\\) factor. The derivative of \\(\\sin(\\omega t)\\) is \\(\\omega \\cos(\\omega t)\\), so \\(|\\text{EMF}_{2,\\text{peak}}| = N_2 \\cdot \\omega \\cdot \\Phi_{\\max}\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>2</falsenextnode>
        <falseanswernote>prt_emf-2-F</falseanswernote>
        <falsefeedback format="html"><text></text></falsefeedback>
      </node>
      <node>
        <name>2</name>
        <answertest>NumRelative</answertest>
        <sans>ans3</sans>
        <tans>float(emf_wrong_N)</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>0.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_emf-3-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>You used \\(N_1\\) instead of \\(N_2\\). The induced EMF in the secondary coil uses \\(N_2\\): \\(|\\text{EMF}_{2,\\text{peak}}| = N_2 \\cdot \\omega \\cdot \\Phi_{\\max}\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_emf-3-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(|\\text{EMF}_{2,\\text{peak}}| = N_2 \\cdot \\omega \\cdot \\Phi_{\\max}\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_prt_debug():
    """PRT for ans4 (debug checkbox), 1 point."""
    return """    <prt>
      <name>prt_debug</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>Sets</answertest>
        <sans>ans4</sans>
        <tans>ta_debug</tans>
        <testoptions></testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_debug-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct! You identified all errors in the worked solution.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_debug-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Not all errors were correctly identified. Review the worked solution carefully.</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_inputs():
    """Generate the 5 input definitions."""
    return """    <input>
      <name>ans1</name>
      <type>numerical</type>
      <tans>ta_reluctance</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>1.23e5</syntaxhint>
      <syntaxattribute>0</syntaxattribute>
      <forbidwords></forbidwords>
      <allowwords></allowwords>
      <forbidfloat>0</forbidfloat>
      <requirelowestterms>0</requirelowestterms>
      <checkanswertype>0</checkanswertype>
      <mustverify>1</mustverify>
      <showvalidation>1</showvalidation>
      <options></options>
    </input>
    <input>
      <name>ans2</name>
      <type>numerical</type>
      <tans>ta_flux</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>4.56e-4</syntaxhint>
      <syntaxattribute>0</syntaxattribute>
      <forbidwords></forbidwords>
      <allowwords></allowwords>
      <forbidfloat>0</forbidfloat>
      <requirelowestterms>0</requirelowestterms>
      <checkanswertype>0</checkanswertype>
      <mustverify>1</mustverify>
      <showvalidation>1</showvalidation>
      <options></options>
    </input>
    <input>
      <name>ans3</name>
      <type>numerical</type>
      <tans>ta_emf</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>0.567</syntaxhint>
      <syntaxattribute>0</syntaxattribute>
      <forbidwords></forbidwords>
      <allowwords></allowwords>
      <forbidfloat>0</forbidfloat>
      <requirelowestterms>0</requirelowestterms>
      <checkanswertype>0</checkanswertype>
      <mustverify>1</mustverify>
      <showvalidation>1</showvalidation>
      <options></options>
    </input>
    <input>
      <name>ans4</name>
      <type>checkbox</type>
      <tans>ta_debug</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>0</insertstars>
      <syntaxhint></syntaxhint>
      <syntaxattribute>0</syntaxattribute>
      <forbidwords></forbidwords>
      <allowwords></allowwords>
      <forbidfloat>1</forbidfloat>
      <requirelowestterms>0</requirelowestterms>
      <checkanswertype>0</checkanswertype>
      <mustverify>0</mustverify>
      <showvalidation>0</showvalidation>
      <options></options>
    </input>
    <input>
      <name>ans5</name>
      <type>essay</type>
      <tans></tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>0</insertstars>
      <syntaxhint></syntaxhint>
      <syntaxattribute>0</syntaxattribute>
      <forbidwords></forbidwords>
      <allowwords></allowwords>
      <forbidfloat>1</forbidfloat>
      <requirelowestterms>0</requirelowestterms>
      <checkanswertype>0</checkanswertype>
      <mustverify>0</mustverify>
      <showvalidation>0</showvalidation>
      <options></options>
    </input>"""


def gen_variant(v):
    """Generate a complete <question> element for one variant."""
    vals = compute_values(v)
    qvars = gen_questionvariables(v, vals)
    qtext = gen_questiontext(v, vals)
    gfb = gen_generalfeedback(v, vals)

    return f"""<question type="stack">
  <name>
    <text>Midterm 2 - Q1{v['id']}: Magnetic Circuit + Faraday ({v['name']})</text>
  </name>
  <questiontext format="html">
    <text><![CDATA[
{qtext}
]]></text>
  </questiontext>
  <generalfeedback format="html">
    <text><![CDATA[
{gfb}
]]></text>
  </generalfeedback>
  <defaultgrade>9</defaultgrade>
  <penalty>0.1000000</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <stackversion>
    <text>2024032401</text>
  </stackversion>
  <questionvariables>
    <text><![CDATA[
{qvars}
]]></text>
  </questionvariables>
  <specificfeedback format="html">
    <text><![CDATA[
[[feedback:prt_reluctance]]
[[feedback:prt_flux]]
[[feedback:prt_emf]]
[[feedback:prt_debug]]
]]></text>
  </specificfeedback>
  <questionnote>
    <text>{{@R_total_num@}}, {{@Phi_max_num@}}, {{@emf_peak_num@}}, {{@correct_errors@}}</text>
  </questionnote>
  <questiondescription format="html">
    <text></text>
  </questiondescription>
  <prtcorrect format="html">
    <text><![CDATA[<span style="font-size: 1.5em; color:green;"><i class="fa fa-check"></i></span> Correct answer, well done!]]></text>
  </prtcorrect>
  <prtpartiallycorrect format="html">
    <text><![CDATA[<span style="font-size: 1.5em; color:orange;"><i class="fa fa-adjust"></i></span> Your answer is partially correct.]]></text>
  </prtpartiallycorrect>
  <prtincorrect format="html">
    <text><![CDATA[<span style="font-size: 1.5em; color:red;"><i class="fa fa-times"></i></span> Incorrect answer.]]></text>
  </prtincorrect>
  <multiplicativetries>0</multiplicativetries>
{gen_inputs()}
{gen_prt_reluctance()}
{gen_prt_flux()}
{gen_prt_emf()}
{gen_prt_debug()}
</question>"""


def gen_companion_essay():
    """Generate the companion handwritten upload question."""
    return """<question type="essay">
  <name>
    <text>Midterm 2 - Q1: Upload Handwritten Work (Magnetic Circuit + Faraday)</text>
  </name>
  <questiontext format="html">
    <text><![CDATA[
<h3>Upload Your Handwritten Work for Q1</h3>

<p>Upload clear photos or PDF scans of your <strong>handwritten work</strong> for Question 1 (Magnetic Circuit with Faraday Induction). This is for verification and grading support.</p>

<hr />

<h4>Your uploads must include:</h4>
<ul>
  <li><strong>Part (a) &mdash; Reluctance:</strong>
    <ul>
      <li>The equivalent reluctance circuit you drew from the physical diagram</li>
      <li>Core reluctance and air gap reluctance calculations with units</li>
      <li>Total reluctance clearly stated</li>
    </ul>
  </li>
  <li><strong>Part (b) &mdash; Flux:</strong>
    <ul>
      <li>Application of Ampere&rsquo;s law / reluctance model</li>
      <li>Peak flux calculation showing N&middot;I / R_total</li>
    </ul>
  </li>
  <li><strong>Part (c) &mdash; Induced EMF:</strong>
    <ul>
      <li>Faraday&rsquo;s law setup showing the time derivative</li>
      <li>Differentiation step: d(sin &omega;t)/dt = &omega; cos(&omega;t)</li>
      <li>Final EMF calculation</li>
    </ul>
  </li>
  <li><strong>Part (e) &mdash; Qualitative analysis:</strong>
    <ul>
      <li>Reasoning about how doubling the gap affects each quantity</li>
      <li>Proportionality argument</li>
    </ul>
  </li>
</ul>

<hr />

<h4>Upload Instructions:</h4>
<ol>
  <li>Write your <strong>name and student ID</strong> on every page.</li>
  <li>Use a <strong>dark pen</strong> (blue or black) on white paper.</li>
  <li>Ensure photos are <strong>legible</strong> (good lighting, in focus).</li>
  <li>You may upload up to <strong>2 files</strong>. Accepted: <strong>PDF, JPG, JPEG, PNG</strong>.</li>
</ol>

<p><em>Note: This upload is worth 0 points. Your handwritten work supports the grading of the main question. Failure to upload may affect verification of your answers.</em></p>

<p><strong>Teacher notice:</strong> Ensure &ldquo;Allow attachments&rdquo; is set to 2 or more in Moodle quiz settings &rarr; Files and uploads.</p>
]]></text>
  </questiontext>
  <generalfeedback format="html">
    <text><![CDATA[<p>Thank you for uploading your handwritten work for Q1.</p>]]></text>
  </generalfeedback>
  <defaultgrade>0</defaultgrade>
  <penalty>0</penalty>
  <hidden>0</hidden>
  <responseformat>noinline</responseformat>
  <responserequired>0</responserequired>
  <responsefieldlines>5</responsefieldlines>
  <attachments>2</attachments>
  <attachmentsrequired>1</attachmentsrequired>
  <filetypeslist>.pdf,.jpg,.jpeg,.png</filetypeslist>
  <graderinfo format="html">
    <text><![CDATA[
<h4>Instructor Notes &mdash; Q1 Handwritten Work Review</h4>
<ul>
  <li>Check that the student drew a reluctance circuit from the physical diagram</li>
  <li>Verify correct formulas for R_core and R_gap</li>
  <li>Check Faraday&rsquo;s law differentiation step</li>
  <li>For Part (e): look for proportionality reasoning, not just &ldquo;it decreases&rdquo;</li>
  <li><strong>Red flags:</strong> Final answers with no supporting work, inconsistent handwriting</li>
</ul>
]]></text>
  </graderinfo>
  <responsetemplate format="html">
    <text></text>
  </responsetemplate>
</question>"""


def main():
    """Generate the complete XML file."""
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>", ""]

    for v in VARIANTS:
        parts.append(f"<!-- {'='*60} -->")
        parts.append(f"<!-- Q1 {v['id']}: {v['name']} -->")
        parts.append(f"<!-- {'='*60} -->")
        parts.append(gen_variant(v))
        parts.append("")

    parts.append(f"<!-- {'='*60} -->")
    parts.append("<!-- Companion Essay: Handwritten Upload for Q1 -->")
    parts.append(f"<!-- {'='*60} -->")
    parts.append(gen_companion_essay())
    parts.append("")
    parts.append("</quiz>")

    xml = "\n".join(parts)

    # Determine output path
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base, "xml", "pool_q1_medium.xml")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"Generated {out_path}")
    print(f"  Variants: {len(VARIANTS)}")
    print(f"  Total lines: {xml.count(chr(10)) + 1}")

    # Verify computed values
    print("\nVerification table:")
    print(f"{'Variant':<8} {'R_total':>15} {'Phi_max':>15} {'EMF_peak':>12} {'Errors'}")
    for v in VARIANTS:
        vals = compute_values(v)
        print(f"{v['id']:<8} {vals['R_total']:>15.1f} {vals['Phi_max']:>15.6e} {vals['emf_peak']:>12.4f} {v['debug_errors']}")


if __name__ == "__main__":
    main()
