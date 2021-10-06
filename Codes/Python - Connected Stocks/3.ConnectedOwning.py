# %%
import pickle

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
    df = df.drop(columns = ['Delta_Trunover'])
except:
    1+2
#%%
df = df.rename(columns = 
    {
        '4_Residual' : '4-Residual',
        '5_Residual' : '5-Residual',
        '6_Residual' : '6-Residual',
        '2_Residual' : '2-Residual',
        '5Lag_Residual' : '5Lag-Residual',
        'Delta_TurnOver':'Delta_Trunover'
    }
)
df.head()

# %%
df[df.symbol == "خگستر"].id.iloc[0], df[df.symbol == "خودرو"].id.iloc[0]


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(158)
S_g = gdata.get_group(148)


FCAPf(S_g, g)


# %%
data = pd.DataFrame()
gg = df.groupby(["id"])
counter = 0
for i in list(gg.groups.keys()):
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    df = df[df.id > F_id]
    S_gg = df.groupby(["id"])
    # data = data.append(S_gg.apply(FCAPf, g=g))
    pickle.dump(S_gg.apply(FCAPf, g=g),
                    open(
                        path + "NormalzedFCAP9.1\\NormalzedFCAP9.1_{}.p".format(i), "wb")
                    )
#     if len(data) > 3e6:
#         counter += 1
#         data.to_parquet(path + "NormalzedFCAP9.1-part%s.parquet" % counter)
#         data = pd.DataFrame()

# counter += 1
# data.to_parquet(path + "NormalzedFCAP9.1-part%s.parquet" % counter)
#%%

# from threading import Thread
# import threading
# def excepthook(args):
#     3 == 1 + 2


# threading.excepthook = excepthook

# def creat_for_id(i,result,df,gg):
#     g = gg.get_group(i)
#     F_id = g.id.iloc[0]
#     print("Id " + str(F_id))
#     Next_df = df[df.id > F_id]
#     S_gg = Next_df.groupby(["id"])
#     result[i] = S_gg.apply(FCAPf, g=g)
# j=0
# nums = 5
# ids = list(gg.groups.keys())
# tot = int(len(ids)/nums) + 1
# for i in range(tot):
#     k = min(j + nums, len(ids))
#     print(j, k)
#     NoId = ids[j:k]
#     threads = {}
#     result = {}
#     for id in NoId:
#         threads[id] = Thread(
#             target=creat_for_id,
#             args=(id,result,df,gg),
#         )
#         threads[id].start()
#     for i in threads:
#         threads[i].join()
#         pickle.dump(result[i],
#                     open(
#                         path + "NormalzedFCAP9.1\\NormalzedFCAP9.1_{}.p".format(i), "wb")
#                     )
#     j = k

# %%
