# %%
import pickle
import psutil
from threading import Thread
from ConnectedOwnershipFunctions import *
# %%
def vv4(row):
    row = str(row)
    X = [1, 1, 1]
    X[0] = row[0:4]
    X[1] = row[4:6]
    X[2] = row[6:8]
    return X[0] + "-" + X[1] + "-" + X[2]


def vv(row):
    X = row.split("-")
    return X[0] + X[1] + X[2]


def DriveYearMonthDay(d):
    d["jalaliDate"] = d["jalaliDate"].astype(str)
    d["Year"] = d["jalaliDate"].str[0:4]
    d["Month"] = d["jalaliDate"].str[4:6]
    d["Day"] = d["jalaliDate"].str[6:8]
    d["jalaliDate"] = d["jalaliDate"].astype(int)
    return d


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


def vv2(row):
    X = row.split("/")
    return X[0] + X[1] + X[2]


def vv3(row):
    X = row.split("/")
    if len(X[0]) < 4:
        X[0] = "13" + X[0]
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[2]) < 2:
        X[2] = "0" + X[2]
    return X[0] + X[1] + X[2]


def vv5(row):
    X = row.split("/")
    return X[0]


# %%
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
# path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"

df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")

df.loc[df.week_of_year % 2 == 1, "week_of_year"] = (
    df.loc[df.week_of_year % 2 == 1]["week_of_year"] - 1
)

df = df[df.jalaliDate < 14000000]
try:
    df = df.drop(columns=["Delta_Trunover"])
except:
    1 + 2
df = df.rename(columns = 
    {
        '4_Residual' : '4-Residual',
        '5_Residual' : '5-Residual',
        '6_Residual' : '6-Residual',
        '2_Residual' : '2-Residual',
        '5Lag_Residual' : '5Lag-Residual',
        'Delta_TurnOver':'Delta_Trunover'
    }
)
df.head()


# %%
df[df.symbol == "شستا"].id.iloc[0], df[df.symbol == "خودرو"].id.iloc[0]


# %%
gdata = df.groupby(["id"])
g = gdata.get_group(158)
S_g = gdata.get_group(148)


a1 = FCAPf_allPair(S_g, g)
a2 = FCAPf(S_g, g)
#%%


# %%
