""" EDA for the visits data """
# %%
import pandas as pd
from datetime import date
import json

# %% [markdown]
# ## Load data
df_visits = pd.read_csv('../backend/data/99-visitas_uriel.csv')
df_business_days = pd.read_csv('../backend/data/resultados_uriel_mazabuel.csv') 

# %% [markdown]
# ## visits data
df_visits.info()
# %%
df_visits['timestamp'] = pd.to_datetime(df_visits['timestamp']).dt.tz_localize(None)
df_visits['date'] = pd.to_datetime(df_visits['timestamp']).dt.date
df_visits[['latitude','longitude']] = df_visits['point'].str.split(',', expand=True).astype(float)
df_visits
# %%
df_visits.info()
# %%
df_visits.head()
# %%
df_visits.describe().T
# %%
df_types_visits = pd.DataFrame(df_visits.dtypes)
object_features_visits = df_types_visits[df_types_visits[0] == 'object'].index.to_list()
object_features_visits
# %%
float_features_visits = df_types_visits[df_types_visits[0] == 'float64'].index.to_list()
float_features_visits
# %%
date_features_visits = df_types_visits[df_types_visits[0] == 'datetime64[ns]'].index.to_list()
date_features_visits
# %%
df_visits[object_features_visits].describe(include='all').T
# %% [markdown]
# ## business days data
df_business_days.info()
# %%
df_business_days['fecha'] = pd.to_datetime(df_business_days['fecha']).dt.date
df_business_days['inicio'] = pd.to_datetime(df_business_days['inicio'])
df_business_days['fin'] = pd.to_datetime(df_business_days['fin'])
# %%
df_business_days.info()
# %%
df_business_days.head()
# %%
df_business_days.describe().T
# %%
df_types_business_days = pd.DataFrame(df_business_days.dtypes)
object_features_business_days = df_types_business_days[df_types_business_days[0] == 'object'].index.to_list()
object_features_business_days
# %%
df_business_days[object_features_business_days].describe(include='all').T
# %% [markdown]
# ## labeling business days
# %%
ind = df_visits[df_visits['date'].isin(df_business_days['fecha'])].index
df_visits.loc[ind,'business_day'] = True
ind = df_visits[df_visits['business_day'].isna()].index
df_visits.loc[ind,'business_day'] = False
df_visits
# %%
df_visits.business_day.value_counts(dropna=False)
# %%
df_visits.info()
# %%
df_visits.describe().T
# %%
df_types_visits = pd.DataFrame(df_visits.dtypes)
object_features_visits = df_types_visits[df_types_visits[0] == 'object'].index.to_list()
object_features_visits
# %%
float_features_visits = df_types_visits[df_types_visits[0] == 'float64'].index.to_list()
float_features_visits
# %%
date_features_visits = df_types_visits[df_types_visits[0] == 'datetime64[ns]'].index.to_list()
date_features_visits
# %%
df_visits[object_features_visits].describe(include='all').T
# %%
df_visits[df_visits['date'] == date(2023, 12, 24)]
# %%
df_visits[df_visits['date'] == date(2023, 12, 24)].place.value_counts()
# %% [markdown]
# ## Save data
df_visits.to_csv('../backend/data/visitas_business_days.csv', index=False)
# %% [markdown]
# ## json visitas business days by day
df_visits['timestamp'] = df_visits['timestamp'].astype(str)
dict_visits_business_days_by_day = {}
for day in df_visits['date'].unique():
    data = df_visits[df_visits['date'] == day][[
            'place',
            'timestamp',
            'latitude',
            'longitude'
        ]].to_dict(orient='records')
    if str(day) == '2014-06-06':
        print(f"Processing day: {day} before removing consecutive duplicates")
        print(f"Data length: {len(data)}")
        print(data)
    # Remove consecutive duplicates based on 'place'
    data_no_consecutive_duplicates = [x for i, x in enumerate(data) if i == 0 or x['place'] != data[i - 1]['place']]
    if str(day) == '2014-06-06':
        print(f"Processing day: {day} after removing consecutive duplicates")
        print(f"Data length: {len(data_no_consecutive_duplicates)}")
        print(data_no_consecutive_duplicates)

    dict_visits_business_days_by_day[str(day)] = {
        "data": data_no_consecutive_duplicates,
        "business_day": any(df_visits[df_visits['date'] == day]['business_day']),
    }
# %%
file = "../backend/data/visitas_business_days_by_day.json"
with open(file, 'w') as f:
    json.dump(dict_visits_business_days_by_day, f, indent=4)
# %%
import json
file = "../backend/data/visitas_business_days_by_day.json"
dict_visits_business_days_by_day = json.load(open(file, 'r'))
dict_visits_business_days_by_day_sample = {k: v for k, v in dict_visits_business_days_by_day.items() if k < '2014-06-15'}
dict_visits_business_days_by_day_sample
# %%
file = "../backend/data/visitas_business_days_by_day_sample.json"
with open(file, 'w') as f:
    json.dump(dict_visits_business_days_by_day_sample, f, indent=4)
# %%
