# %%
import pickle

# import psutil
# from threading import Thread
from ConnectedOwnershipFunctions import *
import time

# %%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"


df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")
df["week_of_year"] = df.week_of_year.astype(int)
df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)

df = df[df.jalaliDate < 14000000]
df = df[df.jalaliDate > 13930000]
df = df[~df["5_Residual"].isnull()]
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
        "Month_of_year":"month_of_year"
    }
)
df.head()

# %%
df[df.symbol == "فولاد"].id.iloc[0], df[df.symbol == "خودرو"].id.iloc[0]


# # %%
# gdata = df.groupby(["id"])
# g = gdata.get_group(167)
# S_g = gdata.get_group(157)

# AllPair = True

# n = time.time()
# t1 = FCAPf(S_g, g,AllPair)
# print(time.time() - n)


# AllPair = False
# n = time.time()
# t2 = FCAPf(S_g, g,AllPair)
# print(time.time() - n)

# #%%
# len(t1[t1.FCAPf>0]),len(t2)


#%%
data = pd.DataFrame()
gg = df.groupby(["id"])
counter = 0


def genFile(df, path, g, i):
    S_gg = df.groupby(["id"])
    # data = data.append(S_gg.apply(FCAPf, g=g))
    pickle.dump(
        S_gg.apply(FCAPf, g=g, AllPair=False),
        open(path + "NormalzedFCAP9.1\\NormalzedFCAP9.1_{}.p".format(i), "wb"),
    )

for i in list(gg.groups.keys()):
    n = time.time()
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    df = df[df.id > F_id]
    gg = df.groupby(["id"])
    genFile(df, path, g, i)
    print(time.time() - n)

# threads = {}
# for i in list(gg.groups.keys()):
#     n = time.time()
#     g = gg.get_group(i)
#     F_id = g.id.iloc[0]
#     print("Id " + str(F_id))
#     df = df[df.id > F_id]
#     gg = df.groupby(["id"])
#     genFile(df, path, g, i)
#     print(time.time() - n)
#     while psutil.virtual_memory().percent > 80:
#         1+2
#     threads[i] = Thread(
#             target=genFile,
#             args=(df,path,g,i),
#         )
#     threads[i].start()
# threads[i-1].join()
#%%
# All pairs
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


#     while psutil.virtual_memory().percent > 80:
#         1+2
#     try:
#         threads[i] = Thread(
#                 target=genFile,
#                 args=(df,path,g,i),
#             )
#         threads[i].start()
#     except:
#         while psutil.virtual_memory().percent > 80:
#             1+2
#         threads[i] = Thread(
#                 target=genFile,
#                 args=(df,path,g,i),
#             )
#         threads[i].start()
# threads[i-1].join()
# %%
