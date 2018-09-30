import pandas as pd
import numpy as np

# SKlearn imports
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import xgboost as xgb

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# remove columns that are constant
remove = []
for col in train.columns:
    if train[col].std() == 0:
        remove.append(col)

train.drop(remove, axis=1, inplace=True)
test.drop(remove, axis=1, inplace=True)

# remove duplicated columns
remove = []
cols = train.columns
for i in range(len(cols)-1):
    v = train[cols[i]].values
    for j in range(i+1, len(cols)):
        if np.array_equal(v, train[cols[j]].values):
            remove.append(cols[j])

train.drop(remove, axis=1, inplace=True)
test.drop(remove, axis=1, inplace=True)

# test_id receives the ID column of the test CSV. It is then dropped from test, of course.
test_id = test.ID
test = test.drop(["ID"],axis=1)

# similarly, we drop both the target, and the ID from training set. Drop TARGET so as to make learning better.
X = train.drop(["TARGET","ID"],axis=1)
y = train.TARGET.values

# similar process to what was done in the entire course so far - split the training into two.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1729)

# Then, we select the features we'll be utilizing to train our model.
clf = ExtraTreesClassifier(random_state=1729)
selector = clf.fit(X_train, y_train)

# selects the most important features we found through the extra tree classifier
fs = SelectFromModel(selector, prefit=True)
print(X_train.shape)
# reduces X_train and X_test to these features only.
X_train = fs.transform(X_train)
X_test = fs.transform(X_test)
test = fs.transform(test)
print(X_train.shape)

# Train Models


# ALL SCORES FROM THE PRIVATE LEADERBOARD.


# XGB model. Private score: 0.819772

XGBmodel = xgb.XGBClassifier(n_estimators=110, nthread=-1, max_depth=4, seed=1729)
XGBmodel.fit(X_train, y_train, eval_metric="auc", verbose=False, eval_set=[(X_test, y_test)])
y_pred = XGBmodel.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionXGB.csv", index=False)

# KNN model. Private Score: 0.563689

KNNmodel = KNeighborsClassifier(n_neighbors=3, weights="distance")
KNNmodel.fit(X_train, y_train)
y_pred = KNNmodel.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionKNN.csv", index=False)

# Bagged KNN. Private Score: 0.661960.

baggedKNN = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5, random_state=38)
baggedKNN.fit(X_train, y_train)
y_pred = baggedKNN.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionBaggedKNN.csv", index=False)

# MLPClassifier. Private Score: 0.535727

MLPCmodel = MLPClassifier(random_state=38)
MLPCmodel.fit(X_train, y_train)
y_pred = MLPCmodel.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionMLPC.csv", index=False)

# MLPclassifier (bagged). Private score: 0.701536

baggedMLPC = BaggingClassifier(MLPClassifier(random_state=38), max_samples=0.5, max_features=0.5, random_state=38)
baggedMLPC.fit(X_train, y_train)
y_pred = baggedMLPC.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionBaggedMLPC.csv", index=False)

# GBClassifier. Private Score: 0.818242

GBCmodel = GradientBoostingClassifier(random_state=38)
GBCmodel.fit(X_train, y_train)
y_pred = GBCmodel.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionGBC.csv", index=False)

# GBClassifier BAGGED. Private Score: 0.776595)

baggedGBC = BaggingClassifier(GradientBoostingClassifier(random_state=38), max_samples=0.5, max_features=0.5,
                             random_state=38)
baggedGBC.fit(X_train, y_train)
y_pred = baggedGBC.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionBaggedGBC.csv", index=False)

# DTClassifier. Private Score: 0.572142

DTCmodel = DecisionTreeClassifier(random_state=38, criterion="entropy")
DTCmodel.fit(X_train, y_train)
y_pred = DTCmodel.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionDTC.csv", index=False)

# DTClassifier BAGGED. Private Score: 0.701126

baggedDTC = BaggingClassifier(DecisionTreeClassifier(random_state=38), max_samples=0.5, max_features=0.5, random_state=38)
baggedDTC.fit(X_train, y_train)
y_pred = baggedDTC.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionBaggedDTC.csv", index=False)

# Ensembling everything (VOTING CLASSIFIER....)
# --------------------------------------------------------------------
# first lets try ensembling with no baggings... Private Score: 0.781657

ensembleVC = VotingClassifier(estimators=[('xgb', XGBmodel), ('knn', KNNmodel), ('mlpc', MLPCmodel), ('gbc', GBCmodel)
                                           ,('dtc', DTCmodel)], voting="soft")
ensembleVC.fit(X_test, y_test)
y_pred = ensembleVC.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionensembleNoBags.csv", index=False)

# ---------------------------------------------------------------------

# now let us ensemble with only baggings... private Score: 0.736600

ensembleVC = VotingClassifier(estimators=[('xgb', XGBmodel), ('knnbag', baggedKNN), ('mlpcbag', baggedMLPC), ('gbcbag', baggedGBC),
                                          ('dcbag', baggedDTC)], voting="soft")
ensembleVC.fit(X_test, y_test)
y_pred = ensembleVC.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionensembleOnlyBags.csv", index=False)

# ---------------------------------------------------------------------

# now, ensembling EVERYTHING... Private Score: 0.763175

ensembleVC = VotingClassifier(estimators=[('xgb', XGBmodel), ('knn', KNNmodel), ('knnbag', baggedKNN),
                                         ('mlpc', MLPCmodel), ('mlpcbag', baggedMLPC), ('gbc', GBCmodel),
                                         ('gbcbag', baggedGBC), ('dtc', DTCmodel), ('dtcbag', baggedDTC)],
                              voting="soft");
ensembleVC.fit(X_test, y_test)
y_pred = ensembleVC.predict_proba(test)
submission = pd.DataFrame({"ID":test_id, "TARGET": y_pred[:, 1]})
submission.to_csv("submissionensembleALL.csv", index=False)
