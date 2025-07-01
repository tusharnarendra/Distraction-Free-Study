import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import joblib

#Load presaved features and CSV
dataset = pd.read_csv('../results.csv')
X = np.load('../features/features.npy')
y = dataset.iloc[:, -1].values

#Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

#Feature scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Random forest model
classifier = RandomForestClassifier(n_estimators = 100, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

#Generating predictions
y_pred = classifier.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

#Evaluation using confusion matrix and accuracy score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))

#Saving the regression model
joblib.dump(classifier, 'random_forest_model.pkl')
joblib.dump(sc, 'X_scaler.pkl')
