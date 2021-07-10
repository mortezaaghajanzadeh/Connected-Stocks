#%%
import pandas as pd

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
#%%
result = pd.read_csv(path + "TurnOver.csv")

#%%
df = pd.read_stata(path + "FirstStageAmihud.dta")
[
    [
        "_b_delta_amihud_market",
        "_b_delta_amihud_group",
        "_b_delta_amihud_industry",
        "_TimeVar",
    ]
]
df["_TimeVar"] = df._TimeVar.astype(int)
result["regidyear"] = result.regidyear.astype(int)
for i in [
    "_b_delta_amihud_market",
    "_b_delta_amihud_group",
    "_b_delta_amihud_industry",
]:
    mapdict = dict(zip(df._TimeVar, df[i]))
    result["Coef" + i[2:]] = result.regidyear.map(mapdict)
# %%
df = pd.read_stata(path + "FirstStageTurnover.dta")
[
    [
        "_b_deltamarket",
        "_b_deltagroup",
        "_b_deltaindustry",
        "_TimeVar",
    ]
]
df["_TimeVar"] = df._TimeVar.astype(int)
for i in [
    "_b_deltamarket",
    "_b_deltagroup",
    "_b_deltaindustry",
]:
    mapdict = dict(zip(df._TimeVar, df[i]))
    result["Coef" + i[2:]] = result.regidyear.map(mapdict)


#%%
df = result.drop_duplicates(subset=["symbol", "regidyear"], keep="last")
df = df[
    [
        "symbol",
        "id",
        "group_name",
        "close_price",
        "shrout",
        "year",
        "uo",
        "cfr",
        "cr",
        "centrality",
        "position",
        "Grouped",
        "marketCap",
        "regidyear",
        "Coef_delta_amihud_market",
        "Coef_delta_amihud_group",
        "Coef_delta_amihud_industry",
        "Coef_deltamarket",
        "Coef_deltagroup",
        "Coef_deltaindustry",
    ]
]
t = result.groupby(["symbol", "regidyear"]).Amihud_value.mean().to_frame()
mapdict = dict(zip(t.index, t.Amihud_value))
df["Amihud"] = df.set_index(["symbol", "regidyear"]).index.map(mapdict)
t = result.groupby(["symbol", "regidyear"]).TurnOver.mean().to_frame()
mapdict = dict(zip(t.index, t.TurnOver))
df["TurnOver"] = df.set_index(["symbol", "regidyear"]).index.map(mapdict)
a = pd.read_csv(path + "lowImbalanceUO-Annual.csv")
mapdict = dict(zip(a.set_index(["year", "uo"]).index, a.lowImbalanceStd))

df["lowImbalanceStd"] = df.set_index(["year", "uo"]).index.map(mapdict)
df.to_csv(path + "turnovercrosssection.csv", index=False)
# %%
