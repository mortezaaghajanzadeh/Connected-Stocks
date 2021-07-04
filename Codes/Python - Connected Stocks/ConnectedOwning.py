# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import re as ree
from itertools import islice


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
# path = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\\"
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"


# %%

n = path + "Cleaned_Stocks_Holders_1399-09-12_From94.csv"
df = pd.read_csv(n)

df = df.drop(df.loc[df["Holder"] == "شخص حقیقی"].index)
df = df.drop(
    df[
        (df["Trade"] == "No")
        & (
            (df["close_price"] == 10)
            | (df["close_price"] == 1000)
            | (df["close_price"] == 10000)
            | (df["close_price"] == 100000)
        )
    ].index
)
df = df.drop(df[(df["symbol"] == "وقوام") & (df["close_price"] == 1000)].index)
symbols = [
    "سپرده",
    "هما",
    "وهنر-پذیره",
    "نکالا",
    "تکالا",
    "اکالا",
    "توسعه گردشگری ",
    "وآفر",
    "ودانا",
    "نشار",
    "نبورس",
    "چبسپا",
    "بدکو",
    "چکارم",
    "تراک",
    "کباده",
    "فبستم",
    "تولیددارو",
    "قیستو",
    "خلیبل",
    "پشاهن",
    "قاروم",
    "هوایی سامان",
    "کورز",
    "شلیا",
    "دتهران",
    "نگین",
    "کایتا",
    "غیوان",
    "تفیرو",
    "سپرمی",
    "بتک",
]
df = df.drop(df[df["symbol"].isin(symbols)].index)
df = df.drop(df[df.group_name == "صندوق سرمایه گذاری قابل معامله"].index)
df = df.drop(df[(df.symbol == "اتکای") & (df.close_price == 1000)].index)
HolderData = df
df.head()


# %%
n1 = path + "Stocks_Prices_1399-09-12" + ".csv"
df1 = pd.read_csv(n1)

df1["jalaliDate"] = df1["jalaliDate"].apply(vv)
df = df1
symbols = [
    "سپرده",
    "هما",
    "وهنر-پذيره",
    "نکالا",
    "تکالا",
    "اکالا",
    "توسعه گردشگری ",
    "وآفر",
    "ودانا",
    "نشار",
    "نبورس",
    "چبسپا",
    "بدکو",
    "چکارم",
    "تراک",
    "کباده",
    "فبستم",
    "تولیددارو",
    "قیستو",
    "خلیبل",
    "پشاهن",
    "قاروم",
    "هوایی سامان",
    "کورز",
    "شلیا",
    "دتهران",
    "نگین",
    "کایتا",
    "غیوان",
    "تفیرو",
    "سپرمی",
    "بتک",
]
df = df.drop(df[df["name"].isin(symbols)].index)
df = df.drop(df[df.group_name == "صندوق سرمایه گذاری قابل معامله"].index)


df = df.drop(df[(df.name == "اتکای") & (df.close_price == 1000)].index)
df = df.drop_duplicates()
df = (
    df.drop(df.loc[(df["volume"] == 0)].index)
    .sort_values(by=["name", "jalaliDate"])
    .rename(columns={"name": "symbol"})
)
df = DriveYearMonthDay(df)

df.columns


# %%
PriceData = pd.DataFrame()
PriceData = PriceData.append(
    df[
        [
            "jalaliDate",
            "date",
            "symbol",
            "close_price",
            "group_id",
            "value",
            "volume",
            "quantity",
        ]
    ]
)
del df
PriceData["date1"] = PriceData["date"].apply(vv4)
PriceData["date1"] = pd.to_datetime(PriceData["date1"])
PriceData["week_of_year"] = PriceData["date1"].dt.week
PriceData["Month_of_year"] = PriceData["date1"].dt.month
PriceData["year_of_year"] = PriceData["date1"].dt.year
gg = PriceData.groupby("symbol")
PriceData["Ret"] = gg["close_price"].pct_change(periods=1) * 100
PriceData["Amihud"] = abs(PriceData["Ret"]) / PriceData["value"]
PriceData.head()


# %%
n = path + "Factors-Daily.xlsx"
Factors = pd.read_excel(n)
Factors.tail()
PriceData = (
    PriceData.merge(Factors, on=["jalaliDate", "date"])
    .sort_values(by=["symbol", "date"])
    .reset_index(drop=True)
    .dropna()
)

PriceData.head()


# %%
n = path + "RiskFree.xlsx"
df3 = pd.read_excel(n)
df3 = df3.rename(columns={"Unnamed: 2": "Year"})
df3["YM"] = df3["YM"].astype(str)
df3["YM"] = df3["YM"] + "00"
df3["YM"] = df3["YM"].astype(int)
df4 = PriceData
df4["RiskFree"] = np.nan
df4["jalaliDate"] = df4["jalaliDate"].astype(int)
for i in df3.YM:
    df4.loc[df4.jalaliDate >= i, "RiskFree"] = (
        df3.loc[df3["YM"] == i].iloc[0, 1] / 12 / 52 / 7
    )


PriceData = df4
del df4
PriceData["EMarketRet"] = PriceData["Market_return"] - PriceData["RiskFree"]
PriceData["ERet"] = PriceData["Ret"] - PriceData["RiskFree"]

PriceData.head()
#%%

df = pd.DataFrame()
df = df.append(PriceData)


df["year"] = round(df.jalaliDate / 10000, 0)
df["year"] = df["year"].astype(int)


fkey = zip(list(HolderData.symbol), list(HolderData.date))
mapingdict = dict(zip(fkey, HolderData.shrout))
df["shrout"] = df.set_index(["symbol", "date"]).index.map(mapingdict)
df["shrout"] = df.groupby("symbol")["shrout"].fillna(method="ffill")
df["shrout"] = df.groupby("symbol")["shrout"].fillna(method="backfill")

pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
pathBG = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\\"
n = pathBG + "Grouping_CT.xlsx"
BG = pd.read_excel(n)
uolist = (
    BG[BG.listed == 1]
    .groupby(["uo", "year"])
    .filter(lambda x: x.shape[0] >= 3)
    .uo.unique()
)
print(len(BG))
BG = BG[BG.uo.isin(uolist)]
print(len(BG))
BGroup = set(BG["uo"])
names = sorted(BGroup)
ids = range(len(names))
mapingdict = dict(zip(names, ids))
BG["BGId"] = BG["uo"].map(mapingdict)

tt = BG[BG.year == 1397]
tt["year"] = 1398
BG = BG.append(tt).reset_index(drop=True)
tt = BG[BG.year == 1398]
tt["year"] = 1399
BG = BG.append(tt).reset_index(drop=True)

BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3)
for i in ["uo", "cfr", "cr"]:
    print(i)
    fkey = zip(list(BG.symbol), list(BG.year))
    mapingdict = dict(zip(fkey, BG[i]))
    df[i] = df.set_index(["symbol", "year"]).index.map(mapingdict)

df = df[~df.uo.isnull()]
pdf = df[["date", "symbol", "close_price"]].drop_duplicates()
pdf["Return"] = pdf.groupby("symbol").close_price.pct_change()

fkey = zip(list(pdf.symbol), list(pdf.date))
mapingdict = dict(zip(fkey, pdf.Return))
df["Return"] = df.set_index(["symbol", "date"]).index.map(mapingdict)  # %%
df = df[
    [
        "date",
        "symbol",
        "jalaliDate",
        "shrout",
        "close_price",
        "uo",
        "cfr",
        "cr",
        "Return",
    ]
].drop_duplicates()
df["MarketCap"] = df["shrout"] * df["close_price"]


def UoWeight(sg):
    sg["WinUoP"] = sg["MarketCap"] * sg["cr"]
    sg["UoP"] = sg["WinUoP"].sum()
    sg["WinUoP"] = sg["WinUoP"] / (sg["WinUoP"].sum()) * 100

    sg["UoPR"] = sg["WinUoP"] * sg["Return"]
    sg["UoPR"] = sg["UoPR"].sum()
    return sg


def DailyCalculation(g):
    print(g.name)
    # Weight in Uo's portfolio
    Sg = g.groupby("uo")
    t = Sg.apply(UoWeight)
    t = t[["date", "uo", "UoP", "UoPR"]]
    return t


gg = df.groupby("date")
data = gg.apply(DailyCalculation)
#%%

PriceData["jalaliDate"] = PriceData["jalaliDate"].astype(int)
PriceData["year"] = round(PriceData.jalaliDate / 10000, 0)
PriceData["year"] = PriceData["year"].astype(int)

fkey = zip(list(BG.symbol), list(BG.year))
mapingdict = dict(zip(fkey, BG["uo"]))
PriceData["uo"] = PriceData.set_index(["symbol", "year"]).index.map(mapingdict)

fkey = zip(list(data.uo), list(data.date))
mapingdict = dict(zip(fkey, data.UoPR))
PriceData["UoPR"] = PriceData.set_index(["uo", "date"]).index.map(mapingdict)

PriceData["UoPR"] = PriceData["UoPR"].fillna(0)

PriceData = PriceData[PriceData.year >= BG.year.min()]
PriceData["EUoPR"] = PriceData.UoPR - PriceData.RiskFree


# %%

n1 = path + "Industry indexes 1399-09-28.csv"
df1 = pd.read_csv(n1)
df1.date = df1.date.apply(vv3)
df1 = df1.drop(columns=["Unnamed: 0"])
df1 = df1.drop(df1[(df1.index_id == "EWI") | (df1.index_id == "overall_index")].index)
df1.index_id = df1.index_id.astype(int)
df1.date = df1.date.astype(int)
gg = df1.groupby("index_id")
df1["gReturn"] = gg["index"].pct_change(periods=1) * 100
fkey = zip(list(df1.index_id), list(df1.date))
mapingdict = dict(zip(fkey, df1["gReturn"]))
PriceData["gReturn"] = PriceData.set_index(["group_id", "jalaliDate"]).index.map(
    mapingdict
)
PriceData["EgReturn"] = PriceData["gReturn"] - PriceData["RiskFree"]
PriceData["year_of_year"] = PriceData["year_of_year"].astype(str)
PriceData["Month_of_year"] = PriceData["Month_of_year"].astype(str)


def v2(X):
    if len(X) < 2:
        return "0" + X
    return X


PriceData["Month_of_year"] = PriceData["Month_of_year"].apply(v2)
PriceData["YearMonth"] = PriceData["year_of_year"] + PriceData["Month_of_year"]
PriceData.head()


# %%


def ResidualFactor(g):
    print(g.name)
    t = pd.DataFrame()
    t = t.append(g)
    if len(t) < 20:
        print("NO")
        return pd.DataFrame()
    gg2 = g.groupby("YearMonth")
    t["6_Residual"] = (
        gg2.apply(SixFactor, df=g).to_frame().reset_index().set_index("level_1")[0]
    )
    t["5_Residual"] = (
        gg2.apply(FiveFactor, df=g).to_frame().reset_index().set_index("level_1")[0]
    )
    t["4_Residual"] = (
        gg2.apply(FourFactor, df=g).to_frame().reset_index().set_index("level_1")[0]
    )
    t["2_Residual"] = (
        gg2.apply(TwoFactor, df=g).to_frame().reset_index().set_index("level_1")[0]
    )
    t["5Lag_Residual"] = (
        gg2.apply(FiveFactorLag, df=g).to_frame().reset_index().set_index("level_1")[0]
    )
    return t


def SixFactor(g, df):
    lis = set(df[df.YearMonth <= g.name].YearMonth)
    lis = list(sorted(lis, reverse=True))
    lis = list(islice(lis, 0, 3))
    df = df[df.YearMonth.isin(lis)]
    alpha, beta1, beta2, beta3, beta4, beta5, beta6 = SixFactorReg(df)
    return g["ERet"] - (
        alpha
        + beta1 * g["EMarketRet"]
        + beta2 * g["HML"]
        + beta3 * g["SMB"]
        + beta4 * g["Winner_Loser"]
        + beta5 * g["EgReturn"]
        + beta6 * g["EUoPR"]
    )


def SixFactorReg(g):
    try:
        g = g[
            ["ERet", "EMarketRet", "HML", "SMB", "Winner_Loser", "EgReturn", "EUoPR"]
        ].dropna()
        y = g["ERet"]
        x = g[["EMarketRet", "HML", "SMB", "Winner_Loser", "EgReturn", "EUoPR"]]
        OLSReg = LinearRegression(fit_intercept=True).fit(x, y)
        beta1, beta2, beta3, beta4, beta5, beta6 = OLSReg.coef_
        alpha = OLSReg.intercept_

    except:
        alpha, beta1, beta2, beta3, beta4, beta5, beta6 = (
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        )
    return alpha, beta1, beta2, beta3, beta4, beta5, beta6


def FiveFactor(g, df):
    lis = set(df[df.YearMonth <= g.name].YearMonth)
    lis = list(sorted(lis, reverse=True))
    lis = list(islice(lis, 0, 3))
    df = df[df.YearMonth.isin(lis)]
    alpha, beta1, beta2, beta3, beta4, beta5 = FiveFactorReg(df)
    return g["ERet"] - (
        alpha
        + beta1 * g["EMarketRet"]
        + beta2 * g["HML"]
        + beta3 * g["SMB"]
        + beta4 * g["Winner_Loser"]
        + beta5 * g["EgReturn"]
    )


def FiveFactorReg(g):
    try:
        g = g[["ERet", "EMarketRet", "HML", "SMB", "Winner_Loser", "EgReturn"]].dropna()
        y = g["ERet"]
        x = g[["EMarketRet", "HML", "SMB", "Winner_Loser", "EgReturn"]]
        OLSReg = LinearRegression(fit_intercept=True).fit(x, y)
        beta1, beta2, beta3, beta4, beta5 = OLSReg.coef_
        alpha = OLSReg.intercept_

    except:
        alpha, beta1, beta2, beta3, beta4, beta5 = (
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        )
    return alpha, beta1, beta2, beta3, beta4, beta5


def FourFactor(g, df):
    lis = set(df[df.YearMonth <= g.name].YearMonth)
    lis = list(sorted(lis, reverse=True))
    lis = list(islice(lis, 0, 3))
    df = df[df.YearMonth.isin(lis)]
    alpha, beta1, beta2, beta3, beta4 = FourFactorReg(df)
    return g["ERet"] - (
        alpha
        + beta1 * g["EMarketRet"]
        + beta2 * g["HML"]
        + beta3 * g["SMB"]
        + beta4 * g["Winner_Loser"]
    )


def FourFactorReg(g):
    try:
        g = g[["ERet", "EMarketRet", "HML", "SMB", "Winner_Loser"]].dropna()
        y = g["ERet"]
        x = g[["EMarketRet", "HML", "SMB", "Winner_Loser"]]
        OLSReg = LinearRegression(fit_intercept=True).fit(x, y)
        beta1, beta2, beta3, beta4 = OLSReg.coef_
        alpha = OLSReg.intercept_

    except:
        alpha, beta1, beta2, beta3, beta4 = np.nan, np.nan, np.nan, np.nan, np.nan
    return alpha, beta1, beta2, beta3, beta4


def TwoFactor(g, df):
    lis = set(df[df.YearMonth <= g.name].YearMonth)
    lis = list(sorted(lis, reverse=True))
    lis = list(islice(lis, 0, 3))
    df = df[df.YearMonth.isin(lis)]
    alpha, beta1, beta2 = TwoFactorReg(df)
    return g["ERet"] - (alpha + beta1 * g["EMarketRet"] + beta2 * g["EgReturn"])


def TwoFactorReg(g):
    try:
        g = g[["ERet", "EMarketRet", "EgReturn"]].dropna()
        y = g["ERet"]
        x = g[["EMarketRet", "EgReturn"]]
        OLSReg = LinearRegression(fit_intercept=True).fit(x, y)
        beta1, beta2 = OLSReg.coef_
        alpha = OLSReg.intercept_

    except:
        alpha, beta1, beta2 = np.nan, np.nan, np.nan
    return alpha, beta1, beta2


def FiveFactorLag(g, df):
    lis = set(df[df.YearMonth <= g.name].YearMonth)
    lis = list(sorted(lis, reverse=True))
    lis = list(islice(lis, 0, 3))
    df = df[df.YearMonth.isin(lis)]
    alpha, beta1, beta2, beta3, beta4, beta5, beta6, beta7 = FiveFactorLagReg(df)
    return g["ERet"] - (
        alpha
        + beta1 * g["EMarketRet"]
        + beta2 * g["HML"]
        + beta3 * g["SMB"]
        + beta4 * g["Winner_Loser"]
        + beta5 * g["EgReturn"]
        + beta6 * g["EMarketRetLag"]
        + beta7 * g["EgReturnLag"]
    )


def FiveFactorLagReg(g):
    try:
        g = g[
            [
                "ERet",
                "EMarketRet",
                "HML",
                "SMB",
                "Winner_Loser",
                "EgReturn",
                "EMarketRetLag",
                "EgReturnLag",
            ]
        ].dropna()
        y = g["ERet"]
        x = g[
            [
                "EMarketRet",
                "HML",
                "SMB",
                "Winner_Loser",
                "EgReturn",
                "EMarketRetLag",
                "EgReturnLag",
            ]
        ]
        OLSReg = LinearRegression(fit_intercept=True).fit(x, y)
        beta1, beta2, beta3, beta4, beta5, beta6, beta7 = OLSReg.coef_
        alpha = OLSReg.intercept_

    except:
        alpha, beta1, beta2, beta3, beta4, beta5, beta6, beta7 = (
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        )
    return alpha, beta1, beta2, beta3, beta4, beta5, beta6, beta7


# %%
wg = PriceData.groupby(["symbol"])
PriceData["EMarketRetLag"] = wg.EMarketRet.shift(1)
PriceData["EgReturnLag"] = wg.EgReturn.shift(1)
wg = PriceData.groupby(["symbol"])
re = wg.apply(ResidualFactor)

re = re.reset_index(drop=True)
col = "symbol"
re[col] = re[col].apply(lambda x: convert_ar_characters(x))


# %%
residuals = re[re.jalaliDate > 13940000]
del re
fkey = zip(list(residuals.symbol), list(residuals.date))
mapingdict = dict(zip(fkey, residuals["4_Residual"]))
HolderData["4_Residual"] = HolderData.set_index(["symbol", "date"]).index.map(
    mapingdict
)
print("4_Residual done")
fkey = zip(list(residuals.symbol), list(residuals.date))
mapingdict = dict(zip(fkey, residuals["5_Residual"]))
HolderData["5-Residual"] = HolderData.set_index(["symbol", "date"]).index.map(
    mapingdict
)
print("5-Residual done")
fkey = zip(list(residuals.symbol), list(residuals.date))
mapingdict = dict(zip(fkey, residuals["2_Residual"]))
HolderData["2-Residual"] = HolderData.set_index(["symbol", "date"]).index.map(
    mapingdict
)
print("2-Residual done")
fkey = zip(list(residuals.symbol), list(residuals.date))
mapingdict = dict(zip(fkey, residuals["Ret"]))
HolderData["Ret"] = HolderData.set_index(["symbol", "date"]).index.map(mapingdict)
print("Ret done")
fkey = zip(list(PriceData.symbol), list(PriceData.date))
mapingdict = dict(zip(fkey, PriceData["Amihud"]))
HolderData["Amihud"] = HolderData.set_index(["symbol", "date"]).index.map(mapingdict)
print("Amihud")

print("4_Residual done")

fkey = zip(list(residuals.symbol), list(residuals.date))
mapingdict = dict(zip(fkey, residuals["5Lag_Residual"]))
HolderData["5Lag_Residual"] = HolderData.set_index(["symbol", "date"]).index.map(
    mapingdict
)
print("5Lag_Residual done")

HolderData.head()

# %%
df = HolderData


# %%
Holders = list(set(df.Holder))
Holders.sort()
ids = list(range(len(Holders)))
mapingdict = dict(zip(Holders, ids))
df["Holder_id"] = df["Holder"].map(mapingdict)

symbols = list(set(df.symbol))
symbols.sort()
ids = list(range(len(symbols)))
mapingdict = dict(zip(symbols, ids))
df["id"] = df["symbol"].map(mapingdict)


# %%
df["date1"] = df["date"].apply(vv4)
df["date1"] = pd.to_datetime(df["date1"])
df["week_of_year"] = df["date1"].dt.week
df["month_of_year"] = df["date1"].dt.month
df["year_of_year"] = df["date1"].dt.year


# %%
df["MarketCap"] = df["close_price"] * df["shrout"]
market = (
    df.groupby(["date", "symbol"])
    .first()
    .reset_index()[["jalaliDate", "date", "symbol", "MarketCap"]]
)
gm = market.groupby(["date"])

market["Percentile_Rank"] = gm.MarketCap.rank(pct=True)
fkey = zip(list(market.symbol), list(market.date))
mapingdict = dict(zip(fkey, market["Percentile_Rank"]))
df["Percentile_Rank"] = df.set_index(["symbol", "date"]).index.map(mapingdict)

df.head()


# %%
n2 = path + "\\balance sheet - 9811" + ".xlsx"
df2 = pd.read_excel(n2)
df2 = df2.iloc[:, [0, 4, 13, -7]]
df2.rename(
    columns={
        df2.columns[0]: "symbol",
        df2.columns[1]: "date",
        df2.columns[2]: "BookValue",
        df2.columns[3]: "Capital",
    },
    inplace=True,
)
# df2['shrout'] = df2['Capital'] * 100
df2["Year"] = df2["date"].apply(vv5)
df2["Year"] = df2["Year"].astype(str)
df2 = df2.drop(columns=["date", "Capital"])
col = "symbol"
df2[col] = df2[col].apply(lambda x: convert_ar_characters(x))

df = DriveYearMonthDay(df)
df = df.merge(df2, on=["symbol", "Year"], how="left")
df["BookValue"] = df["BookValue"].fillna(method="ffill")
df = df.drop(columns=["Year", "Month", "Day"])
df["BookToMarket"] = df["MarketCap"] / 1e6 / df["BookValue"]


gg = df.groupby("date")
df["BookToMarket"] = gg.BookToMarket.rank(pct=True)

df.head()

df.columns


# %%
HolderData["Percent_Change"] = HolderData["Percent_Change"].replace("-", np.nan)
HolderData["Percent_Change"] = HolderData["Percent_Change"].astype(float)
aa = (
    HolderData.groupby("Holder_id")
    .Percent_Change.mean()
    .to_frame()
    .sort_values(by=["Percent_Change"])
)
aa = aa[~aa.Percent_Change.isnull()].reset_index()
aa["Holder_act"] = 0
aa.loc[aa.Percent_Change > aa.Percent_Change.median(), "Holder_act"] = 1
mapingdict = dict(zip(aa["Holder_id"], aa["Holder_act"]))
df["Holder_act"] = df["Holder_id"].map(mapingdict)

df["year"] = df.jalaliDate.astype(str)
df["year"] = df.year.str[0:4]
df["year"] = df["year"].astype(int)
df.head()


# %%
# pathBG = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
pathBG = path
n = pathBG + "Grouping_CT.xlsx"
BG = pd.read_excel(n)
BG = BG[BG.listed == 1]
BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3)

BGroup = set(BG["uo"])
names = sorted(BGroup)
ids = range(len(names))
mapingdict = dict(zip(names, ids))
BG["BGId"] = BG["uo"].map(mapingdict)

tt = BG[BG.year == 1397]
tt["year"] = 1398
BG = BG.append(tt).reset_index(drop=True)


# %%
fkey = zip(list(BG.symbol), list(BG.year))
mapingdict = dict(zip(fkey, BG["BGId"]))
df["BGId"] = df.set_index(["symbol", "year"]).index.map(mapingdict)
fkey = zip(list(BG.symbol), list(BG.year))
mapingdict = dict(zip(fkey, BG["position"]))
df["position"] = df.set_index(["symbol", "year"]).index.map(mapingdict)
fkey = zip(list(BG.symbol), list(BG.year))
mapingdict = dict(zip(fkey, BG["uo"]))
df["uo"] = df.set_index(["symbol", "year"]).index.map(mapingdict)


# %%
# def fill(gg):
#     print(gg.name, end="\r", flush=True)
#     gg["BGId"] = gg["BGId"].fillna(method="ffill")
#     gg["position"] = gg["position"].fillna(method="ffill")
#     gg["uo"] = gg["uo"].fillna(method="ffill")
#     return gg


# df = df.groupby("symbol").apply(fill)

# %%
del mapingdict
del gg
del PriceData
len(df)

# %%
# df.to_csv(path  + 'Holder_Residual.csv',index = False)
df.to_parquet(path + "Holder_Residual.parquet")


# %%
#
# df = pd.read_csv(path + 'Holder_Residual.csv')
df = pd.read_parquet(path + "Holder_Residual.parquet")
df.head()


# %%

df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)
df.head()
df = df[df.jalaliDate < 13990000]


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
