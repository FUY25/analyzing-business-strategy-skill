#!/usr/bin/env python3
"""
Validate process YAML files for the business-expert skill.
Run after synthesis (Phase 2) and after each validation round (Phase 4),
before the Partner review. Surfaces warnings — does not block execution.

Usage:
    python scripts/validate_process.py process/
    python scripts/validate_process.py process/workstream-a-findings.yaml
"""

import sys
import os
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("WARNING: PyYAML not installed. Install with: pip install pyyaml")
    sys.exit(1)


# Domain-specific recency thresholds (years)
RECENCY_THRESHOLDS = {
    "ai": 3, "tech": 3, "technology": 3, "saas": 3, "software": 3,
    "strategy": 5, "business": 5, "market": 5, "finance": 5, "financial": 5,
    "classic": 50, "framework": 50, "theory": 50,
}
DEFAULT_RECENCY = 5

REQUIRED_FIELDS = ["workstream", "agent", "problem_scope", "status", "key_findings"]
REQUIRED_FINDING_FIELDS = ["finding", "confidence", "source", "implications"]
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_SOURCE_TYPES = {"verified", "model_estimate", "derived"}


def get_recency_threshold(domain_text):
    """Determine how recent sources should be based on domain keywords."""
    domain_lower = domain_text.lower() if domain_text else ""
    for keyword, years in RECENCY_THRESHOLDS.items():
        if keyword in domain_lower:
            return years
    return DEFAULT_RECENCY


def extract_year(source_text):
    """Try to extract a year from source text."""
    if not source_text:
        return None
    matches = re.findall(r'20[0-2]\d|19\d\d', str(source_text))
    if matches:
        return max(int(y) for y in matches)
    return None


def validate_file(filepath):
    """Validate a single YAML process file. Returns (warnings, highlights)."""
    warnings = []
    highlights = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"], []
    except Exception as e:
        return [f"File read error: {e}"], []

    if not isinstance(data, dict):
        return ["File is not a YAML mapping"], []

    filename = os.path.basename(filepath)

    # Check required top-level fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            warnings.append(f"Missing required field: '{field}'")

    # Check status
    status = data.get("status", "")
    if status not in ("complete", "in_progress", "blocked"):
        warnings.append(f"Unexpected status: '{status}' (expected: complete/in_progress/blocked)")

    # Check key_findings
    findings = data.get("key_findings", [])
    if not findings:
        warnings.append("No key_findings — agent produced no results")
    else:
        domain = data.get("workstream", "") or data.get("problem_scope", "")
        recency = get_recency_threshold(domain)
        current_year = datetime.now(timezone.utc).year

        high_confidence_count = 0
        low_confidence_count = 0
        missing_source_count = 0
        total_data_points = 0
        model_estimate_count = 0
        verified_count = 0
        missing_source_type_count = 0

        for i, finding in enumerate(findings, 1):
            if not isinstance(finding, dict):
                warnings.append(f"Finding #{i} is not a mapping")
                continue

            # Check required finding fields
            for field in REQUIRED_FINDING_FIELDS:
                if field not in finding:
                    warnings.append(f"Finding #{i}: missing '{field}'")

            # Check confidence level
            conf = finding.get("confidence", "").lower()
            if conf and conf not in VALID_CONFIDENCE:
                warnings.append(f"Finding #{i}: invalid confidence '{conf}' (use high/medium/low)")
            elif conf == "high":
                high_confidence_count += 1
            elif conf == "low":
                low_confidence_count += 1

            # Check source exists
            source = finding.get("source", "")
            if not source:
                missing_source_count += 1

            # Check source recency
            if source:
                year = extract_year(str(source))
                if year and (current_year - year) > recency:
                    warnings.append(
                        f"Finding #{i}: source from {year} may be stale "
                        f"(domain '{domain}' threshold: {recency} years)"
                    )

            # Highlight high-confidence findings
            if conf == "high" and finding.get("finding"):
                highlights.append(f"[HIGH] {finding['finding'][:120]}")

            # Check data_points for source_type
            data_points = finding.get("data_points", [])
            for j, dp in enumerate(data_points, 1):
                if not isinstance(dp, dict):
                    continue
                total_data_points += 1
                st = dp.get("source_type", "").lower()
                if not st:
                    missing_source_type_count += 1
                elif st not in VALID_SOURCE_TYPES:
                    warnings.append(
                        f"Finding #{i}, data point #{j}: invalid source_type '{st}' "
                        f"(use verified/model_estimate/derived)"
                    )
                elif st == "model_estimate":
                    model_estimate_count += 1
                elif st == "verified":
                    verified_count += 1
                    if not dp.get("source_url"):
                        warnings.append(
                            f"Finding #{i}, data point #{j}: source_type is 'verified' "
                            f"but no source_url provided"
                        )

        # Summary warnings
        if missing_source_count > 0:
            warnings.append(f"{missing_source_count} finding(s) have no source attribution")
        if low_confidence_count > high_confidence_count and len(findings) > 2:
            warnings.append(
                f"More low-confidence ({low_confidence_count}) than high-confidence "
                f"({high_confidence_count}) findings — evidence may be weak"
            )
        if high_confidence_count >= 3:
            highlights.append(f"{high_confidence_count} high-confidence findings — strong evidence base")

        # Source type summary warnings
        if total_data_points > 0:
            if missing_source_type_count > 0:
                warnings.append(
                    f"{missing_source_type_count}/{total_data_points} data point(s) "
                    f"missing source_type field"
                )
            estimate_ratio = model_estimate_count / total_data_points
            if estimate_ratio > 0.1:
                warnings.append(
                    f"⚠️  {model_estimate_count}/{total_data_points} data points are "
                    f"model_estimate ({estimate_ratio:.0%}) — exceeds 10% threshold, "
                    f"agent needs more research"
                )
            elif model_estimate_count > 0:
                highlights.append(
                    f"{verified_count} verified, {model_estimate_count} model_estimate "
                    f"out of {total_data_points} data points"
                )
            if verified_count == total_data_points and total_data_points > 0:
                highlights.append(
                    f"All {total_data_points} data points verified with sources"
                )

    # Check data_gaps section
    gaps = data.get("data_gaps", None)
    if gaps is None:
        warnings.append("No 'data_gaps' section — agent should explicitly note gaps (even if empty list)")
    elif gaps:
        for gap in gaps:
            highlights.append(f"[GAP] {str(gap)[:120]}")

    # Check sources section
    sources = data.get("sources", [])
    if not sources and findings:
        warnings.append("No 'sources' section despite having findings")

    return warnings, highlights


def check_cross_file(all_results):
    """Check for issues across multiple workstream files."""
    cross_warnings = []
    all_findings_text = {}

    for filepath, (data_warnings, data_highlights, data) in all_results.items():
        if not isinstance(data, dict):
            continue
        findings = data.get("key_findings", [])
        for finding in findings:
            if isinstance(finding, dict):
                text = finding.get("finding", "")
                if text:
                    key = text.lower().strip()[:80]
                    if key in all_findings_text:
                        cross_warnings.append(
                            f"Possible duplicate finding across "
                            f"'{os.path.basename(all_findings_text[key])}' and "
                            f"'{os.path.basename(filepath)}': \"{text[:60]}...\""
                        )
                    else:
                        all_findings_text[key] = filepath

    return cross_warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_process.py <process_dir_or_file>")
        sys.exit(1)

    target = sys.argv[1]
    files = []

    if os.path.isdir(target):
        for f in sorted(Path(target).glob("*.yaml")):
            if f.name != "engagement-state.yaml" and f.name != "next-steps-proposal.yaml":
                files.append(str(f))
    elif os.path.isfile(target):
        files.append(target)
    else:
        print(f"Not found: {target}")
        sys.exit(1)

    if not files:
        print("No YAML process files found.")
        sys.exit(0)

    total_warnings = 0
    total_highlights = 0
    all_results = {}

    for filepath in files:
        filename = os.path.basename(filepath)
        warnings, highlights = validate_file(filepath)

        # Load data for cross-file check
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except:
            data = None
        all_results[filepath] = (warnings, highlights, data)

        print(f"\n{'='*60}")
        print(f"  {filename}")
        print(f"{'='*60}")

        if highlights:
            print(f"\n  HIGHLIGHTS ({len(highlights)}):")
            for h in highlights:
                print(f"    + {h}")
            total_highlights += len(highlights)

        if warnings:
            print(f"\n  WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"    ! {w}")
            total_warnings += len(warnings)

        if not warnings and not highlights:
            print("\n    (no issues found)")

    # Cross-file checks
    if len(all_results) > 1:
        cross_warnings = check_cross_file(all_results)
        if cross_warnings:
            print(f"\n{'='*60}")
            print(f"  CROSS-FILE WARNINGS ({len(cross_warnings)})")
            print(f"{'='*60}")
            for w in cross_warnings:
                print(f"    ! {w}")
            total_warnings += len(cross_warnings)

    # Summary
    print(f"\n{'─'*60}")
    print(f"  Summary: {len(files)} file(s) | {total_highlights} highlight(s) | {total_warnings} warning(s)")
    print(f"{'─'*60}")

    sys.exit(1 if total_warnings > 0 else 0)


if __name__ == "__main__":
    main()
