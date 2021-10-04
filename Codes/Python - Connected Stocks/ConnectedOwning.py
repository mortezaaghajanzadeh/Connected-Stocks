# %%
import pandas as pd


# %%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"

df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")

df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)

df = df[df.jalaliDate < 14000000]
try:
    df = df.drop(columns = ['Delta_Trunover'])
except:
    1+2
#%%
df = df.rename(columns = 
    {
        '4_Residual' : '4-Residual',
        '5_Residual' : '5-Residual',
        '6_Residual' : '6-Residual',
        '2_Residual' : '2-Residual',
        '5Lag_Residual' : '5Lag-Residual',
        'Delta_TurnOver':'Delta_Trunover'
    }
)
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

    glist = [
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
        "Percentile_Rank_x",
        "Percentile_Rank_y",
        "BookToMarket_x",
        "BookToMarket_y",
        'TurnOver_x',
        'Amihud_x',
        'volume_x',
        'value_x',
        'TurnOver_y',
        'Amihud_y',
        'volume_y',
        'value_y',
        
    ]
    f = (
        a.groupby(glist)[["FCAPf", "FCA", "Holder_act_y", "Holder_act_x", "Holder_x"]]
        .sum()
        .reset_index()
    )
    mlist = [
        "BGId_x",
        "BGId_y",
        "position_x",
        "position_y",
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
    ]

    for col in mlist:
        mapdict = dict(zip(a.date, a[col]))
        f[col] = f.date.map(mapdict)
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
                'TurnOver_x',
                'Amihud_x',
                'volume_x',
                'value_x',
                'TurnOver_y',
                'Amihud_y',
                'volume_y',
                'value_y',
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
        'TurnOver_x',
        'Amihud_x',
        'volume_x',
        'value_x',
        'TurnOver_y',
        'Amihud_y',
        'volume_y',
        'value_y',
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
            ]
        ]
        .corr()
        .reset_index()
    )

    for i in [
        "2-Residual",
        "4-Residual",
        "5-Residual",
        "6-Residual",
        "5Lag-Residual",
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
                'TurnOver_x',
                'Amihud_x',
                'volume_x',
                'value_x',
                'TurnOver_y',
                'Amihud_y',
                'volume_y',
                'value_y',
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
        'TurnOver_x',
        'Amihud_x',
        'volume_x',
        'value_x',
        'TurnOver_y',
        'Amihud_y',
        'volume_y',
        'value_y',
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
            ]
        ]
        .corr()
        .reset_index()
    )
    for i in [
        "2-Residual",
        "4-Residual",
        "5-Residual",
        "6-Residual",
        "5Lag-Residual",
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


# %%
df[df.symbol == "خگستر"].id.iloc[0], df[df.symbol == "خودرو"].id.iloc[0]


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(158)
S_g = gdata.get_group(148)


a = FCAPf(S_g, g)


# %%
data = pd.DataFrame()
gg = df.groupby(["id"])
# counter = 0
# for i in list(gg.groups.keys()):
#     g = gg.get_group(i)
#     F_id = g.id.iloc[0]
#     print("Id " + str(F_id) , len(data))
#     Next_df = df[df.id > F_id]
#     S_gg = Next_df.groupby(["id"])
#     data = data.append(S_gg.apply(FCAPf, g=g))
#     if len(data) > 3e6:
#         counter += 1
#         data.to_parquet(path + "NormalzedFCAP9.1-part%s.parquet" % counter)
#         data = pd.DataFrame()

# counter += 1
# data.to_parquet(path + "NormalzedFCAP9.1-part%s.parquet" % counter)
#%%
import pickle
from threading import Thread
import threading
def excepthook(args):
    3 == 1 + 2


threading.excepthook = excepthook

def creat_for_id(i,result,df,gg):
    g = gg.get_group(i)
    F_id = g.id.iloc[0]
    print("Id " + str(F_id))
    Next_df = df[df.id > F_id]
    S_gg = Next_df.groupby(["id"])
    result[i] = S_gg.apply(FCAPf, g=g)
j=0
nums = 5
ids = list(gg.groups.keys())
tot = int(len(ids)/nums) + 1
for i in range(tot):
    k = min(j + nums, len(ids))
    print(j, k)
    NoId = ids[j:k]
    threads = {}
    result = {}
    for id in NoId:
        threads[id] = Thread(
            target=creat_for_id,
            args=(id,result,df,gg),
        )
        threads[id].start()
    for i in threads:
        threads[i].join()
        pickle.dump(result[i],
                    open(
                        path + "NormalzedFCAP9.1\\NormalzedFCAP9.1_{}.p".format(i), "wb")
                    )
    j = k

# %%
