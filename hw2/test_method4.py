import numpy as np
import time
import pickle
import random
import sys

class tree:
	def __init__(self,data,feature_nums):
		ones=0
		zeros=0
		for i in data:
			if i[57]==1:
				ones+=1
			else:
				zeros+=1
		if ones==len(data):
			self.leaf=1
			return
		elif zeros==len(data):
			self.leaf=0
			return
		else:
			self.leaf=2
		repeat=1
		while repeat==1:
			repeat=0
			if len(feature_nums)==0:
				feature_nums=np.array(random.sample(np.arange(57),1))
			sort_order=np.array( np.argsort(data[:,feature_nums[0]],axis=0) )
			d=data.copy()
			for i in range(len(sort_order)):
				d[i]=data[ sort_order[i] ]
			# 	raw_input()
			l=0
			r=0
			gini=[]
			for i in d:
				if i[57]==1:
					r=r+1
			for i in range(len(d)-1):
				if d[i][57]==1:
					l+=1
					r-=1
				if d[i][feature_nums[0]]==d[i+1][feature_nums[0]]:
					gini.append(1)
					continue
				# left_probability
				lp=float(i+1)/len(d)
				ql=float(l)/(i+1)
				left_gini_index=1-ql**2-(1-ql)**2
				rl=float(r)/(len(d)-i-1)
				right_gini_index=1-rl**2-(1-rl)**2
				gini_index=lp*left_gini_index+(1-lp)*right_gini_index
				gini.append(gini_index)
			index=np.argmin(gini)
			if gini[index]==1:
				feature_nums=feature_nums[1:]
				# print "feature"
				repeat=1
		self.threshold=float(d[index][feature_nums[0]]+d[index+1][feature_nums[0]])/2
		self.feature_num=feature_nums[0]
		if len(feature_nums)!=1:
			self.left_tree = tree(d[:index+1,:], feature_nums[1:])
			self.right_tree = tree(d[index+1:,:], feature_nums[1:])
		else:
			if ones>=zeros:
				if ones==zeros:
					self.threshold=-1
					self.right_tree = tree(d[index+1:,:],np.array(random.sample(np.arange(57),1)))
					self.leaf=2
				self.leaf=1
			else:
				self.leaf=0


forest=pickle.load(open(sys.argv[1], "r"))
tree_num=len(forest)

# read spam_test.csv
test=np.genfromtxt(sys.argv[2], delimiter="," , dtype="double")
test=test[:,1:]





def check(x):
	global forest
	global tree_num
	counter=0
	for p in forest:
		while p.leaf==2:
			if x[p.feature_num]>=p.threshold:
				p=p.right_tree
			elif x[p.feature_num]<p.threshold:
				p=p.left_tree
		counter+=p.leaf
	if counter>(tree_num/2):
		return 1
	return 0


pre_submit=[]
for i in range(len(test)):
	pre_submit.append(check(test[i]))

#submition
id=[]
id.append('id')
for x in range(1,601):
	id.append(x)
labelstr=[]
labelstr.append('label')
labelstr+=pre_submit
submit=[]
for x in range(601):
	submit.append( [ id[x],labelstr[x] ] )
submit=np.array(submit)
# print submit
np.savetxt(sys.argv[3],submit,fmt="%s",delimiter=',')

