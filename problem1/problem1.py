import numpy as np
from ply.yacc import resultlimit
from scipy.optimize import fsolve
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

delta = 0.55
k = np.array(delta / (2 * np.pi))  # r=kθ的比例系数
d_body = np.array(2.2 - 2 * 0.275)  # 龙头长度
d_head = np.array(3.41 - 2 * 0.275)  # 龙身长度
v0 = np.array(1)  # 龙头速度
num = np.array(223)  # 板凳个数
init_theta0 = np.array(16 * 2 * np.pi)  # 龙头初始位置

def next_theta(theta, is_head=False):
    """θ角递推"""
    global k, d_head, d_body
    d = d_head if is_head else d_body
    def h(theta_prime):
        return theta ** 2 + theta_prime ** 2 - 2 * theta * theta_prime * np.cos(theta_prime - theta) - d ** 2 / k ** 2
    theta_next = fsolve(h, theta + 1)
    return theta_next

def next_v(v, theta, theta_next):
    """速度v递推"""
    x, y = get_xy(theta)
    x_next, y_next = get_xy(theta_next)
    k_board = (y_next - y) / (x_next - x)
    k_curve = (np.sin(theta) + theta * np.cos(theta)) / (np.cos(theta) - theta * np.sin(theta))
    k_curve_next = (np.sin(theta_next) + theta_next * np.cos(theta_next)) / (np.cos(theta_next) - theta_next * np.sin(theta_next))
    phi = np.arctan(k_curve) - np.arctan(k_board)
    phi_next = np.arctan(k_curve_next) - np.arctan(k_board)
    v_next = np.abs((np.cos(phi) / np.cos(phi_next)) * v)
    return v_next

def next_state(theta, v, is_head=False):
    """递推下一把手状态"""
    theta_next = next_theta(theta, is_head)
    v_next = next_v(v, theta, theta_next)
    return theta_next, v_next

def get_xy(theta):
    """极坐标求直角坐标"""
    global k
    x = k * theta * np.cos(theta)
    y = k * theta * np.sin(theta)
    return x, y

def get_positions_and_velocities(theta0):
    """求每个节点的位置和速度"""
    global k, v0, num
    x0, y0 = get_xy(theta0)
    result_x = np.array([x0])
    result_y = np.array([y0])
    result_v = np.array([v0])

    theta = theta0
    v = v0

    for i in range(num + 1):
        theta_next, v_next = next_state(theta, v, is_head=(i == 0))
        x_next, y_next = get_xy(theta_next)
        result_x = np.append(result_x, x_next)
        result_y = np.append(result_y, y_next)
        result_v = np.append(result_v, v_next)
        theta, v = theta_next, v_next

    return result_x, result_y, result_v

def t_to_theta0(t):
    """根据时间求龙头位置"""
    global init_theta0, v0
    def f(theta0_prime):
        return (1/2) * np.arcsinh(theta0_prime) + (1/2) * theta0_prime * np.sqrt(1 + theta0_prime ** 2) - (1/2) * np.arcsinh(init_theta0) - (1/2) * init_theta0 * np.sqrt(1 + init_theta0 ** 2) + v0 * t / k
    theta0 = fsolve(f, 0)
    return theta0

def get_curve(round_num):
    global k
    theta = np.arange(0, round_num * 2 * np.pi, 0.01)
    x = k * theta * np.cos(theta)
    y = k * theta * np.sin(theta)
    return x, y

def save_t_fig(t):
    global delta

    theta0 = t_to_theta0(t)
    x, y ,v = get_positions_and_velocities(theta0)
    x_curve, y_curve = get_curve(np.max(np.abs(x)) // delta + 2)

    fig, ax = plt.subplots()
    ax.plot(x_curve, y_curve, linewidth=1, zorder=1, color='b')
    ax.plot(x, y, linewidth=2, zorder=2, color='orange')
    ax.scatter(x[1:], y[1:], s=3, zorder=3, color='g')
    ax.scatter(x[0], y[0], s=10, zorder=3, color='r')
    ax.set_xlim(-np.max(np.abs(x_curve)), np.max(np.abs(x_curve)))
    ax.set_ylim(-np.max(np.abs(y_curve)), np.max(np.abs(y_curve)))
    ax.set_aspect('equal', adjustable='box')
    plt.savefig(f"problem1/savefig/pdf/{t}s.pdf")
    plt.savefig(f"problem1/savefig/pgf/{t}s.pgf")
    plt.cla()

def save_xlsx():

    df_positions = pd.read_excel("problem1/result1.xlsx", sheet_name="位置")
    df_velocities = pd.read_excel("problem1/result1.xlsx", sheet_name="速度")

    for t in tqdm(range(300 + 1), desc="第一问计算时刻t"):
        theta0 = t_to_theta0(t)
        x, y ,v = get_positions_and_velocities(theta0)
        for i in range(223 + 1):
            df_positions.loc[2 * i, f"{t} s"] = x[i]
            df_positions.loc[2 * i + 1, f"{t} s"] = y[i]
            df_velocities.loc[i, f"{t} s"] = v[i]

    df_positions.columns.values[0] = ''
    df_velocities.columns.values[0] = ''

    with pd.ExcelWriter("problem1/result1.xlsx") as writer:
        df_positions.to_excel(writer, sheet_name="位置", index=False, float_format="%.6f")
        df_velocities.to_excel(writer, sheet_name="速度", index=False, float_format="%.6f")