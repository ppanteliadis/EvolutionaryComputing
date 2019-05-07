from random import shuffle

permutation = []

def set_perm(size):
    # Set the random permutation for the randomly linked fitness functions
    global permutation
    permutation = list(range(size))
    shuffle(permutation)

def counting(creature):
    # The Counting Ones Function
    return creature.count()

def deceptive_tight(creature):
    # The Deceptive Trap Function (Tightly Linked)
    fitness = 0
    for i in range(0, creature.length(), 4):
        ones = creature[i : i + 4].count()
        if ones == 4:
            fitness += 4
        else:
            fitness += 3 - ones
    return fitness

def non_deceptive_tight(creature):
    # The Non-Deceptive Trap Function (Tightly Linked)
    fitness = 0
    for i in range(0, creature.length(), 4):
        ones = creature[i : i + 4].count()
        if ones == 4:
            fitness += 4
        else:
            fitness += (3 - ones) / 2
    return fitness

def deceptive_random(creature):
    # The Deceptive Trap Function (Randomly Linked)
    fitness = 0
    for i in range(0, len(permutation), 4):
        ones = 0
        for index in permutation[i : i + 4]:
            if(creature[index]):
                ones += 1
        if ones == 4:
            fitness += 4
        else:
            fitness += 3 - ones
    return fitness

def non_deceptive_random(creature):
    # The Non-Deceptive Trap Function (Randomly Linked)
    fitness = 0
    for i in range(0, len(permutation), 4):
        ones = 0
        for index in permutation[i : i + 4]:
            if(creature[index]):
                ones += 1
        if ones == 4:
            fitness += 4
        else:
            fitness += (3 - ones) / 2
    return fitness


def get_all():
    # Return a list of all fitness functions and their names to iterate over
    return [(counting, "Counting"), (deceptive_tight, "Deceptive Tight"), (non_deceptive_tight, "Non-Deceptive Tight"),
            (deceptive_random, "Deceptive Random"), (non_deceptive_random, "Non-Deceptive Random")]
    