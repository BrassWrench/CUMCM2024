import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from problem1.problem1 import *
from problem2.problem2 import *
from problem3.problem3 import *

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
r3 = np.sqrt(cut_point3[0] ** 2 + cut_point3[1] ** 2)
theta3_r = theta2 - (np.arctan2(cut_point2[1], cut_point2[0]) - np.arctan2(cut_point3[1], cut_point3[0]))
r4 = np.sqrt(cut_point4[0] ** 2 + cut_point4[1] ** 2)
theta4 = - r4 / k
theta3_l = theta4 + (np.arctan2(cut_point4[1], cut_point4[0]) - np.arctan2(cut_point3[1], cut_point3[0]))

theta_r = theta3_r
theta_l = theta3_l
delta_theta = theta_r - theta_l

def xi_to_theta_value(xi):
    if xi <= theta_r:
        return xi - delta_theta
    return xi

def xi_to_theta(xi):
    if isinstance(xi, (np.ndarray, list, tuple)):
        return np.array([xi_to_theta_value(xi) for xi in xi])
    else:
        return xi_to_theta_value(xi)

def theta_to_xi_value(theta):
    if theta <= theta_l:
        return theta + delta_theta
    elif theta_l <= theta <= theta_r:
        return np.nan
    return theta

def theta_to_xi(theta):
    if isinstance(theta, (np.ndarray, list, tuple)):
        return np.array([theta_to_xi_value(theta) for theta in theta])
    else:
        return theta_to_xi_value(theta)

def f_value(xi):
    theta = xi_to_theta(xi)
    if theta > theta1:
        return k * theta
    elif theta2 <= theta <= theta1:
        return O1[0] * np.cos(theta) + O1[1] * np.sin(theta) + np.sqrt(R1**2 - (O1[0] * np.sin(theta) - O1[1] * np.cos(theta)) ** 2)
    elif theta3_r <= theta <= theta2:
        return O2[0] * np.cos(theta) + O2[1] * np.sin(theta) - np.sqrt(R2**2 - (O2[0] * np.sin(theta) - O2[1] * np.cos(theta)) ** 2)
    elif theta4<= theta <= theta3_l:
        return - O2[0] * np.cos(theta) + O2[1] * np.sin(theta) + np.sqrt(R2**2 - ( - O2[0] * np.sin(theta) - O2[1] * np.cos(theta)) ** 2)
    elif theta <= theta4:
        return - k * theta
    return np.nan

def f(xi):
    if isinstance(xi, (np.ndarray, list, tuple)):
        return np.array([f_value(xi) for xi in xi])
    else:
        return f_value(xi)

def get_xy_value(r, xi):
    theta = xi_to_theta(xi)
    x = np.sign(theta) * r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def get_xy(r, xi):
    if isinstance(xi, (np.ndarray, list, tuple)) and isinstance(r, (np.ndarray, list, tuple)):
        x = []
        y = []
        for r, xi in zip(r, xi):
            x_now, y_now = get_xy_value(r, xi)
            x.append(x_now)
            y.append(y_now)
        return np.array(x), np.array(y)
    else:
        return f_value(xi)

def paint_trace():
    fig, ax = plt.subplots()

    theta = np.arange(- 5 * 2 * np.pi, 5 * 2 * np.pi + 0.01, 0.001)
    xi = theta_to_xi(theta)
    r = f(xi)
    x, y = get_xy(r, xi)
    ax.plot(x, y)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("f_theta.pdf")
    plt.savefig("f_theta.pgf")
    plt.cla()

    theta = np.arange(- 5 * 2 * np.pi, 5 * 2 * np.pi + 0.01, 0.001)
    xi = theta_to_xi(theta)
    r = f(xi)
    ax.plot(xi, r)

    ax.set_xlim(theta_to_xi(- 5 * 2 * np.pi), theta_to_xi(5 * 2 * np.pi))
    ax.set_ylim(0, 10)
    ax.set_xlabel("$\\xi$")
    ax.set_ylabel("$r$")
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("f_value.pdf")
    plt.savefig("f_value.pgf")
    plt.cla()

paint_trace()

