#!/usr/bin/env python3
"""
Validate a TARA JSON file against the base or gear-coupled schema.

Usage:
    python tools/validate.py examples/fast-to-meso.json
    python tools/validate.py examples/fast-to-meso-gear-coupled.json --schema schemas/tara-gear-coupled.schema.json
    python tools/validate.py examples/*.json
"""

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"

GEAR_FIELDS = {"gearRatio", "phaseAlignment", "slippageTolerance",
               "informationCapacity", "cadenceHz", "steganographicEncoding",
               "mechanicalFailureModes"}


def load_registry():
    """Build a referencing.Registry with all schemas so $ref resolves."""
    resources = []
    for schema_path in SCHEMAS_DIR.glob("*.schema.json"):
        with open(schema_path) as f:
            schema = json.load(f)
        uri = schema_path.name
        resources.append((uri, Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def detect_schema(instance):
    """Auto-detect whether to use base or gear-coupled schema."""
    if instance.keys() & GEAR_FIELDS:
        return "tara-gear-coupled.schema.json"
    return "tara.schema.json"


def validate_file(filepath, schema_name=None):
    """Validate a single JSON file. Returns (ok, errors)."""
    filepath = Path(filepath)
    with open(filepath) as f:
        instance = json.load(f)

    if schema_name is None:
        schema_name = detect_schema(instance)

    schema_path = SCHEMAS_DIR / schema_name
    with open(schema_path) as f:
        schema = json.load(f)

    registry = load_registry()
    validator = Draft202012Validator(schema, registry=registry)
    errors = list(validator.iter_errors(instance))
    return len(errors) == 0, errors, schema_name


def main():
    parser = argparse.ArgumentParser(description="Validate TARA JSON files")
    parser.add_argument("files", nargs="+", help="JSON files to validate")
    parser.add_argument("--schema", default=None,
                        help="Schema filename (auto-detected if omitted)")
    args = parser.parse_args()

    all_ok = True
    for filepath in args.files:
        ok, errors, used_schema = validate_file(filepath, args.schema)
        label = Path(filepath).name
        if ok:
            print(f"  ok  {label}  ({used_schema})")
        else:
            all_ok = False
            print(f"FAIL  {label}  ({used_schema})")
            for err in errors:
                path = ".".join(str(p) for p in err.absolute_path) or "(root)"
                print(f"      {path}: {err.message}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
