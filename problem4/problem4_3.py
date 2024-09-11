import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import fsolve
from tqdm import tqdm
from problem4.problem4_2 import Problem4_2


class Problem4_3(Problem4_2):

    d_head = 3.41 - 2 * 0.275
    d_body = 2.2 - 2 * 0.275
    v0 = 1
    num = 223

    def __init__(self):
        super().__init__()

    def next_xi(self, xi, is_head=False):
        """ξ迭代"""
        d = self.d_head if is_head else self.d_body
        def g(xi_prime):
            f_xi = self.f(xi)
            f_xi_prime = self.f(xi_prime)
            return f_xi ** 2 + f_xi_prime ** 2 - 2 * f_xi * f_xi_prime * np.cos(xi_prime - xi) - d ** 2
        xi_next = fsolve(g, xi - 1)
        return xi_next

    def next_v(self, v, xi, xi_next):
        """速度v迭代，用显式求导公式"""
        theta, theta_next = self.xi_to_theta(xi), self.xi_to_theta(xi_next)
        x, y = self.get_xy(xi)
        x_next, y_next = self.get_xy(xi_next)
        f, f_next = self.f(xi), self.f(xi_next)
        diff_f, diff_f_next = self.get_diff_theta(xi), self.get_diff_theta(xi_next)
        k_board = (y_next - y) / (x_next - x)
        k_curve = (diff_f * np.sin(theta) + f * np.cos(theta)) / (diff_f * np.cos(theta) - f * np.sin(theta))
        k_curve_next = (diff_f_next * np.sin(theta_next) + f_next * np.cos(theta_next)) / (diff_f_next * np.cos(theta_next) - f_next * np.sin(theta_next))
        phi = np.arctan(k_curve) - np.arctan(k_board)
        phi_next = np.arctan(k_curve_next) - np.arctan(k_board)
        v_next = np.abs((np.cos(phi) / np.cos(phi_next)) * v)
        return v_next

    def next_state(self, xi, v, is_head=False):
        """下一个状态迭代"""
        xi_next = self.next_xi(xi, is_head)
        v_next = self.next_v(v, xi, xi_next)
        return xi_next, v_next

    def get_diff_theta_value(self, xi):
        """求对θ的导数"""
        theta1, theta2, theta3_in, theta3_out, theta4 = self.theta1, self.theta2, self.theta3_in, self.theta3_out, self.theta4
        R1, R2 = self.R1, self.R2
        r_o1, theta_o1, r_o2, theta_o2 = self.r_o1, self.theta_o1, self.r_o2, self.theta_o2
        k = self.k

        if xi < 0:
            theta = self.xi_to_theta_value(xi)
            if theta > theta1:
                return k
            elif theta2 <= theta <= theta1:
                return -r_o1 * np.sin(theta - theta_o1) + (- 2 * r_o1 * np.cos(theta - theta_o1) *
                            np.sin(theta - theta_o1)) / np.sqrt(R1 ** 2 - r_o1 ** 2 + (r_o1 * np.cos(theta - theta_o1)) ** 2)
            elif theta3_in <= theta <= theta2:
                return -r_o2 * np.sin(theta - theta_o2) - (- 2 * r_o2 * np.cos(theta - theta_o2) *
                            np.sin(theta - theta_o2)) / np.sqrt(R2 ** 2 - r_o2 ** 2 + (r_o2 * np.cos(theta - theta_o2)) ** 2)
        elif xi > 0:
            theta = self.xi_to_theta_value(xi)
            if theta3_out <= theta <= theta4:
                return -r_o2 * np.sin(theta - theta_o2) + (- 2 * r_o2 * np.cos(theta - theta_o2) *
                            np.sin(theta - theta_o2)) / np.sqrt(R2 ** 2 - r_o2 ** 2 + (r_o2 * np.cos(theta - theta_o2)) ** 2)
            elif theta >= theta4:
                return k
        else:
            return 0

    def get_diff_theta(self, xi):
        """求对θ的导数"""
        if xi.shape == ():
            return self.get_diff_theta_value(xi)
        return np.array([self.get_diff_theta_value(xi) for xi in xi])

    def get_diff_xi(self, xi):
        """求对ξ的导数"""
        return np.sign(xi) * self.get_diff_theta(xi)

    def get_positions_and_velocities(self, xi0):
        """求对ξ的导数"""
        v0, num = self.v0, self.num
        x0, y0 = self.get_xy(xi0)
        result_x = np.array([x0])
        result_y = np.array([y0])
        result_v = np.array([v0])

        xi = xi0
        v = v0

        for i in range(num + 1):
            xi_next, v_next = self.next_state(xi, v, is_head=(i == 0))
            x_next, y_next = self.get_xy(xi_next)
            result_x = np.append(result_x, x_next)
            result_y = np.append(result_y, y_next)
            result_v = np.append(result_v, v_next)
            xi, v = xi_next, v_next

        return result_x, result_y, result_v

    def t_to_xi0(self, t):
        xi = self.theta_to_xi(self.theta1, state="in")
        if t == 0: return xi
        target = self.v0 * t
        direct = np.sign(target)
        integ = 0
        d_xi = direct * 0.001
        while direct * integ < direct * target:
            integ += np.sqrt(self.get_diff_xi(xi) ** 2 + self.f(xi) ** 2) * d_xi
            xi += d_xi
        return xi

    def get_t_state(self, t):
        xi0 = self.t_to_xi0(t)
        x, y, v = self.get_positions_and_velocities(xi0)
        return x, y, v

    def save_t_state(self, t, direct):
        x, y, v = self.get_t_state(t)
        xi = self.get_in_and_out((np.max(np.abs(x)) // 1.7 + 1) * 2 * np.pi, 0.001)
        x_curve, y_curve = self.get_xy(xi)
        fig, ax = plt.subplots()
        ax.plot(x_curve, y_curve, linewidth=1, zorder=1, color='blue')
        ax.plot(x, y, linewidth=2, zorder=2, color='chocolate')
        ax.scatter(x[1:], y[1:], s=5, zorder=3, color='royalblue')
        ax.scatter(x[0], y[0], s=10, zorder=3, color='red')
        ax.set_xlim(-np.max(np.abs(x_curve)), np.max(np.abs(x_curve)))
        ax.set_ylim(-np.max(np.abs(y_curve)), np.max(np.abs(y_curve)))
        ax.set_aspect('equal', adjustable='box')
        plt.savefig(f"{direct}/state_{t}s.pdf")
        print(f"保存t={t}s的图像为state_{t}s.pdf，存放在{direct}文件夹里。")
        plt.cla()
        plt.clf()
        plt.close()

    def save_result(self):
        df_positions = pd.read_excel("result/result4.xlsx", sheet_name="位置")
        df_velocities = pd.read_excel("result/result4.xlsx", sheet_name="速度")

        for t in tqdm(np.arange(-100, 100 + 1, 1), desc="计算-100s到100s情况并保存到result4.xlsx中"):
            xi0 = self.t_to_xi0(t)
            x, y, v = self.get_positions_and_velocities(xi0)
            for i in range(223 + 1):
                df_positions.loc[2 * i, str(t) + " s"] = x[i]
                df_positions.loc[2 * i + 1, str(t) + " s"] = y[i]
                df_velocities.loc[i, str(t) + " s"] = v[i]

        df_positions.columns.values[0] = ''
        df_velocities.columns.values[0] = ''

        with pd.ExcelWriter("result/result4.xlsx") as writer:
            df_positions.to_excel(writer, sheet_name="位置", index=False, float_format="%.6f")
            df_velocities.to_excel(writer, sheet_name="速度", index=False, float_format="%.6f")
