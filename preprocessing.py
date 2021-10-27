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
df.Income = df.Income.apply(lambda x: (x-df.Income.min())/(df.Income.max()-df.Income.min()))

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