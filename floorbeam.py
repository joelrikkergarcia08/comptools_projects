import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

def max_deflection(P, L, E, I):
    """Maximum deflection of a simply supported beam under uniform load.
    P: load (N), L: length (m), E: Young's modulus (Pa), I: moment of inertia (m^4)."""
    return (5 * P * L**4) / (384 * E * I)

rng = np.random.default_rng()
N = 100_000
w = rng.normal(20, 3, N)
E = rng.normal(200_00, 10_000, N)

delta = max_deflection(w, 6000, E, 3.375e8)
delta.mean(), np.median(delta), delta.std(), np.percentile(delta, 95)

plt.hist(delta, bins=100)
plt.axvline(6, color="red")
plt.xlabel("Deflection (mm)")
plt.show()

p_fail = np.mean(delta > 6)