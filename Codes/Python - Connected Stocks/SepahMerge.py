#%%
import pandas as pd
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
df = pd.read_parquet(path+"MonthlyNormalzedFCAP9.2.parquet")
# %%
bg1 = pd.read_csv(path + "BGId.csv")
bg1
#%%
bg = pd.read_csv(path + "SId.csv")
bg
# %%
mlist = ['وانصار', 
 'وقوام',
 'حکمت',
 '',
 '',
 '',]
bg[bg.symbol.isin(mlist)]
# %%
df[df.id_x == 127][['Year_Month','Monthlyρ_5',
 'Monthlyρ_6',
 'Monthlyρ_5Lag',
 'Monthlyρ_turn',]]