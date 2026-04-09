"""Embed SVG diagrams into Moodle STACK XML using @@PLUGINFILE@@ approach.

For each [DIAGRAM: ...] placeholder:
1. Replace with <img src="@@PLUGINFILE@@/name.svg"> tag
2. Add <file name="..." encoding="base64"> after the </text> of that questiontext

Also removes ASCII art <pre> blocks that follow placeholders.

Usage:
    python embed_diagrams.py
"""
import base64
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DIAGRAMS = BASE / "diagrams"
XML_DIR = BASE / "xml"

# Ordered SVG list per XML (matches placeholder order in file)
EMBED_CONFIG = {
    "pool_q1_medium.xml": [
        ("q1/v1_ecore.svg", "E-core electromagnet with center-limb air gap and two coils"),
        ("q1/v2_ccore.svg", "C-core electromagnet with single air gap and two coils"),
        ("q1/v3_toroid.svg", "Toroidal core with air gap cut and two coils"),
        ("q1/v4_rectangular.svg", "Rectangular core with two series air gaps and two coils"),
    ],
    "pool_q2_medium.xml": [
        ("q2/v1_series_rlc_natural.svg", "Series RLC natural response circuit with SPDT switch"),
        ("q2/v2_parallel_rlc_step.svg", "Parallel RLC step response with closing switch and current source"),
        ("q2/v3_series_rlc_step.svg", "Series RLC step response with closing switch and voltage source"),
        ("q2/v4_parallel_rlc_natural.svg", "Parallel RLC natural response with pre-charged capacitor"),
    ],
    "pool_q3_high.xml": [
        ("q3/v1_ecore_aiding.svg", "E-core physical winding diagram showing coil directions"),
        ("q3/v2_toroid_opposing.svg", "Toroid physical winding diagram with opposite winding senses"),
        ("q3/v3_ccore_aiding.svg", "C-core physical winding diagram with same winding direction"),
        ("q3/v4_rectangular_opposing.svg", "Rectangular core winding diagram with opposite directions"),
    ],
    "pool_q4_high.xml": [
        ("q4/v1v2_tl_resistive.svg", "Transmission line with source and resistive load"),
        ("q4/v1v2_tl_resistive.svg", "Transmission line with source and resistive load"),
        ("q4/v3_tl_short.svg", "Transmission line with source and short-circuit load"),
        ("q4/v4_tl_open.svg", "Transmission line with source and open-circuit load"),
    ],
    "pool_q5_high.xml": [
        ("q5/v1_gpr_soil.svg", "Ground-penetrating radar signal path through soil"),
        ("q5/v2_wifi_wall.svg", "Wi-Fi signal path through concrete wall"),
        ("q5/v3_iot_earth.svg", "IoT sensor signal path from underground to gateway"),
        ("q5/v4_satellite_roof.svg", "Satellite downlink through building roof"),
    ],
}


def process_xml(xml_name: str, svg_specs: list) -> None:
    xml_path = XML_DIR / xml_name
    content = xml_path.read_text(encoding="utf-8")

    # Find all DIAGRAM placeholders
    placeholder_re = re.compile(r'<p>\[DIAGRAM:.*?\]</p>')
    matches = list(placeholder_re.finditer(content))

    if len(matches) != len(svg_specs):
        print(f"  SKIP {xml_name}: {len(matches)} placeholders vs {len(svg_specs)} SVGs",
              file=sys.stderr)
        return

    # Process in reverse order (to preserve string positions)
    file_elements_to_insert = []  # (questiontext_close_pos, file_element_str)

    for i in range(len(matches) - 1, -1, -1):
        match = matches[i]
        svg_rel, alt_text = svg_specs[i]
        svg_path = DIAGRAMS / svg_rel
        svg_filename = svg_path.name

        # For Q4 shared diagram: give V2 a unique Moodle filename
        if i == 1 and svg_specs[0][0] == svg_specs[1][0]:
            svg_filename = svg_path.stem + "_v2" + svg_path.suffix

        if not svg_path.exists():
            print(f"  ERROR: {svg_path} not found", file=sys.stderr)
            continue

        # Build img tag
        img_tag = (
            f'<p><img src="@@PLUGINFILE@@/{svg_filename}" '
            f'alt="{alt_text}" '
            f'style="max-width:100%%; width:600px;" /></p>'
        )

        # Remove any <pre> block immediately after the placeholder
        after_placeholder = content[match.end():match.end() + 500]
        pre_match = re.match(r'\s*<pre>.*?</pre>', after_placeholder, re.DOTALL)
        end_pos = match.end() + pre_match.end() if pre_match else match.end()

        # Replace placeholder (and optional pre block)
        content = content[:match.start()] + img_tag + content[end_pos:]

        # Base64 encode the SVG
        b64 = base64.b64encode(svg_path.read_bytes()).decode("ascii")
        file_elem = f'  <file name="{svg_filename}" path="/" encoding="base64">{b64}</file>'
        file_elements_to_insert.append((i, file_elem))

    # Now insert <file> elements into the correct <questiontext> blocks
    # Find all </text>\n</questiontext> patterns (questiontext closings)
    qt_close_re = re.compile(r'(]]></text>)\s*(</questiontext>)')
    qt_closes = list(qt_close_re.finditer(content))

    # Match file elements to questiontext blocks
    # The Nth placeholder is in the Nth STACK question's questiontext
    # (companion essay questions don't have DIAGRAM placeholders)
    # qt_closes includes ALL questiontext blocks (STACK + essay)
    # We need to find which qt_close corresponds to which placeholder

    # Strategy: for each placeholder index, find the qt_close that follows it
    # Since we already replaced placeholders with img tags, search for @@PLUGINFILE@@
    pluginfile_re = re.compile(r'@@PLUGINFILE@@')
    pf_matches = list(pluginfile_re.finditer(content))

    for pf_idx, pf_match in enumerate(pf_matches):
        if pf_idx >= len(file_elements_to_insert):
            break
        _, file_elem = file_elements_to_insert[pf_idx]

        # Find the next ]]></text>\n</questiontext> after this @@PLUGINFILE@@
        for qt_close in qt_closes:
            if qt_close.start() > pf_match.start():
                # Insert file element before </questiontext>
                insert_pos = qt_close.start(2)
                content = (content[:insert_pos] + "\n" + file_elem + "\n  "
                          + content[insert_pos:])
                # Re-find qt_closes since positions shifted
                qt_closes = list(qt_close_re.finditer(content))
                break

    xml_path.write_text(content, encoding="utf-8")
    svg_count = len([s for s in svg_specs if (DIAGRAMS / s[0]).exists()])
    print(f"  {xml_name}: {svg_count} diagrams embedded")


def main():
    print("Embedding diagrams into XML files...")
    for xml_name, svg_specs in EMBED_CONFIG.items():
        process_xml(xml_name, svg_specs)
    print("Done.")


if __name__ == "__main__":
    main()
