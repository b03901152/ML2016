from keras.layers import Input, Dense, Activation, Convolution2D, MaxPooling2D, Flatten, MaxoutDense, Dropout
from keras.models import Model
import pickle
import numpy as np
from keras.models import Sequential, load_model
from keras.utils.np_utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
import sys


# 9:16
class CNN:
	def __init__( self ):
		self.model = Sequential()
		self.model.add( Convolution2D(64 ,3 ,3 ,activation='relu', border_mode='same', input_shape=(3,32,32)) )
		self.model.add( Convolution2D(64 ,3 ,3 ,activation='relu', border_mode='same' ) )
		self.model.add( MaxPooling2D((2, 2), border_mode='same') )
		self.model.add( Convolution2D(128 ,3 ,3 ,activation='relu', border_mode='same') )
		self.model.add( Convolution2D(128 ,3 ,3 ,activation='relu', border_mode='same') )
		self.model.add( MaxPooling2D((2, 2), border_mode='same') )
		self.model.add( Convolution2D(256 ,3 ,3 ,activation='relu', border_mode='same'))
		self.model.add( Convolution2D(256 ,3 ,3 ,activation='relu', border_mode='same'))
		# self.model.add( Dropout(0.1) )
		self.model.add( MaxPooling2D((2, 2), border_mode='same') )
		self.model.add( Flatten() )
		self.model.add( Dense( output_dim = 512, activation = 'sigmoid' ) )
		self.model.add( MaxoutDense( output_dim = 10 ) )
		self.model.add(Activation('softmax'))
		self.model.compile( loss = 'categorical_crossentropy', optimizer = 'rmsprop', metrics = [ 'accuracy' ] )
		self.history=[]
		self.datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=15,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images
	def fit(self, nb_epoch):
		self.datagen.fit(self.data)
		self.history.append (self.model.fit_generator(self.datagen.flow(self.data, self.class_label,
				                    batch_size=50),
				                    samples_per_epoch=self.data.shape[0],
				                    nb_epoch=nb_epoch,
				                    validation_data=(self.X_test, self.Y_test)).history)
	def load( self, path ):
		self.model = load_model( path )
		print ('load from ',path)
	def save( self ,path ,history_path):
		self.model.save( path )
		print ('save in',path)
		history=[[],[],[],[]]
		for i in range( len(self.history) ):
			history[0]=np.append( history[0], self.history[i]['acc'], axis=0 )
			history[1]=np.append( history[1], self.history[i]['val_loss'], axis=0 )
			history[2]=np.append( history[2], self.history[i]['loss'], axis=0 )
			history[3]=np.append( history[3], self.history[i]['val_acc'], axis=0 )
		history=np.array(history)
		print ( 'history=',history )
		print ('his path=',history_path)
		# pickle.dump(history,open(history_path,"wb"))
		
	def predict( self, x ):
		return self.model.predict( x )
	def init_datas(self,unlabel,label,label_class):
		self.data=label
		self.class_label=label_class
		self.all_unlabel=unlabel
		self.added_unlabel_class=np.array([])
		self.added_unlabel=np.array([])
		test_data_size=50
		self.X_test=self.data[:test_data_size,:,:,:]
		self.Y_test=self.class_label[:test_data_size,:]
		self.data = self.data[test_data_size:,:,:,:]
		self.class_label = self.class_label[test_data_size: , :]
	def add_unlabel(self):
		predict_result = self.model.predict( self.all_unlabel )
		print ('predicted')
		append_index=[]
		append_class_index=[]
		for i in range(len(predict_result)):
			if np.amax( predict_result[i] ) > 0.9:
				append_index.append(i)
				append_class_index.append(np.argmax( predict_result[i] ))
		length=len(append_index)
		print ('add ',length,' data')
		if length==0:
			return
		new_label_class=to_categorical( np.array( append_class_index ) ,10)
		new_label = np.zeros( (length,3,32,32) )
		for i in range( length ):
			new_label[i]=self.all_unlabel[ append_index[i] ]

		new_unlabel = np.zeros ((self.all_unlabel.shape[0]-length,3,32,32))
		remove_index=np.zeros( (len(self.all_unlabel)) )
		k=0
		for i in range(len(self.all_unlabel)):
			if i == append_index[k]:
				remove_index[i] = True
				k=k+1
				if k == len(append_index):
					break
			else :
				remove_index[i] = False
		
		j=0
		for i in range(len(self.all_unlabel)):
			if remove_index[i] == False:
				new_unlabel[j]=self.all_unlabel[i]
				j=j+1
			if(i==(len(self.all_unlabel)-1) ):
				print ('complete add un_label!')

		self.all_unlabel=new_unlabel
		if len(self.added_unlabel) == 0:
			self.added_unlabel = new_label
			self.added_unlabel_class = new_label_class
		else:
			self.added_unlabel = np.append(self.added_unlabel,new_label,axis=0)
			self.added_unlabel_class = np.append(self.added_unlabel_class,new_label_class,axis=0)
		print ('added datas=',len(self.added_unlabel_class))
		print ('add ',len(new_label),' datas')
		return len(self.added_unlabel_class)
	def fit_unlabel(self,nb_epoch):
		if len(self.added_unlabel)==0:
			return
		self.datagen.fit(self.added_unlabel)
		print('self.X_test.shape=',self.X_test.shape)
		self.history.append(self.model.fit_generator(self.datagen.flow(self.added_unlabel, self.added_unlabel_class,
		                    batch_size=50),
		                    samples_per_epoch=self.added_unlabel.shape[0],
		                    nb_epoch=nb_epoch,
		                    validation_data=(self.X_test, self.Y_test)).history)


all_label=np.array( pickle.load(open(sys.argv[1]+"all_label.p", "rb")) )
all_label=np.reshape( all_label, (5000,3,32,32) ).astype('float32')/255
all_label_class=to_categorical(np.arange(5000)//(500))


all_unlabel=np.array( pickle.load(open(sys.argv[1]+"all_unlabel.p", "rb")) )
all_unlabel=np.reshape( all_unlabel, (45000,3,32,32)).astype('float32')/255
all_unlabel=all_unlabel[:,:,:,:]
test=pickle.load(open(sys.argv[1]+"test.p", "rb"))
test=np.reshape( np.array(test['data']) , (10000,3,32,32)).astype('float32')
all_unlabel=np.append(all_unlabel,test,axis=0)




# id=0
cnn = CNN()
cnn.init_datas( all_unlabel, all_label , all_label_class )
load=0
if load==1:
	cnn.load('data/cnn_last40times')

cnn.fit(40)
# cnn.save('data/cnn_last40times', 'data/cnn_history')

for i in range(2):
	cnn.add_unlabel()
	for j in range(2):
		cnn.fit_unlabel(1)
		cnn.fit(2)
cnn.save(sys.argv[2],'data/cnn_history2')












