# Why detection range should depend on battery voltage

Author: Kunaal Nirmal Khanwani
Written before any measurement was taken.

Module under test: printed-spiral induction detector, board marking
`MetalDetector_V2.3 (303METALDET)`. Schematic in `figures/schematic.png`.

---

## The question

A battery-powered induction metal detector runs from a supply that falls as the
battery discharges. How does the maximum detection range `d_max` depend on
supply voltage `V`? Does range fall, stay flat, or rise as the battery drains,
and by how much?

Voltage enters the detector in two places: it sets how strongly the coil drives
the target, and it can also set the level at which the alarm fires. Which one
dominates decides the sign of the effect.

---

## A. Coil field at the target

```
B(d) = mu0 * I * a^2 / ( 2 * (a^2 + d^2)^(3/2) )  =  (mu0 * I / 2) * g(d)
```

On the axis, every current element contributes an axial component, and the
perpendicular components cancel by symmetry. Integrating gives this exact
result; no approximation is needed on the axis.

Far from the coil (`d >> a`) it reduces to the dipole field `mu0*I*a^2 / 2d^3`.
Close to the coil (`d <~ a`) it is much flatter. This rig detects at distances
comparable to the coil size, so the exact form is kept, and the dipole law is
only a limiting case.

The target is assumed to be on the axis and small compared with `a`.

---

## B. Eddy currents and the target's moment

By Faraday's law, `|eps_t| = omega * B * A_t`. The EMF drives a current
`I_t = eps_t / Z_t`, so the moment is

```
m = I_t * A_t   proportional to   B
```

Every step is linear: EMF proportional to rate of change of flux, current
proportional to EMF through a fixed impedance, moment proportional to current.
So `m ∝ B`, with a constant set by the target's size, conductivity and the
frequency, not by `B`. By Lenz's law, `m` opposes the coil's field.

Linearity would only fail for a ferromagnetic target near saturation, far above
these microtesla fields. A non-ferrous target is still preferred, because it
leaves eddy currents as the only mechanism. Frequency changes the skin depth,
which alters the constant but not the linearity.

---

## C. Coil-to-target coupling

The flux the coil drives through the target per amp of coil current is
`B * A_t / I ∝ g(d)`, so the mutual inductance `M ∝ g(d)`.

---

## D. The return leg, by mutual-inductance symmetry

"The target is a dipole, so its field falls as `1/d^3` again" is only true in the
far field. The exact argument is reciprocity: `M_12 = M_21` — Neumann's formula
is unchanged when the two loops are swapped. So the flux the target drives back
through the coil per amp of target current is the same `M ∝ g(d)`, at every
distance. That gives

```
S  proportional to  omega^2 * M^2 * I   proportional to   g(d)^2 * I
```

The target reflects an impedance `omega^2 * M^2 / Z_t` into the coil, which
appears as extra loss: energy taken out of the oscillator and dissipated in the
metal.

In the far field, `g^2 ∝ 1/d^6`, which recovers the sixth-power law.

---

## E. Supply voltage in the signal

The module is a tuned-collector oscillator with transformer (inductive)
feedback — the Armstrong or Meissner configuration: the tank `L1 ∥ C3` sits at
the transistor's collector, and the coupled second winding `L2` feeds a fraction
of the tank voltage back to the base through `C2`, with both windings returning
to the AC-grounded rail. It is not a Colpitts oscillator, despite the vendor's
description, since no capacitive divider sets the feedback; like any such
oscillator it is self-limiting, its amplitude growing until the transistor runs
out of headroom.

So `I ≈ kV`, and

```
S = kappa * V * g(d)^2
```

This is stated as an assumption, not a law. It fails in three places:

- near the oscillator's start-up voltage, where amplitude is non-linear in `V`;
- below start-up, where oscillation stops;
- if coil resistance drifts with temperature.

Within the rated 3.0–5.0 V range at steady temperature, it is a reasonable
first model, and any departure shows up as curvature in the results.

---

## F. The alarm condition: voltage enters a second time

The alarm fires when `S >= T(V)`. Three cases:

| case | threshold | hypothesis |
|---|---|---|
| fixed margin | `T = T0` | H1 / H2 |
| ratiometric | `T = beta*V` | H0 |
| oscillator margin | `T = c*V - V_BE` | H3 |

In this module, the oscillator's amplitude (proportional to `V`) holds the alarm
transistor off. Metal reduces that amplitude by an amount proportional to
`V*g^2`, and the alarm fires when the remaining amplitude falls to the
transistor's switching point, `beta*V + V_BE`. Rearranging gives

```
T = (alpha - beta) * V - V_BE
```

The fixed `V_BE ≈ 0.6 V` is the only part that does not scale with supply, and
it is what makes range depend on voltage here. `R3` sets how large `V_BE` is
relative to the whole margin, so `R3` must be fixed and recorded.

**Threshold inversion.** `g(d_max)^2 = T(V) / (kappa * V)`, so

- fixed margin → range falls as `V` falls;
- ratiometric → range is independent of `V`;
- oscillator margin → `g(d_max)^2 = (c/kappa) * (1 - V*/V)`, with
  `V* = V_BE / c`. Range **rises** as `V` falls, and at `V*` the alarm fires
  with no target.

**Meaning of `V*`.** At `V*`, the unloaded amplitude already sits at the
switching point. The margin is zero, so the alarm sounds with no disturbance at
all. This is the vendor's "buzzer will sound continuously" warning: turning `R3`
and lowering `V` do the same thing to the margin. `V*` can be measured with no
target, by lowering the supply until the alarm sounds on its own.

---

## G. Sensitivity exponent

Define

```
n_eff = - d ln(g^2) / d ln(d) = 6 * d^2 / (a^2 + d^2)
```

which is 6 in the far field and smaller near the coil. Differentiating the
threshold condition gives

```
s  =  d ln(d_max) / d ln(V)  =  ( 1 - V*T'/T ) / n_eff
```

Only `V*T'/T` differs between the cases:

| case | `V*T'/T` | slope `s` |
|---|---|---|
| fixed margin | 0 | `1/n_eff` — positive; `1/6` far field is H1, larger near the coil is H2 |
| ratiometric | 1 | `0` — H0 |
| oscillator margin | `V/(V-V*) > 1` | `-[V*/(V-V*)] / n_eff` — negative, growing as `V` approaches `V*`; H3 |

The **sign** of the measured slope classifies the detector before any fitting.

**Linearisation.** For H3, `g(d_max)^2` against `1/V` is a straight line whose
x-intercept is `1/V*`. For H1/H2 it is a line through the origin with positive
slope; for H0 it is flat. The no-target `V*` is an independent check on the
fitted `V*`.

---

## Limits and assumptions

1. Exact only on the axis, for a target small compared with `a`; a jig holds it
   on axis.
2. The printed spiral is treated as one loop of mean radius `a`. The error is
   largest near the coil, and `a` is measured, not fitted.
3. Amplitude proportional to supply fails near start-up.
4. The target response is linear for non-ferrous targets.
5. The split of the margin into proportional and fixed parts comes from the
   circuit topology; the schematic should confirm it. With no fixed term, H3
   reduces to H0.
6. Temperature: `V_BE` drifts about −2 mV/°C, so temperature is recorded.
7. All measurements are in air, not soil.
