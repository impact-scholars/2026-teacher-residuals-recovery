#!/usr/bin/env python3
"""Generate lightweight scientific plots from packaged result tables.

The goal is not to recreate every publication panel. It is to prove that the
released tables are executable scientific artifacts: from CSV -> plotted result,
with no training and no third-party plotting dependency.
"""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated_plots"

TEAL = "#009688"
TEAL2 = "#35a99c"
ORANGE = "#ff8a1d"
BLUE = "#2b7bba"
RED = "#cf2e2e"
INK = "#1f2428"
GRID = "#ded8cd"
BG = "#ffffff"


def read_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required table: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def f(row, key):
    try:
        return float(row[key])
    except Exception as exc:
        raise RuntimeError(f"Could not parse {key!r} in {row}") from exc


def svg_text(x, y, text, size=14, weight="400", anchor="middle", color=INK):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{text}</text>'


def nice_ticks(vmin, vmax, n=5):
    if vmax <= vmin:
        vmax = vmin + 1
    span = vmax - vmin
    raw = span / max(1, n - 1)
    mag = 10 ** math.floor(math.log10(abs(raw))) if raw else 1
    step = min([1, 2, 5, 10], key=lambda x: abs(x * mag - raw)) * mag
    lo = math.floor(vmin / step) * step
    hi = math.ceil(vmax / step) * step
    ticks = []
    t = lo
    while t <= hi + 1e-9:
        ticks.append(t)
        t += step
    return ticks


def bar_chart(path, title, groups, series, y_label, higher_text, y_min=None, y_max=None):
    # series = [(label, color, [values], [ci_low], [ci_high])]
    W, H = 980, 560
    ml, mr, mt, mb = 95, 45, 75, 105
    pw, ph = W - ml - mr, H - mt - mb
    vals = []
    for _, _, ys, lows, highs in series:
        vals.extend(ys)
        vals.extend(lows)
        vals.extend(highs)
    if y_min is None:
        y_min = min(vals + [0])
    if y_max is None:
        y_max = max(vals + [0])
    pad = 0.08 * (y_max - y_min if y_max > y_min else 1)
    y_min -= pad
    y_max += pad
    ticks = nice_ticks(y_min, y_max, 6)
    y_min, y_max = min(ticks), max(ticks)

    def X(i, j):
        group_w = pw / len(groups)
        bar_w = min(80, group_w / (len(series) + 1.2))
        start = ml + i * group_w + group_w / 2 - bar_w * len(series) / 2
        return start + j * bar_w

    def Y(v):
        return mt + ph - (v - y_min) / (y_max - y_min) * ph

    elems = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', f'<rect width="100%" height="100%" fill="{BG}"/>']
    elems.append(svg_text(W/2, 36, title, 26, "700"))
    elems.append(svg_text(W/2, H-18, higher_text, 13, "400", color="#5f6c72"))
    for t in ticks:
        y = Y(t)
        elems.append(f'<line x1="{ml}" x2="{W-mr}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        label = f"{t:.0f}" if abs(t) >= 10 else f"{t:.2f}".rstrip("0").rstrip(".")
        elems.append(svg_text(ml-12, y+5, label, 13, anchor="end", color="#445057"))
    elems.append(f'<line x1="{ml}" x2="{W-mr}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" stroke="{INK}" stroke-width="1.6"/>')
    elems.append(f'<line x1="{ml}" x2="{ml}" y1="{mt}" y2="{mt+ph}" stroke="{INK}" stroke-width="1.5"/>')
    elems.append(svg_text(24, mt+ph/2, y_label, 16, "600", anchor="middle"))
    elems[-1] = elems[-1].replace('text-anchor="middle"', 'text-anchor="middle" transform="rotate(-90 24 %.1f)"' % (mt+ph/2))

    for i, g in enumerate(groups):
        group_w = pw / len(groups)
        elems.append(svg_text(ml + i*group_w + group_w/2, H-65, g, 16, "500"))
        for j, (label, color, ys, lows, highs) in enumerate(series):
            x = X(i, j)
            bar_w = min(80, group_w / (len(series) + 1.2)) * 0.82
            y0 = Y(0)
            yv = Y(ys[i])
            top = min(y0, yv)
            height = abs(y0-yv)
            elems.append(f'<rect x="{x:.1f}" y="{top:.1f}" width="{bar_w:.1f}" height="{height:.1f}" fill="{color}"/>')
            cx = x + bar_w/2
            yl, yh = Y(lows[i]), Y(highs[i])
            elems.append(f'<line x1="{cx:.1f}" x2="{cx:.1f}" y1="{yh:.1f}" y2="{yl:.1f}" stroke="{INK}" stroke-width="2"/>')
            elems.append(f'<line x1="{cx-8:.1f}" x2="{cx+8:.1f}" y1="{yh:.1f}" y2="{yh:.1f}" stroke="{INK}" stroke-width="2"/>')
            elems.append(f'<line x1="{cx-8:.1f}" x2="{cx+8:.1f}" y1="{yl:.1f}" y2="{yl:.1f}" stroke="{INK}" stroke-width="2"/>')
    lx = W - mr - 260
    ly = 76
    for k, (label, color, *_rest) in enumerate(series):
        elems.append(f'<rect x="{lx}" y="{ly + k*25}" width="18" height="14" fill="{color}"/>')
        elems.append(svg_text(lx+28, ly+12+k*25, label, 14, anchor="start"))
    elems.append('</svg>')
    path.write_text("\n".join(elems) + "\n")


def humanoid_main():
    rows = read_csv(ROOT / "derived_tables" / "humanoid20_key_results.csv")
    groups = ["push", "sensor", "slip"]
    def get(comp, metric):
        vals, lows, highs = [], [], []
        for g in groups:
            r = next(x for x in rows if x["comparison"] == comp and x["metric"] == metric and x["sweep_type"] == g)
            vals.append(f(r, "mean")); lows.append(f(r, "ci_low")); highs.append(f(r, "ci_high"))
        return vals, lows, highs
    vals, lows, highs = get("imitation_on_minus_off", "fall")
    red_vals = [-v for v in vals]
    red_lows = [-h for h in highs]
    red_highs = [-l for l in lows]
    cvals, clows, chighs = get("consolidated_minus_baseline", "fall")
    cred_vals = [-v for v in cvals]
    cred_lows = [-h for h in chighs]
    cred_highs = [-l for l in clows]
    bar_chart(OUT / "humanoid_fall_auc_reduction.svg", "Humanoid: teacher-guided residual reduces falls", groups,
              [("imitation ON-OFF", TEAL, red_vals, red_lows, red_highs), ("consolidated-baseline", TEAL2, cred_vals, cred_lows, cred_highs)],
              "fall-AUC reduction", "Higher means fewer falls; error bars are paired bootstrap 95% CIs")
    rvals, rlows, rhighs = get("imitation_on_minus_off", "return")
    crvals, crlows, crhighs = get("consolidated_minus_baseline", "return")
    bar_chart(OUT / "humanoid_return_auc_gain.svg", "Humanoid: robustness did not require a return cost", groups,
              [("imitation ON-OFF", ORANGE, rvals, rlows, rhighs), ("consolidated-baseline", "#f6b54b", crvals, crlows, crhighs)],
              "return-AUC gain", "Higher means better return; error bars are paired bootstrap 95% CIs")


def teacher_quality():
    rows = read_csv(ROOT / "derived_tables" / "teacher_quality_replication_summary.csv")
    groups = ["push", "sensor", "slip"]
    series = []
    for variant, color in [("T_full", TEAL), ("T_weak", RED)]:
        vals = []; lows = []; highs = []
        for g in groups:
            candidates = [r for r in rows if r.get("teacher_variant") == variant and r.get("sweep_type") == g]
            if not candidates:
                raise RuntimeError(f"No teacher-quality row for {variant} / {g}")
            r = candidates[0]
            vals.append(-f(r, "delta_auc_fall_mean"))
            lows.append(-f(r, "delta_auc_fall_ci_high"))
            highs.append(-f(r, "delta_auc_fall_ci_low"))
        series.append(("strong teacher" if variant == "T_full" else "weak teacher", color, vals, lows, highs))
    bar_chart(OUT / "teacher_quality_fall_reduction.svg", "Teacher quality changes the sign of the correction", groups, series,
              "student fall-AUC reduction", "Positive values indicate the residual helped; negative values indicate harm")
    return True


def cross_env():
    rows = read_csv(ROOT / "derived_tables" / "cross_environment_summary_micropublication.csv")
    envs = []
    for preferred in ["Humanoid", "Walker2d", "Ant", "Hopper", "humanoid", "walker2d", "ant", "hopper"]:
        if any((r.get("env") or r.get("env_id") or "") == preferred for r in rows) and preferred.lower() not in [e.lower() for e in envs]:
            envs.append(preferred)
    if not envs:
        seen = []
        for r in rows:
            e = r.get("env") or r.get("env_id")
            if e and e not in seen:
                seen.append(e)
        envs = seen[:4]
    vals = []; lows = []; highs = []
    for e in envs:
        candidates = [
            r for r in rows
            if (r.get("env") or r.get("env_id")) == e
            and r.get("metric") == "fall"
            and r.get("source") == "imitation_on_minus_off"
        ]
        if not candidates:
            raise RuntimeError(f"No imitation fall row for {e}")
        r = candidates[0]
        val = f(r, "mean")
        sem = f(r, "sem") if r.get("sem") else 0.0
        vals.append(-val)
        lows.append(-(val + sem))
        highs.append(-(val - sem))
    bar_chart(OUT / "cross_environment_fall_reduction.svg", "Cross-environment fall reduction summary", envs,
              [("imitation ON-OFF", BLUE, vals, lows, highs)], "fall-AUC reduction", "Exploratory cross-body summary; higher means fewer falls")


def main():
    OUT.mkdir(exist_ok=True)
    humanoid_main()
    teacher_quality()
    cross_env()
    manifest = OUT / "plot_manifest.csv"
    plots = sorted(OUT.glob("*.svg"))
    with manifest.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["plot", "source_tables"])
        for p in plots:
            w.writerow([str(p.relative_to(ROOT)), "derived_tables/*.csv"])
    print("Generated scientific plots:")
    for p in plots:
        print(f"- {p.relative_to(ROOT)}")
    print(f"Wrote {manifest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
