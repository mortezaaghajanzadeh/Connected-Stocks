import pandas as pd
import pickle
import numpy as np


def FCAPf(S_g, g, AllPair):
    # print(S_g.name)
    intersection = list(set.intersection(set(S_g.date), set(g.date)))
    if len(intersection) == 0:
        #         print('0')
        return
    f = Calculation(g, S_g, intersection, AllPair)
    f = AfterCal(f, g, S_g, intersection)
    return f


def Calculation(g, S_g, intersection, AllPair):
    a = FirstCal(g, S_g, intersection)
    a = FCalculation(a, g, S_g, AllPair)
    if len(a) == 0:
        return a
    f = SecondCal(a)
    return f


def FirstCal(g, S_g, intersection):
    # intersection = list(set.intersection(set(S_g.date), set(g.date)))
    t1 = pd.DataFrame()
    t1 = t1.append(g.loc[g.date.isin(intersection)])
    t1["Holder"] = 0
    t2 = pd.DataFrame()
    t2 = t2.append(S_g.loc[S_g.date.isin(intersection)])
    t2["Holder"] = 0

    a = t1.merge(
        t2,
        on=[
            "Holder_id",
            "date",
            "jalaliDate",
            "week_of_year",
            "month_of_year",
            "year_of_year",
        ],
    )
    a["Holder"] = 1
    return a


def FCalculation(a, g, S_g, AllPair):
    if AllPair:
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
        tempt = pd.DataFrame()
        tempt = tempt.append(a.loc[a.Holder_id_x == a.Holder_id_y])
        tempt["FCAPf"] = (
            tempt["nshares_x"] * tempt["close_price_x"]
            + tempt["nshares_y"] * tempt["close_price_y"]
        ) / (
            tempt["shrout_x"] * tempt["close_price_x"]
            + tempt["shrout_y"] * tempt["close_price_y"]
        )
        tempt["FCA"] = (
            np.sqrt(tempt["nshares_x"] * tempt["close_price_x"])
            + np.sqrt(tempt["nshares_y"] * tempt["close_price_y"])
        ) / (
            np.sqrt(tempt["shrout_x"] * tempt["close_price_x"])
            + np.sqrt(tempt["shrout_y"] * tempt["close_price_y"])
        )
        a["Holder"] = 0
        a.loc[a.Holder_id_x == a.Holder_id_y, "Holder"] = 1
        a.loc[a.Holder_id_x == a.Holder_id_y, "FCAPf"] = tempt["FCAPf"]
        a.loc[a.Holder_id_x == a.Holder_id_y, "FCA"] = tempt["FCA"]
    else:
        a["FCAPf"] = (
            a["nshares_x"] * a["close_price_x"] + a["nshares_y"] * a["close_price_y"]
        ) / (a["shrout_x"] * a["close_price_x"] + a["shrout_y"] * a["close_price_y"])
        a["FCA"] = (
            np.sqrt(a["nshares_x"] * a["close_price_x"])
            + np.sqrt(a["nshares_y"] * a["close_price_y"])
        ) / (
            np.sqrt(a["shrout_x"] * a["close_price_x"])
            + np.sqrt(a["shrout_y"] * a["close_price_y"])
        )
    return a


def SecondCal(a):

    a["SizeRatio"] = (a["MarketCap_x"]) / (a["MarketCap_y"])

    f = (
        a.groupby(["date"])[["FCAPf", "FCA", "Holder_act_y", "Holder_act_x", "Holder"]]
        .sum()
        .reset_index()
    )
    mlist = [
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
        "BGId_x",
        "BGId_y",
        "position_x",
        "position_y",
        "TurnOver_x",
        "Amihud_x",
        "volume_x",
        "value_x",
        "TurnOver_y",
        "Amihud_y",
        "volume_y",
        "value_y",
        "BGId_x",
        "BGId_y",
        "Delta_Trunover_x",
        "Delta_Trunover_y",
        "Delta_Amihud_x",
        "Delta_Amihud_y",
        "Benchmark_Ret_x",
        "Residual_Bench_x",
        "Benchmark_Ret_y",
        "Residual_Bench_y",
    ]
    for i in mlist:
        mapingdict = dict(zip(a.date, a[i]))
        f[i] = f.date.map(mapingdict)

    a = a[["type_x", "type_y"]].drop_duplicates()
    a["Sametype"] = 0
    a.loc[a.type_x == a.type_y, "Sametype"] = 1

    if a["Sametype"].sum() > 0:
        f["Sametype"] = 1
    else:
        f["Sametype"] = 0

    f = f.rename(columns={"Holder": "numberCommonHolder"})

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


def AfterCal(f, g, S_g, intersection):
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
                "TurnOver_x",
                "Amihud_x",
                "volume_x",
                "value_x",
                "TurnOver_y",
                "Amihud_y",
                "volume_y",
                "value_y",
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
        "TurnOver_x",
        "Amihud_x",
        "volume_x",
        "value_x",
        "TurnOver_y",
        "Amihud_y",
        "volume_y",
        "value_y",
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
    f["MonthlyρLag_5_f"] = f["Monthlyρ_5Lag"].shift(-1)
    f["Monthlyρ_turn_f"] = f["Monthlyρ_turn"].shift(-1)
    f["Monthlyρ_amihud_f"] = f["Monthlyρ_amihud"].shift(-1)
    return f


def MonthlyCorr(f):

    fc = (
        f.groupby(["year_of_year", "month_of_year"])[
            [
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
                "Delta_Trunover_x",
                "Delta_Trunover_y",
                "Delta_Amihud_x",
                "Delta_Amihud_y",
                "Residual_Bench_x",
                "Residual_Bench_y",
            ]
        ]
        .corr(min_periods=10)
        .reset_index()
    )

    for i in [
        "2-Residual",
        "4-Residual",
        "5-Residual",
        "6-Residual",
        "5Lag-Residual",
        "Residual_Bench",
    ]:
        cor = fc.loc[fc.level_2 == i + "_y"][
            ["year_of_year", "month_of_year", i + "_x"]
        ].rename(columns={i + "_x": "ρ_" + i.split("-")[0]})
        TimeId = zip(list(cor.year_of_year), list(cor.month_of_year))
        mapingdict = dict(zip(TimeId, list(cor["ρ_" + i.split("-")[0]])))
        f["Monthly" + "ρ_" + i.split("-")[0]] = f.set_index(
            ["year_of_year", "month_of_year"]
        ).index.map(mapingdict)

    turncor = fc.loc[fc.level_2 == "Delta_Trunover_y"][
        ["year_of_year", "month_of_year", "Delta_Trunover_x"]
    ].rename(columns={"Delta_Trunover_x": "ρ_turn"})
    TimeId = zip(list(turncor.year_of_year), list(turncor.month_of_year))
    mapingdict = dict(zip(TimeId, list(turncor.ρ_turn)))
    f["Monthlyρ_turn"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
        mapingdict
    )
    amihudcor = fc.loc[fc.level_2 == "Delta_Amihud_y"][
        ["year_of_year", "month_of_year", "Delta_Amihud_x"]
    ].rename(columns={"Delta_Amihud_x": "ρ_amihud"})
    TimeId = zip(list(amihudcor.year_of_year), list(amihudcor.month_of_year))
    mapingdict = dict(zip(TimeId, list(amihudcor.ρ_amihud)))
    f["Monthlyρ_amihud"] = f.set_index(["year_of_year", "month_of_year"]).index.map(
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
                "TurnOver_x",
                "Amihud_x",
                "volume_x",
                "value_x",
                "TurnOver_y",
                "Amihud_y",
                "volume_y",
                "value_y",
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
        "TurnOver_x",
        "Amihud_x",
        "volume_x",
        "value_x",
        "TurnOver_y",
        "Amihud_y",
        "volume_y",
        "value_y",
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
    f["WeeklyρLag_5_f"] = f["Weeklyρ_5Lag"].shift(-1)
    f["Weeklyρ_turn_f"] = f["Weeklyρ_turn"].shift(-1)
    f["Weeklyρ_amihud_f"] = f["Weeklyρ_amihud"].shift(-1)
    return f


def WeeklyCorr(f):
    fc = (
        f.groupby(["year_of_year", "week_of_year"])[
            [
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
                "Delta_Trunover_x",
                "Delta_Trunover_y",
                "Delta_Amihud_x",
                "Delta_Amihud_y",
                "Residual_Bench_x",
                "Residual_Bench_y",
            ]
        ]
        .corr(min_periods=5)
        .reset_index()
    )
    for i in [
        "2-Residual",
        "4-Residual",
        "5-Residual",
        "6-Residual",
        "5Lag-Residual",
        "Residual_Bench",
    ]:
        cor = fc.loc[fc.level_2 == i + "_y"][
            ["year_of_year", "week_of_year", i + "_x"]
        ].rename(columns={i + "_x": "ρ_" + i.split("-")[0]})
        TimeId = zip(list(cor.year_of_year), list(cor.week_of_year))
        mapingdict = dict(zip(TimeId, list(cor["ρ_" + i.split("-")[0]])))
        f["Weekly" + "ρ_" + i.split("-")[0]] = f.set_index(
            ["year_of_year", "week_of_year"]
        ).index.map(mapingdict)
    turncor = fc.loc[fc.level_2 == "Delta_Trunover_y"][
        ["year_of_year", "week_of_year", "Delta_Trunover_x"]
    ].rename(columns={"Delta_Trunover_x": "ρ_turn"})
    TimeId = zip(list(turncor.year_of_year), list(turncor.week_of_year))
    mapingdict = dict(zip(TimeId, list(turncor.ρ_turn)))
    f["Weeklyρ_turn"] = f.set_index(["year_of_year", "week_of_year"]).index.map(
        mapingdict
    )
    amihudcor = fc.loc[fc.level_2 == "Delta_Amihud_y"][
        ["year_of_year", "week_of_year", "Delta_Amihud_x"]
    ].rename(columns={"Delta_Amihud_x": "ρ_amihud"})
    TimeId = zip(list(amihudcor.year_of_year), list(amihudcor.week_of_year))
    mapingdict = dict(zip(TimeId, list(amihudcor.ρ_amihud)))
    f["Weeklyρ_amihud"] = f.set_index(["year_of_year", "week_of_year"]).index.map(
        mapingdict
    )

    return f
