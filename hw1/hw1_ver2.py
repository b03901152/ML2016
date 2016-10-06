import numpy as np

data=np.genfromtxt('train.csv', delimiter="," , dtype="string")
data=data[1:,3:]
trainlist=data[0:18,:].tolist()
for x in range(1,240): #240days
	for i in range(18):
		trainlist[i]+=data[18*x+i,:].tolist()
trainlist=np.array(trainlist)
trainlist=np.delete(trainlist,10,0)

# trainlist=np.delete(trainlist,16,0)
# trainlist=np.delete(trainlist,15,0)
# trainlist=np.delete(trainlist,14,0)
# trainlist=np.delete(trainlist,12,0)
# trainlist=np.delete(trainlist,11,0)
# trainlist=np.delete(trainlist,4,0)
# trainlist=np.delete(trainlist,3,0)
# trainlist=np.delete(trainlist,2,0)
# trainlist=np.delete(trainlist,1,0)

trainlist=trainlist.astype(float)
trainlist=np.hsplit(trainlist,12)
trainlist=np.array(trainlist)
np.savetxt('output_test.csv',trainlist,fmt="%s",delimiter=",")

w=[]
epsilon=1
b=0
n0=0.000002
rate_sum=0
n=0.0000002
# y
L=0
tmp=[]
partial_L_partial_w=0
for j in range(9):
	tmp.append(0.1)
for i in range(len(trainlist[0])):
	w.append(tmp)
w=np.array(w)
for x in range(2):
	for i in range(12):
		for j in range(470):#20*24
			trainning=trainlist[i,:,j:j+9]
			y=trainlist[i][9][j+9]#PM2.5 is 9th of data
			partial=b+np.sum(np.sum(w*trainning,axis=0),axis=0)-y
			partial_L_partial_w=partial*trainning
			w=w-n*partial_L_partial_w
			b=b-n*partial
			pp=(rate_sum*1e-12+epsilon)**0.5
			n=n0/pp
			rate_sum+=np.sum(np.sum(partial_L_partial_w*partial_L_partial_w,axis=0),axis=0)
			delta=np.sum(np.sum(partial_L_partial_w*partial_L_partial_w,axis=0),axis=0)
		print pp,delta*1e-6


L=0
for i in range(12):
	for j in range(470):#20*24
		test=trainlist[i,:,j:j+9]
		y=trainlist[i][9][j+9]
		L+= (b+np.sum(np.sum(w*trainning,axis=0),axis=0)-y)**2
print 'L=',L*1e-6


#read the test data
test=np.genfromtxt('test_X.csv', delimiter="," , dtype="string")
test=test[:,2:]
testlist=test[0:18,:].tolist()
for j in range(1,240):
	for i in range(18):
		testlist[i]+=test[18*j+i,:].tolist()

testlist=np.array(testlist)
testlist=np.delete(testlist,10,0)
testlist=np.hsplit(testlist,240)
testlist=np.array(testlist)
testlist=testlist.astype(float)
outcome=[]
for i in range(240):
	outcome.append(np.sum(np.sum( w*testlist[i] ,axis=0),axis=0))
outcome=np.array(outcome)
print outcome

relation=[]
for i in range(12):
		for j in range(470):#20*24
			trainning=trainlist[i,:,j:j+9]
			if len(relation)==0:
				relation=np.sum(w*trainning,axis=1)
			relation=+np.sum(w*trainning,axis=1)

# relation=np.sum(w*testlist[0],axis=1)
# for i in range(1,240):
# 	relation+=np.sum(w*testlist[i],axis=1)
print relation



#submition
id=[]
id.append('id')
for x in range(240):
	id.append('id_'+str(x))
valuestr=[]
outcome.astype(str).tolist()
valuestr.append('value')
valuestr+=outcome
answer=[]
for x in range(241):
	answer.append( [ id[x],valuestr[x] ] )
answer=np.array(answer)
np.savetxt('answer.csv',answer,fmt="%s",delimiter=',')


