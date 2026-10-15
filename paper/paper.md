---
title: "Does a Draining Battery Shorten or Extend a Metal Detector's Range?"
subtitle: "Theory, pre-registered predictions and experimental design for an induction detector — Version 1 (measurements pending)"
author: "Kunaal Nirmal Khanwani · Grade XII, Jamnabai Narsee School, Mumbai · Voluntary ISC Physics project"
date: "October 2026"
---

# Abstract

Battery-powered induction metal detectors lose supply voltage as their batteries discharge, yet how this changes their detection range is rarely stated. A textbook model, in which a received signal is compared with a fixed threshold, predicts that range falls slowly, as the sixth root of supply voltage. This paper shows that the answer depends on how the alarm threshold itself scales with supply, and that for the oscillator-damping detector used on my rover the prediction reverses: range should *increase* as the battery drains, until the detector alarms with no metal present at a characteristic voltage $V^*$. Starting from Faraday's law and the reciprocity of mutual inductance, I derive a single expression for the sensitivity of range to supply voltage that covers four hypotheses — ratiometric (H0), fixed-threshold far-field (H1), fixed-threshold near-field (H2) and oscillator-margin (H3) — and a linearisation in which one graph distinguishes them by the sign of its slope. The predictions, decision rules, exclusion rules and a randomised trial order were committed publicly before any measurement. The apparatus, a microcontroller latch that removes human reaction time from the trigger, and a full uncertainty budget are described. A clearly labelled simulation demonstrates the analysis. Experimental results are pending and will be reported in Version 2.

# 1. Introduction

In June 2025, at the IIT Bombay Makerspace, I built MineRoverX, an autonomous rover that sweeps a metal detector across the ground for landmine detection. The detector module had no data output — it signalled only by sounding a buzzer — so I soldered a connection from the buzzer into the rover's microcontroller. While documenting the rover, I noted that the detector needed recalibrating "for different battery voltages". I had built a machine whose ability to find metal changed while it was running, and I did not know by how much, or even in which direction.

That question is not specific to my rover. Handheld detectors used in humanitarian demining, utility location and inspection are almost all battery powered, and the supply falls throughout a session. If range changes with voltage, a detector that clears ground with a fresh battery may not clear it with a tired one — or may begin to false-alarm.

The textbook expectation is simple. The detection signal scales with supply voltage and falls as the sixth power of distance, so, against a fixed threshold, the maximum range should scale as $V^{1/6}$: a 24 % drop in voltage would cost only about 4–5 % of range. This paper argues that this is incomplete. Supply voltage enters a detector twice — once in the strength of the signal and once in the level at which the alarm fires — and which of these dominates decides not only the size of the effect but its sign.

The contributions of this version are: (i) a derivation that unifies four competing hypotheses in one expression; (ii) numerical predictions for my apparatus, committed publicly before data; (iii) an experimental design that measures trigger *voltage* at fixed distance, which is about a hundred times more precise than measuring distance directly; and (iv) an uncertainty analysis. Measurements will be reported in Version 2.

# 2. Theory

## 2.1 The detector

The module is a commercial induction metal detector (ProtoSupplies MOD-43 type) with a square spiral coil printed on the circuit board. Its schematic shows a transformer-feedback, tuned-collector oscillator running at roughly 300 kHz: the tank $L_1 \parallel C_3$ sits at the transistor's collector, and a coupled second winding $L_2$ feeds part of the tank voltage back to the base. The oscillation amplitude holds an alarm transistor off; when metal near the coil absorbs energy, the amplitude falls, the alarm transistor switches on, and the buzzer sounds. A trimmer potentiometer, R3, sets the sensitivity.

## 2.2 The coil's field at the target

Treating the coil as a single circular loop of radius $a$ carrying current $I$, the Biot–Savart law gives the field on its axis at distance $d$:

$$B(d) = \frac{\mu_0 I a^2}{2\,(a^2+d^2)^{3/2}} = \frac{\mu_0 I}{2}\, g(d), \qquad g(d) = \frac{a^2}{(a^2+d^2)^{3/2}}.$$

Far from the coil ($d \gg a$) this reduces to the dipole field, proportional to $1/d^3$. My detector works at distances comparable to the coil's size, so the exact form is kept throughout.

## 2.3 Eddy currents in the target

The coil current alternates at angular frequency $\omega$, so by Faraday's law the target experiences an EMF $\mathcal{E} = -\,d\Phi/dt$ of magnitude $\omega B A_t$, where $A_t$ is the effective area of its current path. This drives eddy currents, whose magnetic moment is proportional to $B$ at every step: the EMF is proportional to the rate of change of flux, the current to the EMF, and the moment to the current. By Lenz's law, the eddy currents oppose the change that produced them.

## 2.4 Why the coupling appears twice

The detector does not sense the target directly; it senses the target's effect on its own coil. The coupling from coil to target is a mutual inductance $M \propto g(d)$. The return coupling — from the target's eddy currents back to the coil — is the *same* $M$, because mutual inductance is symmetric ($M_{12} = M_{21}$; Neumann's formula is unchanged when the two loops are swapped). The target therefore reflects an impedance proportional to $\omega^2 M^2$ into the coil, which appears as extra loss. The detection signal scales as

$$S \propto g(d)^2 \cdot I.$$

This argument holds at every distance on the axis, near or far; in the far field it recovers the familiar $1/d^6$ law.

## 2.5 Supply voltage in the signal

A self-limiting oscillator grows until its transistor runs out of headroom, so its amplitude — and the coil current — is approximately proportional to the supply: $I \approx kV$, giving $S = \kappa V g(d)^2$. This is an assumption, not a law: it fails near the oscillator's start-up voltage and below it, and drifts if coil resistance changes with temperature.

## 2.6 The alarm condition — supply voltage enters a second time

The alarm fires when the signal exceeds a margin $T(V)$. Three physically distinct cases arise:

| Case | Margin $T(V)$ | Typical circuit | Hypothesis |
|---|---|---|---|
| Fixed | $T_0$ | absolute threshold on a received signal | H1, H2 |
| Ratiometric | $\beta V$ | threshold from a divider across the supply | H0 |
| Oscillator margin | $cV - V_{BE}$ | amplitude must fall to a transistor's fixed turn-on voltage | H3 |

In this module the alarm transistor's switching point is partly set by a divider through R3 (proportional to supply) and partly by its base–emitter voltage $V_{BE} \approx 0.6$ V (fixed). Writing the oscillator amplitude as $\alpha V$, the loss caused by the target as a fraction $\beta g^2$ of it, and the switching point as $\gamma V + V_0$, the alarm fires when

$$\alpha V\,(1 - \beta g^2) \le \gamma V + V_0,$$

which rearranges to

$$V_{\text{trig}}(d) = \frac{V^*}{1 - K g(d)^2}, \qquad V^* = \frac{V_0}{\alpha - \gamma}, \qquad K = \frac{\alpha\beta}{\alpha-\gamma}.$$

$V^*$ has a direct physical meaning: at $V = V^*$ the oscillation with *no target present* already sits at the switching point, so the alarm sounds on its own. The vendor's warning that, if the sensitivity is set too high, "the buzzer will sound continuously" is this effect reached by turning R3 rather than by lowering the supply. $V^*$ can therefore be measured with no target at all.

## 2.7 One expression for all four hypotheses

Define the local coupling exponent

$$n_{\text{eff}} = -\frac{d\ln g^2}{d\ln d} = \frac{6d^2}{a^2+d^2},$$

which equals 6 in the far field and falls towards zero near the coil. Differentiating the threshold condition $g(d_{\max})^2 = T(V)/\kappa V$ gives the sensitivity of range to supply:

$$s \equiv \frac{d\ln d_{\max}}{d\ln V} = \frac{1 - V T'/T}{n_{\text{eff}}}.$$

Only $VT'/T$ differs between the cases:

- **Fixed margin:** $s = 1/n_{\text{eff}} > 0$ — range falls as the battery drains (1/6 in the far field, H1; larger near the coil, H2).
- **Ratiometric:** $s = 0$ — range is independent of supply (H0).
- **Oscillator margin:** $VT'/T = V/(V-V^*) > 1$, so $s = -\dfrac{V^*/(V-V^*)}{n_{\text{eff}}} < 0$ — range *increases* as the battery drains (H3).

The sign of $s$ classifies the detector before any detailed fitting.

## 2.8 Linearisation

For H3, the trigger condition can be rearranged into a straight line:

$$g(d)^2 = \frac{1}{K} - \frac{V^*}{K}\cdot\frac{1}{V_{\text{trig}}}.$$

A graph of $g(d)^2$ against $1/V_{\text{trig}}$ is therefore a straight line with **negative slope** $-V^*/K$, $y$-intercept $1/K$ and $x$-intercept $1/V^*$. For a fixed-threshold detector the alarm switches *off* as the supply falls, at $V_{\text{off}} \propto 1/g^2$, giving a line through the origin with **positive slope**. For a ratiometric detector the alarm does not change state during the sweep at all. The $x$-intercept of the H3 fit provides an independent estimate of $V^*$ that can be checked against the value measured directly with no target.

# 3. Hypotheses and pre-registered predictions

The predictions below were committed to a public GitHub repository before any measurement; the commit history is the evidence of their timing.

**Primary hypothesis: H3**, on circuit grounds — the alarm is a transistor switched by oscillator amplitude, and a transistor's turn-on voltage does not scale with supply. **Main competitor: H0** — if the fixed term is small, H3 collapses towards H0. H1 and H2 are retained as the textbook expectation.

**Worked example at this apparatus's geometry** ($a = 17.5$ mm measured; nominal range $d \approx 50$ mm recalled, to be re-measured), for a single lithium-ion cell discharging from 4.2 V to 3.2 V:

| Hypothesis | Predicted change in $d_{\max}$, 4.2 → 3.2 V |
|---|---|
| H0 | 0 % |
| H1 | −4.4 % |
| H2 | −5.0 % |
| H3, $V^* = 2.0$ V | +6.4 % |
| H3, $V^* = 2.5$ V | +12.1 % |
| H3, $V^* = 2.8$ V | +19.8 % |

This table demonstrates that the hypotheses are numerically separable at this geometry; H3 depends on $V^*$, which is measured, so the three H3 rows bracket plausible cases rather than predicting one value.

**Local exponent at the measurement distances** ($a = 17.5 \pm 1$ mm):

| $d$ (mm) | 10 | 12 | 15 | 20 | 25 | 30 | 35 | 40 |
|---|---|---|---|---|---|---|---|---|
| $n_{\text{eff}}$ | 1.48 | 1.92 | 2.54 | 3.40 | 4.03 | 4.48 | 4.80 | 5.04 |

**Decision rules (fixed in advance).** With the fitted exponent $s$ and its standard error $\sigma$: H0 if $|s| < 2\sigma$; H3 if $s < -2\sigma$ *and* the fitted $V^*$ agrees with the no-target $V^*$ within combined uncertainty; H1 if $s > 2\sigma$ and within $2\sigma$ of 1/6 but not of $1/n_{\text{eff}}$; H2 if within $2\sigma$ of $1/n_{\text{eff}}$. Any other outcome is reported as a failure of all four models.

**What would falsify each.** H0: range changes by more than its uncertainty between 4.2 and 3.2 V. H1/H2: range does not fall as voltage falls. H3: range does not rise as voltage falls; or no spontaneous alarm occurs above the oscillator's dropout; or the directly measured $V^*$ disagrees with the fitted one.

# 4. Apparatus

| Item | Specification | Source |
|---|---|---|
| Detector module | Induction detector, MOD-43 type; transformer-feedback tuned-collector oscillator, ≈300 kHz; rated 3.0–5.0 V | vendor documentation and schematic |
| Coil | Square printed spiral; outer 50 mm, inner 20 mm across the flats, both axes | measured, ruler (1 mm) |
| Effective radius $a$ | 17.5 mm by the pre-registered definition (outer + inner)/4; 19.7 mm equal-area circle, used only as a sensitivity check | computed |
| Target | 2020 ₹1 coin (2019 series): ferritic stainless steel (83 % Fe, 17 % Cr), 20 mm diameter, 3.09 g; attracted by a magnet | official specification; diameter and magnetism checked |
| Supply | School battery eliminator (Jainco, stepped), 6 V tap, with a laboratory rheostat in series for fine control | laboratory equipment |
| Voltmeter | DT830-series 3½-digit digital multimeter, 20 V DC range, 0.01 V resolution; accuracy not stated on the case (series typical ±(0.5 % + 2 digits)); probes on the module's own supply pins | — |
| Trigger latch | ESP32 microcontroller reading the alarm transistor's collector through a 10 kΩ / 15 kΩ divider on GPIO 34; firmware threshold 450 mV; detection confirmed after 50 ms continuous | firmware in repository |
| Modifications | Buzzer disconnected for the main run; 10 kΩ pull-down role taken by the divider; sensitivity trimmer R3 fixed with a witness mark | recorded |
| Environment | Room temperature by thermometer at the start and end of each block | — |

The latch replaces human judgement of "has it triggered?" — otherwise the largest source of error — and records two instants per trial (first active sample and confirmation), whose separation measures the chatter at the trigger point. Near $V^*$ the H3 model predicts this chatter should widen, giving a second, independent signature of H3.

# 5. Method

1. **No-target sweep.** With no metal within 30 cm of the coil, set the supply to 5.00 V and lower it in 0.01 V steps. Record the voltage at which the latch fires on its own ($V^*$), or record "none" and the lowest voltage reached.
2. **Primary measurement — voltage at change of state, at fixed distance.** Place the coin flat and centred on non-metallic spacers at the specified distance. Starting at 5.00 V, lower the supply in 0.01 V steps and record the meter reading at the first change in alarm state, together with its direction (off → on, or on → off). If the alarm does not change state between 5.00 V and the oscillator's dropout, record that outcome; it is itself evidence (H0, or a distance outside the range of the sweep).
3. **Distances:** 10, 12, 15, 20, 25, 30, 35 and 40 mm, five repeats each (40 trials), in a pre-registered randomised order (seed 20261014) arranged in four blocks of ten, with no distance repeated consecutively. Each block is bracketed by no-target sweeps to monitor drift.
4. **Secondary measurement:** at 5.0, 4.2, 3.6 and 3.2 V, move the coin slowly towards the coil and record the distance at first alarm (three repeats each, randomised). This is the quantity a user of the detector experiences, measured by an independent route with independent errors.
5. **Recording:** every reading is logged at the moment it occurs. Raw values are never edited; corrections go in a notes column.

**Pre-registered exclusion rule.** A trial may be excluded only for a reason recorded before its value is read: the supply voltage was not recorded or drifted by more than 0.02 V; the target was moved or found off-axis; metal came within 30 cm of the coil; the module had been powered for less than 60 s; or the trial was out of the randomised order. No trial is excluded because of its value, and the analysis is reported with and without exclusions.

# 6. Uncertainty analysis

**Distance.** Since $g^2 = a^4/(a^2+d^2)^3$, a distance error $\delta d$ produces a fractional error

$$\frac{\delta(g^2)}{g^2} = \frac{6d\,\delta d}{a^2+d^2} = n_{\text{eff}}\,\frac{\delta d}{d},$$

which is largest at $d = a$. With $a = 17.5$ mm and $\delta d = 1$ mm, it is 14.8 % at 10 mm, peaks at 17.1 % at 17.5 mm, and is 12.6 % at 40 mm. The budget is nearly flat across the measurement range. The board's thickness (≈1.6 mm) makes "distance from the coil plane" ambiguous by up to 0.8 mm; distances are measured from the coil face with fixed spacers.

**Voltage.** The meter resolves 0.01 V, but its absolute accuracy is coarser — about ±0.04 V at 3.5 V for this meter type. Resolution and random reading error scatter individual points. A calibration error does not simply shift every point equally once the data are plotted against $1/V$: a gain error rescales the axis, and an offset becomes a non-uniform shift in $1/V$, so both can bias the fitted slope and intercept. The direct comparison of the measured and fitted $V^*$ — made with the same meter — is partly protected against this, since a common error moves both.

**Trigger step.** The true change of state lies somewhere within the last 0.01 V step: ±0.005 V.

**Temperature.** $V_{BE}$ changes by about −2 mV per °C, and $V^* = V_0/(\alpha-\gamma)$ amplifies this if $\alpha-\gamma$ is small. Temperature is recorded at each block, and the bracketing no-target sweeps detect drift directly.

**Supply ripple.** An unsmoothed eliminator carries AC ripple on its DC output; it is measured on the meter's AC range at the module pins before the run.

# 7. Simulated demonstration of the analysis

*Everything in this section is simulated. The parameters are illustrative and were chosen only to make the shapes visible; none of it is a measurement of the apparatus.*

The script `analysis/simulate_demo.py` generates synthetic sweep results at the pre-registered distances for three illustrative detectors, adds reading noise of 0.01 V, rounds to the meter's two decimal places, and applies the linearisation of Section 2.8.

![SIMULATED — the H3 detector (filled circles) gives a line of negative slope whose x-intercept recovers the V* used to generate it; the fixed-threshold detector (open triangles) gives a line through the origin with positive slope; the ratiometric detector produces no change of state and therefore no points.](../figures/SIMULATED_hypothesis_test.png){width=85%}

Two features of the simulation inform the real experiment. First, the fit recovers the parameters used to generate the H3 data, confirming that the analysis pipeline works; it does *not* show that a real detector follows H3, because the data were generated from that model. Second, depending on R3's setting, only some distances may change state inside the 5.0 V sweep; the others will record "no change of state", and the method treats that as an outcome rather than a missing value.

# 8. Limitations

- **Coil shape.** The model treats a square spiral as a single circular loop. The pre-registered $a = 17.5$ mm is the inscribed radius; results will also be reported with the equal-area radius of 19.7 mm to show how much the approximation matters.
- **Target size and material.** The 20 mm coin is comparable in size to the coil, not small as the model assumes, and its ferritic steel adds magnetisation to the eddy-current response.
- **Threshold structure.** The split of the alarm margin into supply-proportional and fixed parts is inferred from the circuit's topology; the measurement of $V^*$ tests it.
- **Oscillator linearity.** Amplitude proportional to supply fails near start-up.
- **Air, not soil.** Ground mineralisation is outside this study.
- **One module, one target.** Generalising requires further detectors and targets.

# 9. Planned measurement and further work

Version 2 will report the measurements described in Section 5, analysed exactly as pre-registered, with all raw data in the repository. Further work: (i) a controlled test of R3's role, by changing it only after the main data are complete and re-measuring $V^*$; (ii) the transient supply sag when the rover's motors accelerate, which this analysis predicts will momentarily change detection range; (iii) a supply-compensated alarm threshold in the rover's firmware, so that sensitivity stays constant as the battery drains; (iv) repetition through soil.

# References

1. D. J. Griffiths, *Introduction to Electrodynamics*, 4th ed., Cambridge University Press — Faraday's law, the field of a current loop, mutual inductance and Neumann's formula.
2. H. C. Verma, *Concepts of Physics*, Vol. 2, Bharati Bhawan — electromagnetic induction and eddy currents.
3. NCERT, *Physics Part I, Class XII*, Chapter 6: Electromagnetic Induction.
4. ProtoSupplies, "Metal Detector Module" (MOD-43) product documentation and schematic, protosupplies.com.
5. Government of India, *Coinage of One Rupee, Two Rupees, Five Rupees, Ten Rupees and Twenty Rupees Rules, 2019* — specification of the ₹1 coin.
6. A. Winfield, *Robotics: A Very Short Introduction*, Oxford University Press.
7. D. J. C. MacKay, *Sustainable Energy — without the Hot Air*, UIT Cambridge.
8. K. N. Khanwani, MineRoverX repository, github.com/Kunz5/mine-rover-x.
