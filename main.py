import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from problem1.problem1 import Problem1
from problem2.problem2 import Problem2
from problem3.problem3 import Problem3
from problem4.problem4_2 import Problem4_2
from problem4.problem4_3 import Problem4_3

mpl.use("pgf")
plt.rcParams.update({
    "pgf.texsystem": "xelatex",
    "font.family": "SimSun",
    "text.usetex": True,
    "pgf.rcfonts": False,
    "axes.unicode_minus": False,
    "pgf.preamble": "\n".join([
         r"\usepackage{amsmath}",
    ]),
})

# pgf_with_pdflatex = {
#     "pgf.texsystem": "xelatex",
#     "pgf.preamble": r"\usepackage{amsmath}"
# }
# mpl.rcParams.update(pgf_with_pdflatex)
# plt.rcParams['font.family'] = 'serif'

if __name__ == '__main__':

    # problem1 = Problem1(k = 0.55 / (2 * math.pi), d_body=2.2 - 2 * 0.275, d_head=3.41 - 2 * 0.275, v0=1, num=223, init_theta0=16 * 2 * np.pi)
    # problem1.save_t_fig(300, "problem1/savefig")

    # problem2 = Problem2(k = 0.55 / (2 * math.pi), d_body=2.2 - 2 * 0.275, d_head=3.41 - 2 * 0.275, v0=1, num=223, init_theta0=16 * 2 * np.pi)
    # problem2.calc_collision_state()
    # problem2.save_collision_fig("problem2/savefig")
    # problem2.save_result()

    #problem3 = Problem3(d_body=2.2 - 2 * 0.275, d_head=3.41 - 2 * 0.275, v0=1, num=223, init_theta0=16 * 2 * np.pi)
    #problem3.calc_collision_states(0.41, 0.55, 0.01, savefig=True)
    #problem3.save_pitch_fig("problem3/savefig")
    #print(problem3.calc_critical_pitch())

    #problem4_2 = Problem4_2()
    #problem4_2.save_curve("problem4/savefig")
    #problem4_2.save_r_xi("problem4/savefig")

    problem4_3 = Problem4_3(d_body=2.2 - 2 * 0.275, d_head=3.41 - 2 * 0.275, v0=1, num=223)
    problem4_3.save_t_state(13, "problem4/savefig")
    #problem4_3.save_result()

