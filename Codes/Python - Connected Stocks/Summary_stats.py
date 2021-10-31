#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re as ree
import numpy as np

path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
pathResult = r"D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report\Output\\"
#%%
n = path + "Holder_Residual_1400_06_28" + ".parquet"
df = pd.read_parquet(n)
df = df[df.jalaliDate < 14000000]
df = df[df.jalaliDate > 13930000]
# %%

gg = (
    df[["BGId", "id", "year_of_year", "Holder_id"]]
    .drop_duplicates()
    .groupby("year_of_year")
)
g = gg.get_group(2019)


def summary(g):
    rdf = g.iloc[0, :1].to_frame().T
    rdf["No. of Firms"] = int(len(set(g.id)))
    rdf["No. of Holders"] = int(len(set(g.Holder_id)))
    rdf = rdf.drop(columns=["BGId"])
    g = g.drop_duplicates(subset=["BGId", "id", "year_of_year"])
    rdf["No. of Groups"] = int(len(set(g.dropna().BGId)))
    rdf["No. of Firms not in Groups"] = int(len(set(g[g.BGId.isnull()].id)))
    rdf["No. of Firms in Groups"] = int(len(set(g[~g.BGId.isnull()].id)))
    rdf["Avg. Number of Members"] = int(round(g.groupby("BGId").size().mean(), 0))
    rdf["Max. Number of Members"] = int(g.groupby("BGId").size().max())
    rdf["Med. of  Number of Members"] = int(round(g.groupby("BGId").size().median(), 0))
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


# %%
tempt = a1.append(a2).drop_duplicates()
tempt = tempt.T.rename(columns={"year_of_year": "Year"})

tempt = tempt.drop(
    columns=["Max. Number of Members", "Max. Number of Owners", "Max. Block. Ownership"]
).rename(
    columns={
        "No. of Holders": "No. of Blockholders",
        "Avg. Number of Members": "Mean Number of Members",
        "Av. Holder Percent": "Mean Of each Blockholder’s ownership",
        "Av. Number of Owners": "Mean Number of Blockholders",
        "Av. Block. Ownership": "Mean Block. Ownership",
    }
)
tempt = tempt.set_index("Year").T
for i in [
    "No. of Firms",
    "No. of Blockholders",
    "No. of Groups",
    "No. of Firms not in Groups",
    "No. of Firms in Groups",
    "Mean Number of Blockholders",
    "Med. Number of Owners",
    "Mean Number of Members",
]:
    tempt.loc[tempt.index == i] = tempt.loc[tempt.index == i].astype(int)
tempt 


#%%

tempt.to_latex(pathResult + "summaryOfOwnership.tex")
tempt
# %%
