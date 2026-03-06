"""
Embed PNG circuit diagrams into STACK/Moodle XML files.

Replaces [INSERT DIAGRAM: ...] placeholders with proper <img> tags
using @@PLUGINFILE@@ and adds base64-encoded <file> elements
so Moodle can display the images after XML import.
"""
import base64
import re
import os

# Map each XML file to its diagram replacements
# Format: (placeholder_path_substring, png_file_path, alt_text)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPLACEMENTS = {
    "xml/pool_q1_easy.xml": [
        ("diagrams/q1/q1_v1_two_node.svg", "diagrams/q1/q1_v1_two_node.png", "Q1-V1 Two-node DC circuit"),
        ("diagrams/q1/q1_v2_two_mesh.svg", "diagrams/q1/q1_v2_two_mesh.png", "Q1-V2 Two-mesh DC circuit"),
        ("diagrams/q1/q1_v3_t_network.svg", "diagrams/q1/q1_v3_t_network.png", "Q1-V3 T-network circuit"),
        ("diagrams/q1/q1_v4_bridge.svg", "diagrams/q1/q1_v4_bridge.png", "Q1-V4 Wheatstone bridge circuit"),
    ],
    "xml/pool_q2_medium_a.xml": [
        ("diagrams/q2/q2_v1_inductor_rl.svg", "diagrams/q2/q2_v1_inductor_rl.png", "Q2-V1 Series RL circuit"),
        ("diagrams/q2/q2_v2_capacitor_rc.svg", "diagrams/q2/q2_v2_capacitor_rc.png", "Q2-V2 Series RC circuit"),
        ("diagrams/q2/q2_v3_inductor_waveform.svg", "diagrams/q2/q2_v3_inductor_waveform.png", "Q2-V3 Inductor with piecewise linear current waveform"),
        ("diagrams/q2/q2_v4_capacitor_parallel.svg", "diagrams/q2/q2_v4_capacitor_parallel.png", "Q2-V4 Parallel capacitor circuit"),
    ],
    "xml/pool_q3_medium_b.xml": [
        ("diagrams/q3/q3_v1_rl_step.svg", "diagrams/q3/q3_v1_rl_step.png", "Q3-V1 RL step response circuit"),
        ("diagrams/q3/q3_v2_rc_step.svg", "diagrams/q3/q3_v2_rc_step.png", "Q3-V2 RC step response circuit"),
        ("diagrams/q3/q3_v3_rl_natural.svg", "diagrams/q3/q3_v3_rl_natural.png", "Q3-V3 RL natural response circuit"),
        ("diagrams/q3/q3_v4_rc_natural.svg", "diagrams/q3/q3_v4_rc_natural.png", "Q3-V4 RC natural response circuit"),
    ],
    "xml/pool_q4_difficult.xml": [
        ("diagrams/q4/q4_v1_rc_switch.svg", "diagrams/q4/q4_v1_rc_switch.png", "Q4-V1 RC circuit with switch"),
        ("diagrams/q4/q4_v2_rl_switch.svg", "diagrams/q4/q4_v2_rl_switch.png", "Q4-V2 RL circuit with switch"),
        ("diagrams/q4/q4_v3_thevenin_rc.svg", "diagrams/q4/q4_v3_thevenin_rc.png", "Q4-V3 Thevenin equivalent RC circuit"),
    ],
}


def encode_png(filepath):
    """Read a PNG file and return its base64 encoding."""
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def process_xml(xml_rel_path, replacements):
    """Process one XML file: replace placeholders with img tags and add file elements."""
    xml_path = os.path.join(REPO_ROOT, xml_rel_path)
    with open(xml_path, "r", encoding="utf-8") as f:
        content = f.read()

    for svg_placeholder, png_rel_path, alt_text in replacements:
        png_path = os.path.join(REPO_ROOT, png_rel_path)
        png_filename = os.path.basename(png_rel_path)

        if not os.path.exists(png_path):
            print(f"  WARNING: {png_path} not found, skipping")
            continue

        # Step 1: Replace the [INSERT DIAGRAM] placeholder with <img> tag
        placeholder_pattern = (
            r'<p><strong>\[INSERT DIAGRAM: '
            + re.escape(svg_placeholder)
            + r'\]</strong></p>'
        )
        img_tag = (
            f'<p><img src="@@PLUGINFILE@@/{png_filename}" '
            f'alt="{alt_text}" style="max-width:600px;" /></p>'
        )

        if not re.search(placeholder_pattern, content):
            print(f"  WARNING: placeholder for {svg_placeholder} not found")
            continue

        content = re.sub(placeholder_pattern, img_tag, content)

        # Step 2: Add <file> element with base64-encoded PNG
        # Insert right before </questiontext> that follows this image
        b64_data = encode_png(png_path)
        file_element = (
            f'    <file name="{png_filename}" path="/" '
            f'encoding="base64">{b64_data}</file>\n'
        )

        # Find the </text> that closes the CDATA containing this image,
        # and insert the <file> element between </text> and </questiontext>
        # Strategy: find the img tag we just inserted, then find the next
        # ]]></text> after it, and insert the file element after that line.

        img_pos = content.find(f'@@PLUGINFILE@@/{png_filename}')
        if img_pos == -1:
            print(f"  WARNING: Could not find inserted img tag for {png_filename}")
            continue

        # Find the next ]]></text> after the img tag
        cdata_end = content.find("]]></text>", img_pos)
        if cdata_end == -1:
            print(f"  WARNING: Could not find ]]></text> after {png_filename}")
            continue

        text_close_end = cdata_end + len("]]></text>")
        # Find the end of that line
        newline_pos = content.find("\n", text_close_end)
        if newline_pos == -1:
            newline_pos = text_close_end

        # Insert the file element after the </text> line
        content = content[:newline_pos + 1] + file_element + content[newline_pos + 1:]

        print(f"  Embedded {png_filename} ({len(b64_data)} chars base64)")

    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Updated {xml_rel_path}")


def main():
    print("Embedding PNG diagrams into STACK/Moodle XML files...")
    print(f"Repository root: {REPO_ROOT}")
    print()

    for xml_file, replacements in REPLACEMENTS.items():
        print(f"Processing {xml_file}:")
        process_xml(xml_file, replacements)
        print()

    print("Done! All images embedded.")


if __name__ == "__main__":
    main()
