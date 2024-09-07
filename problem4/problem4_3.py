import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from problem4.problem4_2 import Problem4_2
from problem4.problem4_2_old import xi_to_theta


class Problem4_3:
    def __init__(self, d_body, d_head, v0, num):
        self.d_body = d_body
        self.d_head = d_head
        self.v0 = v0
        self.num = num

        self.problem4_2 = Problem4_2()
        self.f = self.problem4_2.f
        self.get_xy = self.problem4_2.get_xy
        self.xi_to_theta = self.problem4_2.xi_to_theta
        self.theta_to_xi = self.problem4_2.theta_to_xi
        self.get_in_and_out = self.problem4_2.get_in_and_out

    def next_xi(self, xi, is_head=False):
        d = self.d_head if is_head else self.d_body
        def g(xi_prime):
            f_xi = self.f(xi)
            f_xi_prime = self.f(xi_prime)
            return f_xi ** 2 + f_xi_prime ** 2 - 2 * f_xi * f_xi_prime * np.cos(xi_prime - xi) - d ** 2
        xi_next = fsolve(g, xi - 1)
        return xi_next

    def next_v(self, v, xi, xi_next):
        theta, theta_next = self.xi_to_theta(xi), self.xi_to_theta(xi_next)
        x, y = self.get_xy(xi)
        x_next, y_next = self.get_xy(xi_next)
        f, f_next = self.f(xi), self.f(xi_next)
        diff_f, diff_f_next = self.get_diff_theta(xi), self.get_diff_theta(xi_next)
        k_board = (y_next - y) / (x_next - x)
        k_curve = (diff_f * np.sin(theta) + f * np.cos(theta)) / (diff_f * np.cos(theta) - f * np.sin(theta))
        k_curve_next = (diff_f_next * np.sin(theta_next) + f * np.cos(theta_next)) / (diff_f_next * np.cos(theta_next) - f * np.sin(theta_next))
        phi = np.arctan(k_curve) - np.arctan(k_board)
        phi_next = np.arctan(k_curve_next) - np.arctan(k_board)
        v_next = np.abs((np.cos(phi) / np.cos(phi_next)) * v)
        return v_next

    def next_state(self, xi, v, is_head=False):
        xi_next = self.next_xi(xi, is_head)
        v_next = self.next_v(v, xi, xi_next)
        return xi_next, v_next

    def get_diff_theta(self, xi):
        return np.sign(xi) * self.get_diff_xi(xi)

    def get_diff_xi(self, xi):
        return (self.f(xi + 0.00001) - self.f(xi)) / 0.00001

    def get_positions_and_velocities(self, xi0):
        """求每个节点的位置和速度"""
        v0, num = self.v0, self.num
        x0, y0 = self.get_xy(xi0)
        result_x = np.array([x0])
        result_y = np.array([y0])
        result_v = np.array([v0])

        xi = xi0
        v = v0

        for i in range(num + 1):
            theta_next, v_next = self.next_state(xi, v, is_head=(i == 0))
            x_next, y_next = self.get_xy(theta_next)
            result_x = np.append(result_x, x_next)
            result_y = np.append(result_y, y_next)
            result_v = np.append(result_v, v_next)
            xi, v = theta_next, v_next

        return result_x, result_y, result_v

    def t_to_xi0(self, t, v0):
        xi = self.theta_to_xi(self.problem4_2.theta1, state="in")
        if t == 0: return xi
        target = v0 * t
        direct = np.sign(target)
        integ = 0
        d_xi = direct * 0.001
        while direct * integ < direct * target:
            integ += np.sqrt(self.get_diff_xi(xi) ** 2 + self.f(xi) ** 2) * d_xi
            xi += d_xi
        return xi

    def save_t_state(self, t, direct):
        xi0 = self.t_to_xi0(t, self.v0)
        x, y, v = self.get_positions_and_velocities(xi0)

        xi = self.get_in_and_out((np.max(np.abs(x)) // 1.7 + 2) * 2 * np.pi, 0.001)
        x_curve, y_curve = self.get_xy(xi)
        fig, ax = plt.subplots()
        plt.plot(x_curve, y_curve, linewidth=0.2)
        plt.plot(x, y, linewidth=0.4)
        plt.scatter(x, y, s=0.4)
        plt.scatter(x[0], y[0], s=1, c='r')
        ax.set_xlim(-np.max(np.abs(x_curve)), np.max(np.abs(x_curve)))
        ax.set_ylim(-np.max(np.abs(y_curve)), np.max(np.abs(y_curve)))
        ax.set_aspect('equal', adjustable='box')
        plt.savefig(f"{direct}/state_{str(t)}s.pdf")
        plt.cla()
        plt.clf()
        plt.close()

        plt.plot(np.arange(1, len(v) + 1), v)
        plt.grid()
        plt.savefig(f"{direct}/velocities_{str(t)}s.pdf")
        plt.cla()
        plt.clf()
        plt.close()