/*
 * trigger_latch - records the instant the detector's alarm fires.
 *
 * Replaces the human judgement "has it triggered?" with a measured edge.
 * Reaction time is the largest error in the primary measurement; this removes
 * it, and lifting the buzzer also removes the 23 mA sag at the trigger point.
 *
 * Reads Q3's collector. Q3 is a PNP high-side switch, so the line rises to
 * about (V - 0.1) when the alarm sounds and is held near ground otherwise by
 * the buzzer, or by the pull-down / divider if the buzzer has been lifted.
 *
 * WHY ANALOG AND NOT A DIGITAL PIN
 * The swing scales with the supply, but a logic threshold does not. An ESP32
 * wants about 2.48 V to read high and an Uno about 3.0 V, so near the bottom of
 * the sweep the alarm fires and the pin never notices:
 *
 *     at V = 2.6 V   ESP32 10k/20k -> 1.67 V    ESP32 10k/15k -> 1.50 V
 *                    Uno direct    -> 2.50 V    all below threshold
 *
 * which is precisely where V* lives. So the line is read with analogRead() and
 * thresholded here at 450 mV. When Q3 is off the pin sits near 0 V; when it is
 * on the pin clears 1.4 V even at a 2.5 V supply, so the margin is wide across
 * the whole sweep. ADC non-linearity is irrelevant to a yes/no decision this
 * coarse, and the multimeter remains the authority on voltage.
 *
 * REPORTS TWO INSTANTS PER TRIAL, NOT ONE
 *     t_first    the first sample above threshold
 *     t_confirm  the first moment it had held for STABLE_MS
 * Their difference is the chatter at the trigger point, and it is data: near V*
 * the alarm margin collapses, the alarm loads the rail, and the sag pushes it
 * further in, so the chatter should widen as V falls. That is a second,
 * independent signature of H3, invisible to a stopwatch.
 *
 * Serial: 115200 baud.  n = arm next trial   r = reset counter   z = self-test
 *
 * Kunaal Nirmal Khanwani
 */

#if defined(ESP32)
  #define SENSE_PIN      34      // ADC1, input-only. ADC2 is unusable with WiFi.
  #define ADC_MAX        4095
  #define ADC_FS_MV      3300    // default 11 dB attenuation
#else
  #define SENSE_PIN      A0      // Uno
  #define ADC_MAX        1023
  #define ADC_FS_MV      5000
#endif

#define THRESHOLD_MV   450UL   // Q3 off ~0 mV; Q3 on >=1400 mV worst case.
#define STABLE_MS      50UL    // continuous hold before a trigger is confirmed.
#define SETTLE_MS      300UL   // ignored after arming, for switch bounce.

// A self-oscillating buzzer chops the collector current, so while the buzzer is
// still fitted the line is a pulse train rather than a steady level. Treat it as
// active if any sample in the last HOLD_MS cleared the threshold. With the
// buzzer lifted set this to 0 for the finest chatter resolution.
#define HOLD_MS        10UL

const uint16_t THRESHOLD_COUNTS = (uint16_t)(THRESHOLD_MV * ADC_MAX / ADC_FS_MV);

enum State { ARMED, SEEN, LATCHED };

State    state     = LATCHED;
uint16_t trial     = 0;
uint32_t t_armed   = 0, t_first = 0, t_stable = 0, t_high = 0;
uint16_t dropouts  = 0, peak = 0;

static inline uint16_t mv(uint16_t counts) {
  return (uint16_t)((uint32_t)counts * ADC_FS_MV / ADC_MAX);
}

void arm() {
  trial++;
  state    = ARMED;
  t_armed  = millis();
  t_first  = t_stable = t_high = 0;
  dropouts = peak = 0;
  Serial.print(F("# armed, trial ")); Serial.println(trial);
}

void selftest() {
  uint16_t c = analogRead(SENSE_PIN);
  Serial.print(F("# raw ")); Serial.print(c);
  Serial.print(F("  ")); Serial.print(mv(c)); Serial.print(F(" mV  threshold "));
  Serial.print(THRESHOLD_COUNTS); Serial.print(F(" ("));
  Serial.print(THRESHOLD_MV); Serial.print(F(" mV)  -> "));
  Serial.println(c >= THRESHOLD_COUNTS ? 1 : 0);
}

void setup() {
  Serial.begin(115200);
  pinMode(SENSE_PIN, INPUT);     // external divider / pull-down, never INPUT_PULLUP
  delay(200);
  Serial.println(F("# trial,t_first_ms,t_confirm_ms,chatter_ms,dropouts,peak_mV"));
  Serial.println(F("# n = arm, r = reset counter, z = self-test"));
  selftest();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == 'n') arm();
    else if (c == 'r') { trial = 0; Serial.println(F("# counter reset")); }
    else if (c == 'z') selftest();
  }

  if (state == LATCHED) return;

  uint32_t now = millis();
  if (now - t_armed < SETTLE_MS) return;

  uint16_t counts = analogRead(SENSE_PIN);
  if (counts > peak) peak = counts;
  if (counts >= THRESHOLD_COUNTS) t_high = now;
  bool on = t_high && (now - t_high) <= HOLD_MS;

  if (state == ARMED) {
    if (on) { t_first = t_stable = now; state = SEEN; }
    return;
  }

  // Keep t_first, but restart the hold clock on every dropout, so a confirmed
  // trigger means genuinely continuous and not merely eventual.
  if (!on) {
    if (now - t_stable < STABLE_MS) dropouts++;
    t_stable = now;
    return;
  }

  if (now - t_stable >= STABLE_MS) {
    uint32_t t_confirm = t_stable + STABLE_MS;
    Serial.print(trial);                              Serial.print(',');
    Serial.print(t_first - t_armed);                  Serial.print(',');
    Serial.print(t_confirm - t_armed);                Serial.print(',');
    Serial.print(t_confirm - t_first - STABLE_MS);    Serial.print(',');
    Serial.print(dropouts);                           Serial.print(',');
    Serial.println(mv(peak));
    state = LATCHED;
  }
}
