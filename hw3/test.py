from keras.layers import Input, Dense, Activation, Convolution2D, MaxPooling2D, Flatten, MaxoutDense, Dropout
from keras.models import Model
import pickle
import numpy as np
from keras.models import Sequential, load_model
from keras.utils.np_utils import to_categorical
import sys

model=load_model(sys.argv[2])


test=pickle.load(open(sys.argv[1]+'test.p', "rb"))
test=np.reshape( np.array(test['data']) , (10000,3,32,32)).astype('float32')
predict_result = model.predict( test )
print ('predicted')
pre_submit=[]
for i in range(len(predict_result)):
	pre_submit.append( np.argmax( predict_result[i] ) )



#submition
id=[]
id.append('ID')
for x in range(len(pre_submit)):
	id.append(x)
labelstr=[]
labelstr.append('class')
labelstr+=pre_submit
submit=[]
for x in range(len(pre_submit)+1):
	submit.append( [ id[x],labelstr[x] ] )
submit=np.array(submit)
np.savetxt(sys.argv[3],submit,fmt="%s",delimiter=',')
