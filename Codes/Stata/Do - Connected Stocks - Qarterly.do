cls
clear
import delimited "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\QarterlyNormalzedFCAP5.1.csv", encoding(UTF-8) 


cd "G:\Dropbox\Dropbox\Connected Stocks\Final Report"

label define sgroup 0 "No" 1 "Yes"


label values sgroup sgroup





label variable monthlyρ_2 " $ \rho_t $ "
label variable monthlyρ_4 " $ \rho_t $ "
label variable monthlyρ_5 " $ \rho_t $ "



label variable quarterlysamesize "Samesize"

label variable quarterlysize1 "Size1"
label variable quarterlysize2 "Size2"

rename quarterlyfca QFCA

rename quarterlyfcapf QFCAPf
rename quarterlyfcap NQFCAP

drop if QFCAP >1

rename v87 NQFCA



generate Qsize1size2 =  quarterlysize1 * quarterlysize2
label variable Qsize1size2 "$ Size1 \times Size2 $"


generate NQFCA2 = NQFCA * NQFCA


label variable NQFCA "$ \text{FCA*} $"
label variable NQFCAP "$ \text{FCAP*} $"


label variable NQFCA2 "$ { \text{FCA}^ * } ^ 2$"

generate lnQFCA = ln(QFCA)
label variable lnQFCA "$\ln(FCA)$"
 




xtset id t_month  


eststo v0: quietly xtfmb monthlyρ_5_f NQFCA , lag(4) 

eststo v1: quietly xtfmb monthlyρ_5_f NQFCA monthlyρ_5 , lag(4) 

eststo v2: quietly xtfmb monthlyρ_5_f NQFCA monthlyρ_5  sgroup quarterlysamesize , lag(4) 

eststo v3: quietly xtfmb monthlyρ_5_f NQFCA monthlyρ_5  sgroup quarterlysize1 quarterlysize2 , lag(4) 

eststo v4: quietly xtfmb monthlyρ_5_f NQFCA monthlyρ_5  sgroup quarterlysamesize Qsize1size2 , lag(4) 

eststo v5: quietly xtfmb monthlyρ_5_f NQFCA monthlyρ_5  sgroup quarterlysize1 quarterlysize2 Qsize1size2 , lag(4) 


esttab v0 v1 v2 v3 v4 v5, label nomtitle  r2  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated quarterly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (four lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) ,using Qresult2.tex ,replace



eststo v0: quietly xtfmb monthlyρ_5_f NQFCAP , lag(4) 

eststo v1: quietly xtfmb monthlyρ_5_f NQFCAP monthlyρ_5 , lag(4) 

eststo v2: quietly xtfmb monthlyρ_5_f NQFCAP monthlyρ_5  sgroup quarterlysamesize , lag(4) 

eststo v3: quietly xtfmb monthlyρ_5_f NQFCAP monthlyρ_5  sgroup quarterlysize1 quarterlysize2 , lag(4) 

eststo v4: quietly xtfmb monthlyρ_5_f NQFCAP monthlyρ_5  sgroup quarterlysamesize Qsize1size2 , lag(4) 

eststo v5: quietly xtfmb monthlyρ_5_f NQFCAP monthlyρ_5  sgroup quarterlysize1 quarterlysize2 Qsize1size2 , lag(4) 


esttab v0 v1 v2 v3 v4 v5, label nomtitle  r2  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated quarterly and include paper measure of institutional connectedness," " FCAP and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (four lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) ,using QPresult2.tex ,replace

