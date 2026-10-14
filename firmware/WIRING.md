# Wiring note — trigger latch

The sketch in `trigger_latch/` watches Q3's collector and timestamps the alarm.
It exists to remove the largest error in the primary measurement: the moment a
human decides "has it triggered?".

Four conditions, all of which must hold before the pilot.

---

## 1. Keep the voltage safe for the board

Q3 is a PNP high-side switch: its emitter sits on the supply rail, so its
collector rises to **V+ when the alarm sounds** and is held at ground by the
buzzer otherwise. With the module at 5 V, that line swings to 5 V.

**ESP32** — its pins are 3.3 V only, so the line must be divided. **10 kΩ / 15 kΩ**,
signal taken at the tap, on an **ADC1** pin — GPIO 34 is input-only and cannot
clash with anything. ADC2 pins stop working the moment WiFi is enabled.

```
Q3 collector ──[ 10k ]──┬── ESP32 GPIO34
                        │
                      [ 15k ]
                        │
                       GND
```

5 V × 15/25 = **3.0 V** against a 3.6 V limit. 10 k/20 k would give 3.33 V, which
is inside spec but thin; the extra margin is free because the bottom of the
sweep is handled in firmware rather than by the divider ratio.

**Arduino Uno at 5 V** — connect directly to **A0**, no divider.

**Both** — the module and the microcontroller must **share a ground**. Without a
common ground the input reads noise.

## 2. Record the buzzer change — and note the correction

Lifting the buzzer removes the 23 mA sag at the trigger point, which is worth
doing. But it also removes the only thing holding Q3's collector low.

> **This is a pull-down, not a pull-up.** Q3 is PNP with its emitter on the
> rail, so it drives the collector *high* on alarm; the buzzer is what returns
> the line to ground when Q3 is off. A pull-up to V+ would hold the input high
> permanently and the trigger would never be seen. Use **10 kΩ from Q3's
> collector to ground**.
>
> On the ESP32 the divider already does this — its 30 kΩ to ground replaces the
> buzzer's pull-down, so no extra resistor is needed. The Uno, connected
> directly, needs the 10 kΩ, because AVR inputs offer internal pull-ups only.

Lifting the buzzer is a **deliberate modification to the circuit under test**.
Record it in `data/rig_notes.md` as such, and run a few pilot trials **both with
and without** the buzzer at the same distance. If the trigger voltage shifts
between the two, the modification is not neutral and the result has to be
reported against the unmodified board.

## 3. The signal is read with analogRead(), not a digital pin

A digital pin goes deaf at exactly the voltage this experiment is about.

Q3's collector rises to about `V − 0.1` when the alarm fires, so the swing
scales with the supply — but a logic threshold does not. An ESP32 needs about
0.75 × 3.3 = **2.48 V** to read high; an Uno at 5 V needs 0.6 × 5 = **3.0 V**.

| supply | pin, 10k/15k | pin, 10k/20k | pin, Uno direct |
|---|---|---|---|
| 5.0 V | 2.94 | 3.27 | 4.90 |
| 4.2 V | 2.46 | 2.73 | 4.10 |
| 3.2 V | 1.86 | 2.07 | 3.10 |
| **2.6 V** | **1.50** | **1.67** | **2.50** |

Every entry at 2.6 V is below its threshold. The alarm would fire and the pin
would never notice — and 2.6 V is the region where `V*` is expected to be. The
10k/20k divider goes deaf below about 3.8 V; 10k/15k below about 4.2 V; the Uno
below about 3.1 V.

The fix needs no extra parts: read the line with `analogRead()` and threshold it
in firmware at **450 mV** (558 counts on the ESP32, 92 on the Uno). With Q3 off
the pin sits near 0 V; with Q3 on it clears **1.44 V even at a 2.5 V supply** —
more than three times the threshold, across the whole sweep. A yes/no decision
this coarse does not care about ADC non-linearity.

One cosmetic consequence: the ESP32's ADC compresses above about 3.1 V on the
default attenuation, so the diagnostic `peak_mV` field will plateau near the top
of the sweep instead of tracking the true pin voltage. It is diagnostic only and
nothing depends on it.

## 4. The multimeter is the authority on voltage

The ESP32's ADC is non-linear by tens of millivolts across its range — more than
the effect being measured at some distances. The firmware latches *when* the
trigger happened; the meter says *at what voltage*.

If the firmware is ever made to log voltage as well, calibrate its ADC against
the meter across the whole 3–5 V span first, record the calibration points in
`rig_notes.md`, and still report the meter value as the measurement. The sketch
ships with no ADC logging for this reason.

## 5. Separate commit, before the pilot

This goes in on its own, after the analysis pre-registration and before any
data. The root commit stays untouched.

---

## Using it

115200 baud. `n` arms a trial, `r` resets the counter, `z` prints the pin state
so the wiring can be checked before anything is measured.

Each trial prints one line:

```
trial,t_first_ms,t_confirm_ms,chatter_ms,dropouts,peak_mV
```

`t_first` is the first active sample. `t_confirm` is the first moment the line
had held active continuously for 50 ms. **The gap between them is data, not
noise** — near `V*` the alarm margin collapses, the alarm itself loads the rail,
and the sag pushes it further in. How wide the chatter grows as `V` falls is
itself a prediction of H3, and it would have been invisible to a stopwatch.

### Self-test before the first trial

`z` prints the raw count, the millivolts and the resulting decision.

1. Target far away, supply at 5.0 V — must read **0**.
2. Metal held on the coil, supply at **5.0 V** — must read **1**.
3. Metal held on the coil, supply at **2.6 V** — must **also** read 1.

Step 3 is the one that matters. If it reads 1 at 5.0 V and 0 at 2.6 V, the
decision is still being made against a logic threshold somewhere and the rig
will silently lose every trigger at the bottom of the sweep — which is where the
result lives. Do not take a single trial until step 3 passes.
