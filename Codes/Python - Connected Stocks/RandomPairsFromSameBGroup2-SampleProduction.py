# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import random


# %%
# path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
path = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\\"
# df = pd.read_csv(path + 'Holder_Residual.csv')
# n3 = path + 'NormalzedFCAP5.1.csv'


# %%
def RPair(g, Pairs, dgg, timeId, GData):
    if len(g) == 0:
        return
    print(g.name, end="\r", flush=True)
    x = pd.DataFrame()
    RP = x

    CFactor = g[
        [
            "t",
            "FCAPf",
            "FCA",
            "MonthlyFCAPf",
            "MonthlyFCA",
            "WeeklyFCAPf",
            "WeeklyFCA",
            "FCAP*",
            "FCA*",
            "WeeklyFCAP*",
            "WeeklyFCA*",
            "MonthlyFCAP*",
            "MonthlyFCA*",
            "Holder_act",
            "sBgroup",
        ]
    ]
    flag = 0
    j = 1
    dg = x
    S_g = x
    while flag == 0 and j < 100:
        nid_x, nid_y = randomId(g, GData, Pairs)
        if nid_x == "n":
            j += 1
            continue
        dg = dgg.get_group(nid_x)
        S_g = dgg.get_group(nid_y)
        dg = dg.loc[dg.date.isin(g.date)]
        S_g = S_g.loc[S_g.date.isin(g.date)]
        #             print(j , len(dg),len(S_g))
        if len(dg) >= 0.5 * len(g) and len(S_g) >= 0.5 * len(g):
            flag = 1
        j += 1

    if len(dg) < 0.5 * len(g) or len(S_g) < 0.5 * len(g):
        return RP

    RP = RFCAPf(S_g, dg)
    RP = RP.merge(timeId, on="date")
    RP = RP.merge(CFactor, on="t")
    RP["nId"] = str(g.name)

    return RP


def randomId(g, GData, Pairs):
    Gx = set(GData[(GData.BGId == g.BGId_x.iloc[0]) & (GData.id != g.id_y.iloc[0])].id)
    id_x = g.id_x.iloc[0]
    P_x = set(Pairs[Pairs.id_x == id_x].id_y)
    P_x.update(Pairs[Pairs.id_y == id_x].id_x)
    P_x = Gx.difference(P_x)
    P_x = list(P_x)

    Gy = set(GData[(GData.BGId == g.BGId_y.iloc[0]) & (GData.id != g.id_x.iloc[0])].id)
    id_y = g.id_y.iloc[0]
    P_y = set(Pairs[Pairs.id_x == id_y].id_y)
    P_y.update(Pairs[Pairs.id_y == id_y].id_x)
    P_y = Gy.difference(P_y)
    P_y = list(P_y)

    round = max(len(P_x), len(P_y))

    flag = 0
    j = 0
    while flag == 0 and j < round:
        nid_x = P_x[random.randint(0, len(P_x) - 1)]
        nid_y = P_y[random.randint(0, len(P_y) - 1)]
        ns = set(Pairs[Pairs.id_x == nid_x].id_y)
        ns.update(Pairs[Pairs.id_y == nid_x].id_x)
        if nid_y not in ns:
            flag = 1

        j = j + 1
        if flag == 0 and j >= round:
            nid_x, nid_y = "n", "n"

    return nid_x, nid_y


def RFCAPf(S_g, g):
    f = RCalculation(g, S_g)
    if len(f) == 0:
        return f
    f = MonthlyCalculation(f)
    return f


def RCalculation(g, S_g):
    intersection = list(set.intersection(set(S_g.date), set(g.date)))
    g = g.loc[g.date.isin(intersection)].drop(
        columns=[
            "Holder",
            "nshares",
            "type",
            "Percent",
            "Number_Change",
            "Percent_Change",
            "Condition",
            "Trade",
        ]
    )
    S_g = S_g.loc[S_g.date.isin(intersection)].drop(
        columns=[
            "Holder",
            "nshares",
            "type",
            "Percent",
            "Number_Change",
            "Percent_Change",
            "Condition",
            "Trade",
        ]
    )

    a = g.merge(
        S_g, on=["date", "jalaliDate", "week_of_year", "month_of_year", "year_of_year"]
    )

    a["SizeRatio"] = (a["MarketCap_x"]) / (a["MarketCap_y"])
    f = a
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
    f["SameSize"] = f["size2"] - f["size1"]
    f["sgroup"] = 0
    f.loc[f.group_name_x == f.group_name_y, "sgroup"] = 1
    f.loc[f.group_name_x == f.group_name_y, "sgroup"] = 1
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
    ]

    for i in vlist:
        TimeId = zip(list(ff.year_of_year), list(ff.month_of_year))
        mapingdict = dict(zip(TimeId, list(ff[i])))
        f["Monthly" + i] = f.set_index(["year_of_year", "month_of_year"]).index.map(
            mapingdict
        )

    f["Monthlyρ_2_f"] = f["Monthlyρ_2"].shift(-1)
    f["Monthlyρ_4_f"] = f["Monthlyρ_4"].shift(-1)
    f["Monthlyρ_5_f"] = f["Monthlyρ_5"].shift(-1)
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
    return f


# %%
df = pd.read_parquet(path + "Holder_Residual.parquet")
df = df[df.jalaliDate < 13990000]
# df = df.rename(columns = {'4_Residual':'4-Residual'})
df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)
df = df.drop_duplicates(["date", "symbol"])
dgg = df.groupby(["id"])
SId = pd.read_csv(path + "SId" + ".csv")
GData = pd.read_csv(path + "GData" + ".csv")
Pairs = pd.read_csv(path + "Pairs" + ".csv")
timeId = pd.read_csv(path + "timeId" + ".csv")
BG = df[["id", "BGId"]].drop_duplicates().reset_index(drop=True)
m = 10


# %%
n = path + "NormalzedFCAP6.1" + ".parquet"
a = pd.read_parquet(n)
# a = a.rename(columns = {'4_Residual_x':'4-Residual_x','4_Residual_y':'4-Residual_y'})
a = a[
    [
        "t",
        "FCAPf",
        "FCA",
        "MonthlyFCAPf",
        "MonthlyFCA",
        "WeeklyFCAPf",
        "WeeklyFCA",
        "FCAP*",
        "FCA*",
        "WeeklyFCAP*",
        "WeeklyFCA*",
        "MonthlyFCAP*",
        "MonthlyFCA*",
        "Holder_act",
        "sBgroup",
        "id",
        "BGId_x",
        "BGId_y",
        "id_x",
        "id_y",
        "date",
    ]
]
gg = a.groupby("id")
del a


# %%
range(60, 100)[0]


# %%

for morteza in range(60, 100):

    print("Round ", morteza + 1)
    print("Start")
    Rdata = pd.DataFrame()
    Rdata = (
        gg.apply(RPair, GData=BG, Pairs=Pairs, dgg=dgg, timeId=timeId)
        .reset_index()
        .drop(columns=["level_1"])
    )

    print("End")

    dt = Rdata.drop_duplicates(["nId", "t_Month"], keep="last")
    del Rdata
    dt = dt[~dt.nId.isnull()]
    dt = dt.sort_values(by=["id"]).reset_index(drop=True)

    Holders = list(set(dt.nId))
    ids = list(range(len(Holders)))
    mapingdict = dict(zip(Holders, ids))
    dt["MergeId"] = dt["nId"].map(mapingdict)
    dt = dt.drop_duplicates(["MergeId", "t_Month"])

    n3 = path + "RBGMonthlyNormalzedFCAP6.1" + "-Sample" + str(morteza + 1) + ".parquet"
    dt.to_parquet(n3)

    print("RBGMonthly done")
    del dt


# %%
