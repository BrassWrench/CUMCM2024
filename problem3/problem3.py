import numpy as np
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
from problem2.problem2 import Problem2


class Problem3(Problem2):

    def __init__(self):
        super().__init__()
        self.pitch_critical = None
        self.collision_radius_critical = None
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
        pass_critical = False
        for p in tqdm(np.arange(pmin, pmax, interval), desc="对每个螺距求解碰撞半径"):
            collision_radius = self.get_collision_radius(p, savefig)
            if collision_radius < 4.5 and not pass_critical:
                pass_critical = True
                self.pitch_critical = p
                self.collision_radius_critical = collision_radius
                self.theta0_critical = self.theta0_collision
                self.rectangles_critical = self.rectangles_collision
                self.x_critical = self.x_collision
                self.y_critical = self.y_collision
                self.v_critical = self.v_collision
            self.collision_radius[str(p)] = collision_radius

    def save_pitch_fig(self, direct):
        pitch, collision_radius = [], []
        for key, value in self.collision_radius.items():
            pitch.append(float(key))
            collision_radius.append(value)
        plt.plot(pitch, collision_radius, color="blue", zorder=1)
        plt.scatter(self.pitch_critical, self.collision_radius_critical, color="red", zorder=2)
        plt.plot(pitch, np.ones_like(pitch) * 4.5, linestyle='--', color="orange", zorder=3)
        plt.grid()
        plt.xlabel("螺距p(m)")
        plt.ylabel("碰撞半径", rotation="horizontal", labelpad=10)
        plt.savefig(f"{direct}/pitch_and_collision_radius.pdf")
        plt.cla()
        plt.clf()
        plt.close()
        print(f"保存螺距和碰撞半径关系的图像，存放在{direct}文件夹里。")