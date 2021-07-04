#%%
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
import re as ree


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


path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
#%%
df = pd.read_parquet(path + "Holder_Residual.parquet")
df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)

df = df[df.jalaliDate < 13990000]
df.head()
#%%
pdata = pd.read_parquet(
    r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Stocks_Prices_1400-02-07.parquet"
)

pdata["name"] = pdata["name"].apply(lambda x: convert_ar_characters(x))

#%%
pdata["stock_id"] = pdata["stock_id"].astype(float)
pdata["date"] = pdata["date"].astype(float)
mapdict = dict(zip(pdata.set_index(["stock_id", "date"]).index, pdata.close_price))
df["stock_id"] = df["stock_id"].astype(float)
df["date"] = df["date"].astype(float)
df["close_price"] = df.set_index(["stock_id", "date"]).index.map(mapdict)
#%%
mapdict = dict(zip(pdata.set_index(["name", "date"]).index, pdata.close_price))
df["close_price2"] = df.set_index(["symbol", "date"]).index.map(mapdict)
#%%
df.loc[(df.close_price.isnull()) & (~df.close_price2.isnull()), "close_price"] = df.loc[
    (df.close_price.isnull()) & (~df.close_price2.isnull())
].close_price2
df = df[~df.close_price.isnull()].drop(columns=["close_price2"])
#%%
df["close_price"] = df["close_price"].astype(float)
df["MarketCap"] = df["shrout"] * df["close_price"]
df = df[~df["5-Residual"].isnull()]
# %%
def FCAPf(S_g, g):
    intersection = list(set.intersection(set(S_g.date), set(g.date)))
    if len(intersection) == 0:
        # print('0')
        return
    f = Calculation(g, S_g)
    print(S_g.id.iloc[0])
    if len(f) == 0:
        # print('No')
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


def kCall(t):
    cos_vec = 1 - cosine(t["Percent_y"], t["Percent_x"])
    return cos_vec


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
    tempt = a[["date", "Percent_y", "Percent_x"]]
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
                "MarketCap_x",
                "MarketCap_y",
                "Percentile_Rank_x",
                "Percentile_Rank_y",
                "BookToMarket_x",
                "BookToMarket_y",
            ]
        )[["FCAPf", "FCA", "Holder_act_y", "Holder_act_x", "Holder_x"]]
        .sum()
        .reset_index()
    )
    clist = [
        "Ret_x",
        "SizeRatio",
        "Ret_y",
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
        "BGId_x",
        "BGId_y",
        "position_x",
        "position_y",
    ]
    for i in clist:
        mapdict = dict(zip(a.date, a[i]))
        f[i] = f.date.map(mapdict)
    f
    tg = tempt.groupby("date")

    f = f.set_index("date")
    f["k"] = tg.apply(kCall)
    f = f.reset_index()

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
        f.groupby(["year_of_year", "month_of_year"])[["FCAPf", "FCA", "k"]]
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
    TimeId = zip(list(mfcapf.year_of_year), list(mfcapf.month_of_year))
    mapingdict = dict(zip(TimeId, list(mfcapf.k)))
    f["Monthlyk"] = f.set_index(["year_of_year", "month_of_year"]).index.map(mapingdict)

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
        f.groupby(["year_of_year", "week_of_year"])[["FCAPf", "FCA", "k"]]
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
    TimeId = zip(list(wfcapf.year_of_year), list(wfcapf.week_of_year))
    mapingdict = dict(zip(TimeId, list(wfcapf.k)))
    f["Weeklyk"] = f.set_index(["year_of_year", "week_of_year"]).index.map(mapingdict)

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
(df[df.symbol == "خگستر"].id.iloc[0], df[df.symbol == "خودرو"].id.iloc[0])


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(149)
S_g = gdata.get_group(139)


FCAPf(S_g, g)
#%%
