import numpy as np  
import matplotlib.pyplot as plt

def turbine_power(v, theta, eta, rho=1.225, D=80):
    """Power of one wind turbine in MW.
    v: wind speed (m/s), theta: wind direction (degrees),
    eta: efficiency (0 to 1), rho: air density (kg/m^3), D: rotor diameter (m)."""
    A = np.pi * D**2 / 4                          # swept area, m^2
    v_eff = v * np.cos(np.radians(theta - 90))    # wind component facing the rotor
    return 0.5 * rho * A * eta * v_eff**3 / 1e6   # W -> MW

# beta parameters (a, b) of the 10 turbine efficiencies
ab = np.array([[5, 2], [6, 2], [4, 1.5], [5, 1.5],
               [7, 2], [6, 3], [5, 2.5], [8, 3],
               [4, 2], [6, 2]])

np.random.seed(1)
N = 10_000                                        # simulated days

v = np.random.normal(8, 1.5, (N, 1))              # m/s, the same for all turbines
theta = np.random.normal(90, 15, (N, 1))          # degrees, the same for all turbines
eta = 0.62 + 0.33 * np.random.beta(ab[:, 0], ab[:, 1], (N, 10))   # 62 % to 95 %

power = turbine_power(v, theta, eta)              # shape (N, 10), MW
energy = 24 * power.sum(axis=1)                   # MWh per day, shape (N,)

eta_mean = 0.62 + 0.33 * ab[:, 0] / ab.sum(axis=1)
print("best guess (average inputs): %.0f MWh" % (24 * turbine_power(8, 90, eta_mean).sum()))
print("mean %.0f MWh, median %.0f MWh" % (np.mean(energy), np.median(energy)))
p95 = np.percentile(energy, 5)                    # exceeded on 95 % of days
print("P95: at least %.0f MWh on 95 %% of days" % p95)

plt.hist(energy, bins=60, density=True, color="skyblue", edgecolor="black")
plt.axvline(p95, color="red", linestyle="--", label="P95 = %.0f MWh" % p95)
plt.xlabel("Energy generated in one day (MWh)")
plt.ylabel("Density")
plt.legend()
plt.show()