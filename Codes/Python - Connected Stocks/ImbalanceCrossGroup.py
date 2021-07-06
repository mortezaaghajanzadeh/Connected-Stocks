#%%
import pandas as pd
import numpy as np
import re
import seaborn as sns
from scipy import stats

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
n1 = path + "MonthlyNormalzedFCAP7.2" + ".csv"
df = pd.read_csv(n1)
# %%
tempt = df[df.sBgroup == 1].groupby("id").last()
tempt["Monthlyρ_5_f"] = df[df.sBgroup == 1].groupby("id").Monthlyρ_5_f.mean()

te = (
    df[df.sBgroup == 1]
    .groupby(["uo_x", "lowImbalanceStd"])
    .Monthlyρ_5_f.mean()
    .to_frame()
    .reset_index()
)

sns.histplot(data=tempt, x="Monthlyρ_5_f", hue="lowImbalanceStd")
#%%
tempt = tempt[~tempt.Monthlyρ_5_f.isnull()]
stats.ttest_ind(
    tempt[tempt.lowImbalanceStd == 1].Monthlyρ_5_f,
    tempt[tempt.lowImbalanceStd == 0].Monthlyρ_5_f,
)

# %%
tempt[tempt.lowImbalanceStd == 1].Monthlyρ_5_f.mean(), tempt[
    tempt.lowImbalanceStd == 0
].Monthlyρ_5_f.mean()
# %%
te[te.lowImbalanceStd == 1].Monthlyρ_5_f.mean(), te[
    te.lowImbalanceStd == 0
].Monthlyρ_5_f.mean()
# %%
