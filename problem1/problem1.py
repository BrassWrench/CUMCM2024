import numpy as np
from scipy.optimize import fsolve
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import time

mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "xelatex",
    "pgf.rcfonts": True,
    "pgf.preamble": r"\usepackage{amsmath}"
}
mpl.rcParams.update(pgf_with_pdflatex)
plt.rcParams['font.family'] = 'serif'

def next_theta(theta, k, d):
    """θ角递推"""
    def f(theta_next):
        return theta**2 + theta_next**2 - 2 * theta * theta_next * np.cos(theta_next - theta) - d**2 / k**2
    theta_next = fsolve(f, theta + 0.2)#+0.2是为了更好的找到零点
    return theta_next

def get_phi(r, r_next, theta, theta_next):
    phi_s = np.arctan((r_next * np.sin(theta_next - theta)) / (r - r_next * np.cos(theta_next - theta)))
    phi_e = phi_s + theta_next - theta
    return phi_s, phi_e

def next_v_theta(v_theta, phi_s, phi_e, r, r_next, k):
    """速度vθ递推"""
    v_theta_next = ((k / r) * np.cos(phi_s) - np.sin(phi_s)) / ( (k / r_next) * np.cos(phi_e) - np.sin(phi_e)) * v_theta
    return v_theta_next

def get_r(theta, k):
    """螺线公式"""
    r = k * theta
    return r

def get_v_r(v_theta, k, r):
    """vr与vθ关系"""
    v_r = (k / r) * v_theta
    return v_r

def get_v(v_r, v_theta):
    v = np.sqrt(v_r**2 + v_theta**2)
    return v

def get_xy(r, theta):
    """求绝对坐标"""
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def get_positions_and_velocities(v0, theta0, k, d, d_prime, num, round_num):
    """递推求位置和速度"""

    #龙头位置和速度
    result_x = []
    result_y = []
    result_v = []
    r0 = get_r(theta0, k)
    x0, y0 = get_xy(r0, theta0)
    v_theta_0 = - v0 / np.sqrt((k / r0)**2 + 1)
    result_x.append(x0.item())
    result_y.append(y0.item())
    result_v.append(v0.item())

    #第一个龙身位置和速度，为后续递推做准备
    theta1 = next_theta(theta0, k, d_prime)

    if theta1 >= round_num * 2 * np.pi:
        result_x.extend([k * round_num * 2 * np.pi for _ in range((num))])
        result_y.extend([0 for _ in range(num)])
        result_v.extend([0 for _ in range(num)])
        return result_x, result_y, result_v

    r1 = get_r(theta1, k)
    x1, y1 = get_xy(r1, theta1)
    phi_s, phi_e = get_phi(r0, r1, theta0, theta1)
    v_theta_1 = next_v_theta(v_theta_0, phi_s, phi_e, r0, r1, k)
    v_r_1 = get_v_r(v_theta_1, k, r1)
    v1 = get_v(v_r_1, v_theta_1)
    result_x.append(x1.item())
    result_y.append(y1.item())
    result_v.append(v1.item())

    #即将进入递推
    theta = theta1
    v_theta = v_theta_1
    r = r1

    for i in range(num-1):
        theta_next = next_theta(theta, k, d)

        if theta_next >= round_num * 2 * np.pi:
            result_x.extend([k * round_num * 2 * np.pi for _ in range(num - 1 - i)])
            result_y.extend([0 for _ in range(num - 1 - i)])
            result_v.extend([0 for _ in range(num - 1 - i)])
            return result_x, result_y, result_v

        r_next = get_r(theta_next, k)
        x_next, y_next = get_xy(r_next, theta_next)
        phi_s, phi_e = get_phi(r, r_next, theta, theta_next)
        v_theta_next = next_v_theta(v_theta, phi_s, phi_e, r, r_next, k)
        v_r_next = get_v_r(v_theta_next, k, r_next)
        v_next = get_v(v_r_next, v_theta_next)

        result_x.append(x_next.item())
        result_y.append(y_next.item())
        result_v.append(v_next.item())

        theta = theta_next
        v_theta = v_theta_next
        r = r_next

    return result_x, result_y, result_v

def get_spiral(k, round_num):
    theta = np.linspace(0, 2 * np.pi * round_num, 1000)
    r = k * theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def get_theta_from_time(t, k ,v, round_num):
    theta_m = round_num * 2 * np.pi
    def f(theta):
        return (1/2) * theta * np.sqrt(1 + theta ** 2) + (1/2) * np.arcsinh(theta) - (1/2) * theta_m * np.sqrt(1 + theta_m ** 2) + (1/2) * np.arcsinh(theta_m) + v * t / k
    theta = fsolve(f, np.array(0))
    return theta

if __name__ == '__main__':

    k = 0.55 / (2 * np.pi)
    d = 2.2 - 2 * 0.275
    d_prime = 3.41 - 2 * 0.275
    v0 = 1
    num = 223
    round_num = 16

    v0 = np.array(v0)
    k = np.array(k)
    d = np.array(d)
    d_prime = np.array(d_prime)
    num = np.array(num)
    round_num = np.array(round_num)

    theta0 = get_theta_from_time(300, k, v0, round_num)

    x, y ,v = get_positions_and_velocities(v0, theta0, k, d, d_prime, num, round_num)

    x_spiral, y_spiral = get_spiral(k, round_num)
    plt.plot(x_spiral, y_spiral)
    plt.plot(x, y)
    plt.scatter(x, y)
    plt.savefig("line_graph.pgf")

    df_positions = pd.read_excel("result1.xlsx", sheet_name="位置")
    df_velocities = pd.read_excel("result1.xlsx", sheet_name="速度")

    for t in tqdm(range(300 + 1), desc="进度"):
        theta0 = get_theta_from_time(t, k, v0, round_num)
        x, y ,v = get_positions_and_velocities(v0, theta0, k, d, d_prime, num, round_num)
        for i in range(223 + 1):
            df_positions.iloc[2 * i, t + 1] = x[i]
            df_positions.iloc[2 * i + 1, t + 1] = y[i]
            df_velocities.iloc[i, t + 1] = v[i]

    with pd.ExcelWriter("result1.xlsx") as writer:
        df_positions.to_excel(writer, sheet_name="位置", index=False, float_format="%.6f")
        df_velocities.to_excel(writer, sheet_name="速度", index=False, float_format="%.6f")