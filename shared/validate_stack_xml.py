#!/usr/bin/env python
"""
STACK XML Validator — validates Moodle STACK question XML files against
project conventions (PATTERNS.md P-STACK-01 through P-STACK-23).

Reports only. Does not modify files.

Usage:
    python shared/validate_stack_xml.py path/to/file.xml
    python shared/validate_stack_xml.py weekly/          # all XMLs in dir
    python shared/validate_stack_xml.py --all            # entire repo
    python shared/validate_stack_xml.py --exams-only     # exam files only
"""

import sys
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path


# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------

class Result:
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class CheckResult:
    def __init__(self, status, check_num, check_name, message):
        self.status = status
        self.check_num = check_num
        self.check_name = check_name
        self.message = message

    def __str__(self):
        return f"  [{self.status}] Check {self.check_num}: {self.check_name} — {self.message}"


# ---------------------------------------------------------------------------
# Check 1 — PRT chain integrity (P-STACK-08)
# ---------------------------------------------------------------------------

def check_prt_chains(question, q_name):
    results = []
    prts = question.findall(".//prt")
    if not prts:
        results.append(CheckResult(Result.PASS, 1, "PRT chain integrity", "no PRTs found"))
        return results

    all_valid = True
    total_prts = len(prts)

    for prt in prts:
        prt_name_el = prt.find("name")
        prt_name = prt_name_el.text if prt_name_el is not None and prt_name_el.text else "unnamed"
        nodes = prt.findall("node")
        node_names = set()

        for node in nodes:
            name_el = node.find("name")
            if name_el is not None and name_el.text is not None:
                node_names.add(name_el.text.strip())

        # Check each node's next-node references
        referenced_nodes = set()
        for node in nodes:
            name_el = node.find("name")
            node_name = name_el.text.strip() if name_el is not None and name_el.text else "?"

            for direction in ["truenextnode", "falsenextnode"]:
                next_el = node.find(direction)
                if next_el is not None and next_el.text is not None:
                    next_val = next_el.text.strip()
                    if next_val == "-1":
                        continue  # valid terminal
                    if next_val not in node_names:
                        results.append(CheckResult(
                            Result.FAIL, 1, "PRT chain integrity",
                            f"{prt_name}/node{node_name} — {direction}={next_val} references non-existent node"
                        ))
                        all_valid = False
                    else:
                        referenced_nodes.add(next_val)

        # Check for unreachable nodes (not the first node, never referenced)
        if node_names:
            first_node = min(node_names, key=lambda x: int(x) if x.isdigit() else float('inf'))
            for nn in node_names:
                if nn != first_node and nn not in referenced_nodes:
                    results.append(CheckResult(
                        Result.WARN, 1, "PRT chain integrity",
                        f"{prt_name}/node{nn} — unreachable (never referenced as next node)"
                    ))
                    all_valid = False

    if all_valid:
        results.append(CheckResult(
            Result.PASS, 1, "PRT chain integrity",
            f"{total_prts} PRTs, all chains valid"
        ))
    return results


# ---------------------------------------------------------------------------
# Check 2 — Answer test selection (P-STACK-02, P-STACK-05, P-STACK-07)
# ---------------------------------------------------------------------------

def check_answer_tests(question, q_name):
    results = []
    prts = question.findall(".//prt")
    issues_found = False

    for prt in prts:
        prt_name_el = prt.find("name")
        prt_name = prt_name_el.text if prt_name_el is not None and prt_name_el.text else "unnamed"

        for node in prt.findall("node"):
            node_name_el = node.find("name")
            node_name = node_name_el.text.strip() if node_name_el is not None and node_name_el.text else "?"
            test_el = node.find("answertest")
            test = test_el.text.strip() if test_el is not None and test_el.text else ""

            tans_el = node.find("tans")
            tans = tans_el.text.strip() if tans_el is not None and tans_el.text else ""

            # NumRelative with teacher answer that looks like 0
            if test == "NumRelative" and tans in ("0", "0.0", "0.00"):
                results.append(CheckResult(
                    Result.WARN, 2, "Answer test selection",
                    f"{prt_name}/node{node_name} — NumRelative with teacher answer '{tans}', verify not zero"
                ))
                issues_found = True

            # NumSigFigs as primary answer test (P-STACK-05)
            if test == "NumSigFigs":
                results.append(CheckResult(
                    Result.FAIL, 2, "Answer test selection",
                    f"{prt_name}/node{node_name} — NumSigFigs as primary answer test (P-STACK-05)"
                ))
                issues_found = True

            # SigFigsStrict as scoring gate (P-STACK-07)
            if test == "SigFigsStrict":
                # Check if it affects score
                for mode_tag in ["truescoremode", "falsescoremode"]:
                    mode_el = node.find(mode_tag)
                    if mode_el is not None:
                        results.append(CheckResult(
                            Result.FAIL, 2, "Answer test selection",
                            f"{prt_name}/node{node_name} — SigFigsStrict as scoring gate (P-STACK-07)"
                        ))
                        issues_found = True
                        break

    if not issues_found:
        results.append(CheckResult(
            Result.PASS, 2, "Answer test selection",
            "all answer tests comply with conventions"
        ))
    return results


# ---------------------------------------------------------------------------
# Check 3 — MCQ shuffle (P-STACK-23)
# ---------------------------------------------------------------------------

def check_mcq_shuffle(question, q_name):
    results = []
    inputs = question.findall(".//input")
    qvars_el = question.find(".//questionvariables/text")
    qvars = ""
    if qvars_el is not None and qvars_el.text:
        qvars = qvars_el.text

    issues_found = False
    mcq_count = 0

    for inp in inputs:
        type_el = inp.find("type")
        name_el = inp.find("name")
        if type_el is None or type_el.text is None:
            continue
        inp_type = type_el.text.strip()
        inp_name = name_el.text.strip() if name_el is not None and name_el.text else "?"

        if inp_type in ("dropdown", "radio"):
            mcq_count += 1
            # Check if questionvariables contain random_permutation
            if "random_permutation(" not in qvars:
                results.append(CheckResult(
                    Result.FAIL, 3, "MCQ shuffle",
                    f"{q_name}/{inp_name} — {inp_type} input missing random_permutation() (P-STACK-23)"
                ))
                issues_found = True

    if mcq_count == 0:
        results.append(CheckResult(
            Result.PASS, 3, "MCQ shuffle", "no MCQ inputs found"
        ))
    elif not issues_found:
        results.append(CheckResult(
            Result.PASS, 3, "MCQ shuffle",
            f"{mcq_count} MCQ inputs, all use random_permutation()"
        ))
    return results


# ---------------------------------------------------------------------------
# Check 4 — insertstars (P-STACK-10)
# ---------------------------------------------------------------------------

def check_insertstars(question, q_name):
    results = []
    inputs = question.findall(".//input")
    issues_found = False

    for inp in inputs:
        type_el = inp.find("type")
        name_el = inp.find("name")
        if type_el is None or type_el.text is None:
            continue
        inp_type = type_el.text.strip()
        inp_name = name_el.text.strip() if name_el is not None and name_el.text else "?"

        if inp_type == "algebraic":
            stars_el = inp.find("insertstars")
            stars_val = stars_el.text.strip() if stars_el is not None and stars_el.text else "0"
            if stars_val != "1":
                results.append(CheckResult(
                    Result.FAIL, 4, "insertstars",
                    f"{q_name}/{inp_name} — algebraic input missing insertstars=1 (P-STACK-10)"
                ))
                issues_found = True

    if not issues_found:
        results.append(CheckResult(
            Result.PASS, 4, "insertstars", "all algebraic inputs have insertstars=1 (or none found)"
        ))
    return results


# ---------------------------------------------------------------------------
# Check 5 — CDATA wrapping (P-STACK-04)
# ---------------------------------------------------------------------------

def _has_bare_lt(text_content):
    """Check if text contains a literal < outside of CDATA blocks."""
    if not text_content:
        return False
    # Remove CDATA blocks
    cleaned = re.sub(r'<!\[CDATA\[.*?\]\]>', '', text_content, flags=re.DOTALL)
    # Check for < that isn't part of an XML tag pattern — look for < followed by
    # something that looks like a comparison (space, digit, variable name not forming a tag)
    # We look for < that appears in Maxima code contexts (e.g., "if x < 5")
    # A bare < in Maxima code would be like: variable < value
    if re.search(r'(?<!\!)\b\w+\s*<\s*\w', cleaned):
        return True
    return False


def check_cdata(question, q_name):
    results = []
    issues_found = False

    for tag_name in ["questionvariables", "feedbackvariables"]:
        for elem in question.iter(tag_name):
            text_el = elem.find("text")
            if text_el is None:
                continue
            # Get the raw text including any text content
            raw = text_el.text if text_el.text else ""
            if _has_bare_lt(raw):
                # Find which PRT this belongs to (if feedbackvariables)
                parent_prt = None
                for prt in question.findall(".//prt"):
                    if elem in list(prt.iter(tag_name)):
                        prt_name_el = prt.find("name")
                        parent_prt = prt_name_el.text if prt_name_el is not None else "?"
                        break
                location = f"{parent_prt}/{tag_name}" if parent_prt else tag_name
                results.append(CheckResult(
                    Result.FAIL, 5, "CDATA wrapping",
                    f"{q_name}/{location} — bare '<' outside CDATA block (P-STACK-04)"
                ))
                issues_found = True

    if not issues_found:
        results.append(CheckResult(
            Result.PASS, 5, "CDATA wrapping", "no bare '<' found outside CDATA blocks"
        ))
    return results


# ---------------------------------------------------------------------------
# Check 6 — Base64 in exam XMLs (P-STACK-15)
# ---------------------------------------------------------------------------

def check_base64_exam(filepath, raw_content):
    results = []
    if "exam" in str(filepath).lower():
        if "data:image/" in raw_content:
            results.append(CheckResult(
                Result.FAIL, 6, "Base64 in exam",
                f"exam file contains base64 image data (P-STACK-15)"
            ))
        else:
            results.append(CheckResult(
                Result.PASS, 6, "Base64 in exam", "no base64 images in exam file"
            ))
    else:
        results.append(CheckResult(
            Result.PASS, 6, "Base64 in exam", "not an exam file (skipped)"
        ))
    return results


# ---------------------------------------------------------------------------
# Check 7 — Non-empty name tags (P-STACK-01)
# ---------------------------------------------------------------------------

def check_name_tags(question, q_name):
    results = []
    name_el = question.find("name/text")
    if name_el is None or not name_el.text or not name_el.text.strip():
        results.append(CheckResult(
            Result.FAIL, 7, "Non-empty name",
            "question <name><text> is empty or missing (P-STACK-01)"
        ))
    else:
        results.append(CheckResult(
            Result.PASS, 7, "Non-empty name", f"'{name_el.text.strip()}'"
        ))
    return results


# ---------------------------------------------------------------------------
# Check 8 — Exact arithmetic (P-STACK-06)
# ---------------------------------------------------------------------------

def check_exact_arithmetic(question, q_name):
    results = []
    issues_found = False

    for tag_name in ["questionvariables", "feedbackvariables"]:
        for elem in question.iter(tag_name):
            text_el = elem.find("text")
            if text_el is None or not text_el.text:
                continue
            content = text_el.text
            # Look for float literals like 1e-7, 1e-6, etc.
            matches = re.findall(r'\b\d+e[+-]?\d+\b', content, re.IGNORECASE)
            for match in matches:
                # Skip common acceptable uses like 3e8 (speed of light) or
                # engineering notation in float() wrappers
                # Flag specifically problematic patterns like 1e-7 for mu0
                parent_prt = None
                for prt in question.findall(".//prt"):
                    if elem in list(prt.iter(tag_name)):
                        prt_name_el = prt.find("name")
                        parent_prt = prt_name_el.text if prt_name_el is not None else "?"
                        break
                location = f"{parent_prt}/{tag_name}" if parent_prt else tag_name
                results.append(CheckResult(
                    Result.WARN, 8, "Exact arithmetic",
                    f"{q_name}/{location} — float literal '{match}' found, consider exact form like 1/10^7 (P-STACK-06)"
                ))
                issues_found = True

    if not issues_found:
        results.append(CheckResult(
            Result.PASS, 8, "Exact arithmetic", "no float literals found"
        ))
    return results


# ---------------------------------------------------------------------------
# Check 9 — Companion handwritten notes question (exam files only)
# ---------------------------------------------------------------------------

def check_handwritten_notes(questions, filepath):
    results = []
    if "exam" not in str(filepath).lower():
        results.append(CheckResult(
            Result.PASS, 9, "Handwritten notes companion", "not an exam file (skipped)"
        ))
        return results

    # Collect all question names by type
    stack_names = []
    essay_names = set()

    for q in questions:
        q_type = q.get("type", "")
        name_el = q.find("name/text")
        if name_el is None or not name_el.text:
            continue
        name = name_el.text.strip()

        if q_type == "stack":
            if not name.endswith("_handwritten_notes"):
                stack_names.append(name)
        elif q_type == "essay":
            essay_names.add(name)

    issues_found = False
    for sname in stack_names:
        companion = sname + "_handwritten_notes"
        if companion not in essay_names:
            results.append(CheckResult(
                Result.WARN, 9, "Handwritten notes companion",
                f"WARN: {sname} has no companion handwritten notes question. "
                f"For new exam questions, generate one using exam mode in STACK_XML_Generator."
            ))
            issues_found = True

    if not issues_found:
        if stack_names:
            results.append(CheckResult(
                Result.PASS, 9, "Handwritten notes companion",
                f"{len(stack_names)} STACK questions, all have companions"
            ))
        else:
            results.append(CheckResult(
                Result.PASS, 9, "Handwritten notes companion", "no STACK questions in exam file"
            ))

    return results


# ---------------------------------------------------------------------------
# Main validation logic
# ---------------------------------------------------------------------------

def validate_file(filepath):
    """Validate a single XML file. Returns list of CheckResults."""
    filepath = Path(filepath)
    results = []

    # Read raw content for checks that need it
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_content = f.read()
    except Exception as e:
        results.append(CheckResult(Result.FAIL, 0, "File read", str(e)))
        return results

    # Parse XML
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        results.append(CheckResult(Result.FAIL, 0, "XML parse", f"malformed XML: {e}"))
        return results

    # Find all questions
    questions = root.findall(".//question")
    stack_questions = [q for q in questions if q.get("type") == "stack"]

    if not stack_questions:
        results.append(CheckResult(Result.PASS, 0, "File scan", "no STACK questions found"))
        return results

    # Run checks 1-8 on each STACK question
    for q in stack_questions:
        q_name_el = q.find("name/text")
        q_name = q_name_el.text.strip() if q_name_el is not None and q_name_el.text else "unnamed"

        results.extend(check_name_tags(q, q_name))          # Check 7
        results.extend(check_prt_chains(q, q_name))          # Check 1
        results.extend(check_answer_tests(q, q_name))        # Check 2
        results.extend(check_mcq_shuffle(q, q_name))         # Check 3
        results.extend(check_insertstars(q, q_name))         # Check 4
        results.extend(check_cdata(q, q_name))               # Check 5
        results.extend(check_exact_arithmetic(q, q_name))    # Check 8

    # Run file-level checks
    results.extend(check_base64_exam(filepath, raw_content))   # Check 6
    results.extend(check_handwritten_notes(questions, filepath))  # Check 9

    return results


def find_xml_files(path, exams_only=False):
    """Find all XML files under a path."""
    path = Path(path)
    if path.is_file() and path.suffix == ".xml":
        return [path]

    pattern = "**/*.xml"
    files = sorted(path.glob(pattern))

    if exams_only:
        files = [f for f in files if "exam" in str(f).lower()]

    return files


def print_results(filepath, results):
    """Print results for a file and return counts."""
    print(f"\nValidating: {filepath}")

    fail_count = 0
    warn_count = 0
    pass_count = 0

    for r in results:
        print(str(r))
        if r.status == Result.FAIL:
            fail_count += 1
        elif r.status == Result.WARN:
            warn_count += 1
        else:
            pass_count += 1

    print(f"\n  Summary: {fail_count} FAIL, {warn_count} WARN, {pass_count} PASS")
    return fail_count, warn_count, pass_count


# ---------------------------------------------------------------------------
# Self-test with known-good minimal STACK XML
# ---------------------------------------------------------------------------

SELF_TEST_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
<question type="stack">
  <name><text>Self-Test Question</text></name>
  <questiontext format="html">
    <text><![CDATA[
    <p>What is 2+2?</p>
    <p>[[input:ans1]] [[validation:ans1]]</p>
    <p>Which is bigger?</p>
    <p>[[input:ans2]] [[validation:ans2]]</p>
    ]]></text>
  </questiontext>
  <generalfeedback format="html"><text></text></generalfeedback>
  <defaultgrade>2.0000000</defaultgrade>
  <penalty>0.0000000</penalty>
  <hidden>0</hidden>
  <questionvariables>
    <text><![CDATA[
ta1: 4;
options: random_permutation([[1, true, "4"], [2, false, "5"]]);
ta2_correct: 1;
]]></text>
  </questionvariables>
  <specificfeedback format="html">
    <text>[[feedback:prt1]][[feedback:prt2]]</text>
  </specificfeedback>
  <questionnote><text>Self-test</text></questionnote>
  <input>
    <name>ans1</name>
    <type>numerical</type>
    <tans>ta1</tans>
    <boxsize>5</boxsize>
    <strictsyntax>1</strictsyntax>
    <insertstars>0</insertstars>
    <syntaxhint/>
    <syntaxattribute>0</syntaxattribute>
    <forbidwords/>
    <allowwords/>
    <forbidfloat>0</forbidfloat>
    <requirelowestterms>0</requirelowestterms>
    <checkanswertype>0</checkanswertype>
    <mustverify>1</mustverify>
    <showvalidation>1</showvalidation>
    <options/>
  </input>
  <input>
    <name>ans2</name>
    <type>dropdown</type>
    <tans>options</tans>
    <boxsize>5</boxsize>
    <strictsyntax>1</strictsyntax>
    <insertstars>0</insertstars>
    <syntaxhint/>
    <syntaxattribute>0</syntaxattribute>
    <forbidwords/>
    <allowwords/>
    <forbidfloat>1</forbidfloat>
    <requirelowestterms>0</requirelowestterms>
    <checkanswertype>0</checkanswertype>
    <mustverify>1</mustverify>
    <showvalidation>1</showvalidation>
    <options/>
  </input>
  <prt>
    <name>prt1</name>
    <value>1.0000000</value>
    <autosimplify>1</autosimplify>
    <feedbackstyle>1</feedbackstyle>
    <feedbackvariables><text/></feedbackvariables>
    <node>
      <name>0</name>
      <description>Check answer</description>
      <answertest>NumRelative</answertest>
      <sans>ans1</sans>
      <tans>ta1</tans>
      <testoptions>0.05</testoptions>
      <quiet>0</quiet>
      <truescoremode>=</truescoremode>
      <truescore>1.0000000</truescore>
      <truepenalty/>
      <truenextnode>-1</truenextnode>
      <trueanswernote>prt1-0-T</trueanswernote>
      <truefeedback format="html"><text>Correct!</text></truefeedback>
      <falsescoremode>=</falsescoremode>
      <falsescore>0.0000000</falsescore>
      <falsepenalty/>
      <falsenextnode>-1</falsenextnode>
      <falseanswernote>prt1-0-F</falseanswernote>
      <falsefeedback format="html"><text>Incorrect.</text></falsefeedback>
    </node>
  </prt>
  <prt>
    <name>prt2</name>
    <value>1.0000000</value>
    <autosimplify>1</autosimplify>
    <feedbackstyle>1</feedbackstyle>
    <feedbackvariables><text/></feedbackvariables>
    <node>
      <name>0</name>
      <description>Check MCQ</description>
      <answertest>AlgEquiv</answertest>
      <sans>ans2</sans>
      <tans>ta2_correct</tans>
      <testoptions/>
      <quiet>0</quiet>
      <truescoremode>=</truescoremode>
      <truescore>1.0000000</truescore>
      <truepenalty/>
      <truenextnode>-1</truenextnode>
      <trueanswernote>prt2-0-T</trueanswernote>
      <truefeedback format="html"><text>Correct!</text></truefeedback>
      <falsescoremode>=</falsescoremode>
      <falsescore>0.0000000</falsescore>
      <falsepenalty/>
      <falsenextnode>-1</falsenextnode>
      <falseanswernote>prt2-0-F</falseanswernote>
      <falsefeedback format="html"><text>Incorrect.</text></falsefeedback>
    </node>
  </prt>
</question>
</quiz>
"""


def run_self_test():
    """Run validator against a known-good inline XML. Returns True if all pass."""
    import tempfile
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False, encoding="utf-8")
    tmp.write(SELF_TEST_XML)
    tmp.close()

    try:
        results = validate_file(tmp.name)
        fails = [r for r in results if r.status == Result.FAIL]
        if fails:
            print("SELF-TEST FAILED — known-good XML produced failures:")
            for f in fails:
                print(f"  {f}")
            return False
        else:
            print("Self-test passed: known-good XML validated cleanly.")
            return True
    finally:
        os.unlink(tmp.name)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Run self-test first
    print("=" * 60)
    print("Running self-test...")
    print("=" * 60)
    if not run_self_test():
        print("\nSelf-test failed. Aborting.")
        sys.exit(1)
    print()

    arg = sys.argv[1]
    exams_only = "--exams-only" in sys.argv

    if arg == "--all":
        # Find repo root (look for CLAUDE.md)
        search_dir = Path(".")
        xml_files = find_xml_files(search_dir, exams_only)
    elif arg == "--exams-only":
        search_dir = Path(".")
        xml_files = find_xml_files(search_dir, exams_only=True)
    else:
        target = Path(arg)
        if not target.exists():
            print(f"Error: {target} does not exist")
            sys.exit(1)
        xml_files = find_xml_files(target, exams_only)

    if not xml_files:
        print("No XML files found.")
        sys.exit(0)

    print("=" * 60)
    print(f"Validating {len(xml_files)} XML file(s)...")
    print("=" * 60)

    total_fail = 0
    total_warn = 0
    total_pass = 0

    for f in xml_files:
        results = validate_file(f)
        f_count, w_count, p_count = print_results(f, results)
        total_fail += f_count
        total_warn += w_count
        total_pass += p_count

    print("\n" + "=" * 60)
    print(f"GRAND TOTAL: {total_fail} FAIL, {total_warn} WARN, {total_pass} PASS")
    print(f"Files scanned: {len(xml_files)}")
    print("=" * 60)

    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
