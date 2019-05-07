from bitarray import bitarray
from random import randint

def two_point(parent1, parent2):
    # The 2-Point Crossover Function
    child1 = bitarray(parent1)
    child2 = bitarray(parent2)
    cross1 = randint(0, child1.length() - 1)
    cross2 = randint(1, child1.length() - 1)
    if cross2 <= cross1:
        cross1, cross2 = cross2 - 1, cross1
    for i in range(cross1, cross2):
        child1[i], child2[i] = child2[i], child1[i]
    return child1, child2

def uniform(parent1, parent2):
    # The Uniform Crossover Function
    child1 = bitarray(parent1)
    child2 = bitarray(parent2)
    for i in range(child1.length()):
        if randint(0, 1):
            child1[i], child2[i] = child2[i], child1[i]
    return child1, child2

def get_all():
    # Return a list of all crossover functions and their names to iterate over
    return [(two_point, "2-Point"), (uniform, "Uniform")]
