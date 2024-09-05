import numpy as np
import matplotlib.pyplot as plt

# 定义等距螺线的方程
def archimedean_spiral(a, b, theta):
    r = a + b * theta
    return r

# 计算弧长增量，防止溢出
def arc_length_increment(a, b, theta1, theta2):
    r1 = archimedean_spiral(a, b, theta1)
    r2 = archimedean_spiral(a, b, theta2)
    # 限制 delta_theta 和 delta_r 范围以避免溢出
    delta_theta = np.clip(theta2 - theta1, -np.pi, np.pi)
    delta_r = np.clip(r2 - r1, -1e6, 1e6)
    # 使用更稳健的弧长增量公式
    ds = np.hypot(r1 * delta_theta, delta_r)  # np.hypot 防止溢出
    return ds

# 计算两个点之间的直线距离
def distance_between_points(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# 模拟线段两端点的运动，后一个端点在满足条件后开始进入螺线
def simulate_motion_with_fixed_start(a, b, theta_start, segment_length, speed, total_time, delta_t):
    theta_front = theta_start
    theta_back = theta_start  # 后一个点初始位置与前一个点相同
    positions_front = []
    positions_back = []
    times = np.arange(0, total_time, delta_t)
    
    # 记录螺线起点的坐标
    r_start = archimedean_spiral(a, b, theta_start)
    x_start = r_start * np.cos(theta_start)
    y_start = r_start * np.sin(theta_start)
    
    # 标志后一个点是否开始移动
    back_point_started = False
    
    for t in times:
        # 前一个点的坐标
        r_front = archimedean_spiral(a, b, theta_front)
        x_front = r_front * np.cos(theta_front)
        y_front = r_front * np.sin(theta_front)
        positions_front.append((x_front, y_front))
        
        # 检测前一个点与起点的距离
        current_distance = distance_between_points(x_front, y_front, x_start, y_start)
        if not back_point_started and current_distance >= segment_length:
            back_point_started = True  # 后一个点开始移动
        
        if back_point_started:
            # 后一个点开始移动，并保持与前一个点距离为 segment_length
            r_back = archimedean_spiral(a, b, theta_back)
            x_back = r_back * np.cos(theta_back)
            y_back = r_back * np.sin(theta_back)
            
            # 调整后一个点的位置，使其保持与前一个点距离为 segment_length
            current_distance = distance_between_points(x_front, y_front, x_back, y_back)
            if current_distance < segment_length:
                # 增大后一个点的径向距离以保持固定距离
                r_back += (segment_length - current_distance)
            elif current_distance > segment_length:
                # 减小后一个点的径向距离以保持固定距离
                r_back -= (current_distance - segment_length)
            
            # 更新后一个点的坐标
            x_back = r_back * np.cos(theta_back)
            y_back = r_back * np.sin(theta_back)
            positions_back.append((x_back, y_back))
            
            # 计算后一个点的角度变化，基于恒定线速度
            s_back = speed * delta_t  # 计算后一个点的目标弧长增量
            theta_back_next = theta_back - s_back / b  # 计算下一个角度
            # 调整后一个点的角度，使其保持线速度为 1
            while arc_length_increment(a, b, theta_back, theta_back_next) > s_back:
                theta_back_next += (arc_length_increment(a, b, theta_back, theta_back_next) - s_back) / b
            theta_back = theta_back_next  # 更新后一个点的角度
        
        else:
            # 后一个点在起点位置保持不动
            positions_back.append((x_start, y_start))
        
        # 计算前一个点的角度变化，基于恒定线速度
        s_front = speed * delta_t  # 计算前一个点的目标弧长增量
        theta_front_next = theta_front - s_front / b  # 计算下一个角度
        # 调整前一个点的角度，使其保持线速度为 1
        while arc_length_increment(a, b, theta_front, theta_front_next) > s_front:
            theta_front_next += (arc_length_increment(a, b, theta_front, theta_front_next) - s_front) / b
        theta_front = theta_front_next  # 更新前一个点的角度
    
    return np.array(positions_front), np.array(positions_back), times

# 参数设置
a = 0  # 起始半径
b = 0.55/(np.pi * 2)  # 螺线的扩展速度
theta_start = 32 * np.pi  # 起始角度
segment_length = 2.86  # 线段长度
speed = 1  # 前一个点的线速度恒定为 1 m/s
n_times = 2  # 模拟的时间倍数
total_time = 300  # 模拟总时间
delta_t = 0.1  # 每步时间增量

# 模拟运动
positions_front, positions_back, times = simulate_motion_with_fixed_start(a, b, theta_start, segment_length, speed, total_time, delta_t)

# 每2.86个单位时间绘制一次连接线
step_interval = int(2.86 / delta_t)  # 每2.86个单位时间对应的步数

# 生成螺线轨迹用于绘制
theta_values = np.linspace(0, theta_start, 1000)
r_values = archimedean_spiral(a, b, theta_values)
x_spiral = r_values * np.cos(theta_values)
y_spiral = r_values * np.sin(theta_values)

# 绘制模拟结果
plt.figure(figsize=(6, 6))

# 绘制螺线
plt.plot(x_spiral, y_spiral, label='Archimedean Spiral', color='blue')

# 遍历每2.86个单位时间，绘制前后两点并连接
for i in range(0, len(times), step_interval):
    # 连接前后两点
    plt.plot([positions_front[i, 0], positions_back[i, 0]], [positions_front[i, 1], positions_back[i, 1]], 'gray', lw=1)
    # 绘制前后两个点
    plt.plot(positions_front[i, 0], positions_front[i, 1], 'bo')
    plt.plot(positions_back[i, 0], positions_back[i, 1], 'ro')

plt.title('Motion of Two Points Along Archimedean Spiral (Connection Every 2.86 Units Time)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()