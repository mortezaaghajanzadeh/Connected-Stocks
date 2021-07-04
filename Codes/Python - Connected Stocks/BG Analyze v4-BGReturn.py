#%%
import pandas as pd
import re
import numpy as np
import random

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
#%%


def vv(row):
    X = row.split("-")
    return int(X[0] + X[1] + X[2])


def year(row):
    X = row.split("-")
    return int(X[0])


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


def vv4(row):
    row = str(row)
    X = [1, 1, 1]
    X[0] = row[0:4]
    X[1] = row[4:6]
    X[2] = row[6:8]
    return X[0] + "-" + X[1] + "-" + X[2]


def vv3(row):
    X = row.split("/")
    if len(X[0]) < 4:
        X[0] = "13" + X[0]
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[2]) < 2:
        X[2] = "0" + X[2]
    return X[0] + X[1] + X[2]


#%%
df = pd.read_parquet(path + "Stocks_Prices_1399-09-12.parquet")

PriceData = pd.DataFrame()
PriceData = PriceData.append(
    df[
        [
            "jalaliDate",
            "date",
            "name",
            "close_price",
            "group_id",
            "value",
            "volume",
            "quantity",
        ]
    ]
)
del df
PriceData = PriceData.sort_values(by=["name", "date"])
PriceData["close_price"] = PriceData.close_price.astype(float)
PriceData["value"] = PriceData.value.astype(float)
PriceData = PriceData[PriceData.volume != 0]
gg = PriceData.groupby("name")
PriceData["Ret"] = gg["close_price"].pct_change(periods=1) * 100
PriceData["Amihud"] = abs(PriceData["Ret"]) / PriceData["value"]
PriceData["jalaliDate"] = PriceData.jalaliDate.apply(vv)
PriceData.head()
# %%
n = path + "Factors-Daily.xlsx"
Factors = pd.read_excel(n)
Factors.tail()
PriceData = (
    PriceData.merge(Factors, on=["jalaliDate", "date"])
    .sort_values(by=["name", "date"])
    .reset_index(drop=True)
    .dropna()
)

PriceData.head()

PriceData = PriceData[PriceData.jalaliDate > 13930000]

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

# %%

df = pd.read_csv(path + "Cleaned_Stocks_Holders_1399-09-12_From94" + ".csv")
df["year"] = round(df.jalaliDate / 10000, 0)
df["year"] = df["year"].astype(int)
gg = df.groupby("symbol")
g = gg.get_group("فارس")
g = g[["symbol", "shrout", "date"]].drop_duplicates()
g["dif"] = g.shrout.diff()
g[g.dif != 0.0]


pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
# pathBG = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\\"
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
        "group_name",
        "shrout",
        "close_price",
        "uo",
        "cfr",
        "cr",
        "Return",
    ]
].drop_duplicates()
# %%
df["MarketCap"] = df["shrout"] * df["close_price"]


def UoWeight(sg):
    sg["WinUoP"] = sg["MarketCap"] * sg["cr"]
    sg["UoP"] = sg["WinUoP"].sum()
    sg["WinUoP"] = sg["WinUoP"] / (sg["WinUoP"].sum()) * 100

    sg["UoPR"] = sg["WinUoP"] * sg["Return"]
    sg["UoPR"] = sg["UoPR"].sum()
    return sg


def WinI(sg):
    sg["WinI"] = sg.MarketCap / sg.MarketCap.sum()
    return sg


def DailyCalculation(g):
    print(g.name)
    # Weight in Uo's portfolio
    Sg = g.groupby("uo")
    t = Sg.apply(UoWeight)
    t = t.iloc[:, [0, 1, -3, -2, -1]]
    for i in ["WinUoP", "UoP", "UoPR"]:
        fkey = zip(t.date, t.symbol)
        mapdict = dict(zip(fkey, t[i]))
        g[i] = g.set_index(["date", "symbol"]).index.map(mapdict)
    sgg = g.groupby("group_name")
    g = sgg.apply(WinI)
    return g


gg = df.groupby("date")
data = gg.apply(DailyCalculation)
data = data.dropna()


#%%
result = data[["date", "symbol", "UoP", "UoPR", "WinI","WinUoP"]].rename(
    columns={"symbol": "name"}
)
a = PriceData.merge(result, on=["date", "name"], how="left")
# %%
# mapdict = dict(zip(data.set_index(["symbol", "date"]).index, data.UoPR))
# PriceData["UoPR"] = PriceData.set_index(["name", "date"]).index.map(mapdict)
# mapdict = dict(zip(data.set_index(["symbol", "date"]).index, data.WinUoP))
# PriceData["WinUoP"] = PriceData.set_index(["name", "date"]).index.map(mapdict)
# mapdict = dict(zip(data.set_index(["symbol", "date"]).index, data.WinI))
# PriceData["WinI"] = PriceData.set_index(["name", "date"]).index.map(mapdict)

# %%
mergedData = pd.DataFrame()
mergedData = mergedData.append(a[~a.UoPR.isnull()])
mergedData["UoPR"] = (mergedData.UoPR - mergedData.WinUoP * mergedData.Ret) / (
    1 - mergedData.WinUoP
)
mergedData["EUoPR"] = mergedData.UoPR - mergedData.RiskFree
mergedData["gReturn_Firmout"] = (
    mergedData.gReturn - mergedData.WinI * mergedData.Ret
) / (1 - mergedData.WinI)
mergedData.loc[
    abs(mergedData.gReturn_Firmout)>10000000,"gReturn_Firmout"
    ] = mergedData.loc[
        abs(mergedData.gReturn_Firmout)>10000000]["gReturn"]
mergedData["EgReturn_Firmout"] = mergedData.gReturn_Firmout - mergedData.RiskFree


# %%
mapdict = dict(zip(mergedData.name.unique(), range(len(mergedData.name.unique()))))
mergedData["id"] = mergedData.name.map(mapdict)
mergedData = mergedData.dropna()


#%%
mergedData.to_csv(path + "BGReturn.csv", index=False)
# %%
mergedData.groupby("id").size().max()

# %%
