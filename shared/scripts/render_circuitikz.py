#!/usr/bin/env python3
"""Compile CircuiTikZ/TikZ .tex files to SVG.

Usage:
    python render_circuitikz.py input.tex [output.svg]
    python render_circuitikz.py --all directory/

Single-file mode:
    Compiles input.tex → output.svg (default: same name, .svg extension).

Batch mode (--all):
    Compiles every .tex file in the given directory to .svg.

Supports pdf2svg (preferred) or dvisvgm (fallback) for PDF-to-SVG conversion.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _find_svg_converter():
    """Return ('pdf2svg', ...) or ('dvisvgm', ...) depending on availability."""
    if shutil.which("pdf2svg"):
        return "pdf2svg"
    if shutil.which("dvisvgm"):
        return "dvisvgm"
    return None


def compile_tex_to_svg(tex_path: Path, svg_path: Path) -> bool:
    """Compile a .tex file to .svg via pdflatex + pdf2svg/dvisvgm.

    Returns True on success, False on failure.
    """
    tex_path = tex_path.resolve()
    svg_path = svg_path.resolve()

    converter = _find_svg_converter()
    if converter is None:
        print("ERROR: Neither pdf2svg nor dvisvgm found on PATH.", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory() as tmpdir:
        # pdflatex → PDF
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode",
             f"-output-directory={tmpdir}", str(tex_path)],
            capture_output=True, text=True, timeout=60,
        )
        pdf_name = tex_path.stem + ".pdf"
        pdf_path = Path(tmpdir) / pdf_name

        if result.returncode != 0 or not pdf_path.exists():
            print(f"ERROR compiling {tex_path.name}:", file=sys.stderr)
            # Show last 20 lines of log for diagnostics
            log_lines = result.stdout.splitlines()
            for line in log_lines[-20:]:
                print(f"  {line}", file=sys.stderr)
            return False

        # PDF → SVG
        if converter == "pdf2svg":
            result = subprocess.run(
                ["pdf2svg", str(pdf_path), str(svg_path)],
                capture_output=True, text=True, timeout=30,
            )
        else:  # dvisvgm
            result = subprocess.run(
                ["dvisvgm", "--pdf", str(pdf_path), "-o", str(svg_path), "--no-fonts"],
                capture_output=True, text=True, timeout=30,
            )

        if result.returncode != 0:
            print(f"ERROR converting {pdf_name} to SVG ({converter}):", file=sys.stderr)
            print(f"  {result.stderr}", file=sys.stderr)
            return False

    print(f"  {tex_path.name} -> {svg_path.name}  [{converter}]")
    return True


def main():
    parser = argparse.ArgumentParser(description="Compile .tex to .svg")
    parser.add_argument("input", help=".tex file or directory (with --all)")
    parser.add_argument("output", nargs="?", help="Output .svg path (single-file mode)")
    parser.add_argument("--all", action="store_true",
                        help="Batch compile all .tex files in directory")
    args = parser.parse_args()

    if args.all:
        directory = Path(args.input)
        if not directory.is_dir():
            print(f"Error: {directory} is not a directory", file=sys.stderr)
            sys.exit(1)

        tex_files = sorted(directory.glob("*.tex"))
        if not tex_files:
            print(f"No .tex files found in {directory}")
            sys.exit(0)

        print(f"Compiling {len(tex_files)} .tex files in {directory}:")
        failures = []
        for tex_file in tex_files:
            svg_file = tex_file.with_suffix(".svg")
            if not compile_tex_to_svg(tex_file, svg_file):
                failures.append(tex_file.name)

        if failures:
            print(f"\nFailed: {', '.join(failures)}", file=sys.stderr)
            sys.exit(1)
        print(f"\nAll {len(tex_files)} files compiled successfully.")

    else:
        tex_file = Path(args.input)
        if not tex_file.exists():
            print(f"Error: {tex_file} not found", file=sys.stderr)
            sys.exit(1)

        if args.output:
            svg_file = Path(args.output)
        else:
            svg_file = tex_file.with_suffix(".svg")

        if not compile_tex_to_svg(tex_file, svg_file):
            sys.exit(1)


if __name__ == "__main__":
    main()
