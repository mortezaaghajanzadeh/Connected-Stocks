# %%
import pickle
from ConnectedOwnershipFunctions import *
import time

# %%
def prepare():
    path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
    # path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
    df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")
    df["week_of_year"] = df.week_of_year.astype(int)
    df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
        df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
    )

    df = df[df.jalaliDate < 13990000]
    df = df[df.jalaliDate > 13930000]
    df = df[~df["5_Residual"].isnull()]
    print(len(df))
    df = df[df.volume > 0]
    print(len(df))
    try:
        df = df.drop(columns=["Delta_Trunover"])
    except:
        1 + 2

    df = df.rename(
        columns={
            "4_Residual": "4-Residual",
            "5_Residual": "5-Residual",
            "6_Residual": "6-Residual",
            "2_Residual": "2-Residual",
            "5Lag_Residual": "5Lag-Residual",
            "Delta_TurnOver": "Delta_Trunover",
            "Month_of_year": "month_of_year",
        }
    )
    return df


df = prepare()


#%%
df[df.symbol == "شیراز"].id.iloc[0], df[df.symbol == "خموتور"].id.iloc[0]


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(480)
S_g = gdata.get_group(100)


#%%

AllPair = True

n = time.time()
t1 = FCAPf(S_g, g, AllPair)
print(time.time() - n)


AllPair = False
n = time.time()
t2 = FCAPf(S_g, g, AllPair)
print(time.time() - n)

#%%
len(t1[t1.FCAPf > 0]), len(t2)
#%%
data = pd.DataFrame()
gg = df.groupby(["id"])
counter = 0


def genFile(df, path, g, i):
    S_gg = df.groupby(["id"])
    # data = data.append(S_gg.apply(FCAPf, g=g))
    pickle.dump(
        S_gg.apply(FCAPf, g=g, AllPair=False),
        # parallel,
        open(path + "NormalzedFCAP9.1\\NormalzedFCAP9.1_{}.p".format(i), "wb"),
    )


import functools, multiprocessing
from multiprocessing import Pool, cpu_count
import pandas as pd
import numpy as np
import timeit
import time


#%%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"

for i in list(gg.groups.keys()):
    n = time.time()
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    df = df[df.id > F_id]
    gg = df.groupby(["id"])
    genFile(df, path, g, i)
    print(time.time() - n)

#%%
# All pairs

df = prepare()
data = pd.DataFrame()
gg = df.groupby(["id"])
counter = 0


def genFile(df, path, g, i):
    S_gg = df.groupby(["id"])
    # data = data.append(S_gg.apply(FCAPf, g=g))
    pickle.dump(
        S_gg.apply(FCAPf, g=g, AllPair=True),
        open(
            path
            + "NormalzedFCAP9.1_AllPairs\\NormalzedFCAP9.1_AllPairs_{}.p".format(i),
            "wb",
        ),
    )


threads = {}
for i in list(gg.groups.keys()):
    n = time.time()
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    df = df[df.id > F_id]
    gg = df.groupby(["id"])
    genFile(df, path, g, i)
    print(time.time() - n)


# %%
