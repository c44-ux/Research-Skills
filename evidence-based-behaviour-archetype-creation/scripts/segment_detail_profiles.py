"""Rich segment profiles: pains, values, and mapped field distributions (domain-neutral)."""
from __future__ import annotations

from collections import Counter

from segment_pains import (
    _row_pains_for_column,
    _source_label,
    is_frequency_pain,
    pain_source_key,
    resolve_segment_column,
    segment_defs_from_column,
)


def _top_list(counter: Counter, n: int) -> list[dict]:
    return [{"label": k, "count": c} for k, c in counter.most_common(n)]


def _top_pains(counter: Counter, n: int, *, task_only: bool = True) -> list[dict]:
    items = []
    for pain, count in counter.most_common(n * 4):
        if task_only and is_frequency_pain(pain):
            continue
        items.append({"pain": pain, "count": count})
        if len(items) >= n:
            break
    return items


def _profile_fields_from_plan(plan) -> dict[str, str]:
    """Mapped exact fields to include in per-segment pattern counts (excluding segment keys)."""
    skip = {
        "segment_primary",
        "segment_secondary",
        "segment",
        "task_narrative",
        "routine_text",
        "quotes",
    }
    return {k: v for k, v in plan.exact.items() if k not in skip and v}


def compute_segment_detail_profiles(
    df, plan, row_get, split_multi, *, segment_col: str | None = None, top_n: int = 8
) -> dict:
    col = segment_col or resolve_segment_column(plan)
    if not col:
        raise ValueError(
            "Map a segment column in .column_mapping.csv "
            "(segment_primary, segment_secondary, usage_context, or segment)."
        )

    segment_defs = segment_defs_from_column(df, col, row_get)
    if not segment_defs:
        raise ValueError(f"No segment values in column: {col}")

    label_to_key = {label: key for key, label in segment_defs.items()}
    extra_cols = _profile_fields_from_plan(plan)

    pain_cols_by_source: dict[str, list[str]] = {}
    for c in plan.pain_columns:
        key = pain_source_key(c)
        if key:
            pain_cols_by_source.setdefault(key, []).append(c)

    values_col = plan.exact.get("values")
    if not values_col and "values" in plan.groups:
        block = plan.groups["values"]
        values_col = block[0] if block else None

    keys = list(segment_defs.keys())
    segment_n = {k: 0 for k in keys}
    combined_pains = {k: Counter() for k in keys}
    pains_by_source = {k: {s: Counter() for s in pain_cols_by_source} for k in keys}
    values_ct = {k: Counter() for k in keys}
    patterns = {k: {field: Counter() for field in extra_cols} for k in keys}

    for idx in range(len(df)):
        row = df.iloc[idx]
        raw = row_get(row, col)
        if raw is None:
            continue
        seg_key = label_to_key.get(str(raw).strip())
        if not seg_key:
            continue
        segment_n[seg_key] += 1

        for src, cols in pain_cols_by_source.items():
            for pain_col in cols:
                for pain in _row_pains_for_column(row, pain_col, row_get, split_multi):
                    if src == "difficulties_frequency":
                        pains_by_source[seg_key][src][pain] += 1
                    elif not is_frequency_pain(pain):
                        pains_by_source[seg_key][src][pain] += 1
                        combined_pains[seg_key][pain] += 1

        if values_col:
            for val in split_multi(row_get(row, values_col)):
                v = val.strip()
                if v:
                    values_ct[seg_key][v] += 1

        for field, pain_col in extra_cols.items():
            v = row_get(row, pain_col)
            if v is None:
                continue
            s = str(v).strip()
            if s:
                patterns[seg_key][field][s] += 1

    segments_out: dict = {}
    for key, label in segment_defs.items():
        n = segment_n[key]
        sub_pains = {}
        for src, cols in pain_cols_by_source.items():
            task_only = src != "difficulties_frequency"
            sub_pains[src] = {
                "survey_question": _source_label(src, cols),
                "items": _top_pains(pains_by_source[key][src], top_n, task_only=task_only),
            }

        pattern_block = {
            field: _top_list(counter, 5)
            for field, counter in patterns[key].items()
            if counter
        }

        segments_out[key] = {
            "label": label,
            "n": n,
            "pains_combined": _top_pains(combined_pains[key], top_n, task_only=True),
            "pains_by_source": sub_pains,
            "desired_outcomes": _top_list(values_ct[key], top_n),
            "observed_patterns": pattern_block,
        }

    return {
        "segment_column": col,
        "note": "Segment detail profiles from mapped columns only (counts within each segment value).",
        "segments": segments_out,
    }


def render_segment_detail_markdown(data: dict) -> str:
    lines = [
        "# Segment behaviour archetypes (detail)",
        "",
        f"**Segment column:** `{data.get('segment_column', '')}`",
        "",
    ]
    for _key, seg in data["segments"].items():
        n = seg["n"]
        lines.append(f"## {seg['label']} (n={n})")
        lines.append("")
        lines.append("### Pains — combined")
        lines.append("| Pain | Count | % of segment |")
        lines.append("|------|------:|-------------:|")
        for item in seg.get("pains_combined", [])[:8]:
            pct = round(100 * item["count"] / n, 0) if n else 0
            lines.append(f"| {item['pain']} | {item['count']} | {pct:.0f}% |")
        lines.append("")
        for src_key, block in seg.get("pains_by_source", {}).items():
            if not block.get("items"):
                continue
            title = src_key.replace("_", " ").title()
            lines.append(f"### Pains — {title}")
            lines.append(f"*{block.get('survey_question', '')}*")
            lines.append("")
            lines.append("| Item | Count |")
            lines.append("|------|------:|")
            for item in block.get("items", [])[:8]:
                label = item.get("pain") or item.get("label", "")
                lines.append(f"| {label} | {item['count']} |")
            lines.append("")
        lines.append("### Stated values / priorities")
        lines.append("| Value | Count | % of segment |")
        lines.append("|-------|------:|-------------:|")
        for item in seg.get("desired_outcomes", [])[:8]:
            pct = round(100 * item["count"] / n, 0) if n else 0
            lines.append(f"| {item['label']} | {item['count']} | {pct:.0f}% |")
        lines.append("")
        lines.append("### Other mapped fields (this segment)")
        pat = seg.get("observed_patterns", {})
        for field, items in pat.items():
            if not items:
                continue
            title = field.replace("_", " ").title()
            lines.append(
                f"**{title}:** "
                + ", ".join(f"{x['label']} ({x['count']})" for x in items[:4])
            )
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)
