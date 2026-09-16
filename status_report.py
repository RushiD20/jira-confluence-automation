"""Utilities for generating a weekly status report in Markdown."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping


def fetch_status_data() -> dict:
    """Return the current team status snapshot used for report generation."""
    return {
        "reporting_period": "2026-09-08 to 2026-09-14",
        "project_or_team": "ARE Platform Team",
        "owner": "Engineering Manager",
        "overall_status": "On track",
        "accomplishments": [
            "Completed the user authentication API and merged it to the main branch.",
            "Resolved 12 priority-two defects from the current sprint.",
            "Published the updated deployment runbook in Confluence.",
        ],
        "progress_and_metrics": {
            "completed_work": "18 of 24 planned story points.",
            "key_metric_or_milestone": "Authentication API is ready for integration testing.",
            "current_progress": "75% of sprint story points are complete.",
        },
        "blockers_and_risks": [
            {
                "blocker_or_risk": "Integration testing depends on the test environment upgrade.",
                "impact": "Testing could slip by one business day if the upgrade is delayed.",
                "owner_and_next_action": "DevOps will complete the upgrade by 2026-09-15.",
            }
        ],
        "next_period_plan": [
            "Complete integration testing for authentication.",
            "Deliver the remaining six sprint story points.",
            "Review release readiness with product and operations teams.",
        ],
        "decisions_or_support_needed": [
            "Confirm whether the release window remains 2026-09-18.",
        ],
    }


def _render_bullets(items: Iterable[str]) -> str:
    """Format a list of strings as Markdown bullet points."""
    return "\n".join(f"- {item}" for item in items)


def build_report(data: Mapping[str, object]) -> str:
    """Build a standard weekly status report from a data dictionary."""
    accomplishments = data.get("accomplishments", [])
    next_plan = data.get("next_period_plan", [])
    decisions = data.get("decisions_or_support_needed", [])
    blockers = data.get("blockers_and_risks", [])
    progress = data.get("progress_and_metrics", {})

    blocker_lines = []
    for blocker in blockers:
        if isinstance(blocker, Mapping):
            blocker_lines.extend(
                [
                    f"- Blocker or risk: {blocker.get('blocker_or_risk', '')}",
                    f"- Impact: {blocker.get('impact', '')}",
                    f"- Owner and next action: {blocker.get('owner_and_next_action', '')}",
                ]
            )
        else:
            blocker_lines.append(f"- {blocker}")

    report = [
        "# Weekly Status Report",
        "",
        f"**Reporting period:** {data.get('reporting_period', 'YYYY-MM-DD to YYYY-MM-DD')}  ",
        f"**Project or team:** {data.get('project_or_team', '')}  ",
        f"**Owner:** {data.get('owner', '')}  ",
        f"**Overall status:** {data.get('overall_status', 'On track')}",
        "",
        "## Accomplishments",
        _render_bullets(accomplishments),
        "",
        "## Progress and Metrics",
        f"- Completed work: {progress.get('completed_work', '')}",
        f"- Key metric or milestone: {progress.get('key_metric_or_milestone', '')}",
        f"- Current progress: {progress.get('current_progress', '')}",
        "",
        "## Blockers and Risks",
        *blocker_lines,
        "",
        "## Next Period's Plan",
        _render_bullets(next_plan),
        "",
        "## Decisions or Support Needed",
        _render_bullets(decisions),
        "",
    ]
    return "\n".join(report).strip() + "\n"


def generate_report(data: Mapping[str, object] | None = None, output_path: str | Path | None = None) -> Path:
    """Generate a Markdown report file and return the output path."""
    report_data = fetch_status_data() if data is None else data
    doc_path = Path(output_path) if output_path is not None else Path("weekly_status_report.md")
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(build_report(report_data), encoding="utf-8")
    return doc_path


if __name__ == "__main__":
    output = generate_report()
    print(f"Report generated at: {output}")
