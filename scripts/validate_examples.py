#!/usr/bin/env python3

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    (
        ROOT / "schemas" / "collector-export.schema.json",
        ROOT / "examples" / "collector" / "forever-observation-batch.json",
    ),
    (
        ROOT / "schemas" / "datasets" / "entity-observations.schema.json",
        ROOT / "examples" / "datasets" / "forever-spell-observations.json",
    ),
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(schema_path, example_path):
    schema = load_json(schema_path)
    instance = load_json(example_path)

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )

    if errors:
        messages = []
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path)
            if not location:
                location = "<root>"
            messages.append(
                f"{example_path.relative_to(ROOT)}:{location}: {error.message}"
            )
        raise ValueError("\n".join(messages))

    print(
        f"Valid: {example_path.relative_to(ROOT)} "
        f"against {schema_path.relative_to(ROOT)}"
    )


def main():
    for schema_path, example_path in CASES:
        validate(schema_path, example_path)


if __name__ == "__main__":
    main()
