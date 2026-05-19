"""Full employee-size segment behaviour archetypes with pains, values, and patterns."""
from __future__ import annotations

from collections import Counter

from segment_pains import (
    EMPLOYEE_SIZE_ALIASES,
    EMPLOYEE_SIZE_SEGMENTS,
    _resolve_employee_size_key,
    _row_pains_for_column,
    _source_label,
    is_frequency_pain,
    pain_source_key,
)


def _find_col(columns, substring: str) -> str | None:
    sub = substring.lower()
    for col in columns:
        if sub in str(col).lower():
            return col
    return None


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


def compute_employee_behaviour_archetype_profiles(df, plan, row_get, split_multi, top_n: int = 8) -> dict:
    columns = list(df.columns)
    size_col = _find_col(columns, "size of your business")
    if not size_col:
        raise ValueError("Business size column not found")

    extra_cols = {
        "software": plan.exact.get("software") or _find_col(columns, "accounting or bookkeeping software"),
        "admin_approach": plan.exact.get("admin_approach") or _find_col(columns, "how you manage the spending and expenses admin"),
        "usage_context": plan.exact.get("usage_context") or _find_col(columns, "how you tend to manage expenses"),
        "goals": plan.exact.get("goals") or _find_col(columns, "main focus right now"),
        "occupation": plan.exact.get("occupation") or _find_col(columns, "industry your business"),
        "transaction_volume": _find_col(columns, "how many expense transactions"),
        "accountant_frequency": plan.exact.get("accountant_frequency") or _find_col(columns, "how often do you work with an accountant"),
        "accountant_relationship": plan.exact.get("accountant_relationship") or _find_col(columns, "typically work with your accountant"),
        "admin_working_well": _find_col(columns, "how well is this working for you at the moment"),
        "monitor_spending": _find_col(columns, "how do you monitor spending"),
        "importance_monitoring": _find_col(columns, "how important is it to you to monitor business expenses"),
        "confidence_spending": _find_col(columns, "confident are you in your ability to identify"),
    }
    values_col = plan.exact.get("values") or _find_col(columns, "very important to you in an accounting software")

    pain_cols_by_source: dict[str, list[str]] = {}
    for col in plan.pain_columns:
        key = pain_source_key(col)
        if key:
            pain_cols_by_source.setdefault(key, []).append(col)

    keys = list(EMPLOYEE_SIZE_SEGMENTS.keys())
    segment_n = {k: 0 for k in keys}
    combined_pains = {k: Counter() for k in keys}
    pains_by_source = {k: {s: Counter() for s in pain_cols_by_source} for k in keys}
    values_ct = {k: Counter() for k in keys}
    patterns = {k: {field: Counter() for field in extra_cols if extra_cols[field]} for k in keys}
    software_tokens = {k: Counter() for k in keys}

    for idx in range(len(df)):
        row = df.iloc[idx]
        seg_key = _resolve_employee_size_key(row_get(row, size_col))
        if not seg_key:
            continue
        segment_n[seg_key] += 1

        for src, cols in pain_cols_by_source.items():
            for col in cols:
                for pain in _row_pains_for_column(row, col, row_get, split_multi):
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

        for field, col in extra_cols.items():
            if not col:
                continue
            v = row_get(row, col)
            if v is None:
                continue
            s = str(v).strip()
            if s:
                patterns[seg_key][field][s] += 1

        sw_col = extra_cols.get("software")
        if sw_col:
            for tool in split_multi(row_get(row, sw_col)):
                t = tool.strip()
                if t:
                    software_tokens[seg_key][t] += 1

    segments_out: dict = {}
    for key, label in EMPLOYEE_SIZE_SEGMENTS.items():
        n = segment_n[key]
        sub_pains = {}
        for src in ("most_time_consuming", "hardest", "difficulties_frequency"):
            if src in pains_by_source[key]:
                task_only = src != "difficulties_frequency"
                sub_pains[src] = {
                    "survey_question": _source_label(src),
                    "items": _top_pains(pains_by_source[key][src], top_n, task_only=task_only),
                }

        pattern_block = {}
        for field, counter in patterns[key].items():
            pattern_block[field] = _top_list(counter, 5)
        if software_tokens[key]:
            pattern_block["software_mentions"] = _top_list(software_tokens[key], 6)

        segments_out[key] = {
            "label": label,
            "n": n,
            "pains_combined": _top_pains(combined_pains[key], top_n, task_only=True),
            "pains_by_source": sub_pains,
            "desired_outcomes": _top_list(values_ct[key], top_n),
            "observed_patterns": pattern_block,
        }

    return {
        "segment_dimension": "employee_count",
        "note": "Full employee-size behaviour archetypes. All counts within band only (not pooled).",
        "segments": segments_out,
    }


def render_behaviour_archetype_markdown(data: dict) -> str:
    lines = [
        "# Phase 4 — Employee size behaviour archetypes (full)",
        "",
        "**Lead attribute:** Number of employees. **Not pooled** across bands.",
        "",
    ]
    for key, seg in data["segments"].items():
        n = seg["n"]
        lines.append(f"## {seg['label']} (n={n})")
        lines.append("")
        lines.append("### Pains — combined (any pain question)")
        lines.append("| Pain | Count | % of band |")
        lines.append("|------|------:|----------:|")
        for item in seg.get("pains_combined", [])[:8]:
            pct = round(100 * item["count"] / n, 0) if n else 0
            lines.append(f"| {item['pain']} | {item['count']} | {pct:.0f}% |")
        lines.append("")
        for src_key, title in [
            ("most_time_consuming", "Pains — most time-consuming (pick up to 3)"),
            ("hardest", "Pains — hardest tasks"),
            ("difficulties_frequency", "Difficulties — how often (frequency scale)"),
        ]:
            block = seg.get("pains_by_source", {}).get(src_key)
            if not block:
                continue
            lines.append(f"### {title}")
            lines.append(f"*{block.get('survey_question', '')}*")
            lines.append("")
            lines.append("| Item | Count |")
            lines.append("|------|------:|")
            for item in block.get("items", [])[:8]:
                label = item.get("pain") or item.get("label", "")
                lines.append(f"| {label} | {item['count']} |")
            lines.append("")
        lines.append("### Desired outcomes (values in accounting software)")
        lines.append("| Value | Count | % of band |")
        lines.append("|-------|------:|----------:|")
        for item in seg.get("desired_outcomes", [])[:8]:
            pct = round(100 * item["count"] / n, 0) if n else 0
            lines.append(f"| {item['label']} | {item['count']} | {pct:.0f}% |")
        lines.append("")
        lines.append("### Other observed patterns (this band)")
        pat = seg.get("observed_patterns", {})
        for field, items in pat.items():
            if not items:
                continue
            title = field.replace("_", " ").title()
            lines.append(f"**{title}:** " + ", ".join(f"{x['label']} ({x['count']})" for x in items[:4]))
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)
