import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from problem1.problem1_old import *
from problem2.problem2_old import *

mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "xelatex",
    "pgf.rcfonts": True,
    "pgf.preamble": r"\usepackage{amsmath}"
}
mpl.rcParams.update(pgf_with_pdflatex)
plt.rcParams['font.family'] = 'serif'

def get_collision_by_theta(theta0_start, v0, k, d, d_prime, num, round_num):
    theta0_collision = 0
    rectangles_collision = []
    x_collision, y_collision, v_collision = [], [], []
    for theta0 in np.flip(np.arange(1, theta0_start, 0.1)):
        print(f"theta0:{theta0:.1f}")
        x, y ,v = get_positions_and_velocities(v0, theta0, k, d, d_prime, num, round_num)
        rectangles = get_rectangles(x, y)
        if check_collision(rectangles):
            print("撞了！")
            theta0_collision  = theta0
            rectangles_collision = rectangles
            x_collision, y_collision, v_collision = x, y, v
            break
    return theta0_collision, rectangles_collision, x_collision, y_collision, v_collision

if __name__ == '__main__':

    delta = 0.55
    theta0_lowest, rectangles_lowest, x_lowest, y_lowest, v_lowest = [], [], [], [], []

    d = 2.2 - 2 * 0.275
    d_prime = 3.41 - 2 * 0.275
    v0 = 1
    num = 223
    turn_radius = 9 / 2
    k = delta / (2 * np.pi)
    round_num = 16

    v0 = np.array(v0)
    d = np.array(d)
    d_prime = np.array(d_prime)
    num = np.array(num)
    delta = np.array(delta)
    k = np.array(k)
    round_num = np.array(round_num)

    # theta_collision, rectangles_collision, x_collision, y_collision, v_collision = get_collision_by_theta(26, v0, k, d, d_prime, num, round_num)
    #
    # fig, ax = plt.subplots()
    # ax.plot(x_spiral, y_spiral, linewidth=1)
    # ax.scatter(x_collision, y_collision, s=1, color='green')
    # for rectangle in rectangles_collision:
    #     ax.add_patch(rectangle)
    #
    # ax.set_xlim(-10, 10)
    # ax.set_ylim(-10, 10)
    # ax.set_aspect('equal', adjustable='box')
    # plt.savefig("tet.pdf")

    delta = 0.45

    while delta > 0:
        #delta -= 0.01
        k = delta / (2 * np.pi)
        round_num = 16 * 0.55 / delta

        theta0_collision, rectangles_collision, x_collision, y_collision, v_collision = get_collision_by_theta(64, v0, k, d, d_prime, num, round_num)

        x_spiral, y_spiral = get_spiral(k, round_num)
        fig, ax = plt.subplots()
        ax.plot(x_spiral, y_spiral, linewidth=1)
        ax.scatter(x_collision, y_collision, s=1, color='green')
        for rectangle in rectangles_collision:
            ax.add_patch(rectangle)

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect('equal', adjustable='box')
        plt.savefig(f"rectangle_line/rectangle_line_{delta:.2f}.pdf")
        plt.savefig(f"rectangle_line/rectangle_line_{delta:.2f}.pgf")
        plt.close(fig)

        collision_radius = np.sqrt(x_collision[0]**2 + y_collision[0]**2)
        print(f"collision_radius:{collision_radius}")
        if collision_radius > turn_radius:
            theta0_lowest, rectangles_lowest, x_lowest, y_lowest, v_lowest = theta0_collision, rectangles_collision, x_collision, y_collision, v_collision
            break

    fig, ax = plt.subplots()
    ax.plot(x_spiral, y_spiral, linewidth=1)
    ax.scatter(x_lowest, y_lowest, s=1, color='green')

    for rectangle in rectangles_lowest:
        ax.add_patch(rectangle)

    ax.text(-10, 10, s=f"delta={delta}")

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("lowest_delta.pdf")
    plt.savefig("lowest_delta.pgf")
    plt.close(fig)

