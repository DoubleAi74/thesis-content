import numpy as np
import matplotlib.pyplot as plt
from math import floor


'''
The genetic algorithm is used in an attempt to fit a polynomial function to an observed data set.
'''

def read_file(file_path):
    '''Gets the data set from a text file.'''
    X, Y = [], []

    with open(file_path, 'r') as file:
        # Read the entire content as a string
        content = file.read()
        # Alternatively, read the lines of the file into a list
        # lines = file.readlines()
        
        # Process the content as needed

        rows = content.split('\n')
        for row in rows[:-1]:
            items = row.split(',')
            X.append(float(items[0]))
            Y.append(float(items[-1]))
            
    return X, Y


Pvals, Avals = read_file('AdataSave.txt')

print(Pvals)
print(Avals)

NumBases = 100 # number of terms in the polynomial
N = 50 # solutions in the evolving population 
mutRate = 0.3 # probability of a given base mutating 

'''The polynomial is of the form sum (a_i P^i). we consider only the first 
NumBases (10) terms. Each cefficient is a rational number of the form a_i = b1_i / b2_i.
A specific polynomial function can hense be described it terms of two lists of 
integers. This is how a particular solution is codefied:
[np.array(b1_1, b1_2, ...), np.array(b2_1, b2_2, ...)].'''


def generateRandomSolution():
    '''Two arrays of 10 integers are generated randomly. Each number is normally 
    distributed with mean 0 and standard deviation, 5.'''
    chrom1 = np.random.normal(0, 5, NumBases).astype(int)
    chrom2 = np.random.normal(0, 5, NumBases).astype(int)
    chrom2 = np.where(chrom2==0, 1, chrom2)
    
    # Fixing the first term to be 1/2 so as to satisfy the IC
    chrom1[0] = 1
    chrom2[0] = 2
    
    trialSolution = [chrom1, chrom2]
    return(trialSolution)

def evaluatePolynomial(P, solution):
    '''Computes the value of a given polynomial for a particular value of P.'''
    polyOut = 0
    for i, tup in enumerate([(n1,n2) for n1,n2 in zip(solution[0], solution[1])]):
        polyOut += (tup[0]/tup[1])*P**i
    return polyOut

def scoreSolution(solution):
    '''Measures the mean squared error between a given polynomial curve and
    the data points.'''
    
    diffs = []
    for i, P in enumerate(Pvals):
        A = Avals[i]
        polyVal = evaluatePolynomial(P, solution)

        squareDiff = (A - polyVal)**2
        diffs.append(squareDiff)
        
    mse = sum(diffs) / len(diffs)
    
    frmZeroSq = evaluatePolynomial(0.5, solution)**2
    
    score = mse + frmZeroSq*100
    
    return(score)



    
    

def plotSolutions(solutionsList):
    '''Takes a list of solutions (polynomials), and plots them all alongside
    the data points. '''
    
    
    # Create the plot
    fig, ax = plt.subplots()
    
    formatPlot(ax)

    ax.scatter(Pvals, Avals, linewidths = 0.2)

    for i, solution in reversed(list(enumerate(solutionsList))):
        
        col = "red" if i == 0 else 'black' 
        alp = 1 if i == 0 else 0.1
        lw = 3 if i == 0 else 1
      
        
        Fvals = []
        X = np.arange(0,0.6,0.01)
        for P in X: 
            Fvals.append(evaluatePolynomial(P, solution))
            
        ax.plot(X, Fvals, color = col, linewidth = lw, alpha = alp)
    
    
    
    
def formatPlot(ax):
    # Add a horizontal line at y=0
    ax.axhline(y=0, color='black', linewidth=0.5)

    # Remove the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set the bottom and left spines to be the x and y axis, respectively
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))

    # Add a title and axis labels
    ax.set_title("Genetic algorithm converging polynomials")
    ax.set_ylabel("Constant: A(P)", labelpad=5)
    ax.set_xlabel("P")

    # Set the limits of the x and y axes
    ax.set_xlim([0, 0.6])
    ax.set_ylim([0, 0.6])

    # Remove the tick marks on the top and right spines
    ax.xaxis.tick_bottom()
    ax.yaxis.tick_left()

    # Remove the 0.0 tick label from the y-axis
    y_ticks = ax.get_yticks()
    ax.set_yticks([tick for tick in y_ticks if tick != 0])
    

def chooseRandFromOrder(N):
    '''Randomly chooses indecies of a list according to a descending
    geometric distribution.
    This is used to select parents of the next population at random, those 
    with higher fitness being selected with a greater likelihood. '''
    probs = np.array([1/i for i in range(1, N+1)])
    prSum = np.sum(probs)
    probs /= prSum
    
    index = np.random.choice(list(range(N)), p = probs)
    
    return index




def mutate(child):
    '''For a newly generated solution, each number may be moved by + or - 1
    with some mutation probability. If one of the denominators is modified 
    to be 0, the same modification will take place again. For example, if 
    1 is mutated to 0, it will immediately become -1.'''
    for chromIndx in range(2): 
        # The first base location isn't mutated to matain the initial condition
        for baseIndx in range(1, NumBases): 
            if np.random.uniform(0,1) < mutRate:
                #mutation = np.random.choice([-1,1])
                mutation = np.random.normal(0,5,1).astype(int)[0]
                child[chromIndx][baseIndx] += mutation
                if chromIndx == 1 and child[chromIndx][baseIndx] == 0:
                    child[chromIndx][baseIndx] += mutation
                    
    return child

def crossover(parent1, parent2):
    '''Two parent solutions are used to generate one new offspring. Each digit
    of the two lists is taken either from the first parent, or the or the second;
    either option taking place with probabiliy 0.5.'''
    child = [np.zeros(NumBases), np.zeros(NumBases)]

    for chromIndx in range(2): 
        for baseIndx in range(NumBases):
            heritance = None
            
            if np.random.uniform(0,1) < 0.5:
                heritance = parent1[chromIndx][baseIndx]
            else:
                heritance = parent2[chromIndx][baseIndx]
            
            child[chromIndx][baseIndx] = heritance

    return child

def makeNewGeneration(populationSorted): 
    '''A new population is generated by crossing and mutating those of the 
    previous. Fitter solutions are chosen preferentially; the best solution 
    is always kept unchanged, the remaining 49 generated a new.'''
    
    population = [populationSorted[0]] # always keep best
    
    for i in range(N-1): # 49 pairs of parents 
        parent1 = populationSorted[chooseRandFromOrder(N)]
        parent2 = populationSorted[chooseRandFromOrder(N)]
        
        child = crossover(parent1, parent2)
        child = mutate(child)
        
        population.append(child)
    
    return population
    


def sortOnFitness(population, mseVals):
    
    mseIndexTuples = [(mse, i) for i, mse in enumerate(mseVals)]
    mseIndexTuples = sorted(mseIndexTuples)
    
    sortedPopulation = []
    for tup in mseIndexTuples:
        sortedPopulation.append(population[tup[1]])
    
    return sortedPopulation, mseIndexTuples[0][0]







def iterateGeneration(population):
    
    # Score each individual; compute the mean squared error values (fitness)
    mseVals = [scoreSolution(sol) for sol in population]
    
    sortedPopulation, bestMSE = sortOnFitness(population, mseVals)
    print(bestMSE)
    
    plotSolutions(sortedPopulation)#[:10])

    
    newPopulation = makeNewGeneration(sortedPopulation)
    
    return newPopulation

    
# Generate an initial population
population = [generateRandomSolution() for i in range(N)]

numGenerations = 100
for gen in range(numGenerations):
    population = iterateGeneration(population)
    
    
print(population[0])

#1/2 - 1/3 P - 1/6P^2
    
    



    
    
    
    