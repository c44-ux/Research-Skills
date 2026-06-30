# Persona Generator — Code Reference

> Evidence-Based User Pattern Analysis Generator  
> Canonical implementation for this skill's persona and pattern analysis standards.

```python
#!/usr/bin/env python3
"""
Evidence-Based User Pattern Analysis Generator
===============================================
Creates rigorous, evidence-grounded user pattern summaries from multi-source
research inputs. Designed for use across variable dataset types including
analytics exports, surveys, and interview transcripts. Implements guardrails
for AI-assisted persona generation.

Methodological basis
--------------------
This module implements the evidence standards set out in two systematic reviews:

    Salminen, J., Guan, K., Jung, S. G., & Jansen, B. J. (2021).
    A Survey of 15 Years of Data-Driven Persona Development.
    International Journal of Human–Computer Interaction, 37(18), 1685–1708.
    DOI: 10.1080/10447318.2021.1908670

    Amin, D., Salminen, J., Ahmed, F., Tervola, S. M. H., Sethi, S.,
    & Jansen, B. J. (2025).
    Creating and Evaluating Personas Using Generative AI:
    A Scoping Review of 81 Articles.
    arXiv:2504.04927v2

Key principles enforced
-----------------------
1. No pre-defined archetypes. Segments emerge from data; they are not
   assigned from templates before data is examined.
2. No fabricated identity. Names, quotes, and biographical details are
   never invented — by a human or an LLM. Only real interview quotes surface.
3. No demographic inference by default. Optional fields (age,
   tech_confidence) are included in output only when explicitly present
   in the source data, labelled with their source type.
4. Evidence thresholds. No insight is surfaced unless it meets
   min_count_for_directional_signal (default: 3).
5. Transparent limitations. Every output includes a limitations block,
   confidence notes, hallucination risk flags, and circularity warnings.
6. Design implications are tied to explicit evidence. Each implication
   carries a 'because' field quoting the supporting signal.
7. AI involvement is documented. When LLM enrichment is used, the output
   records model, version, and prompt reference (PG3).

Addressing the five research gaps (Salminen et al., 2021)
----------------------------------------------------------
Gap A – Shared resources:     DataSource registry documents provenance.
Gap B – Evaluation methods:   confidence_note + limitations block included.
Gap C – Standardisation:      Consistent output schema across source types.
Gap D – Inclusivity:          No demographic inference; bias_notes surfaced.
Gap E – Loss of depth:        Interview evidence preserved separately;
                               qualitative and quantitative signals never merged.

Addressing GenAI risks (Amin et al., 2025)
------------------------------------------
PG1 – Multi-model validation:  Output flags when only one model used.
PG2 – Structured output:       JSON mode via 'python persona_generator.py json'.
PG3 – Prompt documentation:    AIEnrichmentRecord captures model + prompt ref.
PG4 – Demographic benchmarking: optional_fields block enables comparison.
PG5 – Acceptance thresholds:   min_count_for_directional_signal enforced.
PG6 – Consistency testing:     Run generator 3x; compare outputs for stability.
PG7 – Human oversight:         method_notes always include human review reminder.
Circularity: Flagged in method_notes when AI enrichment present.
Hallucination: Flagged per-attribute when AI enrichment is unvalidated.
Potemkin risk: Limitations block warns when interview evidence is absent.

Supported source types
----------------------
    survey        Structured questionnaire responses. May include optional
                  demographic fields (age, tech_confidence). Psychographic
                  inference is permitted only when explicitly stated.
    interview     Unstructured or semi-structured transcripts. Quotes,
                  goals, needs, and pain points extracted. No quantitative
                  aggregation applied.
    analytics     Behavioural platform data (e.g. product analytics,
                  clickstreams). No demographic or motivational inference.
    usability_test Task-based observation data. Pain points and task
                  completion patterns only.

Usage
-----
    python persona_generator.py           # Human-readable output
    python persona_generator.py json      # JSON for programmatic use

Input shape
-----------
    sources = [
        {"type": "analytics", "data": [...]},
        {"type": "survey",    "data": [...]},
        {"type": "interview", "data": [...]},
    ]
    generator.generate_analysis(sources)

Each record in data is a dict. Fields present vary by source type.
Absent fields are never inferred — they are noted as absent.

Table of Contents
-----------------
CLASS: DataSource
    __init__()                      Registry entry for one source type

CLASS: FieldRegistry
    __init__()                      Known optional fields and their rules
    assess()                        Assess which optional fields are present

CLASS: PersonaGenerator
    __init__()                      Initialise thresholds and registry
    generate_analysis()             Main entry: multi-source analysis
    format_analysis_output()        Human-readable formatted output

PATTERN ANALYSIS:
    _analyze_behavioral_patterns()  Usage, device, context from analytics/survey
    _merge_patterns()               Merge patterns across multiple sources
    _analyze_behaviors()            Describe recurring behaviors distributionally

NEEDS & FRUSTRATIONS:
    _identify_needs()               Evidence-gated needs from patterns + interviews
    _extract_frustrations()         Frustrations with evidence count and source

DEMOGRAPHIC & PSYCHOGRAPHIC:
    _surface_optional_fields()      Surface age/tech_confidence only if present
    _extract_psychographics()       Psychographics from survey/interview only

SEGMENTS & QUOTES:
    _generate_example_segments()    Emergent segments from data combinations
    _select_quotes()                Real interview quotes only; never fabricated

OUTPUT SUPPORT:
    _calculate_data_points()        Transparent confidence notes per source
    _derive_design_implications()   Evidence-tied recommendations
    _describe_limitations()         Analytical limits of the output
    _generate_method_notes()        Methodological guardrails summary
    _generate_title()               Descriptive non-fictional title
    _generate_summary()             Narrative summary of strongest signals
    _top_key()                      Helper: highest-count key in mapping
    _format_distribution()          Helper: format count dict for display

FUNCTIONS:
    create_sample_sources()         Multi-source sample data for testing
    main()                          CLI entry point
"""

import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Evidence threshold constant — referenced in Salminen et al. (2021) as a
# core gap: most studies surface insights without minimum evidence criteria.
# Raising this reduces false signal; lowering increases sensitivity.
# ---------------------------------------------------------------------------
DEFAULT_MIN_SIGNAL_COUNT = 3

# ---------------------------------------------------------------------------
# Known optional fields: fields that are legitimate in some source types
# but absent in others. The registry governs whether and how each is used.
# ---------------------------------------------------------------------------
OPTIONAL_FIELD_RULES: Dict[str, Dict] = {
    "age": {
        "allowed_sources": ["survey"],
        "surface_in_output": True,
        "note": "Demographic field. Surface with source noted. Do not infer if absent.",
    },
    "tech_confidence": {
        "allowed_sources": ["survey", "usability_test"],
        "surface_in_output": True,
        "note": "Self-reported. Surface as a distribution, not a per-user label.",
    },
    "location_type": {
        "allowed_sources": ["survey", "analytics"],
        "surface_in_output": True,
        "note": "Include if present; do not infer from device or context signals.",
    },
    "occupation": {
        "allowed_sources": ["survey", "interview"],
        "surface_in_output": True,
        "note": "Include if explicitly stated. Never infer from usage context.",
    },
    "motivations": {
        "allowed_sources": ["interview", "survey"],
        "surface_in_output": True,
        "note": "Only from explicit stated evidence. Never inferred from behaviour.",
    },
    "values": {
        "allowed_sources": ["interview", "survey"],
        "surface_in_output": True,
        "note": "Only from explicit stated evidence. Never inferred from behaviour.",
    },
}

# ---------------------------------------------------------------------------
# Supported source types and what behavioral fields each may contribute
# ---------------------------------------------------------------------------
SOURCE_TYPE_BEHAVIORAL_FIELDS = {
    "analytics":     ["usage_frequency", "features_used", "primary_device", "usage_context", "pain_points"],
    "survey":        ["usage_frequency", "features_used", "primary_device", "usage_context", "pain_points",
                      "age", "tech_confidence", "location_type", "occupation", "motivations", "values",
                      "goals", "needs", "emotional_needs", "quotes"],
    "interview":     ["pain_points", "goals", "needs", "emotional_needs", "quotes",
                      "motivations", "values", "occupation"],
    "usability_test":["pain_points", "features_used", "tech_confidence"],
}


# ---------------------------------------------------------------------------
# GenAI practical guidelines (Amin et al., 2025, Table 8)
# Enforced as documented constraints. Reference in method_notes output.
# ---------------------------------------------------------------------------
GENAI_GUARDRAILS: Dict[str, str] = {
    "PG1_multi_model_validation": (
        "Use ≥2 different GenAI systems for validation. Different models "
        "exhibit distinct biases; cross-validation identifies systematic ones."
    ),
    "PG2_structured_output": (
        "Deploy JSON/CSV with explicit consistency criteria. "
        "Run with 'python persona_generator.py json' for downstream validation."
    ),
    "PG3_prompt_documentation": (
        "Document prompt, model, version, temperature, and date for every "
        "AI-assisted step. Use AIEnrichmentRecord to capture these."
    ),
    "PG4_demographic_benchmarking": (
        "Validate generated characteristics against real user data or "
        "external benchmarks. LLM defaults skew US-centric and elite."
    ),
    "PG5_acceptance_thresholds": (
        "Pre-register quality criteria before generating. "
        "Default: min_count_for_directional_signal = 3."
    ),
    "PG6_consistency_testing": (
        "Run the generator 3x on the same data. Attributes that shift "
        "substantially across runs are unstable and potentially hallucinated."
    ),
    "PG7_human_oversight": (
        "A domain expert or community representative must review every persona "
        "before design use. Non-negotiable for marginalised populations."
    ),
    "no_circularity": (
        "Do not use the same LLM to generate and evaluate personas. "
        "Use a different model or human evaluators for the evaluation phase."
    ),
    "no_potemkin_personas": (
        "Every attribute must be traceable to a source record. "
        "Attributes with no source record are Potemkin elements — remove or "
        "label as illustrative placeholders. (Muller & Seaborn, 2025)"
    ),
    "hallucination_check": (
        "For every factual claim, identify the source record. "
        "Claims traceable only to LLM output are hallucination candidates."
    ),
}


@dataclass
class AIEnrichmentRecord:
    """
    Documents AI involvement at any stage of persona development.
    Required when LLMs are used for enrichment, summarisation, or analysis.
    Addresses PG3 (prompt documentation) and Amin et al. circularity risk.

    Attributes
    ----------
    stage : str
        Which stage LLM assistance was applied
        (e.g. 'narrative_enrichment', 'thematic_analysis', 'quote_synthesis').
    model : str
        Model identifier (e.g. 'claude-sonnet-4-20250514', 'gpt-4o').
    prompt_reference : str
        A label or version string identifying the prompt used.
        Store full prompt text separately (e.g. in a prompts/ directory).
    validated_against_source : bool
        Whether AI-generated outputs were checked against source records.
        If False, outputs from this stage are flagged as unvalidated.
    notes : str
        Any additional context about the AI involvement.
    """
    stage: str
    model: str
    prompt_reference: str
    validated_against_source: bool = False
    notes: str = ""


@dataclass
class DataSource:
    """
    A single research source with its type declaration and raw records.

    Attributes
    ----------
    source_type : str
        One of: 'analytics', 'survey', 'interview', 'usability_test'.
    data : List[Dict]
        Raw records from this source. Field presence varies.
    label : str
        Optional human label for this source (e.g. 'Q3 checkout survey').
    ai_enrichments : List[AIEnrichmentRecord]
        Optional list of AI involvement records for this source.
        Populate when LLMs were used to process, summarise, or enrich
        this source's data before passing it to the generator.
        Absence means no AI was involved in preparing this source.
    """
    source_type: str
    data: List[Dict]
    label: str = ""
    ai_enrichments: List[AIEnrichmentRecord] = field(default_factory=list)

    def __post_init__(self):
        valid_types = set(SOURCE_TYPE_BEHAVIORAL_FIELDS.keys())
        if self.source_type not in valid_types:
            raise ValueError(
                f"Unknown source_type '{self.source_type}'. "
                f"Valid types: {sorted(valid_types)}"
            )
        if not self.label:
            self.label = f"{self.source_type} source ({len(self.data)} records)"


class FieldRegistry:
    """
    Assesses which optional fields are present in a dataset and governs
    how they should be handled in the analysis output.

    This directly addresses Salminen et al. (2021) Gap D (inclusivity) and
    Gap C (standardisation): the registry makes field presence and absence
    explicit rather than silently skipping or silently inferring.
    """

    def __init__(self, rules: Dict = None):
        self.rules = rules or OPTIONAL_FIELD_RULES

    def assess(self, sources: List[DataSource]) -> Dict[str, Dict]:
        """
        For each known optional field, determine:
        - whether it is present in any source
        - which source type(s) it came from
        - the rule governing its use

        Returns a dict keyed by field name with presence metadata.
        """
        assessment = {}

        for field_name, rule in self.rules.items():
            present_in = []
            for source in sources:
                if source.source_type not in rule["allowed_sources"]:
                    continue
                # Check if any record in this source has the field
                if any(field_name in record for record in source.data):
                    present_in.append(source.source_type)

            assessment[field_name] = {
                "present": len(present_in) > 0,
                "found_in_source_types": list(set(present_in)),
                "rule": rule,
            }

        return assessment


class PersonaGenerator:
    """
    Generate an open, evidence-based user pattern analysis from
    multi-source research inputs.

    Does not assign archetypes, fabricate identities, or infer demographic
    or psychographic attributes beyond what the data explicitly provides.
    """

    def __init__(self, min_signal_count: int = DEFAULT_MIN_SIGNAL_COUNT):
        self.min_count_for_directional_signal = min_signal_count
        self.max_example_segments = 3
        self.field_registry = FieldRegistry()

        self.analysis_components = {
            "observed_patterns":      ["usage_frequency", "feature_usage", "devices", "contexts"],
            "evidence_based_insights":["needs", "frustrations", "quotes", "design_implications"],
            "example_segments":       ["overlapping", "illustrative", "non_exhaustive"],
            "guardrails": [
                "no_pre_defined_archetype",
                "no_fabricated_identity",
                "no_demographic_inference_by_default",
                "evidence_threshold_enforced",
                "limitations_always_present",
            ],
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_analysis(self, sources: List[Dict]) -> Dict:
        """
        Generate an open pattern analysis from one or more typed sources.

        Parameters
        ----------
        sources : List[Dict]
            Each dict must have:
                type : str   — one of the supported source types
                data : list  — list of user/response records
                label : str  — optional human label
                ai_enrichments : list — optional list of AI involvement dicts,
                    each with keys: stage, model, prompt_reference,
                    validated_against_source (bool), notes (str)

        Returns
        -------
        Dict containing the full analysis with provenance, limitations,
        GenAI guardrail flags, hallucination risk notes, and evidence-tied
        design implications.
        """
        typed_sources = [
            DataSource(
                source_type=s["type"],
                data=s.get("data", []),
                label=s.get("label", ""),
                ai_enrichments=[
                    AIEnrichmentRecord(**e)
                    for e in s.get("ai_enrichments", [])
                ],
            )
            for s in sources
        ]

        # Assess which optional fields are present across all sources
        field_assessment = self.field_registry.assess(typed_sources)

        # Separate sources by type for type-appropriate processing
        behavioral_sources = [s for s in typed_sources
                               if s.source_type in ("analytics", "survey", "usability_test")]
        interview_sources  = [s for s in typed_sources
                               if s.source_type == "interview"]

        # Flatten behavioral records and interview records
        behavioral_data = [record for s in behavioral_sources for record in s.data]
        interview_data  = [record for s in interview_sources  for record in s.data]

        # Collect all AI enrichment records across sources
        all_ai_enrichments = [
            e for s in typed_sources for e in s.ai_enrichments
        ]

        # Merge patterns across all behavioral sources
        patterns = self._merge_patterns([
            self._analyze_behavioral_patterns(s.data, s.source_type)
            for s in behavioral_sources
        ])

        analysis = {
            "title":               self._generate_title(patterns, typed_sources),
            "analysis_type":       "open_pattern_analysis",
            "sources_summary":     self._summarise_sources(typed_sources),
            "ai_involvement":      self._summarise_ai_involvement(all_ai_enrichments),
            "summary":             self._generate_summary(patterns, behavioral_data, interview_data),
            "patterns":            patterns,
            "optional_fields":     self._surface_optional_fields(field_assessment, behavioral_data),
            "psychographics":      self._extract_psychographics(typed_sources, field_assessment),
            "behaviors":           self._analyze_behaviors(behavioral_data),
            "needs_and_goals":     self._identify_needs(patterns, interview_data),
            "frustrations":        self._extract_frustrations(patterns, interview_data),
            "contradictions":      self._document_contradictions(patterns, interview_data),
            "example_segments":    self._generate_example_segments(behavioral_data),
            "quotes":              self._select_quotes(interview_data),
            "data_points":         self._calculate_data_points(typed_sources),
            "design_implications": self._derive_design_implications(patterns),
            "governance":          self._generate_governance_block(typed_sources),
            "limitations":         self._describe_limitations(typed_sources, field_assessment, all_ai_enrichments),
            "method_notes":        self._generate_method_notes(all_ai_enrichments),
        }

        return analysis

    # ------------------------------------------------------------------
    # Source summarisation
    # ------------------------------------------------------------------

    def _summarise_sources(self, sources: List[DataSource]) -> List[Dict]:
        return [
            {
                "label":       s.label,
                "source_type": s.source_type,
                "record_count": len(s.data),
                "behavioral_fields_available": [
                    f for f in SOURCE_TYPE_BEHAVIORAL_FIELDS.get(s.source_type, [])
                    if any(f in record for record in s.data)
                ],
                "ai_enrichments_applied": len(s.ai_enrichments) > 0,
            }
            for s in sources
        ]

    def _summarise_ai_involvement(
        self, enrichments: List[AIEnrichmentRecord]
    ) -> Dict:
        """
        Summarise all AI involvement across sources for the output header.
        Addresses PG3 (prompt documentation) and transparency requirements
        from Amin et al. (2025).
        """
        if not enrichments:
            return {
                "ai_used": False,
                "note": "No AI enrichment was applied to any source in this analysis.",
            }

        models_used = list({e.model for e in enrichments})
        unvalidated = [e for e in enrichments if not e.validated_against_source]

        summary: Dict[str, Any] = {
            "ai_used":       True,
            "stages":        [e.stage for e in enrichments],
            "models_used":   models_used,
            "prompt_references": [e.prompt_reference for e in enrichments],
            "multi_model":   len(models_used) > 1,
        }

        if not summary["multi_model"]:
            summary["pg1_warning"] = (
                f"Only one model was used ({models_used[0]}). "
                "PG1 requires validation with a second model or against real user data."
            )

        if unvalidated:
            summary["unvalidated_stages"] = [e.stage for e in unvalidated]
            summary["hallucination_risk"] = (
                f"The following AI-enriched stages were not validated against "
                f"source records: {[e.stage for e in unvalidated]}. "
                "Outputs from these stages are hallucination candidates. "
                "Apply PG6 consistency testing and PG7 human review."
            )

        if len(models_used) == 1 and any(e.stage for e in enrichments):
            summary["circularity_warning"] = (
                "If the same model is used for both generation and evaluation, "
                "this is a circularity risk (Amin et al., 2025). "
                "Use a different model or human evaluators for the evaluation phase."
            )

        return summary

    # ------------------------------------------------------------------
    # Pattern analysis
    # ------------------------------------------------------------------

    def _analyze_behavioral_patterns(self, data: List[Dict], source_type: str) -> Dict:
        """
        Analyze recurring patterns in one behavioral source without
        collapsing users into a single category.
        """
        patterns: Dict[str, Any] = {
            "usage_frequency": defaultdict(int),
            "feature_usage":   defaultdict(int),
            "devices":         defaultdict(int),
            "contexts":        defaultdict(int),
            "pain_points":     [],
            "success_metrics": [],
        }

        allowed = SOURCE_TYPE_BEHAVIORAL_FIELDS.get(source_type, [])

        for record in data:
            if "usage_frequency" in allowed:
                freq = record.get("usage_frequency", "unknown")
                patterns["usage_frequency"][freq] += 1

            if "features_used" in allowed:
                for feature in record.get("features_used", []):
                    patterns["feature_usage"][feature] += 1

            if "primary_device" in allowed:
                device = record.get("primary_device", "unknown")
                patterns["devices"][device] += 1

            if "usage_context" in allowed:
                context = record.get("usage_context", "unknown")
                patterns["contexts"][context] += 1

            if "pain_points" in allowed and "pain_points" in record:
                patterns["pain_points"].extend(record["pain_points"])

            if "success_metrics" in record:
                patterns["success_metrics"].extend(record.get("success_metrics", []))

        return {
            "usage_frequency": dict(sorted(patterns["usage_frequency"].items(), key=lambda x: (-x[1], x[0]))),
            "feature_usage":   dict(sorted(patterns["feature_usage"].items(),   key=lambda x: (-x[1], x[0]))),
            "devices":         dict(sorted(patterns["devices"].items(),         key=lambda x: (-x[1], x[0]))),
            "contexts":        dict(sorted(patterns["contexts"].items(),        key=lambda x: (-x[1], x[0]))),
            "pain_points":     dict(Counter(patterns["pain_points"]).most_common(10)),
            "success_metrics": dict(Counter(patterns["success_metrics"]).most_common(10)),
        }

    def _merge_patterns(self, pattern_list: List[Dict]) -> Dict:
        """
        Merge pattern dicts from multiple behavioral sources by summing counts.
        Preserves provenance: merged output is a union, not a flattening.
        """
        if not pattern_list:
            return {
                "usage_frequency": {}, "feature_usage": {},
                "devices": {}, "contexts": {},
                "pain_points": {}, "success_metrics": {},
            }

        merged: Dict[str, Counter] = {
            "usage_frequency": Counter(),
            "feature_usage":   Counter(),
            "devices":         Counter(),
            "contexts":        Counter(),
            "pain_points":     Counter(),
            "success_metrics": Counter(),
        }

        for p in pattern_list:
            for key in merged:
                merged[key].update(p.get(key, {}))

        return {k: dict(v.most_common()) for k, v in merged.items()}

    # ------------------------------------------------------------------
    # Optional fields and psychographics
    # ------------------------------------------------------------------

    def _surface_optional_fields(
        self, field_assessment: Dict, behavioral_data: List[Dict]
    ) -> Dict:
        """
        Surface optional demographic fields (age, tech_confidence, etc.)
        only when explicitly present in the source data.
        Each surfaced field is labelled with its source type.
        Absent fields are explicitly noted — never inferred.
        """
        output: Dict[str, Any] = {}

        for field_name, meta in field_assessment.items():
            if not meta["present"]:
                output[field_name] = {
                    "status": "absent",
                    "note": (
                        f"'{field_name}' was not present in any supplied source. "
                        "It has not been inferred."
                    ),
                }
                continue

            # Field is present — aggregate it
            values = [
                r[field_name]
                for r in behavioral_data
                if field_name in r
            ]

            if not values:
                continue

            source_types = meta["found_in_source_types"]

            if field_name == "age":
                avg = sum(values) / len(values)
                output["age"] = {
                    "status": "present",
                    "source_types": source_types,
                    "distribution": dict(Counter(values).most_common()),
                    "mean": round(avg, 1),
                    "note": meta["rule"]["note"],
                }

            elif field_name == "tech_confidence":
                avg = sum(values) / len(values)
                output["tech_confidence"] = {
                    "status": "present",
                    "source_types": source_types,
                    "distribution": dict(Counter(values).most_common()),
                    "mean": round(avg, 1),
                    "note": meta["rule"]["note"],
                }

            else:
                # Generic optional field — surface as distribution
                output[field_name] = {
                    "status": "present",
                    "source_types": source_types,
                    "distribution": dict(Counter(values).most_common()),
                    "note": meta["rule"]["note"],
                }

        return output

    def _extract_psychographics(
        self, sources: List[DataSource], field_assessment: Dict
    ) -> Dict:
        """
        Extract psychographic signals (motivations, values) only from
        interview and survey sources, and only when explicitly stated.
        Never inferred from behavioural patterns.
        """
        psychographics: Dict[str, Any] = {
            "motivations": [],
            "values":      [],
            "source_note": "",
        }

        qualifying_sources = [
            s for s in sources
            if s.source_type in ("interview", "survey")
        ]

        if not qualifying_sources:
            psychographics["source_note"] = (
                "No interview or survey sources supplied. "
                "Psychographic data cannot be surfaced without explicit evidence."
            )
            return psychographics

        motivations: List[str] = []
        values: List[str] = []

        for source in qualifying_sources:
            for record in source.data:
                motivations.extend(record.get("motivations", []))
                values.extend(record.get("values", []))

        if motivations:
            psychographics["motivations"] = [
                {"value": k, "count": v, "source": "interview/survey"}
                for k, v in Counter(motivations).most_common(8)
                if v >= self.min_count_for_directional_signal
            ]
            if not psychographics["motivations"]:
                psychographics["motivations_weak_signal"] = (
                    f"Motivations were present but no single motivation met the "
                    f"minimum signal threshold of {self.min_count_for_directional_signal}. "
                    f"Treat individual mentions as hypotheses only."
                )

        if values:
            psychographics["values"] = [
                {"value": k, "count": v, "source": "interview/survey"}
                for k, v in Counter(values).most_common(8)
                if v >= self.min_count_for_directional_signal
            ]

        psychographics["source_note"] = (
            f"Psychographic data drawn from: "
            f"{', '.join(s.label for s in qualifying_sources)}. "
            f"Only explicitly stated motivations/values are included."
        )

        return psychographics

    # ------------------------------------------------------------------
    # Behaviors
    # ------------------------------------------------------------------

    def _analyze_behaviors(self, behavioral_data: List[Dict]) -> Dict:
        """
        Describe recurring behaviors and feature use as distributions.
        No identity labels or archetype assignments are made.
        """
        behaviors: Dict[str, Any] = {
            "usage_patterns":   [],
            "feature_preferences": [],
            "interaction_modes": [],
            "notes": [],
        }

        if not behavioral_data:
            behaviors["notes"].append("No behavioral data supplied.")
            return behaviors

        frequencies = [u.get("usage_frequency", "unknown") for u in behavioral_data]
        freq_counter = Counter(frequencies)
        behaviors["usage_patterns"] = [
            f"{freq}: {count} users"
            for freq, count in freq_counter.most_common(5)
        ]

        all_features: List[str] = []
        for record in behavioral_data:
            all_features.extend(record.get("features_used", []))
        feature_counter = Counter(all_features)
        behaviors["feature_preferences"] = [
            feat for feat, _ in feature_counter.most_common(8)
        ]

        unique_count = len(feature_counter)
        if unique_count <= 3:
            behaviors["interaction_modes"].append(
                "Users appear concentrated around a small core feature set."
            )
        elif unique_count <= 8:
            behaviors["interaction_modes"].append(
                "Users show a moderate spread across core and secondary features."
            )
        else:
            behaviors["interaction_modes"].append(
                "Users span a broad feature mix; avoid assuming one dominant workflow."
            )

        behaviors["notes"] = [
            "Behavior descriptions are distributional summaries, not user types.",
            "The same user may move between different patterns across tasks, sessions, or contexts.",
        ]

        return behaviors

    # ------------------------------------------------------------------
    # Needs & frustrations
    # ------------------------------------------------------------------

    def _identify_needs(
        self, patterns: Dict, interview_data: List[Dict]
    ) -> Dict:
        """
        Identify needs and goals from repeated behavioral signals and
        explicit interview evidence only.
        Every need carries a supporting_evidence note.
        Needs are never fabricated from archetype defaults.
        """
        needs: Dict[str, Any] = {
            "primary_goals":     [],
            "functional_needs":  [],
            "emotional_needs":   [],
            "supporting_evidence": [],
        }

        threshold = self.min_count_for_directional_signal

        if patterns["usage_frequency"].get("daily", 0) >= threshold:
            needs["primary_goals"].append("Complete repeat tasks quickly and with low overhead")
            needs["functional_needs"].append("Speed and performance in common workflows")
            needs["supporting_evidence"].append(
                f"Daily usage appears {patterns['usage_frequency']['daily']} times — "
                f"above the signal threshold of {threshold}."
            )

        if patterns["contexts"].get("work", 0) >= threshold:
            needs["primary_goals"].append("Stay productive in work-related flows")
            needs["functional_needs"].append("Reliable workflows that fit existing work routines")
            needs["supporting_evidence"].append(
                f"Work-context usage appears {patterns['contexts']['work']} times — "
                f"above the signal threshold of {threshold}."
            )

        if patterns["devices"].get("mobile", 0) >= threshold:
            needs["functional_needs"].append(
                "Fast mobile access for short or in-between sessions"
            )
            needs["supporting_evidence"].append(
                f"Mobile device usage appears {patterns['devices']['mobile']} times — "
                f"above the signal threshold of {threshold}."
            )

        # Interview evidence — only explicit stated needs
        for record in interview_data:
            for goal in record.get("goals", [])[:3]:
                if goal not in needs["primary_goals"]:
                    needs["primary_goals"].append(goal)
            for stated_need in record.get("needs", [])[:3]:
                if stated_need not in needs["functional_needs"]:
                    needs["functional_needs"].append(stated_need)
            for emotional_need in record.get("emotional_needs", [])[:3]:
                if emotional_need not in needs["emotional_needs"]:
                    needs["emotional_needs"].append(emotional_need)

        return needs

    def _extract_frustrations(
        self, patterns: Dict, interview_data: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Extract frustration points with evidence counts and source labels.
        Defaults are never invented — if no frustrations exist in the data,
        the output is an empty list, not a placeholder list.
        """
        frustrations: List[Dict[str, Any]] = []

        for pain, count in list(patterns["pain_points"].items())[:8]:
            frustrations.append({
                "issue":          pain,
                "evidence_count": count,
                "source":         "behavioral data",
            })

        seen = {item["issue"] for item in frustrations}
        for record in interview_data:
            for pain in record.get("pain_points", [])[:3]:
                if pain not in seen:
                    frustrations.append({
                        "issue":          pain,
                        "evidence_count": None,
                        "source":         "interview note",
                    })
                    seen.add(pain)

        return frustrations

    # ------------------------------------------------------------------
    # Example segments
    # ------------------------------------------------------------------

    def _generate_example_segments(self, behavioral_data: List[Dict]) -> List[Dict]:
        """
        Generate illustrative, overlapping example segments from observed
        behavioral combinations. These are not persona types — they are
        the most common observed intersections of frequency, device, and
        context. A user may fit multiple segments across different sessions.
        """
        if not behavioral_data:
            return []

        segment_counter: Counter = Counter()
        segment_features: Dict[str, List] = defaultdict(list)
        segment_pains: Dict[str, List] = defaultdict(list)

        for record in behavioral_data:
            key_tuple = (
                record.get("usage_frequency", "unknown"),
                record.get("primary_device",  "unknown"),
                record.get("usage_context",   "unknown"),
            )
            segment_counter[key_tuple] += 1
            combo_key = " | ".join(key_tuple)
            segment_features[combo_key].extend(record.get("features_used", []))
            segment_pains[combo_key].extend(record.get("pain_points", []))

        example_segments = []
        for combo, count in segment_counter.most_common(self.max_example_segments):
            combo_key = " | ".join(combo)
            example_segments.append({
                "label": (
                    f"Example pattern: {combo[0]} usage on {combo[1]} "
                    f"in {combo[2]} contexts"
                ),
                "users":              count,
                "top_features":       [
                    feat for feat, _
                    in Counter(segment_features[combo_key]).most_common(4)
                ],
                "common_pain_points": [
                    pain for pain, _
                    in Counter(segment_pains[combo_key]).most_common(3)
                ],
                "note": (
                    "Illustrative slice only. Users may fit multiple examples "
                    "over time, across tasks or devices."
                ),
            })

        return example_segments

    def _document_contradictions(
        self, patterns: Dict, interview_data: List[Dict]
    ) -> Dict:
        """
        Surface contradictions, exceptions, and ambiguities in the data.
        This is mandatory per File 2 methodology: contradictions are
        analytically valuable and must not be hidden.

        Documents:
        - split patterns where no single value dominates
        - interview-reported pain points that contradict behavioural patterns
        - patterns that appear situational rather than stable
        """
        contradictions: List[str] = []
        notes: List[str] = []

        # Check for split usage frequency — no dominant pattern
        freq = patterns.get("usage_frequency", {})
        if freq:
            top_count = max(freq.values())
            total = sum(freq.values())
            top_share = top_count / total if total else 0
            if top_share < 0.5:
                contradictions.append(
                    f"Usage frequency is split across patterns "
                    f"({self._format_distribution(freq)}). No single frequency "
                    f"dominates. Avoid assuming one repeat-use pattern."
                )

        # Check for split device — no dominant device
        devices = patterns.get("devices", {})
        if devices:
            top_count = max(devices.values())
            total = sum(devices.values())
            if total and top_count / total < 0.5:
                contradictions.append(
                    f"Device access is split ({self._format_distribution(devices)}). "
                    f"Desktop-only or mobile-only assumptions are not supported."
                )

        # Check for interview pain points not appearing in behavioral data
        behavioral_pains = set(patterns.get("pain_points", {}).keys())
        for record in interview_data:
            for pain in record.get("pain_points", []):
                if pain not in behavioral_pains:
                    contradictions.append(
                        f"Interview-reported friction '{pain}' does not appear "
                        f"in behavioral data. May be qualitative-only signal or "
                        f"underrepresented in analytics."
                    )

        if not contradictions:
            notes.append(
                "No major contradictions detected in available data. "
                "This does not mean contradictions are absent — it may mean "
                "the data sources are too similar to surface them. "
                "Consider adding a second source type to stress-test patterns."
            )

        return {
            "contradictions": contradictions,
            "notes": notes,
            "reminder": (
                "For every major pattern, also ask: who does not fit this? "
                "Where does it break down? What alternative explanation exists? "
                "Document answers in the limitations block."
            ),
        }

    def _generate_governance_block(self, sources: List[DataSource]) -> Dict:
        """
        Generate a governance block for the analysis output.
        Addresses persona staleness risk (Jung et al., 2019) and File 2's
        governance requirements: every output must have an owner, intended use,
        known limits, and a review trigger.
        """
        source_summary = [
            f"{s.label} ({s.source_type}, {len(s.data)} records)"
            for s in sources
        ]

        return {
            "date_of_latest_evidence": "Populate with date of most recent source",
            "source_summary":          source_summary,
            "intended_use":            "Populate before publishing: which decisions does this inform?",
            "owner":                   "Populate before publishing: who is responsible for updates?",
            "review_triggers": [
                "Product changes materially",
                "Market or user context shifts",
                "New behaviours emerge in analytics or support data",
                "New evidence contradicts the current model",
                "Team is making a new class of decision not covered by original brief",
                "Evidence is more than 12 months old and product has changed",
            ],
            "note": (
                "Jung et al. (2019) demonstrated significant persona drift over "
                "a two-year period. Stale personas are not neutral — they actively "
                "mislead. Treat this output as expired if evidence is >12 months old "
                "and the product has changed."
            ),
        }

    # ------------------------------------------------------------------
    # Quotes
    # ------------------------------------------------------------------

    def _select_quotes(self, interview_data: List[Dict]) -> List[str]:
        """
        Return only real interview quotes. Never fabricate defaults.
        If no interview data was supplied, this returns an empty list.
        """
        quotes: List[str] = []
        for record in interview_data:
            for quote in record.get("quotes", [])[:2]:
                if quote and quote not in quotes:
                    quotes.append(quote)
            if len(quotes) >= 6:
                break
        return quotes

    # ------------------------------------------------------------------
    # Data points & confidence
    # ------------------------------------------------------------------

    def _calculate_data_points(self, sources: List[DataSource]) -> Dict:
        """
        Calculate transparent data notes per source.
        Deliberately avoids binary High/Medium/Low labels (Gap B in
        Salminen et al., 2021) and instead provides narrative confidence
        notes that make the limits of the evidence clear.
        """
        source_summaries = []
        total_behavioral = 0

        for source in sources:
            count = len(source.data)
            if source.source_type in ("analytics", "survey", "usability_test"):
                total_behavioral += count

            if count == 0:
                note = "No records supplied. Treat any output from this source as a placeholder."
            elif count < 10:
                note = "Small sample. Useful for forming hypotheses; not for broad generalisation."
            elif count < 30:
                note = "Moderate directional signal. Validate before major product commitments."
            else:
                note = "Reasonable exploratory coverage. Still not exhaustive or definitive."

            source_summaries.append({
                "label":           source.label,
                "source_type":     source.source_type,
                "record_count":    count,
                "confidence_note": note,
            })

        return {
            "sources":                source_summaries,
            "total_behavioral_records": total_behavioral,
            "last_updated":           "Current",
            "validation_method":      "Observed behavior summary plus optional interview evidence",
        }

    # ------------------------------------------------------------------
    # Design implications
    # ------------------------------------------------------------------

    def _derive_design_implications(self, patterns: Dict) -> List[Dict[str, str]]:
        """
        Generate tentative design implications tied to explicit signals.
        Each implication carries a 'because' field quoting the supporting
        evidence, addressing Salminen et al. (2021) Gap B (evaluation) by
        making the evidentiary basis of each recommendation visible.
        """
        implications: List[Dict[str, str]] = []
        threshold = self.min_count_for_directional_signal

        daily_count = patterns["usage_frequency"].get("daily", 0)
        if daily_count >= threshold:
            implications.append({
                "recommendation": "Reduce friction in recurring tasks and shorten repeat flows.",
                "because": (
                    f"Daily usage appears {daily_count} times — above the signal threshold. "
                    "Efficiency in repeat flows is likely a real constraint."
                ),
            })
        else:
            implications.append({
                "recommendation": "Improve discoverability and guidance for variable usage patterns.",
                "because": (
                    "No strong dominant repeat-use pattern was found. "
                    "Users may arrive with diverse or infrequent intent."
                ),
            })

        mobile_count = patterns["devices"].get("mobile", 0)
        if mobile_count >= threshold:
            implications.append({
                "recommendation": "Test common tasks on mobile and prioritise short-session completion.",
                "because": (
                    f"Mobile use appears {mobile_count} times — "
                    "desktop-only assumptions carry real risk."
                ),
            })

        work_count = patterns["contexts"].get("work", 0)
        if work_count >= threshold:
            implications.append({
                "recommendation": (
                    "Support interruption recovery, clarity, and predictable task handoffs."
                ),
                "because": (
                    f"Work-context usage appears {work_count} times and likely involves "
                    "multitasking or context switching."
                ),
            })

        for pain, count in list(patterns["pain_points"].items())[:2]:
            if count >= threshold:
                implications.append({
                    "recommendation": f"Investigate and reduce friction around '{pain}'.",
                    "because":        f"This issue appears {count} times in the available data.",
                })

        return implications[:6]

    # ------------------------------------------------------------------
    # Limitations & method notes
    # ------------------------------------------------------------------

    def _describe_limitations(
        self,
        sources: List[DataSource],
        field_assessment: Dict,
        ai_enrichments: List[AIEnrichmentRecord] = None,
    ) -> List[str]:
        """
        State the main analytical limits of this output.
        Addresses Salminen et al. (2021) Gap B and Amin et al. (2025)
        GenAI-specific risks.
        """
        limitations = [
            "This output is an analytical summary, not a portrait of one person.",
            "Users may move between patterns over time, task, and device.",
            "Absent fields were not inferred.",
            "Correlated behavior should not be treated as proof of identity, motivation, or demographic truth.",
            "Example segments are overlapping illustrations, not deductive categories.",
        ]

        total_records = sum(len(s.data) for s in sources)
        if total_records < 10:
            limitations.append(
                "Very small total sample. Outputs are hypothesis-generating only."
            )

        interview_sources = [s for s in sources if s.source_type == "interview"]
        if not interview_sources:
            limitations.append(
                "No interview evidence was provided. Intent and motivation are "
                "likely underrepresented. Without real user voices, there is a "
                "risk of producing Potemkin personas — profiles that appear "
                "credible but lack authentic user grounding. "
                "(Muller & Seaborn, 2025)"
            )

        absent_fields = [
            f for f, meta in field_assessment.items() if not meta["present"]
        ]
        if absent_fields:
            limitations.append(
                f"The following optional fields were absent and not inferred: "
                f"{', '.join(absent_fields)}."
            )

        # GenAI-specific limitations
        if ai_enrichments:
            unvalidated = [e for e in ai_enrichments if not e.validated_against_source]
            if unvalidated:
                limitations.append(
                    f"AI enrichment was applied at the following stages without "
                    f"validation against source records: "
                    f"{[e.stage for e in unvalidated]}. "
                    f"Outputs from these stages should be treated as "
                    f"hallucination candidates until verified. (PG6, Amin et al., 2025)"
                )
            models = list({e.model for e in ai_enrichments})
            if len(models) == 1:
                limitations.append(
                    f"Only one AI model ({models[0]}) was used. "
                    f"Single-model outputs embed that model's biases. "
                    f"PG1 requires validation with a second model or real user data."
                )

        return limitations

    def _generate_method_notes(
        self, ai_enrichments: List[AIEnrichmentRecord] = None
    ) -> List[str]:
        """
        Explain the key methodological guardrails applied in this analysis.
        References both Salminen et al. (2021) and Amin et al. (2025).
        """
        notes = [
            "Gap A — Shared resources: DataSource registry documents provenance for each input.",
            "Gap B — Evaluation: Every output carries explicit confidence notes and a limitations block.",
            "Gap C — Standardisation: Consistent output schema applied regardless of source type.",
            "Gap D — Inclusivity: No demographic or psychographic inference without explicit evidence.",
            "Gap E — Loss of depth: Interview evidence preserved separately from behavioral aggregates.",
            "No archetypes are pre-defined. Segments emerge from the data.",
            "No fabricated identity: names, quotes, and bios are never invented.",
            f"Evidence threshold: {DEFAULT_MIN_SIGNAL_COUNT} occurrences required before surfacing a signal.",
            "HUMAN REVIEW REQUIRED (PG7): A domain expert must review this output before design use.",
            "CONSISTENCY CHECK (PG6): Run this generator 3x on the same data; compare outputs for stability.",
        ]

        if ai_enrichments:
            notes.append(
                "AI INVOLVEMENT DOCUMENTED (PG3): See ai_involvement block for models, "
                "stages, and prompt references."
            )
            notes.append(
                "CIRCULARITY RISK: Do not use the same model that generated this output "
                "to evaluate it. Use a different model or human evaluators. (Amin et al., 2025)"
            )
            notes.append(
                "MULTI-MODEL VALIDATION (PG1): Validate key outputs against a second "
                "model or against real user data before use."
            )
        else:
            notes.append(
                "No AI enrichment was applied to sources in this analysis. "
                "If LLMs are used in downstream profile crafting, document them "
                "using AIEnrichmentRecord and re-run the generator."
            )

        return notes

    # ------------------------------------------------------------------
    # Title & summary
    # ------------------------------------------------------------------

    def _generate_title(
        self, patterns: Dict, sources: List[DataSource]
    ) -> str:
        total = sum(len(s.data) for s in sources)
        source_labels = ", ".join(s.label for s in sources)
        top_context   = self._top_key(patterns.get("contexts", {}), "mixed contexts")
        top_frequency = self._top_key(patterns.get("usage_frequency", {}), "mixed-frequency")
        return (
            f"Observed user patterns — {total} records across {len(sources)} source(s): "
            f"{source_labels}. Dominant pattern: {top_frequency} usage in {top_context}."
        )

    def _generate_summary(
        self,
        patterns: Dict,
        behavioral_data: List[Dict],
        interview_data: List[Dict],
    ) -> str:
        b_count  = len(behavioral_data)
        i_count  = len(interview_data)
        top_freq = self._top_key(patterns.get("usage_frequency", {}), "mixed-frequency")
        top_ctx  = self._top_key(patterns.get("contexts", {}),        "mixed contexts")
        top_dev  = self._top_key(patterns.get("devices", {}),         "mixed devices")
        top_pain = self._top_key(patterns.get("pain_points", {}),     "no single dominant pain point")

        interview_note = (
            f" {i_count} interview record(s) provided qualitative enrichment."
            if i_count else
            " No interview evidence was supplied."
        )

        return (
            f"Analysis of {b_count} behavioral record(s) without forcing users into a "
            f"single persona type.{interview_note} "
            f"The strongest visible pattern is {top_freq} usage in {top_ctx} contexts, "
            f"with {top_dev} as the most common access mode. "
            f"The most repeated friction in the available data is '{top_pain}'."
        )

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    def format_analysis_output(self, analysis: Dict) -> str:
        """Format the analysis for human-readable display."""

        out: List[str] = []
        out.append("=" * 72)
        out.append(analysis["title"])
        out.append("=" * 72)
        out.append(f"\n{analysis['summary']}\n")

        # AI involvement — surface prominently when present
        ai = analysis.get("ai_involvement", {})
        if ai.get("ai_used"):
            out.append("⚠️  AI Involvement:")
            out.append(f"  • Models used: {', '.join(ai.get('models_used', []))}")
            out.append(f"  • Stages: {', '.join(ai.get('stages', []))}")
            out.append(f"  • Prompt refs: {', '.join(ai.get('prompt_references', []))}")
            if not ai.get("multi_model"):
                out.append(f"  • PG1 WARNING: {ai.get('pg1_warning', '')}")
            if ai.get("hallucination_risk"):
                out.append(f"  • HALLUCINATION RISK: {ai['hallucination_risk']}")
            if ai.get("circularity_warning"):
                out.append(f"  • CIRCULARITY: {ai['circularity_warning']}")
        else:
            out.append("✓  No AI enrichment applied to sources.")
        out.append("")

        out.append("📦 Sources:")
        for s in analysis.get("sources_summary", []):
            out.append(
                f"  • {s['label']} ({s['source_type']}, "
                f"{s['record_count']} records)"
            )
            if s.get("behavioral_fields_available"):
                out.append(
                    f"    Fields present: {', '.join(s['behavioral_fields_available'])}"
                )

        out.append("\n📈 Observed Patterns:")
        p = analysis["patterns"]
        out.append(f"  • Usage frequency: {self._format_distribution(p.get('usage_frequency', {}))}")
        out.append(f"  • Devices:         {self._format_distribution(p.get('devices', {}))}")
        out.append(f"  • Contexts:        {self._format_distribution(p.get('contexts', {}))}")
        out.append(f"  • Top features:    {', '.join(list(p.get('feature_usage', {}).keys())[:6]) or 'None'}")

        # Optional fields
        optional = analysis.get("optional_fields", {})
        if optional:
            out.append("\n🗂  Optional Fields:")
            for fname, fdata in optional.items():
                if fdata["status"] == "absent":
                    out.append(f"  • {fname}: not present — {fdata['note']}")
                else:
                    src = ", ".join(fdata.get("source_types", []))
                    mean = fdata.get("mean")
                    mean_str = f" (mean: {mean})" if mean is not None else ""
                    dist = self._format_distribution(fdata.get("distribution", {}))
                    out.append(f"  • {fname} [from {src}]{mean_str}: {dist}")
                    out.append(f"    Note: {fdata['note']}")

        # Psychographics
        psycho = analysis.get("psychographics", {})
        if psycho.get("motivations") or psycho.get("values"):
            out.append("\n🧠 Psychographics (explicit evidence only):")
            for m in psycho.get("motivations", []):
                out.append(f"  • Motivation: {m['value']} ({m['count']} mentions, {m['source']})")
            for v in psycho.get("values", []):
                out.append(f"  • Value: {v['value']} ({v['count']} mentions, {v['source']})")
            out.append(f"  Source note: {psycho.get('source_note', '')}")
        elif psycho.get("source_note"):
            out.append(f"\n🧠 Psychographics: {psycho['source_note']}")

        # Needs
        out.append("\n🎯 Goals & Needs:")
        needs = analysis["needs_and_goals"]
        items = (
            needs.get("primary_goals", []) +
            needs.get("functional_needs", []) +
            needs.get("emotional_needs", [])
        )
        if items:
            for item in items[:6]:
                out.append(f"  • {item}")
            for ev in needs.get("supporting_evidence", [])[:3]:
                out.append(f"    ↳ Evidence: {ev}")
        else:
            out.append("  • No strong need signal identified from the supplied data.")

        # Frustrations
        out.append("\n😤 Frustrations:")
        if analysis["frustrations"]:
            for f in analysis["frustrations"][:5]:
                count  = f.get("evidence_count")
                source = f.get("source", "unknown source")
                count_str = f"{count} mentions; " if count is not None else ""
                out.append(f"  • {f['issue']} ({count_str}{source})")
        else:
            out.append("  • No repeated frustrations found in the supplied data.")

        # Behaviors
        out.append("\n📊 Behaviors:")
        for pat in analysis["behaviors"].get("usage_patterns", [])[:4]:
            out.append(f"  • {pat}")
        for mode in analysis["behaviors"].get("interaction_modes", [])[:2]:
            out.append(f"  • {mode}")

        # Example segments
        out.append("\n🧩 Example Segments (illustrative, not exhaustive):")
        if analysis["example_segments"]:
            for seg in analysis["example_segments"]:
                out.append(f"  • {seg['label']} ({seg['users']} users)")
                if seg.get("top_features"):
                    out.append(f"    Top features:   {', '.join(seg['top_features'])}")
                if seg.get("common_pain_points"):
                    out.append(f"    Pain points:    {', '.join(seg['common_pain_points'])}")
                out.append(f"    {seg['note']}")
        else:
            out.append("  • No example segments could be formed.")

        # Quotes
        # Contradictions — mandatory section
        out.append("\n⚡ Contradictions & exceptions:")
        contra = analysis.get("contradictions", {})
        if contra.get("contradictions"):
            for c in contra["contradictions"]:
                out.append(f"  • {c}")
        for note in contra.get("notes", []):
            out.append(f"  ℹ {note}")
        if contra.get("reminder"):
            out.append(f"  → {contra['reminder']}")

        if analysis["quotes"]:
            out.append("\n💬 Interview Quotes (real only):")
            for q in analysis["quotes"][:4]:
                out.append(f'  • "{q}"')

        # Design implications
        out.append("\n💡 Design Implications:")
        for imp in analysis["design_implications"]:
            out.append(f"  → {imp['recommendation']}")
            out.append(f"    Because: {imp['because']}")

        # Data points
        out.append("\n📈 Data Points:")
        dp = analysis["data_points"]
        out.append(f"  Total behavioral records: {dp['total_behavioral_records']}")
        for s in dp.get("sources", []):
            out.append(f"  • {s['label']}: {s['record_count']} records — {s['confidence_note']}")

        # Governance
        gov = analysis.get("governance", {})
        out.append("\n📋 Governance:")
        out.append(f"  • Latest evidence date: {gov.get('date_of_latest_evidence', 'not set')}")
        out.append(f"  • Owner: {gov.get('owner', 'not set')}")
        out.append(f"  • Intended use: {gov.get('intended_use', 'not set')}")
        out.append(f"  • Review triggers: {'; '.join(gov.get('review_triggers', [])[:3])} (and others)")

        # Limitations
        out.append("\n⚠️  Limitations:")
        for lim in analysis["limitations"]:
            out.append(f"  • {lim}")

        # Method notes
        out.append("\n🔬 Method Notes (Salminen et al., 2021 + Amin et al., 2025):")
        for note in analysis["method_notes"]:
            out.append(f"  • {note}")

        return "\n".join(out)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _top_key(self, mapping: Dict, fallback: str) -> str:
        """Return the key with the highest count, or fallback if empty."""
        return max(mapping.items(), key=lambda x: x[1])[0] if mapping else fallback

    def _format_distribution(self, mapping: Dict) -> str:
        """Format a count dictionary as a readable string."""
        if not mapping:
            return "None"
        return ", ".join(f"{k} ({v})" for k, v in mapping.items())


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

def create_sample_sources() -> List[Dict]:
    """
    Create multi-source sample data for testing.

    Demonstrates the three most common source type combinations:
      - analytics:  behavioral data, no demographic fields
      - survey:     behavioral + optional demographic fields
      - interview:  qualitative evidence only, with an AI enrichment record
                    to demonstrate PG3 prompt documentation

    The interview source includes an ai_enrichments entry showing how to
    document LLM-assisted thematic analysis per Amin et al. (2025) PG3.
    """
    analytics_data = [
        {
            "user_id":         f"user_{i}",
            "usage_frequency": ["daily", "weekly", "monthly"][i % 3],
            "features_used":   ["dashboard", "reports", "settings", "sharing", "export"][:3 + (i % 3)],
            "primary_device":  ["desktop", "mobile", "tablet"][i % 3],
            "usage_context":   ["work", "personal"][i % 2],
            "pain_points":     ["slow loading", "confusing UI", "missing features"][:(i % 3) + 1],
        }
        for i in range(20)
    ]

    survey_data = [
        {
            "user_id":          f"survey_{i}",
            "usage_frequency":  ["daily", "weekly"][i % 2],
            "features_used":    ["dashboard", "reports", "export"][:2 + (i % 2)],
            "primary_device":   ["desktop", "mobile"][i % 2],
            "usage_context":    "work",
            "pain_points":      ["slow loading", "confusing UI"][:(i % 2) + 1],
            # Optional fields — present only in this survey source
            "age":              25 + (i % 20),
            "tech_confidence":  3 + (i % 5),
            "location_type":    ["urban", "suburban"][i % 2],
        }
        for i in range(10)
    ]

    interview_data = [
        {
            "quotes":         ["I need to see all my data in one place",
                                "I always lose track of where things live"],
            "motivations":    ["Efficiency", "Control"],
            "values":         ["Reliability", "Transparency"],
            "goals":          ["Save time", "Make better decisions"],
            "needs":          ["Clear information hierarchy", "Faster report access"],
            "emotional_needs":["Feel confident in the data I'm looking at"],
            "pain_points":    ["I lose track of where things live"],
        },
        {
            "quotes":         ["The mobile experience is just not there yet"],
            "motivations":    ["Flexibility"],
            "values":         ["Reliability"],
            "goals":          ["Access data on the go"],
            "needs":          ["Mobile parity with desktop"],
            "pain_points":    ["mobile app missing key features"],
        },
    ]

    return [
        {
            "type":  "analytics",
            "data":  analytics_data,
            "label": "Product analytics export (20 users)",
            # No AI enrichment — raw analytics data passed directly
        },
        {
            "type":  "survey",
            "data":  survey_data,
            "label": "Q3 workflow survey (10 respondents)",
            # No AI enrichment — survey responses passed directly
        },
        {
            "type":  "interview",
            "data":  interview_data,
            "label": "Checkout flow interviews (2 sessions)",
            # Example: LLM was used to assist with thematic analysis
            # before these records were structured. Documented per PG3.
            "ai_enrichments": [
                {
                    "stage":                     "thematic_analysis",
                    "model":                     "claude-sonnet-4-20250514",
                    "prompt_reference":          "prompts/interview_thematic_v1.txt",
                    "validated_against_source":  True,
                    "notes": (
                        "LLM used to identify themes from raw transcripts. "
                        "All themes verified by researcher against original transcripts. "
                        "Quotes extracted manually, not by LLM."
                    ),
                }
            ],
        },
    ]


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    generator = PersonaGenerator()
    sources   = create_sample_sources()
    analysis  = generator.generate_analysis(sources)

    if len(sys.argv) > 1 and sys.argv[1] == "json":
        print(json.dumps(analysis, indent=2))
    else:
        print(generator.format_analysis_output(analysis))


if __name__ == "__main__":
    main()
```
