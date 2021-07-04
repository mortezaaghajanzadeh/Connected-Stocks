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

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
# n1 = path + "MonthlyNormalzedFCAP6.1" + ".csv"
# df1 = pd.read_csv(n1)

n1 = path + "WeeklyNormalzedFCAP6.1" + ".parquet"
df1 = pd.read_parquet(n1)


# %%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
BGId = pd.read_csv(path + "BGId.csv")
mapdict = dict(zip(BGId.BGId, BGId.uo))
df1["uo_x"] = df1["BGId_x"].map(mapdict)
mapdict = dict(zip(BGId.BGId, BGId.uo))
df1["uo_y"] = df1["BGId_y"].map(mapdict)
df1[["BGId_x", "BGId_y", "uo_x", "uo_y"]].isnull().sum()


#%%
pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
# pathBG = path
n = pathBG + "Grouping_CT.xlsx"
BG = pd.read_excel(n)
BG = BG[BG.listed == 1]
BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3.0)
df1["year"] = round(df1.jalaliDate / 10000, 0)
df1["year"] = df1["year"].astype(int)
tt = BG[BG.year == 1397]
tt["year"] = 1398
BG = BG.append(tt).reset_index(drop=True)

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
pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
# pathBG = path
n = pathBG + "Grouping_CT.xlsx"
DD = pd.read_excel(n)
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

# %%

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
n1 = path + "WeeklyNormalzedFCAP6.1" + ".csv"
df1 = df1[(df1.MonthlyFCAPf < 1) & (df1.WeeklyFCAPf < 1) & (df1.FCAPf < 1)]
gg = df1.groupby(["t_Month"])


def NormalTransform(df_sub):
    col = df_sub.rank(pct=True)
    return (col - col.mean()) / col.std()


df1["WeeklyFCAP*"] = gg["WeeklyFCAPf"].apply(NormalTransform)
df1["WeeklyFCA*"] = gg["WeeklyFCA"].apply(NormalTransform)


#%%

pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
# pathBG = path
n = pathBG + "Grouping_CT.xlsx"
BG = pd.read_excel(n)
BG = BG[BG.listed == 1]
BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3.0)
BG = BG[BG.year >= 1394]
tt = BG[BG.year == 1397]
tt["year"] = 1398
BG = BG.append(tt).reset_index(drop=True)

# %%

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"

n2 = path + "\\balance sheet - 9811" + ".xlsx"
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
# path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
# holder = pd.read_csv(path + "BlockHolders - 800308-990528 - Annual" + ".csv")
# gg = holder.groupby(['symbol','jalaliDate'])
# def s(g):
#     return g.nshares.sum()
# holder = gg.last()
# holder['shrOut'] = gg.apply(s)
# holder = holder.reset_index()
# holder = holder [['symbol', 'jalaliDate', 'year', 'shrOut']]
# fkey = zip(holder.symbol,holder.year)
# mapdict = dict(zip(fkey,holder.shrOut))
# BG['shrOut2'] = BG.set_index(['symbol','year']).index.map(mapdict)

#%%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
price = pd.read_csv(path + "Stocks_Prices_1399-09-24" + ".csv")

price = price[["jalaliDate", "date", "name", "close_price"]]


def vv(row):
    X = row.split("-")
    return int(X[0])


price["year"] = price["jalaliDate"].apply(vv)
price = price.groupby(["name", "year"]).last().reset_index()
price["name"] = price.name.apply(convert_ar_characters)
fkey = zip(price.name, price.year)
mapdict = dict(zip(fkey, price.close_price))
BG["close"] = BG.set_index(["symbol", "year"]).index.map(mapdict)

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
    columns={0: "Number",
             1: "GroupMarketCap", 2: "Totalcfr", 3: "uoMarketCap"}
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


# for t in ['QuantileNumber',
#           'QuantileGroupMarketCap',
#           'QuantileTotalcfr',
#        'QuantileuoMarketCap']:
#     df1[t+"_x"] = df1.groupby('id')[t+"_x"].fillna(method = 'ffill')
#     df1[t+"_y"] = df1.groupby('id')[t+"_y"].fillna(method = 'ffill')

#%%

n = path + "Holder_Residual.parquet"
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


for a in [df1]:
    mapingdict = dict(zip(SData.id, SData.GRank))
    a["id_x"] = a["id_x"].astype(int)
    a["id_y"] = a["id_y"].astype(int)
    a["GRank_x"] = a["id_x"].map(mapingdict)
    a["GRank_y"] = a["id_y"].map(mapingdict)
    a["SameGRank"] = 0
    a.loc[a.GRank_x == a.GRank_y, "SameGRank"] = 1
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
df1 = df1.rename(columns={"WeeklyFCA*": "NWFCA"})
df1['WeeklyCrossOwnership'] = df1.WeeklyCrossOwnership.replace(np.nan,0)
df1 = df1.drop(
    columns=[
        "Monthlyρ_2",
        "Monthlyρ_4",
        "Monthlyρ_5",
        "MonthlyρLag_5",
        "MonthlySizeRatio",
        "MonthlyMarketCap_x",
        "MonthlyMarketCap_y",
        "MonthlyPercentile_Rank_x",
        "MonthlyPercentile_Rank_y",
        "Monthlysize1",
        "Monthlysize2",
        "MonthlySameSize",
        "MonthlyB/M1",
        "MonthlyB/M2",
        "MonthlySameB/M",
        "MonthlyFCAPf",
        "MonthlyFCA",
        "Monthlyρ_2_f",
        "Monthlyρ_4_f",
        "Monthlyρ_5_f",
        "MonthlyρLag_5_f",
        "FCAP*",
        "FCA*",
        "MonthlyFCAP*",
        "MonthlyFCA*",
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
        "5Lag_Residual_x",
        "5Lag_Residual_y",
        "Percentile_Rank_x",
        "Percentile_Rank_y",
        "BookToMarket_x",
        "BookToMarket_y",
        "MonthlyCrossOwnership",
    ]
)
#%%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
n1 = path + "WeeklyNormalzedFCAP6.2" + ".csv"
print(len(df1))
df1.to_csv(n1)
# %%
import pandas as pd
import numpy as np

path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
n1 = path + "MonthlyNormalzedFCAP6.1" + ".csv"
df = pd.read_csv(n1)
# %%
df[["BGId_x", "uo_x"]].drop_duplicates().sort_values(by="BGId_x")
# %%
df1["PairType"] = 0
df1.loc[(df1.GRank_x >= 5) & (df1.GRank_y >= 5), "PairType"] = 2
df1.loc[(df1.GRank_x < 5) & (df1.GRank_y < 5), "PairType"] = 1
df1.groupby("PairType").NMFCA.describe()
