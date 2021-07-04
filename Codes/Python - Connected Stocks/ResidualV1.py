# %%
import pandas as pd
import numpy as np
import statsmodels.api as sm
from itertools import islice
import re as ree


def DriveYearMonthDay(d):
    d["jalaliDate"] = d["jalaliDate"].astype(str)
    d["Year"] = d["jalaliDate"].str[0:4]
    d["Month"] = d["jalaliDate"].str[4:6]
    d["Day"] = d["jalaliDate"].str[6:8]
    d["jalaliDate"] = d["jalaliDate"].astype(int)
    return d


def vv(row):
    X = row.split("-")
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


def vv4(row):
    row = str(row)
    X = [1, 1, 1]
    X[0] = row[0:4]
    X[1] = row[4:6]
    X[2] = row[6:8]
    return X[0] + "-" + X[1] + "-" + X[2]


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


# %%

# path = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\\"
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"


#%%

n1 = path + "Stocks_Prices_1399-09-12" + ".csv"
PriceData = pd.read_csv(n1)

PriceData["jalaliDate"] = PriceData["jalaliDate"].apply(vv)
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
PriceData = PriceData.drop(PriceData[PriceData["name"].isin(symbols)].index)
PriceData = PriceData.drop(
    PriceData[PriceData.group_name == "صندوق سرمایه گذاری قابل معامله"].index
)


df = PriceData.drop(
    PriceData[(PriceData.name == "اتکای") & (PriceData.close_price == 1000)].index
)
PriceData = PriceData.drop_duplicates()
PriceData = (
    df.drop(df.loc[(df["volume"] == 0)].index)
    .sort_values(by=["name", "jalaliDate"])
    .rename(columns={"name": "symbol"})
)
PriceData = DriveYearMonthDay(PriceData)
PriceData["date1"] = PriceData["date"].apply(vv4)
PriceData["date1"] = pd.to_datetime(PriceData["date1"])
PriceData["week_of_year"] = PriceData["date1"].dt.week
PriceData["Month_of_year"] = PriceData["date1"].dt.month
PriceData["year_of_year"] = PriceData["date1"].dt.year
gg = PriceData.groupby("symbol")
PriceData["Ret"] = gg["close_price"].pct_change(periods=1) * 100
PriceData["Amihud"] = abs(PriceData["Ret"]) / PriceData["value"]
PriceData.head()


#%%

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
        return pd.DataFrame()
    gg2 = g.groupby("YearMonth")
    t["5_Residual"] = (
        gg2.apply(FiveFactor, df=g).to_frame().reset_index().set_index("level_1")[0]
    )
    t["4_Residual"] = (
        gg2.apply(FourFactor, df=g).to_frame().reset_index().set_index("level_1")[0]
    )
    t["2_Residual"] = (
        gg2.apply(TwoFactor, df=g).to_frame().reset_index().set_index("level_1")[0]
    )
    return t


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
        y = "ERet"
        x = ["EMarketRet", "HML", "SMB", "Winner_Loser", "EgReturn"]
        model = sm.OLS(g[y], sm.add_constant(g[x])).fit()
        alpha = model.params[0]
        beta1 = model.params[1]
        beta2 = model.params[2]
        beta3 = model.params[3]
        beta4 = model.params[4]
        beta5 = model.params[5]

    except:
        alpha = np.nan
        beta1 = np.nan
        beta2 = np.nan
        beta3 = np.nan
        beta4 = np.nan
        beta5 = np.nan
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
        y = "ERet"
        x = ["EMarketRet", "HML", "SMB", "Winner_Loser"]
        model = sm.OLS(g[y], sm.add_constant(g[x])).fit()
        alpha = model.params[0]
        beta1 = model.params[1]
        beta2 = model.params[2]
        beta3 = model.params[3]
        beta4 = model.params[4]

    except:
        alpha = np.nan
        beta1 = np.nan
        beta2 = np.nan
        beta3 = np.nan
        beta4 = np.nan
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
        y = "ERet"
        x = ["EMarketRet", "EgReturn"]
        model = sm.OLS(g[y], sm.add_constant(g[x])).fit()
        alpha = model.params[0]
        beta1 = model.params[1]
        beta2 = model.params[2]

    except:
        alpha = np.nan
        beta1 = np.nan
        beta2 = np.nan
    return alpha, beta1, beta2


# %%
wg = PriceData.groupby(["symbol"])

g = wg.get_group("فولاد")

re = wg.apply(ResidualFactor)
# %%
re = re.reset_index(drop=True)
col = "symbol"
re[col] = re[col].apply(lambda x: convert_ar_characters(x))


# %%

re.to_csv(path + "Residuals" + ".csv", index=False)
# %%
