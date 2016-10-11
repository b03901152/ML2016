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
average=np.average(trainlist,axis=1)
print trainlist.shape, trainlist[0].shape
print np.corrcoef(trainlist)[9]

















