__author__ = "Nikolaos Kouroumalos, Mark Green"
import drawColours
import numpy as np


def get_colours_list():
    """
    Returns the list of colours present in the colours.txt. Possibly not the best solution but if there is the need
    to change the colours.txt to a different .txt the change will need to take place only in this module, instead
    of all modules that make use of the list.
    :return: A list of colours
    """
    n_colours, colours_list = drawColours.read_file('colours.txt')
    colours_list = list(np.float_(colours_list))  # Changing the colours_list from strings to floats
    return colours_list
