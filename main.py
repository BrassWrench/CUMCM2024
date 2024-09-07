import matplotlib as mpl
import matplotlib.pyplot as plt
from problem1.problem1 import Problem1
from problem2.problem2 import Problem2
import math

from problem2.problem2 import Problem2

mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "xelatex",
    "pgf.rcfonts": True,
    "pgf.preamble": r"\usepackage{amsmath}"
}
mpl.rcParams.update(pgf_with_pdflatex)
plt.rcParams['font.family'] = 'serif'

if __name__ == '__main__':

    # problem1 = Problem1(k = 0.55 / (2 * math.pi), d_body=2.2 - 2 * 0.275, d_head=3.41 - 2 * 0.275, v0=1, num=223, init_theta0=16 * 2 * math.pi)
    # problem1.save_t_fig(300, "problem1/savefig")

    problem2 = Problem2(k = 0.55 / (2 * math.pi), d_body=2.2 - 2 * 0.275, d_head=3.41 - 2 * 0.275, v0=1, num=223, init_theta0=16 * 2 * math.pi)
    theta0, rectangles, x, y, v = problem2.get_collision_state()
    problem2.save_collision_fig(rectangles, x, y, "problem2/savefig")
    problem2.save_result(x, y, v)
