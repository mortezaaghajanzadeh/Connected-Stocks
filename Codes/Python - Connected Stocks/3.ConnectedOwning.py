# %%
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
threads = {}
for i in list(gg.groups.keys()):
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    df = df[df.id > F_id]
    gg = df.groupby(["id"])
    while psutil.virtual_memory().percent > 70:
        1+2     
    threads[i] = Thread(
            target=genFile,
            args=(df,path,g,i),
        )
    threads[i].start()
threads[i].join()
#%%
# All pairs 
data = pd.DataFrame()
gg = df.groupby(["id"])
counter = 0
def genFile(df,path,g,i):
    S_gg = df.groupby(["id"])
    # data = data.append(S_gg.apply(FCAPf, g=g))
    pickle.dump(
        S_gg.apply(FCAPf, g=g,AllPair = True),
        open(path + "NormalzedFCAP9.1_AllPairs\\NormalzedFCAP9.1_AllPairs_{}.p".format(i), "wb")
    )
threads = {}
for i in list(gg.groups.keys()):
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    df = df[df.id > F_id]
    gg = df.groupby(["id"])
    while psutil.virtual_memory().percent > 50:
        1+2     
    threads[i] = Thread(
            target=genFile,
            args=(df,path,g,i),
        )
    threads[i].start()
threads[i].join()