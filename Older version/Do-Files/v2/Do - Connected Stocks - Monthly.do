cls
clear
import delimited "C:\Project\Connected Stocks\MonthlyNormalzedFCAP3.1.csv", encoding(UTF-8) 

cd "C:\Project\Connected Stocks\Final Report"

label define sgroup 0 "No" 1 "Yes"


label values sgroup sgroup

label variable weeklysize1 "WSize1"
label variable weeklysize2 "WSize2"
label variable weeklyρ_4_f "WForwardCorr"
label variable weeklyρ_4 "WCorr"
label variable weeklysamesize "WSamesize"

label variable monthlysize1 "MSize1"
label variable monthlysize2 "MSize2"
label variable monthlyρ_4_f "MForwardCorr"
label variable monthlyρ_4 "MCorr"
label variable monthlysamesize "MSamesize"




rename fcap NFCAP
rename monthlyfcap NMFCAP

rename v60 NFCA
rename v61 NWFCA
rename v62 NMFCA

rename fca FCA

generate msize1size2 =  monthlysize1 * monthlysize2

binscatter monthlyρ_4_f NMFCA , ytitle("Future Monthly Correlation of 4Factor Daily Residuals") nquantiles(100) by (sgroup) legend(pos(1) ring(0) col(1) label(1 "Same Group") label(2 "Separate Group") ) msymbol(T S) 


graph export mcorr.eps,replace
graph export mcorr.png,replace


eststo v0: quietly reg monthlyρ_4_f NMFCA , cluster(id)

eststo v1: quietly reg monthlyρ_4_f NMFCA monthlyρ_4 , cluster(id)

eststo v2: quietly reg monthlyρ_4_f NMFCA monthlyρ_4  sgroup monthlysamesize , cluster(id)

eststo v3: quietly reg monthlyρ_4_f NMFCA monthlyρ_4  sgroup monthlysize1 monthlysize2 , cluster(id)

eststo v4: quietly reg monthlyρ_4_f NMFCA monthlyρ_4  sgroup monthlysamesize msize1size2 , cluster(id)

eststo v5: quietly reg monthlyρ_4_f NMFCA monthlyρ_4  sgroup monthlysize1 monthlysize2 msize1size2 , cluster(id)




esttab v0 v1 v2 v3 v4 v5, drop(_cons) nomtitle label ,using mresult1.tex ,replace


xtset id t_month  


eststo v0: quietly asreg monthlyρ_4_f NMFCA , fmb

eststo v1: quietly asreg monthlyρ_4_f NMFCA monthlyρ_4 , fmb

eststo v2: quietly asreg monthlyρ_4_f NMFCA monthlyρ_4  sgroup monthlysamesize , fmb

eststo v3: quietly asreg monthlyρ_4_f NMFCA monthlyρ_4  sgroup monthlysize1 monthlysize2 , fmb

eststo v4: quietly asreg monthlyρ_4_f NMFCA monthlyρ_4  sgroup monthlysamesize msize1size2 , fmb

eststo v5: quietly asreg monthlyρ_4_f NMFCA monthlyρ_4  sgroup monthlysize1 monthlysize2 msize1size2 , fmb


esttab v0 v1 v2 v3 v4 v5,drop(_cons) label nomtitle  ,using mresult2.tex ,replace

///Part III:




generate lmonthlyρ_4_f = log(1+monthlyρ_4_f) - log(1-monthlyρ_4_f)
generate  lmonthlyρ_4 = log(1+monthlyρ_4) -log(1-monthlyρ_4)


bootstrap, reps(1000) seed(1): eststo OLS1 : reg lmonthlyρ_4_f NMFCA lmonthlyρ_4  sgroup monthlysize1 monthlysize2 msize1size2  

bootstrap, reps(1000) seed(1):eststo Tobit1 : tobit lmonthlyρ_4_f NMFCA lmonthlyρ_4  sgroup monthlysize1 monthlysize2 msize1size2 

bootstrap, reps(1000) seed(1): eststo ML : qreg lmonthlyρ_4_f NMFCA lmonthlyρ_4 sgroup monthlysize1 monthlysize2 msize1size2 

esttab OLS1 Tobit1 ML ,drop(_cons) label nomtitle ,using MOresult.tex ,replace