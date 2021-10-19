#%%

from multiprocessing import Pool, cpu_count
import multiprocessing 

import pickle
import psutil
from threading import Thread
from ConnectedOwnershipFunctions import *

# %%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"


df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")

df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)

df = df[df.jalaliDate < 14000000]

try:
    df = df.drop(columns=["Delta_Trunover"])
except:
    1 + 2
#%%
df = df.rename(
    columns={
        "4_Residual": "4-Residual",
        "5_Residual": "5-Residual",
        "6_Residual": "6-Residual",
        "2_Residual": "2-Residual",
        "5Lag_Residual": "5Lag-Residual",
        "Delta_TurnOver": "Delta_Trunover",
    }
)
df.head()

# %%
df[df.symbol == "خگستر"].id.iloc[0], df[df.symbol == "خودرو"].id.iloc[0]


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(158)
S_g = gdata.get_group(148)

AllPair = True
FCAPf(S_g, g,AllPair)

# %%


#%%
def applyParallel(dfGrouped,g,AllPair):

    with Pool(cpu_count()-1) as p:
        t = [group for name, group in dfGrouped]
        ret_list = p.map(FCAPf,t , [g] * len(t) , [AllPair]*len(t))
    return pd.concat(ret_list)
S_gg = df.groupby(["id"])
import time
now = time.time() 
t = applyParallel(S_gg,g,AllPair = False)
print(now - time.time() )
now = time.time() 
t2 =  S_gg.apply(FCAPf, g=g,AllPair = False)
print(now - time.time() )
#%%
text = "test"
def harvester(text, case):
    X = case[0]
    text+ str(X)
    

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=6)
    case = ['RAW_DATASET']
    pool.map(harvester(text,case),case, 1)
    pool.close()
    pool.join()


#%%
data = pd.DataFrame()
gg = df.groupby(["id"])
counter = 0
def genFile(df,path,g,i):
    S_gg = df.groupby(["id"])
    # data = data.append(S_gg.apply(FCAPf, g=g))
    pickle.dump(
        S_gg.apply(FCAPf, g=g,AllPair = False),
        open(path + "NormalzedFCAP9.1\\NormalzedFCAP9.1_{}.p".format(i), "wb"),
    )
#%%