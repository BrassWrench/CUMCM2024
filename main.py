import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from problem1.problem1 import *
from problem2.problem2 import *
from problem3.problem3 import *

def get_inverse_spiral(k, round_num):
    theta = np.linspace(np.pi, round_num * 2 * np.pi + np.pi, 1000)
    r = k * (theta - np.pi)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

x_spiral, y_spiral = get_spiral(1.7 / (2 * np.pi), 4)
plt.plot(x_spiral, y_spiral)

x_spiral, y_spiral = get_inverse_spiral(1.7 / (2 * np.pi), 4)
plt.plot(x_spiral, y_spiral)

plt.savefig("two_spiral.pdf")
plt.savefig("two_spiral.pgf")