#!/usr/bin/env python3
"""Reproduce every figure and fitted number in the paper from the raw trials.

Pre-registered before any measurement exists. The procedures fixed here are the
ones reported.

Four hypotheses are tested, and the decisive test is a single linearisation.
Writing the normalised geometric factor

    G(d) = ( a^2 / (a^2 + d^2) )^3      -- equals g(d)^2 scaled to G(0) = 1

the threshold condition at the trigger point becomes, in each case:

    H0  ratiometric threshold      G = constant                 flat line
    H1  fixed threshold, far field G = k * (1/V)                through origin
    H2  fixed threshold, exact     G = k * (1/V)                through origin
    H3  oscillator margin          G = A * (1 - V*/V)           negative slope,
                                                                x-intercept 1/V*

so plotting G against 1/V separates all four by the *shape* of one line, before
any slope is compared with a predicted number. For H3 the x-intercept gives V*,
which is independently measurable by sweeping the supply down with no target.

Run from the repository root:

    python analysis/make_figures.py

The script refuses to invent anything. With no data rows it says so and stops.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import ScalarFormatter, NullFormatter  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "raw_measurements.csv")
FIGDIR = os.path.join(ROOT, "figures")
RIG = os.path.join(ROOT, "analysis", "rig_constants.json")

COLUMNS = ["trial_id", "order", "mode", "voltage_V", "distance_mm",
           "edge_rate", "temp_C", "target", "notes"]

# Pre-registered exclusion rule. A trial is dropped only if its notes carry an
# explicit tag written before the value was read. Nothing is dropped for its
# value. Every analysis is reported with and without the excluded trials.
EXCLUSION_TAGS = ("EXCLUDE:",)

C_H0, C_H1, C_H2, C_H3 = "#2f855a", "#2b6cb0", "#6b46c1", "#9b2c2c"
C_FIT, C_DATA = "#b7791f", "#1a1a1a"


# --------------------------------------------------------------------------- #
# geometry
# --------------------------------------------------------------------------- #

def G(d_mm, a_mm):
    """Normalised geometric factor, G(0) = 1, far-field limit (a/d)^6."""
    a2 = float(a_mm) ** 2
    return (a2 / (a2 + np.asarray(d_mm, dtype=float) ** 2)) ** 3


def n_eff(a_mm, d_mm):
    """-d ln G / d ln d. Six in the far field, smaller near the coil."""
    return 6.0 * d_mm ** 2 / (a_mm ** 2 + d_mm ** 2)


def slope_fixed_threshold(a_mm, d_mm):
    """H2 slope 1/n_eff; equivalently (1/6)(1 + a^2/d^2). H1 is its a->0 limit."""
    return 1.0 / n_eff(a_mm, d_mm)


def slope_h3(a_mm, d_mm, v, v_star):
    """H3 slope: negative, steepening as V approaches V*."""
    return -(v_star / (v - v_star)) / n_eff(a_mm, d_mm)


# --------------------------------------------------------------------------- #
# input
# --------------------------------------------------------------------------- #

def load_rig_constants():
    if not os.path.exists(RIG):
        return {}
    with open(RIG) as fh:
        return json.load(fh)


def _num(s):
    s = (s or "").strip()
    return float(s) if s else math.nan


def load_trials(path=DATA):
    """Returns (kept, excluded, malformed)."""
    if not os.path.exists(path):
        sys.exit(f"no data file at {path}")

    kept, excluded, malformed = [], [], []
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        missing = set(COLUMNS) - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"data file is missing columns: {sorted(missing)}")

        for row in reader:
            try:
                row["voltage_V"] = _num(row["voltage_V"])
                row["distance_mm"] = _num(row["distance_mm"])
                row["edge_rate"] = _num(row["edge_rate"])
                row["temp_C"] = _num(row["temp_C"])
                row["order"] = int(row["order"]) if row["order"].strip() else -1
                row["mode"] = (row["mode"] or "").strip().lower()
            except (ValueError, KeyError, AttributeError):
                malformed.append(row)
                continue
            if any(tag in (row.get("notes") or "") for tag in EXCLUSION_TAGS):
                excluded.append(row)
                continue
            kept.append(row)

    return kept, excluded, malformed


def by_mode(trials, mode):
    return [t for t in trials if t["mode"] == mode]


# --------------------------------------------------------------------------- #
# fitting
# --------------------------------------------------------------------------- #

def ols(x, y):
    """Least squares of y on x with the textbook standard errors."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    good = np.isfinite(x) & np.isfinite(y)
    x, y = x[good], y[good]
    n = x.size
    if n < 3:
        return None
    sxx = np.sum((x - x.mean()) ** 2)
    if sxx <= 0:
        return None
    slope = np.sum((x - x.mean()) * (y - y.mean())) / sxx
    intercept = y.mean() - slope * x.mean()
    resid = y - (intercept + slope * x)
    dof = n - 2
    s2 = np.sum(resid ** 2) / dof if dof > 0 else float("nan")
    se_slope = math.sqrt(s2 / sxx) if dof > 0 else float("nan")
    se_inter = (math.sqrt(s2 * (1.0 / n + x.mean() ** 2 / sxx))
                if dof > 0 else float("nan"))
    cov_si = -s2 * x.mean() / sxx if dof > 0 else float("nan")
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 - np.sum(resid ** 2) / ss_tot if ss_tot > 0 else float("nan")
    return {"slope": slope, "intercept": intercept, "se_slope": se_slope,
            "se_intercept": se_inter, "cov_slope_intercept": cov_si,
            "n": int(n), "r2": r2, "resid": resid, "x": x, "y": y}


def ols_loglog(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    good = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    if good.sum() < 3:
        return None
    return ols(np.log(x[good]), np.log(y[good]))


def v_star_from_fit(fit):
    """x-intercept of G against 1/V, inverted. Returns (V*, sigma).

    G = intercept + slope*(1/V); G = 0 at 1/V = -intercept/slope, so
    V* = -slope/intercept. Uncertainty by first-order propagation, keeping the
    slope-intercept covariance, which is large here and cannot be dropped.
    """
    m, b = fit["slope"], fit["intercept"]
    if not (m < 0 < b):
        return None  # not an H3-shaped line: no positive x-intercept
    v_star = -m / b
    dvdm, dvdb = -1.0 / b, m / b ** 2
    var = (dvdm ** 2 * fit["se_slope"] ** 2
           + dvdb ** 2 * fit["se_intercept"] ** 2
           + 2 * dvdm * dvdb * fit["cov_slope_intercept"])
    return v_star, (math.sqrt(var) if var > 0 else float("nan"))


# --------------------------------------------------------------------------- #
# plotting
# --------------------------------------------------------------------------- #

def style(ax):
    ax.grid(True, which="both", lw=0.4, alpha=0.3)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def plain_log_ticks(ax, values, axis):
    target = ax.xaxis if axis == "x" else ax.yaxis
    target.set_major_formatter(ScalarFormatter())
    target.set_minor_formatter(NullFormatter())
    target.set_major_locator(plt.FixedLocator(sorted(set(values))))
    target.set_minor_locator(plt.NullLocator())


def figure_linearisation(primary, rig, results):
    """The decisive test: G against 1/V. Shape alone separates H0, H1/H2, H3."""
    a_mm = rig.get("coil_radius_mm")
    if not a_mm:
        return "coil_radius_mm is null in analysis/rig_constants.json"
    pts = [(t["distance_mm"], t["voltage_V"]) for t in primary
           if math.isfinite(t["distance_mm"]) and math.isfinite(t["voltage_V"])
           and t["voltage_V"] > 0]
    if len(pts) < 3:
        return "fewer than three usable primary trials"

    d = np.array([p[0] for p in pts])
    v = np.array([p[1] for p in pts])
    x, y = 1.0 / v, G(d, a_mm)
    fit = ols(x, y)
    if fit is None:
        return "primary trials do not span a range of voltages"

    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.plot(x, y, marker="o", ls="none", ms=5.5, color=C_DATA,
            label=f"trigger points (n={len(pts)})")

    xs = np.linspace(0.0, max(x) * 1.12, 100)
    ax.plot(xs, fit["intercept"] + fit["slope"] * xs, lw=1.8, color=C_FIT,
            label="fit")

    # Hypothesis shapes, each anchored to the data so the comparison is of form.
    ax.axhline(float(np.mean(y)), ls="-", lw=1.0, color=C_H0,
               label="H0: flat")
    k = float(np.sum(x * y) / np.sum(x * x))          # best line through origin
    ax.plot(xs, k * xs, ls="--", lw=1.2, color=C_H1,
            label="H1/H2: through origin, positive slope")

    vs = v_star_from_fit(fit)
    if vs:
        v_star, sig = vs
        ax.axvline(1.0 / v_star, ls=":", lw=1.3, color=C_H3)
        ax.annotate(f"1/V* = {1/v_star:.4f}\nV* = {v_star:.3f} +/- {sig:.3f} V",
                    xy=(1.0 / v_star, ax.get_ylim()[1] * 0.72), fontsize=8,
                    color=C_H3, ha="left" if 1 / v_star < max(x) else "right")
        results["v_star_fitted"] = {"value": v_star, "sigma": sig}
    ax.axhline(0.0, lw=0.7, color="#888888")

    ax.set_xlabel("1 / V at the trigger point   (V^-1)")
    ax.set_ylabel("G(d) = (a² / (a² + d²))³")
    ax.set_title("Decisive test: hypothesis shape, before any slope comparison",
                 fontsize=11)
    ax.legend(fontsize=7.5, frameon=False, loc="best")
    style(ax)
    fig.tight_layout()
    out = os.path.join(FIGDIR, "linearisation.png")
    fig.savefig(out, dpi=200)
    plt.close(fig)
    results["linearisation_fit"] = {k2: fit[k2] for k2 in
                                    ("slope", "intercept", "se_slope",
                                     "se_intercept", "n", "r2")}
    return out


def figure_range_vs_voltage(trials, rig, results, tag="range_vs_voltage"):
    fit = ols_loglog([t["voltage_V"] for t in trials],
                     [t["distance_mm"] for t in trials])
    pts = [(t["voltage_V"], t["distance_mm"]) for t in trials
           if math.isfinite(t["voltage_V"]) and math.isfinite(t["distance_mm"])
           and t["voltage_V"] > 0 and t["distance_mm"] > 0]
    if len(pts) < 2:
        return "no usable distance measurements"

    buckets = {}
    for v, dd in pts:
        buckets.setdefault(v, []).append(dd)
    vs = sorted(buckets)
    ms = [float(np.mean(buckets[v])) for v in vs]
    sds = [float(np.std(buckets[v], ddof=1)) if len(buckets[v]) > 1 else 0.0
           for v in vs]

    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=".", ls="none",
            ms=5, alpha=0.35, color="#555555",
            label=f"individual trials (n={len(pts)})")
    ax.errorbar(vs, ms, yerr=sds, marker="o", ms=5, lw=1.2, capsize=3,
                color=C_DATA, label="mean +/- 1 sd per voltage")

    v0, d0 = vs[0], ms[0]
    grid = np.linspace(min(vs), max(vs), 60)
    a_mm = rig.get("coil_radius_mm")
    d_ref = float(rig.get("nominal_range_mm") or d0)

    ax.axhline(d0, lw=1.0, color=C_H0, alpha=0.8, label="H0: slope 0")
    ax.plot(grid, d0 * (grid / v0) ** (1 / 6), ls="--", lw=1.1, color=C_H1,
            label="H1: slope 0.167")
    if a_mm:
        s2 = slope_fixed_threshold(float(a_mm), d_ref)
        ax.plot(grid, d0 * (grid / v0) ** s2, ls="-.", lw=1.1, color=C_H2,
                label=f"H2: slope {s2:.3f}")
        vstar = (results.get("v_star_fitted") or {}).get("value") \
            or rig.get("v_star_measured")
        if vstar and min(vs) > float(vstar):
            s3 = slope_h3(float(a_mm), d_ref, float(np.mean(vs)), float(vstar))
            ax.plot(grid, d0 * (grid / v0) ** s3, ls=":", lw=1.4, color=C_H3,
                    label=f"H3: slope {s3:.3f} (V*={float(vstar):.2f} V)")
    if fit:
        ax.plot(grid, math.exp(fit["intercept"]) * grid ** fit["slope"],
                lw=1.7, color=C_FIT,
                label=f"fit: {fit['slope']:.3f} +/- {fit['se_slope']:.3f}")

    ax.set_xlabel("supply voltage at module terminals   V")
    ax.set_ylabel("detection distance   mm")
    ax.set_title("Detection range against supply voltage", fontsize=11)
    ax.legend(fontsize=7, frameon=False, loc="best")
    style(ax)
    plain_log_ticks(ax, vs, "x")
    plain_log_ticks(ax, [round(m) for m in ms], "y")
    fig.tight_layout()
    out = os.path.join(FIGDIR, f"{tag}.png")
    fig.savefig(out, dpi=200)
    plt.close(fig)
    if fit:
        results[f"{tag}_fit"] = {k: fit[k] for k in
                                 ("slope", "se_slope", "n", "r2")}
    return out


def figure_drift_check(trials, results):
    sel = [t for t in trials if t["order"] >= 0
           and math.isfinite(t["distance_mm"]) and math.isfinite(t["voltage_V"])]
    if len(sel) < 4:
        return None
    fit = ols_loglog([t["voltage_V"] for t in sel],
                     [t["distance_mm"] for t in sel])
    if not fit:
        return None
    order = np.array([t["order"] for t in sel], dtype=float)
    order = order[:fit["resid"].size]
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.plot(order, fit["resid"], marker="o", ls="none", ms=4, color=C_DATA)
    ax.axhline(0.0, lw=0.9, color=C_H3)
    trend = ols(order, fit["resid"])
    if trend:
        results["drift_slope_per_trial"] = {
            "value": trend["slope"], "sigma": trend["se_slope"]}
        ax.plot(order, trend["intercept"] + trend["slope"] * order, lw=1.2,
                color=C_FIT,
                label=f"drift {trend['slope']:+.2e} +/- {trend['se_slope']:.1e} per trial")
        ax.legend(fontsize=7.5, frameon=False)
    ax.set_xlabel("trial order within the session")
    ax.set_ylabel("residual in ln(distance)")
    ax.set_title("Drift check: residual against measurement order", fontsize=11)
    style(ax)
    fig.tight_layout()
    out = os.path.join(FIGDIR, "drift_check.png")
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #

def main():
    os.makedirs(FIGDIR, exist_ok=True)
    rig = load_rig_constants()
    trials, excluded, malformed = load_trials()

    print(f"trials read      : {len(trials)}")
    print(f"excluded by rule : {len(excluded)}")
    print(f"malformed rows   : {len(malformed)}")

    if not trials:
        print("\nNo measurements in data/raw_measurements.csv.")
        print("Nothing is plotted and no numbers are reported, by design:")
        print("this script will not substitute, smooth or simulate data.")
        print("Add real trials to the CSV and run it again.")
        return 0

    results = {"n_trials": len(trials), "n_excluded": len(excluded)}
    primary = by_mode(trials, "primary")
    secondary = by_mode(trials, "secondary")
    no_target = by_mode(trials, "no_target")
    print(f"  primary {len(primary)}   secondary {len(secondary)}"
          f"   no_target {len(no_target)}")

    if no_target:
        vals = [t["voltage_V"] for t in no_target
                if math.isfinite(t["voltage_V"])]
        if vals:
            v_meas = float(np.mean(vals))
            sd = float(np.std(vals, ddof=1)) if len(vals) > 1 else float("nan")
            results["v_star_measured"] = {"value": v_meas, "sd": sd,
                                          "n": len(vals)}
            print(f"\nV* measured with no target : {v_meas:.3f} +/- {sd:.3f} V"
                  f"  (n={len(vals)})")

    if primary:
        print()
        out = figure_linearisation(primary, rig, results)
        lf = results.get("linearisation_fit")
        if lf:
            print(f"linearisation  slope {lf['slope']:.4e} "
                  f"+/- {lf['se_slope']:.1e}   intercept {lf['intercept']:.4e} "
                  f"+/- {lf['se_intercept']:.1e}   r2 {lf['r2']:.3f}")
            if lf["slope"] < 0 < lf["intercept"]:
                shape = "negative slope, positive intercept -> H3 shape"
            elif abs(lf["slope"]) < 2 * lf["se_slope"]:
                shape = "slope consistent with zero -> H0 shape"
            else:
                shape = "positive slope -> H1/H2 shape"
            print(f"               {shape}")
            results["shape_verdict"] = shape
        vsf = results.get("v_star_fitted")
        if vsf:
            print(f"               fitted V* = {vsf['value']:.3f} "
                  f"+/- {vsf['sigma']:.3f} V  (x-intercept)")
        vsm = results.get("v_star_measured")
        if vsf and vsm:
            diff = abs(vsf["value"] - vsm["value"])
            comb = math.hypot(vsf["sigma"], vsm["sd"] or 0.0)
            agree = diff < 2 * comb if comb > 0 else None
            results["v_star_agreement"] = {"difference": diff,
                                           "combined_sigma": comb,
                                           "within_2_sigma": agree}
            print(f"               fitted V* vs no-target V*: "
                  f"differ by {diff:.3f} V against {comb:.3f} V combined "
                  f"-> {'agree' if agree else 'DISAGREE'}")
        print(f"               figure -> {out}")
        print()
        print(f"primary range  -> {figure_range_vs_voltage(primary, rig, results, 'range_primary')}")
        rf = results.get("range_primary_fit")
        if rf:
            print(f"               log-log slope {rf['slope']:+.4f} "
                  f"+/- {rf['se_slope']:.4f}  (n={rf['n']}, r2={rf['r2']:.3f})")
            print("               note: in the primary design the measurement "
                  "error is in V, not d, so this slope is")
            print("               attenuated toward zero. Treat it as "
                  "conservative; the linearisation is the test.")

    if secondary:
        print()
        print(f"secondary range -> {figure_range_vs_voltage(secondary, rig, results, 'range_secondary')}")
        rf = results.get("range_secondary_fit")
        if rf:
            print(f"               log-log slope {rf['slope']:+.4f} "
                  f"+/- {rf['se_slope']:.4f}  (n={rf['n']}, r2={rf['r2']:.3f})")

    a_mm, d_ref = rig.get("coil_radius_mm"), rig.get("nominal_range_mm")
    if a_mm and d_ref:
        a_mm, d_ref = float(a_mm), float(d_ref)
        ne = n_eff(a_mm, d_ref)
        results["n_eff"] = ne
        results["predicted_slopes"] = {"H0": 0.0, "H1": 1 / 6,
                                       "H2": slope_fixed_threshold(a_mm, d_ref)}
        print(f"\npredicted      n_eff {ne:.3f}   H0 0   H1 {1/6:.4f}   "
              f"H2 {slope_fixed_threshold(a_mm, d_ref):.4f}")
        vstar = (results.get("v_star_fitted") or {}).get("value")
        if vstar:
            s3 = slope_h3(a_mm, d_ref, 3.7, float(vstar))
            results["predicted_slopes"]["H3_at_3.7V"] = s3
            print(f"               H3 at 3.7 V with fitted V* : {s3:+.4f}")

    out_d = figure_drift_check(trials, results)
    if out_d:
        print(f"\ndrift          figure -> {out_d}")

    with open(os.path.join(ROOT, "analysis", "results.json"), "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("\nnumbers -> analysis/results.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
