#%%
import pandas as pd

df1 = pd.read_csv('./merging_data/epidemic_deaths_annual_number.csv')
df2 = pd.read_csv('./merging_data/life_expectancy_years.csv')

#%%
pd.merge(
    right=df1,
    left=df2,
    how="inner",
    on="country",
)

#%%
df3 = pd.read_json('./merging_data/attribute.json')
df4 = pd.read_json('./merging_data/calibrated_sensor.json')
df45 = pd.merge(
    right=df3,
    left=df4,
    how="inner",
    on="token",
)

