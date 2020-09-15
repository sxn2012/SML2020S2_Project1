# -*- coding: utf-8 -*-
"""SML models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/162RiBtcvbbZ-PxaKAkwN4p6lUKFl3Ku9

- Read Data
"""

import os
import codecs
def readfile(filename):
	current_path=os.path.abspath(os.curdir)
	file_path=os.path.join(current_path,filename)
	if not os.path.exists(file_path):
		print("error:file not found:"+filename)
		return ""
	f=codecs.open(file_path,"r","utf-8")
	s=f.read()
	f.close()
	return s

train_data=readfile("train.csv")
test_data=readfile("test.csv")

"""- Data Transforming"""

data_train=[]
label_train=[]
temp_list=train_data.splitlines()
del temp_list[0]
for item in temp_list:
  temp=item.split(",")
  data_train.append([float(temp[0]),float(temp[1]),float(temp[2])])
  label_train.append(int(temp[3]))
data_test=[]
temp_list=test_data.splitlines()
del temp_list[0]
for item in temp_list:
  temp=item.split(",")
  data_test.append([float(temp[0]),float(temp[1]),float(temp[2])])

print(len(data_train))
print(len(label_train))
print(len(data_test))

print(data_train[0:20])
print(label_train[0:20])
print(data_train[30000:30020])
print(label_train[30000:30020])
print(data_test[0:100])

from sklearn.model_selection import train_test_split
X_train, X_dev, Y_train, Y_dev = train_test_split(data_train, label_train, test_size=0.3, random_state=0)

"""- Fully Connected NN"""

# def AUC(yTrue, yPred):
#     import tensorflow as tf
#     auc = tf.metrics.auc(yTrue, yPred)
#     return auc[0]
import tensorflow as tf
from tensorboard.plugins.hparams import api
from keras import models as md
from keras import layers as lr
import numpy as np

model = md.Sequential()
model.add(lr.Dense(128,activation="relu"))
model.add(lr.Dense(4,activation="relu"))
model.add(lr.Dense(32,activation="relu"))
model.add(lr.Dense(1,activation="sigmoid"))
model.compile(optimizer="adam",loss="binary_crossentropy",metrics=["accuracy"])#compile the model
model.fit(X_train, Y_train, epochs=4, batch_size=16)#fit the model

loss, acc = model.evaluate(X_dev, Y_dev)
print(loss,acc)

Y_test=model.predict(data_test).tolist()
print(len(Y_test))

current_path=os.path.abspath(os.curdir)
file_path=os.path.join(current_path,"output.csv")
f=codecs.open(file_path,"w","utf-8")
f.write("Id,Predicted\n")
for i in range(0,len(Y_test)):
  f.write(str(i+1)+","+str(Y_test[i][0])+"\n")
f.close()
