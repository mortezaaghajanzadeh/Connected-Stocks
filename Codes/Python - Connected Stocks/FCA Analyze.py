#%%
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import seaborn as sns
import re as ree
import numpy as np

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"


# %%

n2 = path + "MonthlyNormalzedFCAP7.2" + ".csv"
df2 = pd.read_csv(n2)
print("n2 Done")

timeId = pd.read_csv(path + "timeId.csv")
#%%
df2['pairType'] = 'Hybrrid'

df2.loc[(df2.GRank_x>=5)&(df2.GRank_y>=5),'pairType'] = 'Big'
df2.loc[(df2.GRank_x<5)&(df2.GRank_y<5),'pairType'] = 'Small'



#%%

fig = plt.figure(figsize=(8, 4))

g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA")

time = timeId.drop_duplicates(subset=["t_Month"], keep="last")[["date", "t_Month"]]
time["date"] = round(time.date / 100).astype(int)
time
labels = time.date.to_list()
tickvalues = time.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
pathS = r"D:\Dropbox\Connected Stocks\Final Report"

plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
fig.set_rasterized(True)
plt.savefig(pathS + "\\FCAtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\FCAtimeSeries.png", bbox_inches="tight")
#%%
fig = plt.figure(figsize=(8, 4))

g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA"
                 ,hue='pairType')

time = timeId.drop_duplicates(subset=["t_Month"], keep="last")[["date", "t_Month"]]
time["date"] = round(time.date / 100).astype(int)
time
labels = time.date.to_list()
tickvalues = time.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
pathS = r"D:\Dropbox\Connected Stocks\Final Report"

plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
fig.set_rasterized(True)
plt.savefig(pathS + "\\FCAtimeSeriesPairType.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\FCAtimeSeriesPairType.png", bbox_inches="tight")



#%%
ar = df2.groupby(['t_Month','sBgroup']).MonthlyFCA.mean().to_frame().reset_index()

ar = ar[ar.sBgroup == 1].merge(ar[ar.sBgroup == 0],on = 't_Month')
ar.plot.area(
    y=["MonthlyFCA_y", "MonthlyFCA_x"], figsize=(15, 8), stacked=True
)