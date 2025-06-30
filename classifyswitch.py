import pandas as pd
from sklearn.model_selection import train_test_split

datapath = "prototype3data/data160.csv" # varies with which dataset we use
numpoints = 160 # varies with which dataset we use

# setting number of columns this way gets rid of issue where number of data points
# differed in some readings
columns = [i for i in range(613)] # varies with dataset
data = pd.read_csv(datapath, header=None, usecols=columns) 

# Note: since the data doesn't have headers, just know that the formatting
# of csv files is switchtype,sensor1data1,sensor1data2,...,sensor1datak,sensor2data1,
# ...,sensor2datak,sensor3data1,...,sensor3datak,sensor4data1,sensor4datak

target = data.iloc[:, 0] #target is the first column
features = data.iloc[:, 1:] #features are all the sensor data (all data excluding column 1)

# temporarily setting random_state to 0 to ensure reproducability
train_X, val_X, train_y, val_y = train_test_split(features, target,random_state = 0)


from sklearn.ensemble import RandomForestClassifier

# using random_state=1 to ensure reproducability for now
forest_model = RandomForestClassifier(random_state=1)
forest_model.fit(train_X, train_y)
preds = forest_model.predict(val_X)

correct = [(i == j) for i,j in zip(val_y.values,preds)]
comparison = pd.DataFrame({
    'True': val_y.values,
    'Predicted': preds,
    'Correct': correct
})
print(comparison.to_string(index=False))

numcorrect = correct.count(True)
print(f"{numcorrect} correct out of {len(preds)}")