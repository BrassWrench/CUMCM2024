import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from problem1.problem1 import *

mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "xelatex",
    "pgf.rcfonts": True,
    "pgf.preamble": r"\usepackage{amsmath}"
}
mpl.rcParams.update(pgf_with_pdflatex)
plt.rcParams['font.family'] = 'serif'

def get_rectangle(x, y, x_next, y_next):
    nx = (x_next - x) / np.sqrt((x_next - x) ** 2 + (y_next - y) ** 2)
    ny = (y_next - y) / np.sqrt((x_next - x) ** 2 + (y_next - y) ** 2)
    mx = - ny
    my = nx
    anchor_x = x - nx * 0.275 - mx * 0.15
    anchor_y = y - ny * 0.275 - my * 0.15
    width = np.sqrt((x_next - x) ** 2 + (y_next - y) ** 2) + 2 * 0.275
    height = 0.3
    angle = np.rad2deg(np.arctan2(y_next - y, x_next - x))
    rect = patches.Rectangle((anchor_x, anchor_y), width=width, height=height, angle=angle, rotation_point="xy", linewidth=1, edgecolor='r', facecolor='none')
    return rect

if __name__ == '__main__':

    k = 0.55 / (2 * np.pi)
    d = 2.2 - 2 * 0.275
    d_prime = 3.41 - 2 * 0.275
    v0 = 1
    num = 223
    round_num = 16

    v0 = np.array(v0)
    k = np.array(k)
    d = np.array(d)
    d_prime = np.array(d_prime)
    num = np.array(num)
    round_num = np.array(round_num)

    theta0 = get_theta_from_time(300, k, v0, round_num)
    x, y ,v = get_positions_and_velocities(v0, theta0, k, d, d_prime, num, round_num)
    x_spiral, y_spiral = get_spiral(k, round_num)

    fig, ax = plt.subplots()
    ax.plot(x_spiral, y_spiral, linewidth=1)
    ax.scatter(x, y, s=1, color='green')

    for i in range(len(x) - 1):
        if x[i+1] == 8.8 and y[i+1] == 0:
            break
        rect = get_rectangle(x[i], y[i], x[i + 1], y[i + 1])
        ax.add_patch(rect)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("rectangle_line.pdf")

    # fig, ax = plt.subplots()
    #
    # rect = get_rectangle(-2.88, 4.89, -4.18, 3.88)
    # ax.add_patch(rect)
    # ax.scatter(-2.88, 4.89, c='b', s=2)
    # ax.scatter(-4.18, 3.88, c='y', s=2)
    # ax.scatter(-2.75, 5.17, c='g', s=2)
    #
    # ax.set_xlim(-10, 10)
    # ax.set_ylim(-10, 10)
    # ax.set_aspect('equal', adjustable='box')
    # plt.savefig("a_simple_rectangle.pdf")

