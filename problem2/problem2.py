import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import problem1 as p1

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.format'] = 'svg'
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern']
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

# 创建一个图形和一个坐标轴
fig, ax = plt.subplots()

# 创建一个矩形对象
# Rectangle(xy, width, height, **kwargs)
rect = patches.Rectangle((1, 1), 4, 2, linewidth=1, edgecolor='r', facecolor='none')

# 将矩形添加到坐标轴
ax.add_patch(rect)


