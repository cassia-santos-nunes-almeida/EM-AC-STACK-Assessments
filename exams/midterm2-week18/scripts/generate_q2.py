#!/usr/bin/env python
"""
Generate pool_q2_medium.xml — RLC Transient with Waveform Debug
Midterm 2, Q2 (Medium, 9 pts), 4 variants + companion essay

Textbook: Nilsson & Riedel Ch.8 Problems 8.1-8.8 (series), 8.14-8.22 (parallel)
"""

import math
import os

# ─── Variant definitions ────────────────────────────────────────────

VARIANTS = [
    {
        "id": "V1",
        "name": "Series RLC Natural Response, Underdamped",
        "topology": "series", "response": "natural", "regime": "underdamped",
        "R": 10, "L": 0.01, "C": 50e-6,  # R=10 Ohm, L=10mH, C=50uF
        "Vs": 20, "Is": None,  # voltage source for charging
        "t1": 0.001,  # evaluation time = 1 ms
        "R_display": "10\\;\\Omega", "L_display": "10\\;\\text{mH}",
        "C_display": "50\\;\\mu\\text{F}", "source_display": "V_s = 20\\;\\text{V}",
        "circuit_desc": (
            "A series RLC circuit is powered by a DC voltage source \\(V_s\\). "
            "The capacitor is fully charged in steady state. At \\(t = 0\\), a switch disconnects "
            "the source, leaving the series R-L-C loop closed for current to flow."
        ),
        "initial_cond_desc": (
            "Before switching: \\(v_C(0^-) = V_s\\), \\(i_L(0^-) = 0\\) (capacitor fully charged, "
            "no current in steady state)."
        ),
        "ask_variable": "i",  # asking for i(t1)
        "ask_desc": "the current \\(i(t_1)\\) at \\(t_1 = 1\\;\\text{ms}\\)",
        "waveform_errors_desc": (
            "A student plotted \\(i(t)\\) for \\(t > 0\\). Their plot shows:<br/>"
            "(i) The current starts at \\(i(0^+) = 2\\;\\text{A}\\) (but it should start at 0).<br/>"
            "(ii) The oscillation envelope decays with a time constant of 4 ms "
            "(but \\(1/\\alpha = 2\\;\\text{ms}\\)).<br/>"
            "(iii) The oscillation frequency appears correct.<br/>"
            "(iv) The current approaches 0 as \\(t \\to \\infty\\) (correct for natural response)."
        ),
        "debug_errors": [1, 2],
        "debug_options": [
            ("The initial value i(0+) is wrong; it should be 0 for a fully charged capacitor", True),
            ("The decay envelope uses the wrong time constant (too slow)", True),
            ("The oscillation frequency does not match the damped frequency omega_d", False),
            ("The final value should approach a nonzero DC level", False),
            ("The waveform should not oscillate because the circuit is overdamped", False),
        ],
    },
    {
        "id": "V2",
        "name": "Parallel RLC Step Response, Overdamped",
        "topology": "parallel", "response": "step", "regime": "overdamped",
        "R": 20, "L": 0.1, "C": 10e-6,  # R=20 Ohm, L=100mH, C=10uF
        "Vs": None, "Is": 0.1,  # current source step
        "t1": 0.0005,  # evaluation time = 0.5 ms
        "R_display": "20\\;\\Omega", "L_display": "100\\;\\text{mH}",
        "C_display": "10\\;\\mu\\text{F}", "source_display": "I_s = 100\\;\\text{mA}",
        "circuit_desc": (
            "A parallel RLC circuit has zero initial conditions. At \\(t = 0\\), a DC current source "
            "\\(I_s\\) is switched on, delivering current to the parallel combination of R, L, and C."
        ),
        "initial_cond_desc": (
            "Before switching: \\(v(0^-) = 0\\), \\(i_L(0^-) = 0\\) (all zero initial conditions)."
        ),
        "ask_variable": "v",
        "ask_desc": "the voltage \\(v(t_1)\\) across the parallel combination at \\(t_1 = 0.5\\;\\text{ms}\\)",
        "waveform_errors_desc": (
            "A student plotted \\(v(t)\\) for \\(t > 0\\). Their plot shows:<br/>"
            "(i) The voltage starts at \\(v(0^+) = 0\\) (correct).<br/>"
            "(ii) The voltage oscillates with a damped sinusoid (but the circuit is overdamped!).<br/>"
            "(iii) The voltage approaches \\(v(\\infty) = I_s \\cdot R = 2\\;\\text{V}\\) "
            "(but at DC, the inductor is a short, so \\(v(\\infty) = 0\\)).<br/>"
            "(iv) The voltage rises then falls back — double exponential shape."
        ),
        "debug_errors": [2, 3],
        "debug_options": [
            ("The initial value v(0+) = 0 is correct", False),
            ("The waveform should NOT oscillate because the circuit is overdamped", True),
            ("The final value v(infinity) should be 0, not I_s*R", True),
            ("The damping coefficient alpha was computed with the wrong formula", False),
            ("The waveform should start at a nonzero value", False),
        ],
    },
    {
        "id": "V3",
        "name": "Series RLC Step Response, Critically Damped",
        "topology": "series", "response": "step", "regime": "critically_damped",
        "R": 200, "L": 0.1, "C": 10e-6,  # R=200 Ohm, L=100mH, C=10uF
        "Vs": 10, "Is": None,
        "t1": 0.002,  # 2 ms
        "R_display": "200\\;\\Omega", "L_display": "100\\;\\text{mH}",
        "C_display": "10\\;\\mu\\text{F}", "source_display": "V_s = 10\\;\\text{V}",
        "circuit_desc": (
            "A series RLC circuit with zero initial conditions is connected to a DC voltage source "
            "\\(V_s\\) at \\(t = 0\\). The circuit response is the capacitor voltage \\(v_C(t)\\)."
        ),
        "initial_cond_desc": (
            "Before switching: \\(v_C(0^-) = 0\\), \\(i_L(0^-) = 0\\) (zero initial conditions)."
        ),
        "ask_variable": "v_C",
        "ask_desc": "the capacitor voltage \\(v_C(t_1)\\) at \\(t_1 = 2\\;\\text{ms}\\)",
        "waveform_errors_desc": (
            "A student plotted \\(v_C(t)\\) for \\(t > 0\\). Their plot shows:<br/>"
            "(i) \\(v_C(0^+) = V_s = 10\\;\\text{V}\\) (but it should start at 0!).<br/>"
            "(ii) The voltage overshoots \\(V_s\\) before settling "
            "(but critically damped response does NOT overshoot!).<br/>"
            "(iii) The final value is \\(v_C(\\infty) = V_s = 10\\;\\text{V}\\) (correct).<br/>"
            "(iv) The response reaches 63% of final value in about 1 ms."
        ),
        "debug_errors": [1, 2],
        "debug_options": [
            ("The initial value v_C(0+) should be 0, not V_s", True),
            ("A critically damped response does NOT overshoot; the plot is wrong", True),
            ("The final value v_C(infinity) = V_s is correct for a step response", False),
            ("The time constant is wrong; it should be 1/alpha = 1 ms", False),
            ("The circuit is actually underdamped, not critically damped", False),
        ],
    },
    {
        "id": "V4",
        "name": "Parallel RLC Natural Response, Underdamped",
        "topology": "parallel", "response": "natural", "regime": "underdamped",
        "R": 100, "L": 0.025, "C": 5e-6,  # R=100 Ohm, L=25mH, C=5uF
        "Vs": None, "Is": None, "V0": 15,  # pre-charged capacitor
        "t1": 0.0005,  # 0.5 ms
        "R_display": "100\\;\\Omega", "L_display": "25\\;\\text{mH}",
        "C_display": "5\\;\\mu\\text{F}", "source_display": "V_0 = 15\\;\\text{V}",
        "circuit_desc": (
            "A parallel RLC circuit has a capacitor pre-charged to \\(V_0\\). "
            "At \\(t = 0\\), a switch closes, connecting the capacitor to R and L in parallel. "
            "The voltage \\(v(t)\\) across the combination is the response."
        ),
        "initial_cond_desc": (
            "Before switching: \\(v(0^-) = V_0 = 15\\;\\text{V}\\), \\(i_L(0^-) = 0\\)."
        ),
        "ask_variable": "v",
        "ask_desc": "the voltage \\(v(t_1)\\) at \\(t_1 = 0.5\\;\\text{ms}\\)",
        "waveform_errors_desc": (
            "A student plotted \\(v(t)\\) for \\(t > 0\\). Their plot shows:<br/>"
            "(i) The voltage starts at \\(v(0^+) = V_0 = 15\\;\\text{V}\\) (correct).<br/>"
            "(ii) The envelope decays with time constant \\(1/\\omega_0\\) instead of \\(1/\\alpha\\).<br/>"
            "(iii) The oscillation frequency is \\(\\omega_0\\) instead of the damped frequency "
            "\\(\\omega_d = \\sqrt{\\omega_0^2 - \\alpha^2}\\).<br/>"
            "(iv) The voltage approaches 0 as \\(t \\to \\infty\\) (correct for natural response)."
        ),
        "debug_errors": [2, 3],
        "debug_options": [
            ("The initial value v(0+) = V_0 is correct", False),
            ("The decay envelope uses omega_0 instead of alpha for the time constant", True),
            ("The oscillation frequency should be omega_d, not omega_0", True),
            ("The final value should be nonzero", False),
            ("The waveform should be a pure exponential (no oscillation)", False),
        ],
    },
]


def compute_values(v):
    """Compute all derived values for a variant."""
    R, L, C = v["R"], v["L"], v["C"]

    if v["topology"] == "series":
        alpha = R / (2 * L)
        alpha_wrong = 1 / (2 * R * C)  # parallel formula (wrong)
    else:
        alpha = 1 / (2 * R * C)
        alpha_wrong = R / (2 * L)  # series formula (wrong)

    omega0 = 1 / math.sqrt(L * C)

    if v["regime"] == "underdamped":
        omega_d = math.sqrt(omega0**2 - alpha**2)
    else:
        omega_d = 0

    t1 = v["t1"]

    # Compute the response value at t1
    if v["id"] == "V1":
        # Series RLC natural, underdamped: i(t) = (Vs/(omega_d*L)) * exp(-alpha*t) * sin(omega_d*t)
        Vs = v["Vs"]
        val_at_t1 = (Vs / (omega_d * L)) * math.exp(-alpha * t1) * math.sin(omega_d * t1)
    elif v["id"] == "V2":
        # Parallel RLC step, overdamped: v(t) = A1*exp(s1*t) + A2*exp(s2*t)
        Is = v["Is"]
        disc = math.sqrt(alpha**2 - omega0**2)
        s1 = -alpha + disc
        s2 = -alpha - disc
        # v(0+) = 0, dv/dt(0+) = Is/C
        A1 = Is / (C * (s1 - s2))
        A2 = -A1
        val_at_t1 = A1 * math.exp(s1 * t1) + A2 * math.exp(s2 * t1)
    elif v["id"] == "V3":
        # Series RLC step, critically damped: vC(t) = Vs*(1 - (1 + alpha*t)*exp(-alpha*t))
        Vs = v["Vs"]
        val_at_t1 = Vs * (1 - (1 + alpha * t1) * math.exp(-alpha * t1))
    elif v["id"] == "V4":
        # Parallel RLC natural, underdamped: v(t) = V0*exp(-alpha*t)*(cos(omega_d*t) - (alpha/omega_d)*sin(omega_d*t))
        # Sign: dv/dt(0+) = -(V0)/(RC) = -2*alpha*V0, so A2 = -V0*alpha/omega_d (negative)
        V0 = v["V0"]
        val_at_t1 = V0 * math.exp(-alpha * t1) * (
            math.cos(omega_d * t1) - (alpha / omega_d) * math.sin(omega_d * t1)
        )

    return {
        "alpha": alpha, "omega0": omega0, "omega_d": omega_d,
        "alpha_wrong": alpha_wrong, "val_at_t1": val_at_t1,
    }


def gen_questionvariables(v, vals):
    """Generate Maxima questionvariables."""
    R, L, C = v["R"], v["L"], v["C"]

    if v["topology"] == "series":
        alpha_formula = f"R_val/(2*L_val)"
        alpha_wrong_formula = f"1/(2*R_val*C_val)"
    else:
        alpha_formula = f"1/(2*R_val*C_val)"
        alpha_wrong_formula = f"R_val/(2*L_val)"

    regime_map = {
        "underdamped": ("Underdamped", "Overdamped", "Critically damped"),
        "overdamped": ("Overdamped", "Underdamped", "Critically damped"),
        "critically_damped": ("Critically damped", "Underdamped", "Overdamped"),
    }
    correct_r, wrong1, wrong2 = regime_map[v["regime"]]

    # Build response formula in Maxima
    if v["id"] == "V1":
        source_vars = f"Vs_val: {v['Vs']};"
        response_formula = "val_at_t1: float((Vs_val/(omega_d*L_val))*exp(-alpha_val*t1)*sin(omega_d*t1));"
        omega_d_line = "omega_d: sqrt(omega0_val^2 - alpha_val^2);"
    elif v["id"] == "V2":
        source_vars = f"Is_val: {v['Is']};"
        response_formula = """disc: sqrt(alpha_val^2 - omega0_val^2);
s1: -alpha_val + disc;
s2: -alpha_val - disc;
A1: Is_val/(C_val*(s1 - s2));
A2: -A1;
val_at_t1: float(A1*exp(s1*t1) + A2*exp(s2*t1));"""
        omega_d_line = "omega_d: 0;  /* overdamped — no oscillation */"
    elif v["id"] == "V3":
        source_vars = f"Vs_val: {v['Vs']};"
        response_formula = "val_at_t1: float(Vs_val*(1 - (1 + alpha_val*t1)*exp(-alpha_val*t1)));"
        omega_d_line = "omega_d: 0;  /* critically damped */"
    elif v["id"] == "V4":
        source_vars = f"V0_val: {v['V0']};"
        response_formula = """omega_d: sqrt(omega0_val^2 - alpha_val^2);
val_at_t1: float(V0_val*exp(-alpha_val*t1)*(cos(omega_d*t1) + (alpha_val/omega_d)*sin(omega_d*t1)));"""
        omega_d_line = "omega_d: sqrt(omega0_val^2 - alpha_val^2);"

    # Debug options
    opts = []
    for i, (text, is_err) in enumerate(v["debug_options"], 1):
        bval = "true" if is_err else "false"
        opts.append(f'[{i}, {bval}, "{text}"]')
    opts_str = "[" + ", ".join(opts) + "]"
    correct_set = "{" + ",".join(str(i) for i in v["debug_errors"]) + "}"

    return f"""/* {v['id']}: {v['name']} */
R_val: {R};
L_val: {L};
C_val: {C};
{source_vars}
t1: {v['t1']};

/* Damping parameters */
alpha_val: {alpha_formula};
omega0_val: 1/sqrt(L_val*C_val);
{omega_d_line}

/* Wrong alpha (other topology formula) for error detection */
alpha_wrong: {alpha_wrong_formula};

/* Regime classification MCQ */
regime_opts: random_permutation([[1, true, "{correct_r}"], [2, false, "{wrong1}"], [3, false, "{wrong2}"]]);

/* Response at t1 */
{response_formula}

/* Debug MCQ-MA */
debug_opts: random_permutation({opts_str});
correct_errors: {correct_set};

/* Teacher answers */
ta_alpha: float(alpha_val);
ta_omega0: float(omega0_val);
ta_regime: regime_opts;
ta_value: val_at_t1;
ta_debug: correct_errors;"""


def gen_questiontext(v, vals):
    """Generate question HTML."""
    t1_ms = v["t1"] * 1000

    return f"""<h3>Midterm 2 &ndash; Q2{v['id']}: RLC Transient with Waveform Debug ({v['name']})</h3>
<p><em>Electromagnetism and Circuit Analysis &mdash; LUT University, Finland</em></p>
<p><strong>Total: 9 points | Penalty per wrong attempt: 10%</strong></p>
<p><em>Inspired by Nilsson &amp; Riedel Ch.8.</em></p>
<hr />

<h4>Circuit Description</h4>
<p>{v['circuit_desc']}</p>
<p>[DIAGRAM: {v['name']} &mdash; CircuiTikZ diagram to be added]</p>

<h4>Component Values</h4>
<ul>
  <li>\\(R = {v['R_display']}\\)</li>
  <li>\\(L = {v['L_display']}\\)</li>
  <li>\\(C = {v['C_display']}\\)</li>
  <li>Source: \\({v['source_display']}\\)</li>
</ul>

<h4>Initial Conditions</h4>
<p>{v['initial_cond_desc']}</p>

<hr />

<h4>Part (a) &mdash; Damping Parameters and Classification (2 points)</h4>
<p>Calculate the <strong>neper frequency</strong> (damping coefficient) \\(\\alpha\\) and the <strong>resonant frequency</strong> \\(\\omega_0\\).</p>
<p>\\(\\alpha = \\) [[input:ans1]] \\(\\text{{Np/s}}\\) &nbsp; [[validation:ans1]]</p>
<p><em>Enter a number, e.g. <code>1234</code></em></p>

<p>\\(\\omega_0 = \\) [[input:ans2]] \\(\\text{{rad/s}}\\) &nbsp; [[validation:ans2]]</p>
<p><em>Enter a number, e.g. <code>5678</code></em></p>

<p>Classify the damping regime: [[input:ans3]] &nbsp; [[validation:ans3]]</p>

<h4>Part (b) &mdash; Response Value (2 points)</h4>
<p>Calculate {v['ask_desc']}.</p>
<p>\\({v['ask_variable']}(t_1) = \\) [[input:ans4]] &nbsp; [[validation:ans4]]</p>
<p><em>Enter a number, e.g. <code>0.567</code></em></p>

<h4>Part (c) &mdash; Waveform Error Identification (2 points)</h4>
<p>A student attempted to plot the response and made errors. Their waveform is described below:</p>
<blockquote>{v['waveform_errors_desc']}</blockquote>
<p><strong>Select ALL statements that identify actual errors in the student&rsquo;s waveform:</strong></p>
<p>[[input:ans5]] &nbsp; [[validation:ans5]]</p>

<h4>Part (d) &mdash; Parameter Sensitivity (3 points, manually graded)</h4>
<p>Suppose the resistance \\(R\\) is <strong>doubled</strong>.</p>
<ol>
  <li>How does this change \\(\\alpha\\)?</li>
  <li>Does the damping regime change? If so, from what to what?</li>
  <li>Sketch the qualitative shape of the new response and explain whether energy dissipation is faster or slower.</li>
</ol>
<p>[[input:ans6]] &nbsp; [[validation:ans6]]</p>"""


def gen_generalfeedback(v, vals):
    """Generate solution feedback."""
    if v["topology"] == "series":
        alpha_formula_text = "\\\\alpha = \\\\frac{R}{2L}"
    else:
        alpha_formula_text = "\\\\alpha = \\\\frac{1}{2RC}"

    regime_text = v["regime"].replace("_", " ")

    return f"""<h4>Solution for {v['id']} ({v['name']})</h4>
<p><strong>Part (a):</strong></p>
<p>\\({alpha_formula_text} = {{@ta_alpha@}}\\;\\text{{Np/s}}\\)</p>
<p>\\(\\omega_0 = \\frac{{1}}{{\\sqrt{{LC}}}} = {{@ta_omega0@}}\\;\\text{{rad/s}}\\)</p>
<p>Since \\(\\alpha {'<' if v['regime'] == 'underdamped' else '>' if v['regime'] == 'overdamped' else '='} \\omega_0\\), the circuit is <strong>{regime_text}</strong>.</p>

<p><strong>Part (b):</strong> \\({v['ask_variable']}(t_1) = {{@ta_value@}}\\)</p>

<p><strong>Part (c):</strong> The errors are statements {{@correct_errors@}}.</p>

<p><strong>Part (d):</strong> When R doubles:</p>
<ul>
  <li>{'\\(\\alpha\\) doubles (since \\(\\alpha = R/(2L)\\))' if v['topology'] == 'series' else '\\(\\alpha\\) halves (since \\(\\alpha = 1/(2RC)\\))'}</li>
  <li>The damping regime may change depending on the new \\(\\alpha\\) vs \\(\\omega_0\\)</li>
  <li>{'More damping = faster energy dissipation, response decays quicker' if v['topology'] == 'series' else 'Less damping = slower energy dissipation, response oscillates more'}</li>
</ul>"""


def gen_inputs():
    """Generate input definitions for Q2."""
    return """    <input>
      <name>ans1</name>
      <type>numerical</type>
      <tans>ta_alpha</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>1234</syntaxhint>
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
      <tans>ta_omega0</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>5678</syntaxhint>
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
      <type>dropdown</type>
      <tans>ta_regime</tans>
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
      <name>ans4</name>
      <type>numerical</type>
      <tans>ta_value</tans>
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
      <name>ans5</name>
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
      <name>ans6</name>
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


def gen_prt_alpha():
    """PRT for ans1 (alpha), weight toward 1 pt."""
    return """    <prt>
      <name>prt_alpha</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans1</sans>
        <tans>ta_alpha</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_alpha-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct \\(\\alpha\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>1</falsenextnode>
        <falseanswernote>prt_alpha-1-F</falseanswernote>
        <falsefeedback format="html"><text></text></falsefeedback>
      </node>
      <node>
        <name>1</name>
        <answertest>NumRelative</answertest>
        <sans>ans1</sans>
        <tans>float(alpha_wrong)</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>0.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_alpha-2-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>You used the wrong formula. Check whether this is a series or parallel RLC circuit and use the correct \\(\\alpha\\) formula.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_alpha-2-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect \\(\\alpha\\). Review the damping coefficient formula for this circuit topology.</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_prt_omega0():
    """PRT for ans2 (omega0), 0.5 pt."""
    return """    <prt>
      <name>prt_omega0</name>
      <value>0.5000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans2</sans>
        <tans>ta_omega0</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_omega0-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct \\(\\omega_0\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_omega0-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(\\omega_0 = 1/\\sqrt{LC}\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_prt_regime():
    """PRT for ans3 (regime dropdown), 0.5 pt."""
    return """    <prt>
      <name>prt_regime</name>
      <value>0.5000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>AlgEquiv</answertest>
        <sans>ans3</sans>
        <tans>1</tans>
        <testoptions></testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_regime-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct classification.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_regime-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. Compare \\(\\alpha\\) with \\(\\omega_0\\): if \\(\\alpha < \\omega_0\\), underdamped; if \\(\\alpha > \\omega_0\\), overdamped; if \\(\\alpha = \\omega_0\\), critically damped.</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_prt_value():
    """PRT for ans4 (response value), 2 pts."""
    return """    <prt>
      <name>prt_value</name>
      <value>2.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans4</sans>
        <tans>ta_value</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_value-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct response value.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_value-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. Review the response formula for this damping regime and check your calculations.</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_prt_debug():
    """PRT for ans5 (debug checkbox), 2 pts."""
    return """    <prt>
      <name>prt_debug</name>
      <value>2.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>Sets</answertest>
        <sans>ans5</sans>
        <tans>ta_debug</tans>
        <testoptions></testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_debug-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct! You identified all waveform errors.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_debug-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Not all waveform errors were correctly identified.</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_variant(v):
    """Generate a complete <question> element for one variant."""
    vals = compute_values(v)
    qvars = gen_questionvariables(v, vals)
    qtext = gen_questiontext(v, vals)
    gfb = gen_generalfeedback(v, vals)

    return f"""<question type="stack">
  <name>
    <text>Midterm 2 - Q2{v['id']}: RLC Transient + Debug ({v['name']})</text>
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
[[feedback:prt_alpha]]
[[feedback:prt_omega0]]
[[feedback:prt_regime]]
[[feedback:prt_value]]
[[feedback:prt_debug]]
]]></text>
  </specificfeedback>
  <questionnote>
    <text>{{@ta_alpha@}}, {{@ta_omega0@}}, {{@ta_value@}}, {{@correct_errors@}}</text>
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
{gen_prt_alpha()}
{gen_prt_omega0()}
{gen_prt_regime()}
{gen_prt_value()}
{gen_prt_debug()}
</question>"""


def gen_companion_essay():
    """Generate companion upload question."""
    return """<question type="essay">
  <name>
    <text>Midterm 2 - Q2: Upload Handwritten Work (RLC Transient)</text>
  </name>
  <questiontext format="html">
    <text><![CDATA[
<h3>Upload Your Handwritten Work for Q2</h3>

<p>Upload clear photos or PDF scans of your <strong>handwritten work</strong> for Question 2 (RLC Transient with Waveform Debug).</p>

<hr />

<h4>Your uploads must include:</h4>
<ul>
  <li><strong>Part (a):</strong>
    <ul>
      <li>\\(\\alpha\\) calculation with the correct formula for the circuit topology</li>
      <li>\\(\\omega_0\\) calculation</li>
      <li>Classification logic: comparison of \\(\\alpha\\) vs \\(\\omega_0\\)</li>
    </ul>
  </li>
  <li><strong>Part (b):</strong>
    <ul>
      <li>Response formula setup (which form: overdamped, underdamped, or critically damped)</li>
      <li>Coefficient calculation from initial conditions</li>
      <li>Evaluation at \\(t_1\\)</li>
    </ul>
  </li>
  <li><strong>Part (d):</strong>
    <ul>
      <li>New \\(\\alpha\\) calculation with doubled R</li>
      <li>Qualitative waveform sketch showing the change in behavior</li>
      <li>Energy dissipation reasoning</li>
    </ul>
  </li>
</ul>

<h4>Upload Instructions:</h4>
<ol>
  <li>Write your <strong>name and student ID</strong> on every page.</li>
  <li>Use a <strong>dark pen</strong> (blue or black) on white paper.</li>
  <li>Ensure photos are <strong>legible</strong>.</li>
  <li>Up to <strong>2 files</strong>. Accepted: <strong>PDF, JPG, JPEG, PNG</strong>.</li>
</ol>

<p><em>Worth 0 points. Supports grading verification.</em></p>
<p><strong>Teacher notice:</strong> Set &ldquo;Allow attachments&rdquo; to 2+ in quiz settings.</p>
]]></text>
  </questiontext>
  <generalfeedback format="html">
    <text><![CDATA[<p>Thank you for uploading your handwritten work for Q2.</p>]]></text>
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
<h4>Instructor Notes &mdash; Q2 Handwritten Work Review</h4>
<ul>
  <li>Check correct \\(\\alpha\\) formula for the topology (series vs parallel)</li>
  <li>Verify response form matches the damping regime</li>
  <li>For Part (d): look for correct reasoning about how R affects \\(\\alpha\\) and the regime</li>
  <li><strong>Red flags:</strong> Answers without supporting calculations, inconsistent handwriting</li>
</ul>
]]></text>
  </graderinfo>
  <responsetemplate format="html">
    <text></text>
  </responsetemplate>
</question>"""


def main():
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>", ""]

    for v in VARIANTS:
        parts.append(f"<!-- {'='*60} -->")
        parts.append(f"<!-- Q2 {v['id']}: {v['name']} -->")
        parts.append(f"<!-- {'='*60} -->")
        parts.append(gen_variant(v))
        parts.append("")

    parts.append(f"<!-- {'='*60} -->")
    parts.append("<!-- Companion Essay: Handwritten Upload for Q2 -->")
    parts.append(f"<!-- {'='*60} -->")
    parts.append(gen_companion_essay())
    parts.append("")
    parts.append("</quiz>")

    xml = "\n".join(parts)

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base, "xml", "pool_q2_medium.xml")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"Generated {out_path}")
    print(f"  Variants: {len(VARIANTS)}")
    print(f"  Total lines: {xml.count(chr(10)) + 1}")

    print("\nVerification table:")
    print(f"{'Var':<4} {'Topology':<10} {'Regime':<18} {'alpha':>10} {'omega0':>10} {'val@t1':>12} {'Errors'}")
    for v in VARIANTS:
        vals = compute_values(v)
        print(f"{v['id']:<4} {v['topology']:<10} {v['regime']:<18} {vals['alpha']:>10.1f} {vals['omega0']:>10.1f} {vals['val_at_t1']:>12.6f} {v['debug_errors']}")

    # P-STACK-32 check
    hints = {"ans1": 1234, "ans2": 5678, "ans4": 0.567}
    answers = {"ans1": [], "ans2": [], "ans4": []}
    for v in VARIANTS:
        vals = compute_values(v)
        answers["ans1"].append(vals["alpha"])
        answers["ans2"].append(vals["omega0"])
        answers["ans4"].append(vals["val_at_t1"])

    print("\nP-STACK-32 Syntaxhint Check:")
    all_ok = True
    for inp, hint_val in hints.items():
        for i, ans_val in enumerate(answers[inp], 1):
            if ans_val == 0:
                continue
            ratio = abs(hint_val - ans_val) / abs(ans_val)
            if ratio < 0.15:
                print(f"  FAIL: {inp} hint={hint_val} vs V{i} answer={ans_val:.4g} ({ratio:.3f})")
                all_ok = False
    print("  ALL PASS" if all_ok else "  FAILURES DETECTED")


if __name__ == "__main__":
    main()
