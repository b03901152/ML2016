import numpy as np

data=np.genfromtxt('train.csv', delimiter="," , dtype="string")
data=data[1:,3:]
trainlist=data[0:18,:].tolist()
for x in range(1,240): #240days
	for i in range(18):
		trainlist[i]+=data[18*x+i,:].tolist()
trainlist=np.array(trainlist)
index_or_rows_should_be_delete=[10,16,15,14,13,10,4,3,2,1,0]
PM2_5_index=4 #1th
for i in index_or_rows_should_be_delete:
	trainlist=np.delete(trainlist,i,0)
trainlist=trainlist.astype(float)
trainlist=np.hsplit(trainlist,12)
trainlist=np.array(trainlist)

#read the test data
test=np.genfromtxt('test_X.csv', delimiter="," , dtype="string")
test=test[:,2:]
testlist=test[0:18,:].tolist()
for j in range(1,240):
	for i in range(18):
		testlist[i]+=test[18*j+i,:].tolist()
testlist=np.array(testlist)
for i in index_or_rows_should_be_delete:
	testlist=np.delete(testlist,i,0)
testlist=np.hsplit(testlist,240)
testlist=np.array(testlist)
testlist=testlist.astype(float)

# answer=np.genfromtxt('answer.csv', delimiter="," , dtype="string")
# answer=answer.astype(float)


w=[]
outcome=[]
test=[]

# y
tmp=[]
def init_w():
	global w
	for i in range(9):
		tmp.append(0.1)
	for i in range(len(trainlist[0])):
		w.append(tmp)
	w=np.array(w)
w=np.genfromtxt('w.csv', delimiter="," , dtype="string")
w=w.astype(float)
# init_w()

def test_L():
	L=0
	global trainlist
	global w
	for i in range(12):
		for j in range(470):#20*24
			test=trainlist[i,:,j:j+9]
			y=trainlist[i][PM2_5_index][j+9]
			L+= (b+np.sum(np.sum(w*trainning,axis=0),axis=0)-y)**2
	print 'L of trainning=',L/(471)/12
	return L/471/12

# def true_L():
# 	L=0
# 	global outcome
# 	global answer

# 	for i in range(240):
# 		L+= (outcome[i]-answer[i])**2
# 	print 'true L:',L/240
# 	return L/240

partial_L_partial_w=0
epsilon=1
b=0
n=n0=1e-8
rate_sum=1e7
counter=0
L_hold=0
counter=0
lamda=0
t=0
for x in range(1):
	for i in range(12):
		for j in range(470):#20*24
			trainning=trainlist[i,:,j:j+9]
			y=trainlist[i][PM2_5_index][j+9]#PM2.5 is 9th of data
			# regulation=np.sum(np.sum(w*w,axis=0),axis=0)
			partial=b+np.sum(np.sum(w*trainning,axis=0),axis=0)-y
			partial_L_partial_w=partial*trainning
			w=w-n*partial_L_partial_w
			b=b-n*partial
			rate=np.sum(np.sum(partial_L_partial_w*partial_L_partial_w,axis=0),axis=0)/1e10
			rate_sum+=rate
			G=(rate_sum+epsilon)**0.5
			n=n0/G



outcome=[]
for i in range(240):
	outcome.append(np.sum(np.sum( w*testlist[i] ,axis=0),axis=0))
outcome=np.array(outcome)
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
np.savetxt('kaggle_best.csv',answer,fmt="%s",delimiter=',')


