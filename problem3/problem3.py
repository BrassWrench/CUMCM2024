from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import bisect
from problem2.problem2 import Problem2

class Problem3(Problem2):

    def __init__(self):
        super().__init__()
        self.pitch_critical = None
        self.theta0_critical = None
        self.rectangles_critical = None
        self.x_critical = None
        self.y_critical = None
        self.v_critical = None
        self.collision_radius = {}

    def get_collision_radius(self, p, savefig=False):
        k = p / (2 * np.pi)
        self.set_k(k)
        self.calc_collision_state(previous=True, desc=False)
        if savefig: self.save_collision_fig("problem3/savefig")
        time.sleep(0.1)
        collision_radius = k * self.theta0_collision
        return collision_radius

    def calc_collision_states(self, pmin, pmax, interval, savefig=False):

        for p in tqdm(np.arange(pmin, pmax, interval), desc="对每个螺距求解碰撞半径"):
            collision_radius = self.get_collision_radius(p, savefig)
            self.collision_radius[str(p)] = collision_radius

    def save_pitch_fig(self, direct):
        pitch, collision_radius = [], []
        for key, value in self.collision_radius.items():
            pitch.append(float(key))
            collision_radius.append(value)
        plt.plot(pitch, collision_radius, color="blue", zorder=1)
        #plt.scatter(pitch, collision_radius, color="green", zorder=2)
        plt.plot(pitch, np.ones_like(pitch) * 4.5, linestyle='--', color="orange", zorder=3)
        plt.grid()
        plt.xlabel("螺距p(m)")
        plt.ylabel("碰撞半径", rotation="horizontal")
        plt.savefig(f"{direct}/pitch_and_collision_radius.pdf")
        plt.cla()
        plt.clf()
        plt.close()
        print(f"保存螺距和碰撞半径关系的图像，存放在{direct}文件夹里。")