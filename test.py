#%%
import pandas as pd

df = pd.read_csv('./bank-additional-full.csv')
#%%
df.drop(df.select_dtypes('object').columns, axis=1, inplace=True)

#%%
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
result = pca.fit_transform(df)
#%%
df['x'] = result[:,1]
df['y'] = result[:,0]
