import json
import random
#import submission as sub
import client as server
from datetime import datetime
import numpy as np

SECRET_KEY='IujyVmfSoYj21ypDeh9dgFRqVY5ehtC7gmDmNn7JfVrIQQhuoo'
population=1 #anything greater than 7
size=11
gens=5
pool_size=10
#overfit=[0, 0, -2.2905717e-05, 0.000462009974, -1.75214947e-06, -1.8525075e-15, -10, 2.29423303e-05, -2.04721003e-06, -1.59792835e-08, 9.98214034e-10]
overfit=[0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

def initializing():
		a=np.zeros(size)
		q1=2e-16
		q2=9e-18
		operation ='-'
		print("limits",q1,q2)
		print("operation"+operation)
		for i in range(size):
			aa=random.uniform(q1,q2)
			if(((abs(overfit[i]-(aa)))<10 and (abs(overfit[i]-(aa)))>-10) ):
				a[i]=overfit[i]-(aa)
				print("random chosen",aa)
			else:
				a[i]=random.uniform(-1e-10,1e-10)					
			print("after changing",a[i])
		return a
def fitness_per_population(err,each_parent,fitness):	
	fitness[each_parent][0]=np.copy((err[0]*0.7+err[1]))
	fitness[each_parent][1]=np.copy((err[0]))
	fitness[each_parent][2]=np.copy((err[1]))
	print('fitness')
	print(fitness[each_parent][0])
def mating(b,fitness):
		population_fitness=np.column_stack((population, fitness))
		population_fitness=population_fitness[np.argsort(fitness[:,-1])]
		return population_fitness
def create_child(mating_pool):
	mating_pool=mating_pool[:,:-1]
	for i in range(population/2):
		r=random.randint(0,pool_size)
		first_parent=mating_pool[r]
		r1=random.randint(0,pool_size)
		second_parent=mating_pool[r1]
		child_1,child_2=crossover(first_parent,second_parent)
def crossover(first_parent,second_parent):
	child_1=np.empty(10)
	child_2=np.empty(10)
	p1=first_parent.tolist()
	p2=second_parent.tolist()
	point_is=np.random.choice(11,5,replace=False)
	cross_at=point_is.tolist()
	for i in cross_at:
        child1[i] = np.copy(second_parent[i])
        child2[i] = np.copy(first_parent[i])

def main():
	print("")
	fitness = np.zeros((population,3))
	now=datetime.now()
	print(now)
	b=np.zeros((population,size))
	for i in range(population):
		print(i)
		b[i]=initializing()
		print(b[i])
	for i in range(population):
		vec=b[i].tolist()
		err=server.get_errors(SECRET_KEY,vec)
		print(err)
		print('calculating fitness for generation',i)
		fitness_per_population(err,i,fitness)
	for i in range(gens):
		mated=mating(b,fitness)
		childs=create_child(mated)
		



	print(err)
if __name__=='__main__':
	main()
