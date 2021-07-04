#%%
from numpy.core.numeric import True_
import pandas as pd
import re as ree

#%%
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
n1 = path + "MonthlyNormalzedFCAP6.1" + ".parquet"
df = pd.read_parquet(n1)
# %%
from finance_byu.fama_macbeth import (
    fama_macbeth,
    fama_macbeth_parallel,
    fm_summary,
    fama_macbeth_numba,
)
import numpy as np

# %%
df = df[df.jalaliDate < 13990000]
df = df[
    [
        "Monthlyρ_5_f",
        "Monthlyρ_5",
        "MonthlyFCA*",
        "MonthlySizeRatio",
        "Monthlysize1",
        "Monthlysize2",
        "MonthlySameSize",
        "MonthlyB/M1",
        "MonthlyB/M2",
        "MonthlySameB/M",
        "t_Month",
        "id",
        "GRank_x",
        "GRank_y",
        "SameGRank",
        "Holder_act",
        "sgroup",
        "sBgroup",
        "BGId_x",
        "BGId_y",
        "symbol_x",
        "symbol_y",
    ]
]
df = df.dropna()
df["MonthlyFCA*>Median"] = 0
df.loc[df["MonthlyFCA*"] > df["MonthlyFCA*"].median(), "MonthlyFCA*>Median"] = 1
df["Median*FCA*"] = df["MonthlyFCA*>Median"] * df["MonthlyFCA*"]
df["SBFCA*"] = df["sBgroup"] * df["MonthlyFCA*"]
df["HAFCA*"] = df["Holder_act"] * df["MonthlyFCA*"]
#%%
result = fama_macbeth(
    df,
    "t_Month",
    "Monthlyρ_5_f",
    [
        "MonthlyFCA*",
        "sBgroup",
        "SBFCA*",
        "Holder_act",
        "HAFCA*",
        "Monthlyρ_5",
        "MonthlySameSize",
        "MonthlySameB/M",
        "sgroup",
    ],
    intercept=True,
)


# %%
df4 = df[df.sBgroup == 1]
# gg = df4.groupby("BGId_x")
# g = gg.get_group(1)


# def reg(g):
#     print(g.name)
#     result = fama_macbeth(
#         g,
#         "t_Month",
#         "Monthlyρ_5_f",
#         [
#             "MonthlyFCA*",
#             "sBgroup",
#             "SBFCA*",
#             "Holder_act",
#             "HAFCA*",
#             "Monthlyρ_5",
#             "MonthlySameSize",
#             "MonthlySameB/M",
#             "sgroup",
#         ],
#         intercept=True,
#     )
#     return fm_summary(result).T["SBFCA*"].iloc[0]


# betas = gg.apply(reg)
# betas = betas.sort_values()


# #%%
# tt = betas
# BGId = pd.read_csv(path + "BGId.csv")
# tt = tt.to_frame().reset_index()
# tt = tt.merge(BGId, left_on="BGId_x", right_on="BGId", how="left")
# bb = tt.head()
# bb = bb.append(tt.tail())

# tt.to_csv(path + "Betas.csv", index=False)
# bb
sigId = [33, 3, 43, 14, 25, 30, 7, 19, 12, 0, 42, 28, 36, 23]

# %%
# Leastdf = df4[df4.BGId_x.isin(set(betas.head().index))]
# Mostdf = df4[df4.BGId_x.isin(set(betas.tail().index))]
# LestSymbols = set(Leastdf.symbol_x)
# LestSymbols.update(set(Leastdf.symbol_y))
# MostSymbols = set(Mostdf.symbol_x)
# MostSymbols.update(set(Mostdf.symbol_y))

BankUO = [40.0, 3.0, 41.0, 22.0, 42.0, 2.0, 1.0, 0.0]
Bankdf = df4[df4.BGId_x.isin(BankUO)]
BankSymbols = set(Bankdf.symbol_x)
BankSymbols.update(set(Bankdf.symbol_y))


InvInG = [33.0, 23.0, 40.0, 38.0, 21.0, 17.0, 7.0, 32.0, 25.0, 27.0]
Invdf = df4[df4.BGId_x.isin(InvInG)]
InvdfSymbols = set(Invdf.symbol_x)
InvdfSymbols.update(set(Invdf.symbol_y))

BankIn = [23.0, 21.0, 17.0, 7.0, 41.0]
BankIndf = df4[df4.BGId_x.isin(BankIn)]
BankInSymbols = set(BankIndf.symbol_x)
BankInSymbols.update(set(BankIndf.symbol_y))

# %%
PriceData = pd.read_parquet(
    r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
    + "Stocks_Prices_1399-09-12.parquet"
)


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


col = "name"
PriceData[col] = PriceData[col].apply(lambda x: convert_ar_characters(x))

PriceData["date1"] = PriceData["date"].apply(vv4)
PriceData["date1"] = pd.to_datetime(PriceData["date1"])
PriceData["week_of_year"] = (PriceData["date1"].dt.week).astype(str)
PriceData["Month_of_year"] = (PriceData["date1"].dt.month).astype(str)
PriceData["year_of_year"] = (PriceData["date1"].dt.year).astype(str)


def vv(x):
    if len(x) < 2:
        return "0" + x
    return x


PriceData["Month_of_year"] = PriceData["Month_of_year"].apply(vv)
PriceData["YearMonth"] = PriceData["year_of_year"] + PriceData["Month_of_year"]


def vv(X):
    X = X.split("-")
    return int(X[0] + X[1] + X[2])


PriceData["jalaliDate"] = PriceData.jalaliDate.apply(vv)
PriceData = PriceData[PriceData.jalaliDate < 13990000]

PriceData = PriceData[PriceData.jalaliDate > 13940000]

gg = PriceData.groupby("name")
PriceData["Ret"] = gg["close_price"].pct_change()


def monthStd(g):
    tempt = g.groupby("YearMonth")["Ret"].std().to_frame()
    mapdict = dict(zip(tempt.index, tempt.Ret))
    g["std"] = g.YearMonth.map(mapdict)
    return g


PriceData = gg.apply(monthStd)

PriceData = PriceData.drop_duplicates(
    subset=["YearMonth", "name"], keep="last"
).sort_values(by=["name", "YearMonth"])
PriceData["MonthRet"] = PriceData.groupby("name")["close_price"].pct_change(1) * 100
PriceData = PriceData[abs(PriceData.MonthRet) < 300]
PriceData = PriceData[abs(PriceData['std']) < 2]
# %%
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
sdf = pd.read_csv(path + "Cleaned_Stocks_Holders_1399-09-12_From94.csv")
sdf = sdf[["symbol", "jalaliDate", "date", "shrout"]].rename(columns={"symbol": "name"})

sdf["date1"] = sdf["date"].apply(vv4)
sdf["date1"] = pd.to_datetime(sdf["date1"])
sdf["week_of_year"] = (sdf["date1"].dt.week).astype(str)
sdf["Month_of_year"] = (sdf["date1"].dt.month).astype(str)
sdf["year_of_year"] = (sdf["date1"].dt.year).astype(str)


def vv(x):
    if len(x) < 4:
        return "0" + x
    return x


sdf["Month_of_year"] = sdf["Month_of_year"].apply(vv)

sdf["YearMonth"] = sdf["year_of_year"] + sdf["Month_of_year"]
sdf = sdf[sdf.jalaliDate < 13990000]

sdf = sdf[["name", "YearMonth", "shrout"]]
sdf = sdf.drop_duplicates(subset=["YearMonth", "name"], keep="last").sort_values(
    by=["name", "YearMonth"]
)

# %%
PriceData = PriceData.merge(sdf, how="left", on=["name", "YearMonth"])
PriceData["shrout"] = PriceData.groupby("name")["shrout"].fillna(method="bfill")

# %%# %%
# LessPriceData = (
#     PriceData[PriceData.name.isin(LestSymbols)]
#     .groupby("YearMonth")
#     .filter(lambda x: x.size > 20)
# )[["YearMonth", "MonthRet", "shrout", "name", "close_price"]]
# MostPriceData = (
#     PriceData[PriceData.name.isin(MostSymbols)]
#     .groupby("YearMonth")
#     .filter(lambda x: x.size > 20)
# )[["YearMonth", "MonthRet", "shrout", "name", "close_price"]]

BankPriceData = (
    PriceData[PriceData.name.isin(BankSymbols)]
    .groupby("YearMonth")
    .filter(lambda x: x.size > 20)
)[["YearMonth", "MonthRet", "shrout", "name", "close_price", "std"]]

BankInPriceData = (
    PriceData[PriceData.name.isin(InvdfSymbols)]
    .groupby("YearMonth")
    .filter(lambda x: x.size > 20)
)[["YearMonth", "MonthRet", "shrout", "name", "close_price", "std"]]
InvPriceData = (
    PriceData[PriceData.name.isin(BankInSymbols)]
    .groupby("YearMonth")
    .filter(lambda x: x.size > 20)
)[["YearMonth", "MonthRet", "shrout", "name", "close_price", "std"]]

OtherPriceData = (
    PriceData[
        (
            ~PriceData.name.isin(BankInSymbols)
            & (~PriceData.name.isin(InvdfSymbols))
            & (~PriceData.name.isin(BankSymbols))
        )
    ]
    .groupby("YearMonth")
    .filter(lambda x: x.size > 20)
)[["YearMonth", "MonthRet", "shrout", "name", "close_price", "std"]]


# %%


# %%
def cal(g):
    g["Weight"] = g["close_price"] * g["shrout"]
    g["Weight"] = g["Weight"] / (g["Weight"].sum())
    return (g["Weight"] * g["MonthRet"]).sum()


# LessData = (
#     LessPriceData.groupby("YearMonth").apply(cal).to_frame().rename(columns={0: "Less"})
# )
# MostData = (
#     MostPriceData.groupby("YearMonth").apply(cal).to_frame().rename(columns={0: "Most"})
# )

BankData = (
    BankPriceData.groupby("YearMonth").apply(cal).to_frame().rename(columns={0: "Bank"})
)
BankInData = (
    BankInPriceData.groupby("YearMonth")
    .apply(cal)
    .to_frame()
    .rename(columns={0: "BankIn"})
)
InvData = (
    InvPriceData.groupby("YearMonth").apply(cal).to_frame().rename(columns={0: "Inv"})
)
OtherData = (
    OtherPriceData.groupby("YearMonth")
    .apply(cal)
    .to_frame()
    .rename(columns={0: "Other"})
)


def cal(g):
    g["Weight"] = g["close_price"] * g["shrout"]
    g["Weight"] = g["Weight"] / (g["Weight"].sum())
    return (g["Weight"] * g["std"]).sum()


BankData2 = (
    BankPriceData.groupby("YearMonth").apply(cal).to_frame().rename(columns={0: "Bank"})
)
BankInData2 = (
    BankInPriceData.groupby("YearMonth")
    .apply(cal)
    .to_frame()
    .rename(columns={0: "BankIn"})
)
InvData2 = (
    InvPriceData.groupby("YearMonth").apply(cal).to_frame().rename(columns={0: "Inv"})
)
OtherData = (
    OtherPriceData.groupby("YearMonth")
    .apply(cal)
    .to_frame()
    .rename(columns={0: "Other"})
)

# %%

Data = BankInData.merge(BankData, left_index=True, right_index=True).reset_index()
Data = InvData.merge(Data, left_index=True, right_on="YearMonth")
Data = OtherData.merge(Data, left_index=True, right_on="YearMonth")
Data["CROther_Ret"] = Data["Other"].cumsum()
Data["CRBank_Ret"] = Data["Bank"].cumsum()
Data["CRBankIn_Ret"] = Data["BankIn"].cumsum()
Data["CRInv_Ret"] = Data["Inv"].cumsum()


Data2 = BankInData2.merge(BankData2, left_index=True, right_index=True).reset_index()
Data2 = InvData2.merge(Data2, left_index=True, right_on="YearMonth")
Data2 = OtherData.merge(Data2, left_index=True, right_on="YearMonth")
Data["Other_std"] = Data2["Other"]
Data["Bank_std"] = Data2["Bank"]
Data["BankIn_std"] = Data2["BankIn"]
Data["Inv_std"] = Data2["Inv"]


# %%
import matplotlib.pyplot as plt

Data.plot(
    use_index=True,
    figsize=(8, 4),
    y=["Bank_std", "BankIn_std", "Inv_std", "Other_std"],
)
labels = Data.YearMonth.to_list()
tickvalues = Data.index


plt.xticks(ticks=tickvalues[::-2], labels=labels[::-2], rotation="vertical")
plt.ylabel("The Cumulative Return")
plt.xlabel("Year-Month")
plt.legend(
    [
        "The Banks' Business Group",
        "Groups that consist of one bank",
        "Groups that consist of one Investment firm",
        "Other",
    ]
)
plt.title("The Cumulative return of portfolios  ")
# pathS = r"G:\Dropbox\Dropbox\Connected Stocks\Final Report"
# plt.savefig(pathS + "\\Effective3.eps", bbox_inches="tight")
# plt.savefig(pathS + "\\Effective3.png", bbox_inches="tight")


# Data.plot(use_index=True, figsize=(8, 4), y=["CRBank", "CRBankIn", "CRInv"])
# labels = Data.YearMonth.to_list()
# tickvalues = Data.index


# plt.xticks(ticks=tickvalues[::-2], labels=labels[::-2], rotation="vertical")
# plt.ylabel("The Cumulative Return")
# plt.xlabel("Year-Month")
# plt.legend(
#     [
#         "The Banks' Business Group",
#         "Groups that consist of one bank",
#         "Groups that consist of one Investment firm",
#     ]
# )
# plt.title("The Cumulative return of portfolios  ")
# pathS = r"G:\Dropbox\Dropbox\Connected Stocks\Final Report"
# plt.savefig(pathS + "\\Effective1.eps", bbox_inches="tight")
# plt.savefig(pathS + "\\Effective1.png", bbox_inches="tight")


# Data.plot(use_index=True, figsize=(8, 4), y=["CRMost", "CRLess"])
# labels = Data.YearMonth.to_list()
# tickvalues = Data.index


# plt.xticks(ticks=tickvalues[::-2], labels=labels[::-2], rotation="vertical")
# plt.ylabel("The Cumulative Return")
# plt.xlabel("Year-Month")
# plt.legend(
#     ["The Most effective Business Groups", "The Leasr effective Business Groups"]
# )
# plt.title("The Cumulative return of portfolios  ")
# pathS = r"G:\Dropbox\Dropbox\Connected Stocks\Final Report"
# plt.savefig(pathS + "\\Effective.eps", bbox_inches="tight")
# plt.savefig(pathS + "\\Effective.png", bbox_inches="tight")

# %%
