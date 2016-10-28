import numpy as np
import time
import pickle
import sys
tStart = time.time()


data=np.genfromtxt(sys.argv[1], delimiter="," , dtype="string")

data=data[:,1:].astype(float)
answer=data[:,57]
data=data[:,:57]


average=np.average(data,axis=0)
Standard_Deviation=np.std(data,axis=0)
data=data-average
data=data/Standard_Deviation
w=1/average/len(data[0])/2

def trainning_L():
	global data
	global w
	global bias
	global answer
	loss=0
	z=np.sum(w*data,axis=1)+bias
	for k in range (len(z)):
		if z[k]<= -709:
			z[k]=-700
	f=1/(1+np.exp(-z))
	y=answer
	for i in range(len(f)):
		if f[i]==0:
			f[i]=0.00000000001
		elif f[i]==1:
			f[i]=0.99999999999
	loss=-np.sum(y*np.log(f)+(1-y)*np.log(1-f))
	print 'avg loss=',loss/len(data[0])
	tEnd = time.time()
	print  "It cost time=",tEnd - tStart
	return loss/len(data[0])



batch_num=100
eta0=0.11
bias=0
rho=0.92
def run():
	eta=eta0	
	Gt=0
	global batch_num
	global rho
	global bias
	global data
	global answer
	global w
	# w=1/average/len(data[0])/2
	rhos_outputs=[]
	batch_nums_outpus=[]
	Gt=0
	for number_of_times in range(10):
		for i in range (len(data)/batch_num):
			batch_data=data[i*batch_num:(i+1)*batch_num,:]
			z=np.sum(w*batch_data,axis=1)+bias
			for k in range (len(z)):
				if z[k]<= -709:
					z[k]=-700
			f=1/(1+np.exp(-z))
			y=answer[i*batch_num:(i+1)*batch_num]
			partial=np.sum(-(y-f)*np.transpose(batch_data),axis=1)
			partial_scale=np.sum(partial*partial,axis=0)
			Gt=rho*Gt+(1-rho)*partial_scale
			eta=eta0/((Gt+1)**0.5)
			w=w-eta*partial
			bias-=eta*np.sum(-(y-f),axis=0)
	# return trainning_L()
submit=1
if submit==1:
	while 1:
		if (time.time() - tStart)>570 and trainning_L()<14:
			break
		run()
run()

obj=[w,bias,average,Standard_Deviation]
pickle.dump(obj,open(sys.argv[2],"w"))

