# %%
import datetime

import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

# %%

df = pd.read_csv('./data/marketing_campaign.csv', sep='\t')
df['age'] = 2021 - df.Year_Birth
df.Education = df.Education.map({'Basic': 1, '2n Cycle': 2, 'Graduation': 3, 'Master': 4, 'PhD': 5})
df.Income[df.Income > 600000] = None
df.Dt_Customer = (datetime.datetime.now() - pd.to_datetime(df.Dt_Customer)).dt.days
df = df.drop(['ID', 'Year_Birth', 'Z_CostContact', 'Z_Revenue'], axis=1)

aggregate_vols = [
    'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
    'MntSweetProducts', 'MntGoldProds'
]

campaign_cols = [
    'AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3',
    'AcceptedCmp4', 'AcceptedCmp5', 'Response']

binary_cols = campaign_cols + [
    'Complain'
]

categorical = [
    'Marital_Status',
]

not_categorical = list(set(df.columns) - set(categorical))
df[not_categorical] = df[not_categorical].fillna(df[not_categorical].mean())
df[categorical] = df[categorical].fillna(df[not_categorical].median())

# %%
import json

profile = ProfileReport(df)
profile_json = json.loads(profile.to_json())
profile.to_file("output.html")

# %%
from sklearn.cluster import AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score


model = AgglomerativeClustering(n_clusters=50)
# model = DBSCAN()
ndf = pd.get_dummies(df)
ndf = ndf.drop(campaign_cols, axis=1)
ndf = ndf.drop(aggregate_vols, axis=1)
prediction = model.fit_predict(ndf)
print(silhouette_score(ndf, prediction))

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
pca = TSNE(n_components=2)
pca_df = pd.DataFrame(pca.fit_transform(ndf))
pca_df['cluster'] = prediction

#%%
import plotly.express as px
fig = px.scatter(pca_df, x=0, y=1, color='cluster', )
fig.show()


#%%
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

model = RandomForestRegressor()

cols = list(df.columns[:7]) + ['age', 'Complain', 'Response']
ndf = df[cols]
d_ndf = pd.get_dummies(ndf)
# MntWines: Amount spent on wine in last 2 years
# MntFruits: Amount spent on fruits in last 2 years
# MntMeatProducts: Amount spent on meat in last 2 years
# MntFishProducts: Amount spent on fish in last 2 years
# MntSweetProducts: Amount spent on sweets in last 2 years
# MntGoldProds: Amount spent on gold in last 2 years
X_train, X_test, y_train, y_test = train_test_split(d_ndf, df.MntWines, test_size=0.33, random_state=42)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
# plot_tree(model)
# plt.savefig("mygraph.png", dpi=600)


#%%
# df.columns[:7]

#%%
# from matplotlib import pyplot as plt
# from scipy.cluster.hierarchy import dendrogram, linkage
#
# linked = linkage(ndf, 'single')
#
# labelList = range(1, 11)
#
# plt.figure(figsize=(10, 7))
# dendrogram(linked,
#             orientation='top',
#             # labels=labelList,
#             distance_sort='descending',
#             show_leaf_counts=True)
#
# plt.savefig("mygraph.png", dpi=300)
