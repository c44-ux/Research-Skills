"""Pain-point and value distributions per survey segment (domain-neutral)."""
from __future__ import annotations

import re
from collections import Counter

# Substrings in column headers → pain source bucket (edit in code if your survey uses other wording).
PAIN_SOURCE_HINTS: dict[str, str] = {
    "take the most time": "time_consuming",
    "most time-consuming": "time_consuming",
    "most time consuming": "time_consuming",
    "hardest": "hardest",
    "most challenging": "hardest",
    "biggest challenge": "hardest",
    "how often": "difficulties_frequency",
    "frequency": "difficulties_frequency",
    "difficult": "difficulties_frequency",
    "problem": "difficulties_frequency",
}

SEGMENT_FIELD_PRIORITY = (
    "segment_primary",
    "segment_secondary",
    "usage_context",
    "segment",
)


def _slug_key(label: str, used: set[str]) -> str:
    base = re.sub(r"[^\w\s-]", "", str(label).lower())
    base = re.sub(r"[-\s]+", "_", base).strip("_")[:60] or "segment"
    key = base
    n = 2
    while key in used:
        key = f"{base}_{n}"
        n += 1
    used.add(key)
    return key


def segment_defs_from_column(df, column: str, row_get) -> dict[str, str]:
    """Build segment key → answer label from unique values in a mapped column."""
    seen: set[str] = set()
    defs: dict[str, str] = {}
    for idx in range(len(df)):
        raw = row_get(df.iloc[idx], column)
        if raw is None:
            continue
        label = str(raw).strip()
        if not label or label.lower() in ("nan", "none", "n/a"):
            continue
        if label in defs.values():
            continue
        key = _slug_key(label, seen)
        defs[key] = label
    return defs


def segment_defs_from_records(records: list[dict], field: str = "usage_context") -> dict[str, str]:
    seen: set[str] = set()
    defs: dict[str, str] = {}
    for rec in records:
        label = str(rec.get(field) or "").strip()
        if not label:
            continue
        if label in defs.values():
            continue
        key = _slug_key(label, seen)
        defs[key] = label
    return defs


def resolve_segment_column(plan) -> str | None:
    for name in SEGMENT_FIELD_PRIORITY:
        col = plan.exact.get(name)
        if col:
            return col
    return None


def pain_source_key(column_name: str) -> str | None:
    c = column_name.lower()
    for hint, key in PAIN_SOURCE_HINTS.items():
        if hint in c:
            return key
    return None


def is_frequency_pain(pain: str) -> bool:
    sl = pain.lower().strip()
    if sl.startswith("about once"):
        return True
    if "once a quarter" in sl or "few times a year" in sl:
        return True
    if sl in {"daily", "weekly", "monthly", "rarely", "never", "often", "always"}:
        return True
    if "sometimes (" in sl or "very often" in sl or "almost daily" in sl:
        return True
    return False


def _row_pains_for_column(row, col: str, row_get, split_multi) -> list[str]:
    v = row_get(row, col)
    if v is None:
        return []
    return [p.strip() for p in split_multi(v) if p.strip()]


def _source_label(src: str, columns_for_src: list[str]) -> str:
    if columns_for_src:
        return columns_for_src[0]
    return src.replace("_", " ")


def _build_segment_output(
    segment_defs: dict[str, str],
    segment_n: dict[str, int],
    combined: dict[str, Counter],
    by_source: dict[str, dict[str, Counter]],
    values_counters: dict[str, Counter],
    top_n: int,
    pain_cols_by_source: dict[str, list[str]],
) -> dict:
    def _top(counter: Counter, n: int, *, task_only: bool = True) -> list[dict]:
        items = []
        for pain, count in counter.most_common(n * 3):
            if task_only and is_frequency_pain(pain):
                continue
            items.append({"pain": pain, "count": count})
            if len(items) >= n:
                break
        return items

    out_segments: dict = {}
    for key, label in segment_defs.items():
        n = segment_n.get(key, 0)
        sub: dict = {}
        for src in pain_cols_by_source:
            if src not in by_source.get(key, {}):
                continue
            task_only = src != "difficulties_frequency"
            sub[src] = {
                "survey_question": _source_label(src, pain_cols_by_source.get(src, [])),
                "items": _top(by_source[key][src], top_n, task_only=task_only),
            }
        out_segments[key] = {
            "label": label,
            "n": n,
            "pains": [{"pain": p, "count": c} for p, c in combined[key].most_common(top_n)],
            "pains_by_source": sub,
            "desired_outcomes": [
                {"value": v, "count": c}
                for v, c in values_counters[key].most_common(top_n)
            ],
        }
    return out_segments


def compute_segments_from_df(
    df,
    plan,
    row_get,
    split_multi,
    segment_defs: dict[str, str],
    segment_col: str,
    *,
    resolve_key=None,
    top_n: int = 6,
) -> dict:
    """Generic segment slicer: pains (combined + by question) and values (select-all)."""
    label_to_key = {label: key for key, label in segment_defs.items()}
    if resolve_key is None:
        resolve_key = lambda raw: label_to_key.get(str(raw).strip())  # noqa: E731

    pain_cols_by_source: dict[str, list[str]] = {}
    for col in plan.pain_columns:
        key = pain_source_key(col)
        if key:
            pain_cols_by_source.setdefault(key, []).append(col)

    values_col = plan.exact.get("values")
    if not values_col and "values" in plan.groups:
        block = plan.groups["values"]
        values_col = block[0] if block else None

    segment_n = {key: 0 for key in segment_defs}
    combined = {key: Counter() for key in segment_defs}
    by_source = {key: {src: Counter() for src in pain_cols_by_source} for key in segment_defs}
    values_counters = {key: Counter() for key in segment_defs}

    for idx in range(len(df)):
        row = df.iloc[idx]
        raw = row_get(row, segment_col)
        if raw is None:
            continue
        seg_key = resolve_key(raw)
        if not seg_key:
            continue
        segment_n[seg_key] += 1

        for src, cols in pain_cols_by_source.items():
            for col in cols:
                for pain in _row_pains_for_column(row, col, row_get, split_multi):
                    if src == "difficulties_frequency":
                        by_source[seg_key][src][pain] += 1
                    elif not is_frequency_pain(pain):
                        by_source[seg_key][src][pain] += 1
                        combined[seg_key][pain] += 1

        if values_col:
            for val in split_multi(row_get(row, values_col)):
                v = val.strip()
                if v:
                    values_counters[seg_key][v] += 1

    return {
        "segments": _build_segment_output(
            segment_defs,
            segment_n,
            combined,
            by_source,
            values_counters,
            top_n,
            pain_cols_by_source,
        ),
    }


def compute_segment_pains_from_df(
    df, plan, row_to_record, row_get, split_multi, top_n: int = 6, *, segment_col: str | None = None
) -> dict:
    """Pains and values per segment, using mapped segment column and answer labels from data."""
    col = segment_col or resolve_segment_column(plan)
    if not col:
        return {
            "segments": {},
            "note": "No segment column mapped. Add segment_primary (or usage_context / segment) in .column_mapping.csv.",
            "skipped": True,
        }

    segment_defs = segment_defs_from_column(df, col, row_get)
    if not segment_defs:
        return {
            "segments": {},
            "segment_column": col,
            "note": f"No segment values found in column: {col}",
            "skipped": True,
        }

    out = compute_segments_from_df(
        df, plan, row_get, split_multi, segment_defs, col, top_n=top_n
    )
    out["segment_column"] = col
    out["note"] = "Pain counts per segment value in the mapped segment column (labels from survey data)."
    return out


def compute_segment_pains_secondary_from_df(
    df, plan, row_get, split_multi, top_n: int = 6
) -> dict:
    """Optional second segmentation dimension (map segment_secondary in column mapping)."""
    col = plan.exact.get("segment_secondary")
    if not col:
        return {
            "segments": {},
            "note": "segment_secondary not mapped — skipped.",
            "skipped": True,
        }
    out = compute_segment_pains_from_df(
        df, plan, None, row_get, split_multi, top_n=top_n, segment_col=col
    )
    out["segment_dimension"] = "segment_secondary"
    return out


def compute_segment_pains(
    records: list[dict],
    segments: dict[str, str] | None = None,
    *,
    segment_field: str = "usage_context",
    top_n: int = 8,
) -> dict:
    segments = segments or segment_defs_from_records(records, segment_field)
    if not segments:
        return {"segments": {}, "note": f"No values for field {segment_field!r} in records."}

    label_to_key = {label: key for key, label in segments.items()}
    counters: dict[str, Counter] = {key: Counter() for key in segments}
    segment_n: dict[str, int] = {key: 0 for key in segments}

    for rec in records:
        ctx = rec.get(segment_field)
        if not ctx:
            continue
        key = label_to_key.get(str(ctx).strip())
        if not key:
            continue
        segment_n[key] += 1
        for pain in rec.get("pain_points") or []:
            p = str(pain).strip()
            if not p or is_frequency_pain(p):
                continue
            counters[key][p] += 1

    out: dict = {
        "segments": {},
        "segment_field": segment_field,
        "note": "Pain counts per segment value (from record field, not pooled).",
    }
    for key, label in segments.items():
        pains = [{"pain": pain, "count": count} for pain, count in counters[key].most_common(top_n)]
        out["segments"][key] = {"label": label, "n": segment_n[key], "pains": pains}
    return out
