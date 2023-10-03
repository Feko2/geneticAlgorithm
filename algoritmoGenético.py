import random
import numpy as np
from matplotlib import pyplot as plt
from copy import copy
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from tqdm import tqdm




class Individuo():
    def __init__(self):
        self.individual_number = 0
        
    def createIndividuo(self):
        individuo=[]
        for i in range (20):
            magnitude = round(random.uniform(-3,3),3)
            direction = random.randint(0,1)
            point=[0,0]
            if direction == 0:
                point[0]=magnitude
                point[1]=0
            else:
                point[1]=magnitude
                point[0]=0
            point = tuple(point)
            individuo.append(point)
        return individuo
    
    
    
class populationManager():
    def __init__(self):
        self.len = 100
        self.individuos =[]
        
    def createFirstGeneration(self):
        individuos = self.individuos
        lenPoblacion = self.len
        for i in range(lenPoblacion):
            newIndividuo = Individuo()
            ind = newIndividuo.createIndividuo()
            individuos.append(ind)
        return individuos
    
    
    
    
class AlgoritmoGenetico():
    def __init__(self, reloaded=True):
        self.exit = []
        self.population=[]
        self.numGeneration = 0
        self.fitnessList=[]
        self.Generations= 200000
        self.d={}
        self.numMut=0
        self.xs=[]
        self.ys=[]
        self.reloaded = reloaded
        
    def initializeProcess(self):
        x = round(random.uniform(-30,30),3)
        y = round(random.uniform(-30,30),3)
        self.exit = [17.13,-15.764]
        poblacion = populationManager()
        self.population = poblacion.createFirstGeneration()
        self.numGeneration += 1
    
    def continueProcessing(self):
        fitness=[]
        orderedFitness = self.fitness(self.population)
        self.fitnessList.append(orderedFitness[0][1])
        fit=orderedFitness[0][1]
        self.d[fit]=1
        Generations = self.Generations
        for i in tqdm(range(Generations)):
            self.numGeneration +=1
            generation = self.cruza(orderedFitness)
            if self.d[fit] >= 40: 
                generation = self.mutacion(generation)
                
            orderedFitness = self.fitness(generation)
            self.fitnessList.append(orderedFitness[0][1])#
            fitness.append(orderedFitness[0][1])#

            fit = orderedFitness[0][1]
            if fit not in self.d.keys():
                self.d[fit]=1
            else:
                self.d[fit]+=1
                
                
            #criterios de salida
            if fit ==0:
                print("EXACT SOLUTION")
                self.getLastBestFitness(orderedFitness)
                break
            if (fit < 0.0001 and i > 20000) or self.d[fit]> 10000:
                print("NOT EXACT SOLUTION")
                break
                
        return orderedFitness

        
    def graphFitness(self):
        return self.fitnessList
    
        
    def fitness(self, population):
        exit = self.exit
        data = []
        listxs=[]
        listys=[]
        for j in range (len(population)):  
            sumX=0
            sumY=0
            for x, y in population[j]:
                sumX+=x
                sumY+=y
            sumX=round(sumX,3)
            sumY=round(sumY,3)
            resX = exit[0]-sumX
            resY =exit[1]-sumY
            resX=round(resX,3)
            resY=round(resY,3)
            magnitude = np.sqrt(resX**2 + resY**2)

            data.append(tuple([population[j], magnitude]))
            
            listxs.append(sumX)
            listys.append(sumY)
            
        self.xs.append(listxs)
        self.ys.append(listys)
        data.sort(key=lambda tup: tup[1])
        return data[0:100]
    
    def getLastBestFitness(self, generationWithFitness):
        listxs=[]
        listys=[]
        for j in range (len(generationWithFitness)):  
            sumX=0
            sumY=0
            for x, y in generationWithFitness[j][0]:
                sumX+=x
                sumY+=y
            sumX=round(sumX,3)
            sumY=round(sumY,3)
            listxs.append(sumX)
            listys.append(sumY)
            
        self.xs.append(listxs)
        self.ys.append(listys)


    def cruza(self, orderedPopulation):
        chosenCruza=[]
        newOrganismos=[]
        for i in range (25):
            chosenCruza.append(orderedPopulation[i][0])
        for i in range (59, 49, -1):
            chosenCruza.append(orderedPopulation[i][0])
        for i in range(99, 94, -1):
            chosenCruza.append(orderedPopulation[i][0])
            
        random.shuffle(chosenCruza)

        for i in range(0,40,2):        
            puntoDeCorte= random.randint(4, 15)
            
            hijo1=chosenCruza[i][0:puntoDeCorte]+chosenCruza[i+1][puntoDeCorte:20]
            hijo2=chosenCruza[i+1][0:puntoDeCorte]+chosenCruza[i][puntoDeCorte:20]
            newOrganismos.append(hijo1)
            newOrganismos.append(hijo2)

        for individuo in orderedPopulation:
            newOrganismos.append(individuo[0])
            
        if len (newOrganismos) < 140:
            print(len(newOrganismos))
        return newOrganismos
    
    def mutacion(self, population):
        self.numMut += 1
        mutatedNumbers=[]
        
        for i in range (100):
            newGenes=[]
            newNumber=True 
            while newNumber:
                toMutate=random.randint(0, len(population)-1)
                if toMutate not in mutatedNumbers:
                    newNumber = False
                    mutatedNumbers.append(toMutate)
                    
            mutateGenes = random.randint(1, 4)  
            for x in range (mutateGenes):
                newNumber = True                
                while newNumber:
                    posMutation = random.randint(0, 19)
                    if posMutation not in newGenes:
                        newNumber = False
                        newGenes.append(posMutation)
                        
                magnitude = round(random.uniform(-3,3),3)
                direction = random.randint(0,1)
                point=[0,0]
                if direction == 0:
                    point[0]=magnitude
                    point[1]=0
                else:
                    point[1]=magnitude
                    point[0]=0
                point = tuple(point)

                if self.reloaded == True:
                    if x ==0:
                        ind = copy(population[toMutate])
                        ind[posMutation]=point
                    else:
                        ind[posMutation]=point
                else:
                    population[toMutate][posMutation] = point

            if self.reloaded == True:
                population.append(ind)      
        return population


def graph(listx, listy, lenlists, exit ):
    xs=ys=[]
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    colors = ['g']
    colorsPob = ['r']
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set(xlim=(-32, 32), ylim=(-32, 32))
    scat = ax.scatter(xs, ys, c = colorsPob, s=45)
    ax.scatter(exit[0], exit[1], c = colors, s=50)
    result = []

    def animate(frame_num):
        xs = listx[frame_num]
        ys = listy[frame_num]
        scat.set_offsets(np.c_[xs, ys]) 
        ax.set_title('Gen ' + str(frame_num))
        result.append(xs)
        return scat

    anim = FuncAnimation(fig, animate, frames= lenlists, interval=1, repeat=False)
    plt.show()

def plot_best_individual_steps(best_individual, exit):
    # Starting point
    x, y = [0], [0]
    
    # Calculate cumulative steps
    for dx, dy in best_individual:
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)

    # Plot the steps
    plt.figure(figsize=(10, 10))
    plt.plot(x, y, '-o', label='Path')
    plt.scatter(exit[0], exit[1], c='red', label='Target', s=100)
    plt.title("Desplazón of the Best Individual")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    AG = AlgoritmoGenetico(True)
    AG.initializeProcess()
    data = AG.continueProcessing()
    pop = data[0][0]
    sumX=0
    sumY=0
    for x, y in pop:
        sumX+=x
        sumY+=y
    sumX=round(sumX,3)
    sumY=round(sumY,3)
    print("\nCoordenadas obtenidas: ", "("+str(sumX) +"," ,str(sumY)+")")
    print("Salida verdadera:",tuple(AG.exit))
    li = AG.graphFitness()
    print("Fitness inicial:", li[0])
    print("Fitness final:",li[-1])
    print("Desplazón Perfecto:", data[0][0])
    graph(AG.xs, AG.ys, len(AG.xs), AG.exit)
    if data[0][1] == 0:
        best_individual = data[0][0]
        plot_best_individual_steps(best_individual, AG.exit)
    
if __name__ == "__main__":
    main()
