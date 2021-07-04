#%%
from numpy.core.numeric import True_
import pandas as pd

path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\\"
n1 = path + "Holder_Residual" + ".parquet"
df = pd.read_parquet(n1)
# %%
BGId = df[['uo','BGId']].drop_duplicates().reset_index(drop = True)
# %%
idss = [
    29,
    31,
    5,
    2,
    3,
    9,
    14,
    43,
    38,
    8,
    0,
    7,
    30,
    12,
    6,
    24,
    28,
    40,
    36,
    23
]



#%%
beta = pd.read_csv(path + "Betas.csv")
# %%

bankingUo = [
    "وبصادر", 
    "بانک ملی ایران",
    "وبملت",
    "دی",
    "وتجارت",
    "بانک مسکن",
    "بانک صنعت ومعدن",
    "بانک سپه"
    ]
bankingSymbol=[
    'وملت',
    'وسینا',
    'وپاسار',
    'وبملت',
    'وبصادر',
    'وتجارت',
    'وپست',
    'ومسکن',
    'وحکمت',
    'وزمین'
    ]
investmentSymbol =[
    'واعتبار',
    'وسپه',
    'ونیکی',
    'والبر',
    'وپترو',
    'وتوشه',
    'وغدیر',
    'ورنا',
    'وبانک',
    'ونفت',
    'وبیمه',
    'وصندوق',
    'وصنعت',
    'ومعادن',
    'وآردل',
    'وتوکا',
    'وبوعلی',
    'واتی',
    'وتوسم',
    'وامید',
    'ونیرو',
    'وساپا',
    'ودی',
    'وشمال',
    'وگستر',
    'وسکاب',
    'ولتجار',
    'وخارزم',
    'وکادو',
    'ومشان',
    'وآفر',
    'وبهمن',
    'وثوق',
    'وسنا',
    'وارس',
    'وجامی',
    'وآتوس',
    'وبرق',
    'وپسا',
    'وسبحان',
    'ومعین',
    'وپویا',
    'وایرا',
    'وآذر',
    
    ]   

#%%
path1 = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
DD = pd.read_excel(path1 + "Control Right - Cash Flow Right - 9809.xlsx")
DD[DD.symbol.str.startswith('و')].symbol.unique()
# %%
bankinGroup = list(DD[DD.symbol.isin(bankingSymbol)]['ultimate owner'].unique())
invinGroup = list(DD[DD.symbol.isin(investmentSymbol)]['ultimate owner'].unique())

# %%
beta['Bank in Group'] = 0
beta.loc[beta.uo.isin(bankinGroup),'Bank in Group'] = 1
beta['Bank is UO'] = 0
beta.loc[beta.uo.isin(bankingUo),'Bank is UO'] = 1
beta['Inv. in Group'] = 0
beta.loc[beta.uo.isin(invinGroup),'Inv. in Group'] = 1
# %%
beta.head()
# %%
beta.groupby('Bank in Group')[['0']].mean().append(
    beta.groupby('Bank is UO')[['0']].mean()
).append(
    beta.groupby('Inv. in Group')[['0']].mean()
)
# %%
from scipy import stats

stats.ttest_ind(beta.groupby('Bank in Group').get_group(0)['0'],beta.groupby('Bank in Group').get_group(1)['0'])
#%%
stats.ttest_ind(beta.groupby('Bank is UO').get_group(0)['0'],beta.groupby('Bank is UO').get_group(1)['0'])

# %%
stats.ttest_ind(beta.groupby('Inv. in Group').get_group(0)['0'],beta.groupby('Inv. in Group').get_group(1)['0'])

# %%
