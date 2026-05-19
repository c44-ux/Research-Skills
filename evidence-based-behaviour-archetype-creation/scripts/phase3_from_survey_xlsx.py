#!/usr/bin/env python3
"""
Phase 3: Excel survey -> evidence-based behaviour archetype markdown (+ optional HTML checklist).

Usage:
  python phase3_from_survey_xlsx.py "<path-to.xlsx>" [output.md]
  python phase3_from_survey_xlsx.py --list-columns "<path-to.xlsx>"
  python phase3_from_survey_xlsx.py --export-mapping-template "<path-to.xlsx>"
  python phase3_from_survey_xlsx.py --export-mapping-template --force "<path-to.xlsx>"

Editable mapping table (open in Excel), beside your survey file:
  <survey-name>.column_mapping.csv

Generate it first:
  python phase3_from_survey_xlsx.py --export-mapping-template "<path-to.xlsx>"

Requires: pandas, openpyxl
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MIN_SIGNAL = 3
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_METADATA_PREFIXES = [
    "Respondent ID",
    "Collector ID",
    "Start Date",
    "End Date",
    "IP Address",
    "Email Address",
    "First Name",
    "Last Name",
    "Custom Data",
    "rq_flag",
    "status",
]
CHECKLIST_HTML = SCRIPT_DIR.parent / "docs" / "evidence_based_behaviour_archetypes_checklist.html"
GENERATOR = SCRIPT_DIR.parents[1] / "cs-ux-personas" / "scripts" / "persona_generator.py"

TOOL_KEYWORDS = [
    "xero",
    "myob",
    "quickbooks",
    "spreadsheet",
    "excel",
    "expensify",
    "receipt",
    "bank feed",
    "google sheet",
    "zoho",
    "freshbooks",
    "accounting software",
]

# Optional pain-column heuristics seeded into a new mapping template (edit per survey).
GENERIC_PAIN_RULE_ROWS: list[dict[str, str]] = [
    {"behaviour_archetype_field": "", "map_type": "pain_contains", "survey_column_header": "frustrat", "active": "Y", "notes": "Header substring match"},
    {"behaviour_archetype_field": "", "map_type": "pain_contains", "survey_column_header": "biggest challenge", "active": "Y", "notes": ""},
    {"behaviour_archetype_field": "", "map_type": "pain_contains", "survey_column_header": "most challenging", "active": "Y", "notes": ""},
    {"behaviour_archetype_field": "", "map_type": "pain_contains", "survey_column_header": "pain point", "active": "Y", "notes": ""},
    {"behaviour_archetype_field": "", "map_type": "pain_contains", "survey_column_header": "what is hard", "active": "Y", "notes": ""},
    {"behaviour_archetype_field": "", "map_type": "pain_contains", "survey_column_header": "what makes it difficult", "active": "Y", "notes": ""},
    {"behaviour_archetype_field": "", "map_type": "pain_contains", "survey_column_header": "barrier", "active": "Y", "notes": ""},
]


@dataclass
class SurveyPlan:
    """Resolved column plan for one survey export."""

    exact: dict[str, str] = field(default_factory=dict)
    groups: dict[str, list[str]] = field(default_factory=dict)
    pain_columns: list[str] = field(default_factory=list)
    motivation_rank_columns: list[str] = field(default_factory=list)
    supplemental: dict[str, str] = field(default_factory=dict)
    all_used_columns: list[str] = field(default_factory=list)

    def describe(self) -> dict[str, str | list[str]]:
        out: dict[str, str | list[str]] = {}
        for k, v in self.exact.items():
            out[k] = v
        for k, cols in self.groups.items():
            out[k] = cols if len(cols) > 1 else cols[0]
        if self.motivation_rank_columns:
            out["motivations (rank columns)"] = self.motivation_rank_columns
        if self.pain_columns:
            out["pain_points"] = self.pain_columns
        return out


SUBROW_LABELS_SKIP = {
    "Response",
    "Other (please specify)",
    "Open-Ended Response",
    "Question Viewed",
    "",
}


def load_generator():
    spec = importlib.util.spec_from_file_location("persona_generator", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load persona_generator at {GENERATOR}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def is_metadata_column(name: str, prefixes: list[str]) -> bool:
    if name.startswith("Unnamed:"):
        return True
    return any(name.startswith(p) for p in prefixes)


def group_surveymonkey_columns(columns: list[str], metadata_prefixes: list[str]) -> list[tuple[str, list[str]]]:
    """Group a parent question with following Unnamed:* sub-columns."""
    groups: list[tuple[str, list[str]]] = []
    i = 0
    while i < len(columns):
        name = columns[i]
        if is_metadata_column(name, metadata_prefixes):
            i += 1
            continue
        block = [name]
        j = i + 1
        while j < len(columns) and columns[j].startswith("Unnamed:"):
            block.append(columns[j])
            j += 1
        groups.append((name, block))
        i = j
    return groups


def resolve_map_path(survey_path: Path) -> Path:
    """Column mapping CSV lives beside the survey export (one file per study)."""
    return survey_path.with_name(survey_path.stem + ".column_mapping.csv")


def _dedupe_column_names(names: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out: list[str] = []
    for name in names:
        if name not in seen:
            seen[name] = 0
            out.append(name)
        else:
            seen[name] += 1
            out.append(f"{name} [{seen[name]}]")
    return out


def load_survey_dataframe(survey_path: Path):
    """Load .xlsx or condensed SurveyMonkey .csv (two header rows)."""
    import pandas as pd

    survey_path = Path(survey_path)
    if survey_path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(survey_path, engine="openpyxl").dropna(how="all")

    if survey_path.suffix.lower() != ".csv":
        raise ValueError(f"Unsupported survey file type: {survey_path.suffix}")

    raw = pd.read_csv(survey_path, header=None, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    if len(raw) < 3:
        return pd.read_csv(survey_path, encoding="utf-8-sig").dropna(how="all")

    subrow = raw.iloc[1].astype(str).str.strip()
    if subrow.str.contains("Response", na=False).sum() < 3:
        return pd.read_csv(survey_path, encoding="utf-8-sig").dropna(how="all")

    qrow = raw.iloc[0]
    names: list[str] = []
    current_q = ""
    for i in range(raw.shape[1]):
        q = str(qrow.iloc[i]).strip() if pd.notna(qrow.iloc[i]) else ""
        s = str(subrow.iloc[i]).strip() if pd.notna(subrow.iloc[i]) else ""
        if q:
            current_q = " ".join(q.split())
        if s in SUBROW_LABELS_SKIP:
            if current_q:
                names.append(current_q)
            elif q:
                names.append(" ".join(q.split()))
            else:
                names.append(f"_col_{i}")
        elif s:
            if current_q:
                names.append(f"{current_q} || {s}")
            else:
                names.append(s)
        elif current_q:
            names.append(current_q)
        elif q:
            names.append(" ".join(q.split()))
        else:
            names.append(f"_col_{i}")

    names = _dedupe_column_names(names)
    df = raw.iloc[2:].copy()
    df.columns = names
    df = df[~df.apply(lambda r: r.astype(str).str.strip().eq("").all(), axis=1)]
    return df.reset_index(drop=True)


def _is_active(val) -> bool:
    if val is None:
        return True
    s = str(val).strip().lower()
    return s in ("", "y", "yes", "1", "true", "x")


def load_survey_plan(
    columns: list[str],
    map_path: Path | None = None,
    survey_path: Path | None = None,
) -> SurveyPlan:
    if map_path is None and survey_path is not None:
        map_path = resolve_map_path(survey_path)
    if map_path is None or not map_path.is_file():
        hint = resolve_map_path(survey_path) if survey_path else map_path
        raise FileNotFoundError(
            f"Column mapping not found: {hint}\n"
            'Run: python phase3_from_survey_xlsx.py --export-mapping-template "<survey-file>"\n'
            "Then edit the .column_mapping.csv before running Phase 3."
        )

    if map_path.suffix.lower() == ".json":
        return _load_survey_plan_from_json(columns, map_path)
    return _load_survey_plan_from_csv(columns, map_path)


def _load_survey_plan_from_csv(columns: list[str], map_path: Path) -> SurveyPlan:
    import csv

    colset = set(columns)
    plan = SurveyPlan()
    pain_hints: list[str] = []
    skip_exact: set[str] = set()
    group_parents: dict[str, str] = {}
    metadata_prefixes = list(DEFAULT_METADATA_PREFIXES)

    with map_path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if not _is_active(row.get("active")):
                continue
            field = (row.get("behaviour_archetype_field") or "").strip()
            map_type = (row.get("map_type") or "exact").strip().lower()
            header = (row.get("survey_column_header") or "").strip()
            if not header:
                continue

            if map_type == "exact" and field:
                if header in colset:
                    plan.exact[field] = header
                    plan.all_used_columns.append(header)
            elif map_type == "group_parent" and field:
                group_parents[field] = header
            elif map_type == "skip":
                skip_exact.add(header)
            elif map_type == "pain_contains":
                pain_hints.append(header.lower())

    grouped = group_surveymonkey_columns(columns, metadata_prefixes)
    for group_key, parent_header in group_parents.items():
        for parent, block in grouped:
            if parent == parent_header:
                plan.groups[group_key] = block
                plan.all_used_columns.extend(block)
                break

    for col in columns:
        if col in skip_exact:
            continue
        cl = col.lower()
        if any(h in cl for h in pain_hints):
            plan.pain_columns.append(col)
            plan.all_used_columns.append(col)

    for key in ("accountant_frequency", "accountant_relationship"):
        if key in plan.exact:
            plan.supplemental[key] = plan.exact[key]

    return plan


def _load_survey_plan_from_json(columns: list[str], map_path: Path) -> SurveyPlan:
    cfg = json.loads(map_path.read_text(encoding="utf-8"))
    colset = set(columns)
    metadata_prefixes = cfg.get("metadata_prefixes", DEFAULT_METADATA_PREFIXES)
    plan = SurveyPlan()

    for field, header in cfg.get("exact_columns", {}).items():
        if header in colset:
            plan.exact[field] = header
            plan.all_used_columns.append(header)

    grouped = group_surveymonkey_columns(columns, metadata_prefixes)
    for group_key, parent_header in cfg.get("column_groups", {}).items():
        for parent, block in grouped:
            if parent == parent_header:
                plan.groups[group_key] = block
                plan.all_used_columns.extend(block)
                break

    never_pain = set(cfg.get("never_map_to_pain_points", []))
    pain_hints = cfg.get("pain_point_column_contains", [])
    for col in columns:
        if col in never_pain:
            continue
        cl = col.lower()
        if any(h in cl for h in pain_hints):
            plan.pain_columns.append(col)
            plan.all_used_columns.append(col)

    for key in ("accountant_frequency", "accountant_relationship"):
        if key in plan.exact:
            plan.supplemental[key] = plan.exact[key]

    return plan


def _write_mapping_csv(out: Path, fieldnames: list[str], rows_out: list[dict[str, str]]) -> Path:
    import csv
    from datetime import datetime

    def write_to(path: Path) -> None:
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in rows_out:
                writer.writerow({k: row.get(k, "") for k in fieldnames})

    try:
        write_to(out)
        return out
    except PermissionError:
        candidates = [
            out.with_name(out.stem + ".generated.csv"),
            out.parent / f"{out.stem}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        ]
        for fallback in candidates:
            try:
                write_to(fallback)
                print(
                    "\nWARNING: Could not overwrite the mapping file (it is probably open in Excel).\n"
                    f"  Locked file: {out}\n"
                    f"  Wrote to:    {fallback}\n"
                    "  Close Excel, then either:\n"
                    "    - Copy/rename the .generated.csv over the .column_mapping.csv, or\n"
                    f"    - Re-run with: --map \"{fallback}\"\n",
                    file=sys.stderr,
                )
                return fallback
            except PermissionError:
                continue
        raise PermissionError(
            f"Permission denied writing mapping CSV. Close Excel/OneDrive lock on:\n  {out}"
        ) from None


def _default_row_for_column(col: str) -> list[str]:
    if col.startswith("Unnamed:"):
        return ["", "skip", col, "N", "SurveyMonkey sub-column — attach via group_parent row above, or skip"]
    if any(col.startswith(p) for p in DEFAULT_METADATA_PREFIXES):
        return ["", "skip", col, "N", "Metadata"]
    return ["", "skip", col, "N", "Optional — set behaviour_archetype_field + map_type only if you need this column"]


def _load_existing_mapping_rows(path: Path) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    import csv

    existing_rows: list[dict[str, str]] = []
    by_header: dict[str, dict[str, str]] = {}
    if not path.is_file():
        return existing_rows, by_header
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            header = (row.get("survey_column_header") or "").strip()
            if not header or header.startswith("#"):
                existing_rows.append(row)
                continue
            existing_rows.append(row)
            by_header[header] = row
    return existing_rows, by_header


def _row_for_column(col: str, by_header: dict[str, dict[str, str]], fieldnames: list[str]) -> dict[str, str]:
    if col in by_header and (by_header[col].get("behaviour_archetype_field") or by_header[col].get("map_type")):
        return by_header[col]
    cells = _default_row_for_column(col)
    return dict(zip(fieldnames, cells))


def export_mapping_template(survey_path: Path, force: bool = False) -> Path:
    """Write or update .column_mapping.csv with every column from the survey export."""
    import csv

    df = load_survey_dataframe(survey_path)
    columns = [str(c) for c in df.columns]
    out = survey_path.with_name(survey_path.stem + ".column_mapping.csv")
    fieldnames = ["behaviour_archetype_field", "map_type", "survey_column_header", "active", "notes"]

    _, by_header = _load_existing_mapping_rows(out)

    if force or not out.is_file():
        rows_out: list[dict[str, str]] = [
            {"behaviour_archetype_field": "", "map_type": "", "survey_column_header": "# map_type: exact | group_parent | skip | pain_contains", "active": "", "notes": ""},
            {
                "behaviour_archetype_field": "",
                "map_type": "",
                "survey_column_header": "# Blank behaviour_archetype_field is OK for skip rows. Only map questions you need.",
                "active": "",
                "notes": "",
            },
            {
                "behaviour_archetype_field": "",
                "map_type": "",
                "survey_column_header": "# Suggested fields: usage_context, routine_text, goals, motivations, values, occupation (your survey may differ)",
                "active": "",
                "notes": "",
            },
        ]
        rows_out.extend(GENERIC_PAIN_RULE_ROWS)
        for col in columns:
            rows_out.append(_row_for_column(col, by_header, fieldnames))
        action = "Rebuilt mapping template"
    else:
        rows_out = []
        with out.open(encoding="utf-8-sig", newline="") as f:
            rows_out = list(csv.DictReader(f))
        known = {
            (r.get("survey_column_header") or "").strip()
            for r in rows_out
            if (r.get("survey_column_header") or "").strip()
            and not (r.get("survey_column_header") or "").strip().startswith("#")
        }
        added = 0
        for col in columns:
            if col in known:
                continue
            rows_out.append(_row_for_column(col, by_header, fieldnames))
            added += 1
        action = f"Updated (+{added} new columns)" if added else "No new columns to add"

    written = _write_mapping_csv(out, fieldnames, rows_out)

    print(f"{action}: {written}")
    print(f"  Survey columns in xlsx: {len(columns)}")
    print(f"  Rows in mapping file: {len(rows_out)}")
    return written


def norm_freq(val: str) -> str:
    v = val.strip().lower()
    if not v or v in ("nan", "none", "n/a"):
        return "unknown"
    if any(x in v for x in ("never", "not applicable", "n/a")):
        return "rare"
    if any(x in v for x in ("daily", "every day", "each day", "day")):
        return "daily"
    if any(x in v for x in ("week", "weekly", "fortnight")):
        return "weekly"
    if any(x in v for x in ("month", "monthly", "quarter")):
        return "monthly"
    if any(x in v for x in ("rare", "seldom", "occasion", "ad hoc", "tax time")):
        return "occasional"
    return v[:80]


def norm_device_from_answer(text: str) -> str | None:
    v = text.lower()
    if any(x in v for x in ("mobile", "phone", "smartphone", "on the go")):
        return "mobile"
    if any(x in v for x in ("tablet", "ipad")):
        return "tablet"
    if any(x in v for x in ("desktop", "laptop", "computer", "pc ", " on pc")):
        return "desktop"
    return None


def extract_tools(text: str) -> list[str]:
    v = text.lower()
    found = []
    for tool in TOOL_KEYWORDS:
        if tool in v:
            found.append(tool)
    return found


def cell_selected(val) -> bool:
    if val is None:
        return False
    try:
        import pandas as pd

        if pd.isna(val):
            return False
    except ImportError:
        pass
    s = str(val).strip().lower()
    return s not in ("", "nan", "none", "n/a")


def row_get(row, col: str):
    if col not in row.index:
        return None
    v = row[col]
    if v is None:
        return None
    try:
        import pandas as pd

        if pd.isna(v):
            return None
    except ImportError:
        pass
    return v


def split_multi(val) -> list[str]:
    if val is None:
        return []
    try:
        import pandas as pd

        if pd.isna(val):
            return []
    except ImportError:
        pass
    s = str(val).strip()
    if not s or s.lower() in ("nan", "none", "n/a"):
        return []
    parts = re.split(r"[;|,/\n]+", s)
    return [p.strip() for p in parts if p.strip()]


def parse_ordinal_confidence(text: str) -> int | None:
    v = text.lower()
    for score, word in enumerate(
        ["not at all", "slightly", "moderately", "very", "extremely"],
        start=1,
    ):
        if word in v:
            return score
    return None


def extract_ranked_motivations(row, rank_columns: list[str]) -> list[str]:
    ranked: list[tuple[int, str]] = []
    for col in rank_columns:
        v = row_get(row, col)
        if v is None:
            continue
        try:
            rank = int(float(str(v).strip()))
        except ValueError:
            continue
        label = col.split(" || ")[-1].strip() if " || " in col else col
        ranked.append((rank, label))
    ranked.sort(key=lambda x: x[0])
    return [label for _, label in ranked]


def collect_group_selections(row, columns: list[str], parent: str) -> list[str]:
    """Multi-select / matrix: non-empty cells; use column header as option label."""
    selected: list[str] = []
    for col in columns:
        if not cell_selected(row_get(row, col)):
            continue
        label = col if not col.startswith("Unnamed:") else str(row_get(row, col))
        label = str(label).strip()
        if label and label not in selected:
            selected.append(label)
    return selected


def row_to_record(row, plan: SurveyPlan, idx: int) -> dict:
    rec: dict = {"user_id": f"survey_{idx}"}

    routine_col = plan.exact.get("routine_text")
    routine_text = ""
    if routine_col:
        v = row_get(row, routine_col)
        if v is not None:
            routine_text = str(v).strip()

    ctx_col = plan.exact.get("usage_context")
    if ctx_col:
        v = row_get(row, ctx_col)
        if v is not None:
            ctx = str(v).strip()
            rec["usage_context"] = ctx[:120]
            rec["usage_frequency"] = norm_freq(ctx)

    if routine_text:
        rec["usage_frequency"] = norm_freq(routine_text)
        tools = extract_tools(routine_text)
        if tools:
            rec.setdefault("features_used", [])
            for t in tools:
                if t not in rec["features_used"]:
                    rec["features_used"].append(t)
        device = norm_device_from_answer(routine_text)
        if device:
            rec["primary_device"] = device

    sw_col = plan.exact.get("software")
    if sw_col:
        rec.setdefault("features_used", [])
        for tool in split_multi(row_get(row, sw_col)):
            if tool.lower() not in [f.lower() for f in rec["features_used"]]:
                rec["features_used"].append(tool)

    admin_col = plan.exact.get("admin_approach")
    if admin_col:
        v = row_get(row, admin_col)
        if v is not None:
            # Stated admin model (e.g. DIY vs delegated) — keep as goal-adjacent signal
            admin = str(v).strip()
            rec.setdefault("goals", [])
            if admin not in rec["goals"]:
                rec["goals"].append(admin)

    if plan.exact.get("goals"):
        v = row_get(row, plan.exact["goals"])
        if v is not None:
            g = str(v).strip()
            rec.setdefault("goals", [])
            if g not in rec["goals"]:
                rec["goals"].append(g)

    if plan.motivation_rank_columns:
        rec["motivations"] = extract_ranked_motivations(row, plan.motivation_rank_columns)
    elif "motivations" in plan.groups:
        rec["motivations"] = collect_group_selections(row, plan.groups["motivations"], plan.groups["motivations"][0])

    if "values" in plan.groups:
        rec["values"] = collect_group_selections(row, plan.groups["values"], plan.groups["values"][0])
    elif plan.exact.get("values"):
        vals = split_multi(row_get(row, plan.exact["values"]))
        if vals:
            rec["values"] = vals

    pains: list[str] = []
    for col in plan.pain_columns:
        v = row_get(row, col)
        if v is None:
            continue
        pains.extend(split_multi(v))
    if pains:
        rec["pain_points"] = pains

    if plan.exact.get("tech_confidence"):
        v = row_get(row, plan.exact["tech_confidence"])
        if v is not None:
            score = parse_ordinal_confidence(str(v))
            if score is not None:
                rec["tech_confidence"] = score

    if plan.exact.get("age"):
        v = row_get(row, plan.exact["age"])
        if v is not None:
            rec["age"] = str(v).strip()

    if plan.exact.get("quotes"):
        v = row_get(row, plan.exact["quotes"])
        if v is not None and str(v).strip():
            rec["quotes"] = [str(v).strip()]

    occ_col = plan.exact.get("occupation")
    if occ_col:
        v = row_get(row, occ_col)
        if v is not None:
            rec["occupation"] = str(v).strip()

    return {k: v for k, v in rec.items() if v is not None}


def build_markdown(analysis: dict, meta: dict, checklist_path: Path | None) -> str:
    gen = load_generator()
    g = gen.PersonaGenerator(min_signal_count=MIN_SIGNAL)
    formatted = g.format_analysis_output(analysis)

    lines = [
        "# Evidence-based behaviour archetype (survey)",
        "",
        f"**Generated from:** {meta['xlsx_path']}",
        f"**Respondents (rows):** {meta['n_rows']}",
        f"**Signal threshold:** {MIN_SIGNAL} (directional)",
        f"**Column map:** `{meta.get('map_file', '')}`",
        f"**AI involvement this run:** Claude-assisted synthesis from survey export only (PG3). Human review required before design use (PG7).",
        "",
        "## Evidence scope",
        "",
        "### Data / source summary",
        "- **Source type:** survey (single source)",
        f"- **Label:** {meta['label']}",
        f"- **Records:** {meta['n_rows']}",
        "- **Column mapping used:**",
    ]
    for field, spec in meta["mapping"].items():
        if isinstance(spec, list):
            lines.append(f"  - `{field}` ← {len(spec)} columns (SurveyMonkey group)")
            for c in spec[:6]:
                lines.append(f"    - `{c}`")
            if len(spec) > 6:
                lines.append(f"    - … +{len(spec) - 6} more")
        elif spec:
            lines.append(f"  - `{field}` ← `{spec}`")

    if meta.get("supplemental"):
        lines.append("- **Supplemental (reported separately, not in generator schema):**")
        for k, col in meta["supplemental"].items():
            lines.append(f"  - `{k}` ← `{col}`")

    unmapped = [c for c in meta["columns"] if c not in meta["used_columns"]]
    if unmapped:
        lines.append(f"- **Unmapped columns:** {len(unmapped)} (metadata, matrix tails, or not in map)")

    lines.extend(["", "### Data quality caveats"])
    for lim in analysis.get("limitations", [])[:8]:
        lines.append(f"- {lim}")
    for s in analysis.get("data_points", {}).get("sources", []):
        lines.append(f"- **{s['label']}:** {s['confidence_note']}")

    lines.extend(["", "## Observed patterns", ""])
    p = analysis.get("patterns", {})
    lines.append(f"- **Usage frequency:** {_fmt_dist(p.get('usage_frequency', {}))}")
    lines.append(f"- **Devices:** {_fmt_dist(p.get('devices', {}))}")
    lines.append(f"- **Contexts:** {_fmt_dist(p.get('contexts', {}))}")
    lines.append(f"- **Top features:** {', '.join(list(p.get('feature_usage', {}).keys())[:8]) or 'None observed'}")
    lines.append(f"- **Repeated pain points:** {_fmt_dist(p.get('pain_points', {}))}")

    lines.extend(["", "## Behaviour archetype profile", ""])
    lines.append(f"**Behavioural label (illustrative):** {_behavioural_label(analysis)}")
    lines.append("")
    lines.append(analysis.get("summary", ""))
    lines.append("")

    needs = analysis.get("needs_and_goals", {})
    lines.append("### Goals and needs (evidence-gated)")
    for gitem in needs.get("primary_goals", [])[:5]:
        lines.append(f"- {gitem}")
    for n in needs.get("functional_needs", [])[:5]:
        lines.append(f"- {n}")
    for ev in needs.get("supporting_evidence", [])[:4]:
        lines.append(f"  - *Evidence:* {ev}")

    lines.append("")
    lines.append("### Frustrations")
    if analysis.get("frustrations"):
        for f in analysis["frustrations"][:6]:
            c = f.get("evidence_count")
            cs = f"{c} mentions; " if c is not None else ""
            lines.append(f"- {f['issue']} ({cs}{f.get('source', 'survey')})")
    else:
        lines.append("- No dedicated friction question mapped in this export (see limitations).")

    lines.extend(["", "## Design implications", ""])
    for imp in analysis.get("design_implications", []):
        lines.append(f"- **Recommendation:** {imp['recommendation']}")
        lines.append(f"  - **Because:** {imp['because']}")

    lines.extend(["", "## Limitations and confidence", ""])
    for lim in analysis.get("limitations", []):
        lines.append(f"- {lim}")
    contra = analysis.get("contradictions", {})
    for c in contra.get("contradictions", []):
        lines.append(f"- **Contradiction / exception:** {c}")

    lines.extend(["", "---", "", "## Generator detail (Phase 3)", "", "```", formatted, "```", ""])

    if checklist_path and checklist_path.is_file():
        html = checklist_path.read_text(encoding="utf-8", errors="replace")
        lines.extend(["", "## Checklist (HTML)", "", html])
    else:
        lines.append(f"\n## Checklist (HTML)\n\n_Checklist not found at `{checklist_path}`._")

    return "\n".join(lines)


def _fmt_dist(d: dict) -> str:
    if not d:
        return "None"
    return ", ".join(f"{k} ({v})" for k, v in list(d.items())[:8])


def _behavioural_label(analysis: dict) -> str:
    segs = analysis.get("example_segments") or []
    if segs:
        return segs[0]["label"].replace("Example pattern: ", "")
    p = analysis.get("patterns", {})
    freq = next(iter(p.get("usage_frequency", {})), "mixed-frequency")
    dev = next(iter(p.get("devices", {})), "mixed devices")
    ctx = next(iter(p.get("contexts", {})), "mixed contexts")
    return f"{freq} usage on {dev} in {ctx} contexts"


def list_columns(survey_path: Path) -> None:
    map_path = resolve_map_path(survey_path)
    print(f"Mapping file: {map_path}\n")

    df = load_survey_dataframe(survey_path)
    columns = [str(c) for c in df.columns]
    plan = load_survey_plan(columns, map_path=map_path, survey_path=survey_path)
    print(f"File: {survey_path}")
    print(f"Rows: {len(df)}  Columns: {len(columns)}\n")
    print("=== Resolved mapping ===")
    for k, v in plan.describe().items():
        print(f"  {k}: {v}")
    print("\n=== All columns (index | mapped?) ===")
    used = set(plan.all_used_columns)
    for i, c in enumerate(columns):
        tag = "MAPPED" if c in used else "    "
        print(f"{i:3} {tag}  {c}")


def _require_survey_path(rest: list[str], usage: str) -> Path:
    if not rest:
        print(usage, file=sys.stderr)
        sys.exit(1)
    survey_path = Path(rest[0])
    if not survey_path.is_file():
        print(f"Survey file not found: {survey_path}", file=sys.stderr)
        sys.exit(1)
    return survey_path


def _parse_cli_args(argv: list[str]) -> tuple[dict[str, str | bool], list[str]]:
    """Extract flags; return (opts, positional)."""
    opts: dict[str, str | bool] = {}
    pos: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--force":
            opts["force"] = True
        elif a == "--map" and i + 1 < len(argv):
            opts["map"] = argv[i + 1]
            i += 1
        elif a.startswith("--"):
            pos.append(a)
        else:
            pos.append(a)
        i += 1
    return opts, pos


def main() -> None:
    args = [a for a in sys.argv[1:] if a]
    opts, pos = _parse_cli_args(args)

    if pos and pos[0] == "--list-columns":
        rest = [p for p in pos[1:] if not p.startswith("--")]
        survey_path = _require_survey_path(
            rest,
            "Usage: python phase3_from_survey_xlsx.py --list-columns <path-to-survey.xlsx|.csv>",
        )
        list_columns(survey_path)
        return

    if pos and pos[0] == "--export-mapping-template":
        rest = [p for p in pos[1:] if not p.startswith("--")]
        survey_path = _require_survey_path(
            rest,
            "Usage: python phase3_from_survey_xlsx.py --export-mapping-template <path-to-survey.xlsx|.csv>",
        )
        export_mapping_template(survey_path, force=bool(opts.get("force")))
        return

    if pos and pos[0] == "--segment-pains":
        rest = [p for p in pos[1:] if not p.startswith("--")]
        survey_path = _require_survey_path(
            rest,
            "Usage: python phase3_from_survey_xlsx.py --segment-pains <path-to-survey.xlsx|.csv>",
        )
        try:
            import pandas as pd  # noqa: F401
        except ImportError:
            import subprocess

            subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl", "-q"])
        df = load_survey_dataframe(survey_path)
        plan = load_survey_plan([str(c) for c in df.columns], survey_path=survey_path)
        records = [row_to_record(df.iloc[i], plan, i) for i in range(len(df))]
        from segment_pains import compute_segment_pains_from_df

        seg = compute_segment_pains_from_df(
            df, plan, row_to_record, row_get, split_multi
        )
        out_json = survey_path.with_name(survey_path.stem + ".segment_pains.json")
        out_json.write_text(json.dumps(seg, indent=2), encoding="utf-8")
        print(json.dumps(seg, indent=2))
        print(f"\nWrote: {out_json}")
        return

    positional = [p for p in pos if not p.startswith("--")]
    survey_path = _require_survey_path(
        positional,
        "Usage: python phase3_from_survey_xlsx.py <path-to-survey.xlsx|.csv> [output.md]",
    )

    out = (
        Path(positional[1])
        if len(positional) > 1
        else survey_path.with_suffix(".behaviour_archetype_phase3.md")
    )

    try:
        import pandas as pd  # noqa: F401
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl", "-q"])

    df = load_survey_dataframe(survey_path)
    columns = [str(c) for c in df.columns]
    map_path = Path(str(opts["map"])) if opts.get("map") else resolve_map_path(survey_path)
    plan = load_survey_plan(columns, map_path=map_path, survey_path=survey_path)

    records = [row_to_record(df.iloc[i], plan, i) for i in range(len(df))]
    label = f"{survey_path.stem} ({len(records)} respondents)"

    sources = [{"type": "survey", "data": records, "label": label}]
    gen_mod = load_generator()
    generator = gen_mod.PersonaGenerator(min_signal_count=MIN_SIGNAL)
    analysis = generator.generate_analysis(sources)

    from segment_pains import compute_segment_pains_from_df

    analysis["segment_pains"] = compute_segment_pains_from_df(
        df, plan, row_to_record, row_get, split_multi
    )

    meta = {
        "xlsx_path": str(survey_path),
        "n_rows": len(records),
        "label": label,
        "columns": columns,
        "mapping": plan.describe(),
        "supplemental": plan.supplemental,
        "used_columns": list(dict.fromkeys(plan.all_used_columns)),
        "map_file": str(map_path),
    }

    md = build_markdown(analysis, meta, CHECKLIST_HTML if CHECKLIST_HTML.is_file() else None)
    out.write_text(md, encoding="utf-8")
    json_out = survey_path.with_name(survey_path.stem + ".behaviour_archetype_phase3.analysis.json")
    json_out.write_text(json.dumps(analysis, indent=2), encoding="utf-8")

    print(f"Wrote: {out}")
    print(f"Wrote: {json_out}")
    print(f"Rows: {len(records)}")
    print("Column mapping:")
    for k, v in plan.describe().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
