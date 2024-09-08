import matplotlib as mpl
import matplotlib.pyplot as plt
from tqdm import tqdm
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

    # problem1 = Problem1()
    # problem1.save_t_fig(300, "problem1/savefig")
    #
    # problem2 = Problem2()
    # problem2.calc_collision_state()
    # problem2.save_collision_fig("problem2/savefig")
    # problem2.save_result()

    problem3 = Problem3()
    problem3.calc_collision_states(0.41, 0.55, 0.001, savefig=False)
    problem3.save_pitch_fig("problem3/savefig")

    #problem4_2 = Problem4_2()
    # problem4_2.save_curve("problem4/savefig")
    # problem4_2.save_r_xi("problem4/savefig")

    # problem4_3 = Problem4_3()
    # problem4_3.save_t_state(13, "problem4/savefig")
    # problem4_3.save_result()

    # problem4_3 = Problem4_3()
    # v = []
    # t = np.arange(10, 20, 0.1)
    # for t_now in tqdm(t, desc="第五问时间戳计算"):
    #     x_n, y_n, v_n = problem4_3.get_t_state(t_now)
    #     v.append(v_n)
    #
    # v = np.array(v)
    # v = v.T
    # for v_t in v:
    #     plt.plot(t, v_t, color="black")
    #
    # plt.grid()
    # plt.savefig("v.pdf")



