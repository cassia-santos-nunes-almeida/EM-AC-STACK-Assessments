#!/usr/bin/env python
"""
Generate pool_q5_high.xml — EM Wave Propagation + Wireless Link Budget
Midterm 2, Q5 (High, 12 pts), 4 variants + companion essay

Parts: (a) Media classify 1pt, (b) Attenuation 2pt, (c) FSPL 1pt,
       (d) Link budget 1pt, (e) MCQ-MA 2pt, (f) Essay trade-off 5pt
Textbook: Ulaby Ch.7 Ex 7-5, Ch.9 Ex 9-4, Prob 9.25
"""

import math
import os

MU0 = 4 * math.pi * 1e-7
EPS0 = 8.854e-12
C0 = 3e8

VARIANTS = [
    {
        "id": "V1",
        "name": "Ground-Penetrating Radar (GPR) through soil",
        "scenario": (
            "A ground-penetrating radar (GPR) system operates at \\(f = 100\\;\\text{MHz}\\). "
            "The radar signal must penetrate \\(d = 2\\;\\text{m}\\) of moist soil "
            "(\\(\\sigma = 0.01\\;\\text{S/m}\\), \\(\\varepsilon_r = 10\\), \\(\\mu_r = 1\\)) "
            "before reflecting off a buried pipe. After emerging from the soil, the return signal "
            "travels \\(R = 5\\;\\text{m}\\) through free space to the receiver."
        ),
        "f": 100e6, "d": 2, "R": 5,
        "sigma": 0.01, "eps_r": 10, "mu_r": 1,
        "Pt_dBm": 30, "Gt_dBi": 10, "Gr_dBi": 10,
        "mcq_true": [1, 3],
        "mcq_opts": [
            ("Double the transmit power (+3 dB)", True),
            ("Move to 1 GHz for better resolution (increases both alpha and FSPL)", False),
            ("Use a higher-gain antenna (+3 dBi each gives +6 dB total)", True),
            ("Reduce material thickness by half (may not be possible for GPR)", False),
            ("Switch to a lower frequency (reduces alpha but increases antenna size)", False),
        ],
    },
    {
        "id": "V2",
        "name": "Through-wall Wi-Fi communication",
        "scenario": (
            "A 5 GHz Wi-Fi access point transmits through a concrete wall "
            "(\\(\\sigma = 0.05\\;\\text{S/m}\\), \\(\\varepsilon_r = 6\\), \\(\\mu_r = 1\\), "
            "thickness \\(d = 0.3\\;\\text{m}\\)) to a laptop \\(R = 10\\;\\text{m}\\) away "
            "(measured from the wall exit to the laptop)."
        ),
        "f": 5e9, "d": 0.3, "R": 10,
        "sigma": 0.05, "eps_r": 6, "mu_r": 1,
        "Pt_dBm": 20, "Gt_dBi": 3, "Gr_dBi": 0,
        "mcq_true": [1, 4],
        "mcq_opts": [
            ("Double the transmit power (+3 dB)", True),
            ("Move to 60 GHz for more bandwidth (dramatically increases FSPL and alpha)", False),
            ("Use a thinner wall material (may not be feasible)", False),
            ("Halve the free-space distance (reduces FSPL by 6 dB)", True),
            ("Switch to 2.4 GHz (lower FSPL but also lower bandwidth)", False),
        ],
    },
    {
        "id": "V3",
        "name": "Agricultural IoT sensor through wet earth",
        "scenario": (
            "An agricultural IoT sensor buried at depth \\(d = 0.5\\;\\text{m}\\) in moist soil "
            "(\\(\\sigma = 0.02\\;\\text{S/m}\\), \\(\\varepsilon_r = 15\\), \\(\\mu_r = 1\\)) "
            "transmits at \\(f = 433\\;\\text{MHz}\\) (ISM band). After emerging from the soil, "
            "the signal travels \\(R = 300\\;\\text{m}\\) through free space to a gateway receiver."
        ),
        "f": 433e6, "d": 0.5, "R": 300,
        "sigma": 0.02, "eps_r": 15, "mu_r": 1,
        "Pt_dBm": 20, "Gt_dBi": 0, "Gr_dBi": 6,
        "mcq_true": [1, 4],
        "mcq_opts": [
            ("Increase transmit power by 6 dB (quadruple power)", True),
            ("Move to 2.4 GHz for more bandwidth (increases both alpha and FSPL)", False),
            ("Bury the sensor deeper for better protection (increases attenuation)", False),
            ("Use a higher-gain receive antenna (+6 dBi)", True),
            ("Switch to a wired connection (defeats the purpose of wireless IoT)", False),
        ],
    },
    {
        "id": "V4",
        "name": "Satellite-to-indoor receiver through roof",
        "scenario": (
            "A satellite downlink at \\(f = 12\\;\\text{GHz}\\) passes through a building roof "
            "(reinforced concrete: \\(\\sigma = 0.1\\;\\text{S/m}\\), \\(\\varepsilon_r = 7\\), "
            "\\(\\mu_r = 1\\), thickness \\(d = 0.2\\;\\text{m}\\)). "
            "The satellite is \\(R = 500\\;\\text{m}\\) slant range from the building."
        ),
        "f": 12e9, "d": 0.2, "R": 500,
        "sigma": 0.1, "eps_r": 7, "mu_r": 1,
        "Pt_dBm": 33, "Gt_dBi": 30, "Gr_dBi": 0,
        "mcq_true": [1, 5],
        "mcq_opts": [
            ("Increase satellite transmit power", True),
            ("Move to 60 GHz (more bandwidth but far worse FSPL and penetration)", False),
            ("Remove the roof (not practical!)", False),
            ("Use a thinner roof material (structural constraint)", False),
            ("Place an external antenna on the roof and run cable inside", True),
        ],
    },
]


def compute_values(v):
    f = v["f"]
    omega = 2 * math.pi * f
    sigma = v["sigma"]
    eps_r = v["eps_r"]
    mu_r = v["mu_r"]
    eps = eps_r * EPS0
    mu = mu_r * MU0
    d = v["d"]
    R = v["R"]

    # Loss tangent
    loss_tangent = sigma / (omega * eps)

    # Media classification
    if loss_tangent > 100:
        classification = "Good conductor"
        class_idx = 1
    elif loss_tangent < 0.01:
        classification = "Low-loss dielectric"
        class_idx = 2
    else:
        classification = "Quasi-conductor (lossy dielectric)"
        class_idx = 3

    # Attenuation constant (general formula)
    # alpha = omega * sqrt(mu*eps/2) * sqrt(sqrt(1 + (sigma/(omega*eps))^2) - 1)
    inner = math.sqrt(1 + (sigma / (omega * eps))**2)
    alpha = omega * math.sqrt(mu * eps / 2) * math.sqrt(inner - 1)

    # Power attenuation through material (dB)
    # Power attenuation = e^(-2*alpha*d), in dB = 8.686 * alpha * d
    atten_dB = 8.686 * alpha * d

    # FSPL (dB) for free-space path
    wavelength = C0 / f
    FSPL_dB = 20 * math.log10(4 * math.pi * R / wavelength)

    # Link budget
    Pt = v["Pt_dBm"]
    Gt = v["Gt_dBi"]
    Gr = v["Gr_dBi"]
    Pr_dBm = Pt + Gt + Gr - FSPL_dB - atten_dB

    return {
        "loss_tangent": loss_tangent, "classification": classification,
        "class_idx": class_idx, "alpha": alpha, "atten_dB": atten_dB,
        "FSPL_dB": FSPL_dB, "Pr_dBm": Pr_dBm, "wavelength": wavelength,
    }


def gen_questionvariables(v, vals):
    # MCQ options
    opts = []
    for i, (text, correct) in enumerate(v["mcq_opts"], 1):
        bval = "true" if correct else "false"
        opts.append(f'[{i}, {bval}, "{text}"]')
    correct_set = "{" + ",".join(str(x) for x in v["mcq_true"]) + "}"

    # Classification MCQ options
    class_opts = {1: "Good conductor", 2: "Low-loss dielectric", 3: "Quasi-conductor"}
    correct_class = vals["class_idx"]

    class_opt_list = []
    for idx, label in class_opts.items():
        bval = "true" if idx == correct_class else "false"
        class_opt_list.append(f'[{idx}, {bval}, "{label}"]')

    return f"""/* {v['id']}: {v['name']} */
f_val: {v['f']};
omega_val: 2*%pi*f_val;
sigma_val: {v['sigma']};
epsr_val: {v['eps_r']};
mur_val: {v['mu_r']};
d_val: {v['d']};
R_val: {v['R']};
Pt_dBm: {v['Pt_dBm']};
Gt_dBi: {v['Gt_dBi']};
Gr_dBi: {v['Gr_dBi']};

/* Derived */
eps0: 8.854/10^12;
mu0: 4*%pi/10^7;
eps_val: epsr_val*eps0;
mu_val: mur_val*mu0;

/* Loss tangent */
loss_tangent: sigma_val/(omega_val*eps_val);

/* Classification */
class_opts: random_permutation([{", ".join(class_opt_list)}]);

/* Attenuation constant (general formula) */
alpha_val: omega_val*sqrt(mu_val*eps_val/2)*sqrt(sqrt(1 + (sigma_val/(omega_val*eps_val))^2) - 1);

/* Power attenuation through material */
atten_dB: float(8.686*alpha_val*d_val);

/* FSPL */
lambda_val: 3*10^8/f_val;
FSPL_dB: float(20*log(4*%pi*R_val/lambda_val)/log(10));

/* Link budget */
Pr_dBm: float(Pt_dBm + Gt_dBi + Gr_dBi - FSPL_dB - atten_dB);

/* MCQ-MA */
mcq_opts: random_permutation([{", ".join(opts)}]);
correct_mcq: {correct_set};

/* Teacher answers */
ta_class: class_opts;
ta_alpha: float(alpha_val);
ta_atten: float(atten_dB);
ta_FSPL: float(FSPL_dB);
ta_Pr: float(Pr_dBm);
ta_mcq: correct_mcq;"""


def gen_questiontext(v, vals):
    return f"""<h3>Midterm 2 &ndash; Q5{v['id']}: EM Wave Propagation + Link Budget ({v['name']})</h3>
<p><em>Electromagnetism and Circuit Analysis &mdash; LUT University, Finland</em></p>
<p><strong>Total: 12 points | Penalty per wrong attempt: 10%</strong></p>
<p><em>Inspired by Ulaby Ch.7 Example 7-5, Ch.9 Example 9-4, Problem 9.25.</em></p>
<hr />

<h4>Scenario</h4>
<p>{v['scenario']}</p>
<p>[DIAGRAM: Multi-segment signal path for {v['name']} &mdash; to be added]</p>

<h4>System Parameters</h4>
<ul>
  <li>Transmit power: \\(P_t = {{@Pt_dBm@}}\\;\\text{{dBm}}\\)</li>
  <li>Transmit antenna gain: \\(G_t = {{@Gt_dBi@}}\\;\\text{{dBi}}\\)</li>
  <li>Receive antenna gain: \\(G_r = {{@Gr_dBi@}}\\;\\text{{dBi}}\\)</li>
</ul>

<hr />

<h4>Part (a) &mdash; Media Classification (1 point)</h4>
<p>Compute the loss tangent \\(\\tan\\delta = \\sigma/(\\omega\\varepsilon)\\) and classify the material:</p>
<p>[[input:ans1]] &nbsp; [[validation:ans1]]</p>

<h4>Part (b) &mdash; Material Attenuation (2 points)</h4>
<p>Calculate the attenuation constant \\(\\alpha\\) (Np/m) and the total power attenuation (in dB) through the material layer.</p>
<p>\\(\\alpha = \\) [[input:ans2]] \\(\\text{{Np/m}}\\) &nbsp; [[validation:ans2]]</p>
<p><em>Enter a number, e.g. <code>12.3</code></em></p>
<p>Power attenuation = \\(8.686 \\times \\alpha \\times d = \\) [[input:ans3]] \\(\\text{{dB}}\\) &nbsp; [[validation:ans3]]</p>
<p><em>Enter a number, e.g. <code>45.6</code></em></p>

<h4>Part (c) &mdash; Free-Space Path Loss (1 point)</h4>
<p>Calculate the free-space path loss (FSPL) in dB for the air path.</p>
<p>\\(\\text{{FSPL}} = 20\\log_{{10}}\\left(\\frac{{4\\pi R}}{{\\lambda}}\\right) = \\) [[input:ans4]] \\(\\text{{dB}}\\) &nbsp; [[validation:ans4]]</p>
<p><em>Enter a number, e.g. <code>45.6</code></em></p>

<h4>Part (d) &mdash; Link Budget (1 point)</h4>
<p>Calculate the received power \\(P_r\\) in dBm:</p>
<p>\\(P_r = P_t + G_t + G_r - \\text{{FSPL}} - \\text{{Material attenuation}} = \\) [[input:ans5]] \\(\\text{{dBm}}\\) &nbsp; [[validation:ans5]]</p>
<p><em>Enter a number, e.g. <code>-23.4</code></em></p>

<h4>Part (e) &mdash; System Improvement (2 points)</h4>
<p>The received power is insufficient. <strong>To improve the signal by at least 6 dB</strong>, select ALL changes that would achieve this:</p>
<p>[[input:ans6]] &nbsp; [[validation:ans6]]</p>

<h4>Part (f) &mdash; Frequency Trade-off Analysis (5 points, manually graded)</h4>
<p>A colleague suggests moving to a frequency <strong>10 times higher</strong> to get more bandwidth.</p>
<p>Analyze the trade-offs:</p>
<ol>
  <li>How would this affect the material attenuation \\(\\alpha\\)?</li>
  <li>How would this affect the free-space path loss?</li>
  <li>How would this affect the antenna size?</li>
  <li>What is the net effect on the total link margin?</li>
  <li>Would you recommend the frequency change? Justify your answer.</li>
</ol>
<p>[[input:ans7]] &nbsp; [[validation:ans7]]</p>"""


def gen_generalfeedback(v, vals):
    return f"""<h4>Solution for {v['id']}</h4>
<p><strong>Part (a):</strong> Loss tangent = {{@float(loss_tangent)@}}. Classification: <strong>{vals['classification']}</strong>.</p>
<p><strong>Part (b):</strong> \\(\\alpha = {{@ta_alpha@}}\\;\\text{{Np/m}}\\), Attenuation = {{@ta_atten@}} dB.</p>
<p><strong>Part (c):</strong> FSPL = {{@ta_FSPL@}} dB.</p>
<p><strong>Part (d):</strong> \\(P_r = {{@ta_Pr@}}\\;\\text{{dBm}}\\).</p>
<p><strong>Part (e):</strong> Correct selections: {{@correct_mcq@}}.</p>
<p><strong>Part (f):</strong> At 10x frequency: \\(\\alpha\\) increases (more loss in material), FSPL increases by 20 dB (\\(20\\log_{{10}}(10) = 20\\)), antenna becomes smaller. Net: significantly worse link margin. Generally NOT recommended unless bandwidth is critical.</p>"""


def gen_inputs():
    return """    <input>
      <name>ans1</name>
      <type>dropdown</type>
      <tans>ta_class</tans>
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
      <tans>ta_alpha</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>12.3</syntaxhint>
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
      <tans>ta_atten</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>45.6</syntaxhint>
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
      <tans>ta_FSPL</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>45.6</syntaxhint>
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
      <tans>ta_Pr</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>1</insertstars>
      <syntaxhint>-23.4</syntaxhint>
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


# PRT definitions
PRT_CLASS = """    <prt>
      <name>prt_class</name>
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
        <trueanswernote>prt_class-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct media classification.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_class-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. Compute \\(\\tan\\delta = \\sigma/(\\omega\\varepsilon)\\) and classify.</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_ALPHA = """    <prt>
      <name>prt_alpha</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans2</sans>
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
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_alpha-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect \\(\\alpha\\). Use the general formula.</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_ATTEN = """    <prt>
      <name>prt_atten</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans3</sans>
        <tans>ta_atten</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_atten-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct material attenuation.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_atten-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. Attenuation (dB) = 8.686 &times; &alpha; &times; d.</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_FSPL = """    <prt>
      <name>prt_FSPL</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumRelative</answertest>
        <sans>ans4</sans>
        <tans>ta_FSPL</tans>
        <testoptions>0.05</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_FSPL-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct FSPL.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_FSPL-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. FSPL = 20 log<sub>10</sub>(4&pi;R/&lambda;).</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_PR = """    <prt>
      <name>prt_Pr</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackvariables><text></text></feedbackvariables>
      <node>
        <name>0</name>
        <answertest>NumAbsolute</answertest>
        <sans>ans5</sans>
        <tans>ta_Pr</tans>
        <testoptions>0.5</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty/>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt_Pr-1-T</trueanswernote>
        <truefeedback format="html"><text><![CDATA[<p>Correct received power.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_Pr-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Incorrect. P<sub>r</sub> = P<sub>t</sub> + G<sub>t</sub> + G<sub>r</sub> - FSPL - Material attenuation.</p>]]></text></falsefeedback>
      </node>
    </prt>"""

PRT_MCQ = """    <prt>
      <name>prt_mcq</name>
      <value>2.0000000</value>
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
        <truefeedback format="html"><text><![CDATA[<p>All correct improvements identified.</p>]]></text></truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty/>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt_mcq-1-F</falseanswernote>
        <falsefeedback format="html"><text><![CDATA[<p>Not all correct improvements identified.</p>]]></text></falsefeedback>
      </node>
    </prt>"""


def gen_variant(v):
    vals = compute_values(v)
    return f"""<question type="stack">
  <name><text>Midterm 2 - Q5{v['id']}: EM Waves + Link Budget ({v['name']})</text></name>
  <questiontext format="html"><text><![CDATA[
{gen_questiontext(v, vals)}
]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[
{gen_generalfeedback(v, vals)}
]]></text></generalfeedback>
  <defaultgrade>12</defaultgrade>
  <penalty>0.1000000</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <stackversion><text>2024032401</text></stackversion>
  <questionvariables><text><![CDATA[
{gen_questionvariables(v, vals)}
]]></text></questionvariables>
  <specificfeedback format="html"><text><![CDATA[
[[feedback:prt_class]]
[[feedback:prt_alpha]]
[[feedback:prt_atten]]
[[feedback:prt_FSPL]]
[[feedback:prt_Pr]]
[[feedback:prt_mcq]]
]]></text></specificfeedback>
  <questionnote><text>{{@ta_alpha@}}, {{@ta_atten@}}, {{@ta_FSPL@}}, {{@ta_Pr@}}</text></questionnote>
  <questiondescription format="html"><text></text></questiondescription>
  <prtcorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:green;"><i class="fa fa-check"></i></span> Correct!]]></text></prtcorrect>
  <prtpartiallycorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:orange;"><i class="fa fa-adjust"></i></span> Partially correct.]]></text></prtpartiallycorrect>
  <prtincorrect format="html"><text><![CDATA[<span style="font-size: 1.5em; color:red;"><i class="fa fa-times"></i></span> Incorrect.]]></text></prtincorrect>
  <multiplicativetries>0</multiplicativetries>
{gen_inputs()}
{PRT_CLASS}
{PRT_ALPHA}
{PRT_ATTEN}
{PRT_FSPL}
{PRT_PR}
{PRT_MCQ}
</question>"""


COMPANION = """<question type="essay">
  <name><text>Midterm 2 - Q5: Upload Handwritten Work (EM Waves + Link Budget)</text></name>
  <questiontext format="html"><text><![CDATA[
<h3>Upload Handwritten Work for Q5</h3>
<p>Upload work for Question 5 (EM Wave Propagation + Wireless Link Budget).</p>
<h4>Include:</h4>
<ul>
  <li>Loss tangent calculation and classification</li>
  <li>Alpha computation with formula for the medium type</li>
  <li>FSPL calculation</li>
  <li>Complete link budget arithmetic</li>
  <li>Frequency trade-off analysis for Part (f)</li>
</ul>
<p>Up to 2 files. Worth 0 points.</p>
<p><strong>Teacher notice:</strong> Set Allow attachments to 2+ in quiz settings.</p>
]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Thank you.</p>]]></text></generalfeedback>
  <defaultgrade>0</defaultgrade><penalty>0</penalty><hidden>0</hidden>
  <responseformat>noinline</responseformat><responserequired>0</responserequired>
  <responsefieldlines>5</responsefieldlines>
  <attachments>2</attachments><attachmentsrequired>1</attachmentsrequired>
  <filetypeslist>.pdf,.jpg,.jpeg,.png</filetypeslist>
  <graderinfo format="html"><text><![CDATA[
<ul><li>Check loss tangent and classification</li><li>Verify alpha formula matches medium type</li>
<li>For Part (f): look for multi-dimensional trade-off analysis, not just one factor</li></ul>
]]></text></graderinfo>
  <responsetemplate format="html"><text></text></responsetemplate>
</question>"""


def main():
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>", ""]
    for v in VARIANTS:
        parts.extend([f"<!-- {'='*60} -->", f"<!-- Q5 {v['id']}: {v['name']} -->",
                       f"<!-- {'='*60} -->", gen_variant(v), ""])
    parts.extend([f"<!-- {'='*60} -->", "<!-- Companion Essay -->",
                   f"<!-- {'='*60} -->", COMPANION, "", "</quiz>"])
    xml = "\n".join(parts)

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base, "xml", "pool_q5_high.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"Generated {out_path}")
    print(f"  Lines: {xml.count(chr(10)) + 1}")
    print("\nVerification:")
    print(f"{'Var':<4} {'Class':<25} {'alpha':>10} {'Atten(dB)':>10} {'FSPL(dB)':>10} {'Pr(dBm)':>10}")
    for v in VARIANTS:
        vals = compute_values(v)
        print(f"{v['id']:<4} {vals['classification']:<25} {vals['alpha']:>10.3f} "
              f"{vals['atten_dB']:>10.2f} {vals['FSPL_dB']:>10.2f} {vals['Pr_dBm']:>10.2f}")

    # P-STACK-32
    hints = {"ans2": 12.3, "ans3": 45.6, "ans4": 45.6, "ans5": -23.4}
    answers = {"ans2": [], "ans3": [], "ans4": [], "ans5": []}
    for v in VARIANTS:
        vals = compute_values(v)
        answers["ans2"].append(vals["alpha"])
        answers["ans3"].append(vals["atten_dB"])
        answers["ans4"].append(vals["FSPL_dB"])
        answers["ans5"].append(vals["Pr_dBm"])
    print("\nP-STACK-32:")
    ok = True
    for inp, h in hints.items():
        for i, a in enumerate(answers[inp], 1):
            if abs(a) < 0.001: continue
            r = abs(h - a) / abs(a)
            if r < 0.15:
                print(f"  FAIL: {inp} hint={h} vs V{i} ans={a:.4g} ({r:.3f})")
                ok = False
    print("  ALL PASS" if ok else "  FAILURES")


if __name__ == "__main__":
    main()
