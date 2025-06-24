""" EDA for the visits data """
# %%
import pandas as pd

# %% [markdown]
# ## Load data
df_visits = pd.read_csv('../backend/data/99-visitas_uriel.csv')
df_business_days = pd.read_csv('../backend/data/resultados_uriel_mazabuel.csv') 

# %% [markdown]
# ## visits data
df_visits.info()
# %%
df_visits['timestamp'] = pd.to_datetime(df_visits['timestamp']).dt.tz_localize(None)
df_visits[['latitude','longitude']] = df_visits['point'].str.split(',', expand=True).astype(float)
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
df_business_days['fecha'] = pd.to_datetime(df_business_days['fecha'])
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
# ## Merge visits with business days
df_visits_business_days = df_visits.merge(df_business_days, how='right', left_on='timestamp', right_on='inicio')
# %%
df_visits_business_days
# %% [markdown]
# ## visits with business days data
df_visits_business_days.info()
# %% [markdown]
# ## droping duplicates on visits with business days data
df_visits_business_days.drop_duplicates(subset=['timestamp'], inplace=True)
df_visits_business_days.info()
# %%
df_visits_business_days.describe().T
# %%
df_types_visits_business_days = pd.DataFrame(df_visits_business_days.dtypes)
object_features_visits_business_days = df_types_visits_business_days[df_types_visits_business_days[0] == 'object'].index.to_list()
object_features_visits_business_days
# %%
float_features_visits_business_days = df_types_visits_business_days[df_types_visits_business_days[0] == 'float64'].index.to_list()
float_features_visits_business_days
# %%
date_features_visits_business_days = df_types_visits_business_days[df_types_visits_business_days[0] == 'datetime64[ns]'].index.to_list()
date_features_visits_business_days
# %%
df_visits_business_days[object_features_visits_business_days].describe(include='all').T
# %%
df_visits_business_days.fecha.value_counts()
# %%
df_visits_business_days[df_visits_business_days['fecha'] == '2022-02-12']
# %% [markdown]
# ## Save data
df_visits_business_days.to_csv('../backend/data/visitas_business_days.csv', index=False)
# %%