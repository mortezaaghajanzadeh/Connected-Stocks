#%%
import pandas as pd
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


# %%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Balance Sheet\\"
balance = pd.read_excel(path + "balance sheet - 9811.xlsx")
# %%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Incomesheet\\"
income = pd.read_csv(path + "incomesheet.csv")
income = (
    income[["year", "سود خالص", "season", "stock", "target"]]
    .dropna()
    .sort_values(by=["stock", "year", "season"])
    .loc[income.year >= 1394]
)
income["year"] = income.year.astype(int)
income["season"] = income["season"] / 3
income["season"] = income.season.astype(int)
col = "stock"
income[col] = income[col].apply(lambda x: convert_ar_characters(x))
income = income.rename(
    columns={
        "stock": "name",
        "target": "stock_id",
        "سود خالص": "netProfit",
        "season": "quarter",
    }
)
income

#%%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
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
            "stock_id",
        ]
    ]
)
del df
PriceData = PriceData.sort_values(by=["name", "date"])
PriceData["close_price"] = PriceData.close_price.astype(float)
PriceData["value"] = PriceData.value.astype(float)
PriceData = PriceData[PriceData.volume != 0]


def vv(row):
    X = row.split("-")
    return int(X[1])


PriceData["month"] = PriceData.jalaliDate.apply(vv)

PriceData["quarter"] = 1
PriceData.loc[PriceData.month > 3, "quarter"] = 2
PriceData.loc[PriceData.month > 6, "quarter"] = 3
PriceData.loc[PriceData.month > 9, "quarter"] = 4


def vv(row):
    X = row.split("-")
    return int(X[0])


PriceData["year"] = PriceData.jalaliDate.apply(vv)

PriceData = PriceData.loc[PriceData.year >= 1394]


def vv(row):
    X = row.split("-")
    return int(X[0] + X[1] + X[2])


PriceData["jalaliDate"] = PriceData.jalaliDate.apply(vv)

PriceData
# %%
gg = PriceData.groupby(["name", "year", "quarter"])
a = gg[["value", "volume", "quantity"]].sum()
b = (gg.last()["close_price"] / gg.first()["close_price"]) - 1
# .to_frame().rename(columns = {'close_price':'quarterReturn'} )
quarterdata = gg.last()[["group_id", "stock_id", "close_price"]].merge(
    a, left_index=True, right_index=True
)
quarterdata["Return"] = b * 100
quarterdata = quarterdata.reset_index()


def BG(df):
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

    BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3)
    for i in ["uo", "cfr", "cr"]:
        print(i)
        fkey = zip(list(BG.symbol), list(BG.year))
        mapingdict = dict(zip(fkey, BG[i]))
        df[i] = df.set_index(["name", "year"]).index.map(mapingdict)
    return df


quarterdata = BG(quarterdata)


col = "name"
quarterdata[col] = quarterdata[col].apply(lambda x: convert_ar_characters(x))


quarterdata
# %%

df = pd.read_csv(path + "Cleaned_Stocks_Holders_1399-09-12_From94" + ".csv")
df = df[
    [
        "symbol",
        "jalaliDate",
        "stock_id",
        "group_name",
        "group_id",
        "shrout",
        "close_price",
    ]
].drop_duplicates()
df["year"] = round(df.jalaliDate / 10000).astype(int)
df["month"] = round(df.jalaliDate / 100) - round(df.jalaliDate / 10000) * 100
df["month"] = df["month"].astype(int)
df["quarter"] = 1
df.loc[df.month > 3, "quarter"] = 2
df.loc[df.month > 6, "quarter"] = 3
df.loc[df.month > 9, "quarter"] = 4

df = df[
    [
        "symbol",
        "year",
        "quarter",
        "stock_id",
        "group_name",
        "group_id",
        "shrout",
        "close_price",
    ]
].drop_duplicates(keep="last")

# %%

a = df.set_index(["symbol", "year", "quarter"])
mapdict = dict(zip(a.index, a.shrout))

quarterdata = quarterdata.set_index(["name", "year", "quarter"])
quarterdata["shrout"] = quarterdata.index.map(mapdict)
quarterdata = quarterdata.reset_index()
quarterdata.isnull().sum()
#%%
quarterdata[quarterdata.shrout.isnull()].name.unique()
quarterdata = quarterdata[~quarterdata.shrout.isnull()]
#%%
a = income.set_index(["name", "year", "quarter"])
mapdict = dict(zip(a.index, a.netProfit))

quarterdata = quarterdata.set_index(["name", "year", "quarter"])
quarterdata["netProfit"] = quarterdata.index.map(mapdict)
quarterdata = quarterdata.reset_index()
quarterdata.isnull().sum()
# %%
quarterdata = quarterdata[~quarterdata.netProfit.isnull()]
# %%
quarterdata["MarketCap"] = quarterdata.close_price * quarterdata.shrout


def UoWeight(sg):
    sg["WinUoP"] = sg["MarketCap"] * sg["cr"]
    sg["UoP"] = sg["WinUoP"].sum()
    sg["WinUoP"] = sg["WinUoP"] / (sg["WinUoP"].sum()) * 100

    sg["UoPEarning"] = sg["WinUoP"] * sg["netProfit"]
    sg["UoPEarning"] = sg["UoPEarning"].sum()
    return sg


def DailyCalculation(g):
    print(g.name)
    # Weight in Uo's portfolio
    Sg = g.groupby("uo")
    t = Sg.apply(UoWeight)
    t = t.iloc[:, [0, 1, 2, -3,-1]].dropna().set_index(["name"])
    
    print(t.columns)
    for i in ["WinUoP",  "UoPEarning"]:
        mapdict = dict(zip(t.index, t[i]))
        g[i] = g.set_index(
            ["name"]).index.map(mapdict)
    
    
    
    return g
gg = quarterdata.groupby(["year", "quarter"])
data = gg.apply(DailyCalculation)
#%%
Sg = g.groupby("uo")
t = Sg.apply(UoWeight)
t = t.iloc[:, [0, 1, 2, -3,-1]].dropna().set_index(["name"])
print(t.columns)
for i in ["WinUoP",  "UoPEarning"]:
    mapdict = dict(zip(t.index, t[i]))
    g[i] = g.set_index(
        ["name"]).index.map(mapdict)
# .dropna().set_index(["name", "year", "quarter"])
    
# %%
