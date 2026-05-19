"""Compute pain-point and value distributions per survey segment."""
from __future__ import annotations

from collections import Counter

USAGE_CONTEXT_SEGMENTS: dict[str, str] = {
    "as_it_happens": "I do expenses as they happen: log them straight away or in the same week",
    "monthly_batch": "I do expenses in batches: save them up and batch process about once a month",
    "bas_tax": "I leave expenses until BAS/tax time: I catch up once quarter or even less frequently than that",
    "delegated": "I don\u2019t manage expenses: someone else handles it",
}

EMPLOYEE_SIZE_SEGMENTS: dict[str, str] = {
    "sole_trader": "Just me (sole trader)",
    "employees_2_4": "2\u20134 employees",
    "employees_5_19": "5\u201319 employees",
    "employees_20_plus": "20\u201399 employees",  # includes 100+ (n=1) when present
}

EMPLOYEE_SIZE_ALIASES: dict[str, str] = {
    "100+ employees": "employees_20_plus",
}

PAIN_SOURCE_HINTS: dict[str, str] = {
    "take the most time": "most_time_consuming",
    "hardest for you or your team": "hardest",
    "difficulties or problems with your business expenses admin": "difficulties_frequency",
}


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
    if sl in {"daily", "weekly", "monthly", "rarely", "never", "often", "always", "tax"}:
        return True
    if "sometimes (" in sl or "very often" in sl or "almost daily" in sl:
        return True
    return False


def _row_pains_for_column(row, col: str, row_get, split_multi) -> list[str]:
    v = row_get(row, col)
    if v is None:
        return []
    return [p.strip() for p in split_multi(v) if p.strip()]


def _resolve_employee_size_key(raw: str) -> str | None:
    raw = str(raw).strip()
    if not raw:
        return None
    if raw in EMPLOYEE_SIZE_ALIASES:
        return EMPLOYEE_SIZE_ALIASES[raw]
    label_to_key = {label: key for key, label in EMPLOYEE_SIZE_SEGMENTS.items()}
    return label_to_key.get(raw)


def _build_segment_output(
    segment_defs: dict[str, str],
    segment_n: dict[str, int],
    combined: dict[str, Counter],
    by_source: dict[str, dict[str, Counter]],
    values_counters: dict[str, Counter],
    top_n: int,
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
        for src in ("most_time_consuming", "hardest", "difficulties_frequency"):
            if src not in by_source.get(key, {}):
                continue
            task_only = src != "difficulties_frequency"
            sub[src] = {
                "survey_question": _source_label(src),
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
            segment_defs, segment_n, combined, by_source, values_counters, top_n
        ),
    }


def compute_segment_pains_from_df(df, plan, row_to_record, row_get, split_multi, top_n: int = 6) -> dict:
    """Usage-context segments (expense routine)."""
    ctx_col = plan.exact.get("usage_context")
    if not ctx_col:
        raise ValueError("usage_context column not mapped")
    out = compute_segments_from_df(
        df, plan, row_get, split_multi, USAGE_CONTEXT_SEGMENTS, ctx_col, top_n=top_n
    )
    out["note"] = "Pain counts per usage-context segment. Sub-lists match survey questions."
    return out


def compute_employee_size_segments_from_df(df, plan, row_get, split_multi, top_n: int = 6) -> dict:
    """Business size by number of employees — pains and desired outcomes per size band."""
    size_col = None
    for col in df.columns:
        if "size of your business" in str(col).lower():
            size_col = col
            break
    if not size_col:
        raise ValueError("Business size column not found (What is the size of your business?)")

    out = compute_segments_from_df(
        df,
        plan,
        row_get,
        split_multi,
        EMPLOYEE_SIZE_SEGMENTS,
        size_col,
        resolve_key=_resolve_employee_size_key,
        top_n=top_n,
    )
    out["note"] = (
        "Segmented by number of employees. Pains and desired outcomes are per size band only "
        "(not pooled). 100+ employees rolled into 20–99 band when present."
    )
    out["segment_dimension"] = "employee_count"
    return out


def _source_label(src: str) -> str:
    labels = {
        "most_time_consuming": "Which parts of managing expenses take the most time? (Pick up to 3)",
        "hardest": "Which of these tasks are hardest for you or your team to manage?",
        "difficulties_frequency": "How often do you have difficulties or problems with your business expenses admin?",
    }
    return labels.get(src, src)


def compute_segment_pains(records: list[dict], segments: dict[str, str] | None = None, top_n: int = 8) -> dict:
    segments = segments or USAGE_CONTEXT_SEGMENTS
    label_to_key = {label: key for key, label in segments.items()}
    counters: dict[str, Counter] = {key: Counter() for key in segments}
    segment_n: dict[str, int] = {key: 0 for key in segments}

    for rec in records:
        ctx = rec.get("usage_context")
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

    out: dict = {"segments": {}, "note": "Pain counts per usage-context segment only (not pooled)."}
    for key, label in segments.items():
        pains = [{"pain": pain, "count": count} for pain, count in counters[key].most_common(top_n)]
        out["segments"][key] = {"label": label, "n": segment_n[key], "pains": pains}
    return out
