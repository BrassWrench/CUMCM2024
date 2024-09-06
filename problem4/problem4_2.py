import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from problem1.problem1 import *
from problem2.problem2 import *
from problem3.problem3 import *
from scipy.optimize import fsolve

mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "xelatex",
    "pgf.rcfonts": True,
    "pgf.preamble": r"\usepackage{amsmath}"
}
mpl.rcParams.update(pgf_with_pdflatex)
plt.rcParams['font.family'] = 'serif'

slope = np.array(1.17086605)  # 两条直线的斜率
intercept1 = np.array(-0.41585755)  # 直线1的截距
intercept2 = np.array(0.41585755)   # 直线2的截距
cut_point1 = np.array((-2.711855863706647, -3.591077522761084))#第一个圆和第一段螺线的切点
cut_point2 = np.array((0.903951954500684,1.1970258408177847))#两个圆的切点
cut_point3 = np.array((2.361918498354993, 1.082285086397807))#坐标原点对第二个圆的切点
cut_point4 = np.array((2.711855863706647, 3.591077522761084))#第二个圆和第二段螺线的切点
R1=np.array(3.0054176677561504)#第一个圆的半径
R2=np.array(1.5027088338780752)#第二个圆的半径
O1 = np.array((-0.7600091139658178,-1.3057264286867012))#第一个圆的圆心
O2 = np.array((1.7359324888362324,2.4484019757238924))#第二个圆的圆心
k = np.array(1.7 / (2 * np.pi))

r1 = np.sqrt(cut_point1[0] ** 2 + cut_point1[1] ** 2)
theta1 = r1 / k
r2 = np.sqrt(cut_point2[0] ** 2 + cut_point2[1] ** 2)
theta2 =  theta1 - (np.arctan2(cut_point1[1], cut_point1[0]) + 2 * np.pi - np.arctan2(cut_point2[1], cut_point2[0]))
r4 = np.sqrt(cut_point4[0] ** 2 + cut_point4[1] ** 2)
theta4 = r4 / k + np.pi
r3 = np.sqrt(cut_point3[0] ** 2 + cut_point3[1] ** 2)
theta3_in = theta2 - (np.arctan2(cut_point2[1], cut_point2[0]) - np.arctan2(cut_point3[1], cut_point3[0]))
theta3_out = theta4 - (np.arctan2(cut_point4[1], cut_point4[0]) - np.arctan2(cut_point3[1], cut_point3[0]))

theta_in = theta3_in
theta_out = theta3_out

def xi_to_theta_value(xi):
    if xi <= 0:
        return - xi + theta_in
    elif xi >= 0:
        return xi + theta_out

def xi_to_theta(xi):
    if isinstance(xi, (np.ndarray, list, tuple)):
        return np.array([xi_to_theta_value(xi) for xi in xi])
    else:
        return xi_to_theta_value(xi)

def theta_to_xi_value(theta, state):
    if state == "in" and theta >= theta_in:
        return - (theta - theta_in)
    elif state == "out" and theta >= theta_out:
        return theta - theta_out
    return np.nan

def theta_to_xi(theta, state):
    if isinstance(theta, (np.ndarray, list, tuple)):
        return np.array([theta_to_xi_value(theta, state) for theta in theta])
    else:
        return theta_to_xi_value(theta, state)

def get_in_and_out(theta_max, interval):
    xi_in = theta_to_xi(np.flip(np.arange(theta_in, theta_max + interval, interval)), state="in")
    xi_out = theta_to_xi(np.arange(theta_out, theta_max + np.pi + interval, interval), state="out")
    xi = np.hstack((xi_in, xi_out))
    return xi

def f_value(xi):
    if xi < 0:
        theta = xi_to_theta_value(xi)
        if theta > theta1:
            return k * theta
        elif theta2 <= theta <= theta1:
            return O1[0] * np.cos(theta) + O1[1] * np.sin(theta) + np.sqrt(R1 ** 2 - (O1[0] * np.sin(theta) - O1[1] * np.cos(theta)) ** 2)
        elif theta3_in <= theta <= theta2:
            return O2[0] * np.cos(theta) + O2[1] * np.sin(theta) - np.sqrt(R2 ** 2 - (O2[0] * np.sin(theta) - O2[1] * np.cos(theta)) ** 2)
    elif xi > 0:
        theta = xi_to_theta_value(xi)
        if theta3_out <= theta <= theta4:
            return O2[0] * np.cos(theta) + O2[1] * np.sin(theta) + np.sqrt(R2 ** 2 - (O2[0] * np.sin(theta) - O2[1] * np.cos(theta)) ** 2)
        elif theta >= theta4:
            return k * (theta - np.pi)
    else: return r3

def f(xi):
    if isinstance(xi, (np.ndarray, list, tuple)):
        return np.array([f_value(xi) for xi in xi])
    else:
        return f_value(xi)

def get_xy_value(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def get_xy(r, theta):
    if isinstance(r, (np.ndarray, list, tuple)) and isinstance(theta, (np.ndarray, list, tuple)):
        x = []
        y = []
        for r, theta in zip(r, theta):
            x_now, y_now = get_xy_value(r, theta)
            x.append(x_now)
            y.append(y_now)
        return np.array(x), np.array(y)
    else:
        return get_xy_value(r, theta)

def paint_trace():

    fig, ax = plt.subplots()

    xi = get_in_and_out(5 * 2 * np.pi, 0.001)
    r = f(xi)
    theta = xi_to_theta(xi)
    x, y = get_xy(r, theta)
    ax.plot(x, y)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("f_theta.pdf")
    plt.savefig("f_theta.pgf")
    plt.cla()

    xi = get_in_and_out(5 * 2 * np.pi, 0.001)
    r = f(xi)
    ax.plot(xi, r)

    ax.set_xlim(theta_to_xi(5 * 2 * np.pi, state="in"), theta_to_xi(5 * 2 * np.pi, state="out"))
    ax.set_ylim(0, 10)
    ax.set_xlabel("$\\xi$")
    ax.set_ylabel("$r$")
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("f_value.pdf")
    plt.savefig("f_value.pgf")
    plt.cla()

def next_xi(xi, d):
    def g(xi_next):
        f_xi = f(xi)
        f_xi_next = f(xi_next)
        return f_xi**2 + f_xi_next**2 - 2 * f_xi * f_xi_next * np.cos(f_xi_next - f_xi) - d**2
    xi_next = fsolve(g, xi + 0.2)
    return xi_next

paint_trace()
