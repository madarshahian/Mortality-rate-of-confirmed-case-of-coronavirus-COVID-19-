import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import theano as th
from datetime import date,timedelta
last_updated_date = date.today()
delta = timedelta(days=1)
import requests
base_url =  'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
url = base_url+last_updated_date.strftime("%m-%d-%Y")+'.csv'
while requests.get(url).status_code==404:
    last_updated_date-=delta
    url = base_url+last_updated_date.strftime("%m-%d-%Y")+'.csv'
print("last updated file found in %s"%last_updated_date)
past_days = 60
all_data = []

Country = 'Iran'

for day in range(past_days):
    data_date = last_updated_date-timedelta(days=day)
    url = base_url+data_date.strftime("%m-%d-%Y")+'.csv'
    df = pd.read_csv(url,index_col=0,parse_dates=[0])
    if 'Last_Update' in df.columns:
        if 'Country_Region' in df.columns:
            ss = df[df['Country_Region']==Country][['Last_Update','Confirmed','Deaths','Recovered']]
            ss.rename(columns = {'Last_Update':'Date'}, inplace = True)
            ss['Date'] = data_date.strftime("%m-%d")
        else:
            ss = df[df['Country/Region']==Country][['Last_Update','Confirmed','Deaths','Recovered']]
            ss.rename(columns = {'Last_Update':'Date'}, inplace = True)
            ss['Date'] = data_date.strftime("%m-%d")
    else:
         if 'Country_Region' in df.columns:
            ss = df[df['Country_Region']==Country][['Last Update','Confirmed','Deaths','Recovered']]
            ss.rename(columns = {'Last Update':'Date'}, inplace = True)
            ss['Date'] = data_date.strftime("%m-%d")
         else:
            ss = df[df['Country/Region']==Country][['Last Update','Confirmed','Deaths','Recovered']]  
            ss.rename(columns = {'Last Update':'Date'}, inplace = True)
            ss['Date'] = data_date.strftime("%m-%d")
    
    all_data.append(ss)
#%%
df_iran = all_data[0]
for item in all_data[1:]:
    df_iran = pd.concat([item,df_iran])
df_iran.reset_index(drop=True)
#%%
df_iran['Death_diff'] = df_iran['Deaths'].diff().shift(periods=-1)
df_iran['Death_growth'] = df_iran['Death_diff']/df_iran['Deaths'];
fig,ax = plt.subplots(figsize=(30,16))
ax.plot(df_iran['Death_growth'].values*100,'o',ms=12)
ax.plot(df_iran['Death_growth'].values*100,alpha = 0.4,lw = 3)
ax.set_xticks(range(len(df_iran)));
ax.set_xticklabels(df_iran['Date'].values,rotation = 90,fontsize = 24);
ax.tick_params(axis='y', which='major', labelsize=22)
#ax.set_ylabel(r"$100\times(today\_deaths-yesterday\_deaths)/yesterday\_deaths$",fontsize = 24)
ax.set_ylabel(r"$100\times \frac{today\_deaths-yesterday\_deaths}{yesterday\_deaths}$",fontsize = 28)
ax.set_xlabel("Date mm-dd",fontsize = 24)
plt.grid('minor')
#%%
fig,ax = plt.subplots(figsize=(30,16))
ax.plot(df_iran['Confirmed'].values,'bo',ms=12,label = "Confirmed")
ax.plot(df_iran['Confirmed'].values,'b',alpha = 0.4,lw = 3)
ax.plot(df_iran['Deaths'].values,'ro',ms=12,label = "Deaths")
ax.plot(df_iran['Deaths'].values,'r',alpha = 0.4,lw = 3)
ax.plot(df_iran['Recovered'].values,'go',ms=12,label = "Recovered")
ax.plot(df_iran['Recovered'].values,'g',alpha = 0.4,lw = 3)

ax.set_xticks(range(len(df_iran)));
ax.set_xticklabels(df_iran['Date'].values,rotation = 90,fontsize = 24);
ax.tick_params(axis='y', which='major', labelsize=22)
ax.set_ylabel("Counts",fontsize = 24)
ax.set_xlabel("Date mm-dd",fontsize = 24)
plt.title("Repoted data from Johns Hopkins University database for "+Country ,fontsize = 36)
plt.legend(fontsize = 30)