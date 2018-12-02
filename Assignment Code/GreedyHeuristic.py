__author__ = "Nikolaos Kouroumalos, Mark Green"
import random as ran
import Calculations
import Permutations
import ColourList
import drawColours
import time as timer

colour_list = ColourList.get_colours_list()


def initial_colour():
    """Each algorithm will approach this problem differently 
    This function returns a random index from the original 1000 colour list

    :return: The random number from the colour list
    """
    return ran.randint(0, len(colour_list) - 1)


def initial_colour_relative(problem_size: int):
    """
    This function generates a random number between 0 and the problem size

    :param problem_size: The size of the problem
    :return: The random number
    """
    return ran.randint(0, problem_size)


def greedy_search(start_index: int, problem_size: int):
    """
    This function performs a greedy search of a list of colours.
    It begins with a random colour and builds a list of colours,
    using the closest points to each colour it identifies

    :param start_index: The random index to begin the search
    :param problem_size: The number of colours to group
    :return: returns an ordered list of colours
    """
    ordered_colours = []
    value_list = []
    ordered_colours.append(start_index)
    time_start = timer.time()
    for i in range(problem_size - 1):
        current_colour = ordered_colours[i]
        best_distance = 1000  # impossibly high starting distance to allow the function to reset it
        best_colour = 0
        for j in range(len(colour_list) - 1):
            colour_a = colour_list[current_colour]
            if j != current_colour and ordered_colours.__contains__(j) is False:
                colour_b = colour_list[j]
            else:
                continue
            distance_new = Calculations.get_euclidean_distance(colour_a, colour_b)
            if distance_new < best_distance:
                best_colour = j
                best_distance = distance_new
                value_list.append(distance_new)
        ordered_colours.append(best_colour)
    time_finish = timer.time()
    time_elapsed = time_finish - time_start
    print("Time elapsed for problem size " + str(problem_size) + ": " + str(time_elapsed))
    print("Objective Value: " + str(Permutations.evaluate_permutation(ordered_colours)))
    return ordered_colours, value_list


def run(problem_size: int):
    test_size = problem_size  # Size of the subset of colours for testing
    test_colours = colour_list[0:test_size]  # list of colours for testing
    test, values = greedy_search(initial_colour(), test_size)
    drawColours.plot_colours(test_colours, test)


run(100)

# hc_values = hc.multi_start_hc(30, test_size)
# results = [values, hc_values]
# plt.figure()
# plt.boxplot(results,labels=["Greedy Search", "Multi-Start"], showfliers=False)
# plt.show()
# drawColours.plot_colours(test_colours, test)/
