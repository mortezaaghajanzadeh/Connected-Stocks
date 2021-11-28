#%%
import pandas as pd
import os
import pickle

path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"


def add(row):
    if len(row) < 2:
        row = "0" + row
    return row


def firstStep(d, df):
    mapingdict = dict(zip(df.id, df.symbol))

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
df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")
SId = df[["id", "symbol"]].drop_duplicates().reset_index(drop=True)

SData = (
    df.groupby("symbol")[["Percentile_Rank"]]
    .mean()
    .sort_values(by=["Percentile_Rank"])
    .reset_index()
)
SData = SData.merge(SId)
SData["Rank"] = SData.Percentile_Rank.rank()
SData["GRank"] = 0
for i in range(9):
    t = i + 1
    tempt = (SData["Rank"].max()) / 10
    SData.loc[SData["Rank"] > tempt * t, "GRank"] = t

#%%
Monthly = pd.DataFrame()
Weekly = pd.DataFrame()
time = pd.DataFrame()
d = pd.DataFrame()
mlist = [
            "Weeklyρ_2",
            "Weeklyρ_4",
            "Weeklyρ_5",
            "Weeklyρ_6",
            "Weeklyρ_5Lag",
            "Weeklyρ_turn",
            "Weeklyρ_amihud",
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
            "WeeklyTurnOver_x",
            "WeeklyAmihud_x",
            "Weeklyvolume_x",
            "Weeklyvalue_x",
            "WeeklyTurnOver_y",
            "WeeklyAmihud_y",
            "Weeklyvolume_y",
            "Weeklyvalue_y",
            "WeeklyFCAPf",
            "WeeklyFCA",
            "Weeklyρ_2_f",
            "Weeklyρ_4_f",
            "Weeklyρ_5_f",
            "Weeklyρ_6_f",
            "WeeklyρLag_5_f",
            "Weeklyρ_turn_f",
            "Weeklyρ_amihud_f",
        ]
arrs = os.listdir(path + "NormalzedFCAP9.1")
arrs.remove("Old")
counter_file = 0
for counter, i in enumerate(arrs):
    print(counter, len(Monthly))
    d = pd.read_pickle(path + "NormalzedFCAP9.1\\" + i)
    if len(d) == 0:
        continue
    d = d.drop(
        columns= mlist
    )
    if len(d) == 0:
        continue
    d = firstStep(d, df)
    m = d.drop_duplicates(["id", "t_Month"], keep="last")
    Monthly = Monthly.append(m)
    d = pd.DataFrame()
    if len(Monthly) > 6e6:
        counter_file += 1
        pickle.dump(
            Monthly,
            open(
                path + "mergerd_first_step_monthly_part_{}.p".format(counter_file),
                "wb",
            ),
        )
        Monthly = pd.DataFrame()
counter_file += 1
pickle.dump(
    Monthly,
    open(
        path + "mergerd_first_step_monthly_part_{}.p".format(counter_file),
        "wb",
    ),
)
Monthly = pd.DataFrame()
# %%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\NormalzedFCAP9.1_AllPairs\\"
path2 = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
arr = os.listdir(path)
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
        columns= mlist
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

