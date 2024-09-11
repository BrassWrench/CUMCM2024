import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from problem4.problem4_3 import Problem4_3

class Problem5(Problem4_3):

    def __init__(self):
        super().__init__()
        self.t = None
        self.v_t = None
        self.vmax_t = None

    def calc_v_t(self, tmin, tmax, interval):
        """计算tmin到tmax的速度情况（也就是每一个t对应的225个节点的v）"""
        self.t = np.arange(tmin, tmax, interval)
        _, _, self.v_t = self.get_t_state(self.t[0])
        for t_now in tqdm(self.t[1:], desc=f"计算从{tmin}s到{tmax}s的速度情况，模拟时间间隔为{interval}"):
            _, _, v_now = self.get_t_state(t_now)
            self.v_t = np.vstack((self.v_t, v_now))
        self.v_t = self.v_t.T

    def calc_vmax_t(self):
        "计算t时刻速度v的最大值"
        self.vmax_t = np.max(self.v_t, axis=0)

    def save_v_and_vmax_t_fig(self, direct):
        plt.plot(self.t, self.vmax_t, color="red", linewidth=2, zorder=2, label="整条舞龙队的速度最大值")
        plt.plot(self.t, self.v_t[0], color="deepskyblue", linewidth=1, alpha=0.5, zorder=1, label="每个舞龙队把手的速度")
        for v_n_t in self.v_t[1:]:
            plt.plot(self.t, v_n_t, color="deepskyblue", linewidth=1, alpha=0.5, zorder=1)
        plt.grid()
        plt.legend()
        plt.xlabel("时间t/(s)", x=0.9)
        plt.ylabel("速度v(m/s)", rotation="horizontal", y = 1)
        plt.tight_layout()
        plt.savefig(f"{direct}/v_and_vmax_t.pdf")
        plt.cla()
        plt.clf()
        plt.close()