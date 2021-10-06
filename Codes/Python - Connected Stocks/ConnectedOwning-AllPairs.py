# %%
import pandas as pd
import re as ree

# %%
def vv4(row):
    row = str(row)
    X = [1, 1, 1]
    X[0] = row[0:4]
    X[1] = row[4:6]
    X[2] = row[6:8]
    return X[0] + "-" + X[1] + "-" + X[2]


def vv(row):
    X = row.split("-")
    return X[0] + X[1] + X[2]


def DriveYearMonthDay(d):
    d["jalaliDate"] = d["jalaliDate"].astype(str)
    d["Year"] = d["jalaliDate"].str[0:4]
    d["Month"] = d["jalaliDate"].str[4:6]
    d["Day"] = d["jalaliDate"].str[6:8]
    d["jalaliDate"] = d["jalaliDate"].astype(int)
    return d


def convert_ar_characters(input_str):

    mapping = {
        "ك": "ک",
        "گ": "گ",
        "دِ": "د",
        "بِ": "ب",
        "زِ": "ز",
        "ذِ": "ذ",
        "شِ": "ش",
        "سِ": "س",
        "ى": "ی",
        "ي": "ی",
    }
    return _multiple_replace(mapping, input_str)


def _multiple_replace(mapping, text):
    pattern = "|".join(map(ree.escape, mapping.keys()))
    return ree.sub(pattern, lambda m: mapping[m.group()], str(text))


def vv2(row):
    X = row.split("/")
    return X[0] + X[1] + X[2]


def vv3(row):
    X = row.split("/")
    if len(X[0]) < 4:
        X[0] = "13" + X[0]
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[2]) < 2:
        X[2] = "0" + X[2]
    return X[0] + X[1] + X[2]


def vv5(row):
    X = row.split("/")
    return X[0]


# %%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"

df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")

df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)

df = df[df.jalaliDate < 14000000]
try:
    df = df.drop(columns=["Delta_Trunover"])
except:
    1 + 2

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
    f["CrossOwnership"] = f["date"].map(mapdict).fillna(0)
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
    a = FCalculatio(a, g, S_g)

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
                "2_Residual_x",
                "2_Residual_y",
                "4_Residual_x",
                "4_Residual_y",
                "5_Residual_x",
                "5_Residual_y",
                "6_Residual_x",
                "6_Residual_y",
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


def FCalculatio(a, g, S_g):
    if len(a) == 0:
        a = g.merge(
            S_g,
            on=[
                "date",
                "jalaliDate",
                "week_of_year",
                "month_of_year",
                "year_of_year",
            ],
        )
        a["FCAPf"] = 0
        a["FCA"] = 0
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
                "2_Residual_x",
                "2_Residual_y",
                "4_Residual_x",
                "4_Residual_y",
                "5_Residual_x",
                "5_Residual_y",
                "6_Residual_x",
                "6_Residual_y",
                "5Lag_Residual_x",
                "5Lag_Residual_y",
            ]
        ]
        .corr()
        .reset_index()
    )

    TwoCor = fc.loc[fc.level_2 == "2_Residual_y"][
        ["year_of_year", "month_of_year", "2_Residual_x"]
    ].rename(columns={"2_Residual_x": "ρ_2"})
    FourCor = fc.loc[fc.level_2 == "4_Residual_y"][
        ["year_of_year", "month_of_year", "4_Residual_x"]
    ].rename(columns={"4_Residual_x": "ρ_4"})
    ThreeCor = fc.loc[fc.level_2 == "5_Residual_y"][
        ["year_of_year", "month_of_year", "5_Residual_x"]
    ].rename(columns={"5_Residual_x": "ρ_5"})
    SixCor = fc.loc[fc.level_2 == "6_Residual_y"][
        ["year_of_year", "month_of_year", "6_Residual_x"]
    ].rename(columns={"6_Residual_x": "ρ_6"})
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
                "2_Residual_x",
                "2_Residual_y",
                "4_Residual_x",
                "4_Residual_y",
                "5_Residual_x",
                "5_Residual_y",
                "6_Residual_x",
                "6_Residual_y",
                "5Lag_Residual_x",
                "5Lag_Residual_y",
            ]
        ]
        .corr()
        .reset_index()
    )

    TwoCor = fc.loc[fc.level_2 == "2_Residual_y"][
        ["year_of_year", "week_of_year", "2_Residual_x"]
    ].rename(columns={"2_Residual_x": "ρ_2"})
    FourCor = fc.loc[fc.level_2 == "4_Residual_y"][
        ["year_of_year", "week_of_year", "4_Residual_x"]
    ].rename(columns={"4_Residual_x": "ρ_4"})
    ThreeCor = fc.loc[fc.level_2 == "5_Residual_y"][
        ["year_of_year", "week_of_year", "5_Residual_x"]
    ].rename(columns={"5_Residual_x": "ρ_5"})
    SixCor = fc.loc[fc.level_2 == "6_Residual_y"][
        ["year_of_year", "week_of_year", "6_Residual_x"]
    ].rename(columns={"6_Residual_x": "ρ_6"})
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
df[df.symbol == "شستا"].id.iloc[0], df[df.symbol == "خودرو"].id.iloc[0]


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(297)
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
    Next_df = df[df.id > F_id]
    S_gg = Next_df.groupby(["id"])
    data = data.append(S_gg.apply(FCAPf, g=g))
    if len(data) > 2e6:
        counter += 1
        data.to_parquet(path + "AllPairs\AllPairs-part%s.parquet" % counter)
        data = pd.DataFrame()

#%%
#%%
import pandas as pd
import os

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
