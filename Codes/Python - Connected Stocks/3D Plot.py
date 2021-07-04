#%%
import pandas as pd
import matplotlib.pyplot as plt
import re as ree
import numpy as np

path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
# %%

n2 = path + "MonthlyNormalzedFCAP6.1" + ".csv"
df = pd.read_csv(n2)
print("n2 Done")

# %%
df = df[["MonthlyFCA*", "t_Month", "Monthlyρ_5_f"]]
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.bar(
    df["MonthlyFCA*"], df.t_Month, df["Monthlyρ_5_f"], zdir="y", color="c", alpha=0.8
)
# %%
