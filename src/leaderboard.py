#!/usr/bin/env python3
"""The legacy mixed-condition board is superseded by the versioned reproduction snapshot."""
from pathlib import Path
import subprocess, sys
root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,'-I','reproduce.py'],cwd=root/'reproduction',check=True)
print("Current condition comparisons: leaderboard.md; primary and supplementary bootstrap commands: README.md")
