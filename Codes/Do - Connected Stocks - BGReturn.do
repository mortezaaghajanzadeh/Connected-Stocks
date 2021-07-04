cls
clear
import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\BGReturn.csv", encoding(UTF-8) 


cd "D:\Dropbox\Connected Stocks\Final Report"

xtset id jalalidate  
 
rename eret ereturn


label variable ereturn " $ R $ "

label variable emarketret " $ R_M $ "

label variable egreturn " $ R_{Industry} $ "
label variable egreturn_firmout " $ R_{Industry} $ "


label variable euopr " $ R_{Business group} $ "

label variable winner_loser " $ UMD $ "

label variable hml " $ HML $ "
label variable smb " $ SMB $ "

summ euopr egreturn_firmout



eststo v0 : quietly asreg ereturn emarketret  ,fmb newey(7)
eststo v1 : quietly asreg ereturn egreturn_firmout emarketret ,fmb newey(7)
eststo v2 : quietly asreg ereturn egreturn_firmout euopr emarketret,fmb newey(7)
eststo v3 : quietly asreg ereturn egreturn_firmout emarketret smb winner_loser hml,fmb newey(7)
eststo v4 : quietly asreg ereturn egreturn_firmout euopr emarketret smb winner_loser hml,fmb newey(7)
esttab v0 v1 v3 v2  v4 , n r2 nomtitle label order( emarketret egreturn_firmout euopr smb winner_loser hml ) compress



 mgroups(" $ \text{Return}_i - r_f = R_i$ "   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using BGReturn.tex ,replace


