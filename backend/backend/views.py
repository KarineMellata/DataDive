# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

from rest_framework.decorators import api_view

# Create your views here.

# THIS ENTIRE PAGE IS A MESS.
# THIS WAS A HACKATHON PROJECT AND TIME WAS RUNNING SHORT

@api_view(['GET', 'POST'])
def index(request):


	# coding: utf-8

	# In[17]:

	import ast

	dataDict = ast.literal_eval(next(iter(request.POST)))

	# THIS WAS DONE BECAUSE WE WERE RUNNING OUT OF TIME AND
	# COULDN'T FIGURE OUT WHY ALL THE POST DATA WAS BEING STORED
	# IN JUST THE FIRST KEY

	print "THESE ARE THE WORDS: ", dataDict['words']

	import os


	try:
	    import unicodecsv
	except:
	    get_ipython().system(u'pip install unicodecsv')
	    import unicodecsv


	# In[18]:


	try:
	    import numpy
	except:
	    get_ipython().system(u'pip install numpy')
	    import numpy


	# In[19]:


	try:
	    import nltk
	except:
	    get_ipython().system(u'pip install nltk')
	    import nltk


	# In[20]:


	import pandas as pd
	import numpy as np
	import time
	from sklearn.model_selection import cross_val_predict
	from sklearn import linear_model
	import matplotlib.pyplot as plt
	from sklearn.model_selection import train_test_split
	from sklearn.preprocessing import StandardScaler
	from sklearn.feature_extraction.text import TfidfVectorizer


	# In[21]:

	# bitcoinFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),'bitcoin_dataset.csv')
	# abcFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),'abcnews-date-text.csv')


	time1 = time.clock()
#	x_dataset = pd.read_csv('bitcoin_dataset.csv', delimiter=",", dtype=str, header=0, usecols=["Date"]).values
	y_dataset = pd.read_csv('bitcoin_dataset.csv', delimiter=",", dtype=str, header=0, usecols=["dervative"]).values
	date_headlines = pd.read_csv('abcnews-date-text.csv', delimiter=",", dtype=str, header=0, usecols=["publish_date"]).values
	text_headlines = pd.read_csv('abcnews-date-text.csv', delimiter=",", dtype=str, header=0, usecols=["headline_text"]).values
	x_dataset = np.loadtxt("x_dataset.csv", delimiter=",", dtype=str, skiprows=1)
	time2 = time.clock()
	print("Loading training set inputs took " + str(time2-time1) + " seconds")

#	x_dataset = x_dataset.tolist()
	y_dataset = y_dataset.tolist()
	date_headlines = date_headlines.tolist()
	text_headlines = text_headlines.tolist()


	# In[ ]:


	# for i in range(len(x_dataset)):
	#     string = str(x_dataset[i])
	#     string = string.replace("-","")
	#     x_dataset[i] = string[2:10]


	# In[ ]:


	for j in range(len(date_headlines)):
	    string = str(date_headlines[j])
	    string = string.replace("'","")
	    string = string.replace("[","")
	    string = string.replace("]","")
	    date_headlines[j] = string


	# In[6]:


	for k in range(len(text_headlines)):
	    string = str(text_headlines[k])
	    string = string.replace("'","")
	    string = string.replace("[","")
	    string = string.replace("]","")
	    text_headlines[k] = string


	# In[7]:


	# j = 0
	# time1 = time.clock()
	# for f in x_dataset:
	#     stuff = ' '
	#     i = 0
	#     for m in date_headlines:
	#         if (m == f):
	#             stuff += text_headlines[i]
	#             stuff += ' '
	#         i = i + 1
	#     x_dataset[j] = stuff
	#     j = j + 1
	# time2 = time.clock()
	# print("Loading this bullshit took " + str(time2-time1) + " seconds")


	# In[8]:


	y_dataset[0] = 0
	y_dataset[2605] = 0.5
	for r in range(len(y_dataset)):
	    string = str(y_dataset[r])
	    string = string.replace("'","")
	    string = string.replace("[","")
	    string = string.replace("]","")
	    y_dataset[r] = float(string)


	# In[9]:


	for r in range(len(y_dataset)):
	    #Stability
	    if(y_dataset[r] > -0.33 and y_dataset[r] < 0.53):
	        y_dataset[r] = 2
	    #Low 
	    if(y_dataset[r] < 2.50 and y_dataset[r] >= 0.53):
	        y_dataset[r] = 3
	    if(y_dataset[r] >= 2.50):
	        y_dataset[r] = 4
	    if(y_dataset[r] <= -1.91):
	        y_dataset[r] = 0
	    if(y_dataset[r] <= -0.33 and y_dataset[r] > -1.91):
	        y_dataset[r] = 1


	# In[10]:

	def create_vectorizer():
	    # Arguments here are tweaked for working with a particular data set.
	    # All that's really needed is the input argument.
	    return TfidfVectorizer(input='content', max_features=200,
	                           max_df=0.05,
	                           stop_words='english')


	# In[11]:

	x_dataset_try = x_dataset
	vectorizer = create_vectorizer()
	tfidf_result = vectorizer.fit_transform(x_dataset_try.ravel())


	# In[12]:


	# In[13]:


	n = 0
	j = 0
	for i in range(len(y_dataset)):
	    if(y_dataset[j] == 3):
	        n = n + 1
	    j = j + 1


	# In[14]:


	from sklearn.neural_network import MLPClassifier
	MLP = MLPClassifier(random_state=1, max_iter=1000, learning_rate='adaptive')
	X_train, X_test, y_train, y_test = train_test_split(tfidf_result, y_dataset, train_size=0.7, test_size=0.3)


	# In[15]:


	MLP.fit(X_train,y_train)
	score = MLP.score(X_test,y_test) * 100
	inputData = request.POST.get('words')

	# In[16]:

	print("Predicting your query...")
	xtfidf2 = vectorizer.transform(np.array([dataDict['words']]))
	finalOutput = MLP.predict(xtfidf2)

	print "FINAL OUTPUT: ", finalOutput

	finalOutputStr = str(finalOutput[0])

	finalFinalOutput = ""

	if finalOutputStr == "4":
		finalFinalOutput = "High increase"
	if finalOutputStr == "3":
		finalFinalOutput = "Low increase"
	if finalOutputStr == "2":
		finalFinalOutput = "Stable"
	if finalOutputStr == "1":
		finalFinalOutput = "Low decrease"
	if finalOutputStr == "0":
		finalFinalOutput = "High decrease"

	if request.method == 'GET':
		return HttpResponse("this is a get")
	if request.method == 'POST':
		return HttpResponse(str(finalFinalOutput))

	# if request.method == 'GET':
	# 	return HttpResponse("this is a get")
	# if request.method == 'POST':
	# 	return HttpResponse("this was posted: " + request.POST.get('somekey'))