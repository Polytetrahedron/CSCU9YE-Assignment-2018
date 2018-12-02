__author__ = "Nikolaos Kouroumalos, Mark Green"
import random
import math
import time
import drawColours
import Calculations
import Permutations
import Visualize
import ColourList


def generate_initial_population(size_of_population, size_of_individual):
    """
    Generates a random population.
    :param size_of_population: The size of the population
    :param size_of_individual: The size of an individual inside the population
    :return: A randomly generated population
    """
    initial_population = []
    for i in range(size_of_population):
        initial_population.append(Permutations.random_permutation(size_of_individual))
    return initial_population


def evaluate_population_fitness(population):
    """
    Evaluates the fitness of the entire population and returns a population sorted by their fitness score
    (total summary of the distances between colours). Lowest values go first (lowest = better individual).
    :param population: The population to be evaluated
    :return: A sorted (by the individuals fitness score) population.
    """
    # A list that keeps the fitness score of all the individuals in a population
    fitness_list = []
    for i in range(len(population) - 1):
        fitness_list.append(Permutations.evaluate_permutation(population[i]))
    # Making a 2D list of the population and its fitness in order to be sorted afterwards
    population_fitness = [list(a) for a in zip(population, fitness_list)]
    # sorting the population_fitness list based on the fitness. Lowest value goes first.
    sorted_population_fitness = sorted(population_fitness, key=lambda l: l[1])
    # A new list that will hold only the population part (list) of the sorted_population_fitness 2D list
    sorted_population = []
    for i in range(len(sorted_population_fitness)):
        sorted_population.append(sorted_population_fitness[i][0])
    return sorted_population


def breed_population(population):
    """
    It creates the next generation of the population by keeping a percentage of the best performing ones (elite)
    and breeding good perfming (upper 50%) with bad perfoming (lower 50%)
    :param population:
    :return:
    """
    next_generation = []
    # Converting the elite_percentage to a number while rounding it up to the nearest integer
    elite_number = int(math.ceil((elite_percentage * len(population)) / 100))
    for i in range(elite_number):
        next_generation.append(population[i])  # The top performing individuals
    # Converting the diversity_percentage to a number while rounding it up to the nearest integer
    diversity_number = int(math.ceil((diversity_percentage * len(population)) / 100))
    for i in range(diversity_number):
        parent_a = population[random.randint(0, (len(population) - 1) / 2)]
        parent_b = population[random.randint((len(population) - 1) / 2, len(population) - 1)]
        next_generation.append(one_point_crossover(parent_a, parent_b))
        # next_generation.append(ox_crossover(parent_a, parent_b))
    return next_generation


def ox_crossover(parent_a, parent_b):
    """
    An implementation of the OX1 crossover where a random part of parent_a is copied as is in the exact same indexes to
    the offspring and the remaining empty spots are filled from parent_b.
    :param parent_a: The first parent
    :param parent_b: The second parent
    :return: An offspring
    """
    # Getting 2 random points using a parent. Which parent doesn't matter as all have the same size
    rand_start, rand_end = random_start_end(parent_a)
    offspring = []
    # Creating a list the size of a parent
    for i in range(len(parent_a)):
        offspring.append(-1)
    # Copying the starting and ending point of parent_a to the same indexes in the offspring
    for i in range(rand_start, rand_end):
        offspring[i] = parent_a[i]
    # Copying from the end point to the end of paren_b while checking for duplicates
    for i in range(rand_end, len(parent_b)):
        if parent_b[i] in offspring:  # If a value already exists the skip to the next iteration
            continue
        offspring[i] = parent_b[i]
    # Copying from 0 to the start point while checking for duplicates
    for i in range(0, rand_start):
        if parent_b[i] in offspring:  # If a value already exists the skip to the next iteration
            continue
        offspring[i] = parent_b[i]

    # In case there are too many duplicates I'm filling the remaining spots (-1) with values from parent_a
    if -1 in offspring:
        for i in range(len(parent_a)):
            if parent_a[i] in offspring:
                continue
            offspring[offspring.index(-1)] = parent_a[i]
    return offspring


def one_point_crossover(parent_a, parent_b):
    """
    An implementation of one point crossover. The percentage of the crossover depends on the global variable named
    crossover and it starts with parent_a. For example 75% crossover means that 75% of the offspring will be
    from parent_a and 25% will be from parent_b.
    :param parent_a: The first parent
    :param parent_b: The second parent
    :return: An offspring
    """
    offspring = []
    crossover_number = int(math.ceil((crossover_percentage * len(parent_a)) / 100))
    # Fill in the first values based on the crossover number
    for i in range(crossover_number):
        offspring.append(parent_a[i])
    # Fill in the remaining values if possible (duplication is an issue)
    for i in range(len(parent_b)):
        if len(offspring) < len(parent_b):  # Making sure it stays within the correct size
            if parent_b[i] in offspring:  # If a value already exists the skip to the next iteration
                continue
            offspring.append(parent_b[i])
    # If at the end the size of offspring doesn't match its parent (because of the duplicates)
    # we fill the remaining spots with values from the first parent.
    if len(offspring) < len(parent_a):
        for i in range(len(parent_a)):
            if len(offspring) < len(parent_a):  # Making sure it stays within the correct size
                if parent_a[i] in offspring:  # If a value already exists the skip to the next iteration
                    continue
                offspring.append(parent_a[i])
    return offspring


def mutate_population(population):
    """
    Mutates individuals from the provided population using three different mutations. Scramble mutation,
    inversion mutation and swap_mutation. Which mutation will be used is chosen randomly.
    The percentage of the population to be mutated depends on the global variable named mutation.
    :param population: The population to be mutated
    :return: A mutated population
    """
    next_generation = population.copy()
    mutation_number = int(math.ceil((mutation_percentage * len(next_generation)) / 100))
    for i in range(mutation_number):
        # Get the position of a random individual to be mutated
        rand_individual_pos = next_generation.index(next_generation[random.randint(0, len(next_generation) - 1)])
        rand_mutation = random.randint(0, 2)
        rand_individual = []
        if rand_mutation == 0:
            rand_individual = scramble_mutation(next_generation[rand_individual_pos])
        elif rand_mutation == 1:
            rand_individual = inversion_mutation(next_generation[rand_individual_pos])
        elif rand_mutation == 2:
            rand_individual = swap_mutation(next_generation[rand_individual_pos])
        next_generation[rand_individual_pos] = rand_individual
    return next_generation


def scramble_mutation(individual):
    """
    A random subset of genes from the individual are being randomly shuffled. It is possible to shuffle the entire
    individual.
    :param individual: The individual to have their genomes shuffled
    :return: An individual with part of their genes shuffled
    """
    rand_start, rand_end = random_start_end(individual)
    # The part that will be shuffled
    sublist = individual[rand_start:rand_end]
    random.shuffle(sublist)
    individual[rand_start:rand_end] = sublist
    return individual


def inversion_mutation(individual):
    """
    A random subset of genes from the individual will be reversed. It is possible to reverse the entire individual.
    :param individual: The individual to have their genomes reversed
    :return: An individual with part of their genes reversed
    """
    rand_start, rand_end = random_start_end(individual)
    # The part that will be reversed
    sublist = individual[rand_start:rand_end]
    individual[rand_start:rand_end] = reversed(sublist)
    return individual


def swap_mutation(individual):
    """
    Two random genes from the individual will be swapped.
    :param individual: The individual to have two of their genes swapped
    :return: An individual with two of their genes swapped
    """
    rand_start, rand_end = random_start_end(individual)
    # The genes swap
    value_a = individual[rand_start]
    value_b = individual[rand_end]
    individual[rand_start] = value_b
    individual[rand_end] = value_a
    return individual


def random_start_end(individual):
    """
    Creates a random starting and ending point based on an individuals size and it's used in mutation functions.
    The starting and ending point will never be the same, however the two extremes are allowed (0 and max size)
    :param individual: The individual to be used in order to decide on the random points
    :return: The starting and ending point to be used by the mutation.
    """
    rand_start = random.randint(0, len(individual) / 2)
    rand_end = random.randint(len(individual) / 2, len(individual) - 1)
    # In order to avoid having the same starting and ending point which would result in no shuffling at all.
    while rand_end == rand_start:
        rand_end = random.randint(len(individual) / 2, len(individual) - 1)
    return rand_start, rand_end


def start_genetic_algorithm(generations, size_of_population, size_of_individual):
    """
    Starts a run of the genetic algorithm.
    :param generations: The number of generations the GA should run for
    :param size_of_population: The size of the population per generation
    :param size_of_individual: The size of an individual in the population (The colour size)
    :return: The best individual of the entire run
    """
    # For benchmarking the runtime of the algorithm
    t1 = time.time()
    population = generate_initial_population(size_of_population, size_of_individual)
    evaluated_population = evaluate_population_fitness(population)
    best_performing_individuals = []  # Used to create a plot for a single run of the GA
    for i in range(generations):
        # Get a new generation after breeding
        new_generation = breed_population(evaluated_population)
        # Mutate the new generation
        new_mutated_generation = mutate_population(new_generation)
        # Evaluate the new generation
        evaluated_population = evaluate_population_fitness(new_mutated_generation)
        # Store the best performing individual for plotting.
        best_performing_individuals.append(Permutations.evaluate_permutation(evaluated_population[0]))
        print("Generation: ", i)
    # For benchmarking the runtime of the algorithm
    t2 = time.time()
    print('Time elapsed: ', (t2 - t1))  # Prints the total time the algorithm was running

    # ---------- In case we want to visualize each single run of the GA ----------
    #Visualize.plot(best_performing_individuals, 'Number of Generations')
    #test_colours = colours_list[0:size_of_individual]
    #drawColours.plot_colours(test_colours, evaluated_population[0])
    # ----------------------------------------------------------------------------

    # At the end the best individual of a population will be at the top of the list
    return evaluated_population[0]


# The percentage of the elite population during breeding
elite_percentage = 10
# The percentage of the diverse population during breeding
diversity_percentage = 90
# The percentage of the crossover when breeding two parents (if 100 then no breeding will occur)
crossover_percentage = 100
# The percentage of the population that will be mutated
mutation_percentage = 50

colours_list = ColourList.get_colours_list()


def run(iterations, number_of_generations, size_of_population, size_of_individual):
    """
    Runs multiple iterations of the genetic algorithm. Keeps track of the best solution, plots the result and
    reports the objective function of it. Also reports the mean, median and standard deviation of all the solutions.
    :param iterations: The number of iterations we should run the genetic algorithm for
    :param number_of_generations: The number of generations the GA should run for
    :param size_of_population: The size of the population per generation
    :param size_of_individual: The size of an individual in the population (The colour size)
    """
    all_solutions = []  # Stores all the best individuals returned by the genetic algorithm
    best_objective_function_value = 0
    best_solution = []  # Stores the best solution (permutation) out of all iterations
    t1 = time.time()
    for i in range(iterations):
        best_individual = start_genetic_algorithm(number_of_generations, size_of_population, size_of_individual)
        all_solutions.append(Permutations.evaluate_permutation(best_individual))

        if len(all_solutions) == 1:
            best_objective_function_value = all_solutions[i]
            best_solution = best_individual
        # Keeping track of the best solution out of all iterations
        if best_objective_function_value > all_solutions[i]:
            best_objective_function_value = all_solutions[i]
            best_solution = best_individual

    t2 = time.time()
    print("Total runtime: ", (t2 - t1))
    if iterations > 2:  # Need more than 2 runs in order to properly calculate the mean/median/standard deviation
        print("Mean: ", Calculations.get_mean(all_solutions), " Median: ", Calculations.get_median(all_solutions),
              " Standard Deviation: ", Calculations.get_standard_deviation(all_solutions))
    print("Objective function value: ", best_objective_function_value)
    test_colours = colours_list[0:size_of_individual]
    drawColours.plot_colours(test_colours, best_solution)


run(1, 100, 100, 100)  # iterations, number_of_generations, size_of_population, size_of_individual
# start_genetic_algorithm(1000, 100, 100)  # number_of_generations, size_of_population, size_of_individual
