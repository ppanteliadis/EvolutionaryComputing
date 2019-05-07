import time
from bitarray import bitarray
from random import randint, shuffle

def random_creature(length):
    # Create a creature of a certain length, filled with random bits
    creature = bitarray(length)
    for i in range(length):
        creature[i] = randint(0, 1)
    return creature

def execute(fitness, crossover, size, length):
    # Run the 25 experiments
    start_time = time.time()
    avg_generations = 0
    successes = 0
    for _ in range(25):
        # Create a random starting population and start the experiment
        population = []
        for _ in range(size):
            creature = random_creature(length)
            population.append((creature, fitness(creature)))
        success, generations = loop(fitness, crossover, population, length)
        avg_generations += generations
        if success:
            successes += 1
    avg_generations /= 25
    # In every generation, all children get evaluated, so the amount of evaluations is the amount of generations times the population size
    avg_evaluations = avg_generations * size
    avg_time = (time.time() - start_time) / 25
    return successes, avg_generations, avg_evaluations, avg_time

def loop(fitness, crossover, population, length):
    # We use the history dictionary as a hash table to record all the creatures that have occured in the history of this experiment
    history = {}
    for creature in population:
        history[creature[0].tobytes()] = True
    
    # Run generations until there are no new creatures or the maximum fitness is reached
    new = True
    max_fitness = max(population, key = lambda c: c[1])[1]
    generations = 0
    while new and max_fitness != length:
        shuffle(population)
        new = False
        # For every pair of parents
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1]
            # Do crossover
            c1, c2 = crossover(parent1[0], parent2[0])
            # Calculate the childrens' fitness
            child1 = (c1, fitness(c1))
            child2 = (c2, fitness(c2))
            # Select the members of the family with the highest fitness, preferring children
            family = sorted([child1, child2, parent1, parent2], key = lambda c: c[1], reverse = True)
            population[i] = family[0]
            population[i + 1] = family[1]
            # If there is a new creature, record it and make sure a next generation will be run
            if family[0][0].tobytes() not in history:
                history[family[0][0].tobytes()] = True
                new = True
            if family[1][0].tobytes() not in history:
                history[family[1][0].tobytes()] = True
                new = True
        max_fitness = max(population, key = lambda c: c[1])[1]
        generations += 1
    return max_fitness == length, generations

# Special version of the execute function for the single experiment to avoid overhead
def execute_single(fitness, crossover, size, length):
    # Create a random starting population and start the experiment
    population = []
    for _ in range(size):
        creature = random_creature(length)
        population.append((creature, fitness(creature)))
    return loop_single(fitness, crossover, population, length)

# Special version of the loop function for the single experiment to avoid overhead
def loop_single(fitness, crossover, population, length):
    data = []
    proportion, mean, deviation = get_data(population, length)
    data.append((proportion, mean, deviation, 0))
    
    # We use the history dictionary as a hash table to record all the creatures that have occured in the history of this experiment
    history = {}
    for creature in population:
        history[creature[0].tobytes()] = True
    
    # Run generations until there are no new creatures or the maximum fitness is reached
    new = True
    max_fitness = max(population, key = lambda c: c[1])[1]
    while new and max_fitness != length:
        shuffle(population)
        total_error = 0
        new = False
        # For every pair of parents
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1]
            # Do crossover
            c1, c2 = crossover(parent1[0], parent2[0])
            # Calculate the childrens' fitness
            child1 = (c1, fitness(c1))
            child2 = (c2, fitness(c2))
            # Select the members of the family with the highest fitness, preferring children
            family = sorted([child1, child2, parent1, parent2], key = lambda c: c[1], reverse = True)
            population[i] = family[0]
            population[i + 1] = family[1]
            # If there is a new creature, record it and make sure a next generation will be run
            if family[0][0].tobytes() not in history:
                history[family[0][0].tobytes()] = True
                new = True
            if family[1][0].tobytes() not in history:
                history[family[1][0].tobytes()] = True
                new = True
            
            total_error += selection_error(parent1[0], parent2[0], family[0][0], family[1][0])
        max_fitness = max(population, key = lambda c: c[1])[1]
        
        proportion, mean, deviation = get_data(population, length)
        data.append((proportion, mean, deviation, total_error))
    return data

def get_data(population, length):
    # Calulcate the proportion of ones and the mean and standard deviation of the fitness
    total = 0
    for creature in population:
        total += creature[1]
    proportion = total / (len(population) * length)
    mean = total / len(population)
    sum_of_squares = 0
    for creature in population:
        sum_of_squares += (creature[1] - mean) ** 2
    deviation = (sum_of_squares / len(population)) ** 0.5
    return proportion, mean, deviation

def selection_error(parent1, parent2, winner1, winner2):
    # Use bitwise operators to find all selection errors, parents have to be different and the winners both 0:
    # (parent1 XOR parent2) AND (winner1 NOR winner2)
    return ((parent1 ^ parent2) & ~(winner1 | winner2)).count()
