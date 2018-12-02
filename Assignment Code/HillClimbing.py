__author__ = "Nikolaos Kouroumalos, Mark Green"
import random
import time
import drawColours
import Permutations
import Visualize
import ColourList
import Calculations

colours_list = ColourList.get_colours_list()


def random_neighbour(permutation):
    """
    Returns a random neighbour permutation using the inverse operation.
    :param permutation: The original permutation
    :return: A neighbour of the original permutation
    """
    # Making a copy of the permutation list in order to avoid changing the original list
    new_permutation = permutation.copy()
    has_operation_finished = False
    # Initial random positions of the indices
    indice_a = random.randint(0, len(permutation) - 1)
    indice_b = random.randint(0, len(permutation) - 1)

    # In case the first time both have the same position in the permutation list
    while indice_a == indice_b:
        indice_b = random.randint(0, len(permutation) - 1)

    # Inverse Operator
    while not has_operation_finished:
        # The values are swapped
        value_a = permutation[indice_a]
        value_b = permutation[indice_b]
        new_permutation[indice_a] = value_b
        new_permutation[indice_b] = value_a
        # Changes the indices based on their position and terminates the loop if they are either in the same position
        # or if they swapped positions
        if indice_a < indice_b:
            indice_a += 1
            indice_b -= 1
            if indice_a >= indice_b:
                has_operation_finished = True
                continue
        else:
            indice_b += 1
            indice_a -= 1
            if indice_a <= indice_b:
                has_operation_finished = True
                continue
    return new_permutation


def hill_climbing(starting_permutation):
    """
    A hill climbing function using a nearest neighbour with an inverse
    operator.
    :param starting_permutation: The starting permutation
    :return: The final (and best) permutation
    """
    # Used for benchmarking how long the algorithm will take in total
    t1 = time.time()
    final_permutation = starting_permutation
    # Keeps a record of the total sum of all better solutions. It's used for plotting.
    best_solutions = []
    for i in range(10000):
        total_sum = Permutations.evaluate_permutation(final_permutation)
        neighbour_permutation = random_neighbour(final_permutation)
        neighbour_total_sum = Permutations.evaluate_permutation(neighbour_permutation)
        # If the neighbour total sum is less that the current total sum then the neighbour solution is better
        if neighbour_total_sum < total_sum:
            final_permutation.clear()
            best_solutions.append(neighbour_total_sum)
            final_permutation = neighbour_permutation.copy()

            neighbour_permutation.clear()
        print('Iteration: ', i)
    # Used for benchmarking how long the algorithm will take in total
    t2 = time.time()
    print('Time elapsed: ', (t2 - t1))  # Prints the total time the algorithm was running
    return best_solutions, final_permutation


def single_run(problem_size):
    """
    A single run of the hill climbing algorithm producing a plot showing the progress each iteration as well as
    a plot of colours showing the final result.
    :param problem_size: The colour list size
    """
    test_colours = colours_list[0:problem_size]  # list of colours for testing
    best_solutions, best_permutation = hill_climbing(Permutations.random_permutation(problem_size))
    Visualize.plot(best_solutions, "Number of Better Solutions")
    drawColours.plot_colours(test_colours, best_permutation)


def multi_start_hc(iterations: int, problem_size: int):
    """
    This is a multistart version of the single hillclimbing algorithm.
    This function runs for a set number of iterations and finds the best hillclimbing
    solution

    :param iterations: The number of iterations the function will perform
    :param problem_size: The size of the problem domain
    :return: The best solution found, the best distance of that solution, the list of solutions it found
    """
    best_solution = []
    best_distance = 0
    value_list = []
    for i in range(iterations):
        bs, permutation = hill_climbing(Permutations.random_permutation(problem_size))
        new_distance = Permutations.evaluate_permutation(permutation)
        if new_distance < best_distance or i == 0:
            best_solution = permutation.copy()
            best_distance = new_distance
            value_list.append(new_distance)
    math_calc(value_list)
    print("Best objective function value: ", best_distance)
    test_colours = colours_list[0:problem_size]  # list of colours for testing
    drawColours.plot_colours(test_colours, best_solution)
    return value_list


def math_calc(values: list):
    print("Mean: ", Calculations.get_mean(values),
          " Median: ", Calculations.get_median(values),
          " Standard Deviation: ", Calculations.get_standard_deviation(values))


def run(iterations: int, problem_size: int):
    """
    Runs the hill climbing algorithm as many times as the iterations variable dictates. If only 1 iteration is send
    then a sing run will be performed and two plots will be produced. If more than 1 iteration is send then a multi hc
    run will start and will produce the plot of the best solution as well as report the mean, median and standard
    deviation
    :param iterations: The number of times the hill climbing algorithm should run
    :param problem_size: The colour list size
    """
    if iterations > 1:
        multi_start_hc(iterations, problem_size)
    else:
        single_run(problem_size)


run(5, 100)
