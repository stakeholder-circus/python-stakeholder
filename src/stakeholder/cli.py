from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence, TextIO

from .catalog import list_values
from .config import Complexity, DevelopmentType, JargonLevel, OutputFormat, SessionConfig
from .runtime import run_session, serialize_events, text_lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stakeholder")
    parser.add_argument("--dev-type", default=DevelopmentType.BACKEND.value)
    parser.add_argument("--jargon", default=JargonLevel.MEDIUM.value)
    parser.add_argument("--complexity", default=Complexity.MEDIUM.value)
    parser.add_argument("--duration", type=int, default=0)
    parser.add_argument("--alerts", action="store_true")
    parser.add_argument("--project", default="distributed-cluster")
    parser.add_argument("--minimal", action="store_true")
    parser.add_argument("--team", action="store_true")
    parser.add_argument("--framework", default="")
    parser.add_argument("--seed")
    parser.add_argument("--output-format", default=OutputFormat.TEXT.value)
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--list-values", action="store_true")
    parser.add_argument("--experimental-provider")
    parser.add_argument("--experimental-model")
    parser.add_argument("--experimental-profile")
    parser.add_argument("--experimental-prompt")
    parser.add_argument("--experimental-adapter-mode")
    return parser


def run(
    argv: Sequence[str] | None = None, stdout: TextIO | None = None, stderr: TextIO | None = None
) -> int:
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    args = build_parser().parse_args(argv)
    if args.list_values:
        json.dump(list_values(), stdout)
        stdout.write("\n")
        return 0
    if any(
        value is not None
        for value in (
            args.experimental_provider,
            args.experimental_model,
            args.experimental_profile,
            args.experimental_prompt,
            args.experimental_adapter_mode,
        )
    ):
        stderr.write(
            "experimental provider runtime is not implemented in python-stakeholder; use javascript-stakeholder for provider-backed runs\n"
        )
        return 2
    config = SessionConfig(
        dev_type=DevelopmentType(args.dev_type),
        jargon_level=JargonLevel(args.jargon),
        complexity=Complexity(args.complexity),
        duration_seconds=args.duration,
        alerts_enabled=args.alerts,
        project_name=args.project,
        minimal_output=args.minimal,
        team_activity=args.team,
        framework=args.framework,
        seed=args.seed,
        output_format=OutputFormat(args.output_format),
        no_color=args.no_color,
        trace=args.trace,
    )
    if config.output_format is OutputFormat.JSON:
        json.dump(serialize_events(run_session(config)), stdout)
        stdout.write("\n")
        return 0
    for line in text_lines(config):
        stdout.write(f"{line}\n")
    return 0


def main() -> int:
    return run()
