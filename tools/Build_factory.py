"""Build a local definition of the Jira close-parent automation path."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CLOSE_PARENT_PATH: dict[str, Any] = {
    "name": "Close Parent When Sub-Tasks Finish",
    "project": "ARE",
    "trigger": {
        "type": "issue_transitioned",
        "condition": "destination_status_category_is_done",
    },
    "conditions": [
        "project_is_ARE",
        "issue_type_is_sub_task",
        "issue_has_parent",
        "parent_has_at_least_one_sub_task",
        "all_parent_sub_tasks_are_done",
        "parent_status_category_is_not_done",
    ],
    "branch": "parent",
    "actions": [
        {
            "type": "add_comment",
            "body": "[Automation] Evaluated sub-tasks and transitioning parent to DONE.",
        },
        {
            "type": "transition_issue",
            "transition": "DONE",
        },
    ],
    "failure_action": {
        "type": "add_diagnostic_comment",
        "requirements": [
            "include_sub_task_condition",
            "include_attempted_transition",
            "include_failure_reason_when_available",
            "include_required_manual_action",
            "mention_parent_assignee",
        ],
    },
}


def build_close_parent_path(output_paths: list[Path]) -> list[Path]:
    """Write the close-parent automation definition to each output path."""
    if not output_paths:
        raise ValueError("at least one output path is required")

    content = json.dumps(CLOSE_PARENT_PATH, indent=2) + "\n"
    written_paths = []
    for output_path in output_paths:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        written_paths.append(output_path)
    return written_paths


def parse_arguments() -> argparse.Namespace:
    """Parse output paths from the command line."""
    parser = argparse.ArgumentParser(
        description="Build a local JSON definition of the Jira close-parent path."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="one or more JSON output paths",
    )
    return parser.parse_args()


def main() -> None:
    """Build the automation definition and report each output path."""
    arguments = parse_arguments()
    for output_path in build_close_parent_path(arguments.paths):
        print(f"Automation path written to: {output_path}")


if __name__ == "__main__":
    main()
