"""Shared Python dependencies for survey export scripts."""
from __future__ import annotations

import subprocess
import sys


def ensure_survey_dependencies(*, quiet_install: bool = True) -> None:
    """Import pandas + openpyxl, or install them with pip if missing."""
    try:
        import openpyxl  # noqa: F401
        import pandas  # noqa: F401
    except ImportError:
        cmd = [sys.executable, "-m", "pip", "install", "-r"]
        req = __import__("pathlib").Path(__file__).resolve().parent.parent / "requirements.txt"
        if req.is_file():
            cmd.append(str(req))
        else:
            cmd = [sys.executable, "-m", "pip", "install", "pandas>=2.0", "openpyxl>=3.1"]
        if quiet_install:
            cmd.append("-q")
        print(
            "Survey scripts require pandas and openpyxl. Installing (one-time)…",
            file=sys.stderr,
        )
        subprocess.check_call(cmd)
