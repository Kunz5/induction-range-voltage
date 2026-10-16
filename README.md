# Does a draining battery shorten — or extend — a metal detector's range?

An induction metal detector is given a fixed detection range in its datasheet.
The battery driving it does not hold a fixed voltage. This repository measures
what happens in between.

The textbook answer is that range falls slowly, as `V^(1/6)`. This project
argues the textbook answer is incomplete, and that for the detector on my rover
the sign of the effect reverses: **range should grow as the battery drains**,
until the detector alarms with no metal present at all.

> **Status.** Theory, predictions, apparatus and analysis code are complete and
> public. **[Paper v1.1](paper/paper_v1.pdf) is published; it reports no
> measurements and says so** — read it as [`paper/paper.md`](paper/paper.md) on
> GitHub, or as a [typeset PDF](paper/paper_v1.pdf).
> `data/raw_measurements.csv` currently holds nothing but its header.

---

## The question, and why the textbook answer is incomplete

Supply voltage enters a detector **twice** — once in the strength of the signal
it generates, and once in the level at which the alarm fires. Which of the two
dominates decides not just the size of the effect but its direction.

| | threshold behaviour | predicted slope `dln(d)/dln(V)` |
|---|---|---|
| **H0** | ratiometric — reference scales with the supply | `0` |
| **H1** | fixed threshold, far field | `1/6 = 0.167` |
| **H2** | fixed threshold, exact loop geometry | `1/n_eff` |
| **H3** | **oscillator margin** — alarm transistor switches at its own fixed `V_BE` | **negative** |

**H3 is the primary hypothesis, and it comes from the circuit rather than the
textbook.** The alarm transistor is held off by an oscillator amplitude that
scales with the supply, but it switches at its own base-emitter voltage, about
0.6 V, which does not. That fixed term is what makes range depend on supply —
and it predicts range *increases* as the battery drains, until at
`V* = V_BE / c` the detector alarms with nothing near the coil.

## One graph decides it

Writing `G(d) = (a²/(a²+d²))³`, all four hypotheses separate by the **shape** of
a single line — `G` plotted against `1/V` at the trigger point:

| hypothesis | shape |
|---|---|
| H0 | flat — in fact no change of alarm state at all during the sweep |
| H1 / H2 | straight through the origin, positive slope |
| H3 | negative slope, x-intercept at `1/V*` |

The shape is read **before** any slope is compared with a predicted number. The
x-intercept then gives `V*`, which is independently measurable by sweeping the
supply down with nothing near the coil — so the fit has a check it cannot talk
its way out of.

## What makes this different from a school practical

Everything that could be tuned after seeing a result was committed **before the
result existed**, with GitHub's timestamps as the witness:

- [**Predictions registered, 14 October 2026**](../../commit/44b44fd) — the four hypotheses, their
  numerical predictions, the decision rules and the exclusion rule, in the
  repository's root commit, before any apparatus was documented.
- [**Analysis fixed before data**](../../commit/9f0c5c4) — the exact fitting code,
  committed while the data file was still empty. It refuses to run on no data
  rather than producing an empty plot.
- [**Trial order randomised in advance**](../../commit/d156a1b) — seed 20261014,
  reproducible byte-for-byte on two Python versions.
- [**A retraction**](../../commit/181a6cf) — a pilot was recorded, then found to
  be invalid: the module had been powered from a fixed 3.3 V rail, so no sweep
  was possible and the numbers could not have been measured. They were
  withdrawn in public rather than quietly deleted, and the history was not
  rewritten.

A [protocol amendment](../../commit/82bdee3) is recorded the same way. The
original wording — *"lower the supply until the alarm first sounds"* — could only
record the transition H3 predicts, which would have made the outcomes refuting
H3 unrecordable. Widening it removed a bias in favour of my own hypothesis.

## Apparatus

A commercial induction module (MOD-43 type) with a square printed spiral,
`a = 17.5 ± 1 mm`. The vendor calls the circuit a Colpitts oscillator; its own
schematic shows transformer feedback with no capacitive divider, and the
schematic is taken as authoritative.

The alarm is read by a microcontroller latch at the alarm transistor's
collector, which removes the largest error in the measurement — a human
deciding *"has it triggered?"*. It is sensed with `analogRead` and thresholded
in firmware at 450 mV, because a logic-level input goes deaf at exactly the
supply voltage this experiment is about. See [`firmware/WIRING.md`](firmware/WIRING.md).

The latch records **two** instants per trial and the gap between them, because
near `V*` the alarm margin collapses, the alarm loads the supply, and the sag
pushes it further in — so the chatter should widen as the supply falls. That is
a second, independent signature of H3 that a stopwatch could not see.

## Pilot

At 20 mm the alarm appeared at about 3.0 V as the supply fell, over twelve
trials recorded only as a summary. The direction — switching **on** as voltage
falls — is H3's and the opposite of a fixed threshold. It is **not evidence**
until the no-target sweep shows whether the module alarms on its own at that
voltage, in which case the number is `V*` and not a detection. An earlier pilot
was [retracted](../../commit/181a6cf) as invalid.

Supply is a Jainco battery eliminator on its 6 V tap with a series laboratory
rheostat; the regulated bench supply was not used, and the consequences are in
the error budget.

## Results

**Pending.** They will be Version 2 of the paper.

**No data here is simulated. One clearly labelled demonstration figure is** —
Section 7 of the paper shows how the analysis separates the hypotheses, using
synthetic sweeps from three illustrative detectors. It is marked as simulated in
its section heading, its filename, its caption, its plot title and its source.
Nothing in this repository reports a measurement.

## Reproducing

```bash
pip install -r analysis/requirements.txt
python analysis/make_figures.py     # figures + analysis/results.json
python analysis/gen_order.py        # regenerates the committed trial order
```

`make_figures.py` reads `data/raw_measurements.csv`, one row per trial and never
an average. With no rows it says so and stops: it will not substitute, smooth or
simulate data.

## Layout

```
paper/      the write-up — paper.md renders on GitHub; PDF and DOCX alongside
theory/     the derivation and the pre-registered predictions (frozen)
data/       rig notes, the randomised trial order, the raw trial-by-trial data
analysis/   the fitting code, fixed before any data existed
figures/    board photographs, vendor schematic, output figures
firmware/   the trigger latch and its wiring note
```

## Limitations, known before measuring

- The coil is close enough to the target that the far-field `1/d⁶` expansion is
  invalid: `a²/d² ≈ 0.19`, so the dipole form understates the signal by about
  40 %. The exact on-axis loop expression is used throughout.
- The target is a ₹1 coin, 20 mm across against a 17.5 mm coil — **not** small
  relative to the coil as the derivation assumes — and it is ferritic stainless,
  so magnetisation adds to the eddy-current response. Both conflict with the
  pre-registration, and both are recorded rather than quietly resolved.
- The module is a sealed commercial part. Its oscillator topology and alarm
  reference are read from the vendor schematic, not verified against the die.
- All measurements are in air, not soil. Temperature is recorded, not
  controlled.

## How this was made

The derivation, the predictions and the discussion are my own work and my own
wording. Then the repository scaffolding, the plotting and
fitting code, the typesetting, and as a check on my algebra — where it disagreed
with me I had to satisfy myself which of us was right before changing anything.
It caught several errors I had made, and I caught some of its. No data was
generated, estimated or completed by it at any point.

## Licence

MIT — see [`LICENSE`](LICENSE).

**Kunaal Nirmal Khanwani** · Grade XII, Jamnabai Narsee School, Mumbai
