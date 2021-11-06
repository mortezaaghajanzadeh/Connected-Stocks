#%%
import os
import pandas as pd
import pickle
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
#%%


result = pd.read_pickle(
    path + "mergerd_first_step_monthly_all_part_{}.p".format(1)
).drop(
    columns=[
        "Ret_x",
        "Ret_y",
        "SizeRatio",
        "MarketCap_x",
        "MarketCap_y",
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
        "Percentile_Rank_x",
        "Percentile_Rank_y",
        "BookToMarket_x",
        "BookToMarket_y",
        "Amihud_x",
        "volume_x",
        "value_x",
        "TurnOver_y",
        "Amihud_y",
        "volume_y",
        "value_y",
        "Delta_Trunover_x",
        "Delta_Trunover_y",
        "Delta_Amihud_x",
        "Delta_Amihud_y",
    ]
)
result = result.append(
    pd.read_pickle(path + "mergerd_first_step_monthly_all_part_{}.p".format(2)).drop(
        columns=[
            "Ret_x",
            "Ret_y",
            "SizeRatio",
            "MarketCap_x",
            "MarketCap_y",
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
            "Percentile_Rank_x",
            "Percentile_Rank_y",
            "BookToMarket_x",
            "BookToMarket_y",
            "Amihud_x",
            "volume_x",
            "value_x",
            "TurnOver_y",
            "Amihud_y",
            "volume_y",
            "value_y",
            "Delta_Trunover_x",
            "Delta_Trunover_y",
            "Delta_Amihud_x",
            "Delta_Amihud_y",
        ]
    )
)

#%%
def firstStep(d):
    d["month_of_year"] = d["month_of_year"].astype(str).apply(add)
    d["week_of_year"] = d["week_of_year"].astype(str).apply(add)

    d["year_of_year"] = d["year_of_year"].astype(str)

    d["Year_Month_week"] = d["year_of_year"] + d["week_of_year"]
    d["Year_Month"] = d["year_of_year"] + d["month_of_year"]

    days = list(set(d.date))
    days.sort()
    t = list(range(len(days)))
    mapingdict = dict(zip(days, t))
    d["t"] = d["date"].map(mapingdict)

    days = list(set(d.Year_Month_week))
    days.sort()
    t = list(range(len(days)))
    mapingdict = dict(zip(days, t))
    d["t_Week"] = d["Year_Month_week"].map(mapingdict)

    days = list(set(d.Year_Month))
    days.sort()
    t = list(range(len(days)))
    mapingdict = dict(zip(days, t))
    d["t_Month"] = d["Year_Month"].map(mapingdict)

    d["id_x"] = d.id_x.astype(str)
    d["id_y"] = d.id_y.astype(str)
    d["id"] = d["id_x"] + "-" + d["id_y"]
    ids = list(set(d.id))
    id = list(range(len(ids)))
    mapingdict = dict(zip(ids, id))
    d["id"] = d["id"].map(mapingdict)
    return d


result = firstStep(result)
#%%

result[["t_Month", "Year_Month"]].drop_duplicates().sort_values(by=["t_Month"])
#%%
#%%
result[
    (result.symbol_x == "آبادا") & (result.symbol_y == "اوان")
].isnull().sum().to_frame().tail(15)

#%%
result["id"] = result["symbol_x"] + "-" + result["symbol_y"]
ids = list(set(result.id))
id = list(range(len(ids)))
mapingdict1 = dict(zip(ids, id))
result["id"] = result["id"].map(mapingdict1)
# %%

#%%


def NormalTransform(df_sub):
    col = df_sub.transform("rank")
    return (col - col.mean()) / col.std()


result = result.reset_index(drop=True)
gg = result.groupby(["t_Month"])

result["MonthlyFCAP*"] = gg["MonthlyFCAPf"].apply(NormalTransform)
result["NMFCA"] = gg["MonthlyFCA"].apply(NormalTransform)
#%%
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
result.to_csv(path + "MonthlyAllPairs_1400_06_28.csv", index=False)
# %%
result.groupby("t_Month").size()

# %%
