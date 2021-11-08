#%%
import pandas as pd
import matplotlib.pyplot as plt
import jdatetime
from matplotlib.ticker import FuncFormatter
from scipy import stats
import seaborn as sns
from pandas_jalali.converter import get_gregorian_date_from_jalali_date

#%%
path = r"E:\RA_Aghajanzadeh\Data\PriceTradeData\\"
df = pd.read_parquet(path + "mergerdPriceAllData_cleaned.parquet")


def vv1(row):
    row = str(row)
    return int(row[0:4])


def vv2(row):
    row = str(row)
    return int(row[4:6])


def vv3(row):
    row = str(row)
    return int(row[6:8])


def vv(row):
    row = row.split("-")
    return int(row[0] + row[1] + row[2])


df = df[~df.ind_buy_count.isnull()].drop(
    columns=[
        "basevalue",
        "market",
        "pricechange",
        "priceMin",
        "priceMax",
        "priceYesterday",
        "priceFirst",
        "stock_id",
        "close_price",
        "last_price",
        "count",
        "volume",
        "value",
        "max",
        "min",
    ]
)


#%%
df["jalaliDate"] = df.jalaliDate.apply(vv)
df["year"] = df["jalaliDate"].apply(vv1)
df["month"] = df["jalaliDate"].apply(vv2)
df["day"] = df["jalaliDate"].apply(vv3)
df = df[df.year >= 1393]
#%%

df["year_of_year"] = df["year"]
df["Month_of_year"] = df["month"].astype(int)
df["day"] = df["day"].astype(int)
#%%


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
df["yearMonth"] = round(df.jalaliDate / 100)
df["yearMonth"] = df["yearMonth"].astype(int)

#%%
frequency = "yearMonth"
mdf = df.groupby(["name", frequency]).first().drop(columns=["jalaliDate"])
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
        # "group_name",
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
    time = jdatetime.date(int(row[0:4]), int(row[4:6]), 28).togregorian()
    return str(time.year) + "-" + str(time.month)


result["date"] = result.yearMonth.apply(togreforian)
result
#%%
result = result.dropna()
result = result[result.yearMonth < 139901]
#%%
a = result.groupby("uo")[Imbalances[:-1]].mean()
a = a.sort_values(by=Imbalances[-2]).dropna()
a

# %%
b = result.groupby(["yearMonth", "Grouped"]).mean().reset_index()
#%%
tt = (
    b.groupby("Grouped")[Imbalances[-2]]
    .describe()
    .T.rename(
        columns={
            0.0: "Ungrouped",
            1.0: "Grouped",
        }
    )
    .T.round(3)
)
tt["count"] = tt["count"].astype(int)
tt.to_latex(
    r"E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Final Report\Output"
    + "\\ImbalanceSummary.tex"
)
tt
#%%

# %%
result["yearMonth"] = result.yearMonth.astype(str)
fig = plt.figure(figsize=(8, 4))
g = sns.lineplot(
    data=result, x="yearMonth", y="InsImbalance_value", hue="Grouped", ci=0
)
a = result.yearMonth.unique()
labels = list(result.yearMonth.unique())
tickvalues = a
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
pathS = r"E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Final Report\Output"

plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Monthly standard errors' Time Series")
plt.legend(["Ungrouped", "Grouped"])
fig.set_rasterized(True)
plt.savefig(pathS + "\\GroupedSTD.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\GroupedSTD.png", bbox_inches="tight")

#%%
stats.ttest_ind(
    b[b.Grouped == 1].InsImbalance_value,
    b[b.Grouped == 0].InsImbalance_value,
)
