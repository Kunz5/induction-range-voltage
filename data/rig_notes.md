# Rig notes

> **TEMPLATE — fields to be filled from the physical rig.**
> Every field is either a measured quantity or a fact read off a component.
> Leave a field as `unknown` rather than guessing. `unknown` is a usable
> limitation in the paper; a guess is not.

Recorded by: Kunaal Nirmal Khanwani
Date rig assembled:
Date these notes taken:

---

## Detector module

| field | value |
|---|---|
| module marking / part number | Silkscreen: `MetalDetector_V2.3 (303METALDET)`. Vendor-matched by eye to a ProtoSupplies MOD-43 or clone; the marking is the primary identification, the vendor name is not. |
| architecture | Tuned-collector oscillator with transformer feedback (tank `L1 ∥ C3` at collector; feedback via coupled winding `L2` through `C2`); vendor text describes it as Colpitts, the schematic shows otherwise. |
| how the architecture was determined | Read from the vendor schematic in `figures/`; the vendor's written description (Colpitts) disagrees with its own schematic, and the schematic is taken as authoritative. |
| drive frequency, measured | **pending.** Vendor text says ~300 kHz; not yet measured here, and not used in any calculation until it is. |
| how frequency was measured | **pending** — scope or frequency counter on the tank node. |
| regulator present between battery and oscillator? | **No.** The schematic shows the supply rail feeding R1, both coil windings, C1/C3/C4/C5 and Q3's emitter directly. There is no regulator, shunt reference or zener anywhere on the board; the only semiconductors are Q1 (9018), Q2 (9015) and Q3 (9012). |
| regulator part number, if present | n/a |
| alarm threshold: fixed reference or supply-referenced? | Mixed, by inspection: Q2's base sits at the rail through L1 (a DC short), so Q2 switches at its own base-emitter voltage below the rail — a fixed ~0.6 V inside a margin that otherwise scales with supply. This is the structure section F of `theory/derivation.md` argues produces H3. To be confirmed by measurement. |
| how that was determined | Read from the vendor schematic, `figures/schematic.png`. Not yet confirmed against the physical board with a meter. |

> The architecture decides whether the hypothesis is testable at all. A BFO
> module detects a frequency shift and is close to amplitude-independent.

## Search coil

| field | value |
|---|---|
| coil outer diameter, across flats | 50 mm on axis 1, 50 mm on axis 2 |
| coil inner diameter, across flats | 20 mm on axis 1, 20 mm on axis 2 |
| radius `a` used in the model, and why that choice | **17.5 ± 1 mm**, measured as `(outer + inner)/4`, the mean radius of the winding. Not rounded: the value recorded is the value found. The ±1 mm is the practical limit of a ruler on a printed spiral. The spiral is square, so this is an equivalent-circular-loop substitution and is stated as such wherever it is used. |
| number of turns, if countable | **pending** — countable from `figures/board_front.png`, not yet done. |
| shape | square spiral, printed traces, one per board face |
| `a`, pre-registered definition `(outer + inner)/4` | **17.5 mm** — half the mean side, the inscribed circle of the mean square |
| `a`, equal-area circle, `35/√π` | 19.7 mm — **sensitivity check only**, not the pre-registered value |
| wire gauge, if known | n/a — printed copper, not wire. |
| measured inductance | **pending.** Two spirals, one per board face (`L1`, `L2`); a continuity check also settles whether they are separate coupled windings or one centre-tapped winding. |
| measurement instrument | ruler, 1 mm resolution |

## Supply

Rated 3.0–5.0 V. Vendor current figures, not yet verified here: ≈ 5 mA silent,
≈ 28 mA while beeping. That 23 mA step is a measurement hazard — see the error
list below.

**Variable supply not yet acquired.** The module was previously powered from the
ESP32's fixed 3.3 V rail on the rover, which is why no sweep has been possible
and why the self-test and pilot are both outstanding. Acquiring an LM2596
adjustable buck converter, or using a school lab variable DC supply.

| field | value |
|---|---|
| source (bench supply / battery) | **none yet** — LM2596 adjustable buck converter or lab variable DC supply |
| bench supply model | |
| voltage measured at the module terminals, not at the supply | |
| meter used, and its stated accuracy | DT830-series 3½-digit DMM, 20 V DC range, 0.01 V resolution. No accuracy printed on the case; the series is typically ±(0.5 % + 2 digits), which is **an assumption about this meter, not a specification of it** |
| series resistance between supply and module, if measured | |

## Target

| field | value | source |
|---|---|---|
| object | ₹1 coin, dated 2020 (2019 series) | measured |
| material | ferritic stainless steel, 83 % Fe / 17 % Cr (Coinage Rules 2019). **Magnet test on this coin: it sticks** — magnetic, confirmed directly rather than inferred from the published composition | spec + measured |
| dimensions | diameter **20 mm measured by ruler**, agreeing with the 20 mm in the Rules. Mass 3.09 g (permitted 2.97–3.21 g) and thickness are spec only, not measured — no scale, and a 1 mm ruler cannot resolve the thickness | measured + spec |
| orientation | flat, parallel to the coil, centred on the axis; same coin every trial | measured |
| same object for every trial | yes — this coin is set aside for the experiment | measured |

**Note.** 20 mm diameter is comparable to the coil (`a` = 17.5 mm), not small
relative to it as the model assumes; ferritic steel adds magnetisation to the
eddy-current response. Both are limitations. Dimensions are official spec, not
measured.

**Two conflicts with the pre-registered derivation, recorded rather than
resolved here.** Section B of `theory/derivation.md` states that a non-ferrous
target is preferred, "because it leaves eddy currents as the only mechanism",
and the derivation assumes throughout a target small compared with `a`. This
target is neither. `derivation.md` is the pre-registration and is not edited;
the conflict is reported, and its consequences belong in the paper's discussion.

Sources: *Coinage of One Rupee, Two Rupees, Five Rupees, Ten Rupees and Twenty
Rupees Rules, 2019*; Wikipedia, "Indian 1-rupee coin".

## Geometry and measurement method

| field | value |
|---|---|
| fixed distances for the primary measurement | 10, 12, 15, 20, 25, 30, 35, 40 mm |
| how distance was measured | |
| resolution of the distance measurement | |
| how the coil was held fixed | |
| how the target was moved | |
| what counted as a detection | |
| how `edge_rate` was defined and captured | |
| instrument used for `edge_rate` | |

## Environment

| field | value |
|---|---|
| ambient temperature range over the session | 26 °C measured with a thermometer at the time the coil and coin were measured; to be recorded at the start and end of every block in the main run |
| nearby metal, and distance to it | |
| mains or other interference noted | |
| floor or bench material | |

## Photographs

| file | shows | status |
|---|---|---|
| `figures/board_front.png` | component side: printed spiral, Q1–Q3, R3 sensitivity pot, buzzer, power connector | in repo |
| `figures/board_back.png` | reverse side: second printed spiral, silkscreen marking | in repo |
| `figures/schematic.png` | vendor schematic, as supplied | in repo |
| `figures/rig_overview.jpg` | coil mount, target jig, supply and meter | pending — rig not built |
| `figures/measurement_setup.jpg` | target on axis at a set distance | pending — rig not built |

---

## Deliberate modifications to the circuit under test

Anything changed on the board itself, recorded before it is used.

| change | why | when | reverted? |
|---|---|---|---|
| Buzzer SG1 lifted; 10 kΩ fitted from Q3's collector to ground | The buzzer draws ~23 mA when it sounds, and that step sags the supply at the exact moment the trigger voltage is being read. Under H3 a sag lowers V, which raises sensitivity, which feeds back — so the unmodified board chatters around its own trigger point. The buzzer was also the only pull-down on Q3's collector, hence the resistor. | **pending** | |
| Trigger sensed by microcontroller at Q3's collector | Removes the operator's reaction time, the largest error in the primary measurement. See `firmware/WIRING.md`. | **pending** | |

This is a change to the thing being measured, not just to how it is measured.
Pilot trials are run at one fixed distance **both with and without** the buzzer.
If the trigger voltage differs between the two by more than its repeatability,
the modification is not neutral and every result must be reported against the
unmodified board.

## Coil shape

The model treats the coil as a single circular loop. The coil is square. The
primary analysis uses the pre-registered `a` = 17.5 mm, half the mean side, the
inscribed circle of the mean square. A secondary and clearly labelled
sensitivity analysis uses the equal-area radius 19.7 mm, which matches the
loop's far-field moment.

Recorded here **before any main-run data**, so that the alternative was declared
in advance rather than chosen after seeing the result. `theory/predictions.md`
is not changed: 17.5 mm remains the pre-registered value and the equal-area
figure is reported alongside, never in place of it.

## Self-test — firmware latch

**NOT YET RUN.**

A previous version of this file recorded readings of 0 / 1 / 1 at supplies of
5.0 V and 2.6 V. Those readings were not valid. The module was powered from the
ESP32's fixed 3.3 V pin and no variable supply existed, so neither 5.0 V nor
2.6 V could be applied and no such reading could have been taken. The entry is
withdrawn rather than corrected; see the retraction commit.

| step | condition | expected | read |
|---|---|---|---|
| 1 | no metal near coil, 5.0 V | 0 | — |
| 2 | metal on coil, 5.0 V | 1 | — |
| 3 | metal on coil, **2.6 V** | 1 | — |

Step 3 remains the one that matters: it is what confirms the trigger is decided
against the 450 mV firmware threshold rather than a logic level. Until it has
been run, the divider and pull-down wiring is unverified and the firmware's
trigger path is unexercised on hardware.

## Pilot

**NOT YET RUN.** No pilot data exists.

A previous version of this file recorded four trigger voltages at 20 mm
(3.52 / 3.54 / 3.50 / 3.51 V) and a buzzer comparison drawn from them. Those
were not measurements. The supply was the ESP32's fixed 3.3 V rail, so no sweep
down to a trigger point was possible and no trigger voltage could have been
read. `data/pilot.csv` is deleted and the statistics derived from it — the
0.005 V difference, the 0.0171 V scatter, the ±0.073 V interval — are
withdrawn in full.

Planned, once a variable supply is in hand: twelve trials at 20 mm, six with the
buzzer fitted and six lifted, in ABBA order, same coin.

## Fixed from this point

- **R3, the sensitivity potentiometer: to be frozen** at its position as of the
  first valid self-test, by a witness mark on the body and shaft. The mark is
  not yet applied and the position is not yet photographed, so R3 is **not yet
  fixed**. Once marked it is not to be touched for the rest of the experiment. `R3` sets the oscillator's
  amplitude and therefore `V* = V_BE/c`, so moving it moves the quantity being
  measured. If it is moved by accident, record it and treat the data before and
  after as separate series.
- Buzzer: lifted.
- Trial order: `data/run_order.md`.

## Known sources of error, before taking data

Written before measurement. Revised once, before any data, after the firmware
moved the trigger decision off the operator and onto the board.

1. **Distance zero and setting: ±1 mm.** The coil is printed on a board about
   1.6 mm thick, so "distance from coil plane" is ambiguous by up to about
   0.8 mm. Setting the target adds about ±0.5 mm. Effect on coupling `g²`:
   `6·d·δd/(a²+d²)`, equivalently `n_eff · δd/d`. Recomputed with the measured
   `a` = 17.5 mm: **14.8 % at 10 mm, 17.1 % at 17.5 mm, 12.6 % at 40 mm**. It
   peaks at `d = a`, so it is not worst at the close distances — 40 mm is the
   least sensitive point on the list and 10 mm the second least. The estimate
   of `a` = 22 mm used before measurement put the peak at 22 mm and the whole
   budget 3–4 points lower; measuring `a` moved the peak inward and raised it.
   *Mitigation:* measure from the coil face every time, use fixed spacer blocks
   per distance, and record the reference point.

2. **Voltage step resolution: ±0.01 V.** The firmware removes human reaction
   time at the trigger. What is left is the sweep step: the true trigger lies
   somewhere within the last 0.01 V step. Chatter near `V*` may add uncertainty
   there; it is recorded per trial as `t_confirm − t_first`, dropout count and
   peak mV.

3. **Voltage measurement and ripple: ±0.02–0.05 V.** The multimeter's accuracy
   is about ±(0.5 % + 2 digits), roughly ±0.02 V at 3 V. A buck converter adds
   tens of millivolts of ripple. With the buzzer lifted, the lead drop at about
   5 mA is under 5 mV. *Mitigation:* measure at the module's own terminals,
   record the meter model, and prefer a bench supply.

4. **Temperature drift: about ±6 mV in `V_BE`, up to about ±20 mV in `V*`.**
   `V_BE` moves about −2 mV per °C, so ±3 °C in a session gives ±6 mV, and
   `V* = V_BE/c` amplifies that if `c` is small. *Mitigation:* warm up for 60 s,
   record temperature at the start and end, and repeat the no-target `V*` sweep
   at the start and end of every session.

5. **Target placement: a few percent in coupling.** Off-axis or tilted placement
   changes `g(d)`. *Mitigation:* use a jig and keep the same target orientation
   every trial.
