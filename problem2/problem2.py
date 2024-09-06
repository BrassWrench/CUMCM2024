import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from shapely.geometry import Polygon
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
    rect = patches.Rectangle((anchor_x, anchor_y), width=width, height=height, angle=angle, rotation_point="xy", linewidth=0.5, edgecolor='b', facecolor='none')
    return rect

def get_rectangles(x, y):
    rectangles = []
    for i in range(len(x) - 1):
        if x[i+1] == 8.8 and y[i+1] == 0:
            break
        rect = get_rectangle(x[i], y[i], x[i + 1], y[i + 1])
        rectangles.append(rect)
    return rectangles

def is_overlap(rect1_corner, rect2_corner):
    rect1 = Polygon(rect1_corner)
    rect2 = Polygon(rect2_corner)
    return rect1.intersects(rect2)

def check_collision(rectangles):
    is_collision = False
    for i in range(len(rectangles)):
        for j in range(i + 2, len(rectangles)):
            if is_overlap(rectangles[i].get_corners(), rectangles[j].get_corners()):
                is_collision = True
                rectangles[i].set_edgecolor('r')
                rectangles[j].set_edgecolor('r')
                break
        if is_collision:
            break
    return is_collision

def get_collision(t_start):
    t_collision = 0
    rectangles_collision = []
    x_collision, y_collision, v_collision = [], [], []
    for t in np.arange(t_start, 500, 1):
        theta0 = get_theta_from_time(t, k, v0, round_num)
        x, y ,v = get_positions_and_velocities(v0, theta0, k, d, d_prime, num, round_num)
        rectangles = get_rectangles(x, y)
        if check_collision(rectangles):
            t_collision  = t
            rectangles_collision = rectangles
            x_collision, y_collision, v_collision = x, y, v
            break
    return t_collision, rectangles_collision, x_collision, y_collision, v_collision

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
    x_spiral, y_spiral = get_spiral(k, round_num)

    t_collision, rectangles_collision, x_collision, y_collision, v_collision = get_collision(400)

    fig, ax = plt.subplots()
    ax.plot(x_spiral, y_spiral, linewidth=1)
    ax.scatter(x_collision, y_collision, s=1, color='green')
    for rectangle in rectangles_collision:
        ax.add_patch(rectangle)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("rectangle_line.pdf")
    plt.savefig("rectangle_line.pgf")

    df = pd.read_excel("result2.xlsx", sheet_name="Sheet1")

    for i in range(224):
        df.iloc[i, 1] = x_collision[i]
        df.iloc[i, 2] = y_collision[i]
        df.iloc[i, 3] = v_collision[i]

    with pd.ExcelWriter("result2.xlsx") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False, float_format="%.6f")

