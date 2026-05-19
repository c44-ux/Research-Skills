#!/usr/bin/env python3
"""Print all column names from a survey .xlsx or .csv export."""
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python list_survey_columns.py <path-to-survey.xlsx|.csv>", file=sys.stderr)
    sys.exit(1)

path = Path(sys.argv[1])

import pandas as pd

df = pd.read_excel(path, engine="openpyxl")
for i, c in enumerate(df.columns):
    print(f"{i}\t{c}")
