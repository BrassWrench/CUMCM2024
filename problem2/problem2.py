import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from shapely.geometry import Polygon
from problem1.problem1 import Problem1
from tqdm import tqdm
import pandas as pd

class Problem2(Problem1):

    def __init__(self):
        super().__init__()
        self.theta0_collision = None
        self.rectangles_collision = None
        self.x_collision = None
        self.y_collision = None
        self.v_collision = None

    def get_rectangle(self, x, y, x_next, y_next):
        nx = (x_next - x) / np.sqrt((x_next - x) ** 2 + (y_next - y) ** 2)
        ny = (y_next - y) / np.sqrt((x_next - x) ** 2 + (y_next - y) ** 2)
        mx = - ny
        my = nx
        anchor_x = x - nx * 0.275 - mx * 0.15
        anchor_y = y - ny * 0.275 - my * 0.15
        width = np.sqrt((x_next - x) ** 2 + (y_next - y) ** 2) + 2 * 0.275
        height = 0.3
        angle = np.rad2deg(np.arctan2(y_next - y, x_next - x))
        rect = patches.Rectangle((anchor_x, anchor_y), width=width, height=height, angle=angle, rotation_point="xy", linewidth=0.5, edgecolor='b', facecolor='none', zorder=3)
        return rect

    def get_rectangles(self, x, y):
        rectangles = []
        for i in range(len(x) - 1):
            rect = self.get_rectangle(x[i], y[i], x[i + 1], y[i + 1])
            rectangles.append(rect)
        return rectangles

    def is_overlap(self, rect1, rect2):
        rect1 = Polygon(rect1.get_corners())
        rect2 = Polygon(rect2.get_corners())
        return rect1.intersects(rect2)

    def check_collision(self, rectangles, theta0):
        for i in range(2, int((2 * np.pi * self.k * theta0 + 4 * np.pi ** 2) / self.d_body)):
            if self.is_overlap(rectangles[0], rectangles[i]):
                rectangles[0].set_edgecolor('r')
                rectangles[i].set_edgecolor('r')
                return True

        # for i in range(3, int((2 * np.pi * self.k * self.problem1.next_theta(theta0, is_head=True) + 4 * np.pi ** 2) / self.d_body)):
        #     if self.is_overlap(rectangles[1], rectangles[i]):
        #         rectangles[1].set_edgecolor('r')
        #         rectangles[i].set_edgecolor('r')
        #         return True

        return False

    def calc_collision_state(self, previous=False, desc=True):
        start_theta0 = self.theta0_collision if previous else self.init_theta0
        if start_theta0 is None: start_theta0 = self.init_theta0
        it = tqdm(np.flip(np.arange(0, start_theta0, 0.1)), desc=f"计算螺距为{float(self.k * 2 * np.pi):.2f}的碰撞点") if desc else np.flip(np.arange(0, start_theta0, 0.1))
        for theta0 in it:
            x, y, v = self.get_positions_and_velocities(theta0)
            rectangles = self.get_rectangles(x, y)
            if self.check_collision(rectangles, theta0):
                self.theta0_collision, self.rectangles_collision, self.x_collision, self.y_collision, self.v_collision =  theta0, rectangles, x, y, v
                return

    def get_curve(self, round_num):
        """求螺旋曲线"""
        k = self.k
        theta = np.arange(0, round_num * 2 * np.pi, 0.01)
        x = k * theta * np.cos(theta)
        y = k * theta * np.sin(theta)
        return x, y

    def save_collision_fig(self, direct):
        fig, ax = plt.subplots()
        x_curve, y_curve = self.get_curve(np.max(np.abs(self.x_collision)) // (2 * np.pi * self.k) + 2)
        ax.plot(x_curve, y_curve, linewidth=1, zorder=1)
        ax.scatter(self.x_collision, self.y_collision, s=1, color='green', zorder=2)
        for rectangle in self.rectangles_collision:
            ax.add_patch(rectangle)
        ax.set_xlim(-np.max(np.abs(x_curve)), np.max(np.abs(x_curve)))
        ax.set_ylim(-np.max(np.abs(y_curve)), np.max(np.abs(y_curve)))
        ax.set_aspect('equal', adjustable='box')
        plt.savefig(f"{direct}/collision_state_{self.k * 2 * np.pi : .2f}.pdf")
        plt.cla()
        plt.clf()
        plt.close()
        print(f"保存螺距为{self.k * 2 * np.pi : .2f}碰撞状态图像为collision_state_{self.k * 2 * np.pi : .2f}.pdf，存放在{direct}文件夹里。")

    def save_result(self):
        df = pd.read_excel("problem2/result2.xlsx", sheet_name="Sheet1")

        for i in range(224):
            df.iloc[i, 1] = self.x_collision[i]
            df.iloc[i, 2] = self.y_collision[i]
            df.iloc[i, 3] = self.v_collision[i]

        df.columns.values[0] = ''

        with pd.ExcelWriter("problem2/result2.xlsx") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False, float_format="%.6f")

        print("已将碰撞结果保存到result2.xlsx中。")
