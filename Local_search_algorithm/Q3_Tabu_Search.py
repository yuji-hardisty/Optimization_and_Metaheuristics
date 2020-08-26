#need some python libraries
import copy
from random import Random   #need this for the random number generation -- do not change
import numpy as np


#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 5113
myPRNG = Random(seed)

#to get a random number between 0 and 1, use this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

#number of elements in a solution
n = 150

#create an "instance" for the knapsack problem
value = []
for i in range(0,n):
    value.append(round(myPRNG.triangular(5,1000,200),1))
print(value)

weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(10,200,60),1))
print(weights)

#define max weight for the knapsack
maxWeight = 1500

#change anything you like below this line ------------------------------------

#monitor the number of solutions evaluated
solutionsChecked = 0

#function to evaluate a solution x
def evaluate(x):
    
    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)
    
    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection
    
    if totalWeight > maxWeight:
        totalValue = 0          # returns
    return [totalValue, totalWeight]   #returns a list of both total value and total weight


#here is a simple function to create a neighborhood

def neighborhood(x):
    
    nbrhood = []
    
    # add one and remove one simultaneously
    for i in range(0,n):
        for j in range(0,n):
            nbrhood.append(x[:])
            curr_row = i*n + j
            if nbrhood[curr_row][i] == 1:
                nbrhood[curr_row][i] = 0
            else:
                nbrhood[curr_row][i] = 1
            if nbrhood[curr_row][j] == 1:
                nbrhood[curr_row][j] = 0
            else:
                nbrhood[curr_row][j] = 1

#1-flip neighborhood of solution x
for i in range(0,n):
    nbrhood.append(x[:])
        if nbrhood[curr_row+i][i] == 1:
            nbrhood[curr_row+i][i] = 0
    else:
        nbrhood[curr_row+i][i] = 1


return nbrhood



#create the initial solution
def initial_solution():
    x = []   #i recommend creating the solution as a list
    x_array = np.zeros(n)
    # put items in the order of
    sumWeight = 0
    sumValue = 0
    v = np.array(value)
    w = np.array(weights)
    print("initial solution:")
    i = 0
    idx = np.arange(n)
    np.random.seed(4)  # set seed to be 1
    np.random.shuffle(idx)
    while True:
        if (sumWeight + weights[idx[i]])  > maxWeight:
            break
        sumWeight = sumWeight + weights[idx[i]]
        sumValue = sumValue + value[idx[i]]
        x_array[idx[i]] = 1
        print(value[idx[i]], weights[idx[i]])
        i = i + 1
    
    x = list(x_array)
    print ("sum of value = ",sumValue)
    print ("sum of weight = ",sumWeight)
    return x



#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution
x_best = x_curr[:]           #x_best will hold the best solution
f_curr = evaluate(x_curr)   #f_curr will hold the evaluation of the current soluton
f_best = f_curr[:]



#begin Tabu Search ----------------
done = 0
tabu_list = []         # build memory structure for tabu
tabu_list.append(x_curr)
maxTabu = 100          # maximum Tabu_list size
while done == 0:
    
    print ("\ntry new neigborhood")
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
    x_best = Neighborhood[0]
    f_best = evaluate(x_best)[:]
    
    for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
        solutionsChecked = solutionsChecked + 1
        if ((s not in tabu_list) and (evaluate(s)[0] > f_best[0])): # if new solution is not in tabu and better than current solution
            x_best = s[:]                 #find the best member and keep track of that solution
            f_best = evaluate(s)[:]       #and store its evaluation

if f_best == f_curr:               #if there were no improving solutions in the neighborhood
    done = 1
    
    
    if f_best > f_curr:               #if there were no improving solutions in the neighborhood
        x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best[:]         #evalute the current solution

tabu_list.append(x_best[:])    # push to tabu list cause x is considered.
    if (len(tabu_list) > maxTabu):
        tabuList.pop(0)


print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_curr[0])
print ("Weight is: ", f_curr[1])
print ("Total number of items selected: ", np.sum(x_curr))
print ("Best solution: ", x_curr)
