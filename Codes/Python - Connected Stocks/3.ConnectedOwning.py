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

# %%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")
df["week_of_year"] = df.week_of_year.astype(int)
df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)
df[df.jalaliDate >13980200].groupby(["year_of_year", "Month_of_year"]).size()
#%%
df = df[df.jalaliDate < 13990000]

df = df[df.jalaliDate > 13930000]
df[df.jalaliDate >13980200].groupby(["year_of_year", "Month_of_year"]).size()
#%%

# df = df[~df["5_Residual"].isnull()]
print(len(df))
df[df.jalaliDate >13980200][['5_Residual','jalaliDate']]

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
g = gdata.get_group(480)
S_g = gdata.get_group(100)
intersection = list(set.intersection(set(S_g.date), set(g.date)))
f = Calculation(g, S_g, intersection, AllPair)
name1 = g.symbol.iloc[0]
name2 = S_g.symbol.iloc[0]
g = g[(g.date.isin(intersection)) & (g.Holder == name2)][["date", "Percent"]]
S_g = S_g[S_g.date.isin(intersection) & (S_g.Holder == name1)][["date", "Percent"]]
t = g.merge(S_g, on=["date"], how="outer")
t["MaxCommon"] = t[["Percent_x", "Percent_y"]].max(1)
mapdict = dict(zip(t.date, t.MaxCommon))
f["CrossOwnership"] = f["date"].map(mapdict).fillna(0)
#%%
f[f.jalaliDate >13980200].groupby(["year_of_year", "month_of_year"]).size()


#%%
fc = (
    f.groupby(["year_of_year", "month_of_year"])[
        [
            "2-Residual_x",
            "2-Residual_y",
            "4-Residual_x",
            "4-Residual_y",
            "5-Residual_x",
            "5-Residual_y",
            "6-Residual_x",
            "6-Residual_y",
            "5Lag-Residual_x",
            "5Lag-Residual_y",
            "Delta_Trunover_x",
            "Delta_Trunover_y",
            "Delta_Amihud_x",
            "Delta_Amihud_y",
            "Residual_Bench_x",
            "Residual_Bench_y",
        ]
    ]
    .corr(min_periods=0)
    .reset_index()
)

for i in [
    "2-Residual",
    "4-Residual",
    "5-Residual",
    "6-Residual",
    "5Lag-Residual",
    "Residual_Bench",
    ]:
    cor = fc.loc[fc.level_2 == i + "_y"][
        ["year_of_year", "month_of_year", i + "_x"]
    ].rename(columns={i + "_x": "ρ_" + i.split("-")[0]})
    TimeId = zip(list(cor.year_of_year), list(cor.month_of_year))
    mapingdict = dict(zip(TimeId, list(cor["ρ_" + i.split("-")[0]])))
    f["Monthly" + "ρ_" + i.split("-")[0]] = f.set_index(
        ["year_of_year", "month_of_year"]
    ).index.map(mapingdict)




#%%
f[f.jalaliDate >13980200][['jalaliDate','5-Residual_x',
 '5-Residual_y','Monthlyρ_5']]

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
