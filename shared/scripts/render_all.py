#!/usr/bin/env python3
"""
Master render script: generates all circuit diagrams as SVG and PNG.
Runs each circuit script, then copies output to the correct diagram folder.
For pure schemdraw scripts, also generates PNG via matplotlib backend.
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DIAGRAMS_DIR = SCRIPT_DIR.parent

# Map script names to output folders and filenames
CIRCUITS = {
    # Q1: DC Resistive
    'q1_v1_two_node': 'q1',
    'q1_v2_two_mesh': 'q1',
    'q1_v3_t_network': 'q1',
    'q1_v4_bridge': 'q1',
    # Q2: Energy Storage
    'q2_v1_inductor_rl': 'q2',
    'q2_v2_capacitor_rc': 'q2',
    'q2_v3_inductor_waveform': 'q2',
    'q2_v4_capacitor_parallel': 'q2',
    # Q3: Laplace / First-Order
    'q3_v1_rl_step': 'q3',
    'q3_v2_rc_step': 'q3',
    'q3_v3_rl_natural': 'q3',
    'q3_v4_rc_natural': 'q3',
    # Q4: Transient Analysis
    'q4_v1_rc_switch': 'q4',
    'q4_v2_rl_switch': 'q4',
    'q4_v3_thevenin_rc': 'q4',
}

# Scripts that produce their own PNG (matplotlib-based)
SELF_PNG = {'q2_v3_inductor_waveform', 'q4_v1_rc_switch', 'q4_v2_rl_switch', 'q4_v3_thevenin_rc'}


def render_all():
    os.chdir(SCRIPT_DIR)
    success = 0
    errors = 0

    for name, folder in CIRCUITS.items():
        script = SCRIPT_DIR / f'{name}.py'
        out_dir = DIAGRAMS_DIR / folder
        svg_src = SCRIPT_DIR / f'{name}.svg'
        png_src = SCRIPT_DIR / f'{name}.png'
        svg_dst = out_dir / f'{name}.svg'
        png_dst = out_dir / f'{name}.png'

        print(f'Rendering {name}...')
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f'  ERROR: {result.stderr.strip()}')
            errors += 1
            continue

        # Copy SVG
        if svg_src.exists():
            shutil.copy2(svg_src, svg_dst)
            print(f'  SVG → {svg_dst}')
        else:
            print(f'  WARNING: No SVG produced')

        # Generate PNG for pure schemdraw scripts
        if name not in SELF_PNG:
            try:
                import schemdraw
                # Re-run with PNG save by modifying the save path
                script_content = script.read_text()
                png_script = script_content.replace(
                    f"d.save('{name}.svg')",
                    f"d.save('{name}.png', dpi=150)"
                )
                exec(compile(png_script, str(script), 'exec'))
                if png_src.exists():
                    shutil.copy2(png_src, png_dst)
                    print(f'  PNG → {png_dst}')
            except Exception as e:
                print(f'  PNG generation error: {e}')
        else:
            # Script already produces PNG
            if png_src.exists():
                shutil.copy2(png_src, png_dst)
                print(f'  PNG → {png_dst}')

        success += 1

    print(f'\nDone: {success} rendered, {errors} errors')


if __name__ == '__main__':
    render_all()
