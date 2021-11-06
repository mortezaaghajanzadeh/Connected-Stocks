#%%
import os
import pandas as pd
import pickle

path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\NormalzedFCAP9.1_AllPairs\\"
path2 = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
arr = os.listdir(path)


def add(row):
    if len(row) < 2:
        row = "0" + row
    return row


def firstStep(d, mapingdict):
    d["symbol_x"] = d["id_x"].map(mapingdict)
    d["symbol_y"] = d["id_y"].map(mapingdict)

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


def NormalTransform(df_sub):
    col = df_sub.transform("rank")
    return (col - col.mean()) / col.std()


def SecondStep(a):
    a = a.reset_index(drop=True)
    a["id_x"] = a.id_x.astype(str)
    a["id_y"] = a.id_y.astype(str)
    a["id"] = a["id_x"] + "-" + a["id_y"]
    ids = list(set(a.id))
    id = list(range(len(ids)))
    mapingdict = dict(zip(ids, id))
    a["id"] = a["id"].map(mapingdict)
    return a


#%%
tt = pd.read_parquet(path2 + "Holder_Residual_1400_06_28.parquet")
tt["id"] = tt.id.astype(int)
tt = tt[["symbol", "id"]].drop_duplicates()
mapdict = dict(zip(tt.id, tt.symbol))

monthId = pd.read_csv(path2 + "timeId.csv")[["t_Month", "date"]]
monthId["date"] = round(monthId.date / 100).astype(int)
monthId = monthId.drop_duplicates("t_Month")
mapingdict = dict(zip(monthId.date, monthId.t_Month))

# %%
result = pd.DataFrame()
counter, counter_file = 0, 0
# arr.remove("MonthlyAllPairs_1400_06_28.csv")
for i, name in enumerate(arr):
    print(i, len(result))
    d = pd.read_pickle(path + name).reset_index(drop=True)
    if len(d) < 1:
        continue
    d = d.drop(
        columns=[
            "Weeklyρ_2",
            "Weeklyρ_4",
            "Weeklyρ_5",
            "Weeklyρ_6",
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
            "Weeklyρ_5Lag",
            "Weeklyρ_turn",
            "Weeklyρ_amihud",
            "WeeklyTurnOver_x",
            "WeeklyAmihud_x",
            "Weeklyvolume_x",
            "Weeklyvalue_x",
            "WeeklyTurnOver_y",
            "WeeklyAmihud_y",
            "Weeklyvolume_y",
            "Weeklyvalue_y",
            "Weeklyρ_turn_f",
            "Weeklyρ_amihud_f",
        ]
    )
    d = firstStep(d, mapdict).drop_duplicates(["id", "t_Month"], keep="last")
    result = result.append(d)
    d = pd.DataFrame()
    if len(result) > 6e6:
        counter_file += 1
        pickle.dump(
            result,
            open(
                path2
                + "mergerd_first_step_monthly_all_part_{}.p".format(counter_file),
                "wb",
            ),
        )
        result = pd.DataFrame()
counter_file += 1
pickle.dump(
            result,
            open(
                path2
                + "mergerd_first_step_monthly_all_part_{}.p".format(counter_file),
                "wb",
            ),
        )
result = pd.DataFrame()

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

result[['t_Month','Year_Month']].drop_duplicates().sort_values(by = ['t_Month'])
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
