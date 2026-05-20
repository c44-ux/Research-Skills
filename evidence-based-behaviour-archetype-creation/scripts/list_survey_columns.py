#!/usr/bin/env python3
"""Print all column names from a survey .xlsx or .csv export."""
import sys
from pathlib import Path

from survey_deps import ensure_survey_dependencies

if len(sys.argv) < 2:
    print("Usage: python list_survey_columns.py <path-to-survey.xlsx|.csv>", file=sys.stderr)
    sys.exit(1)

ensure_survey_dependencies()

path = Path(sys.argv[1])

import pandas as pd

if path.suffix.lower() == ".csv":
    df = pd.read_csv(path, encoding="utf-8-sig")
else:
    df = pd.read_excel(path, engine="openpyxl")

for i, c in enumerate(df.columns):
    print(f"{i}\t{c}")
