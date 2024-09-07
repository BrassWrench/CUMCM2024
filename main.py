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

    problem4_3 = Problem4_3()
    # problem4_3.save_t_state(13, "problem4/savefig")
    #problem4_3.save_result()

    v1, v2, v3 = [], [], []
    t = np.arange(10, 20 + 0.01, 0.01)
    for t_now in tqdm(t, desc="第五问时间戳计算"):
        xi0_t = problem4_3.t_to_xi0(t_now)
        v0_t = 1
        xi1_t, v1_t = problem4_3.next_state(xi0_t, v0_t, is_head=True)
        xi2_t, v2_t = problem4_3.next_state(xi1_t, v1_t, is_head=False)
        xi3_t, v3_t = problem4_3.next_state(xi2_t, v2_t, is_head=False)
        v1.append(v1_t)
        v2.append(v2_t)
        v3.append(v3_t)

    plt.plot(t, v1, label="v1")
    plt.plot(t, v2, label="v2")
    plt.plot(t, v3, label="v3")
    plt.legend()
    plt.grid()
    plt.savefig("v.pdf")



