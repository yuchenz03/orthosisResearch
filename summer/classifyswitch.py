import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# Normalizing the data so that each sensor's readings have a mean of 0
# while preserving relative differences between readings.
def normalizedata(features):
    featurescopy = features.values.copy()
    numsensors = 4

    for idx, row in enumerate(featurescopy):
        for sensor_idx in range(numsensors):
            start = sensor_idx * numpoints
            end = start + numpoints
            sensordata = row[start:end]
            meanval = sensordata.mean()
            featurescopy[idx, start:end] = sensordata - meanval

    return pd.DataFrame(featurescopy, columns=features.columns)

datapath = "prototype3data/data160.csv" # varies with which dataset we use
numpoints = 160 # varies with which dataset we use

# setting number of columns this way gets rid of issue where number of data points
# differed in some readings
columns = [i for i in range(613)] # varies with dataset
rowstouse = (0, 150) # The rows used to train the model

data = pd.read_csv(datapath, header=None, usecols=columns) 
data = data.iloc[rowstouse[0]:rowstouse[1]+1, :]
# Note: since the data doesn't have headers, just know that the formatting
# of csv files is switchtype,sensor1data1,sensor1data2,...,sensor1datak,sensor2data1,
# ...,sensor2datak,sensor3data1,...,sensor3datak,sensor4data1,sensor4datak

target = data.iloc[:, 0] #target is the first column
features = data.iloc[:, 1:] #features are all the sensor data (all data excluding column 1)
features = normalizedata(features) # normalizing the data

# temporarily setting random_state to 0 to ensure reproducability
train_X, val_X, train_y, val_y = train_test_split(features, target,random_state = 0)

import numpy as np


def printresults(preds, val_y):
    correct = [(i == j) for i,j in zip(val_y.values,preds)]
    comparison = pd.DataFrame({
        'Actual': val_y.values,
        'Predicted': preds,
        'Correct': correct
    })
    # uncomment for comparison table
    # print(comparison.to_string(index=False))

    switchidentified = [(i == j) if i == 2 or j == 2 else True for i,j in zip(val_y.values,preds)]
    numcorrect = correct.count(True)
    nonevsswitches = switchidentified.count(True)
    print(f"{numcorrect} correct out of {len(preds)} ({numcorrect/len(preds)*100:.2f}%)")
    print(f"{nonevsswitches} correct out of {len(preds)} considering both switches to be equal ({nonevsswitches/len(preds)*100:.2f}%)")

def randomforestclassifier():
    # using random_state=1 to ensure reproducability for now
    forest_model = RandomForestClassifier(random_state=1)
    forest_model.fit(train_X, train_y)
    preds = forest_model.predict(val_X)
    printresults(preds, val_y)


def logisticregression():
    model = LogisticRegression()

    # Train the model using the training data
    model.fit(train_X, train_y)
    preds = model.predict(val_X)
    printresults(preds, val_y)

def lineardiscriminantanalysis():
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    lda_model = LinearDiscriminantAnalysis()
    lda_model.fit(train_X, train_y)
    preds = lda_model.predict(val_X)
    printresults(preds, val_y)

def supportvectorclassifier():
    from sklearn.svm import SVC
    svc_model = SVC()
    svc_model.fit(train_X, train_y)
    preds = svc_model.predict(val_X)
    printresults(preds, val_y)

def main():
    print("\nRandom Forest Classifier")
    randomforestclassifier()
    print("-----------------------------------------------------------")
    print("\nLogistic Regression")
    logisticregression()
    print("-----------------------------------------------------------")
    print("\nLinear Discrimination Analysis")
    lineardiscriminantanalysis()
    print("-----------------------------------------------------------")
    print("\nSupport Vector")
    supportvectorclassifier()
    print("-----------------------------------------------------------")

if __name__ == "__main__":
    main()