import json
import random
import submission as sub
import client as server
from datetime import datetime
import numpy as np
overfit=[0.0, -1.45799022e-12, -2.28980078e-13, 4.62010753e-11, -1.75214813e-10, -1.8366977e-15, 8.5294406e-16, 2.29423303e-05, -2.04721003e-06, -1.59792834e-08, 9.83759863e-10]
pop_size=10
iter=10
SECRET_KEY='IujyVmfSoYj21ypDeh9dgFRqVY5ehtC7gmDmNn7JfVrIQQhuoo'
def initial():
	
	a=np.zeros(11)
	vec=np.random.randn(1,11)*((10**-17))
	a=overfit+vec[0]
	a=a.tolist()
	#print('############Generated Array###########')
	#print(a)
	return a
def mutate(child,prob):
    mutated_indices=[]
    for i in range(11):
        if(np.random.rand()<prob):
            mutated_indices.append(i+1)
            #child[i]=random.uniform(1e-10,-1e-10)
            child[i]=child[i]*(1+np.random.randn()/1000)
        if(abs(child[i])>=10):
            child[i]=child[i]*(1- abs(np.random.randn()/1000))

    print("Mutated Index:", mutated_indices)

    return child
def selection(error,b):
	selected=np.zeros(pop_size)
	mean=np.mean(error)
	std=np.std(error)
	for i in range(pop_size):
		selected[i]=(error[i]-mean)/(std+10**-17)
	[ind1,ind2]=sorted(range(len(selected)), key=lambda i: selected[i],reverse=True)[-2:]
	#print(ind1,ind2)
	arr3=np.zeros(11)
	chec=np.random.randint(0,11)
	print("Crossover point:",chec)
	d=np.random.randint(0,2) 
	print("Parent 1:",b[ind1])
	print("parent 2",b[ind2])
	pp1=b[ind1]
	pp2=b[ind2]
	if(d==0):
		temp=pp1
		pp1=pp2
		pp2=temp
	for i in range(11):
		if ( i<=chec):
			arr3[i]=pp2[i]
		else:
			arr3[i]=pp1[i]
	return(arr3)

#\033[1m  \033[0m
def main():
	#print("Overfit is (errors of order 10^11,10^12)",overfit)
	error=np.zeros(pop_size)
	e=np.zeros((pop_size,2))
	#now=datetime.now()
	#print("-----------------*************Date**************----------------",now)
	b=np.zeros((pop_size,11))
	for i in range(pop_size):
		b[i]=initial()
		#print(b[i])
	#sub.submit(SECRET_KEY,(a))
		#err=server.get_errors(SECRET_KEY,overfit)
		err=server.get_errors(SECRET_KEY,(b[i].tolist()))
		error[i]=((err[0]+(err[1]-err[0]))+(err[1]-(err[1]-err[0])))
	for jj in range(iter):
		print("**************************************************************")
		print("---------------------------New Iteration-----------------------")
		print("Iteration",jj+1)
		for i in range(pop_size):
			print()
			print("Parent population:")
			print(b[i])
			print("Fitness values:")
			print(error[i])
			#print("Error Values",e[i][0],e[i][1])
		children=np.zeros((pop_size,11))
		mutated=np.zeros((pop_size,11))
		child_error=np.zeros(pop_size)
		e2=np.zeros((pop_size,2))

		for i in range(pop_size):
		#print(i)
			print("------------(***)------------")
			print("Child Number:",i+1)
			children[i]=selection(error,b)
			print("Child after Crossover:")
			print(children[i])
			mutated[i]=mutate(children[i],0.2)
			print("Child After Mutation:")
			print(mutated[i])
			err=server.get_errors(SECRET_KEY,(mutated[i].tolist()))
			e2[i][0]=err[0]
			e2[i][1]=err[1]
			child_error[i]=((err[0]+(err[1]-err[0]))+(err[1]-(err[1]-err[0])))
			print("Fitness Value:",child_error[i])
		print()
		print("Children Vectors:")
		print(mutated)
		print()
		print("Fitness Values:")
		print(child_error)
		print()
		print("Errros:")
		print(e2)
		print()
		[ind1,ind2,ind3,ind4,ind5]=sorted(range(len(error)), key=lambda i: error[i],reverse=True)[-5:]
		best_from_parent=[ind1,ind2,ind3,ind4,ind5]
		[ind6,ind7,ind8,ind9,ind10]=sorted(range(len(child_error)), key=lambda i: child_error[i],reverse=True)[-5:]
		best_from_children=[ind6,ind7,ind8,ind9,ind10]
		final_generation=np.zeros((pop_size,11))
		for i in range(0,5):
			final_generation[i]=b[best_from_parent[i]]
		for i in range(5,10):
			final_generation[i]=mutated[best_from_children[5-i]]
		b=np.copy(final_generation)
		print("New Generation Generated:")
		print(b)
		final_errors=np.zeros(pop_size)
		for i in range(0,5):
			final_errors[i]=error[best_from_parent[i]]
		for i in range(5,10):
			final_errors[i]=child_error[best_from_children[5-i]]
		print()
		print("New Fitness Values")
		print(final_errors)
		print()
		print("Best Vector fromt his Generation:")
		print(b[np.argmin(final_errors)])
		print("With errors:")
		print(final_errors[np.argmin(final_errors)])
		error=np.copy(final_errors)


if __name__=='__main__':
	main()


