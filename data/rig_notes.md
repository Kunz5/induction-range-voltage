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
| coil outer diameter | **pending** — measure the printed spiral. |
| coil inner diameter | **pending** — measure the printed spiral. |
| radius `a` used in the model, and why that choice | **pending.** Planned: `a = (outer + inner)/4`, the mean radius of the winding. The spiral is square, so this is an equivalent-circular-loop choice and the substitution must be stated as such. Working estimate 22 mm, not yet measured. |
| number of turns, if countable | **pending** — countable from `figures/board_front.png`, not yet done. |
| wire gauge, if known | n/a — printed copper, not wire. |
| measured inductance | **pending.** Two spirals, one per board face (`L1`, `L2`); a continuity check also settles whether they are separate coupled windings or one centre-tapped winding. |
| measurement instrument | **pending** |

## Supply

Rated 3.0–5.0 V. Vendor current figures, not yet verified here: ≈ 5 mA silent,
≈ 28 mA while beeping. That 23 mA step is a measurement hazard — see the error
list below.

| field | value |
|---|---|
| source (bench supply / battery) | |
| bench supply model | |
| voltage measured at the module terminals, not at the supply | |
| meter used, and its stated accuracy | |
| series resistance between supply and module, if measured | |

## Target

| field | value |
|---|---|
| material | |
| shape and dimensions | |
| mass | |
| orientation relative to the coil axis | |
| how orientation was held constant between trials | |

## Geometry and measurement method

| field | value |
|---|---|
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
| ambient temperature range over the session | |
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

## Known sources of error, before taking data

> Written before measurement. List what you expect to limit the result and
> roughly how large you expect each effect to be.

1.
2.
3.
