# %%
import pandas as pd


# %%
# path = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\\"
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"

df = pd.read_parquet(path + "Holder_Residual.parquet")

df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)

df = df[df.jalaliDate < 13990000]
df.head()

# %%
def FCAPf(S_g, g):
    intersection = list(set.intersection(set(S_g.date), set(g.date)))
    if len(intersection) == 0:
        #         print('0')
        return
    f = Calculation(g, S_g)
    if len(f) == 0:
        #         print('No')
        return
    name1 = g.symbol.iloc[0]
    name2 = S_g.symbol.iloc[0]
    g = g[(g.date.isin(intersection)) & (g.Holder == name2)][["date", "Percent"]]
    S_g = S_g[S_g.date.isin(intersection) & (S_g.Holder == name1)][["date", "Percent"]]
    t = g.merge(S_g, on=["date"], how="outer")
    t["MaxCommon"] = t[["Percent_x", "Percent_y"]].max(1)
    mapdict = dict(zip(t.date, t.MaxCommon))
    f["CrossOwnership"] = f["date"].map(mapdict)
    f = MonthlyCalculation(f)
    f = WeeklyCalculation(f)
    return f


def Calculation(g, S_g):
    intersection = list(set.intersection(set(S_g.date), set(g.date)))
    g = g.loc[g.date.isin(intersection)]
    g["Holder"] = 1
    S_g = S_g.loc[S_g.date.isin(intersection)]
    S_g["Holder"] = 1

    a = g.merge(
        S_g,
        on=[
            "Holder_id",
            "date",
            "jalaliDate",
            "week_of_year",
            "month_of_year",
            "year_of_year",
        ],
    )
    a = FCalculatio(a)
    if len(a) == 0:
        f = pd.DataFrame()
        return f
    a["SizeRatio"] = (a["MarketCap_x"]) / (a["MarketCap_y"])

    f = (
        a.groupby(
            [
                "date",
                "jalaliDate",
                "id_x",
                "id_y",
                "week_of_year",
                "month_of_year",
                "year_of_year",
                "group_name_x",
                "group_name_y",
                "Ret_x",
                "Ret_y",
                "SizeRatio",
                "MarketCap_x",
                "MarketCap_y",
                "2-Residual_x",
                "2-Residual_y",
                "4_Residual_x",
                "4_Residual_y",
                "5-Residual_x",
                "5-Residual_y",
                "6-Residual_x",
                "6-Residual_y",
                "5Lag_Residual_x",
                "5Lag_Residual_y",
                "Percentile_Rank_x",
                "Percentile_Rank_y",
                "BookToMarket_x",
                "BookToMarket_y",
                "BGId_x",
                "BGId_y",
                "position_x",
                "position_y",
            ]
        )[["FCAPf", "FCA", "Holder_act_y", "Holder_act_x", "Holder_x"]]
        .sum()
        .reset_index()
    )

    a = a[["type_x", "type_y"]].drop_duplicates()
    a["Sametype"] = 0
    a.loc[a.type_x == a.type_y, "Sametype"] = 1

    if a["Sametype"].sum() > 0:
        f["Sametype"] = 1
    else:
        f["Sametype"] = 0

    f = f.rename(columns={"Holder_x": "numberCommonHolder"})

    f["Holder_act"] = 0
    f.loc[f["Holder_act_y"] > 0, "Holder_act"] = 1
    f.loc[f["Holder_act_x"] > 0, "Holder_act"] = 1
    f = f.drop(columns=["Holder_act_y", "Holder_act_x"])
    f["FCA"] = f["FCA"] ** 2
    f["size1"] = 0
    f.loc[f.MarketCap_x > f.MarketCap_y, "size1"] = f[f.MarketCap_x > f.MarketCap_y][
        "Percentile_Rank_x"
    ]
    f.loc[f.MarketCap_x < f.MarketCap_y, "size1"] = f[f.MarketCap_x < f.MarketCap_y][
        "Percentile_Rank_y"
    ]
    f["size2"] = 0
    f.loc[f.MarketCap_x > f.MarketCap_y, "size2"] = f[f.MarketCap_x > f.MarketCap_y][
        "Percentile_Rank_y"
    ]
    f.loc[f.MarketCap_x < f.MarketCap_y, "size2"] = f[f.MarketCap_x < f.MarketCap_y][
        "Percentile_Rank_x"
    ]
    f["SameSize"] = -1 * abs(f["size2"] - f["size1"])
    f["sgroup"] = 0
    f.loc[f.group_name_x == f.group_name_y, "sgroup"] = 1
    f["sBgroup"] = 0
    f.loc[(~f.BGId_x.isnull()) & (f.BGId_x == f.BGId_y), "sBgroup"] = 1
    f["sposition"] = 0
    f.loc[(~f.BGId_x.isnull()) & (f.position_x == f.position_y), "sposition"] = 1
    f["B/M1"] = 0
    f.loc[f.MarketCap_x > f.MarketCap_y, "B/M1"] = f[f.MarketCap_x > f.MarketCap_y][
        "BookToMarket_x"
    ]
    f.loc[f.MarketCap_x < f.MarketCap_y, "B/M1"] = f[f.MarketCap_x < f.MarketCap_y][
        "BookToMarket_y"
    ]
    f["B/M2"] = 0
    f.loc[f.MarketCap_x > f.MarketCap_y, "B/M2"] = f[f.MarketCap_x > f.MarketCap_y][
        "BookToMarket_y"
    ]
    f.loc[f.MarketCap_x < f.MarketCap_y, "B/M2"] = f[f.MarketCap_x < f.MarketCap_y][
        "BookToMarket_x"
    ]
    f["SameB/M"] = -1 * abs(f["B/M2"] - f["B/M1"])

    return f


def FCalculatio(a):
    if len(a) == 0:
        a = pd.DataFrame()
        return a
    else:
        a["FCAPf"] = (
            a["nshares_x"] * a["close_price_x"] + a["nshares_y"] * a["close_price_y"]
        ) / (a["shrout_x"] * a["close_price_x"] + a["shrout_y"] * a["close_price_y"])
        a["FCA"] = (
            (a["nshares_x"] * a["close_price_x"]) ** 0.5
            + (a["nshares_y"] * a["close_price_y"]) ** 0.5
        ) / (
            (a["shrout_x"] * a["close_price_x"]) ** 0.5
            + (a["shrout_y"] * a["close_price_y"]) ** 0.5
        )
    return a


# %%
def MonthlyCalculation(f):

    f = MonthlyCorr(f)

    ff = (
        f.groupby(["year_of_year", "month_of_year"])[
            [
                "SizeRatio",
                "MarketCap_x",
                "MarketCap_y",
                "Percentile_Rank_x",
                "Percentile_Rank_y",
                "size1",
                "size2",
                "SameSize",
                "B/M1",
                "B/M2",
                "SameB/M",
                "CrossOwnership",
            ]
        ]
        .mean()
        .reset_index()
    )

    vlist = [
        "SizeRatio",
        "MarketCap_x",
        "MarketCap_y",
        "Percentile_Rank_x",
        "Percentile_Rank_y",
        "size1",
        "size2",
        "SameSize",
        "B/M1",
        "B/M2",
        "SameB/M",
        "CrossOwnership",
    ]

    for i in vlist:
        TimeId = zip(list(ff.year_of_year), list(ff.month_of_year))
        mapingdict = dict(zip(TimeId, list(ff[i])))
        f["Monthly" + i] = f.set_index(["year_of_year", "month_of_year"]).index.map(
            mapingdict
        )

    mfcapf = (
        f.groupby(["year_of_year", "month_of_year"])[["FCAPf", "FCA"]]
        .mean()
        .reset_index()
    )
    TimeId = zip(list(mfcapf.year_of_year), list(mfcapf.month_of_year))
    mapingdict = dict(zip(TimeId, list(mfcapf.FCAPf)))
    f["MonthlyFCAPf"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
        mapingdict
    )
    TimeId = zip(list(mfcapf.year_of_year), list(mfcapf.month_of_year))
    mapingdict = dict(zip(TimeId, list(mfcapf.FCA)))
    f["MonthlyFCA"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
        mapingdict
    )

    f["Monthlyρ_2_f"] = f["Monthlyρ_2"].shift(-1)
    f["Monthlyρ_4_f"] = f["Monthlyρ_4"].shift(-1)
    f["Monthlyρ_5_f"] = f["Monthlyρ_5"].shift(-1)
    f["Monthlyρ_6_f"] = f["Monthlyρ_6"].shift(-1)
    f["MonthlyρLag_5_f"] = f["MonthlyρLag_5"].shift(-1)
    return f


def MonthlyCorr(f):

    fc = (
        f.groupby(["year_of_year", "month_of_year"])[
            [
                "2-Residual_x",
                "2-Residual_y",
                "4_Residual_x",
                "4_Residual_y",
                "5-Residual_x",
                "5-Residual_y",
                "6-Residual_x",
                "6-Residual_y",
                "5Lag_Residual_x",
                "5Lag_Residual_y",
            ]
        ]
        .corr()
        .reset_index()
    )

    TwoCor = fc.loc[fc.level_2 == "2-Residual_y"][
        ["year_of_year", "month_of_year", "2-Residual_x"]
    ].rename(columns={"2-Residual_x": "ρ_2"})
    FourCor = fc.loc[fc.level_2 == "4_Residual_y"][
        ["year_of_year", "month_of_year", "4_Residual_x"]
    ].rename(columns={"4_Residual_x": "ρ_4"})
    ThreeCor = fc.loc[fc.level_2 == "5-Residual_y"][
        ["year_of_year", "month_of_year", "5-Residual_x"]
    ].rename(columns={"5-Residual_x": "ρ_5"})
    SixCor = fc.loc[fc.level_2 == "6-Residual_y"][
        ["year_of_year", "month_of_year", "6-Residual_x"]
    ].rename(columns={"6-Residual_x": "ρ_6"})
    FiveCor = fc.loc[fc.level_2 == "5Lag_Residual_y"][
        ["year_of_year", "month_of_year", "5Lag_Residual_x"]
    ].rename(columns={"5Lag_Residual_x": "ρLag_5"})

    TimeId = zip(list(TwoCor.year_of_year), list(TwoCor.month_of_year))
    mapingdict = dict(zip(TimeId, list(TwoCor.ρ_2)))
    f["Monthlyρ_2"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
        mapingdict
    )

    TimeId = zip(list(FourCor.year_of_year), list(FourCor.month_of_year))
    mapingdict = dict(zip(TimeId, list(FourCor.ρ_4)))
    f["Monthlyρ_4"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
        mapingdict
    )

    TimeId = zip(list(ThreeCor.year_of_year), list(ThreeCor.month_of_year))
    mapingdict = dict(zip(TimeId, list(ThreeCor.ρ_5)))
    f["Monthlyρ_5"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
        mapingdict
    )
    TimeId = zip(list(SixCor.year_of_year), list(SixCor.month_of_year))
    mapingdict = dict(zip(TimeId, list(SixCor.ρ_6)))
    f["Monthlyρ_6"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
        mapingdict
    )
    TimeId = zip(list(FiveCor.year_of_year), list(FiveCor.month_of_year))
    mapingdict = dict(zip(TimeId, list(FiveCor.ρLag_5)))
    f["MonthlyρLag_5"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
        mapingdict
    )
    return f


# %%
def WeeklyCalculation(f):

    f = WeeklyCorr(f)

    ff = (
        f.groupby(["year_of_year", "week_of_year"])[
            [
                "SizeRatio",
                "MarketCap_x",
                "MarketCap_y",
                "Percentile_Rank_x",
                "Percentile_Rank_y",
                "size1",
                "size2",
                "SameSize",
                "B/M1",
                "B/M2",
                "SameB/M",
                "CrossOwnership",
            ]
        ]
        .mean()
        .reset_index()
    )

    vlist = [
        "SizeRatio",
        "MarketCap_x",
        "MarketCap_y",
        "Percentile_Rank_x",
        "Percentile_Rank_y",
        "size1",
        "size2",
        "SameSize",
        "B/M1",
        "B/M2",
        "SameB/M",
        "CrossOwnership",
    ]

    for i in vlist:
        TimeId = zip(list(ff.year_of_year), list(ff.week_of_year))
        mapingdict = dict(zip(TimeId, list(ff[i])))
        f["Weekly" + i] = f.set_index(["year_of_year", "week_of_year"]).index.map(
            mapingdict
        )

    wfcapf = (
        f.groupby(["year_of_year", "week_of_year"])[["FCAPf", "FCA"]]
        .mean()
        .reset_index()
    )
    TimeId = zip(list(wfcapf.year_of_year), list(wfcapf.week_of_year))
    mapingdict = dict(zip(TimeId, list(wfcapf.FCAPf)))
    f["WeeklyFCAPf"] = f.set_index(["year_of_year", "week_of_year"]).index.map(
        mapingdict
    )
    TimeId = zip(list(wfcapf.year_of_year), list(wfcapf.week_of_year))
    mapingdict = dict(zip(TimeId, list(wfcapf.FCA)))
    f["WeeklyFCA"] = f.set_index(["year_of_year", "week_of_year"]).index.map(mapingdict)
    f["Weeklyρ_2_f"] = f["Weeklyρ_2"].shift(-1)
    f["Weeklyρ_4_f"] = f["Weeklyρ_4"].shift(-1)
    f["Weeklyρ_5_f"] = f["Weeklyρ_5"].shift(-1)
    f["Weeklyρ_6_f"] = f["Weeklyρ_6"].shift(-1)
    f["WeeklyρLag_5_f"] = f["WeeklyρLag_5"].shift(-1)
    return f


def WeeklyCorr(f):
    fc = (
        f.groupby(["year_of_year", "week_of_year"])[
            [
                "2-Residual_x",
                "2-Residual_y",
                "4_Residual_x",
                "4_Residual_y",
                "5-Residual_x",
                "5-Residual_y",
                "6-Residual_x",
                "6-Residual_y",
                "5Lag_Residual_x",
                "5Lag_Residual_y",
            ]
        ]
        .corr()
        .reset_index()
    )

    TwoCor = fc.loc[fc.level_2 == "2-Residual_y"][
        ["year_of_year", "week_of_year", "2-Residual_x"]
    ].rename(columns={"2-Residual_x": "ρ_2"})
    FourCor = fc.loc[fc.level_2 == "4_Residual_y"][
        ["year_of_year", "week_of_year", "4_Residual_x"]
    ].rename(columns={"4_Residual_x": "ρ_4"})
    ThreeCor = fc.loc[fc.level_2 == "5-Residual_y"][
        ["year_of_year", "week_of_year", "5-Residual_x"]
    ].rename(columns={"5-Residual_x": "ρ_5"})
    SixCor = fc.loc[fc.level_2 == "6-Residual_y"][
        ["year_of_year", "week_of_year", "6-Residual_x"]
    ].rename(columns={"6-Residual_x": "ρ_6"})
    FiveCor = fc.loc[fc.level_2 == "5Lag_Residual_y"][
        ["year_of_year", "week_of_year", "5Lag_Residual_x"]
    ].rename(columns={"5Lag_Residual_x": "ρLag_5"})

    TimeId = zip(list(TwoCor.year_of_year), list(TwoCor.week_of_year))
    mapingdict = dict(zip(TimeId, list(TwoCor.ρ_2)))
    f["Weeklyρ_2"] = f.set_index(["year_of_year", "week_of_year"]).index.map(mapingdict)

    TimeId = zip(list(FourCor.year_of_year), list(FourCor.week_of_year))
    mapingdict = dict(zip(TimeId, list(FourCor.ρ_4)))
    f["Weeklyρ_4"] = f.set_index(["year_of_year", "week_of_year"]).index.map(mapingdict)

    TimeId = zip(list(ThreeCor.year_of_year), list(ThreeCor.week_of_year))
    mapingdict = dict(zip(TimeId, list(ThreeCor.ρ_5)))
    f["Weeklyρ_5"] = f.set_index(["year_of_year", "week_of_year"]).index.map(mapingdict)
    TimeId = zip(list(SixCor.year_of_year), list(SixCor.week_of_year))
    mapingdict = dict(zip(TimeId, list(SixCor.ρ_6)))
    f["Weeklyρ_6"] = f.set_index(["year_of_year", "week_of_year"]).index.map(mapingdict)

    TimeId = zip(list(FiveCor.year_of_year), list(FiveCor.week_of_year))
    mapingdict = dict(zip(TimeId, list(FiveCor.ρLag_5)))
    f["WeeklyρLag_5"] = f.set_index(["year_of_year", "week_of_year"]).index.map(
        mapingdict
    )

    return f


# %%
df[df.symbol == "خگستر"].id.iloc[0], df[df.symbol == "خودرو"].id.iloc[0]


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(149)
S_g = gdata.get_group(139)


FCAPf(S_g, g)


# %%
data = pd.DataFrame()
gg = df.groupby(["id"])

for i in list(gg.groups.keys()):
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    Next_df = df[df.id > F_id]
    S_gg = Next_df.groupby(["id"])
    data = data.append(S_gg.apply(FCAPf, g=g))


# %%
d = data.reset_index(drop=True)


# %%
d[d.sBgroup == 1][["BGId_x", "BGId_y", "position_x", "position_y"]]


# %%
d.head()


# %%
d.sBgroup.max()


# %%
symbols = list(set(df.symbol))
symbols.sort()
ids = list(range(len(symbols)))
mapingdict = dict(zip(ids, symbols))
d["symbol_x"] = d["id_x"].map(mapingdict)
d["symbol_y"] = d["id_y"].map(mapingdict)


# %%
def add(row):
    if len(row) < 2:
        row = "0" + row
    return row


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
# ids.sort()
id = list(range(len(ids)))
mapingdict = dict(zip(ids, id))
d["id"] = d["id"].map(mapingdict)


def NormalTransform(df_sub):
    col = df_sub.transform("rank")
    return (col - col.mean()) / col.std()


gg = d.groupby(["t"])
d["FCAP*"] = gg[["FCAPf"]].apply(NormalTransform)
d["FCA*"] = gg[["FCA"]].apply(NormalTransform)

gg = d.groupby(["t_Week"])
d["WeeklyFCAP*"] = gg["WeeklyFCAPf"].apply(NormalTransform)
d["WeeklyFCA*"] = gg["WeeklyFCA"].apply(NormalTransform)

gg = d.groupby(["t_Month"])
d["MonthlyFCAP*"] = gg["MonthlyFCAPf"].apply(NormalTransform)
d["MonthlyFCA*"] = gg["MonthlyFCA"].apply(NormalTransform)


# %%
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

for a in [d]:
    mapingdict = dict(zip(SData.id, SData.GRank))
    a["GRank_x"] = a["id_x"].map(mapingdict)
    a["GRank_y"] = a["id_y"].map(mapingdict)
    a["SameGRank"] = 0
    a.loc[a.GRank_x == a.GRank_y, "SameGRank"] = 1


# %%
d = d[~d.Weeklyρ_5.isnull()]
assets = d.groupby("id").size().to_frame()
assets = assets[assets[0] > 14].index
d = d[d.id.isin(assets)].reset_index(drop=True)


# %%
d.head().columns
n3 = path + "NormalzedFCAP6.0.csv"
# d.to_csv(n3,index = False)
print("d done")
a = d.drop_duplicates(["t", "id"])
n3 = path + "NormalzedFCAP6.1.parquet"
a.to_parquet(n3)

Montly = a.drop_duplicates(["id", "t_Month"], keep="last")
n3 = path + "MonthlyNormalzedFCAP6.1"
Montly.to_csv(n3 + ".csv", index=False)
# Montly.to_feather(n3 + ".feather")
Montly.to_parquet(n3 + ".parquet")

Weekly = a.drop_duplicates(["id", "t_Week"], keep="last")
n3 = path + "WeeklyNormalzedFCAP6.1"
Weekly.to_csv(n3 + ".csv", index=False)
# Weekly.to_feather(n3 + ".feather")
Weekly.to_parquet(n3 + ".parquet")

# m = 10
# f = int(a.id.max()/m)+1
# for i in range(m):
#     MaId = (i+1)*f
#     MiId = (i)*f
#     t = a[(a.id < MaId)&((a.id >= MiId))]
#     a = a[~(a.id < MaId)]
#     t.to_csv(path + "PartedNormalzedFCAP6.1" + "-Part" + str(i+1) + ".csv",index = False)
# #     t.to_feather(path + "PartedNormalzedFCAP6.1" + "-Part" + str(i+1) + ".feather")
# #     t.to_parquet(path + "PartedNormalzedFCAP6.1" + "-Part" + str(i+1) + ".parquet")
#     print( i +1 ," Done")


# %%
df.head()
df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)
Rdf = df.drop_duplicates(["date", "symbol"])
dgg = Rdf.groupby(["id"])

a = d.drop_duplicates(["t", "id"])

# gg = a.groupby('id')
SId = df[["id", "symbol"]].drop_duplicates().reset_index(drop=True)
GData = df[["group_name", "id"]].drop_duplicates().reset_index(drop=True)
Pairs = a[["id_x", "id_y", "id"]].drop_duplicates().reset_index(drop=True)
timeId = a[["date", "t", "t_Week", "t_Month"]].drop_duplicates().sort_values(by=["t"])


##dgg.to_csv(path + "dgg" + ".csv",index = False)
SId.to_csv(path + "SId" + ".csv", index=False)
GData.to_csv(path + "GData" + ".csv", index=False)
Pairs.to_csv(path + "Pairs" + ".csv", index=False)
timeId.to_csv(path + "timeId" + ".csv", index=False)


# %%
del d


# %%
del data


# %%
a.head()


# %%
a.head().columns


# %%


# %%
a[["BGId_x", "BGId_y"]].isnull().sum()


# %%
a[a.symbol_x == "شمواد"]
