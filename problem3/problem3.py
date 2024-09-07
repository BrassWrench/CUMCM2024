import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import fsolve
from problem2.problem2 import Problem2

class Problem3:

    def __init__(self, d_body, d_head, v0, num, init_theta0):
        self.d_body = np.array(d_body)
        self.d_head = np.array(d_head)
        self.v0 = np.array(v0)
        self.num = np.array(num)
        self.init_theta0 = np.array(init_theta0)
        self.pitch_critical = None
        self.theta0_critical = None
        self.rectangles_critical = None
        self.x_critical = None
        self.y_critical = None
        self.v_critical = None
        self.collision_radius = {}

    def get_collision_radius(self, p, savefig=False):
        problem2 = Problem2(0, self.d_body, self.d_head, self.v0, self.num, self.init_theta0)
        k = p / (2 * np.pi)
        problem2.set_k(k)
        problem2.calc_collision_state()
        if savefig: problem2.save_collision_fig("problem3/savefig")
        time.sleep(0.1)
        collision_radius = k * problem2.theta0_collision
        return collision_radius

    def calc_collision_states(self, pmin, pmax, interval, savefig=False):
        for p in np.arange(pmin, pmax, interval):
            collision_radius = self.get_collision_radius(p, savefig)
            self.collision_radius[str(p)] = collision_radius

    def calc_critical_pitch(self):
        critical_pitch = fsolve(lambda p : self.get_collision_radius(p) - 4.5, x0=np.array(0.45), xtol=0.001)
        critical_pitch = critical_pitch[0]
        print(critical_pitch)
        print(self.get_collision_radius(critical_pitch))
        return critical_pitch

    def save_pitch_fig(self, direct):
        pitch, collision_radius = [], []
        for key, value in self.collision_radius.items():
            pitch.append(float(key))
            collision_radius.append(value)
        plt.plot(pitch, collision_radius, color="blue", zorder=1)
        plt.scatter(pitch, collision_radius, color="green", zorder=2)
        plt.plot(pitch, np.ones_like(pitch) * 4.5, linestyle='--', color="orange", zorder=3)
        plt.grid()
        plt.xlabel("螺距p(m)")
        plt.ylabel("碰撞半径")
        plt.savefig(f"{direct}/pdf/pitch_and_collision_radius.pdf")
        plt.savefig(f"{direct}/pgf/pitch_and_collision_radius.pgf")
        plt.cla()
        plt.clf()
        plt.close()
        print(f"保存螺距和碰撞半径关系的图像，存放在{direct}/pdf和{direct}/pgf文件夹里。")