
import numpy as np
import pandas as pd
# select the vender has max sell log
raw_data = pd.read_csv('./sales_month_item.csv').as_matrix()
raw_data = np.delete(raw_data, 0, axis = 0) # remove top 1 row
raw_data = np.delete(raw_data, 0, axis = 1) # remove left 1 column
data = raw_data
raw_data = raw_data.tolist();
maxCounterVenderID = 0
maxCounter = 0
allVenderID = []
while ( len(raw_data) != 0 ):
	venderID = raw_data[0][2]
	allVenderID.append(venderID)
	counter = 0
	for row in raw_data:
		if ( row[2] == venderID ):
			counter += 1
	if ( counter >= maxCounter ):
		maxCounter = counter
		maxCounterVenderID = venderID
		# [x for x in a if x != 2]
	raw_data = [ r for r in raw_data if r[2] != venderID ]
	print(len(raw_data))
print ("maxCounterVenderID: ", maxCounterVenderID)
print ("maxCounter: ", maxCounter)

dataList = data.tolist()
filtered_data = [ r for r in dataList if r[2] == maxCounterVenderID ]
print ("len(filtered_data): ", len(filtered_data))

# print (data)

raw_data = np.array(filtered_data)[:,10]
print ("len(raw_data): ", len(raw_data))
print (raw_data)

stopwords = ["not", "identified", "unknown", "item", "&"]
def preprocessing(raw):
	data = []
	for i in range(len(raw)):
		l = raw[i]
		l = l.lower()
		l = [w for w in l.split()]
		l = [w for w in l if w not in stopwords] 
		data.append(l)
	return data

def counting(data):
	dic = {}
	count = 0
	for i in range(len(data)):
		for w in data[i]:
			if w not in dic:
				dic[w] = count
				count += 1
	return dic

def hot_vector(data,dic):
	hot = np.zeros([len(data), len(dic)]) # type = int of float?
	for i in range(len(data)):
		for w in data[i]:
			hot[i][dic[w]] = 1
	print hot[:10, :10]
	return hot
data = preprocessing(raw_data)
dic = counting(data)
hot = hot_vector(data,dic)

filtered_data = np.array(filtered_data)
print(filtered_data.shape)
filtered_data = np.delete(filtered_data, 10, axis = 1) # remove col
filtered_data = np.delete(filtered_data, 9, axis = 1) # remove col
filtered_data = np.delete(filtered_data, 8, axis = 1) # remove col
filtered_data = np.delete(filtered_data, 6, axis = 1) # remove col
# filtered_data = np.delete(filtered_data, 2, axis = 1) # remove col
filtered_data = np.delete(filtered_data, 1, axis = 1) # remove col
filtered_data = np.delete(filtered_data, 0, axis = 1) # remove col
for idx in range(filtered_data.shape[0]):
	[year,month] = filtered_data[idx][1].split('-')
	filtered_data[idx][0] = year
	filtered_data[idx][1] = month
filtered_data = np.c_[filtered_data,hot]
print (filtered_data)

from sklearn.svm import SVR
y = np.random.randn(filtered_data[:,3])
filtered_data = np.delete(filtered_data, 4, axis = 1) # remove col
filtered_data = np.delete(filtered_data, 3, axis = 1) # remove col
x = filtered_data
clf = SVR(C=1.0, epsilon=0.2)
x_valid=x[:10]
y_valid=y[:10]
x=x[10:]
y=y[10:]
clf.fit(x, y)
y_predict = clf.predict(x_valid)

# SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.2, gamma='auto',
#     kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
