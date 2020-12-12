import matplotlib.pyplot as plt
import numpy as np


def plot(file):
    try:
        plt.style.use('ggplot')
        data = np.loadtxt(f"{file}.csv", delimiter=',', skiprows=0)
        fig, ax = plt.subplots(figsize=(16, 9))

        x = np.arange(data.shape[0])
        ax.plot(x, data[:, 0], label=f"Loss")
        ax.legend()

        plt.savefig(f"{file}.png", bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(e)


filename = 'data/saves/%s/results/%s'    # without extension

#for i in range(17):
#    plot(filename % (i, 'training_loss'))
#
#plot(filename % (17, 'training_loss-0'))
#plot(filename % (17, 'training_loss-1'))

for i in range(18, 28):
    plot(filename % (i, 'training_loss'))
