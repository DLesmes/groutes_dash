""" Script to generate final contracts based on annotatd data"""
# %%
import pandas as pd
from datetime import date
import json

# %% [markdown]
# ## appending annotated jsonl batches to get full annotated data
df_annotated_til_20180219 = pd.read_json('../backend/data/annotations/until_20180219_annotations.jsonl', lines=True)
batches_list = [
    df_annotated_til_20180219
]
df_full_annotations = pd.DataFrame()
for batch in batches_list:
    df_full_annotations = pd.concat([df_full_annotations, batch], ignore_index=True)
df_full_annotations
# %%
df_full_annotations.info()
# %%
# %%
df_full_annotations.describe(include='all').T
# %% [markdown]
# ## generating all visits groutes by day
file = "../backend/data/visitas_business_days_by_day.json"
dict_visits_business_days_by_day = json.load(open(file, 'r'))
dict_visits_business_days_by_day['2018-06-15']
# %% [markdown]
# ## adding the start and end timestamps to the annotations dataframe
df_final_contract = df_full_annotations[df_full_annotations['working']].copy()
df_final_contract.reset_index(inplace=True)
df_final_contract['index'] = df_final_contract.index
df_final_contract['start_timestamp'] = None
df_final_contract['end_timestamp'] = None
df_final_contract
# %%
for _, day in df_final_contract.iterrows():
    date_str = str(day.date.strftime('%Y-%m-%d'))
    df_final_contract.loc[day['index'], 'start_timestamp'] = dict_visits_business_days_by_day[date_str]['data'][int(day.start_point)]['timestamp']
    df_final_contract.loc[day['index'], 'end_timestamp'] = dict_visits_business_days_by_day[date_str]['data'][int(day.end_point)]['timestamp']
# %%
df_final_contract = df_final_contract.drop(columns=['index', 'working', 'start_point', 'end_point', 'total_points'])
df_final_contract
# %% [markdown]
# ## generating final contract
df_final_contract.to_csv('../backend/data/final_contract.csv', index=False)
