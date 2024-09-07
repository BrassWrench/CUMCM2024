import matplotlib as mpl
import matplotlib.pyplot as plt
from problem1 import problem1

mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "xelatex",
    "pgf.rcfonts": True,
    "pgf.preamble": r"\usepackage{amsmath}"
}
mpl.rcParams.update(pgf_with_pdflatex)
plt.rcParams['font.family'] = 'serif'

if __name__ == '__main__':

    #problem1.save_t_fig(300)
    problem1.save_xlsx()