import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from problem1.problem1 import *
from problem2.problem2 import *
from problem3.problem3 import *
from problem4.problem4_1 import *
from problem4.problem4_2 import *
from scipy.optimize import fsolve

mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "xelatex",
    "pgf.rcfonts": True,
    "pgf.preamble": r"\usepackage{amsmath}"
}
mpl.rcParams.update(pgf_with_pdflatex)
plt.rcParams['font.family'] = 'serif'

def next_xi(xi, d):
    def g(xi_next):
        f_xi = f(xi)
        f_xi_next = f(xi_next)
        return f_xi**2 + f_xi_next**2 - 2 * f_xi * f_xi_next * np.cos(xi_next - xi) - d**2
    xi_next = fsolve(g, xi - 1)
    return xi_next

def get_phi(r, r_next, theta, theta_next):
    phi_s = np.arctan((r_next * np.sin(theta_next - theta)) / (r - r_next * np.cos(theta_next - theta)))
    phi_e = phi_s + theta_next - theta
    return phi_s, phi_e

def next_v(v, r, r_next, diff, diff_next, phi_s, phi_e):
    v_next = np.sqrt((diff_next**2 + r_next**2) / (diff**2 + r**2)) * ((diff * np.cos(phi_s) - r * np.sin(phi_s)) / (diff_next * np.cos(phi_e) - r_next * np.sin(phi_e))) * v
    v_next = np.abs(v_next)
    return v_next

def get_f_diff(xi):
    return (f(xi + 0.001) - f(xi)) / 0.001#对xi求导

def get_diff(xi):
    diff = np.sign(xi) * get_f_diff(xi)#对theta求导
    return diff

def get_positions_and_velocities(xi0, v0):

    #龙头位置和速度
    result_x = []
    result_y = []
    result_v = []
    r0 = f(xi0)
    theta0 = xi_to_theta(xi0)
    x0, y0 = get_xy(r0, theta0)
    diff0 = get_diff(xi0)
    result_x.append(x0.item())
    result_y.append(y0.item())
    result_v.append(v0.item())

    #第一个龙身位置和速度，为后续递推做准备
    xi1 = next_xi(xi0, d_prime)
    r1 = f(xi1)
    theta1 = xi_to_theta(xi1)
    x1, y1 = get_xy(r1, theta1)
    diff1 = get_diff(xi1)
    phi_s, phi_e = get_phi(r0, r1, theta0, theta1)
    v1 = next_v(v0, r0, r1, diff0, diff1, phi_s, phi_e)
    result_x.append(x1.item())
    result_y.append(y1.item())
    result_v.append(v1.item())

    #即将进入递推
    xi = xi1
    theta = theta1
    v = v1
    r = r1
    diff = diff1
    for i in range(num-1):
        xi_next = next_xi(xi, d)
        r_next = f(xi_next)
        theta_next = xi_to_theta(xi_next)
        x_next, y_next = get_xy(r_next, theta_next)
        phi_s, phi_e = get_phi(r, r_next, theta, theta_next)
        diff_next = get_diff(xi_next)
        v_next = next_v(v, r, r_next, diff, diff_next, phi_s, phi_e)

        result_x.append(x_next.item())
        result_y.append(y_next.item())
        result_v.append(v_next.item())

        xi = xi_next
        theta = theta_next
        v = v_next
        r = r_next
        diff = diff_next

    return result_x, result_y, result_v

def get_xi_from_t(t, v0):
    xi = xi_to_theta_value(theta1)
    d_xi = 0.001
    integ = 0
    target = v0 * t
    while integ <= target:
        integ += np.sqrt(get_f_diff(xi)**2 + f(xi)**2) * d_xi
        xi += d_xi
    return xi

if __name__ == '__main__':

    x, y ,v = get_positions_and_velocities(15, v0)

    x_track, y_track = get_track(np.max(x) // 1.7 + 1)
    plt.plot(x_track, y_track, linewidth=0.2)
    plt.plot(x, y, linewidth=0.4)
    plt.scatter(x, y, s=0.4)
    plt.savefig("line_graph.pdf")
    plt.cla()

    plt.plot(np.arange(len(v)), v)
    plt.savefig("velocity.pdf")
    plt.cla()
