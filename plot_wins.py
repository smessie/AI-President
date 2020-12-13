import matplotlib.pyplot as plt
import numpy as np


def plot(file):
    try:
        plt.style.use('ggplot')

        data = np.loadtxt(f"{file}.csv", delimiter=',', skiprows=0)

        fig, ax = plt.subplots(figsize=(16, 9))

        x = data[:, 0]
        for i in range(1, data.shape[1]):
            ax.plot(x, data[:, i], label=f"Times {i} th place")

        ax.legend()

        plt.savefig(f"{file}.png", bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(e)


filename = 'data/saves/%s/results/%s'    # without extension

#for i in range(17):
#    plot(filename % (i, 'wins-0'))
#    plot(filename % (i, 'wins-benchmark'))
#
#plot(filename % (17, 'wins-0'))
#plot(filename % (17, 'wins-1'))
#plot(filename % (17, 'wins-benchmark-0'))
#plot(filename % (17, 'wins-benchmark-1'))

for i in range(18, 29):
    plot(filename % (i, 'wins-0'))
    plot(filename % (i, 'wins-benchmark'))
