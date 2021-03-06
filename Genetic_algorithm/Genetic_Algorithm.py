#need some python libraries
import copy
import math
from random import Random
import numpy as np


def GeneticAlgorithm(Generations, populationSize):
    
    #to setup a random number generator, we will specify a "seed" value
    seed = 5113
    myPRNG = Random(seed)
    
    lowerBound = -500  #bounds for Schwefel Function search space
    upperBound = 500   #bounds for Schwefel Function search space
    
    #you may change anything below this line that you wish too -----------------------------------------------------------------
    
    #Student name(s):
    #Date:
    
    dimensions = 200   #set dimensions for Schwefel Function search space (should either be 2 or 200 for HM #5)
    
    crossOverRate = 0.8  #currently not used in the implementation; neeeds to be used.
    mutationRate = 0.07   #currently not used in the implementation; neeeds to be used.
    
    
    #create an continuous valued chromosome
    def createChromosome(d, lBnd, uBnd):
        x = []
        for i in range(d):
            x.append(myPRNG.uniform(lBnd,uBnd))   #creating a randomly located solution
        
        return x
    
    #create initial population
    def initializePopulation(): #n is size of population; d is dimensions of chromosome
        population = []
        populationFitness = []
        
        for i in range(populationSize):
            population.append(createChromosome(dimensions,lowerBound, upperBound))
            populationFitness.append(evaluate(population[i]))
        
        tempZip = zip(population, populationFitness)
        popVals = sorted(tempZip, key=lambda tempZip: tempZip[1])
        
        #the return object is a sorted list of tuples:
        #the first element of the tuple is the chromosome; the second element is the fitness value
        #for example:  popVals[0] is represents the best individual in the population
        #popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
        
                return popVals

#implement a linear crossover
def crossover(x1,x2):
    
    d = len(x1) #dimensions of solution
        
        #choose crossover point
        
        #we will choose the smaller of the two [0:crossOverPt] and [crossOverPt:d] to be unchanged
        #the other portion be linear combo of the parents
        
        crossOverPt = myPRNG.randint(1,d-1) #notice I choose the crossover point so that at least 1 element of parent is copied
        
        beta = myPRNG.random()  #random number between 0 and 1
        
        #note: using numpy allows us to treat the lists as vectors
        #here we create the linear combination of the soltuions
        new1 = list(np.array(x1) - beta*(np.array(x1)-np.array(x2)))
        new2 = list(np.array(x2) + beta*(np.array(x1)-np.array(x2)))
        
        #the crossover is then performed between the original solutions "x1" and "x2" and the "new1" and "new2" solutions
        if crossOverPt<d/2:
            offspring1 = x1[0:crossOverPt] + new1[crossOverPt:d]  #note the "+" operator concatenates lists
            offspring2 = x2[0:crossOverPt] + new2[crossOverPt:d]
        else:
            offspring1 = new1[0:crossOverPt] + x1[crossOverPt:d]
            offspring2 = new2[0:crossOverPt] + x2[crossOverPt:d]
        
        return offspring1, offspring2  #two offspring are returned

    #function to evaluate the Schwefel Function for d dimensions
    def evaluate(x):
        val = 0
        d = len(x)
        for i in range(d):
            val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
        
        val = 418.9829*d - val
        
        return val
    
    
    #function to provide the rank order of fitness values in a list
    #not currently used in the algorithm, but provided in case you want to...
    def rankOrder(anyList):
        
        rankOrdered = [0] * len(anyList)
        for i, x in enumerate(sorted(range(len(anyList)), key=lambda y: anyList[y])):
            rankOrdered[x] = i
        
        return rankOrdered
    
    #performs tournament selection; k chromosomes are selected (with repeats allowed) and the best advances to the mating pool
    #function returns the mating pool with size equal to the initial population
    def tournamentSelection(pop,k):
        
        #randomly select k chromosomes; the best joins the mating pool
        matingPool = []
        
        while len(matingPool)<populationSize:
            
            ids = [myPRNG.randint(0,populationSize-1) for i in range(k)]
            competingIndividuals = [pop[i][1] for i in ids]
            bestID=ids[competingIndividuals.index(min(competingIndividuals))]
            matingPool.append(pop[bestID][0])
        
        return matingPool
    
    #function to mutate solutions
    def mutate(x):
        d = len(x)
        
        # select the point to mutate
        mPT = myPRNG.randint(0, d - 1)
        
        # add random number between -5 and 5
        temp_x = x[mPT ] + myPRNG.uniform(-250,250)
        # the mutated value should be inside boundaries
        x[mPT] =(min(max(temp_x , lowerBound), upperBound))
        return x
    
    
    def breeding(matingPool):
        #the parents will be the first two individuals, then next two, then next two and so on
        
        children = []
        childrenFitness = []
        for i in range(0,populationSize-1,2):
            
            child1 = matingPool[i]
            child2 = matingPool[i+1]
            
            prob1 = myPRNG.random() # select random number between 0-1
            if prob1 < crossOverRate:
                child1,child2=crossover(matingPool[i],matingPool[i+1])
            
            prob2 = myPRNG.random() # select random number between 0-1
            if prob2 < mutationRate:
                child1=mutate(child1)
                child2=mutate(child2)
    
            children.append(child1)
            children.append(child2)
            
            childrenFitness.append(evaluate(child1))
        childrenFitness.append(evaluate(child2))
        
        tempZip = zip(children, childrenFitness)
        popVals = sorted(tempZip, key=lambda tempZip: tempZip[1])
        
        #the return object is a sorted list of tuples:
        #the first element of the tuple is the chromosome; the second element is the fitness value
        #for example:  popVals[0] is represents the best individual in the population
        #popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
        
                return popVals


#insertion step
def insert(pop,kids):
    #please implement some type of elitism
    total = pop + kids
        # fittest population goes to next generation
        Vals_total = sorted(total, key=lambda total: total[1])
        new_gen = Vals_total[0:populationSize]
        return new_gen
    
    
    #perform a simple summary on the population: returns the best chromosome fitness, the average population fitness, and the variance of the population fitness
    def summaryFitness(pop):
        a=np.array(list(zip(*pop))[1])
        return np.min(a), np.mean(a), np.var(a)
    
    #the best solution should always be the first element... if I coded everything correctly...
    def bestSolutionInPopulation(pop):
        #print (pop[0])
        return pop[0]
    
    #optional: you can output results to a file -- i've commented out all of the file out put for now
    
    #f = open('out.txt', 'w')  #---uncomment this line to create a file for saving output
    
    #GA main code
    
    best_set = []
    Population = initializePopulation()
    for j in range(Generations):
        mates=tournamentSelection(Population,3)
        Offspring = breeding(mates)
        Population = insert(Population, Offspring)
        
        #end of GA main code
        
        minVal,meanVal,varVal=summaryFitness(Population)  #check out the population at each generation
    #print(summaryFitness(Population))                 #print to screen; turn this off for faster results
    
    #f.write(str(minVal) + " " + str(meanVal) + " " + str(varVal) + "\n")  #---uncomment this line to write to  file
    
    #f.close()   #---uncomment this line to close the file for saving output
    
    #print (summaryFitness(Population))
    best = bestSolutionInPopulation(Population)
    best_set.append(best[1])
    return best_set
