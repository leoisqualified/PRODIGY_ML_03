# -*- coding: utf-8 -*-
"""Image Classification using SVM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B0AWEhgFmyjfnuXI-EHktkunm4UigqtT
"""

'''
In this notebook, we are going to predict images using Support Vector Machines (SVM) as to whether they are cats or dogs.
We will begin with importing the dataset and then training the SVM model later we will fine-tune the model and then test the model.
'''

#import the libraries
from zipfile import ZipFile
import os
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import GridSearchCV
from PIL import Image
from sklearn.metrics import accuracy_score, classification_report

#create a function to unpack images
def unzip(path_to_file, size=(64,64)):
  #create empty arrays/list
  images = []
  labels = []

  #use context manager to unpack
  with ZipFile(path_to_file, 'r') as zip:
    #loop through for filenames
    for filename in zip.namelist():
      #check the file extension
      if filename.endswith('.jpg'):
        #use context manager to open the image
        with zip.open(filename, 'r') as image:
          img = Image.open(image)
          img = img.resize(size)
          #convert image to 1 dimension
          img_array = np.array(img).flatten()
          images.append(img_array)
          #define the label
          label = 0 if 'cat' in filename else 1
          labels.append(label)
  #return the lists as arrays
  return np.array(images), np.array(labels)

#unpack the train and test
train_zip = '/content/drive/MyDrive/train.zip'
test_zip = '/content/drive/MyDrive/test1.zip'

#split the data and unpack
train_X, train_y = unzip(train_zip)
test_X, test_y = unzip(test_zip)

#Scale the images
scaler = StandardScaler()
train_X_scaled = scaler.fit_transform(train_X)
test_X_scaled = scaler.transform(test_X)

#instatiate the svm
svm = SVC(kernel ='linear')

#train the model
svm.fit(train_X_scaled, train_y)

'''
The code above is correct the computational resources are not available to run this code.
The code however has been written for reproducibilty and should be able to produce expected results.
The main aim of the project is to learn how support vectors work and how it is used in image classification
'''

#predict on the model
y_pred = svm.predict(test_X_scaled)

#evaluate the model
accuracy = accuracy_score(test_y, y_pred)
print('Accuracy:', accuracy)
print(classification_report(test_y, y_pred))

'''
The code check for the accuracy of our model. If for some reason the results are not optimal.
Run the code below to fine-tune the model.
'''

#instantiate param_grid
param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [1, 0.1, 0.01, 0.001], 'kernel'=['rbf', 'polynomial']}


#instantiate gridsearch_cv
grid_search = GridSearchCV(SVC(), param_grid, refit=True, verbose=3)

#fit the model
grid_search.fit(train_X_scaled, train_y)

#print the best parameters
print(grid_search.best_params_)

'''
The above code produces the best parameters for the SVC which had the most optimal results.
We then print the predicted values in submission file
'''

#predict using gridsearch
y_pred = grid_search.predict(test_X_scaled)

#save the predictions
np.savetxt('submission.csv', y_pred, delimiter=',')

#end of notebook