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

    BG = BG[BG.listed == 1]
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
gg  = quarterdata.groupby('name')
quarterdata['Earning1'] = gg.netProfit.shift()
quarterdata['Earning1'] = quarterdata['Earning1'] - quarterdata.netProfit
quarterdata['Earning2'] = gg.netProfit.shift(2)
quarterdata['Earning2'] = quarterdata['Earning2'] - quarterdata.netProfit
quarterdata['Earning4'] = gg.netProfit.shift(4)
quarterdata['Earning4'] = quarterdata['Earning4'] - quarterdata.netProfit

def vv2(row):
    X = row.split('/')
    return X[0]
balance = balance.iloc[:,[0,4,13,-7]]
balance.rename(columns={ balance.columns[0]: "symbol" ,balance.columns[1]: "date" ,balance.columns[2]: "BookValue" ,balance.columns[3] : "Capital"}, inplace = True)
balance['shrout'] = balance['Capital'] * 100
balance['Year'] = balance['date'].apply(vv2)
balance['Year'] = balance['Year'].astype(str)
balance = balance.drop(columns = ['date','Capital'])
col = 'symbol'
balance[col] = balance[col].apply(lambda x: convert_ar_characters(x))
balance['year']= balance.Year.astype(int)
balance = balance.set_index(['symbol','year'])
mapdict = dict(zip(balance.index,balance.BookValue))
quarterdata['BookValue'] = quarterdata.set_index(
    ['name','year']
    ).index.map(mapdict)
balance = balance.reset_index()
quarterdata["MarketCap"] = quarterdata.close_price * quarterdata.shrout

for i in ['1','2','4']:
    t = 'Earning' + i
    quarterdata[t] = quarterdata[t] /quarterdata['BookValue']
quarterdata    
# %%


def UoWeight(sg):
    sg["WinUoP"] = sg["MarketCap"] * sg["cr"]
    sg["UoP"] = sg["WinUoP"].sum()
    sg["WinUoP"] = sg["WinUoP"] / (sg["WinUoP"].sum()) * 100

    sg["UoPEarning"] = sg["WinUoP"] * sg["netProfit"]
    sg["UoPEarning"] = sg["UoPEarning"].sum()
    return sg


def QuarterCalculation(g):
    print(g.name)
    uoMean = g.groupby(['uo'])[
        ['Earning1',	'Earning2',	'Earning4']
        ].mean()
    for i in uoMean:
        mapdict = dict(zip(uoMean.index,uoMean[i]))
        g[i + "_group"] = g.uo.map(mapdict)
    t = g.groupby(['uo']).size().to_frame()
    mapdict = dict(zip(t.index,t[0]))
    g['number' + "_group"] = g.uo.map(mapdict)

    indMean = g.groupby(['group_id'])[
        ['Earning1',	'Earning2',	'Earning4']
        ].mean()
    for i in indMean:
        mapdict = dict(zip(indMean.index,indMean[i]))
        g[i + "_ind"] = g.group_id.map(mapdict)
    t = g.groupby(['group_id']).size().to_frame()
    mapdict = dict(zip(t.index,t[0]))
    g['number' + "_ind"] = g.group_id.map(mapdict)

    for i in ['Earning1',	'Earning2',	'Earning4']:
        for j in ["_group","_ind"]:
            g[i+j] = (g[i+j] - g[i]/g['number'+j])/(1-1/g['number'+j])


    for i in ['Earning1',	'Earning2',	'Earning4']:
        g[i + '_market'] = g[i].mean()
    return g
gg = quarterdata.groupby(["year", "quarter"])
g = gg.get_group((1395,4))
data = gg.apply(QuarterCalculation)
# %%
names = sorted(data.name.unique())
ids = range(len(names))
mapingdict = dict(zip(names, ids))
data["id"] = data["name"].map(mapingdict)
data['yearQuarter'] = data.year.astype(str) + '-' + data.quarter.astype(str)
times = sorted(data.yearQuarter.unique())
ids = range(len(times))
mapingdict = dict(zip(times, ids))
data["t"] = data["yearQuarter"].map(mapingdict)
#%%
gg=data.groupby('name')
data['return']= gg.close_price.pct_change()
data
#%%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
data.to_csv(path + "Earnings.csv",index = False)
# %%
