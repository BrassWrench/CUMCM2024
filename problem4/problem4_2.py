import matplotlib.pyplot as plt
import numpy as np

class Problem4_2:

    slope = np.array(1.17086605)  # 两条直线的斜率
    intercept1 = np.array(-0.41585755)  # 直线1的截距
    intercept2 = np.array(0.41585755)  # 直线2的截距
    cut_point1 = np.array((-2.711855863706647, -3.591077522761084))  # 第一个圆和第一段螺线的切点
    cut_point2 = np.array((0.903951954500684, 1.1970258408177847))  # 两个圆的切点
    cut_point3 = np.array((2.361918498354993, 1.082285086397807))  # 坐标原点对第二个圆的切点
    cut_point4 = np.array((2.711855863706647, 3.591077522761084))  # 第二个圆和第二段螺线的切点
    R1 = np.array(3.0054176677561504)  # 第一个圆的半径
    R2 = np.array(1.5027088338780752)  # 第二个圆的半径
    O1 = np.array((-0.7600091139658178, -1.3057264286867012))  # 第一个圆的圆心
    O2 = np.array((1.7359324888362324, 2.4484019757238924))  # 第二个圆的圆心
    k = np.array(1.7 / (2 * np.pi))

    r1 = np.sqrt(cut_point1[0] ** 2 + cut_point1[1] ** 2)
    theta1 = np.array(r1 / k)
    r2 = np.sqrt(cut_point2[0] ** 2 + cut_point2[1] ** 2)
    theta2 = theta1 - (np.arctan2(cut_point1[1], cut_point1[0]) + 2 * np.pi - np.arctan2(cut_point2[1], cut_point2[0]))
    r4 = np.sqrt(cut_point4[0] ** 2 + cut_point4[1] ** 2)
    theta4 = np.array(r4 / k + np.pi)
    r3 = np.sqrt(cut_point3[0] ** 2 + cut_point3[1] ** 2)
    theta3_in = theta2 - (np.arctan2(cut_point2[1], cut_point2[0]) - np.arctan2(cut_point3[1], cut_point3[0]))
    theta3_out = theta4 - (np.arctan2(cut_point4[1], cut_point4[0]) - np.arctan2(cut_point3[1], cut_point3[0]))

    theta_in = theta3_in
    theta_out = theta3_out

    def __init__(self):
        pass

    def xi_to_theta_value(self, xi):
        theta_in, theta_out = self.theta_in, self.theta_out
        if xi <= 0:
            return - xi + theta_in
        elif xi >= 0:
            return xi + theta_out

    def xi_to_theta(self, xi):
        if xi.shape == ():
            return self.xi_to_theta_value(xi)
        return np.array([self.xi_to_theta_value(xi) for xi in xi])

    def theta_to_xi_value(self, theta, state):
        theta_in, theta_out = self.theta_in, self.theta_out
        if state == "in" and theta >= theta_in:
            return - (theta - theta_in)
        elif state == "out" and theta >= theta_out:
            return theta - theta_out
        return np.nan

    def theta_to_xi(self, theta, state):
        if theta.shape == ():
            return self.theta_to_xi_value(theta, state)
        return np.array([self.theta_to_xi_value(theta, state) for theta in theta])

    def f_value(self, xi):
        theta1, theta2, theta3_in, theta3_out, theta4 = self.theta1, self.theta2, self.theta3_in, self.theta3_out, self.theta4
        O1, O2, R1, R2 = self.O1, self.O2, self.R1, self.R2
        k = self.k
        r3 = self.r3

        if xi < 0:
            theta = self.xi_to_theta_value(xi)
            if theta > theta1:
                return k * theta
            elif theta2 <= theta <= theta1:
                return O1[0] * np.cos(theta) + O1[1] * np.sin(theta) + np.sqrt(
                    R1 ** 2 - (O1[0] * np.sin(theta) - O1[1] * np.cos(theta)) ** 2)
            elif theta3_in <= theta <= theta2:
                return O2[0] * np.cos(theta) + O2[1] * np.sin(theta) - np.sqrt(
                    R2 ** 2 - (O2[0] * np.sin(theta) - O2[1] * np.cos(theta)) ** 2)
        elif xi > 0:
            theta = self.xi_to_theta_value(xi)
            if theta3_out <= theta <= theta4:
                return O2[0] * np.cos(theta) + O2[1] * np.sin(theta) + np.sqrt(
                    R2 ** 2 - (O2[0] * np.sin(theta) - O2[1] * np.cos(theta)) ** 2)
            elif theta >= theta4:
                return k * (theta - np.pi)
        else:
            return r3

    def f(self, xi):
        if xi.shape == ():
            return self.f_value(xi)
        return np.array([self.f_value(xi) for xi in xi])

    def get_xy_value(self, xi):
        theta = self.xi_to_theta_value(xi)
        f_xi = self.f_value(xi)
        x = f_xi * np.cos(theta)
        y = f_xi * np.sin(theta)
        return x, y

    def get_xy(self, xi):
        if xi.shape == ():
            return self.get_xy_value(xi)
        x = np.array([])
        y = np.array([])
        for xi in xi:
            x_now, y_now = self.get_xy_value(xi)
            x = np.append(x, x_now)
            y = np.append(y, y_now)
        return x, y

    def get_in_and_out(self, theta_max, interval):
        theta_in, theta_out = self.theta_in, self.theta_out
        xi_in = self.theta_to_xi(np.flip(np.arange(theta_in, theta_max + interval, interval)), state="in")
        xi_out = self.theta_to_xi(np.arange(theta_out, theta_max + np.pi + interval, interval), state="out")
        xi = np.hstack((xi_in, xi_out))
        return xi

    def save_curve(self, direct):
        fig, ax = plt.subplots()

        xi = self.get_in_and_out(5 * 2 * np.pi, 0.001)
        x, y = self.get_xy(xi)
        ax.plot(x, y)

        ax.set_xlim(-np.max(np.abs(x)), np.max(np.abs(x)))
        ax.set_ylim(-np.max(np.abs(y)), np.max(np.abs(y)))
        ax.set_aspect('equal', adjustable='box')
        plt.savefig(f"{direct}/curve.pdf")
        plt.cla()
        plt.clf()
        plt.close()

    def save_r_xi(self, direct):

        xi = self.get_in_and_out(5 * 2 * np.pi, 0.001)
        r = self.f(xi)

        fig, ax = plt.subplots()
        ax.plot(xi, r)
        ax.set_xlim(-15, 15)
        ax.set_ylim(0, 10)
        ax.set_xlabel("$\\xi$")
        ax.set_ylabel("$r$", rotation="horizontal")
        ax.set_aspect('equal', adjustable='box')
        ax.grid()
        plt.savefig(f"{direct}/r_xi.pdf")
        plt.cla()
        plt.clf()
        plt.close()