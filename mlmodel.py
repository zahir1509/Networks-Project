### ======================================= ###
'''Rishabh Goswami & Zahir Ali
mlmodel.py
Please install dependencies from requirements.txt and look at Readme.md for details.
This file contain an ML model to predict if the message is spam or ham
'''
### ======================================= ###

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import csv


# For colored prompts on the terminal
class terminalColor:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Importing the data file with messages and thier lables
spamData = pd.read_csv("./server/spam.csv")

# Creating features and label variables
x = np.array(spamData["email"])
y = np.array(spamData["label"])

# Counting the vectors
CountVectAlgo = CountVectorizer()

# Fit the spamData
X = CountVectAlgo.fit_transform(x) 

# Split the data and train and test data to find the accuracy of the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Classifying the message into spam or ham
classificationAlgo = MultinomialNB()
classificationAlgo.fit(X_train,y_train)

# Predicting if the message is spam or ham
pred = classificationAlgo.predict(X_test)
accuracyscore = accuracy_score(y_test, pred)


# Pridict single string of text
def pred_Text_Email(text):
    textToPredict = CountVectAlgo.transform([text]).toarray()
    return classificationAlgo.predict(textToPredict)

# predict the messages in the CSV
def pred_CSV_Email():
    messages = []
    print(f"\nReading CSV File...")
    with open('./server/datafile.csv', mode ='r', encoding='utf-8') as f: 
        reader = csv.reader(f) 
        next(f)
        for row in reader:
            messages.append(row[0])
    f.close()

    print(f"Processing data...")
    messagesToPred = CountVectAlgo.transform(messages).toarray()
    pred = classificationAlgo.predict(messagesToPred)
    print("\n========= Prediction ===========")
    print(pred)
    return pred, messages

# Update the CSV with the result
def update_CSV_With_Results(pred, messages):
    print(f"\nUpdating Output File...")
    with open('./server/datafile.csv', "w+", encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f) 
        csv_writer.writerow(['Emails','Results'])
        i = 0
        for word in pred:
            csv_writer.writerow([messages[i],word])
            i+=1

    f.close()