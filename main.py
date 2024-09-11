import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from problem1.problem1 import Problem1
from problem2.problem2 import Problem2
from problem3.problem3 import Problem3
from problem4.problem4_1 import Problem4_1
from problem4.problem4_2 import Problem4_2
from problem4.problem4_3 import Problem4_3
from problem5.problem5 import Problem5

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

if __name__ == '__main__':

    print("问题1".center(50, '-'))
    problem1 = Problem1()
    problem1.save_t_fig(300, "problem1/savefig")
    problem1.save_result()

    print("问题2".center(50, '-'))
    problem2 = Problem2()
    problem2.calc_collision_state()
    problem2.save_collision_fig("problem2/savefig")
    problem2.save_result()

    print("问题3".center(50, '-'))
    problem3 = Problem3()
    problem3.calc_collision_states(0.41, 0.55, 0.001, savefig=False)
    problem3.save_pitch_fig("problem3/savefig")
    print(problem3.pitch_critical)
    print(problem3.collision_radius_critical)

    print("问题4".center(50, '-'))
    problem4_1 = Problem4_1()

    problem4_2 = Problem4_2()
    problem4_2.save_curve("problem4/savefig")
    problem4_2.save_r_xi("problem4/savefig")

    problem4_3 = Problem4_3()
    problem4_3.save_t_state(100, "problem4/savefig")
    problem4_3.save_result()

    print("问题5".center(50, '-'))
    problem5 = Problem5()
    problem5.calc_v_t(8, 18, 0.01)
    problem5.calc_vmax_t()
    problem5.save_v_and_vmax_t_fig("problem5/savefig")
    print("最大速度：" + str(np.max(problem5.vmax_t)))
    print("最大速度出现的时间" + str((10 + np.argmax(problem5.vmax_t) * 0.01)))

