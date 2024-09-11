import numpy as np
from scipy.optimize import fsolve

def Problem4_1():
    # 定义螺线和圆的参数
    p = 1.7  # 螺距
    R = 4.5  # 大圆的半径
    D = 2 * R  # D = 2 * R

    # 定义螺线的参数方程
    def spiral(theta):
        r = p * theta / (2 * np.pi)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y

    # 定义螺线的导数方程
    def spiral_derivative(theta):
        # r(θ) 的导数
        dr_dtheta = p / (2 * np.pi)
        # 计算导数
        dx_dtheta = dr_dtheta * np.cos(theta) - (p * theta / (2 * np.pi)) * np.sin(theta)
        dy_dtheta = dr_dtheta * np.sin(theta) + (p * theta / (2 * np.pi)) * np.cos(theta)
        return dx_dtheta, dy_dtheta

    # 定义求解方程：螺线与圆的交点
    def equations(theta):
        x, y = spiral(theta)
        return x**2 + y**2 - R**2

    # 初始猜测 theta 值
    theta_guess = 1.0

    # 使用 fsolve 求解交点
    theta_solution = fsolve(equations, theta_guess)
    theta_solution = theta_solution[0]

    # 计算交点坐标
    x_solution, y_solution = spiral(theta_solution)

    # 计算交点处的导数 (dx/dθ, dy/dθ)
    dx_dtheta, dy_dtheta = spiral_derivative(theta_solution)

    # 计算交点处的切线斜率 dy/dx
    slope = dy_dtheta / dx_dtheta

    # 法线的斜率
    normal_slope = -1 / slope

    # 法线与x轴夹角
    beta = np.arctan(normal_slope)

    # 输出螺线的切点坐标
    print(f"螺线切点坐标: ({x_solution}, {y_solution})")

    # 计算对称点坐标
    x_sym, y_sym = -x_solution, -y_solution
    print(f"对称点坐标: ({x_sym}, {y_sym})")

    # 法线方程：y = m * x + c
    # 交点处的法线
    c_solution = y_solution - normal_slope * x_solution
    print(f"法线方程1: y = {normal_slope} * x + {c_solution}")

    # 对称点处的法线
    c_sym = y_sym - normal_slope * x_sym
    print(f"法线方程2: y = {normal_slope} * x + {c_sym}")

    # 计算对称点到法线的距离
    distance = abs(normal_slope * x_sym - y_sym) / np.sqrt(normal_slope**2 + 1)

    # 定义方程以求解 alpha
    def alpha_equation(alpha):
        return (np.sin(alpha)**2) / (1 - np.cos(alpha))**2 - (distance**2) / (D**2 - distance**2)

    # 初始猜测 alpha 值
    alpha_guess = np.pi / 4

    # 使用 fsolve 求解 alpha
    alpha_solution = fsolve(alpha_equation, alpha_guess)

    # 计算 alpha 对应的弧度值
    alpha = alpha_solution[0]
    alpha_degrees = np.degrees(alpha)
    print(f"alpha 为: {alpha} 弧度, 即 {alpha_degrees} 度")

    # 使用 3 * R_1 * sin(alpha) = distance 计算 R_1（小圆半径）
    R_1 = distance / (3 * np.sin(alpha))
    R_2 = 2 * R_1  # 大圆半径
    print(f"小圆半径 R_1: {R_1}")
    print(f"大圆半径 R_2: {R_2}")

    # 计算小圆圆心坐标
    x_small = x_sym - R_1 * np.cos(beta)
    y_small = y_sym - R_1 * np.sin(beta)
    print(f"小圆圆心坐标: ({x_small}, {y_small})")

    # 计算大圆圆心坐标
    x_large = x_solution + R_2 * np.cos(beta)
    y_large = y_solution + R_2 * np.sin(beta)
    print(f"大圆圆心坐标: ({x_large}, {y_large})")

    # 计算大圆和小圆相切点坐标
    x_tangent_large = x_large + R_2 * np.cos(alpha)
    y_tangent_large = y_large + R_2 * np.sin(alpha)
    print(f"大圆和小圆之间的切点坐标: ({x_tangent_large}, {y_tangent_large})")

    # 计算原点处引出的直线与小圆的切点坐标
    # 斜率 m_tangent 为原点到小圆的切线斜率，利用直线和圆相切的条件
    def tangent_slope_equation(m):
        return np.abs(m * x_small - y_small) / np.sqrt(m**2 + 1) - R_1

    # 初始猜测斜率
    m_guess = 1.0  # 下方的切点，选择负斜率

    # 求解斜率 m_tangent
    m_tangent = fsolve(tangent_slope_equation, m_guess)[0]
    print(f"原点到小圆的切线斜率: {m_tangent}")

    # 联立圆的方程和直线方程求解切点坐标
    def circle_line_intersection(x):
        y = m_tangent * x
        return (x - x_small)**2 + (y - y_small)**2 - R_1**2

    # 初始猜测的 x 值
    x_tangent_guess = x_small

    # 使用 fsolve 求解切点的 x 坐标
    x_tangent_small = fsolve(circle_line_intersection, x_tangent_guess)[0]
    y_tangent_small = m_tangent * x_tangent_small

    print(f"原点到小圆的切点坐标: ({x_tangent_small}, {y_tangent_small})")