import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
import matplotlib.pyplot as plt
import ptitprince as pt
warnings.filterwarnings("ignore")
import seaborn as sns
import scipy.stats as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

containers=pd.read_csv("C:\Users\AniPole\Downloads\containers.csv")
wms=pd.read_csv("C:\Users\AniPole\Downloads\wms_data.csv")
dataset=pd.read_csv("C:\Users\AniPole\Downloads\dataset_filtered_by_cluster_oct.csv")


wms_columns=['container_code', 'date_added', 'dpo_cbm', 'quantity', 'weight']
wms=wms[wms_columns]

data_merged=containers.merge(wms, left_on=['code', 'date_added'], right_on=['container_code', 'date_added'])

cont_col=['container_id', 'code', 'cbm', 'kg', 'cartons', 'content_class', 'date_added', 'dpo_cbm', 'quantity', 'weight']
data_merged=data_merged[cont_col]

data_merged=data_merged[data_merged['code'].isin(dataset.code.unique())]
dataset=dataset[dataset['code'].isin(data_merged.code.unique())]

data_merged['avg_dpo_cbm']=data_merged['dpo_cbm']/data_merged['quantity']
data_merged['avg_weight_split']=data_merged['weight']/data_merged['quantity']

dataset['vol_var']=-1
dataset['weight_var']=-1
dataset['vol_var_cross']=-1
dataset['weight_var_cross']=-1

for code in data_merged.code.unique():
    # restric the data to the specific code and calculate the total vol, avg_vol_box, avg_weight_box
    b = data_merged[data_merged['code'] == code]
    tot_vol = b['dpo_cbm'].sum()
    vol_mean = tot_vol / b['quantity'].sum()
    weight_mean = b['weight'].sum() / b['quantity'].sum()

    # calculate the variance of the volum
    tot_vol_var = 0
    for i in range(len(b)):
        tot_vol_var = (b.iloc[i]['dpo_cbm'] / tot_vol) * ((b.iloc[i]['avg_dpo_cbm'] - vol_mean) ** 2) + tot_vol_var
    dataset['vol_var'][dataset['code'] == code] = tot_vol_var
    dataset['vol_var_cross'][dataset['code'] == code] = tot_vol_var * vol_mean

    # calculate the variance of the weight
    tot_weight_var = 0
    for i in range(len(b)):
        tot_weight_var = (b.iloc[i]['dpo_cbm'] / tot_vol) * (
                    (b.iloc[i]['avg_weight_split'] - weight_mean) ** 2) + tot_weight_var
    dataset['weight_var'][dataset['code'] == code] = tot_weight_var
    dataset['weight_var_cross'][dataset['code'] == code] = tot_weight_var * weight_mean

dataset[['vol_var','weight_var', 'vol_var_cross', 'weight_var_cross']].describe()
x='ca behet kshu'