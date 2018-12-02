__author__ = "Nikolaos Kouroumalos, Mark Green"
import matplotlib.pyplot as plt


def plot(best_solutions, x_label_name):
    """
    Creates a plot based on the best_solutions list.
    :param best_solutions: The list to create a plot from
    :param x_label_name: The name of the x label
    """
    plt.plot(best_solutions)
    plt.ylabel('Total Sum')
    plt.xlabel(x_label_name)
    plt.grid(True)
    plt.show(block=False)
    plt.pause(0.0000001)
