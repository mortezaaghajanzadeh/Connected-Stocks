#%%
import pandas as pd
path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
df = pd.read_parquet(path + "MonthlyNormalzedFCAP9.3.parquet")
#%%
df[df.jalaliDate>13980000]





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

    df = df.rename(
        columns={
            "4_Residual": "4-Residual",
            "5_Residual": "5-Residual",
            "6_Residual": "6-Residual",
            "2_Residual": "2-Residual",
            "5Lag_Residual": "5Lag-Residual",
            "Delta_TurnOver": "Delta_Trunover",
            "Month_of_year": "month_of_year",
        }
    )
    return df


df = prepare()
# %%
df[df.jalaliDate>13980000].isnull().sum()

# %%
df[df.jalaliDate >13980200].groupby(["year_of_year", "month_of_year"]).size()

