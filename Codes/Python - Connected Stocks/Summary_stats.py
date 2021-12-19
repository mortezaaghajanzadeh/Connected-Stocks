#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re as ree
import numpy as np
from matplotlib.ticker import FuncFormatter

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
pathResult = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Report\Output\\"

path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
pathResult = r"E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Report\Output\\"

#%%
def prepare():
    path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
    # path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
    df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")
    df["week_of_year"] = df.week_of_year.astype(int)
    df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
        df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
    )

    df = df[df.jalaliDate < 13990000]
    df = df[df.jalaliDate > 13930000]
    df = df[~df["5_Residual"].isnull()]
    print(len(df))
    df = df[df.volume > 0]
    print(len(df))
    try:
        df = df.drop(columns=["Delta_Trunover"])
    except:
        1 + 2
    return df


df = prepare()


#%%
gg = (
    df[["BGId", "id", "year_of_year", "Holder_id"]]
    .drop_duplicates()
    .groupby("year_of_year")
)
# g = gg.get_group(2019)


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
# g = gg.get_group(2015)


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


# %%
tempt = a1.append(a2).drop_duplicates()
tempt = tempt.T.rename(columns={"year_of_year": "Year"})

tempt.Year = tempt.Year.astype(int)
tempt["Year"] = tempt.Year + 621
tempt = tempt.drop(
    columns=[
        "Max. Number of Members",
        "Max. Number of Owners",
        "Max. Block. Ownership",
        "No. of Firms not in Groups",
        "Med. of  Number of Members",
        # "Med. Number of Owners",
        "Med. Block. Ownership",
    ]
).rename(
    columns={
        "No. of Holders": "No. of Blockholders",
        "Avg. Number of Members": "Ave. Number of group Members",
        "Av. Holder Percent": "Ave. ownership of each Blockholders",
        "Av. Number of Owners": "Ave. Number of Owners",
        "Av. Block. Ownership": "Ave. Block. Ownership",
        "Med. of Owners' Percent": "Med. ownership of each Blockholders",
    }
)
tempt = tempt.set_index("Year").transpose().astype(int)


tempt.to_latex(pathResult + "summaryOfOwnership.tex")
tempt
#%%

n = path + "MonthlyNormalzedFCAP9.3" + ".parquet"
df2 = pd.read_parquet(n)
#%%
ff = df2[
    [
        "MonthlyMarketCap_x",
        "MonthlyMarketCap_y",
    ]
]
ff["m"] = ff.MonthlyMarketCap_x / ff.MonthlyMarketCap_y
ff["mm"] = ff.MonthlyMarketCap_y / ff.MonthlyMarketCap_x
ff["r"] = ff.m
ff.loc[ff.r < 1, "r"] = ff[ff.r < 1].mm
ff
#%%
df2.id.max(), len(set(df2.id_x.to_list() + df2.id_y.to_list()))

#%%
PG = df2[
    ["BGId_x", "BGId_y", "year_of_year", "id", "sBgroup", "numberCommonHolder"]
].drop_duplicates()
gg = PG.groupby("year_of_year")
# g = gg.get_group(2019)


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
# g = gg.get_group(1)


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
# g = gg.get_group(2015)


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

#%%
tempt = a1.append(a2).drop_duplicates()
tempt = tempt.T.rename(columns={"year": "Year"})

tempt["Year"] = tempt["Year"].astype(int)
tempt["Year"] = tempt.Year + 621
tempt = tempt.drop(
    columns=[
        "Max. Number of Common owner",
        "Max. Number of Pairs in one Group",
        "Max. Number of Common owner",
        "Max. Number of Owners",
    ]
).rename(
    columns={
        "Number of Pairs not in one Group": "No. of Pairs not in the same Group",
        "Number of Pairs in one Group": "No. of Pairs in the same Group",
        "Avg. Number of Common owner": "Ave. Number of Common owner",
        "Avg. Number of Pairs in one Group": "Ave. Number of Pairs in one Group",
        "Av. Holder Percent": "Ave. Percent of each blockholder",
        "Median of Owners' Percent": "Med. Percent of each blockholder",
        "Av. Number of Owners": "Ave. Number of Owners",
        "Av. Block. Ownership": "Ave. Block. Ownership",
    }
)
mlist = [
    "Year",
    "No. of Pairs",
    # "No. of Groups",
    "No. of Pairs not in Groups",
    "No. of Pairs not in the same Group",
    "No. of Pairs in the same Group",
    "Ave. Number of Common owner",
    # "Med. Number of Common owner",
    # "Average Percent of each blockholder",
    # "Med. Percent of each blockholder",
    # "Ave. Number of Pairs in one Group",
    # "Med. Number of Pairs in one Group",
    # "Average Number of Owners",
    # "Med. Number of Owners",
    # "Average Block. Ownership",
    # "Med. Block. Ownership",
]
tempt = tempt[mlist].set_index("Year").T.astype(int)
tempt.to_latex(pathResult + "summaryOfPairs.tex")
tempt
#%%

df2.groupby("t_Month").size().describe().to_frame().rename(
    columns={0: "Number of unique paris"}, index={"50%": "Median"}
).T.drop(columns=["count", "std", "25%", "75%"]).astype(int).to_latex(
    pathResult + "numberofPairs.tex"
)
df2.groupby("t_Month").size().describe().to_frame().rename(
    columns={0: "Number of unique paris"}, index={"50%": "Median"}
).T.drop(columns=["count", "std", "25%", "75%"]).astype(int)

#%%

Monthtime = (
    df2[["t_Month", "Year_Month"]]
    .drop_duplicates()
    .sort_values(by=["t_Month"])
    .rename(columns={"Year_Month": "yearmonth"})
)
#%%
g2 = df2.groupby("t_Month")
df2.loc[df2.uo_x.isnull(), "sBgroup"] = np.nan
df2.loc[df2.uo_y.isnull(), "sBgroup"] = np.nan


def s(g):
    t = g.groupby("sBgroup").size().to_frame().T
    t[3] = g.sBgroup.isnull().sum()
    return t


idMonth = g2.apply(s).reset_index()
idMonth = idMonth[idMonth[1] > 100]
mapdict = dict(zip(Monthtime.t_Month, Monthtime.yearmonth))
idMonth["yearmonth"] = idMonth["t_Month"].map(mapdict)
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
plt.savefig(pathResult + "idMonth.eps", bbox_inches="tight")
plt.savefig(pathResult + "idMonth.png", bbox_inches="tight")
#%%
df[df.jalaliDate > 13980000]
#%%
idMonth[idMonth.index > 60]
#%%

fig = plt.figure(figsize=(8, 4))
palette = sns.color_palette()[:2]
g = sns.lineplot(data=df2, x="t_Month", y="Monthlyρ_5", hue="sBgroup", palette=palette)
labels = Monthtime.yearmonth.to_list()
tickvalues = Monthtime.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
plt.ylabel("")
plt.xlabel("Year-Month")
plt.legend(["Others", "In the same BG"])
plt.margins(x=0.01)
plt.title("Co-movement Time Series")
fig.set_rasterized(True)
fig.tight_layout()
plt.savefig(pathResult + "ComovementtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "ComovementtimeSeries.png", bbox_inches="tight")
#%%
fig = plt.figure(figsize=(8, 4))
g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA")
labels = Monthtime.yearmonth.to_list()
tickvalues = Monthtime.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)

plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
fig.set_rasterized(True)
fig.tight_layout()
plt.savefig(pathResult + "FCAtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "FCAtimeSeries.png", bbox_inches="tight")
#%%

#%%
df2["PairType"] = "Hybrid"
df2.loc[(df2.GRank_x < 5) & (df2.GRank_y < 5), "PairType"] = "Small"
df2.loc[(df2.GRank_x >= 5) & (df2.GRank_y >= 5), "PairType"] = "Large"
fig = plt.figure(figsize=(8, 4))

g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA", hue="PairType")
labels = Monthtime.yearmonth.to_list()
tickvalues = Monthtime.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
fig.set_rasterized(True)
fig.tight_layout()
plt.savefig(pathResult + "\\FCAtimeSeriesPairType.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "\\FCAtimeSeriesPairType.png", bbox_inches="tight")
#%%

fig = plt.figure(figsize=(8, 4))

g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA", hue="sBgroup", palette="tab10")
labels = Monthtime.yearmonth.to_list()
tickvalues = Monthtime.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.legend(["Others", "In the same BG"])
plt.margins(x=0.01)
plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
fig.set_rasterized(True)
fig.tight_layout()
plt.savefig(pathResult + "\\FCAtimeSeriesBG.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "\\FCAtimeSeriesBG.png", bbox_inches="tight")
#%%
fig = plt.figure(figsize=(8, 4))

g = sns.lineplot(data=df2, x="t_Month", y="MonthlyFCA")
sns.lineplot(data=df2, x="t_Month", y="MonthlyFCAPf")
labels = Monthtime.yearmonth.to_list()
tickvalues = Monthtime.t_Month
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)
plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Common Ownership Time Series")
plt.legend(["FCA", "FCAP"])
fig.set_rasterized(True)
fig.tight_layout()
plt.savefig(pathResult + "\\FCAComparetimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "\\FCAComparetimeSeries.png", bbox_inches="tight")
#%%


df["Grouped"] = 1
df.loc[df.uo.isnull(), "Grouped"] = 0
df = df.drop_duplicates(subset=["symbol", "year"])
fig = plt.figure(figsize=(8, 4))
g = sns.lineplot(data=df, x="year", y="Grouped")
g.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
plt.ylabel("")
plt.xlabel("Year")
plt.title("Group affiliated firms' Time Series")
fig.set_rasterized(True)
plt.savefig(pathResult + "\\BGtimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "\\BGtimeSeries.png", bbox_inches="tight")
#%%

te = df.groupby(["year", "Grouped"]).MarketCap.sum().to_frame().reset_index()
te = te[te.Grouped == 0].merge(te[te.Grouped == 1], on="year")
te["Group affiliated"] = te.MarketCap_y / (te.MarketCap_y + te.MarketCap_x)
te["Not Group affiliated"] = te.MarketCap_x / (te.MarketCap_y + te.MarketCap_x)
g = te.plot(y=["Group affiliated", "Not Group affiliated"], x="year", figsize=(8, 4))
g.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
plt.ylabel("")
plt.xlabel("Year")
plt.title("Group affiliated market caps' Time Series")
fig.set_rasterized(True)
plt.savefig(pathResult + "\\BGMarketCaptimeSeries.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "\\BGMarketCaptimeSeries.png", bbox_inches="tight")


#%%
mlist = [
    "id",
    "Monthlyρ_2",
    "Monthlyρ_4",
    "Monthlyρ_5",
    "Monthlyρ_Residual_Bench",
    # "Monthlyρ_5Lag",
]
# tempt = df2[df2.Monthlyρ_2<0.9]
tempt = df2[mlist].groupby("id")[mlist[1::]].mean().describe().T

latex = (
    tempt.drop(columns=["count", "25%", "75%"])
    .rename(
        index={
            "Monthlyρ_2": " CAPM + Industry",
            "Monthlyρ_4": "4 Factor",
            "Monthlyρ_5": "4 Factor + Industry",
            "Monthlyρ_5Lag": "4 Factor + Industry (With Lag)",
            "Monthlyρ_Residual_Bench": "Benchmark",
        },
        columns={
            "50%": "median",
        },
    )
    .round(3)
    .to_latex(pathResult + "CorrelationsResultsText.tex")
)
tempt.drop(columns=["count", "25%", "75%"]).rename(
    index={
        "Monthlyρ_2": " CAPM + Industry",
        "Monthlyρ_4": "4 Factor",
        "Monthlyρ_5": "4 Factor + Industry",
        "Monthlyρ_5Lag": "4 Factor + Industry (With Lag)",
        "Monthlyρ_Residual_Bench": "Benchmark",
    },
    columns={
        "50%": "median",
    },
).round(3)

#%%
df2[df2.Monthlyρ_5 == df2.Monthlyρ_5.max()][
    ["symbol_x", "symbol_y", "Monthlyρ_5", "jalaliDate"]
]
df2.Monthlyρ_5.quantile(0.995)

#%%
df2["sBsgroup"] = df2["sgroup"] + df2["sBgroup"]


t = df2.drop_duplicates("id")
tempt = {}
tempt["SameIndustry"] = {"Yes": len(t[t.sgroup == 1]), "No": len(t[t.sgroup == 0])}
tempt["SameGroup"] = {"Yes": len(t[t.sBgroup == 1]), "No": len(t[t.sBgroup == 0])}
tempt["SameGroup & SameIndustry"] = {
    "Yes": len(t[t.sBsgroup == 2]),
    "No": len(t[t.sBgroup != 2]),
}
tempt = pd.DataFrame.from_dict(tempt, orient="index")
tempt = tempt.T
#%%
tempt["p1"] = tempt.SameIndustry.sum()
tempt["p1"] = "(" + (tempt.SameIndustry / tempt.p1 * 100).round(1).astype(str) + "%)"
tempt["p2"] = tempt.SameGroup.sum()
tempt["p2"] = "(" + (tempt.SameGroup / tempt.p2 * 100).round(1).astype(str) + "%)"
tempt["p3"] = tempt["SameGroup & SameIndustry"].sum()
tempt["p3"] = (
    "("
    + (tempt["SameGroup & SameIndustry"] / tempt.p3 * 100).round(1).astype(str)
    + "%)"
)
tempt[
    ["SameIndustry", "p1", "SameGroup", "p2", "SameGroup & SameIndustry", "p3"]
].rename(columns={"p1": "", "p2": "", "p3": ""}).T.to_latex(
    pathResult + "SameGroupSameIndustry.tex"
)
tempt[
    ["SameIndustry", "p1", "SameGroup", "p2", "SameGroup & SameIndustry", "p3"]
].rename(columns={"p1": "", "p2": "", "p3": ""}).T
# %%
tempt = (
    df2.groupby(["id"])[
        [
            # "sgroup",
            # "sBgroup",
            "Monthlysize1",
            "Monthlysize2",
            "MonthlySameSize",
            "MonthlyB/M1",
            "MonthlyB/M2",
            "MonthlySameB/M",
            "MonthlyCrossOwnership",
        ]
    ]
    .mean()
    .describe()
    .T.drop(columns=["count", "25%", "75%"])
    .rename(
        columns={
            "50%": "median",
        }
    )
    .round(2)
    .T.rename(
        columns={
            "sgroup": "SameIndustry",
            "sBgroup": "SameGroup",
            "Monthlysize1": "Size1",
            "Monthlysize2": "Size2",
            "MonthlySameSize": "SameSize",
            "MonthlyB/M1": "BookToMarket1",
            "MonthlyB/M2": "BookToMarket2",
            "MonthlySameB/M": "SameBookToMarket",
            "MonthlyCrossOwnership": "CrossOwnership",
        }
    )
).T


tempt.to_latex(pathResult + "ControlsSummary.tex")
tempt
# %%
tempt = pd.DataFrame()
t = (
    df2[
        [
            "MonthlyFCA",
            "MonthlyFCAPf",
        ]
    ]
    .describe()
    .drop(index=["count"])
    .T
)
t["index"] = "All"
t = t.reset_index().set_index("index").rename(columns={"level_0": "variable"})
tempt = tempt.append(t.round(3))
t = (
    df2[df2.sBgroup == 1][
        [
            "MonthlyFCA",
            "MonthlyFCAPf",
        ]
    ]
    .describe()
    .drop(index=["count"])
    .T
)
t["index"] = "Same Group"
t = t.reset_index().set_index("index").rename(columns={"level_0": "variable"})
tempt = tempt.append(t.round(3))
t = (
    df2[df2.sBgroup == 0][
        [
            "MonthlyFCA",
            "MonthlyFCAPf",
        ]
    ]
    .describe()
    .drop(index=["count"])
    .T
)
t["index"] = "Not Same Group"
t = t.reset_index().set_index("index").rename(columns={"level_0": "variable"})
tempt = tempt.append(t.round(3))
t = (
    df2[df2.sgroup == 1][
        [
            "MonthlyFCA",
            "MonthlyFCAPf",
        ]
    ]
    .describe()
    .drop(index=["count"])
    .T
)
t["index"] = "Same Industry"
t = t.reset_index().set_index("index").rename(columns={"level_0": "variable"})
tempt = tempt.append(t.round(3))
t = (
    df2[df2.sgroup == 0][
        [
            "MonthlyFCA",
            "MonthlyFCAPf",
        ]
    ]
    .describe()
    .drop(index=["count"])
    .T
)
t["index"] = "Not Same Industry"
t = t.reset_index().set_index("index").rename(columns={"level_0": "variable"})
tempt = tempt.append(t.round(3))
#%%
tempt.sort_values(by=["variable"])
#%%
# a = (
#     tempt.replace("MonthlyFCAPf", "FCAP")
#     .replace("MonthlyFCA", "MFCAP")
#     .sort_values(by=["variable"])
#     .reset_index()
#     .rename(columns={"index": "subset"})
#     .set_index(
#         [
#             "variable",
#             "subset",
#         ]
#     )
#     .round(3)
#     .T
# )
#%%
tempt.reset_index()
#%%
a = (
    tempt[tempt.variable == "MonthlyFCA"]
    .merge(
        tempt[tempt.variable == "MonthlyFCAPf"],
        left_index=True,
        right_index=True,
    )
    .T
)
a["variable"] = "MonthlyFCA"
mlist = ["variable_y", "mean_y", "std_y", "min_y", "25%_y", "50%_y", "75%_y", "max_y"]
a.loc[a.index.isin(mlist), "variable"] = "MonthlyFCAPf"
a = a.reset_index()
a["index"] = a["index"].apply(lambda x: x.split("_")[0])
a = a[~a["index"].isin(["25%", "75%"])]
a.loc[a["index"] == "50%", "index"] = "median"
a = (
    a.set_index(["variable", "index"])
    .T.drop(columns=[("MonthlyFCA", "variable"), ("MonthlyFCAPf", "variable")])
    .replace("MonthlyFCAPf", "FCAP")
    .replace("MonthlyFCA", "MFCAP")
    .reset_index()
    .rename(columns={"index": "subset"})
    .set_index("subset")
)
a.to_latex(pathResult + "FCACal.tex")
a

# %%

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
plt.title("Pairs in the same business groups")
plt.savefig(pathResult + "sameIndustryinBG.eps", bbox_inches="tight")
plt.savefig(pathResult + "sameIndustryinBG.jpg", bbox_inches="tight")
plt.show()
# %%
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

plt.title("Other pairs")
plt.savefig(pathResult + "sameIndustryNoinBG.eps", bbox_inches="tight")
plt.savefig(pathResult + "sameIndustryNoinBG.jpg", bbox_inches="tight")
plt.show()
# %%

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
plt.savefig(pathResult + "BGSummary.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "BGSummary.jpg", bbox_inches="tight")
plt.show()
# %%

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
plt.savefig(pathResult + "\\QarterSummary.eps", rasterized=True, dpi=300)
plt.savefig(pathResult + "\\QarterSummary.jpg", bbox_inches="tight")
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
plt.title("Pairs in the forth quarter")
plt.savefig(pathResult + "\\sameIndustryinQuarter.eps", bbox_inches="tight")
plt.savefig(pathResult + "\\sameIndustryinQuarter.jpg", bbox_inches="tight")
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
plt.title("Pairs in the forth quarter")
plt.savefig(pathResult + "\\sameIBGinQuarter.eps", bbox_inches="tight")
plt.savefig(pathResult + "\\sameIBGinQuarter.jpg", bbox_inches="tight")
plt.show()
# %%
