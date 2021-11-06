#%%
import pandas as pd
import numpy as np

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


def add(row):
    if len(row) < 2:
        row = "0" + row
    return row


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
result["Year_Month"] = result.Year_Month.astype(int)
result[result.Year_Month < 139900][
    ["t_Month", "Year_Month"]
].drop_duplicates().sort_values(by=["t_Month"])
#%%
result["Year_Month"] = result.Year_Month.astype(str)
result = result.reset_index(drop=True)

#%%
result["id"] = result["symbol_x"] + "-" + result["symbol_y"]
ids = list(set(result.id))
id = list(range(len(ids)))
mapingdict1 = dict(zip(ids, id))
result["id"] = result["id"].map(mapingdict1)
#%%


def NormalTransform(df_sub):
    col = df_sub.transform("rank")
    return (col - col.mean()) / col.std()


# result = result.reset_index(drop=True)
# gg = result.groupby(["t_Month"])

# result["MonthlyFCAP*"] = gg["MonthlyFCAPf"].apply(NormalTransform)
# result["NMFCA"] = gg["MonthlyFCA"].apply(NormalTransform)

gg = result.groupby(["t_Month"])

result["MonthlyFCAP*"] = gg.MonthlyFCAPf.transform("rank")
gg = result.groupby(["t_Month"])
tempt = gg["MonthlyFCAP*"].mean().to_frame()
mpingdict = dict(zip(tempt.index, tempt["MonthlyFCAP*"]))
result["m"] = result.t_Month.map(mpingdict)
result["MonthlyFCAP*"] = result["MonthlyFCAP*"] - result.m
tempt = gg["MonthlyFCAP*"].std().to_frame()
mpingdict = dict(zip(tempt.index, tempt["MonthlyFCAP*"]))
result["m"] = result.t_Month.map(mpingdict)
result["MonthlyFCAP*"] = result["MonthlyFCAP*"] / result.m


gg = result.groupby(["t_Month"])

result["MonthlyFCA*"] = gg.MonthlyFCA.transform("rank")
gg = result.groupby(["t_Month"])
tempt = gg["MonthlyFCA*"].mean().to_frame()
mpingdict = dict(zip(tempt.index, tempt["MonthlyFCA*"]))
result["m"] = result.t_Month.map(mpingdict)
result["MonthlyFCA*"] = result["MonthlyFCA*"] - result.m
tempt = gg["MonthlyFCA*"].std().to_frame()
mpingdict = dict(zip(tempt.index, tempt["MonthlyFCA*"]))
result["m"] = result.t_Month.map(mpingdict)
result["MonthlyFCA*"] = result["MonthlyFCA*"] / result.m
result = result.drop(columns=["m"])
print("Second step is done")

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
#%%
result.to_parquet(path + "MonthlyAllPairs_1400_06_28.parquet")
#%%
del result
n1 = path + "MonthlyAllPairs_1400_06_28" + ".parquet"
df1 = pd.read_parquet(n1)
df1 = df1[df1.jalaliDate < 13990000]
df1 = df1[df1.jalaliDate > 13930000]

df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")
time = df[["date", "jalaliDate"]].drop_duplicates()
#%%
df["id"] = df.id.astype(int)
mapdict = dict(zip(df.id, df.symbol))
df1["id_x"] = df1.id_x.astype(int)
df1["id_y"] = df1.id_y.astype(int)
df1["symbol_x"] = df1.id_x.map(mapdict)
df1["symbol_y"] = df1.id_y.map(mapdict)
df1[["symbol_x", "symbol_y"]].isnull().sum()
#%%

import requests


def removeSlash(row):
    X = row.split("/")
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[2]) < 2:
        X[2] = "0" + X[2]

    return int(X[0] + X[1] + X[2])


def Overall_index():
    url = (
        r"http://www.tsetmc.com/tsev2/chart/data/Index.aspx?i=32097828799138957&t=value"
    )
    r = requests.get(url)
    jalaliDate = []
    Value = []
    for i in r.text.split(";"):
        x = i.split(",")
        jalaliDate.append(x[0])
        Value.append(float(x[1]))
    df = pd.DataFrame(
        {
            "jalaliDate": jalaliDate,
            "Value": Value,
        },
        columns=["jalaliDate", "Value"],
    )
    df["jalaliDate"] = df.jalaliDate.apply(removeSlash)
    return df


Index = Overall_index()
print(len(Index))
a = df[["date", "jalaliDate"]].drop_duplicates()
mapingdict = dict(zip(a.jalaliDate, a.date))
Index["date"] = Index.jalaliDate.map(mapingdict)
Index = Index.dropna()
Index["year"] = Index.jalaliDate / 1e4
Index["year"] = Index.year.astype(int).astype(str)
Index["Month"] = (
    ((Index.jalaliDate / 1e4 - (Index.jalaliDate / 1e4).astype(int)) * 1e2)
    .astype(int)
    .astype(str)
)


def func(x):
    if len(x) < 2:
        return "0" + x
    return x


Index["Month"] = Index.Month.apply(func)
Index["YearMonth"] = Index.year + Index.Month
Index
#%%

Index = Index[["YearMonth", "Value"]]
Index = Index.drop_duplicates(subset="YearMonth", keep="last")
Index["change"] = Index["Value"].pct_change() * 100
Index["Bullish"] = 0
Index["Bearish"] = 0
Index["change"] = Index.change.shift(-1)

Index.loc[Index.change >= 2, "Bullish"] = 1
Index.loc[Index.change <= -2, "Bearish"] = 1
mapdict = dict(zip(Index.YearMonth, Index.Bullish))
df1["Bullish"] = df1["Year_Month"].map(mapdict)
mapdict = dict(zip(Index.YearMonth, Index.Bearish))
df1["Bearish"] = df1["Year_Month"].map(mapdict)
print(len(df1))
df1 = df1[df1.jalaliDate < 14000000]
df1.isnull().sum()
# %%
BGId = pd.read_csv(path + "BGId.csv")
mapdict = dict(zip(BGId.BGId, BGId.uo))
df1["uo_x"] = df1["BGId_x"].map(mapdict)
mapdict = dict(zip(BGId.BGId, BGId.uo))
df1["uo_y"] = df1["BGId_y"].map(mapdict)
df1[["BGId_x", "BGId_y", "uo_x", "uo_y"]].isnull().sum()


#%%

pathBG = r"E:\RA_Aghajanzadeh\Data\\"
n = pathBG + "Grouping_CT.xlsx"
BG = pd.read_excel(n)

BG = BG[BG.listed == 1]
BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3)
tt = BG[BG.year == 1398]
tt["year"] = 1399
BG = BG.append(tt).reset_index(drop=True)
df1["year"] = round(df1.jalaliDate / 10000, 0)
df1["year"] = df1["year"].astype(int)


for t in BG.year.unique():
    print(t)
    tempt = BG[BG.year == t].uo.unique()
    df1.loc[(~(df1.uo_x.isin(tempt))) & (df1.year == t), "uo_x"] = np.nan
    df1.loc[(~(df1.uo_x.isin(tempt))) & (df1.year == t), "BGId_x"] = np.nan
    df1.loc[(~(df1.uo_y.isin(tempt))) & (df1.year == t), "uo_y"] = np.nan
    df1.loc[(~(df1.uo_y.isin(tempt))) & (df1.year == t), "BGId_y"] = np.nan

df1.isnull().sum()

# %%
print(len(df1))
df1 = df1.drop_duplicates(subset=["id", "t_Month"])
print(len(df1))
# %%
print(len(df1[(df1.MonthlyFCAPf >= 1)]))
df1 = df1[(df1.MonthlyFCAPf < 1)]
gg = df1.groupby(["t_Month"])


def NormalTransform(df_sub):
    col = df_sub.rank(pct=True)
    return (col - col.mean()) / col.std()


df1["MonthlyFCAP*"] = gg["MonthlyFCAPf"].apply(NormalTransform)
df1["MonthlyFCA*"] = gg["MonthlyFCA"].apply(NormalTransform)


#%%

n = pathBG + "Grouping_CT.xlsx"
BG = pd.read_excel(n)
BG = BG[BG.listed == 1]
BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3.0)
# BG = BG[BG.year >= 1394]


# %%
import re


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
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))

n2 = pathBG + "\\balance sheet - 9811" + ".xlsx"
df2 = pd.read_excel(n2)
df2 = df2.iloc[:, [0, 4, 18]]


def vv(row):
    X = row.split("/")
    return int(X[0])


df2.rename(
    columns={
        df2.columns[0]: "symbol",
        df2.columns[1]: "jalaliDate",
        df2.columns[2]: "Capital",
    },
    inplace=True,
)
df2["year"] = df2["jalaliDate"].apply(vv)

df2["symbol"] = df2.symbol.apply(convert_ar_characters)

fkey = zip(df2.symbol, df2.year)
mapdict = dict(zip(fkey, df2.Capital))
BG["shrOut"] = BG.set_index(["symbol", "year"]).index.map(mapdict)

#%%
path = r"E:\RA_Aghajanzadeh\Data\\"
price = pd.read_parquet(path + "Cleaned_Stock_Prices_1400_06_29.parquet")

price = price[["jalaliDate", "date", "name", "close_price"]]


def vv(row):
    X = row.split("-")
    return int(X[0])


price["year"] = round(price["jalaliDate"] / 100, 0)
price = price.groupby(["name", "year"]).last().reset_index()
price["name"] = price.name.apply(convert_ar_characters)
fkey = zip(price.name, price.year)
mapdict = dict(zip(fkey, price.close_price))
BG["close"] = BG.set_index(["symbol", "year"]).index.map(mapdict)
del price, df2
#%%
len(BG[BG.close.isnull()].symbol.unique())
BG["MarketCap"] = BG["close"] * BG["shrOut"]
BG["uoMarketCap"] = BG["MarketCap"] * BG["cfr"]

gg = BG.groupby(["uo"])


def summary(Sg):
    number = Sg.size
    groupMC = Sg.MarketCap.sum()
    uoCFr = Sg.cfr.sum()
    uoCFrMC = Sg.uoMarketCap.sum()
    return pd.Series(data=[number, groupMC, uoCFr, uoCFrMC])


gg = BG.groupby(["uo", "year"])
sResult = gg.apply(summary).reset_index()
sResult = sResult.rename(
    columns={0: "Number", 1: "GroupMarketCap", 2: "Totalcfr", 3: "uoMarketCap"}
)


def Number(g):
    g["QuantileNumber"] = np.nan
    for i in range(1, 5):
        g.loc[
            g.Number >= g.Number.quantile(0.25 * (i - 1)),
            "QuantileNumber",
        ] = i
    return g


def GroupMarketCap(g):
    g["QuantileGroupMarketCap"] = np.nan
    for i in range(1, 5):
        g.loc[
            g.GroupMarketCap >= g.GroupMarketCap.quantile(0.25 * (i - 1)),
            "QuantileGroupMarketCap",
        ] = i
    return g


def Totalcfr(g):
    g["QuantileTotalcfr"] = np.nan
    for i in range(1, 5):
        g.loc[
            g.Totalcfr >= g.Totalcfr.quantile(0.25 * (i - 1)),
            "QuantileTotalcfr",
        ] = i
    return g


def uoMarketCap(g):
    g["QuantileuoMarketCap"] = np.nan
    for i in range(1, 5):
        g.loc[
            g.uoMarketCap >= g.uoMarketCap.quantile(0.25 * (i - 1)),
            "QuantileuoMarketCap",
        ] = i
    return g


gg = sResult.groupby("year")
sResult = gg.apply(Number)
gg = sResult.groupby("year")
sResult = gg.apply(GroupMarketCap)
gg = sResult.groupby("year")
sResult = gg.apply(Totalcfr)
gg = sResult.groupby("year")
sResult = gg.apply(uoMarketCap)

for t in [
    "QuantileNumber",
    "QuantileGroupMarketCap",
    "QuantileTotalcfr",
    "QuantileuoMarketCap",
]:
    fkey = zip(sResult.uo, sResult.year)
    mapdict = dict(zip(fkey, sResult[t]))
    BG[t] = BG.set_index(["uo", "year"]).index.map(mapdict)
del sResult
del gg
#%%
df1["year"] = round(df1.jalaliDate / 10000, 0)
df1["year"] = df1["year"].astype(int)
for t in [
    "QuantileNumber",
    "QuantileGroupMarketCap",
    "QuantileTotalcfr",
    "QuantileuoMarketCap",
]:
    print(t)
    fkey = zip(BG.uo, BG.year)
    mapdict = dict(zip(fkey, BG[t]))
    df1[t + "_x"] = df1.set_index(["uo_x", "year"]).index.map(mapdict)

    fkey = zip(BG.uo, BG.year)
    mapdict = dict(zip(fkey, BG[t]))
    df1[t + "_y"] = df1.set_index(["uo_y", "year"]).index.map(mapdict)

del t
# for t in ['QuantileNumber',
#           'QuantileGroupMarketCap',
#           'QuantileTotalcfr',
#        'QuantileuoMarketCap']:
#     df1[t+"_x"] = df1.groupby('id')[t+"_x"].fillna(method = 'ffill')
#     df1[t+"_y"] = df1.groupby('id')[t+"_y"].fillna(method = 'ffill')

#%%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
n = path + "Holder_Residual_1400_06_28.parquet"
df = pd.read_parquet(n)
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

del df
for a in [df1]:
    mapingdict = dict(zip(SData.id, SData.GRank))
    a["id_x"] = a["id_x"].astype(int)
    a["id_y"] = a["id_y"].astype(int)
    a["GRank_x"] = a["id_x"].map(mapingdict)
    a["GRank_y"] = a["id_y"].map(mapingdict)
    a["SameGRank"] = 0
    a.loc[a.GRank_x == a.GRank_y, "SameGRank"] = 1
del a

#%%
df1 = df1.rename(columns={"MonthlyFCA*": "NMFCA"})
df1["MonthlyCrossOwnership"] = df1.MonthlyCrossOwnership.replace(np.nan, 0)
#%%
df1["sBgroup"] = 0
df1.loc[df1.uo_x == df1.uo_y, "sBgroup"] = 1
df1.loc[df1.uo_x.isnull(), "sBgroup"] = 0
df1.loc[df1.uo_y.isnull(), "sBgroup"] = 0
# df1.loc[df1.year<BG.year.min(),'sBgroup'] = np.nan
df1.sBgroup.isnull().sum()
# %%
df1 = df1.rename(columns={"4rdQarter": "ForthQuarter", "2rdQarter": "SecondQuarter"})
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
n1 = path + "MonthlyNormalzedALLFCAP9.2" + ".csv"
print(len(df1))
df1.to_csv(n1)
n1 = path + "MonthlyNormalzedAllFCAP9.2" + ".parquet"
print(len(df1))
df1.to_parquet(n1)
# %%
