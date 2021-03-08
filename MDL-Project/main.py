import numpy as np
import json
import random
from datetime import datetime
import client as server
SECRET_KEY='IujyVmfSoYj21ypDeh9dgFRqVY5ehtC7gmDmNn7JfVrIQQhuoo'
population=2 #anything greater than 7
size=11
train_factor=0.7
fitness = np.zeros((population,3))
overfit=[0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]
def initializing():
	a=np.zeros(size)
	for i in range(size):
			#print(i)
			#aa=1e-30
			aa=random.uniform(9e-17,1e-18)
			if((abs(overfit[i]-(aa)))<10 and (abs(overfit[i]-(aa)))>-10):
				a[i]=overfit[i]-(aa)
			else:
				a[i]=random.uniform(-1e-10,1e-10)
			print(aa)
	return a
def fitness_per_population(err,each_parent):	
	fitness[each_parent][0]=np.copy((err[0]*train_factor+err[1]))
	fitness[each_parent][1]=np.copy((err[0]))
	fitness[each_parent][2]=np.copy((err[1]))
	print('fitness')
	print(fitness[each_parent][0])

def main():
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
		fitness_per_population(err,i)
		
if __name__=='__main__':
	main()
