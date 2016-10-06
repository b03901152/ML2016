import numpy as np

data=np.genfromtxt('train.csv', delimiter="," , dtype="string")
trainlist=[]
for x in range(len(data)):
	if data[x][2]=='PM2.5':
		if len(trainlist)==0:
			trainlist=data[x,3:].astype(float).tolist()
			continue
		trainlist+=data[x,3:].astype(float).tolist()
trainlist=np.array(trainlist)
trainlist=np.split(trainlist,12)
trainlist=np.array(trainlist)
np.savetxt('test',trainlist,fmt="%s")

w=[]
epsilon=10
b=0
n0=1.0
rate_sum=0
# n
# y
# L
for x in range(9):
	w.append(0.111)
w=np.array(w)
for i in range(12):
	for j in range(470):#20*24
		trainning=trainlist[i,j:j+9]
		y=trainlist[i,j+9]
		partial=b+np.inner(w,trainning)-y
		partial_L_partial_w=partial*trainning
		n=0.00001
		# n=n0/( (rate_sum+epsilon)**0.5 )
		w=w-n*partial_L_partial_w
		b=b-n*partial
		# rate_sum=rate_sum+sum(partial_L_partial_w)


#read the test data
test=np.genfromtxt('test_X.csv', delimiter="," , dtype="string")
testlist=[]
for x in range(len(test)):
	if test[x][1]=='PM2.5':
		testlist.append(test[x,2:].astype(float).tolist())
testlist=np.array(testlist)
# print testlist.shape
# print w.shape

outcome=np.dot(testlist,w)
# print w
# print outcome






#submition
id=[]
id.append('id')
for x in range(240):
	id.append('id_'+str(x))
valuestr=[]
outcome=np.array(outcome)
outcome.astype(str).tolist()
valuestr.append('value')
valuestr+=outcome
answer=[]
for x in range(241):
	answer.append( [ id[x],valuestr[x] ] )
answer=np.array(answer)
print answer.shape
print answer
np.savetxt('answer.csv',answer,fmt="%s",delimiter=',')



