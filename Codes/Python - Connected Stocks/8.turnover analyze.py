#%%
import pandas as pd

# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
#%%
result = pd.read_csv(path + "TurnOver_1400_10_06.csv")
df = pd.read_stata(path + "FirstStageAmihud.dta")
[
    [
        "_b_delta_amihud_market",
        "_b_delta_amihud_group",
        "_b_delta_amihud_industry",
        "_TimeVar",
    ]
]
df["_TimeVar"] = df._TimeVar.astype(int)
result["regidyear"] = result.regidyear.astype(int)
for i in [
    "_b_delta_amihud_market",
    "_b_delta_amihud_group",
    "_b_delta_amihud_industry",
]:
    mapdict = dict(zip(df._TimeVar, df[i]))
    result["Coef" + i[2:]] = result.regidyear.map(mapdict)

df = pd.read_stata(path + "FirstStageTurnover.dta")
[
    [
        "_b_deltamarket",
        "_b_deltagroup",
        "_b_deltaindustry",
        "_TimeVar",
    ]
]
df["_TimeVar"] = df._TimeVar.astype(int)
for i in [
    "_b_deltamarket",
    "_b_deltagroup",
    "_b_deltaindustry",
]:
    mapdict = dict(zip(df._TimeVar, df[i]))
    result["Coef" + i[2:]] = result.regidyear.map(mapdict)


#%%
df = result.drop_duplicates(subset=["regidyear"], keep="last")
df = df[
    [
        "symbol",
        "id",
        "group_name",
        "close_price",
        "shrout",
        "year",
        "month",
        "uo",
        "cfr",
        "cr",
        "centrality",
        "position",
        "Grouped",
        "marketCap",
        "regidyear",
        "Coef_delta_amihud_market",
        "Coef_delta_amihud_group",
        "Coef_delta_amihud_industry",
        "Coef_deltamarket",
        "Coef_deltagroup",
        "Coef_deltaindustry",
    ]
]
len(df.uo.unique())
#%%
t = result.groupby(["symbol", "regidyear"]).Amihud_value.mean().to_frame()
mapdict = dict(zip(t.index, t.Amihud_value))
df["Amihud"] = df.set_index(["symbol", "regidyear"]).index.map(mapdict)
t = result.groupby(["symbol", "regidyear"]).TurnOver.mean().to_frame()
mapdict = dict(zip(t.index, t.TurnOver))
df["TurnOver"] = df.set_index(["symbol", "regidyear"]).index.map(mapdict)
a = pd.read_csv(path + "lowImbalanceUO-Annual.csv")
mapdict = dict(zip(a.set_index(["year", "uo"]).index, a.lowImbalanceStd))

df["lowImbalanceStd"] = df.set_index(["year", "uo"]).index.map(mapdict)
df.to_csv(path + "turnovercrosssection_1400_06_28.csv", index=False)
# %%
list(df)
# %%
df["yearmonth"] = df.year.astype(str) + "-" + df.month.astype(str)
#%%
t = df.groupby(["uo", "yearmonth"]).marketCap.sum().to_frame()
mapingdict = dict(zip(t.index, t.marketCap))
df["weight"] = df.set_index(["uo", "yearmonth"]).index.map(mapingdict)
df["weight"] = df.marketCap / df.weight
df["Coef_deltagroup_mean"] = df["weight"] * df.Coef_deltagroup

#%%
tempt = df.groupby(["uo", "yearmonth"]).Coef_deltagroup_mean.sum().to_frame()
tempt = tempt.reset_index().rename(columns={"Coef_deltagroup_mean": "Coef_deltagroup"})
tempt = tempt.fillna(method="ffill")
tempt = tempt.groupby("uo")[["Coef_deltagroup"]].mean()
tempt["highBeta"] = 0
tempt.loc[tempt.Coef_deltagroup > tempt.Coef_deltagroup.quantile(0.5), "highBeta"] = 1
tempt
#%%
# gg = tempt.groupby("yearmonth")


# def highBeta(g):
#     print(g.name)
#     t = g.Coef_deltagroup.median()
#     print(len(g))
#     g["highBeta"] = 0
#     g.loc[g.Coef_deltagroup > t, "highBeta"] = 1
#     return g


# tempt = gg.apply(highBeta)

# tempt = tempt.set_index(["uo", "yearmonth"])
#%%
tt = pd.read_parquet(path + "MonthlyNormalzedFCAP9.2.parquet")
#%%
# tt['yearmonth'] = tt.year_of_year.astype(int).astype(str) + "-"+tt.month_of_year.astype(int).astype(str)
# mapingdict = dict(zip(tempt.index, tempt.Coef_deltagroup))
# tt["Coef_deltagroup_x"] = tt.set_index(["uo_x", "yearmonth"]).index.map(mapingdict)
# tt["Coef_deltagroup_y"] = tt.set_index(["uo_y", "yearmonth"]).index.map(mapingdict)

# mapingdict = dict(zip(tempt.index, tempt.highBeta))
# tt["highBeta_x"] = tt.set_index(["uo_x", "yearmonth"]).index.map(mapingdict)
# tt["highBeta_y"] = tt.set_index(["uo_y", "yearmonth"]).index.map(mapingdict)
mapingdict = dict(zip(tempt.index, tempt.Coef_deltagroup))
tt["Coef_deltagroup_x"] = tt.set_index(["uo_x"]).index.map(mapingdict)
tt["Coef_deltagroup_y"] = tt.set_index(["uo_y"]).index.map(mapingdict)
mapingdict = dict(zip(tempt.index, tempt.highBeta))
tt["highBeta_x"] = tt.set_index(["uo_x"]).index.map(mapingdict)
tt["highBeta_y"] = tt.set_index(["uo_y"]).index.map(mapingdict)
tt
#%%
tt.loc[tt.highBeta_x.isnull(), "highBeta_x"] = 0
tt.loc[tt.highBeta_y.isnull(), "highBeta_y"] = 0
tt.loc[tt.Coef_deltagroup_x.isnull(), "Coef_deltagroup_x"] = 0
tt.loc[tt.Coef_deltagroup_y.isnull(), "Coef_deltagroup_y"] = 0


# %%
result = pd.read_csv(path + "TurnOver_1400_10_06.csv")

# import math
# def func(x):
#     return math.exp(x)
# result['TurnOver'] = result.TurnOver.apply(func)
mresult = result.groupby(["symbol", "yearmonth"])[
    [
        "group_name",
        "date",
        "group_id",
        "shrout",
        "MarketCap",
        "year",
        "uo",
        "cfr",
        "cr",
        "position",
        "centrality",
        "Grouped",
    ]
].last()

tempt = result.groupby(["symbol", "yearmonth"])[["TurnOver"]].mean()
mapingdict = dict(zip(tempt.index, tempt.TurnOver))
mresult["mTurnOver"] = mresult.index.map(mapingdict)
mresult = mresult.reset_index()
#%%
from numpy import log as ln


def func(g):
    return ln(g.volume / g.MarketCap.sum())


tempt = (
    result.groupby(["yearmonth"])
    .apply(func)
    .to_frame()
    .reset_index()
    .set_index("yearmonth")
)
mapingdict = dict(zip(tempt.index, tempt.volume))
mresult["mTurnOver_market"] = mresult.yearmonth.map(mapingdict)
mresult
#%%
mresult = mresult.sort_values(by=["symbol", "date"], ascending=False).reset_index(
    drop=True
)


def func(g):
    g = g.sort_values(by=["date"], ascending=True)
    return g.mTurnOver.rolling(12).mean()


# mresult[
#     'mTurnOver_annual_avg'
#         ] =
tempt = mresult.groupby("symbol").apply(func).to_frame().reset_index()
mapingdict = dict(zip(tempt.level_1, tempt.mTurnOver))
mresult["mTurnOver_annual_avg"] = mresult.index.map(mapingdict)
mresult
#%%
from sklearn.linear_model import LinearRegression

mresult = mresult[(mresult.year > 1392) & (mresult.year < 1399)]


def trunreg(g):
    tem = g[
        [
            "yearmonth",
            "Grouped",
            "mTurnOver_annual_avg",
            "mTurnOver",
            "mTurnOver_market",
        ]
    ].dropna()
    print(g.name, len(tem))
    if len(tem) < 10:
        return
    g = tem
    y = g["mTurnOver"]
    x = g[["mTurnOver_market", "mTurnOver_annual_avg"]]
    OLSReg = LinearRegression(fit_intercept=True).fit(x, y)
    beta1, beta2 = OLSReg.coef_
    alpha = OLSReg.intercept_
    g["alpha"] = alpha
    g["beta1"] = beta1
    g["beta2"] = beta2
    return g


rr = mresult.groupby("symbol").apply(trunreg).reset_index().drop(columns="level_1")
#%%
rr["residual"] = rr.mTurnOver - (
    rr.alpha + rr.mTurnOver_market * rr.beta1 + rr.mTurnOver_annual_avg * rr.beta2
)
#%%
mapingdict = dict(zip(result.set_index(["symbol", "yearmonth"]).index, result.uo))
rr["uo"] = rr.set_index(["symbol", "yearmonth"]).index.map(mapingdict)
# %%
rr.groupby(["uo", "yearmonth"]).residual.std().to_frame().reset_index().groupby(
    "uo"
).residual.mean().to_frame()

tempt = rr.groupby(["uo", "yearmonth"]).residual.std().to_frame().reset_index()
t = rr.groupby(["uo", "yearmonth"]).size().to_frame()
mapingdict = dict(zip(t.index, t[0]))
tempt["Gsize"] = tempt.set_index(["uo", "yearmonth"]).index.map(mapingdict)
tempt
#%%
gg = tempt.groupby("yearmonth")


def high(g):
    print(g.name)
    t = g.residual.quantile(0.5)
    print(len(g))
    g["LowRes"] = 0
    g.loc[g.residual < t, "LowRes"] = 1
    return g


tempt = gg.apply(high)
tt["yearmonth"] = (
    tt.year_of_year.astype(int).astype(str)
    + "-"
    + tt.month_of_year.astype(int).astype(str)
)

mapingdict = dict(zip(tempt.set_index(["uo", "yearmonth"]).index, tempt.residual))
tt["TrunResStd_x"] = tt.set_index(["uo_x", "yearmonth"]).index.map(mapingdict)
tt["TrunResStd_y"] = tt.set_index(["uo_y", "yearmonth"]).index.map(mapingdict)

mapingdict = dict(zip(tempt.set_index(["uo", "yearmonth"]).index, tempt.Gsize))
tt["Gsize_x"] = tt.set_index(["uo_x", "yearmonth"]).index.map(mapingdict)
tt["Gsize_y"] = tt.set_index(["uo_y", "yearmonth"]).index.map(mapingdict)


mapingdict = dict(zip(tempt.set_index(["uo", "yearmonth"]).index, tempt.LowRes))
tt["LowRes_x"] = tt.set_index(["uo_x", "yearmonth"]).index.map(mapingdict)
tt["LowRes_y"] = tt.set_index(["uo_y", "yearmonth"]).index.map(mapingdict)
# %%
tt.loc[tt.LowRes_x.isnull(), "LowRes_x"] = 0
tt.loc[tt.LowRes_y.isnull(), "LowRes_y"] = 0
tt.loc[tt.Gsize_x.isnull(), "Gsize_x"] = 0
tt.loc[tt.Gsize_y.isnull(), "Gsize_y"] = 0
tt.loc[tt.TrunResStd_x.isnull(), "TrunResStd_x"] = 0
tt.loc[tt.TrunResStd_y.isnull(), "TrunResStd_y"] = 0
tt.to_csv(path + "MonthlyNormalzedFCAP9.3.csv", index=False)

tt.to_parquet(path + "MonthlyNormalzedFCAP9.3.parquet")
t = t.reset_index()
t


#%%
import seaborn as sns
import matplotlib.pyplot as plt

b = rr[rr.Grouped == 0].groupby("yearmonth").residual.std().to_frame().reset_index()
a = (
    rr.groupby(["uo", "yearmonth"])
    .residual.std()
    .to_frame()
    # .groupby("yearmonth")
    # .residual.mean()
    # .to_frame()
).reset_index()

markers = ["x", "o", "^"]

a["Grouped"] = 1
b["Grouped"] = 0

t = a.append(b).reset_index()


def func(x):
    X = x.split("-")
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    return X[0] + X[1]


t["yearmonth"] = t.yearmonth.apply(func)
t = t.sort_values(by="yearmonth").reset_index(drop=True)
t
#%%
pathR = r"E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Report\Output\\"
fig = plt.figure(figsize=(10, 5))
markers = {1: "s", 0: "X"}
g = sns.lineplot(
    data=t,
    x="yearmonth",
    y="residual",
    ci=0,
    hue="Grouped",
    style="Grouped",
    markers=markers,
)
a = t.yearmonth.unique()
labels = list(t.yearmonth.unique())
tickvalues = a
g.set_xticks(range(len(tickvalues))[::-5])  # <--- set the ticks first
g.set_xticklabels(labels[::-5], rotation="vertical")
plt.margins(x=0.01)

plt.ylabel("")
plt.xlabel("Year-Month")
plt.title("Monthly standard error of residual of monthly turnover")
plt.legend(
    [
        "Ungrouped",
        "Grouped",
    ]
)
fig.set_rasterized(True)
plt.savefig(pathR + "\\GroupedResSTD.eps", rasterized=True, dpi=300)
plt.savefig(pathR + "\\GroupedResSTD.png", bbox_inches="tight")
#%%
tt = (
    rr.groupby("Grouped")["residual"]
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
tt = tt.rename(columns={"count": "Firm $ \times $ Month"})
tt.to_latex(pathR + "\\ResidualTrunSummary.tex", column_format='lcccccccc',multicolumn = False,index_names = False)
tt
#%%
rr["uo"] = rr.uo.fillna("None")
tt = (
    rr.groupby(["Grouped", "uo", "yearmonth"])[["residual"]]
    .std()
    .reset_index()
    .groupby(["uo", "yearmonth", "Grouped"])[["residual"]]
    .mean()
    .reset_index()
    .groupby("Grouped")["residual"]
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
tt = tt.rename(columns={"count": "Group $ \times $ Month"})
tt.to_latex(pathR + "\\ResidualTrunStdSummary.tex", column_format='lcccccccc',multicolumn = False,index_names = False)
tt


#%%
