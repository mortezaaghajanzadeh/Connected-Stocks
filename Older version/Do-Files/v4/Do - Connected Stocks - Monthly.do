cls
clear
import delimited "C:\Project\Connected Stocks\MonthlyNormalzedFCAP4.1.csv", encoding(UTF-8) 

cd "C:\Project\Connected Stocks\Final Report"

label define sgroup 0 "No" 1 "Yes"


label values sgroup sgroup



label variable monthlysize1 "MSize1"
label variable monthlysize2 "MSize2"
label variable monthlyρ_4_f "MForwardCorr"
label variable monthlyρ_2 "MCorr2"
label variable monthlyρ_4 "MCorr4"
label variable monthlyρ_5 "MCorr5"
label variable monthlysamesize "MSamesize"





rename monthlyfcap NMFCAP


rename v38 NMFCA



generate msize1size2 =  monthlysize1 * monthlysize2
generate NMFCA2 = NMFCA * NMFCA
label variable NMFCA2 "$\text{NMFCA}^2$"



binscatter monthlyρ_2_f NMFCA, ytitle("Future Monthly Correlation of 2Factor Daily Residuals") nquantiles(20) by (sgroup) legend(pos(2) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(T S) rd(-1  1)
graph export mcorr2.eps,replace
graph export mcorr2.png,replace


binscatter monthlyρ_4_f NMFCA,  ytitle("Future Monthly Correlation of 4Factor Daily Residuals") nquantiles(20) by (sgroup) legend(pos(3) ring(0) col(1)label(1 "Separate Group") label(2 "Same Group") ) msymbol(T S) rd(-1  1)

graph export mcorr4.eps,replace
graph export mcorr4.png,replace



binscatter monthlyρ_5_f NMFCA, ytitle("Future Monthly Correlation of 5Factor Daily Residuals") nquantiles(20) by (sgroup) legend(pos(1) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(T S) rd(-1  1)
graph export mcorr5.eps,replace
graph export mcorr5.png,replace




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