import numpy as np

data=np.genfromtxt('train.csv', delimiter="," , dtype="string")
data=data[1:,3:]
trainlist=data[0:18,:].tolist()
for x in range(1,240): #240days
	for i in range(18):
		trainlist[i]+=data[18*x+i,:].tolist()
trainlist=np.array(trainlist)
trainlist=np.delete(trainlist,10,0)
trainlist=trainlist.astype(float)
# average=np.average(trainlist,axis=1)
print np.corrcoef(trainlist)[9]
remain=17
for i in range(17):
	if np.corrcoef(trainlist)[9][i]<0.35:
		print i
		remain-=1
print 'remain=',remain


# 0.2=> 
# 0.35=> L=10486
# L of trainning= 281.484985478
# true L: 42.3751276974
# 0.4=> L=10600
	# 0.6 42/281
# L of trainning= 281.787973593
# true L: 42.4893611422












