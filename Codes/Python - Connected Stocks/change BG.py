#%%
import pandas as pd
import seaborn as sns

path = r"E:\RA_Aghajanzadeh\Data\Connected_Stocks\\"
df = pd.read_parquet(path + "Holder_Residual_1400_06_28.parquet")
df = df[df.jalaliDate < 13990000]
df = df[df.jalaliDate > 13930000]
# %%
df["Grouped"] = 1
df.loc[df.uo.isnull(), "Grouped"] = 0
# %%
df["yearMonth"] = df.year_of_year + df.Month_of_year
t = (
    df.groupby(["Grouped", "yearMonth"])[["Residual_Bench", "5_Residual"]]
    .mean()
    .reset_index()
)
sns.lineplot(data=t, x="yearMonth", y="5_Residual", hue="Grouped")

# %%
df[["Residual_Bench", "5_Residual"]].describe()

#%%
df = pd.read_parquet(path + "MonthlyNormalzedFCAP9.2.parquet")
# %%
t = df[df.becomeSameBG == 1]
sns.lineplot(data=t[
    abs(t.SBGperiod)<19], x="SBGperiod", y="Monthlyρ_5")


# %%
