#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path


DEFAULT_AUTHOR_PATTERN = r"^(?P<author>[^_]+)"


def _bootstrap_local_src() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    source_path = repository_root / "src"
    if str(source_path) not in sys.path:
        sys.path.insert(0, str(source_path))


_bootstrap_local_src()

from sIArena.grading import grade_input_to_csv  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate one notebook (.ipynb) or a zip archive of notebooks (.zip) "
            "against a grader YAML configuration and write the results to a CSV file."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the .ipynb or .zip file to grade.",
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to the grader .yaml configuration file.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the output .csv file.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of measurement iterations per terrain.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output while evaluating functions.",
    )
    parser.add_argument(
        "--author-pattern",
        default=DEFAULT_AUTHOR_PATTERN,
        help=(
            "Regex used to derive the author from the notebook file stem. "
            "Defaults to the text before the first underscore."
        ),
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    batch_result = grade_input_to_csv(
        args.input,
        args.config,
        args.output,
        iterations=args.iterations,
        debug=args.debug,
        author_pattern=args.author_pattern,
    )

    print(f"Assignment: {batch_result.assignment_id}")
    print(f"Input: {args.input}")
    print(f"Output CSV: {args.output}")
    print(f"Processed submissions: {len(batch_result.submission_grades)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
