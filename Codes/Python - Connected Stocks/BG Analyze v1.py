#%%
import pandas as pd
import re
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
#%%

def vv(row):
    X = row.split("-")
    return int(X[0] + X[1] + X[2])
def year(row):
    X = row.split("-")
    return int(X[0])

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

#%%
df = pd.read_parquet(
    path + "Stocks_Prices_1400-02-07.parquet"
    )
col = "name"
df[col] = df[col].apply(lambda x: convert_ar_characters(x))
df = df[~((df.title.str.startswith("ح")) & (df.name.str.endswith("ح")))]
df = df[~(df.name.str.endswith("پذيره"))]
df = df[
    ["jalaliDate", "date", "name", "group_name", "close_price", "volume", "quantity"]
]
df['year'] = df.jalaliDate.apply(year)
df['jalaliDate'] = df.jalaliDate.apply(vv)
cols = ["close_price", "volume", "quantity"]
for col in cols:
    df[col] = df[col].astype(float)
symbols = [
    "سپرده",
    "هما",
    "وهنر-پذيره",
    "نکالا",
    "تکالا",
    "اکالا",
    "توسعه گردشگری ",
    "وآفر",
    "ودانا",
    "نشار",
    "نبورس",
    "چبسپا",
    "بدکو",
    "چکارم",
    "تراک",
    "کباده",
    "فبستم",
    "تولیددارو",
    "قیستو",
    "خلیبل",
    "پشاهن",
    "قاروم",
    "هوایی سامان",
    "کورز",
    "شلیا",
    "دتهران",
    "نگین",
    "کایتا",
    "غیوان",
    "تفیرو",
    "سپرمی",
    "بتک",
]
df = df.drop(df[df["name"].isin(symbols)].index)
df = df.drop(df[df.group_name == "صندوق سرمایه گذاری قابل معامله"].index)
df = df.drop(df[df.group_name == "فعاليتهاي كمكي به نهادهاي مالي واسط"].index)
df = df.drop(df[(df.name == "اتکای") & (df.close_price == 1000)].index)
df = df.drop_duplicates()
df = (
    df.drop(df.loc[(df["volume"] == 0)].index)
    .sort_values(by=["name", "jalaliDate"])
    .drop(columns=["quantity"])
)
#%%
pathBG = path + "\Control Right - Cash Flow Right\\"
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


# %%
fkey = zip(list(BG.symbol), list(BG.year))
mapingdict = dict(zip(fkey, BG["BGId"]))
df["BGId"] = df.set_index(["name", "year"]).index.map(mapingdict)
fkey = zip(list(BG.symbol), list(BG.year))
mapingdict = dict(zip(fkey, BG["position"]))
df["position"] = df.set_index(["name", "year"]).index.map(mapingdict)
fkey = zip(list(BG.symbol), list(BG.year))
mapingdict = dict(zip(fkey, BG["uo"]))
df["uo"] = df.set_index(["name", "year"]).index.map(mapingdict)

# %%
df = df[(
    df.year>= BG.year.min()
)&
   (
       df.year<= BG.year.max()
   )]
# %%
last = df.groupby(['name','year']
                  ).last().reset_index()
# %%
gg = last.groupby(
    ['year','uo']
    )

def industyNumber(g):
    return len(g.group_name.unique())
a = gg.apply(industyNumber
         ).to_frame().reset_index()
a.groupby('year')[0].describe()
# %%
