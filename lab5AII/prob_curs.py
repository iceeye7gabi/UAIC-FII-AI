import itertools

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from tools.pd_helpers import apply_counts
from sklearn.naive_bayes import BernoulliNB


tennis = pd.DataFrame([
    ('Sunny', 'Hot', 'High', 'Weak', 'No', 1),
    ('Sunny', 'Hot', 'High', 'Strong', 'No', 1),
    ('Overcast', 'Hot', 'High', 'Weak', 'Yes', 1),
    ('Rain', 'Mild', 'High', 'Weak', 'Yes', 1),
    ('Rain', 'Cool', 'Normal', 'Weak', 'Yes', 1),
    ('Rain', 'Cool', 'Normal', 'Strong', 'No', 1),
    ('Overcast', 'Cool', 'Normal', 'Strong', 'Yes', 1),
    ('Sunny', 'Mild', 'High', 'Weak', 'No', 1),
    ('Sunny', 'Cool', 'Normal', 'Weak', 'Yes', 1),
    ('Rain', 'Mild', 'Normal', 'Weak', 'Yes', 1),
    ('Sunny', 'Mild', 'Normal', 'Strong', 'Yes', 1),
    ('Overcast', 'Mild', 'High', 'Strong', 'Yes', 1),
    ('Overcast', 'Hot', 'Normal', 'Weak', 'Yes', 1),
    ('Rain', 'Mild', 'High', 'Strong', 'No', 1)
],
    columns=['Outlook', 'Temperature', 'Humidity', 'Wind', 'EnjoyTennis', 'Count'])

tennis = apply_counts(tennis, 'Count')
tennis

X_features = tennis[['Outlook', 'Temperature', 'Humidity', 'Wind']]
encoder = OneHotEncoder(sparse=False).fit(X_features)
X_transformed = pd.DataFrame(encoder.transform(X_features),
                             columns=list(itertools.chain.from_iterable(encoder.categories_)))

print(X_transformed)


from sklearn import tree
import matplotlib.pyplot as plt
Y = tennis['EnjoyTennis']
dt = tree.DecisionTreeClassifier(criterion='entropy').fit(X_transformed,Y)
fig, ax = plt.subplots(figsize=(7,8))
f = tree.plot_tree(dt, ax=ax, fontsize=10, feature_names=X_transformed.columns)
plt.show()

print("Acuratetea la antrenare ID3: ", dt.score(X_transformed, Y))
print("Eroarea la antrenare ID3: ", 1 - dt.score(X_transformed, Y))

from sklearn.model_selection import LeaveOneOut
loo = LeaveOneOut()
scores = cross_val_score(dt, X_transformed, Y, cv=loo)
print("CVLOO scores ID3:", scores)
print("Acuratetea la CVLOO ID3: ", mean(scores))
print("Eroarea la CVLOO ID3: ", 1 - mean(scores))

from sklearn.naive_bayes import BernoulliNB

cl = BernoulliNB().fit(X_transformed, Y)
print("Acuratetea la antrenare NaiveBayes: " , cl.score(X_transformed, Y))
print("Eroarea la antrenare NaiveBayes: " , 1 - cl.score(X_transformed, Y))


from sklearn.model_selection import LeaveOneOut, cross_val_score
from statistics import mean
loo = LeaveOneOut()
scores = cross_val_score(cl, X_transformed, Y, cv=loo)
print("CVLOO scores NaiveBayes:", scores)
print("Acuratetea la CVLOO NaiveBayes: ", mean(scores))
print("Eroarea la CVLOO NaiveBayes: ", 1 - mean(scores))
