import os
import pandas as pd
path = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\AllPairs\\"

arr = os.listdir(path)
#%%
tt = pd.read_parquet(path[:-10] + "Holder_Residual.parquet")
tt["id"] = tt.id.astype(int)
tt = tt[["symbol", "id"]].drop_duplicates()
mapdict = dict(zip(tt.id, tt.symbol))

monthId = pd.read_csv(path[:-10] + "timeId.csv")[["t_Month", "date"]]
monthId["date"] = round(monthId.date / 100).astype(int)
monthId = monthId.drop_duplicates("t_Month")
mapingdict = dict(zip(monthId.date, monthId.t_Month))
#%%

# %%
result = pd.DataFrame()
counter = 0
for i, name in enumerate(arr):
    print(i)
    df = (
        pd.read_parquet(path + name)
        .reset_index(drop=True)
        .drop(
            columns=[
                "Weeklyρ_2",
                "Weeklyρ_4",
                "Weeklyρ_5",
                "Weeklyρ_6",
                "WeeklyρLag_5",
                "WeeklySizeRatio",
                "WeeklyMarketCap_x",
                "WeeklyMarketCap_y",
                "WeeklyPercentile_Rank_x",
                "WeeklyPercentile_Rank_y",
                "Weeklysize1",
                "Weeklysize2",
                "WeeklySameSize",
                "WeeklyB/M1",
                "WeeklyB/M2",
                "WeeklySameB/M",
                "WeeklyCrossOwnership",
                "WeeklyFCAPf",
                "WeeklyFCA",
                "Weeklyρ_2_f",
                "Weeklyρ_4_f",
                "Weeklyρ_5_f",
                "Weeklyρ_6_f",
                "WeeklyρLag_5_f",
            ]
        )
    )
    df["id_x"] = df.id_x.astype(int)
    df["id_y"] = df.id_y.astype(int)
    df["symbol_x"] = df.id_x.map(mapdict)
    df["symbol_y"] = df.id_y.map(mapdict)
    df[["symbol_x", "symbol_y"]].isnull().sum()
    df = df[df.id_x != df.id_y]
    df["id"] = df["symbol_x"] + "-" + df["symbol_y"]
    ids = list(set(df.id))
    id = list(range(len(ids)))
    mapingdict1 = dict(zip(ids, id))
    df["id"] = df["id"].map(mapingdict1)

    df["yearMonth"] = round(df.date / 100).astype(int)
    df["t_Month"] = df.yearMonth.map(mapingdict)

    dt = df.drop_duplicates(["id", "t_Month"], keep="last")

    result = result.append(dt)
    if len(result) > 3e6:
        counter += 1
        result.to_parquet(path + "MonthlyAllPairs-part%s.parquet" % counter)
        result = pd.DataFrame()
# %%
result[result.t_Month.isnull()].yearMonth.unique()

#%%
result["id"] = result["symbol_x"] + "-" + result["symbol_y"]
ids = list(set(result.id))
id = list(range(len(ids)))
mapingdict1 = dict(zip(ids, id))
result["id"] = result["id"].map(mapingdict1)
# %%

# %%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
result = pd.read_csv(path + "MonthlyAllPairs.csv")
#%%


def NormalTransform(df_sub):
    col = df_sub.transform("rank")
    return (col - col.mean()) / col.std()


gg = result.groupby(["t_Month"])
result["MonthlyFCAP*"] = gg["MonthlyFCAPf"].apply(NormalTransform)
result["NMFCA"] = gg["MonthlyFCA"].apply(NormalTransform)
# %%
result["4rdQarterTotal"] = 0
result["2rdQarter"] = 0
result["4rdQarter"] = 0
gg = result.groupby(["t_Month"])
g = gg.get_group(2)

g[g.MonthlyFCA > 0].MonthlyFCA.quantile(0.75), g.MonthlyFCA.quantile(0.75)

#%%
def quarter(g):
    print(g.name)
    q1 = g[g.MonthlyFCA > 0].MonthlyFCA.quantile(0.75)
    qt = g.MonthlyFCA.quantile(0.75)
    mt = g[g.MonthlyFCA > 0].MonthlyFCA.quantile(0.5)
    g.loc[g.MonthlyFCA > q1, "4rdQarter"] = 1
    g.loc[g.MonthlyFCA > qt, "4rdQarterTotal"] = 1
    g.loc[g.MonthlyFCA > mt, "2rdQarter"] = 1
    return g


gg = result.groupby(["t_Month"])
result = gg.apply(quarter)
# %%
result.to_csv(path + "MonthlyAllPairs.csv", index=False)
# %%
result.groupby("t_Month").size()
