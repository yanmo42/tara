#!/usr/bin/env python3
"""
Compose two TARA JSON files into a single composed TARA.

Usage:
    python tools/compose.py first.json second.json
    python tools/compose.py first.json second.json -o composed.json
    python tools/compose.py step1.json step2.json step3.json   # chain of 3+
"""

import argparse
import json
import sys
from pathlib import Path


TRUST_ORDER = ["self", "neighbor", "external", "synthetic"]
DECAY_ORDER = ["step", "linear", "exponential"]


def arc_id(arc):
    """Extract the id from a string or structured arc."""
    if isinstance(arc, str):
        return arc
    return arc.get("id", "")


def compose_confidence(a, b):
    return round(a * b, 6)


def compose_drift(a, b):
    """Compose drift estimates (number or structured object)."""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return round(a + b, 6)

    # Normalize to objects
    def to_obj(d):
        if isinstance(d, (int, float)):
            return {"overall": d}
        return d

    ao, bo = to_obj(a), to_obj(b)
    result = {"overall": round(ao["overall"] + bo["overall"], 6)}

    # Merge perField
    pf_a = ao.get("perField", {})
    pf_b = bo.get("perField", {})
    if pf_a or pf_b:
        merged = {}
        for k in set(list(pf_a.keys()) + list(pf_b.keys())):
            merged[k] = round(pf_a.get(k, 0) + pf_b.get(k, 0), 6)
        result["perField"] = merged

    # Take faster decay model
    dm_a = ao.get("decayModel")
    dm_b = bo.get("decayModel")
    if dm_a and dm_b:
        result["decayModel"] = dm_a if DECAY_ORDER.index(dm_a) > DECAY_ORDER.index(dm_b) else dm_b
    elif dm_a or dm_b:
        result["decayModel"] = dm_a or dm_b

    return result


def compose_loss_notes(a, b, intermediate_id):
    """Merge loss notes, deduplicate, and add composition loss."""
    notes_a = a or []
    notes_b = b or []
    seen = set()
    merged = []
    for note in notes_a + notes_b:
        if note not in seen:
            seen.add(note)
            merged.append(note)
    comp_note = f"intermediate representation at {intermediate_id} consumed and not preserved"
    if comp_note not in seen:
        merged.append(comp_note)
    return merged


def compose_validity_window(a, b):
    """Take the minimum validity window."""
    if a is None:
        return b
    if b is None:
        return a
    result = {}
    if "ticks" in a and "ticks" in b:
        result["ticks"] = min(a["ticks"], b["ticks"])
    elif "ticks" in a:
        result["ticks"] = a["ticks"]
    elif "ticks" in b:
        result["ticks"] = b["ticks"]
    if "duration" in a and "duration" in b:
        # Simple lexicographic comparison works for ISO 8601 durations of same type
        result["duration"] = min(a["duration"], b["duration"])
    elif "duration" in a:
        result["duration"] = a["duration"]
    elif "duration" in b:
        result["duration"] = b["duration"]
    return result if result else None


def compose_trust_class(a, b):
    """Take the weakest trust class."""
    if a is None:
        return b
    if b is None:
        return a
    return a if TRUST_ORDER.index(a) > TRUST_ORDER.index(b) else b


def compose_two(first, second):
    """Compose two TARAs. Returns the composed TARA dict."""
    # Verify arc matching
    first_target = arc_id(first["targetArc"])
    second_source = arc_id(second["sourceArc"])
    if first_target != second_source:
        print(f"Error: targetArc of first ({first_target}) != sourceArc of second ({second_source})",
              file=sys.stderr)
        sys.exit(1)

    intermediate_id = first_target

    composed = {
        "sourceArc": first["sourceArc"],
        "targetArc": second["targetArc"],
        "timeMarker": second["timeMarker"],
        "stateSummary": second["stateSummary"],
        "confidence": compose_confidence(first["confidence"], second["confidence"]),
        "driftEstimate": compose_drift(first["driftEstimate"], second["driftEstimate"]),
        "reconstructionTarget": second["reconstructionTarget"],
        "lossNotes": compose_loss_notes(
            first.get("lossNotes"), second.get("lossNotes"), intermediate_id
        ),
        "provenance": {
            "emitter": "composed",
            "method": "tara-composition",
            "chain": [first.get("provenance", {}), second.get("provenance", {})]
        }
    }

    # Optional fields
    tc = compose_trust_class(first.get("trustClass"), second.get("trustClass"))
    if tc:
        composed["trustClass"] = tc

    vw = compose_validity_window(first.get("validityWindow"), second.get("validityWindow"))
    if vw:
        composed["validityWindow"] = vw

    return composed


def main():
    parser = argparse.ArgumentParser(description="Compose TARA JSON files")
    parser.add_argument("files", nargs="+", help="Two or more TARA JSON files to compose (in order)")
    parser.add_argument("-o", "--output", default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    if len(args.files) < 2:
        print("Error: need at least two TARA files to compose", file=sys.stderr)
        sys.exit(1)

    taras = []
    for filepath in args.files:
        with open(filepath) as f:
            taras.append(json.load(f))

    # Compose left to right
    result = taras[0]
    for i in range(1, len(taras)):
        result = compose_two(result, taras[i])

    output = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"Composed TARA written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
