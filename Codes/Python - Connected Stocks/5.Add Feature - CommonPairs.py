#%%
import pandas as pd
import numpy as np
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


#%%

path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"


#%%


Monthly = pd.read_pickle(path + "mergerd_first_step_monthly_part_{}.p".format(1)).drop(
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

#%%
Monthly[Monthly.t_Month >59][["t_Month", "Year_Month"]].drop_duplicates().sort_values(by=["t_Month"])

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


Monthly = firstStep(Monthly)
#%%
Monthly[Monthly.t_Month >60][["t_Month", "Year_Month","Monthlyρ_5"]].drop_duplicates().sort_values(by=["t_Month"])

#%%
# Weekly = SecondStep(Weekly)


def NormalTransform(df_sub):
    print(df_sub.name)
    col = df_sub.transform("rank")
    return (col - col.mean()) / col.std()


print("First step is done")
gg = Monthly.groupby(["t_Month"])

Monthly["MonthlyFCAP*"] = gg.MonthlyFCAPf.transform("rank")
gg = Monthly.groupby(["t_Month"])
tempt = gg["MonthlyFCAP*"].mean().to_frame()
mpingdict = dict(zip(tempt.index, tempt["MonthlyFCAP*"]))
Monthly["m"] = Monthly.t_Month.map(mpingdict)
Monthly["MonthlyFCAP*"] = Monthly["MonthlyFCAP*"] - Monthly.m
tempt = gg["MonthlyFCAP*"].std().to_frame()
mpingdict = dict(zip(tempt.index, tempt["MonthlyFCAP*"]))
Monthly["m"] = Monthly.t_Month.map(mpingdict)
Monthly["MonthlyFCAP*"] = Monthly["MonthlyFCAP*"] / Monthly.m


gg = Monthly.groupby(["t_Month"])

Monthly["MonthlyFCA*"] = gg.MonthlyFCA.transform("rank")
gg = Monthly.groupby(["t_Month"])
tempt = gg["MonthlyFCA*"].mean().to_frame()
mpingdict = dict(zip(tempt.index, tempt["MonthlyFCA*"]))
Monthly["m"] = Monthly.t_Month.map(mpingdict)
Monthly["MonthlyFCA*"] = Monthly["MonthlyFCA*"] - Monthly.m
tempt = gg["MonthlyFCA*"].std().to_frame()
mpingdict = dict(zip(tempt.index, tempt["MonthlyFCA*"]))
Monthly["m"] = Monthly.t_Month.map(mpingdict)
Monthly["MonthlyFCA*"] = Monthly["MonthlyFCA*"] / Monthly.m
Monthly = Monthly.drop(columns=["m"])
print("Second step is done")
Monthly[Monthly.t_Month >60][["t_Month", "Year_Month","Monthlyρ_5"]].drop_duplicates().sort_values(by=["t_Month"])


#%%
df = pd.read_parquet(path + "Holder_Residual_1400_10_06.parquet")
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
# for a in [Monthly, Weekly]:
for a in [Monthly]:
    mapingdict = dict(zip(SData.id, SData.GRank))
    a["GRank_x"] = a["id_x"].map(mapingdict)
    a["GRank_y"] = a["id_y"].map(mapingdict)
    a["SameGRank"] = 0
    a.loc[a.GRank_x == a.GRank_y, "SameGRank"] = 1

#%%
Monthly.Monthlyρ_5.isnull().sum()
Monthly[Monthly.Monthlyρ_5 == Monthly.Monthlyρ_5.max()][
    ['symbol_x','symbol_y','Monthlyρ_5','jalaliDate']
]
Monthly2 = Monthly[~Monthly.Monthlyρ_5.isnull()]
Monthly[Monthly.t_Month >60][["t_Month", "Year_Month","Monthlyρ_5"]].drop_duplicates().sort_values(by=["t_Month"])

#%%

n3 = path + "MonthlyNormalzedFCAP9.1"
Monthly.to_parquet(n3 + ".parquet", index=False)
Pairs = Monthly[["id_x", "id_y", "id"]].drop_duplicates().reset_index(drop=True)
del Monthly

# %%
df = pd.read_parquet(path + "Holder_Residual_1400_10_06.parquet")
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
df = df.rename(
    columns={
        "4_Residual": "4-Residual",
        "5_Residual": "5-Residual",
        "6_Residual": "6-Residual",
        "2_Residual": "2-Residual",
        "5Lag_Residual": "5Lag-Residual",
        "Delta_TurnOver": "Delta_Trunover",
        "Month_of_year": "month_of_year",
    }
)

#%%

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


SId = df[["id", "symbol"]].drop_duplicates().reset_index(drop=True)
GData = df[["group_name", "id"]].drop_duplicates().reset_index(drop=True)
timeId = (
    a[["jalaliDate", "date", "t", "t_Week", "t_Month"]]
    .drop_duplicates()
    .sort_values(by=["t"])
)

SId.to_csv(path + "SId" + ".csv", index=False)
GData.to_csv(path + "GData" + ".csv", index=False)
Pairs.to_csv(path + "Pairs" + ".csv", index=False)
timeId.to_csv(path + "timeId" + ".csv", index=False)
df[["BGId", "uo"]].drop_duplicates().dropna().sort_values(by=["BGId"]).to_csv(
    path + "BGId" + ".csv", index=False
)
#%%
del df
n1 = path + "MonthlyNormalzedFCAP9.1" + ".parquet"
df1 = pd.read_parquet(n1)
df1 = df1[df1.jalaliDate < 13990000]
df1 = df1[df1.jalaliDate > 13930000]
df1 = df1[df1.FCA > 0]

df = pd.read_parquet(path + "Holder_Residual_1400_10_06.parquet")
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
BGId = (
    df1[["BGId_x", "uo_x"]]
    .drop_duplicates()
    .rename(columns={"BGId_x": "BGId", "uo_x": "uo"})
    .append(
        df1[["BGId_y", "uo_y"]]
        .drop_duplicates()
        .rename(columns={"BGId_y": "BGId", "uo_y": "uo"})
    )
    .drop_duplicates()
    .reset_index(drop=True)
    .sort_values(by="BGId")
)

bankingUo = [
    "وبصادر",
    "بانک ملی ایران",
    "وبملت",
    "دی",
    "وتجارت",
    "بانک مسکن",
    "بانک صنعت ومعدن",
    "بانک سپه",
]
bankingSymbol = [
    "وملت",
    "وسینا",
    "وپاسار",
    "وبملت",
    "وبصادر",
    "وتجارت",
    "وپست",
    "ومسکن",
    "وحکمت",
    "وزمین",
]
investmentSymbol = [
    "واعتبار",
    "وسپه",
    "ونیکی",
    "والبر",
    "وپترو",
    "وتوشه",
    "وغدیر",
    "ورنا",
    "وبانک",
    "ونفت",
    "وبیمه",
    "وصندوق",
    "وصنعت",
    "ومعادن",
    "وآردل",
    "وتوکا",
    "وبوعلی",
    "واتی",
    "وتوسم",
    "وامید",
    "ونیرو",
    "وساپا",
    "ودی",
    "وشمال",
    "وگستر",
    "وسکاب",
    "ولتجار",
    "وخارزم",
    "وکادو",
    "ومشان",
    "وآفر",
    "وبهمن",
    "وثوق",
    "وسنا",
    "وارس",
    "وجامی",
    "وآتوس",
    "وبرق",
    "وپسا",
    "وسبحان",
    "ومعین",
    "وپویا",
    "وایرا",
    "وآذر",
]
n = pathBG + "Grouping_CT.xlsx"
DD = pd.read_excel(n)
DD = pd.read_excel(n)
DD = DD[DD.listed == 1]
DD = DD.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3)
bankinGroup = list(DD[DD.symbol.isin(bankingSymbol)]["uo"].unique())
invinGroup = list(DD[DD.symbol.isin(investmentSymbol)]["uo"].unique())

BGId["Bank in Group"] = 0
BGId.loc[BGId.uo.isin(bankinGroup), "Bank in Group"] = 1
BGId["Bank is UO"] = 0
BGId.loc[BGId.uo.isin(bankingUo), "Bank is UO"] = 1
BGId["Inv. in Group"] = 0
BGId.loc[BGId.uo.isin(invinGroup), "Inv. in Group"] = 1


mapdict = dict(zip(BGId["BGId"], BGId["Bank in Group"]))
df1["bankinGroup_x"] = df1.BGId_x.map(mapdict)
df1["bankinGroup_y"] = df1.BGId_y.map(mapdict)
mapdict = dict(zip(BGId["BGId"], BGId["Bank is UO"]))
df1["bankingUo_x"] = df1.BGId_x.map(mapdict)
df1["bankingUo_y"] = df1.BGId_y.map(mapdict)
mapdict = dict(zip(BGId["BGId"], BGId["Inv. in Group"]))
df1["invinGroup_x"] = df1.BGId_x.map(mapdict)
df1["invinGroup_y"] = df1.BGId_y.map(mapdict)

df1.isnull().sum()
#%%
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
price = pd.read_parquet(path + "Cleaned_Stock_Prices_14001006.parquet")

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
n = path + "Holder_Residual_1400_10_06.parquet"
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
df1.head()
df1["InvInGroup"] = 0
df1["BankGroup"] = 0
df1["BankInGroup"] = 0
for i in set(BGId.BGId.dropna()):
    dname = "GDummy" + str(int(i))
    df1[dname] = 0
    df1.loc[df1.BGId_x == i, dname] = 1
    df1.loc[df1.BGId_y == i, dname] = 1
    df1.loc[(df1.BGId_x == i) & (df1.invinGroup_x == 1), "InvInGroup"] = 1
    df1.loc[(df1.BGId_y == i) & (df1.invinGroup_y == 1), "InvInGroup"] = 1
    df1.loc[(df1.BGId_x == i) & (df1.bankingUo_x == 1), "BankGroup"] = 1
    df1.loc[(df1.BGId_y == i) & (df1.bankingUo_y == 1), "BankGroup"] = 1
    df1.loc[(df1.bankinGroup_x == i) & (df1.bankinGroup_x == 1), "BankInGroup"] = 1
    df1.loc[(df1.bankinGroup_y == i) & (df1.bankinGroup_y == 1), "BankInGroup"] = 1


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
#%%
df1 = df1.sort_values(by=["id", "t_Month"])
df1["Monthlyρ_5_1"] = df1.groupby("id").Monthlyρ_5.shift(1)
df1["Monthlyρ_5_2"] = df1.groupby("id").Monthlyρ_5.shift(2)
df1["Monthlyρ_5_3"] = df1.groupby("id").Monthlyρ_5.shift(3)
df1["Monthlyρ_5_4"] = df1.groupby("id").Monthlyρ_5.shift(4)
df1["Monthlyρ_5_5"] = df1.groupby("id").Monthlyρ_5.shift(5)
#%%
df1["changedBG"] = 0
df1['SBGperiod'] = 0
df1['changePeriodDummy'] = 0 
df1["sameBgChange"] = 0
df1["becomeSameBG"] = 0
gg = df1.groupby("id")
t = gg.get_group(705)
def changeBg(t):
    print(t.name)
    if t.sBgroup.sum() != len(t) and t.sBgroup.sum() != 0:
        t["changedBG"] = 1
        if t.sBgroup.iloc[0] == 1:
            ind = t.loc[t.sBgroup == 0].t_Month.iloc[0]
            t["sameBgChange"] = 1
            t.loc[t.t_Month >= ind, "changePeriodDummy"] = 1
            t["SBGperiod"] = t.t_Month - ind
        if t.sBgroup.iloc[0] == 0:
            ind = t.loc[t.sBgroup == 1].t_Month.iloc[0]
            t["becomeSameBG"] = 1
            t.loc[t.t_Month >= ind, "changePeriodDummy"] = 1
            t["SBGperiod"] = t.t_Month - ind
    return t
df1 =  gg.apply(changeBg)

#%%
# df1["sameBgChange"] = 0
# df1["becomeSameBG"] = 0
# gg = df1.groupby("id")
# df1["changedBG"] = 0


# def changedBg(t):
#     print(t.name)
#     if t.sBgroup.sum() != len(t) and t.sBgroup.sum() != 0:
#         t["changedBG"] = 1
#         if t.sBgroup.iloc[0] == 1:
#             ind = t.loc[t.sBgroup == 0].index[0]
#             t.loc[t.index >= ind, "sameBgChange"] = 1
#         else:
#             ind = t.loc[t.sBgroup == 1].index[0]
#             t.loc[t.index >= ind, "sameBgChange"] = 1
#             t["becomeSameBG"] = 1
#     return t
#%%
gg = df1.groupby(["t_Month"])
df1['FcaPerncentileRank'] = gg.MonthlyFCA.rank(pct = True)
df1["2rdQarter"] = 0
df1["4rdQarter"] = 0
df1.loc[df1.FcaPerncentileRank >= 0.5, "2rdQarter"] = 1
df1.loc[df1.FcaPerncentileRank >= 0.75, "4rdQarter"] = 1

#%%


def Normalize(df_sub):
    col = df_sub
    return (col - col.mean()) / col.std()


df1["NMFCA2"] = df1["NMFCA"] * df1["NMFCA"]

gg = df1.groupby(["t_Month"])
df1["NMFCA2"] = gg["NMFCA2"].apply(Normalize)
df1.groupby(["t_Month"]).NMFCA2.std()
del gg
#%%
time = df1.drop_duplicates(subset=["jalaliDate", "date"])[["jalaliDate", "date"]]

#%%
mapdict = dict(zip(time.jalaliDate, time.date))
path = r"E:\RA_Aghajanzadeh\Data\PriceTradeData\\"
df = pd.read_parquet(path + "mergerdPriceAllData_cleaned.parquet")


def removedash(row):
    X = row.split("-")
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[2]) < 2:
        X[2] = "0" + X[2]
    return int(X[0] + X[1] + X[2])


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


import re


def _multiple_replace(mapping, text):
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))


df["jalali"] = df.jalaliDate.apply(removedash)
df["name"] = df["name"].apply(lambda x: convert_ar_characters(x))
#%%
df["date"] = df.jalali.map(mapdict)

df = df[~df.ind_buy_count.isnull()].dropna()
df["year"] = round(df.jalali / 10000)
df["year"] = df["year"].astype(int)
df = df[df.year >= df1.year.min()]


def vv4(row):
    row = str(row)
    X = [1, 1, 1]
    X[0] = row[0:4]
    X[1] = row[4:6]
    X[2] = row[6:8]
    return X[0] + "-" + X[1] + "-" + X[2]


df["date1"] = df["date"].apply(vv4)
df["date1"] = pd.to_datetime(df["date1"])
df["week_of_year"] = df["date1"].dt.week
df["Month_of_year"] = df["date1"].dt.month
df["year_of_year"] = df["date1"].dt.year


def BG(df):
    # pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
    pathBG = r"E:\RA_Aghajanzadeh\Data\\"
    n = pathBG + "Grouping_CT.xlsx"
    BG = pd.read_excel(n)
    uolist = (
        BG[BG.listed == 1]
        .groupby(["uo", "year"])
        .filter(lambda x: x.shape[0] >= 3)
        .uo.unique()
    )
    BG = BG[BG.listed == 1]
    BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3)
    print(len(BG))
    BG = BG[BG.uo.isin(uolist)]
    print(len(BG))
    BGroup = set(BG["uo"])
    names = sorted(BGroup)
    ids = range(len(names))
    mapingdict = dict(zip(names, ids))
    BG["BGId"] = BG["uo"].map(mapingdict)

    BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3)
    for i in ["uo", "cfr", "cr"]:
        print(i)
        fkey = zip(list(BG.symbol), list(BG.year))
        mapingdict = dict(zip(fkey, BG[i]))
        df[i] = df.set_index(["name", "year"]).index.map(mapingdict)
    return df


df = BG(df)
df["Grouped"] = 1
df.loc[df.uo.isnull(), "Grouped"] = 0
mlist = [
    "ind_buy_count",
    "ins_buy_count",
    "ind_sell_count",
    "ins_sell_count",
    "ind_buy_volume",
    "ins_buy_volume",
    "ind_sell_volume",
    "ins_sell_volume",
    "ind_buy_value",
    "ins_buy_value",
    "ind_sell_value",
    "ins_sell_value",
]
df["yearMonth"] = round(df.jalali / 100)
df["yearMonth"] = df["yearMonth"].astype(int)
df["yearWeek"] = df["year_of_year"].astype(str) + "-" + df["week_of_year"].astype(str)

#%%
frequency = "yearMonth"
mdf = df.groupby(["name", frequency]).first().drop(columns=["jalali"])
mdf[mlist] = df.groupby(["name", frequency])[mlist].sum()
mdf = mdf.reset_index()
mdf["InsImbalance_count"] = (mdf.ins_buy_count - mdf.ins_sell_count) / (
    mdf.ins_buy_count + mdf.ins_sell_count
)
mdf["InsImbalance_volume"] = (mdf.ins_buy_volume - mdf.ins_sell_volume) / (
    mdf.ins_buy_volume + mdf.ins_sell_volume
)
mdf["InsImbalance_value"] = (mdf.ins_buy_value - mdf.ins_sell_value) / (
    mdf.ins_buy_value + mdf.ins_sell_value
)
mdf = mdf[
    [
        frequency,
        "name",
        "year",
        "uo",
        "cfr",
        "cr",
        "Grouped",
        "InsImbalance_count",
        "InsImbalance_volume",
        "InsImbalance_value",
    ]
].sort_values(by=["name", frequency])
mdf = mdf.reset_index(drop=True)
mdf = mdf[~mdf.InsImbalance_count.isnull()]
mdf
Imbalances = [
    "InsImbalance_count",
    "InsImbalance_volume",
    "InsImbalance_value",
    "Grouped",
]
#%%
gg = mdf.groupby(frequency)


def Pnum(g):
    return len(g[g.InsImbalance_value>0])/len(g)
def Nnum(g):
    return len(g[g.InsImbalance_value<0])/len(g)
def dailyn(g):
    print(g.name)
    Imbalances = [
        "InsImbalance_count",
        "InsImbalance_volume",
        "InsImbalance_value",
        "Grouped",
    ]
    a = g.groupby("uo").apply(Pnum).to_frame().rename(
        columns={0: "Positive"})
    a = a.merge(
        g.groupby("uo").apply(Nnum).to_frame().rename(
        columns={0: "Negative"})
            ,how = "left",on =["uo"])
    # a["Grouped"] = 1
    # a = a.append(
    #     g[g.Grouped == 0][Imbalances].std().to_frame().rename(columns={0: "NotGroup"}).T
    # )
    return a


result = gg.apply(dailyn)
result = result.reset_index().rename(columns={"level_1": "uo"})
result
#%%
a = result.groupby("uo")[['Positive', 'Negative']].mean()
a = a.sort_values(by=['Positive']).dropna()
a
lowlist = list(a[a.Positive <= a.Positive.median()].index)
df1["PositiveSynch"] = 0
df1.loc[df1.uo_x.isin(lowlist), "PositiveSynch"] = 1
df1.loc[df1.uo_y.isin(lowlist), "PositiveSynch"] = 1
mapdict = dict(zip(a.index, a.Positive))
df1["PositiveSynch_x"] = df1.uo_x.map(mapdict)
df1["PositiveSynch_y"] = df1.uo_y.map(mapdict)
#%%

gg = mdf.groupby(frequency)


def daily(g):
    print(g.name)
    Imbalances = [
        "InsImbalance_count",
        "InsImbalance_volume",
        "InsImbalance_value",
        "Grouped",
    ]
    a = g.groupby("uo")[Imbalances].std()
    
    a["Grouped"] = 1
    a = a.append(
        g[g.Grouped == 0][Imbalances].std().to_frame().rename(columns={0: "NotGroup"}).T
    )
    return a


result = gg.apply(daily)
result = result.reset_index().rename(columns={"level_1": "uo"})
#%%

#%%
a = result.groupby("uo")[Imbalances[:-1]].mean()
a = a.sort_values(by=Imbalances[:-1]).dropna()
a
lowlist = list(a[a.InsImbalance_value <= a.InsImbalance_value.median()].index)
df1["lowImbalanceStd"] = 0
df1.loc[df1.uo_x.isin(lowlist), "lowImbalanceStd"] = 1
df1.loc[df1.uo_y.isin(lowlist), "lowImbalanceStd"] = 1
mapdict = dict(zip(a.index, a.InsImbalance_value))
df1["InsImbalance_value_x"] = df1.uo_x.map(mapdict)
df1["InsImbalance_value_y"] = df1.uo_y.map(mapdict)
#%%


#%%
# del result ,a
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
df = pd.read_parquet(path + "Holder_Residual_1400_10_06.parquet")
t = (
    df.drop_duplicates(subset=["symbol"])
    .groupby(["uo"])
    .size()
    .to_frame()
    .sort_values(by=[0])
)
del df
ll = t[t[0] >= t[0].median()].index
df1["BigBusinessGroup"] = 0
df1.loc[df1.uo_x.isin(ll), "BigBusinessGroup"] = 1
df1.loc[df1.uo_y.isin(ll), "BigBusinessGroup"] = 1

#%%


#%%
df1 = df1.rename(columns={"4rdQarter": "ForthQuarter", "2rdQarter": "SecondQuarter"})
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
n1 = path + "MonthlyNormalzedFCAP9.2" + ".parquet"
print(len(df1))
df1.to_parquet(n1)
n1 = path + "MonthlyNormalzedFCAP9.2" + ".csv"
print(len(df1))
df1.to_csv(n1)

# %%
a = result.groupby("uo")[Imbalances[:-1]].mean()
a = a.sort_values(by=Imbalances[:-1]).dropna()
lowlist = list(a[a.InsImbalance_value <= a.InsImbalance_value.median()].index)
a["lowImbalanceStd"] = 0
a.loc[a.index.isin(lowlist), "lowImbalanceStd"] = 1
a.to_csv(path + "lowImbalanceUO.csv")
#%%
result["year"] = result.yearMonth / 100
result["year"] = result.year.astype(int)
gg = result.groupby(["year"])


def lowdummy(g):
    t = g.groupby("uo")[Imbalances[:-1]].mean()
    t = t.sort_values(by=Imbalances[:-1]).dropna()
    lowlist = list(t[t.InsImbalance_value <= t.InsImbalance_value.median()].index)
    t["lowImbalanceStd"] = 0
    t.loc[t.index.isin(lowlist), "lowImbalanceStd"] = 1
    return t


a = gg.apply(lowdummy).reset_index()
a.to_csv(path + "lowImbalanceUO-Annual.csv", index=False)
#%%
# %%
