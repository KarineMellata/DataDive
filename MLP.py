
# coding: utf-8

# In[17]:


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


print("We here")
time1 = time.clock()
x_dataset = pd.read_csv("bitcoin_dataset.csv", delimiter=",", dtype=str, header=0, usecols=["Date"]).values
y_dataset = pd.read_csv("bitcoin_dataset.csv", delimiter=",", dtype=str, header=0, usecols=["dervative"]).values
date_headlines = pd.read_csv("abcnews-date-text.csv", delimiter=",", dtype=str, header=0, usecols=["publish_date"]).values
text_headlines = pd.read_csv("abcnews-date-text.csv", delimiter=",", dtype=str, header=0, usecols=["headline_text"]).values
time2 = time.clock()
print("Loading training set inputs took " + str(time2-time1) + " seconds")

x_dataset = x_dataset.tolist()
y_dataset = y_dataset.tolist()
date_headlines = date_headlines.tolist()
text_headlines = text_headlines.tolist()


# In[ ]:


for i in range(len(x_dataset)):
    string = str(x_dataset[i])
    string = string.replace("-","")
    x_dataset[i] = string[2:10]


# In[ ]:


for j in range(len(date_headlines)):
    string = str(date_headlines[j])
    string = string.replace("'","")
    string = string.replace("[","")
    string = string.replace("]","")
    date_headlines[j] = string
print(date_headlines[0])


# In[6]:


for k in range(len(text_headlines)):
    string = str(text_headlines[k])
    string = string.replace("'","")
    string = string.replace("[","")
    string = string.replace("]","")
    text_headlines[k] = string
print(text_headlines[0])


# In[7]:


j = 0
time1 = time.clock()
for f in x_dataset:
    stuff = ' '
    i = 0
    for m in date_headlines:
        if (m == f):
            stuff += text_headlines[i]
            stuff += ' '
        i = i + 1
    x_dataset[j] = stuff
    j = j + 1
time2 = time.clock()
print("Loading this took " + str(time2-time1) + " seconds")


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
        print(2)
    #Low 
    if(y_dataset[r] < 2.50 and y_dataset[r] >= 0.53):
        y_dataset[r] = 3
        print(3)
    if(y_dataset[r] >= 2.50):
        y_dataset[r] = 4
        print(4)
    if(y_dataset[r] <= -1.91):
        y_dataset[r] = 0
        print(0)
    if(y_dataset[r] <= -0.33 and y_dataset[r] > -1.91):
        y_dataset[r] = 1
        print(1)


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
tfidf_result = vectorizer.fit_transform(x_dataset_try)


# In[12]:


print(y_dataset[7] == 4)
print(y_dataset[45])
print(len(y_dataset))


# In[13]:


n = 0
j = 0
for i in range(len(y_dataset)):
    if(y_dataset[j] == 3):
        n = n + 1
    j = j + 1
print(n)


# In[14]:


from sklearn.neural_network import MLPClassifier
MLP = MLPClassifier(random_state=1, max_iter=1000, learning_rate='adaptive')
X_train, X_test, y_train, y_test = train_test_split(tfidf_result, y_dataset, train_size=0.7, test_size=0.3)


# In[15]:


MLP.fit(X_train,y_train)
score = MLP.score(X_test,y_test) * 100
print("Test score: %.4f" % score)


# In[16]:


xtfidf2 = vectorizer.transform(np.array(['australia crisis senate concern problem high rates']))
MLP.predict(xtfidf2)

