#from numpy import genfromtxt
import numpy as np
import pandas as pd
#from StringIO import StringIO
import pickle


def load_data():
	#raw_data = genfromtxt('intel_data/Items.csv.csv', delimiter = ',')#, dtype = ["S5","S5"])
	raw_data = pd.read_csv('./sales_month_item.csv').as_matrix()
	print "raw_data.shape = ", raw_data.shape

	raw_data = np.delete(raw_data, 0, axis = 0) # remove top 1 row
	raw_data = np.delete(raw_data, 0, axis = 1) # remove left 1 column
		
	print "raw_data.shape = ", raw_data.shape
	return raw_data

def def_stopwords():
	return ["not", "identified", "unknown", "item", "&"]

def preprocessing():
	data = []
	for i in range(len(raw_data)):
		if raw_data[i] != "Not Identified":
			l = raw_data[i][0]
			#l = "".join([w for w in l if not w.isdigit()])
			l = l.lower()
			l = [w for w in l.split()]
			l = [w for w in l if w not in my_stopwords] 
			
			data.append(l)
			
	print "data.shape = ", len(data)
	return data

def counting():
	dic = {}
	count = 0
	for i in range(len(data)):
		for w in data[i]:
			if w not in dic:
				dic[w] = count
				count += 1
	print "dic.len = ", len(dic)
	# pickle.dump(dic, open("item_to_id_dic", "wb")) 
	return dic

def hot_vector():
	# need to change len(data) to the real input data for the model
	hot = np.zeros([len(data), len(dic)]) # type = int of float?
	for i in range(len(data)):
		for w in data[i]:
			hot[i][dic[w]] = 1
	print hot[:10, :10]
	np.save("hot_vector", hot) 

def output_item(): # sprite zero 12oz can 
	fout = open('item_to_id_list.txt','w')
	for i in range(len(data)):
		for j in range(len(data[i])): 
			fout.write(str(data[i][j]) + " ")
		fout.write("\n")
	fout.close()	

def output(): # xxx 1
	fout = open('item_to_id_list.txt','w')
	for key, value in dic.iteritems():
		fout.write(key + " " + str(value) + "\n")
	fout.close()	

my_stopwords = def_stopwords()
raw_data = load_data()
data = preprocessing()
dic = counting()
hot_vector()
output()
