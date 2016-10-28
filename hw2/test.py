import sys
import numpy as np
import pickle
# $1: model name, $2 testing data, $3: prediction.csv
obj=pickle.load(open(sys.argv[1], "r"))
[w,bias,average,Standard_Deviation]=obj


# read spam_test.csv
test=np.genfromtxt(sys.argv[2], delimiter="," , dtype="double")
test=test[:,1:]
test=(test-average)/Standard_Deviation
pre_submit=w*test
pre_submit=np.sum(pre_submit,axis=1)
pre_submit+=bias
pre_submit=1/( 1+np.exp(-pre_submit) )
pre_submit=pre_submit.tolist()
for i in range(len(pre_submit)):
	if pre_submit[i]>=0.5:
		pre_submit[i]='1'
	else:
		pre_submit[i]='0'

# print pre_submit


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
np.savetxt(sys.argv[3],submit,fmt="%s",delimiter=',')

