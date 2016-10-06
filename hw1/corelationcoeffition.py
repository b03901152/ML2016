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
	if np.corrcoef(trainlist)[9][i]<0.4:
		print i
		remain-=1
print 'remain=',remain


# 0.2=> L=14000
# 0.4=> L=10000
	# 0.6 10300













