import numpy as np
import time
import pickle
import random
import sys
tStart = time.time()

origin_data=np.genfromtxt(sys.argv[1], delimiter="," , dtype="string")
origin_data=origin_data[:,1:].astype(float)

undelete=[3177,2837,2352,2294,1325,987]
for i in undelete:
	origin_data=np.delete(origin_data,i,axis=0)

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


# 3894
inner_num=0
sample_num_for_test=3994-inner_num
inner_test=origin_data[sample_num_for_test+1:,:]
origin_data=origin_data[:sample_num_for_test,:]

def test(tn,sample_num,feature_nums_array):

	global inner_test
	global origin_data
	global forest
	global tree_num
	tree_num=tn
	# tree_num=11
	forest=[]
	for i in range(tree_num):
		s=feature_nums_array
		# s=np.array(random.sample(np.arange(57),  random.randint(0,57)   ))
		d=np.array(random.sample(origin_data,sample_num))
		forest.append(tree(d,s))
	# pickle.dump(forest,"method4","w",protocol=2)
	pickle.dump(forest,open(sys.argv[2],"w"),protocol=2)

t=[21,2100,55]
test(t[0],t[1],np.array(random.sample(np.arange(57),t[2])))\

# [3, 1000, 40] 0.882
# [5, 1000, 40] 0.902
# [7, 1000, 40] 0.9
# [9, 1000, 40] 0.907
# [11, 1000, 40] 0.923
# [13, 1000, 40] 0.916
# [15, 1000, 40] 0.917
# [17, 1000, 40] 0.918
# [19, 1000, 40] 0.927
# [21, 1000, 40] 0.928
# [23, 1000, 40] 0.934
# [25, 1000, 40] 0.931
# [27, 1000, 40] 0.924
# [29, 1000, 40] 0.924
# [31, 1000, 40] 0.93
# [33, 1000, 40] 0.932
# [35, 1000, 40] 0.924
# [37, 1000, 40] 0.913
# [39, 1000, 40] 0.916

# [23, 1000, 19] 0.894
# [23, 1000, 21] 0.88
# [23, 1000, 23] 0.895
# [23, 1000, 25] 0.922
# [23, 1000, 27] 0.894
# [23, 1000, 29] 0.905
# [23, 1000, 31] 0.912
# [23, 1000, 33] 0.901
# [23, 1000, 35] 0.925
# [23, 1000, 37] 0.924
# [23, 1000, 39] 0.921
# [23, 1000, 41] 0.919
# [23, 1000, 43] 0.927
# [23, 1000, 45] 0.912
# [23, 1000, 47] 0.923
# [23, 1000, 49] 0.935
# [23, 1000, 51] 0.916
# [23, 1000, 53] 0.922
# [23, 1000, 55] 0.93


