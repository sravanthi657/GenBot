import json
import random
import submission as sub
import client as server
from datetime import datetime
import numpy as np

SECRET_KEY='IujyVmfSoYj21ypDeh9dgFRqVY5ehtC7gmDmNn7JfVrIQQhuoo'
population=8#anything greater than 7
size=11
gens=2
pool_size=5
#overfit=[0, 0, -2.2905717e-05, 0.000462009974, -1.75214947e-06, -1.8525075e-15, -10, 2.29423303e-05, -2.04721003e-06, -1.59792835e-08, 9.98214034e-10]
overfit=[0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]
#fitness = np.empty((population*gens, 3))	

def initializing():
	a=np.copy(overfit)
	for i in range(11):
		fact=random.uniform(-0.1,0.1)
		a[i]=np.random.choice([overfit[i]*(fact+1),overfit[i]],p=[0.2,1-0.2])
		if (a[i]<-10):
			a[i]=-10
		elif(a[i]>10):
			a[i]=10
	return a

def crossover(parent1, parent2):
    child1 = []
    child2 = []
    u = random.uniform(0,1) 
    n_c = random.randint(2,5)
    aa1=((n_c + 1)**-1)
    if (u < 0.5):
        b = (2 * u)**aa1
    else:
        b = ((2*(1-u))**-1)**aa1
    parent1 = np.array(parent1)
    parent2 = np.array(parent2)
    child1 = 0.5*((1 + b) * parent1 + (1 - b) * parent2)
    child2 = 0.5*((1 - b) * parent1 + (1 + b) * parent2)

    return child1, child2
def mutation(child):
	for i in range(11):
		fact=random.uniform(-0.1,0.1)
		child[i]=np.random.choice([child[i]*(fact+1),child[i]],p=[0.8,1-0.8])
		if (child[i]<-10):
			child[i]=-10
		elif(child[i]>10):
			child[i]=10
	return child

        
def fitness_per_population(popu):
	fitness = np.empty((population, 3))
	for i in range(population):
		print(popu[i])
		error = server.get_errors(SECRET_KEY, list(popu[i]))
		fitness[i][2]=np.copy((error[0]+error[1]*0.3))
		fitness[i][0]=np.copy((error[0]))
		fitness[i][1]=np.copy((error[1]))
		print('fitness')
		print("Fitness",fitness[i][0])
		print("Validation:",fitness[i][1])
		print("Train:",fitness[i][2])
	pop_fit = np.column_stack((popu, fitness))
	pop_fit = pop_fit[np.argsort(pop_fit[:,-1])]
	return pop_fit
def mating(population_fitness):
		population_fitness=population_fitness[np.argsort(population_fitness[:,-1])]
		return population_fitness
def create_child(mating_pool):
	mating_pool=mating_pool[:,:-3]
	children=[]
	for i in range(int(population/2)):
		r=random.randint(0,pool_size)
		first_parent=mating_pool[r]
		r1=random.randint(0,pool_size)
		second_parent=mating_pool[r1]
		child1,child2=crossover(first_parent,second_parent)
		child1 = mutation(child1)
		child2 = mutation(child2)
		children.append(child1)
		children.append(child2)
	return children  
def new_generation(parents_fitness, children):
    children_fitness = fitness_per_population(children)
    parents_fitness = parents_fitness[:5]
    children_fitness = children_fitness[:3]
    generation = np.concatenate((parents_fitness, children_fitness))
    generation = generation[np.argsort(generation[:,-1])]
    return generation
def main():
	print("")
	mated=[]
	stacked_fitness=[]
	now=datetime.now()
	print(now)
	b=np.zeros((population,size))
	for i in range(population):
		print(i)
		b[i]=initializing()
		print(b[i])
	stacked_fitness=fitness_per_population(b)
	for i in range(gens):
		mated=mating(stacked_fitness)
		childs=create_child(mated)
		stacked_fitness = new_generation(mated, childs)


if __name__=='__main__':
	main()
