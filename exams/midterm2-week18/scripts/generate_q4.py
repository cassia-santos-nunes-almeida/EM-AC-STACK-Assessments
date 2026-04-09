#!/usr/bin/env python
"""
Generate pool_q4_high.xml — TL Transient + Bounce Diagram
Midterm 2, Q4 (High, 10 pts), 4 variants + companion essay

Parts: (a) TL params 2pt, (b) V at load after reflections 2pt,
       (c) VSWR 1pt, (d) MCQ-MA 1pt, (e) QWT design essay 3pt
Note: JSXGraph bounce diagram deferred to Phase 5 integration.
Textbook: Ulaby Ch.2 Example 2-8, Problems 2.32-2.38
"""

import math
import os

VARIANTS = [
    {
        "id": "V1",
        "name": "Resistive Load, R_L > Z0, Matched Source",
        "Z0": 50, "Rg": 50, "RL": 100, "Vg": 10, "length": 0.5, "vp": 2e8,
        "desc": (
            "A lossless transmission line with characteristic impedance \\(Z_0 = 50\\;\\Omega\\) "
            "and length \\(\\ell = 0.5\\;\\text{m}\\) connects a source (\\(V_g = 10\\;\\text{V}\\), "
            "\\(R_g = 50\\;\\Omega\\)) to a resistive load \\(R_L = 100\\;\\Omega\\). "
            "The phase velocity is \\(v_p = 2 \\times 10^8\\;\\text{m/s}\\)."
        ),
    },
    {
        "id": "V2",
        "name": "Resistive Load, R_L < Z0, Mismatched Source",
        "Z0": 75, "Rg": 50, "RL": 25, "Vg": 12, "length": 0.3, "vp": 2e8,
        "desc": (
            "A lossless TL (\\(Z_0 = 75\\;\\Omega\\), \\(\\ell = 0.3\\;\\text{m}\\)) connects "
            "a source (\\(V_g = 12\\;\\text{V}\\), \\(R_g = 50\\;\\Omega\\)) to \\(R_L = 25\\;\\Omega\\). "
            "Phase velocity \\(v_p = 2 \\times 10^8\\;\\text{m/s}\\)."
        ),
    },
    {
        "id": "V3",
        "name": "Short-Circuit Load, Mismatched Source",
        "Z0": 50, "Rg": 100, "RL": 0.001, "Vg": 8, "length": 0.4, "vp": 2e8,
        "desc": (
            "A lossless TL (\\(Z_0 = 50\\;\\Omega\\), \\(\\ell = 0.4\\;\\text{m}\\)) connects "
            "a source (\\(V_g = 8\\;\\text{V}\\), \\(R_g = 100\\;\\Omega\\)) to a "
            "<strong>short-circuit load</strong> (\\(R_L \\approx 0\\)). "
            "Phase velocity \\(v_p = 2 \\times 10^8\\;\\text{m/s}\\)."
        ),
    },
    {
        "id": "V4",
        "name": "Open-Circuit Load, Matched Source",
        "Z0": 50, "Rg": 50, "RL": 1e9, "Vg": 6, "length": 0.6, "vp": 2e8,
        "desc": (
            "A lossless TL (\\(Z_0 = 50\\;\\Omega\\), \\(\\ell = 0.6\\;\\text{m}\\)) connects "
            "a source (\\(V_g = 6\\;\\text{V}\\), \\(R_g = 50\\;\\Omega\\)) to an "
            "<strong>open-circuit load</strong> (\\(R_L \\to \\infty\\)). "
            "Phase velocity \\(v_p = 2 \\times 10^8\\;\\text{m/s}\\)."
        ),
    },
]


def compute_values(v):
    Z0, Rg, RL, Vg = v["Z0"], v["Rg"], v["RL"], v["Vg"]
    length, vp = v["length"], v["vp"]

    Gamma_L = (RL - Z0) / (RL + Z0)
    Gamma_g = (Rg - Z0) / (Rg + Z0)
    V1_plus = Vg * Z0 / (Z0 + Rg)  # initial forward wave
    T = length / vp  # one-way travel time

    # Voltage at load after bounces
    # V(l, t=T) = V1+(1 + Gamma_L)
    V_at_T = V1_plus * (1 + Gamma_L)
    # V(l, t=3T) = V1+(1+GL) + V1+*GL*Gg*(1+GL)
    V_at_3T = V1_plus * (1 + Gamma_L) * (1 + Gamma_L * Gamma_g)
    # V(l, t=5T) adds another bounce
    V_at_5T = V1_plus * (1 + Gamma_L) * (1 + Gamma_L * Gamma_g + (Gamma_L * Gamma_g)**2)

    # Steady-state voltage (DC)
    V_ss = Vg * RL / (Rg + RL) if RL < 1e8 else Vg  # voltage divider

    # VSWR
    abs_GL = abs(Gamma_L)
    if abs_GL < 0.999:
        VSWR = (1 + abs_GL) / (1 - abs_GL)
    else:
        VSWR = float('inf')

    return {
        "Gamma_L": Gamma_L, "Gamma_g": Gamma_g,
        "V1_plus": V1_plus, "T": T,
        "V_at_3T": V_at_3T, "V_ss": V_ss,
        "VSWR": VSWR, "abs_GL": abs_GL,
    }


def gen_questionvariables(v, vals):
    Z0, Rg, RL, Vg = v["Z0"], v["Rg"], v["RL"], v["Vg"]

    # Handle special loads
    if RL < 1:
        rl_line = "RL_val: 0;  /* short circuit */"
        gl_line = "Gamma_L: -1;"
    elif RL > 1e8:
        rl_line = "RL_val: 1e12;  /* open circuit */"
        gl_line = "Gamma_L: 1;"
    else:
        rl_line = f"RL_val: {RL};"
        gl_line = "Gamma_L: (RL_val - Z0_val)/(RL_val + Z0_val);"

    # MCQ-MA options — topology-dependent
    if abs(vals["Gamma_g"]) < 0.01:
        # Matched source
        mcq_true = [1, 3]
        mcq_opts = [
            ("The steady-state voltage equals V_g * R_L / (R_g + R_L)", True),
            ("The line settles after exactly one round trip (because source is matched)", False),
            ("Increasing R_L toward Z_0 would reduce reflections at the load", True),
            ("VSWR = 1 means the line is perfectly matched at both ends", False),
            ("Doubling the line length doubles the number of bounces needed", False),
        ]
    else:
        mcq_true = [1, 4]
        mcq_opts = [
            ("The steady-state voltage equals V_g * R_L / (R_g + R_L)", True),
            ("Since both ends are mismatched, the voltage never settles", False),
            ("The reflection coefficient at the source is zero", False),
            ("Changing R_L to equal Z_0 would eliminate load reflections", True),
            ("The one-way travel time depends on the load impedance", False),
        ]

    opts_str = "[" + ", ".join(
        f'[{i}, {"true" if c else "false"}, "{t}"]' for i, (t, c) in enumerate(mcq_opts, 1)
    ) + "]"
    correct_set = "{" + ",".join(str(x) for x in mcq_true) + "}"

    return f"""/* {v['id']}: {v['name']} */
Z0_val: {Z0};
Rg_val: {Rg};
{rl_line}
Vg_val: {Vg};
ell_val: {v['length']};
vp_val: {v['vp']};

/* Reflection coefficients */
{gl_line}
Gamma_g: (Rg_val - Z0_val)/(Rg_val + Z0_val);

/* Initial forward wave */
V1_plus: Vg_val*Z0_val/(Z0_val + Rg_val);

/* One-way travel time */
T_val: ell_val/vp_val;

/* Voltage at load at t = 3T (after 1 round trip) */
V_at_3T: float(V1_plus*(1 + Gamma_L)*(1 + Gamma_L*Gamma_g));

/* VSWR */
VSWR_val: if abs(Gamma_L) < 0.999 then float((1 + abs(Gamma_L))/(1 - abs(Gamma_L))) else 999;

/* MCQ-MA */
mcq_opts: random_permutation({opts_str});
correct_mcq: {correct_set};

/* Teacher answers */
ta_GL: float(Gamma_L);
ta_Gg: float(Gamma_g);
ta_V1p: float(V1_plus);
ta_T: float(T_val);
ta_V3T: V_at_3T;
ta_mcq: correct_mcq;"""


def gen_questiontext(v, vals):
    T_ns = vals["T"] * 1e9

    return f"""<h3>Midterm 2 &ndash; Q4{v['id']}: TL Transient + Bounce Diagram ({v['name']})</h3>
<p><em>Electromagnetism and Circuit Analysis &mdash; LUT University, Finland</em></p>
<p><strong>Total: 10 points | Penalty per wrong attempt: 10%</strong></p>
<p><em>Inspired by Ulaby Ch.2 Example 2-8 and Problems 2.32&ndash;2.38.</em></p>
<hr />

<h4>Scenario</h4>
<p>{v['desc']}</p>
<p>[DIAGRAM: Transmission line system &mdash; source, line, load &mdash; to be added]</p>

<hr />

<h4>Part (a) &mdash; Reflection Coefficients and Initial Wave (2 points)</h4>
<p>Calculate the following:</p>
<p>Load reflection coefficient: \\(\\Gamma_L = \\) [[input:ans1]] &nbsp; [[validation:ans1]]</p>
<p><em>Enter a number between -1 and 1, e.g. <code>0.789</code> or <code>-0.5</code></em></p>

<p>Source reflection coefficient: \\(\\Gamma_g = \\) [[input:ans2]] &nbsp; [[validation:ans2]]</p>
<p><em>Enter a number, e.g. <code>0.333</code></em></p>

<p>Initial forward voltage wave: \\(V_1^+ = \\) [[input:ans3]] \\(\\text{{V}}\\) &nbsp; [[validation:ans3]]</p>
<p><em>Enter a number, e.g. <code>3.45</code></em></p>

<p>One-way travel time: \\(T = \\) [[input:ans4]] \\(\\text{{s}}\\) &nbsp; [[validation:ans4]]</p>
<p><em>Enter a number, e.g. <code>2.5e-9</code></em></p>

<h4>Part (b) &mdash; Voltage at Load After Reflections (2 points)</h4>
<p>Using the bounce diagram approach, calculate the voltage at the load at \\(t = 3T\\)
(after the first reflected wave returns and re-reflects from the source).</p>
<p>\\(V(\\ell,\\, 3T) = \\) [[input:ans5]] \\(\\text{{V}}\\) &nbsp; [[validation:ans5]]</p>
<p><em>Enter a number, e.g. <code>1.23</code></em></p>

<h4>Part (c) &mdash; TL Concepts (1 point)</h4>
<p><strong>Select ALL statements that are TRUE about this transmission line system:</strong></p>
<p>[[input:ans6]] &nbsp; [[validation:ans6]]</p>

<h4>Part (d) &mdash; Quarter-Wave Transformer Design (3 points, manually graded)</h4>
<p>A quarter-wave transformer (QWT) section is to be inserted between the line and load to eliminate reflections at the design frequency.</p>
<ol>
  <li>What characteristic impedance \\(Z_{{QWT}}\\) should this section have?</li>
  <li>What is the physical length of the QWT section at the design frequency \\(f\\)?</li>
  <li>If the operating frequency shifts by 10%, does the VSWR improve or worsen? Explain qualitatively.</li>
</ol>
<p>[[input:ans7]] &nbsp; [[validation:ans7]]</p>"""


def gen_generalfeedback(v, vals):
    return f"""<h4>Solution for {v['id']}</h4>
<p><strong>Part (a):</strong></p>
<p>\\(\\Gamma_L = {{@ta_GL@}}\\), \\(\\Gamma_g = {{@ta_Gg@}}\\),
\\(V_1^+ = {{@ta_V1p@}}\\;\\text{{V}}\\), \\(T = {{@ta_T@}}\\;\\text{{s}}\\)</p>
<p><strong>Part (b):</strong> \\(V(\\ell, 3T) = V_1^+(1+\\Gamma_L)(1+\\Gamma_L\\Gamma_g) = {{@ta_V3T@}}\\;\\text{{V}}\\)</p>
<p><strong>Part (c):</strong> Correct selections: {{@correct_mcq@}}</p>
<p><strong>Part (d):</strong> \\(Z_{{QWT}} = \\sqrt{{Z_0 \\cdot R_L}}\\). Length = \\(\\lambda/4\\) at design frequency. At 10% off, the QWT is no longer \\(\\lambda/4\\), so \\(\\Gamma \\neq 0\\) and VSWR worsens.</p>"""


def gen_inputs():
    return """    <input>
      <name>ans1</name>
      <type>numerical</type>
      <tans>ta_GL</tans>
      <boxsize>10</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>0.789</syntaxhint>
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
      <tans>ta_Gg</tans>
      <boxsize>10</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>0.789</syntaxhint>
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
      <tans>ta_V1p</tans>
      <boxsize>10</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>3.45</syntaxhint>
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
      <type>numerical</type>
      <tans>ta_T</tans>
      <boxsize>10</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>2.5e-9</syntaxhint>
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
      <type>numerical</type>
      <tans>ta_V3T</tans>
      <boxsize>10</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>1.23</syntaxhint>
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
      <name>ans6</name>
      <type>checkbox</type>
      <tans>ta_mcq</tans>
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
      <name>ans7</name>
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


PRT_GL = """    <prt>
      <name>prt_GL</name>
      <value>0.5000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumAbsolute</answertest>
        <sans>ans1</sans>
        <tans>ta_GL</tans>
        <testoptions>0.02</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_GL-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct \\(\\Gamma_L\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_GL-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(\\Gamma_L = \\frac{R_L - Z_0}{R_L + Z_0}\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_GG = """    <prt>
      <name>prt_Gg</name>
      <value>0.5000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumAbsolute</answertest>
        <sans>ans2</sans>
        <tans>ta_Gg</tans>
        <testoptions>0.02</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_Gg-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct \\(\\Gamma_g\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_Gg-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(\\Gamma_g = \\frac{R_g - Z_0}{R_g + Z_0}\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_V1P = """    <prt>
      <name>prt_V1p</name>
      <value>0.5000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans3</sans>
        <tans>ta_V1p</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_V1p-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct \\(V_1^+\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_V1p-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(V_1^+ = V_g \\frac{Z_0}{Z_0 + R_g}\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_T = """    <prt>
      <name>prt_T</name>
      <value>0.5000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans4</sans>
        <tans>ta_T</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_T-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct travel time.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_T-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(T = \\ell / v_p\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_V3T = """    <prt>
      <name>prt_V3T</name>
      <value>2.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans5</sans>
        <tans>ta_V3T</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_V3T-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct voltage at \\(t = 3T\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_V3T-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. Sum the forward and reflected waves using the bounce diagram.</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_MCQ = """    <prt>
      <name>prt_mcq</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>Sets</answertest>
        <sans>ans6</sans>
        <tans>ta_mcq</tans>
        <testoptions></testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_mcq-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>All correct statements identified.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_mcq-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Not all correct statements were identified.</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_variant(v):
    vals = compute_values(v)
    qvars = gen_questionvariables(v, vals)
    qtext = gen_questiontext(v, vals)
    gfb = gen_generalfeedback(v, vals)

    return f"""<question type="stack">
  <name><text>Midterm 2 - Q4{v['id']}: TL Transient + Bounce ({v['name']})</text></name>
  <questiontext format="html"><text><![CDATA[
{qtext}
]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[
{gfb}
]]></text></generalfeedback>
  <defaultgrade>10</defaultgrade>
  <penalty>0.1000000</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <stackversion><text>2024032401</text></stackversion>
  <questionvariables><text><![CDATA[
{qvars}
]]></text></questionvariables>
  <specificfeedback format="html"><text><![CDATA[
[[feedback:prt_GL]]
[[feedback:prt_Gg]]
[[feedback:prt_V1p]]
[[feedback:prt_T]]
[[feedback:prt_V3T]]
[[feedback:prt_mcq]]
]]></text></specificfeedback>
  <questionnote><text>{{@ta_GL@}}, {{@ta_Gg@}}, {{@ta_V1p@}}, {{@ta_V3T@}}</text></questionnote>
  <questiondescription format="html"><text></text></questiondescription>
  <prtcorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:green;"><i class="fa fa-check"></i></span> Correct!]]></text></prtcorrect>
  <prtpartiallycorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:orange;"><i class="fa fa-adjust"></i></span> Partially correct.]]></text></prtpartiallycorrect>
  <prtincorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:red;"><i class="fa fa-times"></i></span> Incorrect.]]></text></prtincorrect>
  <multiplicativetries>0</multiplicativetries>
{gen_inputs()}
{PRT_GL}
{PRT_GG}
{PRT_V1P}
{PRT_T}
{PRT_V3T}
{PRT_MCQ}
</question>"""


COMPANION = """<question type="essay">
  <name><text>Midterm 2 - Q4: Upload Handwritten Work (TL Transient)</text></name>
  <questiontext format="html"><text><![CDATA[
<h3>Upload Handwritten Work for Q4</h3>
<p>Upload work for Question 4 (TL Transient + Bounce Diagram).</p>
<h4>Include:</h4>
<ul>
  <li>Reflection coefficient calculations</li>
  <li>Bounce diagram with voltage labels at each bounce</li>
  <li>Summation work for V(l, 3T)</li>
  <li>QWT impedance calculation and frequency reasoning (Part d)</li>
</ul>
<p>Up to 2 files: PDF, JPG, JPEG, PNG. Worth 0 points.</p>
<p><strong>Teacher notice:</strong> Set Allow attachments to 2+ in quiz settings.</p>
]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Thank you.</p>]]></text></generalfeedback>
  <defaultgrade>0</defaultgrade><penalty>0</penalty><hidden>0</hidden>
  <responseformat>noinline</responseformat><responserequired>0</responserequired>
  <responsefieldlines>5</responsefieldlines>
  <attachments>2</attachments><attachmentsrequired>1</attachmentsrequired>
  <filetypeslist>.pdf,.jpg,.jpeg,.png</filetypeslist>
  <graderinfo format="html"><text><![CDATA[
<ul><li>Check bounce diagram completeness</li><li>Verify QWT design: Z_QWT = sqrt(Z0*RL)</li></ul>
]]></text></graderinfo>
  <responsetemplate format="html"><text></text></responsetemplate>
</question>"""


def main():
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>", ""]
    for v in VARIANTS:
        parts.extend([f"<!-- {'='*60} -->", f"<!-- Q4 {v['id']}: {v['name']} -->",
                       f"<!-- {'='*60} -->", gen_variant(v), ""])
    parts.extend([f"<!-- {'='*60} -->", "<!-- Companion Essay -->",
                   f"<!-- {'='*60} -->", COMPANION, "", "</quiz>"])
    xml = "\n".join(parts)

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base, "xml", "pool_q4_high.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"Generated {out_path}")
    print(f"  Lines: {xml.count(chr(10)) + 1}")
    print("\nVerification:")
    print(f"{'Var':<4} {'GL':>8} {'Gg':>8} {'V1+':>8} {'T(ns)':>8} {'V@3T':>10}")
    for v in VARIANTS:
        vals = compute_values(v)
        print(f"{v['id']:<4} {vals['Gamma_L']:>8.3f} {vals['Gamma_g']:>8.3f} "
              f"{vals['V1_plus']:>8.3f} {vals['T']*1e9:>8.1f} {vals['V_at_3T']:>10.4f}")

    # P-STACK-32
    hints = {"ans1": 0.789, "ans2": 0.789, "ans3": 3.45, "ans4": 2.5e-9, "ans5": 1.23}
    answers = {"ans1": [], "ans2": [], "ans3": [], "ans4": [], "ans5": []}
    for v in VARIANTS:
        vals = compute_values(v)
        answers["ans1"].append(vals["Gamma_L"])
        answers["ans2"].append(vals["Gamma_g"])
        answers["ans3"].append(vals["V1_plus"])
        answers["ans4"].append(vals["T"])
        answers["ans5"].append(vals["V_at_3T"])

    print("\nP-STACK-32:")
    ok = True
    for inp, h in hints.items():
        for i, a in enumerate(answers[inp], 1):
            if abs(a) < 0.001: continue  # skip zero/near-zero
            r = abs(h - a) / abs(a)
            if r < 0.15:
                print(f"  FAIL: {inp} hint={h} vs V{i} ans={a:.4g} ({r:.3f})")
                ok = False
    print("  ALL PASS" if ok else "  FAILURES")


if __name__ == "__main__":
    main()
