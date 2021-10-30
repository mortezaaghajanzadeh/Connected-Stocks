#%%
import pandas as pd
import os

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
# Monthly = pd.DataFrame()
# Weekly = pd.DataFrame()
# time = pd.DataFrame()
# d = pd.DataFrame()
# arrs = os.listdir(path + "NormalzedFCAP9.1")
# counter_file = 0
# for counter, i in enumerate(arrs):
#     print(counter, len(Monthly))
#     d = pd.read_pickle(path + "NormalzedFCAP9.1\\" + i)
#     if len(d) == 0:
#         continue
#     d = firstStep(d, df)
#     m = d.drop_duplicates(["id", "t_Month"], keep="last").drop(
#         columns=[
#             "Weeklyρ_2",
#             "Weeklyρ_4",
#             "Weeklyρ_5",
#             "Weeklyρ_6",
#             "Weeklyρ_5Lag",
#             "Weeklyρ_turn",
#             "Weeklyρ_amihud",
#             "WeeklySizeRatio",
#             "WeeklyMarketCap_x",
#             "WeeklyMarketCap_y",
#             "WeeklyPercentile_Rank_x",
#             "WeeklyPercentile_Rank_y",
#             "Weeklysize1",
#             "Weeklysize2",
#             "WeeklySameSize",
#             "WeeklyB/M1",
#             "WeeklyB/M2",
#             "WeeklySameB/M",
#             "WeeklyCrossOwnership",
#             "WeeklyTurnOver_x",
#             "WeeklyAmihud_x",
#             "Weeklyvolume_x",
#             "Weeklyvalue_x",
#             "WeeklyTurnOver_y",
#             "WeeklyAmihud_y",
#             "Weeklyvolume_y",
#             "Weeklyvalue_y",
#             "WeeklyFCAPf",
#             "WeeklyFCA",
#             "Weeklyρ_2_f",
#             "Weeklyρ_4_f",
#             "Weeklyρ_5_f",
#             "Weeklyρ_6_f",
#             "WeeklyρLag_5_f",
#             "Weeklyρ_turn_f",
#             "Weeklyρ_amihud_f",
#         ]
#     )
#     Monthly = Monthly.append(m)
#     # w = d.drop_duplicates(["id", "t_Week"], keep="last").drop(
#     #     columns=[
#     #         "Monthlyρ_2",
#     #         "Monthlyρ_4",
#     #         "Monthlyρ_5",
#     #         "Monthlyρ_6",
#     #         "Monthlyρ_5Lag",
#     #         "Monthlyρ_turn",
#     #         "Monthlyρ_amihud",
#     #         "MonthlySizeRatio",
#     #         "MonthlyMarketCap_x",
#     #         "MonthlyMarketCap_y",
#     #         "MonthlyPercentile_Rank_x",
#     #         "MonthlyPercentile_Rank_y",
#     #         "Monthlysize1",
#     #         "Monthlysize2",
#     #         "MonthlySameSize",
#     #         "MonthlyB/M1",
#     #         "MonthlyB/M2",
#     #         "MonthlySameB/M",
#     #         "MonthlyCrossOwnership",
#     #         "MonthlyTurnOver_x",
#     #         "MonthlyAmihud_x",
#     #         "Monthlyvolume_x",
#     #         "Monthlyvalue_x",
#     #         "MonthlyTurnOver_y",
#     #         "MonthlyAmihud_y",
#     #         "Monthlyvolume_y",
#     #         "Monthlyvalue_y",
#     #         "MonthlyFCAPf",
#     #         "MonthlyFCA",
#     #         "Monthlyρ_2_f",
#     #         "Monthlyρ_4_f",
#     #         "Monthlyρ_5_f",
#     #         "Monthlyρ_6_f",
#     #         "MonthlyρLag_5_f",
#     #         "Monthlyρ_turn_f",
#     #         "Monthlyρ_amihud_f",
#     #     ]
#     # )
#     # Weekly = Weekly.append(w)
#     d = pd.DataFrame()
#     if len(Monthly) > 6e6:
#         counter_file += 1
#         Monthly.to_parquet(
#             path + "mergerd_first_step_monthly_part_{}.parquet".format(counter_file)
#         )
#         Monthly = pd.DataFrame()
# counter_file += 1
# Monthly.to_parquet(
#     path + "mergerd_first_step_monthly_part_{}.parquet".format(counter_file)
# )
# Monthly = pd.DataFrame()
# %%
Monthly = pd.read_parquet( 
        path + "mergerd_first_step_monthly_part_{}.parquet".format(1)
        ).drop(columns = [
            'Ret_x',
 'Ret_y',
 'SizeRatio',
 'MarketCap_x',
 'MarketCap_y',
 '2-Residual_x',
 '2-Residual_y',
 '4-Residual_x',
 '4-Residual_y',
 '5-Residual_x',
 '5-Residual_y',
 '6-Residual_x',
 '6-Residual_y',
 '5Lag-Residual_x',
 '5Lag-Residual_y',
 'Percentile_Rank_x',
 'Percentile_Rank_y',
 'BookToMarket_x',
 'BookToMarket_y',
 'Amihud_x',
 'volume_x',
 'value_x',
 'TurnOver_y',
 'Amihud_y',
 'volume_y',
 'value_y',
 'Delta_Trunover_x',
 'Delta_Trunover_y',
 'Delta_Amihud_x',
 'Delta_Amihud_y',
        ])
Monthly = Monthly.append(
    pd.read_parquet( 
        path + "mergerd_first_step_monthly_part_{}.parquet".format(2)
        ).drop(columns = [
            'Ret_x',
 'Ret_y',
 'SizeRatio',
 'MarketCap_x',
 'MarketCap_y',
 '2-Residual_x',
 '2-Residual_y',
 '4-Residual_x',
 '4-Residual_y',
 '5-Residual_x',
 '5-Residual_y',
 '6-Residual_x',
 '6-Residual_y',
 '5Lag-Residual_x',
 '5Lag-Residual_y',
 'Percentile_Rank_x',
 'Percentile_Rank_y',
 'BookToMarket_x',
 'BookToMarket_y',
 'Amihud_x',
 'volume_x',
 'value_x',
 'TurnOver_y',
 'Amihud_y',
 'volume_y',
 'value_y',
 'Delta_Trunover_x',
 'Delta_Trunover_y',
 'Delta_Amihud_x',
 'Delta_Amihud_y',
        ])
)

#%%
Monthly = SecondStep(Monthly)
# Weekly = SecondStep(Weekly)
print("First step is done")
gg = Monthly.groupby(["t_Month"])
Monthly["MonthlyFCAP*"] = gg["MonthlyFCAPf"].apply(NormalTransform)
Monthly["MonthlyFCA*"] = gg["MonthlyFCA"].apply(NormalTransform)

# gg = Weekly.groupby(["t_Week"])
# Weekly["WeeklyFCAP*"] = gg["WeeklyFCAPf"].apply(NormalTransform)
# Weekly["WeeklyFCA*"] = gg["WeeklyFCA"].apply(NormalTransform)
print("Second step is done")
#%%

# for a in [Monthly, Weekly]:
for a in [Monthly]:
    mapingdict = dict(zip(SData.id, SData.GRank))
    a["GRank_x"] = a["id_x"].map(mapingdict)
    a["GRank_y"] = a["id_y"].map(mapingdict)
    a["SameGRank"] = 0
    a.loc[a.GRank_x == a.GRank_y, "SameGRank"] = 1

Monthly = Monthly[~Monthly.Monthlyρ_5.isnull()]
# Monthly = Monthly.groupby(["id"]).filter(lambda x: x.shape[0] >= 15)
n3 = path + "MonthlyNormalzedFCAP9.1"
Monthly.to_parquet(n3 + ".parquet", index=False)

# Weekly = Weekly[~Weekly.Weeklyρ_5.isnull()]
# assets = Weekly.groupby("id").size().to_frame()
# assets = assets[assets[0] > 14].index
# Weekly = Weekly[Weekly.id.isin(assets)].reset_index(drop=True)
# n3 = path + "WeeklyNormalzedFCAP9.1"
# Weekly.to_parquet(n3 + ".parquet", index=False)
# del Weekly
# %%


df["month_of_year"] = df["month_of_year"].astype(str).apply(add)
df["week_of_year"] = df["week_of_year"].astype(str).apply(add)


df["year_of_year"] = df["year_of_year"].astype(str)

df["Year_Month_week"] = df["year_of_year"] + df["week_of_year"]
df["Year_Month"] = df["year_of_year"] + df["month_of_year"]

days = list(set(df.date))
days.sort()
t = list(range(len(days)))
mapingdict = dict(zip(days, t))
df["t"] = df["date"].map(mapingdict)

days = list(set(df.Year_Month_week))
days.sort()
t = list(range(len(days)))
mapingdict = dict(zip(days, t))
df["t_Week"] = df["Year_Month_week"].map(mapingdict)

days = list(set(df.Year_Month))
days.sort()
t = list(range(len(days)))
mapingdict = dict(zip(days, t))
df["t_Month"] = df["Year_Month"].map(mapingdict)


# %%
df["week_of_year"] = df.week_of_year.astype(int)
df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)
Rdf = df.drop_duplicates(["date", "symbol"])
dgg = Rdf.groupby(["id"])


# gg = a.groupby('id')
SId = df[["id", "symbol"]].drop_duplicates().reset_index(drop=True)
GData = df[["group_name", "id"]].drop_duplicates().reset_index(drop=True)
Pairs = Monthly[["id_x", "id_y", "id"]].drop_duplicates().reset_index(drop=True)
timeId = a[["date", "t", "t_Week", "t_Month"]].drop_duplicates().sort_values(by=["t"])


##dgg.to_csv(path + "dgg" + ".csv",index = False)
SId.to_csv(path + "SId" + ".csv", index=False)
GData.to_csv(path + "GData" + ".csv", index=False)
Pairs.to_csv(path + "Pairs" + ".csv", index=False)
timeId.to_csv(path + "timeId" + ".csv", index=False)
# %%
