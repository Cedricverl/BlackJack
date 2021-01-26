from game import playround
from math import sqrt
import numpy as np


if __name__ == "__main__":

    bankrollist = []
    for i in range(1000):
        bankroll = 100
        for k in range(100):
            bankroll = playround()

        bankrollist.append(bankroll)
    print("after 1000 sets of 100 games you ended op on avg with", np.mean(bankrollist), "euro")
    print("with stdev of", sqrt(np.var(bankrollist)))
