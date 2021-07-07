# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re as ree
import numpy as np

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"


# %%

n2 = path + "MonthlyNormalzedFCAP7.2" + ".csv"
df2 = pd.read_csv(n2)
print("n2 Done")

timeId = pd.read_csv(path + "timeId.csv")

n = path + "Holder_Residual" + ".parquet"
df = pd.read_parquet(n)
#%%
n3 = path + "MonthlyAllPairs" + ".csv"
df3 = pd.read_csv(n3)
#%%

df["Grouped"] = 1
df.loc[df.uo.isnull(), "Grouped"] = 0
df["year"] = round(df.date / 10000).astype(int)
df = df[df.jalaliDate < 13990000]
df = df.drop_duplicates(subset=["symbol", "year"])
fig = plt.figure(figsize=(8, 4))
g = sns.lineplot(data=df, x="year", y="Grouped")

from matplotlib.ticker import FuncFormatter

g.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))

pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

plt.ylabel("")
plt.xlabel("Year")
plt.title("Group affiliated firms' Time Series")
fig.set_rasterized(True)
plt.savefig(pathS + "\\BGtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\BGtimeSeries.png", bbox_inches="tight")
#%%
te = df.groupby(['year','Grouped']).MarketCap.sum().to_frame().reset_index()
te = te[te.Grouped == 0].merge(te[te.Grouped == 1],on = 'year')
te['Group affiliated'] = te.MarketCap_y /(te.MarketCap_y + te.MarketCap_x)
te['Not Group affiliated'] = te.MarketCap_x /(te.MarketCap_y + te.MarketCap_x)
te
g = te.plot(
    y=["Group affiliated", "Not Group affiliated"] ,x = 'year', figsize=(8, 4)
)
from matplotlib.ticker import FuncFormatter

g.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
plt.ylabel("")
plt.xlabel("Year")
plt.title("Group affiliated market caps' Time Series")
fig.set_rasterized(True)
plt.savefig(pathS + "\\BGMarketCaptimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\BGMarketCaptimeSeries.png", bbox_inches="tight")

#%%
n = path + "Holder_Residual" + ".parquet"
df = pd.read_parquet(n)




#%%
df["Grouped"] = 1
df.loc[df.uo.isnull(), "Grouped"] = 0
df["year_Month"] = round(df.date / 100).astype(int).astype(str)
df = df[df.jalaliDate < 13990000]
df = df.drop_duplicates(subset=["symbol", "year_Month"])
fig = plt.figure(figsize=(8, 4))
g = sns.lineplot(data=df, x="year_Month", y="5-Residual", hue="Grouped")

pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
labels = df.year_Month.to_list()
tickvalues = df.year_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Residuals Time Series")
plt.legend(["Others", "Group affiliated"])
fig.set_rasterized(True)
plt.savefig(pathS + "\\ResidualtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\ResidualtimeSeries.png", bbox_inches="tight")
n = path + "Holder_Residual" + ".parquet"
df = pd.read_parquet(n)
#%%
fig = plt.figure(figsize=(8, 4))
g = sns.lineplot(data=df3, x="t_Month", y="Monthlyρ_5")
time = timeId.drop_duplicates(subset=["t_Month"], keep="last")[["date", "t_Month"]]
time["date"] = round(time.date / 100).astype(int)
time
labels = time.date.to_list()
tickvalues = time.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

plt.ylabel("Monthly Correlation")
plt.xlabel("Year-Month")
plt.title("Correlation Time Series")
fig.set_rasterized(True)
plt.savefig(pathS + "\\CorrtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\CorrtimeSeries.png", bbox_inches="tight")
#%%
fig = plt.figure(figsize=(8, 4))
g = sns.lineplot(data=df3, x="t_Month", y="Monthlyρ_5",hue ="sBgroup" )
time = timeId.drop_duplicates(subset=["t_Month"], keep="last")[["date", "t_Month"]]
time["date"] = round(time.date / 100).astype(int)
time
labels = time.date.to_list()
tickvalues = time.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

plt.ylabel("Monthly Correlation")
plt.xlabel("Year-Month")
plt.title("Correlation Time Series")
plt.legend(['Others','Same Group'])
fig.set_rasterized(True)
plt.savefig(pathS + "\\BGCorrtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\BGCorrtimeSeries.png", bbox_inches="tight")

#%%
n = path + "Holder_Residual" + ".parquet"
df = pd.read_parquet(n)
#%%
fig = plt.figure(figsize=(8, 4))

g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA")

time = timeId.drop_duplicates(subset=["t_Month"], keep="last")[["date", "t_Month"]]
time["date"] = round(time.date / 100).astype(int)
time
labels = time.date.to_list()
tickvalues = time.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
fig.set_rasterized(True)
plt.savefig(pathS + "\\FCAtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\FCAtimeSeries.png", bbox_inches="tight")


#%%
fig = plt.figure(figsize=(8, 4))

g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA", hue="sBgroup")

time = pd.read_csv(path + "timeId.csv")
time = time.drop_duplicates(subset=["t_Month"], keep="last")[["date", "t_Month"]]
time["date"] = round(time.date / 100).astype(int)
time
labels = time.date.to_list()
tickvalues = time.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.legend(["Others", "In the same BG"])
plt.margins(x=0.01)
pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
fig.set_rasterized(True)
plt.savefig(pathS + "\\FCAtimeSeriesBG.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\FCAtimeSeriesBG.png", bbox_inches="tight")
# %%
fig = plt.figure(figsize=(8, 4))

g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA")
sns.lineplot(data=df2, x="t_Month", y="MonthlyFCAPf")

time = pd.read_csv(path + "timeId.csv")
time = time.drop_duplicates(subset=["t_Month"], keep="last")[["date", "t_Month"]]
time["date"] = round(time.date / 100).astype(int)
time
labels = time.date.to_list()
tickvalues = time.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
plt.legend(["FCA", "FCAP"])
fig.set_rasterized(True)
plt.savefig(pathS + "\\FCAComparetimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\FCAComparetimeSeries.png", bbox_inches="tight")


#%%

pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
# pathBG = path
n = pathBG + "Grouping_CT.xlsx"
BG = pd.read_excel(n)
BG = BG[BG.listed == 1]
BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3.0)

df["year"] = round(df.jalaliDate / 10000, 0)
df["year"] = df["year"].astype(int)
tt = BG[BG.year == 1397]
tt["year"] = 1398
BG = BG.append(tt).reset_index(drop=True)


# %%
len(set(df[df.BGId.isnull()].symbol))


# %%
gg = df2.groupby("t_Month")
g = gg.get_group(2)


def v(g):
    return len(g.id.unique())


gg.apply(v).describe()


# %%

# df2 #
PG = df2[
    ["BGId_x", "BGId_y", "year_of_year", "id", "sBgroup", "numberCommonHolder"]
].drop_duplicates()
gg = PG.groupby("year_of_year")
g = gg.get_group(2019)


def summary(g):
    rdf = (
        g.dropna()
        .groupby("sBgroup")
        .size()
        .to_frame()
        .T.rename(
            columns={
                0: "Number of Pairs not in one Group",
                1: "Number of Pairs in one Group",
            }
        )
        .reset_index(drop=True)
    )
    rdf["Avg. Number of Pairs in one Group"] = round(
        g[g.sBgroup == 1].groupby("BGId_x").size().mean(), 0
    )
    rdf["Med. Number of Pairs in one Group"] = round(
        g[g.sBgroup == 1].groupby("BGId_x").size().median(), 0
    )
    rdf["Max. Number of Pairs in one Group"] = round(
        g[g.sBgroup == 1].groupby("BGId_x").size().max(), 0
    )
    rdf["No. of Pairs"] = len(g)

    t = set(g.dropna().BGId_x)
    t.update(set(g.dropna().BGId_y))
    rdf["No. of Groups"] = len(t)
    t = set(g[g.BGId_x.isnull()].id)
    t.update(set(g[g.BGId_y.isnull()].id))
    rdf["No. of Pairs not in Groups"] = len(t)
    t = set(g.id)

    rdf["Avg. Number of Common owner"] = g.numberCommonHolder.mean()
    rdf["Med. Number of Common owner"] = g.numberCommonHolder.median()
    rdf["Max. Number of Common owner"] = g.numberCommonHolder.max()
    return rdf


a1 = (
    gg.apply(summary)
    .reset_index()
    .rename(columns={"year_of_year": "year"})
    .drop(columns=["level_1"])
    .T
)
gg = (
    df[["BGId", "id", "year_of_year", "Holder_id", "Percent", "date"]]
    .drop_duplicates()
    .groupby("id")
)
g = gg.get_group(1)


def summary(g):
    rdf = g.iloc[0, :1].to_frame().T
    rdf["Av. Holder Percent"] = round(g.groupby("date").Percent.mean().mean(), 2)
    rdf = rdf.drop(columns="BGId")
    rdf["Median of Owners' Percent"] = round(
        g.groupby("date").Percent.median().median(), 2
    )
    rdf["Av. Number of Owners"] = round(g.groupby("date").size().mean(), 0)
    rdf["Med. Number of Owners"] = round(g.groupby("date").size().median(), 0)
    rdf["Max. Number of Owners"] = round(g.groupby("date").size().max(), 0)
    rdf["Av. Block. Ownership"] = round(g.groupby("date").Percent.sum().mean(), 0)
    rdf["Med. Block. Ownership"] = round(g.groupby("date").Percent.sum().median(), 0)
    return rdf


idlevelData = gg.apply(summary).reset_index().drop(columns=["level_1"])
gg = df2.groupby("year_of_year")
g = gg.get_group(2015)


def sumary(g, idlevelData):
    Pairs = g[["id_x", "id_y", "id"]].drop_duplicates().reset_index(drop=True)
    mapdict = dict(zip(idlevelData.id, idlevelData["Av. Holder Percent"]))
    Pairs["Av. Holder Percent_x"] = Pairs["id_x"].map(mapdict)
    Pairs["Av. Holder Percent_y"] = Pairs["id_y"].map(mapdict)

    mapdict = dict(zip(idlevelData.id, idlevelData["Median of Owners' Percent"]))
    Pairs["Median of Owners' Percent_x"] = Pairs["id_x"].map(mapdict)
    Pairs["Median of Owners' Percent_y"] = Pairs["id_y"].map(mapdict)

    mapdict = dict(zip(idlevelData.id, idlevelData["Med. Number of Owners"]))
    Pairs["Med. Number of Owners_x"] = Pairs["id_x"].map(mapdict)
    Pairs["Med. Number of Owners_y"] = Pairs["id_y"].map(mapdict)

    mapdict = dict(zip(idlevelData.id, idlevelData["Av. Number of Owners"]))
    Pairs["Av. Number of Owners_x"] = Pairs["id_x"].map(mapdict)
    Pairs["Av. Number of Owners_y"] = Pairs["id_y"].map(mapdict)

    mapdict = dict(zip(idlevelData.id, idlevelData["Max. Number of Owners"]))
    Pairs["Max. Number of Owners_x"] = Pairs["id_x"].map(mapdict)
    Pairs["Max. Number of Owners_y"] = Pairs["id_y"].map(mapdict)

    mapdict = dict(zip(idlevelData.id, idlevelData["Av. Block. Ownership"]))
    Pairs["Av. Block. Ownership_x"] = Pairs["id_x"].map(mapdict)
    Pairs["Av. Block. Ownership_y"] = Pairs["id_y"].map(mapdict)

    mapdict = dict(zip(idlevelData.id, idlevelData["Med. Block. Ownership"]))
    Pairs["Med. Block. Ownership_x"] = Pairs["id_x"].map(mapdict)
    Pairs["Med. Block. Ownership_y"] = Pairs["id_y"].map(mapdict)

    Pairs = Pairs.drop(columns=["id_x", "id_y"])
    Pairs["Av. Holder Percent"] = Pairs[
        ["Av. Holder Percent_x", "Av. Holder Percent_y"]
    ].mean(1)
    Pairs["Median of Owners' Percent"] = Pairs[
        ["Median of Owners' Percent_x", "Median of Owners' Percent_y"]
    ].mean(1)
    Pairs["Av. Number of Owners"] = Pairs[
        ["Av. Number of Owners_x", "Av. Number of Owners_y"]
    ].mean(1)
    Pairs["Med. Number of Owners"] = Pairs[
        ["Med. Number of Owners_x", "Med. Number of Owners_y"]
    ].mean(1)
    Pairs["Max. Number of Owners"] = Pairs[
        ["Max. Number of Owners_x", "Max. Number of Owners_y"]
    ].mean(1)
    Pairs["Av. Block. Ownership"] = Pairs[
        ["Av. Block. Ownership_x", "Av. Block. Ownership_y"]
    ].mean(1)
    Pairs["Med. Block. Ownership"] = Pairs[
        ["Med. Block. Ownership_x", "Med. Block. Ownership_y"]
    ].mean(1)

    Pairs = Pairs.drop(
        columns=[
            "Av. Holder Percent_x",
            "Av. Holder Percent_y",
            "Median of Owners' Percent_x",
            "Median of Owners' Percent_y",
            "Av. Number of Owners_x",
            "Av. Number of Owners_y",
            "Max. Number of Owners_x",
            "Max. Number of Owners_y",
            "Av. Block. Ownership_x",
            "Av. Block. Ownership_y",
            "id",
            "Med. Number of Owners_x",
            "Med. Number of Owners_y",
            "Med. Block. Ownership_x",
            "Med. Block. Ownership_y",
        ]
    )
    return Pairs.mean().round(2).to_frame().T


a2 = gg.apply(sumary, idlevelData=idlevelData).reset_index().drop(columns=["level_1"]).T
a2.append(a1)

# %%

# df #

gg = (
    df[["BGId", "id", "year_of_year", "Holder_id"]]
    .drop_duplicates()
    .groupby("year_of_year")
)
g = gg.get_group(2019)


def summary(g):
    rdf = g.iloc[0, :1].to_frame().T
    rdf["No. of Firms"] = len(set(g.id))
    rdf["No. of Holders"] = len(set(g.Holder_id))
    rdf = rdf.drop(columns=["BGId"])
    g = g.drop_duplicates(subset=["BGId", "id", "year_of_year"])
    rdf["No. of Groups"] = len(set(g.dropna().BGId))
    rdf["No. of Firms not in Groups"] = len(set(g[g.BGId.isnull()].id))
    rdf["No. of Firms in Groups"] = len(set(g[~g.BGId.isnull()].id))
    rdf["Avg. Number of Members"] = round(g.groupby("BGId").size().mean(), 0)
    rdf["Max. Number of Members"] = g.groupby("BGId").size().max()
    rdf["Med. of  Number of Members"] = round(g.groupby("BGId").size().median(), 0)
    return rdf


a1 = gg.apply(summary).reset_index().drop(columns=["level_1"]).T


gg = (
    df[["BGId", "id", "year_of_year", "Holder_id", "Percent", "date"]]
    .drop_duplicates()
    .groupby("year_of_year")
)
g = gg.get_group(2015)


def summary(g):
    rdf = g.iloc[0, :1].to_frame().T

    def idlevel(g):
        return g.groupby("date").Percent.mean().mean()

    rdf["Av. Holder Percent"] = round(g.groupby("id").apply(idlevel).mean(), 1)
    rdf = rdf.drop(columns="BGId")

    def idlevel(g):
        return g.groupby("date").Percent.median().median()

    rdf["Med. of Owners' Percent"] = round(g.groupby("id").apply(idlevel).median(), 2)

    def idlevel(g):
        return g.groupby("date").size().mean()

    rdf["Av. Number of Owners"] = round(g.groupby("id").apply(idlevel).mean(), 0)
    rdf["Med. Number of Owners"] = round(g.groupby("id").apply(idlevel).median(), 0)
    rdf["Max. Number of Owners"] = round(g.groupby("id").apply(idlevel).max(), 0)

    def idlevel(g):
        return g.groupby("date").Percent.sum().mean()

    rdf["Av. Block. Ownership"] = round(g.groupby("id").apply(idlevel).mean(), 1)
    rdf["Med. Block. Ownership"] = round(g.groupby("id").apply(idlevel).median(), 1)
    rdf["Max. Block. Ownership"] = round(g.groupby("id").apply(idlevel).max(), 1)
    return rdf


a2 = gg.apply(summary).reset_index().drop(columns=["level_1"]).T

a1.append(a2)

#%%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
n = path + "IRX6XTPI0009.xls"
Index = pd.read_excel(n)

Index["YearMonth"] = (Index["<DTYYYYMMDD>"] / 100).round(0)
Index = Index[["YearMonth", "<CLOSE>"]]
Index = Index.drop_duplicates(subset="YearMonth", keep="last")
Index["Negative"] = Index["<CLOSE>"].pct_change()
Index.loc[Index.Negative >= 0, "Negative"] = 0
Index.loc[Index.Negative < 0, "Negative"] = 1
Index = Index.replace(np.nan, 0)
Index["YearMonth"] = Index["YearMonth"].astype(int)
Index["YearMonth"] = Index["YearMonth"].astype(str)
g2 = df2.groupby("t_Month")
g = g2.get_group(0)

df2.loc[df2.uo_x.isnull(), "sBgroup"] = np.nan
df2.loc[df2.uo_y.isnull(), "sBgroup"] = np.nan


def s(g):
    t = g.groupby("sBgroup").size().to_frame().T
    t[3] = g.sBgroup.isnull().sum()
    return t


idMonth = g2.apply(s).reset_index()

idMonth = idMonth[idMonth[1] > 100]
timeId["yearmonth"] = timeId["date"].astype(str)
timeId["yearmonth"] = timeId["yearmonth"].str[0:6]


MonthtimeId = timeId[["t_Month", "yearmonth"]].drop_duplicates().reset_index(drop=True)
mapdict = dict(zip(MonthtimeId.t_Month, MonthtimeId.yearmonth))
idMonth["yearmonth"] = idMonth["t_Month"].map(mapdict)


mapdict = dict(zip(Index.YearMonth, Index.Negative))
idMonth["Negative"] = idMonth["yearmonth"].map(mapdict)
idMonth["Negative"] = idMonth["Negative"] * 5500
labels = idMonth.yearmonth.to_list()
tickvalues = idMonth.t_Month

idMonth = idMonth.rename(
    columns={0: "Not Same Group", 1: "Same Group", 3: "Not in Groups"}
)

idMonth = idMonth.set_index("t_Month")
idMonth.plot.area(
    y=["Same Group", "Not Same Group", "Not in Groups"], figsize=(15, 8), stacked=True
)

plt.margins(x=0.001)
plt.xticks(ticks=tickvalues[::-2], labels=labels[::-2], rotation="vertical")
plt.ylabel("Number")
plt.xlabel("Year-Month")
plt.legend(["In the Same Group", "In two distinct group", "Not in Groups"])
# plt.title("Number of unique pair in each month")
pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
plt.savefig(pathS + "\\idMonth.eps", bbox_inches="tight")
plt.savefig(pathS + "\\idMonth.png", bbox_inches="tight")


#%%
clist = [
    "Monthlysize1",
    "Monthlysize2",
    "MonthlySameSize",
    "MonthlyB/M1",
    "MonthlyB/M2",
    "MonthlySameB/M",
    "MonthlyCrossOwnership",
    "MonthlyFCA",
    "sBgroup",
]
clist2 = [
    "symbol_x",
    "symbol_y",
    "id_x",
    "id_y",
    "group_name_x",
    "group_name_y",
    "position_x",
    "position_y",
    "Monthlysize1",
    "Monthlysize2",
    "MonthlySameSize",
    "MonthlyB/M1",
    "MonthlyB/M2",
    "MonthlySameB/M",
    "MonthlyCrossOwnership",
    "MonthlyFCA",
    "Monthlyρ_5",
    "uo_x",
    "uo_y",
    "sgroup",
    "sBgroup",
]
Gdf = df2[df2.sBgroup == 1]
gg = Gdf.groupby("id")
gdf = gg.last()
gdf[clist] = gg[clist].mean()
gdf = gdf[
    [
        "symbol_x",
        "symbol_y",
        "id_x",
        "id_y",
        "group_name_x",
        "group_name_y",
        "position_x",
        "position_y",
        "Monthlysize1",
        "Monthlysize2",
        "MonthlySameSize",
        "MonthlyB/M1",
        "MonthlyB/M2",
        "MonthlySameB/M",
        "MonthlyCrossOwnership",
        "MonthlyFCA",
        "Monthlyρ_5",
        "uo_x",
        "uo_y",
        "sgroup",
    ]
]
gdf["positionDif"] = gdf.position_x - gdf.position_y
gdf[
    [
        "MonthlySameSize",
        "MonthlySameB/M",
        "MonthlyCrossOwnership",
        "MonthlyFCA",
        "positionDif",
        "Monthlyρ_5",
        "sgroup",
    ]
].mean()

labels = "Same Industry", "Different Industry"
sizes = [gdf.sgroup.mean() * 100, 100 - gdf.sgroup.mean() * 100]
explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct="%1.1f%%",
    shadow=False,
    startangle=90,
)
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.


pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
plt.title("Pairs in the same business groups")
plt.savefig(pathS + "\\sameIndustryinBG.eps", bbox_inches="tight")
plt.savefig(pathS + "\\sameIndustryinBG.jpg", bbox_inches="tight")
plt.show()


#%%
Ndf = df2[df2.sBgroup == 0]
gg = Ndf.groupby("id")
ndf = gg.last()
ndf[clist] = gg[clist].mean()
ndf = ndf[
    [
        "symbol_x",
        "symbol_y",
        "id_x",
        "id_y",
        "group_name_x",
        "group_name_y",
        "position_x",
        "position_y",
        "Monthlysize1",
        "Monthlysize2",
        "MonthlySameSize",
        "MonthlyB/M1",
        "MonthlyB/M2",
        "MonthlySameB/M",
        "MonthlyCrossOwnership",
        "MonthlyFCA",
        "Monthlyρ_5",
        "uo_x",
        "uo_y",
        "sgroup",
    ]
]
ndf["positionDif"] = ndf.position_x - ndf.position_y
ndf[
    [
        "MonthlySameSize",
        "MonthlySameB/M",
        "MonthlyCrossOwnership",
        "MonthlyFCA",
        "positionDif",
        "Monthlyρ_5",
        "sgroup",
    ]
].mean()
t = ndf.sgroup.mean()
labels = "Same Industry", "Different Industry"
sizes = [t * 100, 100 - t * 100]
explode = (00.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(
    sizes, explode=explode, labels=labels, autopct="%1.1f%%", shadow=False, startangle=0
)
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.


pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
plt.title("Other pairs")
plt.savefig(pathS + "\\sameIndustryNoinBG.eps", bbox_inches="tight")
plt.savefig(pathS + "\\sameIndustryNoinBG.jpg", bbox_inches="tight")
plt.show()
#%%

alldf = df2
gg = alldf.groupby("id")
alldf = gg.last()
alldf[clist] = gg[clist].mean()
alldf = alldf[
    [
        "symbol_x",
        "symbol_y",
        "id_x",
        "id_y",
        "group_name_x",
        "group_name_y",
        "position_x",
        "position_y",
        "Monthlysize1",
        "Monthlysize2",
        "MonthlySameSize",
        "MonthlyB/M1",
        "MonthlyB/M2",
        "MonthlySameB/M",
        "MonthlyCrossOwnership",
        "MonthlyFCA",
        "Monthlyρ_5",
        "uo_x",
        "uo_y",
        "sgroup",
    ]
]
alldf["positionDif"] = alldf.position_x - alldf.position_y

#%%
from matplotlib.ticker import FuncFormatter


data = [
    [
        alldf.MonthlyFCA.mean(),
        alldf.MonthlySameSize.mean(),
        alldf["MonthlySameB/M"].mean(),
        alldf["MonthlyCrossOwnership"].mean() / 100,
    ],
    [
        ndf.MonthlyFCA.mean(),
        ndf.MonthlySameSize.mean(),
        ndf["MonthlySameB/M"].mean(),
        ndf["MonthlyCrossOwnership"].mean() / 100,
    ],
    [
        gdf.MonthlyFCA.mean(),
        gdf.MonthlySameSize.mean(),
        gdf["MonthlySameB/M"].mean(),
        gdf["MonthlyCrossOwnership"].mean() / 100,
    ],
]


x = [0, 1, 2]

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# fig.suptitle("Business Groups summary")
i, j = 0, 0
axs[i, j].bar(
    x,
    [thing[i + j] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)
x_axis_labels = ["Total", "Same business group", "Others"]
axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("Monthly FCA")
i, j = 0, 1
axs[i, j].bar(
    x,
    [thing[i + j] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)
x_axis_labels = ["Total", "Same business group", "Others"]
axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("SameSize")
i, j = 1, 0
axs[i, j].bar(
    x,
    [thing[i + j + 1] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)
x_axis_labels = ["Total", "Same business group", "Others"]
axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("SameBooktoMarket")
i, j = 1, 1
axs[i, j].bar(
    x,
    [thing[i + j + 1] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)
x_axis_labels = ["Total", "Same business group", "Others"]
axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("CrossOwnership")
axs[i, j].yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
fig.set_rasterized(True)
plt.savefig(pathS + "\\BGSummary.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\BGSummary.jpg", bbox_inches="tight")
plt.show()

#%%
clist = [
    "Monthlysize1",
    "Monthlysize2",
    "MonthlySameSize",
    "MonthlyB/M1",
    "MonthlyB/M2",
    "MonthlySameB/M",
    "MonthlyCrossOwnership",
    "MonthlyFCA",
    "sBgroup",
]
clist2 = [
    "symbol_x",
    "symbol_y",
    "id_x",
    "id_y",
    "group_name_x",
    "group_name_y",
    "position_x",
    "position_y",
    "Monthlysize1",
    "Monthlysize2",
    "MonthlySameSize",
    "MonthlyB/M1",
    "MonthlyB/M2",
    "MonthlySameB/M",
    "MonthlyCrossOwnership",
    "MonthlyFCA",
    "Monthlyρ_5",
    "uo_x",
    "uo_y",
    "sgroup",
    "sBgroup",
]
df2["Q3"] = 0
df2.loc[df2.NMFCA >= df2.NMFCA.quantile(0.75), "Q3"] = 1

alldf = df2
gg = alldf.groupby("id")
alldf = gg.last()
alldf[clist] = gg[clist].mean()
alldf = alldf[clist2]
alldf["positionDif"] = alldf.position_x - alldf.position_y
Gdf = df2[df2.Q3 == 1]
gg = Gdf.groupby("id")
gdf = gg.last()
gdf[clist] = gg[clist].mean()
gdf = gdf[clist2]
gdf["positionDif"] = gdf.position_x - gdf.position_y

Ndf = df2[df2.Q3 == 0]
gg = Ndf.groupby("id")
ndf = gg.last()
ndf[clist] = gg[clist].mean()
ndf = ndf[clist2]
ndf["positionDif"] = ndf.position_x - ndf.position_y
#%%
from matplotlib.ticker import FuncFormatter

data = [
    [
        alldf.MonthlyFCA.mean(),
        alldf.MonthlySameSize.mean(),
        alldf["MonthlySameB/M"].mean(),
        alldf["MonthlyCrossOwnership"].mean() / 100,
        alldf.sBgroup.mean(),
        alldf.Monthlyρ_5.mean(),
    ],
    [
        ndf.MonthlyFCA.mean(),
        ndf.MonthlySameSize.mean(),
        ndf["MonthlySameB/M"].mean(),
        ndf["MonthlyCrossOwnership"].mean() / 100,
        ndf.sBgroup.mean(),
        ndf.Monthlyρ_5.mean(),
    ],
    [
        gdf.MonthlyFCA.mean(),
        gdf.MonthlySameSize.mean(),
        gdf["MonthlySameB/M"].mean(),
        gdf["MonthlyCrossOwnership"].mean() / 100,
        gdf.sBgroup.mean(),
        gdf.Monthlyρ_5.mean(),
    ],
]

pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

x = [0, 1, 2]

fig, axs = plt.subplots(2, 3, figsize=(15, 10))

# fig.suptitle("Business Groups summary")
i, j = 0, 0
axs[i, j].bar(
    x,
    [thing[i + j] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)
x_axis_labels = ["Total", "Forth Qarter", "Others"]
axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("Monthly FCA")
i, j = 0, 1
axs[i, j].bar(
    x,
    [thing[i + j] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)

axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("SameSize")
i, j = 1, 0
axs[i, j].bar(
    x,
    [thing[i + j + 1] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)

axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("SameBooktoMarket")
i, j = 1, 1
axs[i, j].bar(
    x,
    [thing[i + j + 1] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)

axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("CrossOwnership")
axs[i, j].yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.1%}".format(y)))

i, j = 0, 2
axs[i, j].bar(
    x,
    [thing[i + j + 2] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)

axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("Same Business Group")
axs[i, j].yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))

i, j = 1, 2
axs[i, j].bar(
    x,
    [thing[i + j + 2] for thing in [data[0], data[2], data[1]]],
    color=(0.1, 0.1, 0.1, 0.1),
    edgecolor="blue",
)

axs[i, j].set_xticks(x)
axs[i, j].set_xticklabels(x_axis_labels)
axs[i, j].set_title("Monthly Correlation")
axs[i, j].yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.1%}".format(y)))

fig.set_rasterized(True)
plt.savefig(pathS + "\\QarterSummary.eps", rasterized=True, dpi=300)
plt.savefig(pathS + "\\QarterSummary.jpg", bbox_inches="tight")
plt.show()
#%%
labels = "Same Industry", "Different Industry"
sizes = [gdf.sgroup.mean() * 100, 100 - gdf.sgroup.mean() * 100]
explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct="%1.1f%%",
    shadow=False,
    startangle=90,
)
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.


pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
plt.title("Pairs in the forth quarter")
plt.savefig(pathS + "\\sameIndustryinQuarter.eps", bbox_inches="tight")
plt.savefig(pathS + "\\sameIndustryinQuarter.jpg", bbox_inches="tight")
plt.show()


labels = "Same Business group", "Others"
sizes = [gdf.sBgroup.mean() * 100, 100 - gdf.sBgroup.mean() * 100]
explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct="%1.1f%%",
    shadow=False,
    startangle=90,
)
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.


pathS = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
plt.title("Pairs in the forth quarter")
plt.savefig(pathS + "\\sameIBGinQuarter.eps", bbox_inches="tight")
plt.savefig(pathS + "\\sameIBGinQuarter.jpg", bbox_inches="tight")
plt.show()

# %%
a1 = df2.MonthlyFCA.describe().to_frame().rename(columns={"MonthlyFCA": "MonthlyFCA"}).T
a1 = a1.append(
    df2[df2.sBgroup == 1]
    .MonthlyFCA.describe()
    .to_frame()
    .rename(columns={"MonthlyFCA": "MonthlyFCA-Same"})
    .T
)
a1 = a1.append(
    df2[df2.sBgroup == 0]
    .MonthlyFCA.describe()
    .to_frame()
    .rename(columns={"MonthlyFCA": "MonthlyFCA-NSame"})
    .T
)
a1 = a1.append(
    df2[df2.sgroup == 1]
    .MonthlyFCA.describe()
    .to_frame()
    .rename(columns={"MonthlyFCA": "MonthlyFCA-SameI"})
    .T
)
a1 = a1.append(
    df2[df2.sgroup == 0]
    .MonthlyFCA.describe()
    .to_frame()
    .rename(columns={"MonthlyFCA": "MonthlyFCA-NSameI"})
    .T
)
a = (
    df2.MonthlyFCAPf.describe()
    .to_frame()
    .rename(columns={"MonthlyFCAPf": "MonthlyFCAP"})
    .T
)
a = a.append(
    df2[df2.sBgroup == 1]
    .MonthlyFCAPf.describe()
    .to_frame()
    .rename(columns={"MonthlyFCAPf": "MonthlyFCAP-Same"})
    .T
)
a = a.append(
    df2[df2.sBgroup == 0]
    .MonthlyFCAPf.describe()
    .to_frame()
    .rename(columns={"MonthlyFCAPf": "MonthlyFCAP-NSame"})
    .T
)
a = a.append(
    df2[df2.sgroup == 1]
    .MonthlyFCAPf.describe()
    .to_frame()
    .rename(columns={"MonthlyFCAPf": "MonthlyFCAP-SameI"})
    .T
)
a = a.append(
    df2[df2.sgroup == 0]
    .MonthlyFCAPf.describe()
    .to_frame()
    .rename(columns={"MonthlyFCAPf": "MonthlyFCAP-NSameI"})
    .T
)
a.append(a1)


# %%
df2[
    ["Monthlyρ_2", "Monthlyρ_4", "Monthlyρ_5", "MonthlyρLag_5", "Monthlyρ_6"]
].describe().T

# %%

print(df2[["sgroup", "sBgroup", "id"]].drop_duplicates("id").isnull().sum())


df2.drop_duplicates("id").groupby("sgroup").size().append(
    df2.drop_duplicates("id").groupby("sBgroup").size()
)

df2["sBsgroup"] = df2["sgroup"] + df2["sBgroup"]


df2.drop_duplicates("id").groupby("sgroup").size().append(
    df2.drop_duplicates("id").groupby("sBgroup").size()
).append(df2.drop_duplicates("id").groupby("sBsgroup").size())

# %%


# %%
df2["MonthlyCrossOwnership"] = df2.MonthlyCrossOwnership / 100
df2.groupby(["id"])[
    [
        "sgroup",
        "sBgroup",
        "Monthlysize1",
        "Monthlysize2",
        "MonthlySameSize",
        "MonthlyB/M1",
        "MonthlyB/M2",
        "MonthlySameB/M",
        "MonthlyCrossOwnership",
    ]
].mean().describe().T


# %%
# g3 = df3.groupby("t")
# a = g3.id.size().describe().to_frame().rename(columns ={'id':'Daily'}).T
# g1 = df1.groupby("t_Week")
# a = a.append(g1.id.size().describe().to_frame().rename(columns ={'id':'Fortnightly'}).T)
g2 = df2.groupby("t_Month")
t = g2.id.size()
t[t > 500].describe().to_frame().rename(columns={"id": "Monthly"}).T


# %%

gg = df2.groupby("id")
t = gg.filter(lambda x: x.sameBgChange.sum() > 0)
t["Period"] = 0
gg = t.groupby("id")
g = gg.get_group(98)


def period(g):
    g["Period"] = g.loc[g.sameBgChange == 1].t_Month.iloc[0]
    g["Period"] = g["t_Month"] - g["Period"]
    return g


t = gg.apply(period)
t.loc[t.id == 98][
    [
        "id",
        "MonthlySameB/M",
        "MonthlyCrossOwnership",
        "MonthlySameSize",
        "Monthlyρ_5",
        "sameBgChange",
        "becomeSameBG",
        "Period",
        "sBgroup",
    ]
]

result = t[
    [
        "id",
        "MonthlySameB/M",
        "MonthlyCrossOwnership",
        "MonthlySameSize",
        "Monthlyρ_5",
        "sameBgChange",
        "becomeSameBG",
        "Period",
    ]
]
result = result[(result.Period > -25) & (result.Period < 25)]
sns.lineplot(data=result, x="Period", y="Monthlyρ_5", hue="becomeSameBG")

#%%

sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA", hue="becomeSameBG")
# labels = idMonth.yearmonth.to_list()
# tickvalues = df2.t_Month
# plt.xticks(ticks=tickvalues[::-5], labels=labels[::-5], rotation="vertical")

# %%
df4 = pd.read_excel(
    r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Factors-Daily.xlsx"
)
df4[df4.date >= 20150325][["SMB", "HML", "Winner_Loser", "Market_return"]].describe().T

df2["T_Q"] = np.nan
for i in range(int(df2.t_Month.max() / 3) + 1):
    df2.loc[(df2.t_Month >= 3 * i) & (df2.t_Month < 3 * (i + 1)), "T_Q"] = i
    print(i)

i = 0
df2.loc[(df2.t_Month >= i) & (df2.t_Month < 3 * (i + 1))]

gg = df2.groupby(
    ["id", "T_Q", "id_x", "id_y", "group_name_x", "group_name_y", "sgroup"]
)
t = (
    gg[
        [
            "MonthlySizeRatio",
            "MonthlyMarketCap_x",
            "MonthlyMarketCap_y",
            "MonthlyPercentile_Rank_x",
            "MonthlyPercentile_Rank_y",
            "Monthlysize1",
            "Monthlysize2",
            "MonthlySameSize",
            "MonthlyFCAPf",
            "MonthlyFCA",
            "MonthlyFCAP*",
            "MonthlyFCA*",
        ]
    ]
    .mean()
    .reset_index()
)
t = t.rename(
    columns={
        "MonthlySizeRatio": "QuarterlySizeRatio",
        "MonthlyMarketCap_x": "QuarterlyMarketCap_x",
        "MonthlyMarketCap_y": "QuarterlyMarketCap_y",
        "MonthlyPercentile_Rank_x": "QuarterlyPercentile_Rank_x",
        "MonthlyPercentile_Rank_y": "QuarterlyPercentile_Rank_y",
        "Monthlysize1": "Quarterlysize1",
        "Monthlysize2": "Quarterlysize2",
        "MonthlySameSize": "QuarterlySameSize",
        "MonthlyFCAPf": "QuarterlyFCAPf",
        "MonthlyFCA": "QuarterlyFCA",
        "MonthlyFCAP*": "QuarterlyFCAP*",
        "MonthlyFCA*": "QuarterlyFCA*",
    }
)

Qdata = df2.merge(
    t, on=["id", "T_Q", "id_x", "id_y", "group_name_x", "group_name_y", "sgroup"]
)
Qdata = Qdata.drop(
    columns=[
        "MarketCap_x",
        "MarketCap_y",
        "Percentile_Rank_x",
        "Percentile_Rank_y",
        "size1",
        "size2",
        "SameSize",
        "MonthlySizeRatio",
        "MonthlyMarketCap_x",
        "MonthlyMarketCap_y",
        "MonthlyPercentile_Rank_x",
        "MonthlyPercentile_Rank_y",
        "Monthlysize1",
        "Monthlysize2",
        "MonthlySameSize",
        "MonthlyFCAPf",
        "MonthlyFCA",
        "MonthlyFCAP*",
        "MonthlyFCA*",
    ]
)


Qdata.to_csv(path + "QarterlyNormalzedFCAP5.1" + ".csv", index=False)

# %%
