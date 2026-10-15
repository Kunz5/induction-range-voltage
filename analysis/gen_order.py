"""Generates the pre-registered randomised trial order. Seed 20261014. Run: python analysis/gen_order.py"""
import random
SEED=20261014
rng=random.Random(SEED)
D=[10,12,15,20,25,30,35,40]
def block():
    while True:
        b=D[:]+rng.sample(D,2)
        rng.shuffle(b)
        if all(b[i]!=b[i+1] for i in range(len(b)-1)): return b
# 4 blocks of 10 = 40 trials; each distance exactly 5 times overall
while True:
    blocks=[block() for _ in range(4)]
    flat=[d for b in blocks for d in b]
    if all(flat.count(d)==5 for d in D) and all(blocks[i][-1]!=blocks[i+1][0] for i in range(3)): break
n=1
for i,b in enumerate(blocks,1):
    print(f"Block {i}: no-target V* sweep (start)")
    for d in b: print(f"  P{n:02d}  {d} mm"); n+=1
    print(f"Block {i}: no-target V* sweep (end)")
V=[5.0,4.2,3.6,3.2]
while True:
    s=[v for v in V for _ in range(3)]; rng.shuffle(s)
    if all(s[i]!=s[i+1] for i in range(len(s)-1)): break
print("Secondary:", ", ".join(f"S{i+1:02d} {v} V" for i,v in enumerate(s)))
