#!/usr/bin/env python3
"""
Estimate effective confidence of a TARA after elapsed time/ticks.

Usage:
    python tools/drift.py examples/fast-to-meso.json --elapsed-ticks 50
    python tools/drift.py examples/fast-to-meso.json --elapsed-ticks 200
    python tools/drift.py examples/fast-to-meso-gear-coupled.json --elapsed-ticks 30
"""

import argparse
import json
import math
import sys
from pathlib import Path


def get_drift_params(tara):
    """Extract drift rate and decay model from a TARA."""
    drift = tara["driftEstimate"]

    if isinstance(drift, (int, float)):
        return drift, "exponential", {}

    overall = drift["overall"]
    model = drift.get("decayModel", "exponential")
    per_field = drift.get("perField", {})
    return overall, model, per_field


def get_validity_ticks(tara):
    """Extract validity window in ticks, if available."""
    vw = tara.get("validityWindow")
    if vw and "ticks" in vw:
        return vw["ticks"]
    return None


def decay(confidence, drift_rate, elapsed, model):
    """Apply decay model to confidence."""
    if model == "exponential":
        return confidence * math.exp(-drift_rate * elapsed)
    elif model == "linear":
        return max(0.0, confidence - drift_rate * elapsed)
    elif model == "step":
        # Step model: confidence holds until validity window, then drops to 0
        # Without a validity window, step is equivalent to no decay
        return confidence
    else:
        raise ValueError(f"Unknown decay model: {model}")


def main():
    parser = argparse.ArgumentParser(description="Estimate TARA drift decay")
    parser.add_argument("file", help="TARA JSON file")
    parser.add_argument("--elapsed-ticks", type=float, required=True,
                        help="Number of ticks elapsed since emission")
    args = parser.parse_args()

    with open(args.file) as f:
        tara = json.load(f)

    confidence = tara["confidence"]
    drift_rate, model, per_field = get_drift_params(tara)
    validity_ticks = get_validity_ticks(tara)
    elapsed = args.elapsed_ticks

    label = Path(args.file).name

    print(f"TARA: {label}")
    print(f"  Original confidence: {confidence}")
    print(f"  Drift rate (overall): {drift_rate}")
    print(f"  Decay model: {model}")
    print(f"  Elapsed ticks: {elapsed}")

    if validity_ticks is not None:
        print(f"  Validity window: {validity_ticks} ticks")

    # Check validity window
    expired = False
    if validity_ticks is not None and elapsed > validity_ticks:
        expired = True

    # Overall effective confidence
    if model == "step":
        if expired:
            effective = 0.0
        else:
            effective = confidence
    else:
        effective = decay(confidence, drift_rate, elapsed, model)

    print()
    if expired:
        print(f"  EXPIRED — elapsed ({elapsed}) exceeds validity window ({validity_ticks})")
        print(f"  Effective confidence: 0.000 (stale)")
    else:
        print(f"  Effective confidence: {effective:.4f}")
        if effective < 0.1:
            print(f"  WARNING: confidence below 0.1 — array is near-useless")
        elif effective < 0.5:
            print(f"  CAUTION: confidence below 0.5 — treat with skepticism")

    # Per-field breakdown
    if per_field:
        print()
        print("  Per-field effective confidence:")
        for field, field_drift in sorted(per_field.items()):
            if expired:
                field_eff = 0.0
            else:
                field_eff = decay(confidence, field_drift, elapsed, model)
            status = ""
            if field_eff < 0.1:
                status = " [near-useless]"
            elif field_eff < 0.5:
                status = " [skeptical]"
            print(f"    {field:20s}: {field_eff:.4f}{status}")

    # Return non-zero if expired
    sys.exit(1 if expired else 0)


if __name__ == "__main__":
    main()
