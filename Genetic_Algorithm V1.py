import random


class Chromosome():
    def __init__(self, chromosome, population_size=None, valid_genes='10', target=None):
        self.chromosome = chromosome
        self.target = target
        self.valid_genes = valid_genes
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        # # TYPE1
        # return self.chromosome.count('1')

        # TYPE2
        fitness = 0
        for gs, gt in zip(self.chromosome, self.target):
            if gs != gt:
                fitness += 1
        return fitness

    def mate(self, par2):
        '''
        Perform mating and produce new offspring
        '''

        # chromosome for offspring
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):

            # random probability
            prob = random.random()

            # if prob is less than 0.45, insert gene
            # from parent 1
            if prob < 0.45:
                child_chromosome.append(gp1)

            # if prob is between 0.45 and 0.90, insert
            # gene from parent 2
            elif prob < 0.90:
                child_chromosome.append(gp2)

            # otherwise insert random gene(mutate),
            # for maintaining diversity
            else:
                child_chromosome.append(self.mutated_genes())

        # create new Individual(offspring) using
        # generated chromosome for offspring
        return Chromosome(child_chromosome)

    def mutated_genes(self):
        '''
        create random genes for mutation
        '''
        gene = random.choice(self.valid_genes)
        return gene


class GeneticAlgorithm():

    '''
    This class will represent the working of genetic algorithm 
    '''

    def __init__(self, valid_genes, target, population_size=10):
        self.population_size = population_size
        self.target = target
        self.current_generation = 1
        self.valid_genes = valid_genes
        self.population = []
        self.startProcess()

    def startProcess(self):
        # step1: Initialize Population
        self.initialPopulation()
        print('*** Population is initialized with size', len(self.population))

        # step2: until stoppping criteria doesn't matched keep searching
        while not self.stoppingCriteria():
            print('In step 2')

            # sort the population in increasing order of fitness score
            self.population = sorted(
                self.population, key=lambda x: x.fitness, reverse=True)

            if self.stoppingCriteria():
                break
            else:
                # Otherwise generate new offsprings for new generation

                # first by elitism
                new_generation = []
                new_generation.extend(self.selection())

                # then by mutation
                new_generation.extend(self.mutation())
                self.population = new_generation
                self.current_generation += 1

                print("Generation: {} String: {} Fitness: {}".
                      format(self.current_generation,
                             "".join(self.population[0].chromosome),
                             self.population[0].fitness))
                # input('Press to continue....')
                # if self.current_generation > 500:
                #     break
        print("Generation: {} String: {} Fitness: {}".
              format(self.current_generation,
                     "".join(self.population[0].chromosome),
                     self.population[0].fitness))

    def createChromosome(self):

        return random.choices('10', weights=None,
                              cum_weights=None, k=len(self.target))

    def initialPopulation(self):
        for i in range(self.population_size):
            self.population.append(Chromosome(
                chromosome=self.createChromosome(), target=self.target))

    def selection(self):
        # Elitism, that mean 15 % of fittest population
        # goes to the next generation without any change
        s = int((10*self.population_size)/100)
        return self.population[:s]

    def crossOver(self):
        pass

    def mutation(self):
        # From 50% of fittest population, Individuals
        # will mate to produce offspring
        s = int((90*self.population_size)/100)
        new_generation = []
        for _ in range(s):
            parent1 = random.choice(self.population[:50])
            parent2 = random.choice(self.population[:50])

            child = parent1.mate(parent2)

            new_generation.append(child)

        # print('Old generation:', self.population[0].chromosome)
        # print('New generation:', new_generation[0].chromosome)
        # print('Fitnesses:')
        # for fitness in self.population:
        #     print(fitness.fitness)

        return new_generation

    def stoppingCriteria(self):
        # if the chromosome have high fitness score (100 in this case) Then problem solved
        if self.population[0].fitness >= 100:
            return True

        return False


POP_SIZE = 10
valid_genes = '10'
TARGET = '1' * 100


GeneticAlgorithm(population_size=POP_SIZE,
                 valid_genes=valid_genes, target=TARGET)
