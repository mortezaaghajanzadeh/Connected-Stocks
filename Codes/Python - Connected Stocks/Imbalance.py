#%%
import pandas as pd
import matplotlib.pyplot as plt
import jdatetime
from matplotlib.ticker import FuncFormatter
from scipy import stats
import seaborn as sns
from pandas_jalali.converter import get_gregorian_date_from_jalali_date
#%%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
def vv1(row):
    row = str(row)
    return int(row[0:4]) 
def vv2(row):
    row = str(row)
    return int(row[4:6])
def vv3(row):
    row = str(row) 
    return int(row[6:8])
df = pd.read_csv(path + "Stock Trade details.csv")
df = df[~df.ind_buy_count.isnull()].drop(
    columns=[
        "baseVol",
        "max_price",
        "min_price",
        "close_price",
        "last_price",
        "open_price",
        "value",
        "volume",
        "quantity",
        "Price",
        "open_Adjprice",
        "Adjusted price",
    ]
)
df['jalali'] = df.jalali.astype(int)
df["year"] = df["jalali"].apply(vv1)
df["month"] = df["jalali"].apply(vv2)
df["day"] = df["jalali"].apply(vv3)
df = df[df.year >= 1394]
#%%

df["year_of_year"] = df["year"]
df["Month_of_year"] = df["month"].astype(int)
df["day"] = df["day"].astype(int)
#%%



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
    BG = BG[BG.listed == 1]
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
        df[i] = df.set_index(["symbol", "year"]).index.map(mapingdict)
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
# df["yearWeek"] = df["year_of_year"].astype(str) + "-" + df["week_of_year"].astype(str)

#%%
frequency = "yearMonth"
mdf = df.groupby(["symbol", frequency]).first().drop(columns=["jalali"])
mdf[mlist] = df.groupby(["symbol", frequency])[mlist].sum()
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
        "symbol",
        "group_name",
        "year",
        "uo",
        "cfr",
        "cr",
        "Grouped",
        "InsImbalance_count",
        "InsImbalance_volume",
        "InsImbalance_value",
    ]
].sort_values(by=["symbol", frequency])
mdf = mdf.reset_index(drop=True)
mdf = mdf[~mdf.InsImbalance_count.isnull()]
mdf
Imbalances = [
    "InsImbalance_count",
    "InsImbalance_volume",
    "InsImbalance_value",
    "Grouped",
]
gg = mdf.groupby([frequency])


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

def togreforian(row):
    row = str(row)
    time = jdatetime.date(int(row[0:4]),int(row[4:6]),28).togregorian()
    return str(time.year)+'-' + str(time.month)
result['date'] = result.yearMonth.apply(togreforian)
result
#%%

a = result.groupby("uo")[Imbalances[:-1]].mean()
a = a.sort_values(by=Imbalances[-2]).dropna()
a

# %%
b = result.groupby(['yearMonth','Grouped']).mean().reset_index()
#%%
b.groupby("Grouped")[Imbalances[-2]].describe().T
#%%
result = result.dropna()
result['yearMonth'] = result.yearMonth.astype(str)
fig = plt.figure(figsize=(8, 4))
g = sns.lineplot(data = result,x='yearMonth',y = 'InsImbalance_value',
         hue = 'Grouped', ci=0)
a = result.yearMonth.unique()
labels = list(result.date.unique())
tickvalues = a
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Monthly standard errors' Time Series")
plt.legend(['Ungrouped','Grouped'])
fig.set_rasterized(True)
plt.savefig(pathS + "\\GroupedSTD.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\GroupedSTD.png", bbox_inches="tight")


stats.ttest_ind(
    b[b.Grouped == 1].InsImbalance_value,
    b[b.Grouped == 0].InsImbalance_value,
)






#%%
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
BG = BG[BG.listed == 1]
print(len(BG))
BG = BG[BG.uo.isin(uolist)]

#%%
a = (
    BG.groupby(["uo", "year"])
    .filter(lambda x: x.shape[0] >= 10)[["year", "uo"]]
    .drop_duplicates()
)

BGlist = list(zip(a.year, a.uo))
result["year"] = round(result.jalali / 10000)
result["year"] = result["year"].astype(int)
result["BigGroup"] = 0
result = result.set_index(["year", "uo"])
result.loc[result.index.isin(BGlist), "BigGroup"] = 1
result = result.reset_index()

result.groupby(["BigGroup", "Grouped"])[Imbalances[:-1]].mean().sort_values(
    by=Imbalances
)

#%%
result2 = result.set_index(["year", "uo"])
result2 = result2[result2.index.isin(BGlist)]
# .sort_values(by=Imbalances)
result2 = result2.reset_index()
a = result2.groupby("uo")[Imbalances[:-1]].mean()
a.append(
    result[result.Grouped == 0][Imbalances[:-1]]
    .mean()
    .to_frame()
    .rename(columns={0: "NotGroup"})
    .T
).sort_values(by=Imbalances[:-1])
#%%
a = result.groupby("uo")[Imbalances[:-1]].mean()
a.sort_values(by=Imbalances[:-1]).dropna()


# #%%
# import seaborn as sns
# import matplotlib.pyplot as plt
# fig = plt.figure(figsize=(8, 4))

# g = sns.lineplot(data=result, x="jalali", y="InsImbalance_count"
#                  ,hue='Grouped')
# labels = result.jalali.to_list()
# tickvalues = result.jalali
# g.set_xticks(range(len(tickvalues))[::-30])  # <--- set the ticks first
# g.set_xticklabels(labels[::-30], rotation="vertical")
# plt.margins(x=0.01)
