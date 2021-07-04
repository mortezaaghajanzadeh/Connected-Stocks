#%%
import pandas as pd
import re
import numpy as np
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
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
n = path + "Holder_Residual" + ".parquet"
df = pd.read_parquet(n)

#%%
last = df.groupby(['symbol','year']
                  ).last().reset_index()
# %%
gg = last[last.uo != 'None'].groupby(
    ['year','uo']
    )

def industyNumber(g):
    return len(g.group_name.unique())


gg.apply(industyNumber
         ).to_frame().reset_index().groupby(
             "year")[0].describe()
#%%
gg.size().to_frame().reset_index().groupby(
    "year")[0].describe()
#%%
gg = df.drop_duplicates(subset = [
    'symbol','date'
    ]).groupby('uo')
def inYearCal(sg):
    result = {}
    symbolList = sg.symbol.unique()
    for id,symbol in enumerate(symbolList):
        if id + 1 == len(symbolList): continue
        t1 = sg[
                sg['symbol'] == symbol
                ]
        tList = symbolList[id+1:]
        t = {}
        for i in tList:
            t2 = sg[
                sg['symbol'] == i
                ]
            a = t1.merge(
                    t2,on=['date']
                    )[['5-Residual_x',
                    '5-Residual_y'
                            ]].corr().iloc[0,1]
            t.update({i:a})
        result.update({symbol : t})
        
    return pd.DataFrame.from_dict(result)
def uoCal(g):
    print(g.name)
    sgg = g.groupby('year')
    return sgg.apply(inYearCal)
t = gg.apply(uoCal)
#%%
t.reset_index()
# %%
