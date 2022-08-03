clear
cls
import delimited "C:\Project\Connected Stocks\WeeklyNormalzedFCAP4.1.csv", encoding(UTF-8) 


cd "C:\Project\Connected Stocks\Final Report"

label define sgroup 0 "No" 1 "Yes"


label values sgroup sgroup

label variable weeklysize1 "WSize1"
label variable weeklysize2 "WSize2"
label variable weeklyρ_4_f "WForwardCorr"
label variable weeklyρ_4 "WCorr"
label variable weeklysamesize "WSamesize"


rename fcap NFCAP
rename weeklyfcap NWFCAP
rename monthlyfcap NMFCAP

rename v60 NFCA
rename v61 NWFCA
rename v62 NMFCA

rename weeklyfca WFCA

rename fca FCA

generate wsize1size2 =  weeklysize1 * weeklysize2


//hist FCA if FCA<=1 ,color(maroon) bin(10) percent
//hist fcap,color(maroon) bin(10) percent

//histogram weeklyρ_4_f,color(maroon) bin(10) percent

//sum id t_week




binscatter weeklyρ_4_f NWFCA , ytitle("Future Weekly Correlation of 4Factor Daily Residuals") nquantiles(100) by (sgroup) legend(pos(1) ring(0) col(1) label(1 "Same Group") label(2 "Separate Group") ) msymbol(T S) 

graph export wcorr.eps,replace
graph export wcorr.png,replace




eststo v0: quietly reg weeklyρ_4_f NWFCA , cluster(id)

eststo v1: quietly reg weeklyρ_4_f NWFCA weeklyρ_4 , cluster(id)

eststo v2: quietly reg weeklyρ_4_f NWFCA weeklyρ_4  sgroup weeklysamesize , cluster(id)

eststo v3: quietly reg weeklyρ_4_f NWFCA weeklyρ_4  sgroup weeklysize1 weeklysize2 , cluster(id)

eststo v4: quietly reg weeklyρ_4_f NWFCA weeklyρ_4  sgroup weeklysamesize wsize1size2 , cluster(id)

eststo v5: quietly reg weeklyρ_4_f NWFCA weeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 , cluster(id)



esttab v0 v1 v2 v3 v4 v5, drop(_cons) nomtitle label ,using wresult1.tex ,replace


xtset id t_week  


eststo v0: quietly asreg weeklyρ_4_f NWFCA , fmb

eststo v1: quietly asreg weeklyρ_4_f NWFCA weeklyρ_4 , fmb

eststo v2: quietly asreg weeklyρ_4_f NWFCA weeklyρ_4  sgroup weeklysamesize , fmb

eststo v3: quietly asreg weeklyρ_4_f NWFCA weeklyρ_4  sgroup weeklysize1 weeklysize2 , fmb

eststo v4: quietly asreg weeklyρ_4_f NWFCA weeklyρ_4  sgroup weeklysamesize wsize1size2 , fmb

eststo v5: quietly asreg weeklyρ_4_f NWFCA weeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 , fmb


esttab v0 v1 v2 v3 v4 v5,drop(_cons) label nomtitle ,using wresult2.tex ,replace



/// 
eststo v0: quietly asreg monthlyρ_4_f NWFCA , fmb

eststo v1: quietly asreg monthlyρ_4_f NWFCA weeklyρ_4 , fmb

eststo v2: quietly asreg monthlyρ_4_f NWFCA weeklyρ_4  sgroup weeklysamesize , fmb

eststo v3: quietly asreg monthlyρ_4_f NWFCA weeklyρ_4  sgroup weeklysize1 weeklysize2 , fmb

eststo v4: quietly asreg monthlyρ_4_f NWFCA weeklyρ_4  sgroup weeklysamesize wsize1size2 , fmb

eststo v5: quietly asreg monthlyρ_4_f NWFCA weeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 , fmb


esttab v0 v1 v2 v3 v4 v5,drop(_cons) label nomtitle ,using mwfamaresult.tex ,replace


///Part III:




generate lweeklyρ_4_f = log(1+weeklyρ_4_f) - log(1-weeklyρ_4_f)
generate  lweeklyρ_4 = log(1+weeklyρ_4) -log(1-weeklyρ_4)


bootstrap, reps(1000) seed(1): eststo OLS1 : reg lweeklyρ_4_f NWFCA lweeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 

bootstrap, reps(1000) seed(1):eststo Tobit1 : tobit lweeklyρ_4_f NWFCA lweeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 

bootstrap, reps(1000) seed(1): eststo ML : qreg lweeklyρ_4_f NWFCA lweeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 


esttab OLS1 Tobit1 ML ,drop(_cons) label nomtitle ,using WOresult.tex ,replace