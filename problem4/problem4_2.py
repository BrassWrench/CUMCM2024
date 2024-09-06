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

def f(theta):
    if theta > theta1:
        return k * theta
    elif theta2 <= theta <= theta1:
        return O1[0] * np.cos(theta) + O1[1] * np.sin(theta) + np.sqrt(R1**2 - (O1[0] * np.sin(theta) - O1[1] * np.cos(theta)) ** 2)
    elif theta3_r <= theta <= theta2:
        return O2[0] * np.cos(theta) + O2[1] * np.sin(theta) - np.sqrt(R2**2 - (O2[0] * np.sin(theta) - O2[1] * np.cos(theta)) ** 2)
    elif theta4 <= theta <= theta3_l:
        return - O2[0] * np.cos(theta) + O2[1] * np.sin(theta) + np.sqrt(R2**2 - ( - O2[0] * np.sin(theta) - O2[1] * np.cos(theta)) ** 2)
    elif theta <= theta4:
        return - k * theta
    return np.nan

def get_xy(r, theta, inverse=False):
    if inverse:
        x = - r * np.cos(theta)
        y = r * np.sin(theta)
    else:
        x = r * np.cos(theta)
        y = r * np.sin(theta)
    return x, y

def paint_trace():
    fig, ax = plt.subplots()

    theta = np.arange(theta1, 5 * 2 * np.pi + 0.01, 0.01)
    r = np.array([f(theta) for theta in theta])
    x, y = get_xy(r, theta)
    ax.plot(x, y)

    theta = np.arange(theta2, theta1, 0.01)
    r = np.array([f(theta) for theta in theta])
    x, y = get_xy(r, theta)
    ax.plot(x, y)

    theta = np.arange(theta3_r, theta2, 0.01)
    r = np.array([f(theta) for theta in theta])
    x, y = get_xy(r, theta)
    ax.plot(x, y)

    theta = np.arange(theta4, theta3_l + 0.01, 0.01)
    r = np.array([f(theta) for theta in theta])
    x, y = get_xy(r, theta, inverse=True)
    ax.plot(x, y)

    theta = np.arange(- 5 * 2 * np.pi, theta4 + 0.01, 0.01)
    r = np.array([f(theta) for theta in theta])
    x, y = get_xy(r, theta, inverse=True)
    ax.plot(x, y)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("f_theta.pdf")
    plt.savefig("f_theta.pgf")

paint_trace()