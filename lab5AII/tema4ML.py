#Ex1
import pandas as pd
from scipy.stats import entropy
X = pd.DataFrame({'X1': [1, 1, 1, 1, 0, 0],
                  'X2': [1, 1, 1, 0, 0, 0]})
Y = pd.Series([1, 1, 2, 3, 2, 3])


P_totala = [1/3]*3
H_totala = entropy(P_totala, base = 2)

P_X1_0 = [0, 1/2, 1/2]
H_X1_0 = entropy(P_X1_0, base = 2)

P_X1_1 = [1/2, 1/4, 1/4]
H_X1_1 = entropy(P_X1_1, base = 2)

prob0 = 1/3
prob1 = 2/3

H_X1_Y = prob0 * H_X1_0 + prob1 * H_X1_1
IG_X1_Y = H_totala - H_X1_Y

print("Castig informatie IG_X1: ", IG_X1_Y)



P_X2_0 = [0, 1/3, 2/3]
H_X2_0 = entropy(P_X2_0, base = 2)

P_X2_1 = [2/3, 1/3, 0]
H_X2_1 = entropy(P_X2_1, base = 2)

prob0_2 = 1/3
prob1_2 = 2/3

H_X2_Y = prob0_2 * H_X2_0 + prob1_2 * H_X2_1
IG_X2_Y = H_totala - H_X2_Y

print("Castig informatie IG_X2: ", IG_X2_Y)

if IG_X1_Y > IG_X2_Y:
    print("Castig informatie IG_X1 mai mare decat Castig informatie IG_X2")
else:
    print("Castig informatie IG_X2 mai mare decat Castig informatie IG_X1")


#Obs: Pct 3 pe foaie


#Exercitiu 4
import pandas as pd
import itertools
from sklearn.preprocessing import OneHotEncoder
from tools.pd_helpers import apply_counts
exoplanets = pd.DataFrame([
  ('Big', 'Near', 'Yes', 20),
  ('Big', 'Far', 'Yes', 170),
  ('Small', 'Near', 'Yes', 139),
  ('Small', 'Far', 'Yes', 45),
  ('Big', 'Near', 'No', 130),
  ('Big', 'Far', 'No', 30),
  ('Small', 'Near', 'No', 11),
  ('Small', 'Far', 'No', 255)
],
columns=['Big', 'Orbit', 'Habitable', 'Count'])
exoplanets = apply_counts(exoplanets, 'Count')


X = exoplanets[['Size', 'Orbit']]
encoder = OneHotEncoder(sparse=False).fit(X)
X_final = pd.DataFrame(encoder.transform(X), columns=list(itertools.chain.from_iterable(encoder.categories_)))


from sklearn import tree
import matplotlib.pyplot as plt
Y = exoplanets['Habitable']
dt = tree.DecisionTreeClassifier(criterion='entropy').fit(X_final,Y)
print(dt.score(X_final,Y))
fig, ax = plt.subplots(figsize=(5,6))
figure = tree.plot_tree(dt, ax=ax, fontsize=10, feature_names=X_final.columns)
plt.show()

