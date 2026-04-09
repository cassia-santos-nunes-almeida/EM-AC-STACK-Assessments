#!/usr/bin/env python
"""
Generate pool_q3_high.xml — Coupled Circuits + Transformer Design
Midterm 2, Q3 (High, 10 pts), 4 variants + companion essay

Parts: (a) Dot config MCQ 1pt, (b) M computation 2pt,
       (c) Stored energy 2pt, (d) MCQ-MA 1pt, (e) Essay 4pt
Textbook: Nilsson Ch.9 Problems 9.6-9.24
"""

import math
import os

VARIANTS = [
    {
        "id": "V1", "name": "E-core, Aiding Dots, Resistive Load",
        "dot_type": "aiding",
        "L1": 0.05, "L2": 0.02, "k": 0.6,
        "i1": 3, "i2": 2,
        "L1_display": "50\\;\\text{mH}", "L2_display": "20\\;\\text{mH}",
        "i1_display": "3\\;\\text{A}", "i2_display": "2\\;\\text{A}",
        "winding_desc": (
            "Both coils are wound in the <strong>same sense</strong> (clockwise when viewed from the top). "
            "Current \\(i_1\\) enters the top terminal of Coil 1, and \\(i_2\\) enters the top terminal of Coil 2."
        ),
        "dot_correct": 1,  # index of correct option
        "dot_options": [
            ("Dots on top terminals of both coils (same-sense winding)", True),
            ("Dot on top of Coil 1, dot on bottom of Coil 2", False),
            ("Dots on bottom terminals of both coils", False),
            ("Dot on bottom of Coil 1, dot on top of Coil 2", False),
        ],
        "mcq_ma_errors": [1, 3],
        "mcq_ma_options": [
            ("Increase the coupling coefficient k", True),
            ("Reverse the direction of i_2", False),
            ("Increase L_1", True),
            ("Decrease both i_1 and i_2 by half", False),
            ("Replace aiding dots with opposing dots", False),
        ],
    },
    {
        "id": "V2", "name": "Toroid, Opposing Dots, RL Load",
        "dot_type": "opposing",
        "L1": 0.04, "L2": 0.01, "k": 0.5,
        "i1": 4, "i2": 3,
        "L1_display": "40\\;\\text{mH}", "L2_display": "10\\;\\text{mH}",
        "i1_display": "4\\;\\text{A}", "i2_display": "3\\;\\text{A}",
        "winding_desc": (
            "The coils are wound in <strong>opposite senses</strong> on a toroidal core. "
            "Current \\(i_1\\) enters the dotted terminal of Coil 1, but \\(i_2\\) enters the "
            "<strong>undotted</strong> terminal of Coil 2."
        ),
        "dot_correct": 2,
        "dot_options": [
            ("Dots on top terminals of both coils", False),
            ("Dot on top of Coil 1, dot on bottom of Coil 2 (opposite sense)", True),
            ("Dots on bottom terminals of both coils", False),
            ("Dot on bottom of Coil 1, dot on top of Coil 2", False),
        ],
        "mcq_ma_errors": [2, 4],
        "mcq_ma_options": [
            ("Increase the coupling coefficient k", False),
            ("Increase i_1", True),
            ("Decrease L_2", False),
            ("Increase L_1", True),
            ("Reverse the direction of i_2 (makes both enter dotted terminals)", False),
        ],
    },
    {
        "id": "V3", "name": "C-core, Aiding Dots, Symmetric",
        "dot_type": "aiding",
        "L1": 0.03, "L2": 0.03, "k": 0.7,
        "i1": 2, "i2": 2,
        "L1_display": "30\\;\\text{mH}", "L2_display": "30\\;\\text{mH}",
        "i1_display": "2\\;\\text{A}", "i2_display": "2\\;\\text{A}",
        "winding_desc": (
            "Both coils have the <strong>same number of turns</strong> and are wound in the "
            "<strong>same direction</strong> on a C-core. Both currents enter their dotted terminals."
        ),
        "dot_correct": 1,
        "dot_options": [
            ("Dots on left terminals of both coils (same winding direction)", True),
            ("Dot on left of Coil 1, dot on right of Coil 2", False),
            ("Dots on right terminals of both coils", False),
            ("No dots needed since L_1 = L_2", False),
        ],
        "mcq_ma_errors": [1, 2],
        "mcq_ma_options": [
            ("Increase k toward 1.0 (tighter coupling)", True),
            ("Increase both i_1 and i_2 equally", True),
            ("Reduce L_1 while keeping L_2 the same", False),
            ("Switch from aiding to opposing dot convention", False),
            ("Decrease the frequency of the source", False),
        ],
    },
    {
        "id": "V4", "name": "Rectangular Core, Opposing Dots, Tight Coupling",
        "dot_type": "opposing",
        "L1": 0.06, "L2": 0.015, "k": 0.45,
        "i1": 2, "i2": 5,
        "L1_display": "60\\;\\text{mH}", "L2_display": "15\\;\\text{mH}",
        "i1_display": "2\\;\\text{A}", "i2_display": "5\\;\\text{A}",
        "winding_desc": (
            "The coils are wound in <strong>opposite directions</strong> on a rectangular core. "
            "Current \\(i_1\\) enters the dotted terminal of Coil 1. "
            "Current \\(i_2\\) enters the <strong>undotted</strong> terminal of Coil 2."
        ),
        "dot_correct": 2,
        "dot_options": [
            ("Dots on the same side of both coils", False),
            ("Dot on top of Coil 1, dot on bottom of Coil 2 (opposite winding)", True),
            ("No dots are needed for this configuration", False),
            ("Dots on opposite sides, but reversed from option B", False),
        ],
        "mcq_ma_errors": [2, 3],
        "mcq_ma_options": [
            ("Decrease k", False),
            ("Increase i_2", True),
            ("Increase L_2", True),
            ("Reverse i_1 direction (makes mutual term positive)", False),
            ("Replace opposing dots with aiding dots", False),
        ],
    },
]


def compute_values(v):
    M = v["k"] * math.sqrt(v["L1"] * v["L2"])
    i1, i2 = v["i1"], v["i2"]

    if v["dot_type"] == "aiding":
        W = 0.5 * v["L1"] * i1**2 + 0.5 * v["L2"] * i2**2 + M * i1 * i2
        sign_text = "+"
    else:
        W = 0.5 * v["L1"] * i1**2 + 0.5 * v["L2"] * i2**2 - M * i1 * i2
        sign_text = "-"

    # T-equivalent elements
    if v["dot_type"] == "aiding":
        La = v["L1"] - M
        Lb = v["L2"] - M
        Lc = M
    else:
        La = v["L1"] + M
        Lb = v["L2"] + M
        Lc = -M

    # Turns ratio estimate
    a = math.sqrt(v["L1"] / v["L2"])

    # Error values
    W_wrong_sign = 0.5 * v["L1"] * i1**2 + 0.5 * v["L2"] * i2**2 + (-1 if v["dot_type"] == "aiding" else 1) * M * i1 * i2
    W_forgot_M = 0.5 * v["L1"] * i1**2 + 0.5 * v["L2"] * i2**2

    return {
        "M": M, "W": W, "La": La, "Lb": Lb, "Lc": Lc, "a": a,
        "sign_text": sign_text, "W_wrong_sign": W_wrong_sign, "W_forgot_M": W_forgot_M,
    }


def gen_questionvariables(v, vals):
    sign_maxima = "+" if v["dot_type"] == "aiding" else "-"

    dot_opts = []
    for i, (text, correct) in enumerate(v["dot_options"], 1):
        bval = "true" if correct else "false"
        dot_opts.append(f'[{i}, {bval}, "{text}"]')

    mcq_opts = []
    for i, (text, correct) in enumerate(v["mcq_ma_options"], 1):
        bval = "true" if correct else "false"
        mcq_opts.append(f'[{i}, {bval}, "{text}"]')

    correct_mcq_set = "{" + ",".join(str(x) for x in v["mcq_ma_errors"]) + "}"

    return f"""/* {v['id']}: {v['name']} */
L1_val: {v['L1']};
L2_val: {v['L2']};
k_val: {v['k']};
i1_val: {v['i1']};
i2_val: {v['i2']};

/* Mutual inductance */
M_val: k_val*sqrt(L1_val*L2_val);

/* Stored energy: W = 1/2*L1*i1^2 + 1/2*L2*i2^2 {sign_maxima} M*i1*i2 */
W_val: 1/2*L1_val*i1_val^2 + 1/2*L2_val*i2_val^2 {sign_maxima} M_val*i1_val*i2_val;

/* Error values */
W_wrong_sign: 1/2*L1_val*i1_val^2 + 1/2*L2_val*i2_val^2 {"- " if v["dot_type"] == "aiding" else "+ "}M_val*i1_val*i2_val;
W_forgot_M: 1/2*L1_val*i1_val^2 + 1/2*L2_val*i2_val^2;

/* T-equivalent elements */
La_val: L1_val {"- " if v["dot_type"] == "aiding" else "+ "}M_val;
Lb_val: L2_val {"- " if v["dot_type"] == "aiding" else "+ "}M_val;

/* Turns ratio estimate */
a_val: sqrt(L1_val/L2_val);

/* Numerical versions */
M_num: float(M_val);
W_num: float(W_val);

/* Part (a) dot config MCQ */
dot_opts: random_permutation([{", ".join(dot_opts)}]);

/* Part (d) MCQ-MA */
mcq_opts: random_permutation([{", ".join(mcq_opts)}]);
correct_mcq: {correct_mcq_set};

/* Teacher answers */
ta_dot: dot_opts;
ta_M: float(M_val);
ta_W: float(W_val);
ta_mcq: correct_mcq;"""


def gen_questiontext(v, vals):
    sign_sym = "+" if v["dot_type"] == "aiding" else "-"
    dot_desc = "aiding (both currents enter dotted terminals)" if v["dot_type"] == "aiding" else "opposing (one current enters undotted terminal)"

    return f"""<h3>Midterm 2 &ndash; Q3{v['id']}: Coupled Circuits + Transformer Design ({v['name']})</h3>
<p><em>Electromagnetism and Circuit Analysis &mdash; LUT University, Finland</em></p>
<p><strong>Total: 10 points | Penalty per wrong attempt: 10%</strong></p>
<p><em>Inspired by Nilsson &amp; Riedel Ch.9 Problems 9.6&ndash;9.24.</em></p>
<hr />

<h4>Scenario</h4>
<p>Two magnetically coupled coils have self-inductances \\(L_1 = {v['L1_display']}\\) and
\\(L_2 = {v['L2_display']}\\), with coupling coefficient \\(k = {{@k_val@}}\\).</p>

<p>{v['winding_desc']}</p>

<p>[DIAGRAM: Physical winding diagram for {v['name']} &mdash; to be added]</p>

<p>The coils carry DC currents \\(i_1 = {v['i1_display']}\\) and \\(i_2 = {v['i2_display']}\\).</p>

<hr />

<h4>Part (a) &mdash; Dot Configuration (1 point)</h4>
<p>Based on the winding description above, select the correct dot placement:</p>
<p>[[input:ans1]] &nbsp; [[validation:ans1]]</p>
<p><em>(This part will be upgraded to drag-and-drop when diagrams are available.)</em></p>

<h4>Part (b) &mdash; Mutual Inductance (2 points)</h4>
<p>Calculate the mutual inductance \\(M\\).</p>
<p>\\(M = \\) [[input:ans2]] \\(\\text{{H}}\\) &nbsp; [[validation:ans2]]</p>
<p><em>Enter a number, e.g. <code>0.0456</code></em></p>

<h4>Part (c) &mdash; Stored Energy (2 points)</h4>
<p>Calculate the total magnetic energy stored in the coupled system.</p>
<p>Recall: \\(W = \\frac{{1}}{{2}}L_1 i_1^2 + \\frac{{1}}{{2}}L_2 i_2^2 \\pm M i_1 i_2\\)</p>
<p>The sign of the mutual term depends on the dot convention and current directions.</p>
<p>\\(W = \\) [[input:ans3]] \\(\\text{{J}}\\) &nbsp; [[validation:ans3]]</p>
<p><em>Enter a number, e.g. <code>0.567</code></em></p>

<h4>Part (d) &mdash; Energy Optimization (1 point)</h4>
<p><strong>Select ALL changes that would increase the total stored energy:</strong></p>
<p>[[input:ans4]] &nbsp; [[validation:ans4]]</p>

<h4>Part (e) &mdash; Ideal Transformer Comparison (4 points, manually graded)</h4>
<p>An engineer proposes modeling these coupled coils as an <strong>ideal transformer</strong> with
turns ratio \\(a = \\sqrt{{L_1/L_2}} = {{@float(a_val)@}}\\).</p>
<ol>
  <li>Under what conditions is the ideal transformer approximation valid?</li>
  <li>What physical effects are lost in the ideal transformer model?</li>
  <li>For the given currents, what is the relationship between \\(i_1\\) and \\(i_2\\)
      under the ideal transformer assumption? Does this match the given values?</li>
</ol>
<p>[[input:ans5]] &nbsp; [[validation:ans5]]</p>"""


def gen_generalfeedback(v, vals):
    sign_sym = "+" if v["dot_type"] == "aiding" else "-"
    return f"""<h4>Solution for {v['id']} ({v['name']})</h4>
<p><strong>Part (a):</strong> The dot configuration is {v['dot_type']}.</p>
<p><strong>Part (b):</strong> \\(M = k\\sqrt{{L_1 L_2}} = {{@M_num@}}\\;\\text{{H}}\\)</p>
<p><strong>Part (c):</strong></p>
<p>\\(W = \\frac{{1}}{{2}}L_1 i_1^2 + \\frac{{1}}{{2}}L_2 i_2^2 {sign_sym} M i_1 i_2 = {{@W_num@}}\\;\\text{{J}}\\)</p>
<p>The sign is <strong>{sign_sym}</strong> because the dot configuration is <strong>{v['dot_type']}</strong>.</p>
<p><strong>Part (d):</strong> The correct selections are {{@correct_mcq@}}.</p>
<p><strong>Part (e):</strong></p>
<ul>
  <li>The ideal transformer requires \\(k \\to 1\\) (perfect coupling) and infinite inductances with finite ratio</li>
  <li>Lost effects: leakage flux, core losses, winding resistance, finite inductance (DC magnetization)</li>
  <li>Ideal transformer: \\(i_1/i_2 = 1/a = {{@float(1/a_val)@}}\\). The given currents \\(i_1 = {v['i1']}\\) A and \\(i_2 = {v['i2']}\\) A may not satisfy this ratio, showing the coils are not ideal.</li>
</ul>"""


def gen_inputs():
    return """    <input>
      <name>ans1</name>
      <type>dropdown</type>
      <tans>ta_dot</tans>
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
      <name>ans2</name>
      <type>numerical</type>
      <tans>ta_M</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>0.0456</syntaxhint>
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
      <tans>ta_W</tans>
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


PRT_DOT = """    <prt>
      <name>prt_dot</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>AlgEquiv</answertest>
        <sans>ans1</sans>
        <tans>1</tans>
        <testoptions></testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_dot-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct dot placement.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_dot-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. The dot marks the terminal where current entering produces flux in the reference direction. Check the winding sense.</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_M = """    <prt>
      <name>prt_M</name>
      <value>2.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans2</sans>
        <tans>ta_M</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_M-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct mutual inductance.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_M-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(M = k\\sqrt{L_1 L_2}\\).</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_W = """    <prt>
      <name>prt_W</name>
      <value>2.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans3</sans>
        <tans>ta_W</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_W-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct stored energy.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>1</falsenextnode>
        <falseanswernote>prt_W-1-F</falseanswernote>
        <falsefeedback format="html"><text></text></falsefeedback>
      </node>
      <node>
        <name>1</name>
        <answertest>NumRelative</answertest>
        <sans>ans3</sans>
        <tans>float(W_wrong_sign)</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>0.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_W-2-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Wrong sign on the mutual term! Check whether the configuration is aiding or opposing. Aiding: +M, Opposing: -M.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>2</falsenextnode>
        <falseanswernote>prt_W-2-F</falseanswernote>
        <falsefeedback format="html"><text></text></falsefeedback>
      </node>
      <node>
        <name>2</name>
        <answertest>NumRelative</answertest>
        <sans>ans3</sans>
        <tans>float(W_forgot_M)</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>0.3000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_W-3-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>You computed only the self-energy terms and forgot the mutual energy term \\(\\pm M i_1 i_2\\).</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_W-3-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. \\(W = \\frac{1}{2}L_1 i_1^2 + \\frac{1}{2}L_2 i_2^2 \\pm M i_1 i_2\\).</p>]]></text></falsefeedback>
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
        <sans>ans4</sans>
        <tans>ta_mcq</tans>
        <testoptions></testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_mcq-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct! All energy-increasing changes identified.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_mcq-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Not all correct changes identified. Consider how each parameter affects the energy formula.</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_variant(v):
    vals = compute_values(v)
    qvars = gen_questionvariables(v, vals)
    qtext = gen_questiontext(v, vals)
    gfb = gen_generalfeedback(v, vals)

    return f"""<question type="stack">
  <name>
    <text>Midterm 2 - Q3{v['id']}: Coupled Circuits + Transformer ({v['name']})</text>
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
  <defaultgrade>10</defaultgrade>
  <penalty>0.1000000</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <stackversion><text>2024032401</text></stackversion>
  <questionvariables>
    <text><![CDATA[
{qvars}
]]></text>
  </questionvariables>
  <specificfeedback format="html">
    <text><![CDATA[
[[feedback:prt_dot]]
[[feedback:prt_M]]
[[feedback:prt_W]]
[[feedback:prt_mcq]]
]]></text>
  </specificfeedback>
  <questionnote><text>{{@M_num@}}, {{@W_num@}}, {{@correct_mcq@}}</text></questionnote>
  <questiondescription format="html"><text></text></questiondescription>
  <prtcorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:green;"><i class="fa fa-check"></i></span> Correct answer, well done!]]></text></prtcorrect>
  <prtpartiallycorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:orange;"><i class="fa fa-adjust"></i></span> Your answer is partially correct.]]></text></prtpartiallycorrect>
  <prtincorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:red;"><i class="fa fa-times"></i></span> Incorrect answer.]]></text></prtincorrect>
  <multiplicativetries>0</multiplicativetries>
{gen_inputs()}
{PRT_DOT}
{PRT_M}
{PRT_W}
{PRT_MCQ}
</question>"""


COMPANION = """<question type="essay">
  <name><text>Midterm 2 - Q3: Upload Handwritten Work (Coupled Circuits)</text></name>
  <questiontext format="html">
    <text><![CDATA[
<h3>Upload Your Handwritten Work for Q3</h3>
<p>Upload handwritten work for Question 3 (Coupled Circuits + Transformer Design).</p>
<h4>Include:</h4>
<ul>
  <li><strong>Part (a):</strong> Winding analysis and dot reasoning</li>
  <li><strong>Part (b):</strong> M calculation</li>
  <li><strong>Part (c):</strong> Energy calculation with sign reasoning</li>
  <li><strong>Part (e):</strong> Ideal transformer comparison and analysis</li>
</ul>
<h4>Instructions:</h4>
<ol>
  <li>Name and student ID on every page</li>
  <li>Dark pen on white paper</li>
  <li>Up to 2 files: PDF, JPG, JPEG, PNG</li>
</ol>
<p><em>Worth 0 points. Supports grading verification.</em></p>
<p><strong>Teacher notice:</strong> Set &ldquo;Allow attachments&rdquo; to 2+ in quiz settings.</p>
]]></text>
  </questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Thank you for uploading.</p>]]></text></generalfeedback>
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
<h4>Instructor Notes</h4>
<ul>
  <li>Check dot reasoning from winding description</li>
  <li>Verify correct sign in energy formula (most common error)</li>
  <li>For Part (e): look for k&rarr;1 condition, mention of leakage flux, finite inductance</li>
</ul>
]]></text>
  </graderinfo>
  <responsetemplate format="html"><text></text></responsetemplate>
</question>"""


def main():
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>", ""]
    for v in VARIANTS:
        parts.append(f"<!-- {'='*60} -->")
        parts.append(f"<!-- Q3 {v['id']}: {v['name']} -->")
        parts.append(f"<!-- {'='*60} -->")
        parts.append(gen_variant(v))
        parts.append("")
    parts.extend([f"<!-- {'='*60} -->", "<!-- Companion Essay -->", f"<!-- {'='*60} -->", COMPANION, "", "</quiz>"])
    xml = "\n".join(parts)

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base, "xml", "pool_q3_high.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"Generated {out_path}")
    print(f"  Lines: {xml.count(chr(10)) + 1}")
    print("\nVerification:")
    print(f"{'Var':<4} {'Dots':<10} {'M(H)':>10} {'W(J)':>10} {'W_wrong':>10} {'MCQ errs'}")
    for v in VARIANTS:
        vals = compute_values(v)
        print(f"{v['id']:<4} {v['dot_type']:<10} {vals['M']:>10.5f} {vals['W']:>10.5f} {vals['W_wrong_sign']:>10.5f} {v['mcq_ma_errors']}")

    # P-STACK-32
    hints = {"ans2": 0.0456, "ans3": 0.567}
    answers = {"ans2": [], "ans3": []}
    for v in VARIANTS:
        vals = compute_values(v)
        answers["ans2"].append(vals["M"])
        answers["ans3"].append(vals["W"])
    print("\nP-STACK-32:")
    ok = True
    for inp, h in hints.items():
        for i, a in enumerate(answers[inp], 1):
            if a == 0: continue
            r = abs(h - a) / abs(a)
            if r < 0.15: print(f"  FAIL: {inp} hint={h} vs V{i} ans={a:.5f} ({r:.3f})"); ok = False
    print("  ALL PASS" if ok else "  FAILURES")


if __name__ == "__main__":
    main()
