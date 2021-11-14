#%%
import pandas as pd

# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
#%%
result = pd.read_csv(path + "TurnOver_1400_06_28.csv")
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
df.to_csv(path + "turnovercrosssection_1400_06_28.csv", index=False)
# %%
list(df)
# %%
tempt = df.groupby(['uo','year']).Coef_deltagroup.mean().to_frame()
tempt = tempt.reset_index()
gg = tempt.groupby('year')
def highBeta(g):
    print(g.name)
    t = g.Coef_deltagroup.median()
    g['highBeta'] = 0
    g.loc[g.Coef_deltagroup > t, 'highBeta'] = 1
    return g
tempt = gg.apply(highBeta).set_index(['uo','year'])
tempt
#%%
tt = pd.read_parquet(path + "MonthlyNormalzedFCAP9.2.parquet")
#%%
tt['year_of_year'] = tt.year_of_year.astype(int)
mapingdict = dict(
    zip(tempt.index,tempt.Coef_deltagroup)
)
tt['Coef_deltagroup_x'] = tt.set_index(
    ['uo_x','year_of_year']
    ).index.map(mapingdict)
tt['Coef_deltagroup_y'] = tt.set_index(
    ['uo_y','year_of_year']
    ).index.map(mapingdict)

mapingdict = dict(
    zip(tempt.index,tempt.highBeta)
)
tt['highBeta_x'] = tt.set_index(
    ['uo_x','year_of_year']
    ).index.map(mapingdict)
tt['highBeta_y'] = tt.set_index(
    ['uo_y','year_of_year']
    ).index.map(mapingdict)
tt
#%%
tt.loc[tt.highBeta_x.isnull(), 'highBeta_x'] = 0
tt.loc[tt.highBeta_y.isnull(), 'highBeta_y'] = 0
tt.loc[tt.Coef_deltagroup_x.isnull(), 'Coef_deltagroup_x'] = 0
tt.loc[tt.Coef_deltagroup_y.isnull(), 'Coef_deltagroup_y'] = 0


# %%
tt.to_parquet(path + "MonthlyNormalzedFCAP9.3.parquet")
tt.to_csv(path + "MonthlyNormalzedFCAP9.3.csv",index = False)
# %%
