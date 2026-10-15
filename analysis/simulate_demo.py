"""
SIMULATED demonstration of how the hypotheses separate. NOT experimental data.

For each pre-registered distance, a sweep from 5.00 V downward records the voltage of
the first change in alarm state. Synthetic detectors with ILLUSTRATIVE parameters:
  H3 (oscillator margin): alarm switches ON at V_trig = V*/(1 - K g^2)
  H1/H2 (fixed threshold): alarm switches OFF at V_off = T / g^2
  H0 (ratiometric): no change of state inside the sweep (on throughout, or off throughout)
Reading noise 0.01 V; values rounded to 2 decimals as on the DMM.
Output: figures/SIMULATED_hypothesis_test.png
Run: python analysis/simulate_demo.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = 17.5
D = np.array([10, 12, 15, 20, 25, 30, 35, 40], float)
VMIN, VMAX = 2.50, 5.00
rng = np.random.default_rng(1)
g2 = lambda d: A**4 / (A**2 + d**2) ** 3
noisy = lambda v: np.round(v + rng.normal(0, 0.01, np.size(v)), 2)

VSTAR, K = 2.30, 400.0              # illustrative only
T = 0.0035                          # illustrative only

v3 = VSTAR / (1 - K * g2(D))
v1 = T / g2(D)
in3 = (v3 > VMIN) & (v3 < VMAX)
in1 = (v1 > VMIN) & (v1 < VMAX)

fig, ax = plt.subplots(figsize=(6.4, 4.4))
x3, y3 = 1 / noisy(v3[in3]), g2(D[in3])
x1, y1 = 1 / noisy(v1[in1]), g2(D[in1])
ax.plot(x3, y3, "o", color="black", label="H3: alarm switches ON (slope < 0)")
ax.plot(x1, y1, "^", color="black", mfc="white", label="H1/H2: alarm switches OFF (through origin, slope > 0)")
for x, y in [(x3, y3), (x1, y1)]:
    m, c = np.polyfit(x, y, 1)
    xx = np.linspace(0, 0.45, 50)
    ax.plot(xx, m * xx + c, "-", color="grey", lw=0.8)
    print(f"slope {m:+.5f} intercept {c:+.6f}" + (f"  fitted V* {-m/c:.3f} V, K {1/c:.0f} mm^2" if m < 0 else ""))
ax.axhline(0, color="black", lw=0.5)
ax.set_xlim(0, 0.45)
ax.set_xlabel("1 / V at change of state  (V$^{-1}$)")
ax.set_ylabel("g(d)$^2$  (mm$^{-2}$)")
ax.set_title("SIMULATED — illustrative parameters, not measurements.\nH0 produces no change of state in the sweep.", fontsize=9)
ax.legend(frameon=False, fontsize=7.5, loc="upper left")
fig.tight_layout()
fig.savefig("figures/SIMULATED_hypothesis_test.png", dpi=200)
print("H3 in-range distances:", D[in3].astype(int).tolist(), " H1 in-range:", D[in1].astype(int).tolist())
