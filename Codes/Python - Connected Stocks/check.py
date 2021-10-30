#%%
import pandas as pd
path = "E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
# df1 = pd.read_csv(path + "MonthlyNormalzedFCAP9.2.csv")
df2 = pd.read_csv(path + "MonthlyAllPairs_1400_06_28.csv")
# %%


len(df2),len(df2[df2.FCA>0])

#%%
df = df2[df2.FCA>0]
len(df1),len(df1[df1.FCA>0]),len(df)
# %%

def gen_mapingdict(df1):
    return dict(zip(df1['nID'].unique(),range(1,len(df1.nID.unique())+1)))


# %%

df1['nID'] = df1.symbol_x + '-' + df1.symbol_x
df['nID'] = df.symbol_x + '-' + df.symbol_x
mapingdict = gen_mapingdict(df1)

df1['nID'] = df1.nID.map(mapingdict)
df['nID'] = df.nID.map(mapingdict)

# %%
df[df.nID.isnull()][['symbol_x','symbol_y']].drop_duplicates()
#%%
df1.groupby(['nID']).size().to_frame().mean(),df.groupby(['nID']).size().to_frame().mean()

