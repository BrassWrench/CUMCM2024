import numpy as np
from scipy.optimize import fsolve
import matplotlib as mpl
import matplotlib.pyplot as plt

def next_theta(theta, k, d):
    """θ角递推"""
    def f(theta_next):
        return theta**2 + theta_next**2 - 2 * theta * theta_next * np.cos(theta_next - theta) - d**2 / k**2
    x = np.linspace(theta, theta + 3, 1000)
    plt.plot(x, f(x))
    plt.plot(x, np.zeros_like(x))
    theta_next = fsolve(f, theta+1)
    print(f"theta:{np.rad2deg(theta)},{theta}, k:{k}, d:{d}, theta_next:{np.rad2deg(theta_next)},{theta_next}")
    plt.scatter(theta_next, 0)
    plt.show()
    return theta_next

next_theta(32.20, 0.0875, 1.65)