"""Validate files with an AI CLI and save one result per file."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def safe_name(path: Path) -> str:
    """Return a filesystem-safe name for an output file."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(path)).strip("_")


def validate_file(
    file_path: Path,
    instruction: str,
    output_dir: Path,
    command: str,
) -> Path:
    """Send one file to the AI CLI and save its response."""
    contents = file_path.read_text(encoding="utf-8")
    prompt = f"{instruction}\n\nTarget file: {file_path}\n\nFile contents:\n{contents}"

    result = subprocess.run(
        [command, "-p", prompt, "-s"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        error = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"AI CLI failed for {file_path}: {error}")

    output_path = output_dir / f"{safe_name(file_path)}.result.md"
    output_path.write_text(result.stdout, encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate files with an AI CLI and save the results."
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Target files to send to the AI.",
    )
    parser.add_argument(
        "-i",
        "--instruction",
        required=True,
        help="Instruction sent with each file's contents.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("ai-validation-results"),
        help="Directory for AI results (default: ai-validation-results).",
    )
    parser.add_argument(
        "--command",
        default="copilot",
        help="AI CLI executable (default: copilot).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    missing = [path for path in args.files if not path.is_file()]
    if missing:
        for path in missing:
            print(f"Missing target file: {path}", file=sys.stderr)
        return 2

    print("Target files:")
    for path in args.files:
        print(f"- {path}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path in args.files:
        try:
            output_path = validate_file(
                path, args.instruction, args.output_dir, args.command
            )
        except (OSError, RuntimeError) as error:
            print(str(error), file=sys.stderr)
            return 1
        print(f"Saved result: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
