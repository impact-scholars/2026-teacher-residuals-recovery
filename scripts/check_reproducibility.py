#!/usr/bin/env python3
"""Lightweight reviewer check for the RNNematode micropublication package.

This script intentionally does not retrain policies and does not require LaTeX.
It validates the packaged result tables and regenerates a small CSV summary from
saved BrainCAD/ReflexBench artifacts bundled with the submission.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ROOT / "derived_tables" / "humanoid20_key_results.csv",
    ROOT / "derived_tables" / "cross_environment_summary_micropublication.csv",
    ROOT / "derived_tables" / "morphology_vs_benefit.csv",
    ROOT / "video_index" / "representative_video_index.csv",
    ROOT / "Figures" / "RNNematode-Figures.svg",
]
OUT = ROOT / "reproducibility_check_outputs"


def read_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def as_float(row, key):
    try:
        return float(row[key])
    except Exception as exc:
        raise RuntimeError(f"Could not parse numeric column {key!r} in row {row}") from exc


def main():
    missing = [p for p in REQUIRED if not p.exists()]
    if missing:
        msg = "\n".join(f"- {p.relative_to(ROOT)}" for p in missing)
        raise FileNotFoundError(
            "Missing required packaged artifacts:\n"
            f"{msg}\n"
            "Run from the released repository root, or restore these files from the submission archive."
        )

    key = read_csv(ROOT / "derived_tables" / "humanoid20_key_results.csv")
    headline = []
    for comparison in ["imitation_on_minus_off", "consolidated_minus_baseline"]:
        for metric in ["fall", "return"]:
            rows = [r for r in key if r.get("comparison") == comparison and r.get("metric") == metric]
            if not rows:
                raise RuntimeError(f"No rows found for {comparison} / {metric}")
            for r in rows:
                headline.append(
                    {
                        "comparison": comparison,
                        "metric": metric,
                        "sweep_type": r["sweep_type"],
                        "mean": f"{as_float(r, 'mean'):.6g}",
                        "ci_low": f"{as_float(r, 'ci_low'):.6g}",
                        "ci_high": f"{as_float(r, 'ci_high'):.6g}",
                        "n": r.get("n", ""),
                    }
                )

    # Basic sign checks matching the micropublication claim.
    im_fall = [as_float(r, "mean") for r in key if r.get("comparison") == "imitation_on_minus_off" and r.get("metric") == "fall"]
    im_return = [as_float(r, "mean") for r in key if r.get("comparison") == "imitation_on_minus_off" and r.get("metric") == "return"]
    if not im_fall or not all(v < 0 for v in im_fall):
        raise AssertionError("Expected imitation ON-OFF fall-AUC deltas to be negative.")
    if not im_return or not all(v > 0 for v in im_return):
        raise AssertionError("Expected imitation ON-OFF return-AUC deltas to be positive.")

    videos = read_csv(ROOT / "video_index" / "representative_video_index.csv")
    OUT.mkdir(exist_ok=True)
    out_csv = OUT / "headline_recomputed_from_packaged_tables.csv"
    with out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(headline[0].keys()))
        writer.writeheader()
        writer.writerows(headline)

    summary = {
        "status": "ok",
        "package_root": ".",
        "checked_files": [str(p.relative_to(ROOT)) for p in REQUIRED],
        "headline_rows": len(headline),
        "video_index_rows": len(videos),
        "outputs": [str(out_csv.relative_to(ROOT))],
        "note": "This check validates packaged result artifacts only; it does not retrain policies.",
    }
    out_json = OUT / "reproducibility_check_summary.json"
    out_json.write_text(json.dumps(summary, indent=2) + "\n")
    print("RNNematode reproducibility check: OK")
    print(f"Wrote {out_csv.relative_to(ROOT)}")
    print(f"Wrote {out_json.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
