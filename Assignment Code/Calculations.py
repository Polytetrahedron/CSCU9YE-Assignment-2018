__author__ = "Nikolaos Kouroumalos, Mark Green"
import math


def get_euclidean_distance(colour_a, colour_b):
    """
    Returns the euclidean distance between two colours.
    :param colour_a: The first colour
    :param colour_b: The second colour
    :return: The euclidean distance between two colours.
    """
    return math.sqrt((colour_b[0] - colour_a[0])**2 + (colour_b[1] - colour_a[1])**2 + (colour_b[2] - colour_a[2])**2)


def get_mean(lst):
    """
    Calculates the mean of a list. Tested for correctness using test samples
    and cross referencing the results with online calculators.
    :param lst: The list to have its mean calculated
    :return: The mean
    """
    mean = 0
    for i in range(len(lst)):
        mean += lst[i]
    mean = mean / len(lst)
    return mean


def get_median(lst):
    """
    Calculates the median of a list. Tested for correctness using test samples
    and cross referencing the results with online calculators.
    :param lst: The list to have its median calculated
    :return: The median
    """
    lst.sort()
    size_of_list = len(lst)
    if size_of_list % 2 == 1:
        return lst[size_of_list // 2]
    else:
        value_a = lst[size_of_list // 2 - 1]
        value_b = lst[size_of_list // 2 + 1]
        mean_values = [value_a, value_b]
        return get_mean(mean_values)


def get_standard_deviation(lst):
    """
    Calculates the standard deviation of a list. Tested for correctness using test samples
    and cross referencing the results with online calculators.
    :param lst: The list to have its standard deviation calculated
    :return: The standard deviation
    """
    mean = get_mean(lst)
    total_of_squared_values = 0
    for i in range(len(lst)):
        subtracted_value = lst[i] - mean
        total_of_squared_values += subtracted_value ** 2
    variance = total_of_squared_values / (len(lst) - 1)
    return math.sqrt(variance)
