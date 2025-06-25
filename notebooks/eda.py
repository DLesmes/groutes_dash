""" EDA for the visits data """
# %%
import pandas as pd
from datetime import date

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
# %%