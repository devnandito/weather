#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Load modules
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd

# Load dataset
df = pd.read_csv(r"lluvias.csv")

# Split into training data and test data
X = df[['Temp_A','Hum_R','Vel_Viento','Precip']]
y = df['Clasificacion']

# Create training and testing vars, It’s usually around 80/20 or 70/30.
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state=1)

# Now we’ll fit the model on the training data
model = SVC(gamma='auto')
model.fit(X_train, Y_train)

# Make predictions on validation dataset
predictions = model.predict(X_test)


# Pickle model 
pd.to_pickle(model,r'new_model.pickle')

# Unpickle model 
model = pd.read_pickle(r'new_model.pickle') 
# read a pickle pd.read_pickle('model.pkl')

# Take input from user
Temp_A = float(input("Enter Temp_A: "))
Hum_R = float(input("Enter Hum_R: "))
Vel_Viento = float(input("Enter Vel_Viento: "))
Precip = float(input("Enter Precip: "))

result = model.predict([[Temp_A,Hum_R,Vel_Viento,Precip]])  # input must be 2D array
print(result)


# In[ ]:




