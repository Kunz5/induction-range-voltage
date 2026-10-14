# Pre-registered predictions

Author: Kunaal Nirmal Khanwani
Written before any measurement was taken.

> Committed in the repository's root commit, together with `derivation.md`, so
> that the commit date is evidence the predictions preceded the data. Nothing in
> this file may be edited after the first data commit. If a prediction turns out
> wrong, that is a result; it is not a reason to change this file.

---

## 1. Why four hypotheses, not three

H0–H2 describe a detector that compares a received signal against a threshold.
This module is a transformer-feedback tuned-collector oscillator whose falling
amplitude switches a transistor, and the derivation shows that structure
produces H3. H3 is included because the
circuit predicts it, not because it is expected to win; the experiment decides.

## 2. Primary hypothesis

**H3 is primary**, on circuit grounds: the alarm is a transistor switched by
oscillator amplitude, and a transistor's turn-on voltage does not scale with
supply.

**H0 is the main competitor**: if the fixed term is small compared with the
supply-proportional part, H3 collapses towards H0. H1 and H2 are kept as the
fixed-threshold textbook expectation.

| | claim | slope `s = dln(d_max)/dln(V)` |
|---|---|---|
| **H0** | ratiometric threshold; range independent of `V` | 0 |
| **H1** | fixed threshold, far field | `1/6 = 0.167` |
| **H2** | fixed threshold, exact loop geometry | `1/n_eff` |
| **H3** | oscillator margin; range **rises** as `V` falls | `-[V*/(V-V*)] / n_eff` |

## 3. Worked example at this rig's estimated geometry

`a` = 22 mm (estimate), `d` = 50 mm (recalled), single Li-ion window
4.2 → 3.2 V, `n_eff = 6d²/(a²+d²) = 5.03`.

| hypothesis | predicted change in range, 4.2 → 3.2 V |
|---|---|
| H0 | 0 % |
| H1 | −4.4 % |
| H2 | −5.3 % |
| H3, `V*` = 2.0 V | **+6.8 %** |
| H3, `V*` = 2.5 V | **+12.8 %** |
| H3, `V*` = 2.8 V | **+20.9 %** |

This table shows that the hypotheses can be told apart numerically; it is not
the final prediction. It gets recomputed once, with the measured `a` and `V*`,
then frozen.

*(At the scaffold's demo geometry, `a` = 75 mm and `d` = 100 mm: H0 0 %,
H1 −4.4 %, H2 −7.0 %, H3 +8.8 % / +16.4 % / +26.7 %.)*

## 4. Primary measurement, and why

Clamp the target on the axis at **10, 12, 15, 20, 25, 30, 35 and 40 mm**. At each
distance, lower the supply from 5.0 V until the alarm first sounds and record
`V_trig`. Add one sweep with **no target** to find `V*`.

Voltage reads to ±0.01 V, while distance by eye is ±1 mm at best. The predicted
effects are only a few millimetres, so measuring voltage at a fixed distance
gives about 100 times better resolution. Each `(d, V_trig)` pair is one point on
`d_max(V)`.

## 5. Secondary measurement, and why

At **5.0, 4.2, 3.6 and 3.2 V**, move the target toward the coil and record the
distance at the first alarm.

This is what a detector's user actually experiences, and it checks the primary
result by an independent route with independent errors. If the two agree,
neither is dominated by a systematic error.

## 6. Pre-registered exclusion rule

A trial is excluded only for a reason written in `notes` **before its value is
read**, and only if:

1. the terminal voltage was not recorded, or drifted more than 0.02 V;
2. the target moved or was off the axis;
3. metal came within 30 cm of the coil;
4. the module had warmed up for less than 60 s;
5. the trial was out of the randomised order.

**No trial is excluded for its value.** Excluded trials stay in the raw file,
flagged, and the analysis is reported both with and without them.

## 7. What would falsify each hypothesis

- **H0** — range changes by more than its uncertainty between 4.2 and 3.2 V.
- **H1 / H2** — range does not decrease as `V` decreases (`s ≤ 0` within
  uncertainty).
- **H3** — range does not increase as `V` falls; or no spontaneous alarm occurs
  above the oscillator's dropout; or the no-target `V*` disagrees with the
  fitted `V*`.
- **Loop geometry** — the dipole model leaves smaller systematic residuals than
  the loop model with the measured `a`.

### Decision rules

- **H0** if `|s| < 2σ`.
- **H3** if `s < −2σ` **and** the fitted intercept agrees with the no-target
  `V*`.
- **H1** if `s > 2σ` and `s` is within 2σ of `1/6` but not of `1/n_eff`.
- **H2** if `s > 2σ` and `s` is within 2σ of `1/n_eff`.
- If `s` is within 2σ of both, report "fixed margin, geometry not resolved".
- Anything else counts as a failure of all four models, with the data shown.

---

## Rig constants

| quantity | value | status |
|---|---|---|
| coil radius `a` | ≈ 22 mm | **estimate** — measure spiral outer and inner diameters, take `a = (outer + inner)/4` |
| nominal range at 5.0 V | ≈ 50 mm | **recalled** — re-measure at 5.0 V with the chosen target |
| fixed distances, primary | 10, 12, 15, 20, 25, 30, 35, 40 mm | fixed |
| supply range | 5.0 V down to oscillator dropout | rated 3.0–5.0 V |
| highlighted window | 4.2 → 3.2 V | single Li-ion cell |
| module | `MetalDetector_V2.3 (303METALDET)`, MOD-43 class | board 65 × 60 mm |
| current draw | ≈ 5 mA silent, ≈ 28 mA beeping | vendor figure |

On the rover the module ran from the ESP32's regulated 3.3 V, so the battery's
decline never reached it. The bench sweep isolates the effect.
