#%%
import pandas as pd
import numpy as np
import re as ree

from numpy import log as ln

# %%
def vv4(row):
    row = str(row)
    X = [1, 1, 1]
    X[0] = row[0:4]
    X[1] = row[4:6]
    X[2] = row[6:8]
    return X[0] + "-" + X[1] + "-" + X[2]


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


def vv5(row):
    X = row.split("/")
    return X[0]


# %%
path = r"E:\RA_Aghajanzadeh\Data\\"
# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"


# %%

n = path + "Cleaned_Stocks_Holders_1400_06_28.csv"
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


#%%
re = pd.read_csv(path + "Connected_Stocks\residuals.csv")
col = "symbol"
HolderData[col] = HolderData[col].apply(lambda x: convert_ar_characters(x))
re["date"] = re.date.astype(int)
HolderData["date"] = HolderData.date.astype(int)

# %%
residuals = re[re.jalaliDate > 13880000]
del re
for i in ["4_Residual","6_Residual", "5_Residual", "2_Residual", "5Lag_Residual"]:
    fkey = zip(list(residuals.symbol), list(residuals.date))
    mapingdict = dict(zip(fkey, residuals[i]))
    HolderData[i] = HolderData.set_index(["symbol", "date"]).index.map(mapingdict)
    print(i + "is done")


for i in ["Ret", "volume", "value", "Amihud"]:

    fkey = zip(list(residuals.symbol), list(residuals.date))
    mapingdict = dict(zip(fkey, residuals[i]))
    HolderData[i] = HolderData.set_index(["symbol", "date"]).index.map(mapingdict)
    print(i + "is done")

HolderData.head()
# %%
df = HolderData
df["marketCap"] = df.close_price * df.shrout
df["volume"] = df["volume"].astype(float)
df["value"] = df["value"].astype(float)
df["TurnOver"] = ln(df.value / df.marketCap)
df["Amihud_ln"] = ln(df["Amihud"])
g = df.groupby(['symbol','date'])
t = g.first().reset_index()
gg = t.groupby("symbol")
#%%
for i in ['TurnOver','Amihud']:
    t['Delta_'+ i] = gg[i].diff()
    mapdict = dict(zip(t.set_index(['symbol','date']).index,t['Delta_'+ i]))
    df['Delta_'+ i]  = df.set_index(['symbol','date']).index.map(mapdict)


# %%
def genereate_id(s):
    names = list(set(s))
    names.sort()
    ids = list(range(len(names)))
    mapingdict = dict(zip(names, ids))
    return s.map(mapingdict)


df["Holder_id"] = genereate_id(df.Holder)

df["id"] = genereate_id(df.symbol)


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
tt = BG[BG.year == 1398]
tt["year"] = 1399
BG = BG.append(tt).reset_index(drop=True)

BGroup = set(BG["uo"])
names = sorted(BGroup)
ids = range(len(names))
mapingdict = dict(zip(names, ids))
BG["BGId"] = BG["uo"].map(mapingdict)


# %%
for i in ['BGId','position','uo']:
    fkey = zip(list(BG.symbol), list(BG.year))
    mapingdict = dict(zip(fkey, BG[i]))
    df[i] = df.set_index(["symbol", "year"]).index.map(mapingdict)
    print(i + " is done")
# %%
del mapingdict
del gg
len(df),list(df)

# %%
df.to_parquet(path + "Holder_Residual.parquet")

# %%
