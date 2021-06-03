# -*- coding: utf-8 -*-
"""TermProjectMLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ndMYJqRMlY-ZZuqrfdBL7AIkyhBhuiQV
"""

#All the imports for our code
import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

#reading the data
path = '/content/drive/MyDrive/data1.csv'
df = pd.read_csv(path)
df.drop(['Unnamed: 0'], axis=1,inplace=True)
df.head()

df.dropna(inplace=True)#droping null rows

"""Making a Tfidf vectorizer"""

df0 = df.sample(frac=0.01,random_state=101)#Tdif vector of 10% of database at 10k features
X = df0.tweet.values
Y = df0.score.values/4

vector = TfidfVectorizer(max_features=1000,lowercase=False,stop_words='english')
X = vector.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

"""Multi-Layer perceptron"""

clf = MLPClassifier(hidden_layer_sizes=(400),learning_rate_init=0.002, momentum=0.87,max_iter=500)#best performing model

clf.fit(X_train, y_train)

acc_train = accuracy_score(y_train, clf.predict(X_train))
acc_test = accuracy_score(y_test, clf.predict(X_test))

print("Accuracy on training set: "+str(acc_train))
print("Accuracy on testing set: "+str(acc_test))

"""Using FS

Here, we used VarianceThreshold to filter features as we want only the best features and we also want to reduce the calculation cost.

As even at threshold = 0.00001 we have 18000-19000 featuers and they are only repeating only one or two times. It gets worse as we increase the sample size.

Our goal was to select best 5500 - 7500 features for the current sample.
"""

from sklearn.feature_selection import VarianceThreshold
constant_filter = VarianceThreshold(threshold=0)
constant_filter.fit(X)

constant_filter.get_support().sum()

Quasi_fil = VarianceThreshold(threshold=0.0000232)
Quasi_fil.fit(X)

Quasi_fil.get_support().sum()

filtered_x_prc = Quasi_fil.transform(X)

"""Now after doing all that we finally changed our values to an array. It is the most ram consuming part. From this we saw that sample size = 30000 - 50000 is the best."""

x_practice = filtered_x_prc.toarray()

print(x_practice)
print(x_practice.shape)

"""Here we generated a list with index values as 'word_i' where i is 0,1,2,3..... array.shape[1]. These will be useful for futher making a dataframe."""

# for getting dictinory keys

ar = []

for i in range(0,1):
	ar.append([])
 
#print(len(ar))

for i in range(x_practice.shape[1]):
  ar[0].append('word_'+str(i))

print(len(ar[0]))

"""We created a dataframe with our weight list and index_values = ar. We did to make further process easier to understand."""

dataframe = pd.DataFrame(x_practice,columns=ar)

dataframe.head()

dataframe.shape

"""### Linear Discriminant Analysis

From here we will get one value as array.

"""

lda=  LinearDiscriminantAnalysis()
x_ld_prc = lda.fit(x_practice,Y)

x_ld_prc = lda.transform(x_practice)

print(x_ld_prc.shape)

"""Model after LDA and Feature selection"""

X_train, X_test, y_train, y_test = train_test_split(x_ld_prc, Y, test_size=0.2, random_state=42)

clf = MLPClassifier(hidden_layer_sizes=(400),learning_rate_init=0.002, momentum=0.87,max_iter=500)
clf.fit(X_train, y_train)

model_Evaluate(clf)