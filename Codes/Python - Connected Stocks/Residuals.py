#%%

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


def vv3(row):
    X = row.split("/")
    if len(X[0]) < 4:
        X[0] = "13" + X[0]
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[2]) < 2:
        X[2] = "0" + X[2]
    return X[0] + X[1] + X[2]


# %%
path = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\\"
# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"

#%%
n = path + "Cleaned_Stocks_Holders_99_From94.parquet"
df = pd.read_parquet(n)

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
#%%
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
    PriceData.merge(Factors, on=["jalaliDate", "date"], how="left")
    .sort_values(by=["symbol", "date"])
    .reset_index(drop=True)
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

df = pd.DataFrame()
df = df.append(PriceData)


df["year"] = round(df.jalaliDate / 10000, 0)
df["year"] = df["year"].astype(int)


fkey = zip(list(HolderData.symbol), list(HolderData.date))
mapingdict = dict(zip(fkey, HolderData.shrout))
df["shrout"] = df.set_index(["symbol", "date"]).index.map(mapingdict)
df["shrout"] = df.groupby("symbol")["shrout"].fillna(method="ffill")
df["shrout"] = df.groupby("symbol")["shrout"].fillna(method="backfill")

# pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
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
PriceData["year"] = PriceData.jalaliDate / 10000
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

PriceData.to_csv(path + "PriceData.csv", index=False)

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
#%%
re.to_csv(path + "residuals.csv", index=False)
