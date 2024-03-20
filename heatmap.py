import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


data = pd.read_csv('data/detailed_results_c_12_20_2022-12_29_00.csv')

mapping = {'basic materials':0, 'consumer discretionary':1, 'consumer staples':2,
           'energy':3, 'financials':4, 'health care':5, 'industrials':6, 
           'real estate':7, 'technology':8, 'telecommunications':9, 'utilities':10}

#data['Industry cat']=data['FTSE industry'].replace(mapping)
data['Industry cat']=data['FTSE industry']
print(data.head())


data['rank_2019'] = pd.qcut(data['2019'],5, labels=[0, 1, 2, 3, 4])
data['rank_2020'] = pd.qcut(data['2020'],5, labels=[0, 1, 2, 3, 4])
data['rank_2021'] = pd.qcut(data['2021'],5, labels=[0, 1, 2, 3, 4])

data_s_m = data.drop(columns=['Unnamed: 0','Company','Company_name','FTSE industry','change'])

data_s2 = data_s_m.sort_values(by='Industry cat').reset_index(drop=True)
data_s2['Industry cat'] = data_s2['Industry cat'].str.title()



##########################
##########################
data_melted = data_s2.melt(id_vars=['Industry cat'], value_vars=['2019', '2020', '2021'], var_name='Year', value_name='Rank')
data_melted = data_melted.reset_index(drop=True)

df = pd.DataFrame()
df['Year'] = np.array(data_melted['Year'])
df['Industry'] = np.array(data_melted['Industry cat'])
df['rank'] = np.array(data_melted['Rank'])

heatmap_data = df.drop_duplicates(['Industry', 'Year']).pivot(index='Year', columns='Industry', values='rank')

plt.figure(figsize=(12, 6))
ax = sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt=".2f")

ax.invert_yaxis()
plt.xticks(rotation=45, ha="right")

plt.show()

##########################
##########################
data_melted2 = data_s2.melt(id_vars=['Industry cat'], value_vars=['rank_2019', 'rank_2020', 'rank_2021'], var_name='Year', value_name='Rank')
data_melted2 = data_melted2.reset_index(drop=True)

#save data_melted2 to csv
#data_melted2.to_csv('data/heatmap_data.csv')
