import time
from random import choice, random, randint
import sys

start_time = time.time()

initial_sudoku_table = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]

]

# Initialises the population
def StartPopulation(table, population_size):
    # return a list of all the tables in the population
    return [createIndivisual(table) for _ in range(population_size)]

# Creates a new individual
def createIndivisual(table):
    list_indivisual = []
    for row in range(len(initial_sudoku_table)):  # range(0,9)
        possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        list_indivisual.append(list(table[row]))
        for column in range(len(initial_sudoku_table)):
            if (list_indivisual[row][column] == 0):
                find_same_number = False
                # same number cannot be repeated in row and column
                while (find_same_number == False):
                    # if there is no same number, choose the possible number and collect it.
                    collect_avaliable_numbers = choice(possible_numbers)
                    # If the numbers collected are not included in the list
                    if (collect_avaliable_numbers not in list_indivisual[row]):
                        # add the number you collected to the appropriate place
                        list_indivisual[row][column] = collect_avaliable_numbers
                        # Subtract the number you added to list_indivitsual from possible numbers
                        possible_numbers.remove(collect_avaliable_numbers)
                        find_same_number = True
                    else:
                        possible_numbers.remove(collect_avaliable_numbers)
    return list_indivisual

# Calculates the fitness of the population
def calculateFitnessPopulation(population, generation = 0):
    # return a list of all the fitnesses of the population
    return [calculateFitness(fitness, generation) for fitness in population]

# Calculates the fitness of a table
def calculateFitness(table, generation):
    fitness = 0

    # Fitness for each row
    for row in range(9):
        list = []
        for column in range(9):
            list.append(table[column][row])
        for element in range(9):
            if (list[element] in list[element + 1:]) == False:
                fitness += 1

    # Fitness for 3*3 subsquares
    list = []
    for row in range(0, 3):
        for column in range(0, 3):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1
    list = []
    for row in range(3, 6):
        for column in range(0, 3):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1
    list = []
    for row in range(6, 9):
        for column in range(0, 3):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1
    list = []
    for row in range(0, 3):
        for column in range(3, 6):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1
    list = []
    for row in range(3, 6):
        for column in range(3, 6):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1
    list = []
    for row in range(6, 9):
        for column in range(3, 6):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1
    list = []
    for row in range(0, 3):
        for column in range(6, 9):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1
    list = []
    for row in range(3, 6):
        for column in range(6, 9):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1
    list = []
    for row in range(6, 9):
        for column in range(6, 9):
            list.append(table[row][column])
    for element in range(9):
        if (list[element] in list[element + 1:]) == False:
            fitness += 1


    result = fitness / 160
    # If the fitness result is 1.0, the result is found.
    if (result == 1.0):
        print()
        print("Solution ")
        printSudoku(table)
        print("Generations:", generation)
        print("Total time:  %s seconds" % (time.time() - start_time))
        sys.exit()

    return result

# Selects the parents for the next generation
def selectPopulation(population, fitness_population, populationSize):
    # zip() function is an iterator of tuples where the first item in each passed iterator is paired together, and the second work with the first iterator
    sortedPopulation = sorted(zip(population, fitness_population), key=lambda individual_fitness: individual_fitness[1])
    # Since the zip function was used, the population amount was halved.
    # return a list of all the parents
    return [individual for individual, fitness in sortedPopulation[int(populationSize / 2):]]



# Makes child using a uniform crossover
def crossoverPopulation(population, populationSize):
    # using a uniform crossover
    # return a list of all the newly made child
    return [crossoverIndividual_Parent(choice(population), choice(population)) for _ in range(populationSize)]

# Applies the crossover operator to make a new child
def crossoverIndividual_Parent(parent1, parent2):
    # return child
    return [list(choice(change_pair)) for change_pair in zip(parent1, parent2)]


# Mutates each child in the population
def mutatePopulation(population, table):
    # return the mutated population
    return [mutateIndividual(individual, table) for individual in population]

# Mutates a given table
def mutateIndividual(individual, table):

    for row in range(9):
        if (random() < 0.1):
            is_mutate = False
            while (is_mutate == False):
                random1 = randint(0, len(initial_sudoku_table)-1)
                random2 = randint(1, len(initial_sudoku_table)-1)
                if (table[row][random1] == 0 and table[row][random2] == 0):
                    # mutate
                    individual[row][random1], individual[row][random2] = individual[row][random2], individual[row][random1]
                    is_mutate = True
    #return the mutated grid
    return list(individual)

# print sudoku table on screen in grid format
def printSudoku(table):

    for row in range(9):
        if row in [3, 6]:
            print("--------------------------")
        for column in range(9):
            if column in [3, 6]:
                print(' | ', table[row][column], end=' ')
            else:
                print(table[row][column], end=' ')
        print(end='\n')

# Tries to find the solution to a sudoku by evolving it using genetic algorithm
def solve_sudoku_with_genetic_algorithm(table, populationSize):
    generation = 0
    minVal = 0
    population = StartPopulation(table, populationSize)
    fitnessPopulation = calculateFitnessPopulation(population)
    while (generation < 100000):
        generation += 1
        parentsPopulation = selectPopulation(population, fitnessPopulation, populationSize)
        CrossoverPoint = crossoverPopulation(parentsPopulation, populationSize)
        population = mutatePopulation(CrossoverPoint, table)
        finalFitness = sorted(fitnessPopulation)[-1]
        fitnessPopulation = calculateFitnessPopulation(population, generation)
        if (finalFitness == sorted(fitnessPopulation)[-1]):
            minVal += 1
            if minVal == 50:
                print("Population...")
                population = StartPopulation(table, populationSize)
                fitnessPopulation = calculateFitnessPopulation(population)
                minVal = 0
                generation = 0
        else:
            minVal = 0
        print("Generation:", generation, "| Best fitness %.5f" % sorted(fitnessPopulation)[-1])

def main():
    solve_sudoku_with_genetic_algorithm(initial_sudoku_table, 1000)
    print("Input grid:")
    printSudoku(initial_sudoku_table)

if __name__ == "__main__":
   main()