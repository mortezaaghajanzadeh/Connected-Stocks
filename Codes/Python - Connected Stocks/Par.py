#%%
import pickle
from threading import Thread
# import psutil
# from threading import Thread
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
df[df.symbol == "سامان"].id.iloc[0], df[df.symbol == "ممسنی"].id.iloc[0]


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(238)
S_g = gdata.get_group(490)


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
def func(S_g, g, AllPair ,results,num):
    results.append(FCAPf(S_g, g, AllPair))
    return results
    
def genFile(df, path, g, i):
    S_gg = df.groupby(["id"])
    # data = data.append(S_gg.apply(FCAPf, g=g))
    pickle.dump(
        S_gg.apply(FCAPf, g=g, AllPair=False),
        # parallel,
        open(path + "NormalzedFCAP9.1\\NormalzedFCAP9.1_{}.p".format(i), "wb"),
    )
    
    

def excepthook(args):
    3 == 1 + 2

import threading
threading.excepthook = excepthook
gg = df.groupby(["id"])
for i in list(gg.groups.keys())[0:1]:
    n = time.time()
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    df = df[df.id > F_id]
    gg = df.groupby(["id"])
    t = pd.DataFrame()
    nn = (len(list(gg.groups.keys())))
    results = []
    threads = [1] * nn
    AllPair = False
    for num,j in enumerate(list(gg.groups.keys())):
        S_g = gg.get_group(j)
        threads[num] = Thread(target=func,args = (S_g, g, AllPair  ,results,num,))
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        print("{} is done".format(i))
        threads[i].join()
    print(time.time() - n)
#%%
len(results)
# %%
n = time.time()
S_gg = df.groupby(["id"])
S_gg.apply(FCAPf, g=g, AllPair=False)
print(time.time() - n)
#%%