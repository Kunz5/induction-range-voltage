# Does a draining battery shorten a metal detector's reach?

An induction sensor on a battery-powered robot is given a fixed detection
range in its datasheet, but the battery driving it does not hold a fixed
voltage. This repository tests whether, and by how much, the usable range of an
inductive metal detector falls as its supply voltage drops across a single
discharge.

**Status: predictions registered, measurements not yet taken.** Every results
section below is marked `unmeasured` and will stay that way until real trials
exist in `data/raw_measurements.csv`. Nothing here is simulated, smoothed or
filled in.

---

## Prediction, registered before measurement

Three competing hypotheses were written down and committed *before any data was
collected*, in `theory/predictions.md`, together with the derivation they come
from in `theory/derivation.md`:

| | claim | predicted slope `d(ln d)/d(ln V)` |
|---|---|---|
| **H0** | ratiometric threshold; range independent of `V` | 0 |
| **H1** | fixed threshold, far field — `d_max ∝ V^(1/6)` | 0.167 |
| **H2** | fixed threshold, exact loop geometry | `1/n_eff = (1/6)(1 + a²/d²)` |
| **H3** | oscillator margin; range **rises** as `V` falls | `−[V*/(V−V*)] / n_eff` |

H3 is the primary hypothesis, and it comes from the circuit rather than from the
textbook. The alarm transistor is held off by the oscillator's amplitude, which
scales with the supply, but it switches at its own base-emitter voltage, about
0.6 V, which does not. The fixed part of that margin is what makes range depend
on supply — and it predicts the range **increases** as the battery drains, until
at `V* = V_BE/c` the detector alarms with no target present. That is the
behaviour these modules are known for on a dying cell, and `V*` can be measured
directly by sweeping the supply down with nothing nearby.

Writing `G(d) = (a²/(a²+d²))³`, all four hypotheses separate by the *shape* of a
single line — `G` plotted against `1/V` at the trigger point:

| hypothesis | shape of `G` vs `1/V` |
|---|---|
| H0 | flat |
| H1 / H2 | straight through the origin, positive slope |
| H3 | negative slope, x-intercept at `1/V*` |

The shape is read before any slope is compared with a predicted number, and the
fitted `V*` is then checked against the independently measured one.

The analysis script that produces the fitted slope, `analysis/make_figures.py`,
was also committed before any data existed, so the fitting procedure could not
have been chosen after seeing the result.

> **Pre-registration commit:** _link and date to be filled once committed._

## Method

> `unmeasured` — coil and module details and the measurement protocol are
> recorded in `data/rig_notes.md`. The board is in `figures/board_front.png` and
> `figures/board_back.png`; the circuit is in `figures/schematic.png`.

Two measurements are taken at each supply voltage:

- **Primary — the supply voltage at which the alarm triggers, with the target
  clamped at a fixed distance.** Voltage reads to ±0.01 V; distance by eye is
  ±1 mm at best, against predicted changes of a few millimetres. Measuring the
  voltage instead buys roughly two orders of magnitude of resolution. A sweep
  with no target gives `V*` directly.
- **Secondary — maximum detection distance at a fixed supply voltage.** This is
  what a user actually experiences, and it checks the primary result by an
  independent route with independent errors.

Supply voltage is set with a bench supply and measured at the module terminals,
not at the supply. Trials are run in a randomised order and the order is
recorded, so that drift over the session can be separated from the effect.

## Result

> `unmeasured` — no trials recorded yet.

Once data exists this section reports the fitted slope with its uncertainty,
the figure `figures/range_vs_voltage.png`, and which of H0, H1 and H2 survives.

## What this means for a battery-powered robot

> `unmeasured` — the practical rule follows from the measured slope, not from
> the prediction. It will be written only after the analysis exists.

## Limitations

Known before measurement, and not expected to be removed by it:

- The coil is close enough to the target that the far-field `1/d⁶` expansion is
  not valid: `a²/d² ≈ 0.19`, so the dipole form understates the signal by about
  40 %. The exact on-axis loop expression is used throughout.
- The spiral is printed, square, and on both faces of the board; treating it as
  one circular loop of a single mean radius is an idealisation, worst close in.
- Only one target material and geometry is tested. The response of a conductor
  to an alternating field depends on its conductivity, permeability and shape,
  so the fitted constant does not transfer to other targets.
- The detector module is a sealed commercial part. Its oscillator topology,
  any internal regulation and the reference used by its alarm comparator are
  inferred from external measurement, not from a schematic.
- Temperature is recorded but not controlled.

## Reproducing the analysis

```bash
python analysis/make_figures.py
```

Reads `data/raw_measurements.csv`, writes every figure in `figures/` and the
fitted numbers to `analysis/results.json`. With no data rows it says so and
stops rather than producing an empty plot.

Requires `numpy` and `matplotlib`.

## Layout

```
theory/     derivation and the pre-registered predictions
data/       rig notes and the raw trial-by-trial measurements
analysis/   the fitting and plotting script, fixed before data existed
figures/    output figures and rig photographs
firmware/   sketch used to capture the signal measurement
paper/      the write-up
```

`data/raw_measurements.csv` holds one row per trial, never an average:

```
trial_id, order, mode, voltage_V, distance_mm, edge_rate, temp_C, target, notes
```

`mode` is one of `primary` (distance fixed, supply swept to the trigger),
`secondary` (supply fixed, distance swept to the trigger) or `no_target`
(supply swept with nothing nearby, to find `V*`).

## Timeline

| date | step |
|---|---|
| _to be filled from the commit log_ | predictions registered |
| | rig built and documented |
| | pilot run |
| | full measurement series |
| | analysis |
| | write-up |

## A note on how this was made

The derivation, the predictions and the discussion are my own work and my own
wording. I used an AI assistant for the repository scaffolding, for the plotting
and fitting script, and as a check on my algebra; where it disagreed with me I
had to satisfy myself which of us was right before changing anything. No data
was generated, estimated or completed by it at any point.

## Licence

MIT — see `LICENSE`.

Kunaal Nirmal Khanwani
