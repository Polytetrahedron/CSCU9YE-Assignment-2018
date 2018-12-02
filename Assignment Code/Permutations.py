__author__ = "Nikolaos Kouroumalos, Mark Green"
import random
import Calculations
import ColourList

colours_list = ColourList.get_colours_list()


def random_permutation(size):
    """
    Returns a random permutation based on the provided size.
    :param size: The size of the permutation
    :return: A random permutation
    """
    return random.sample(range(size), size)


def evaluate_permutation(permutation):
    """
    Returns the distances between all pairs of the provided permutation using
    the euclidean distance
    :param permutation: The permutation
    :return: The sum all of the distances
    """
    total_sum = 0
    for i in range(len(permutation) - 1):
        colour_a = colours_list[permutation[i]]
        colour_b = colours_list[permutation[i+1]]
        distance = Calculations.get_euclidean_distance(colour_a, colour_b)
        total_sum += distance

    return total_sum
