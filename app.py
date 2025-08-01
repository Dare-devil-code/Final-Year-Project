import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import streamlit as st

# load data
data = pd.read_csv('/creditcard.csv')

# separate legitimate and fraudulent transactions
legit = data[data.Class == 0]
fraud = data[data.Class == 1]

# undersample legitimate transactions to balance the classes
legit_sample = legit.sample(n=len(fraud) , random_state=2)
data = pd.concat([legit_sample , fraud], axis=0)

# split data into training and testing sets
X = data.drop(columns="Class" , axis=1)
Y = data['Class']
X_train , X_test , Y_train , Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

# train logistic regression model
model = LogisticRegression()
model.fit(X_train, Y_train)

# evaluate model performance
train_acc = accuracy_score(model.predict(X_train), Y_train)
test_acc = accuracy_score(model.predict(X_test), Y_test)

# create Streamlit app
st.title("Credit Card Fraud Detection Model")
st.write("Enter the following features to check if the transaction is legitimate or fraudulent: ")

# create input fields for the user to enter feature values
input_df = st.text_input("Input All Features")
input_df_lst = input_df.split(',')
# create a button to submit input and get prediction
submit = st.button("Submit")

if submit:
    # gets input feature values
    features  = np.array(input_df_lst, dtype=np.float64)
    # make prediction
    prediction  = model.predict(features.reshape(1, -1))
    # display result
    if prediction[0] == 0:
        st.write("Legitimate Transaction")
    else:
        st.write("Fraudulent transaction")
