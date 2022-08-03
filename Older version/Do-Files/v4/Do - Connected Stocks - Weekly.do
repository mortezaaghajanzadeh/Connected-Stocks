clear
cls
import delimited "C:\Project\Connected Stocks\WeeklyNormalzedFCAP4.1.csv", encoding(UTF-8) 


cd "C:\Project\Connected Stocks\Final Report"

label define sgroup 0 "No" 1 "Yes"


label values sgroup sgroup

label variable weeklysize1 "WSize1"
label variable weeklysize2 "WSize2"
label variable weeklyρ_4_f "WForwardCorr"
label variable weeklyρ_2 "WCorr2"
label variable weeklyρ_4 "WCorr4"
label variable weeklyρ_5 "WCorr5"
label variable weeklysamesize "WSamesize"



rename weeklyfcap NWFCAP

rename v38 NWFCA


rename weeklyfca WFCA

rename weeklyfcap WFCAP

generate wsize1size2 =  weeklysize1 * weeklysize2

generate NWFCA2 = NWFCA * NWFCA
label variable NWFCA2 "$\text{WeeklyFCA}*^2$"


//hist FCA if FCA<=1 ,color(maroon) bin(10) percent
//hist fcap,color(maroon) bin(10) percent

//histogram weeklyρ_4_f,color(maroon) bin(10) percent

sum id t_week

summ NWFCA NWFCAP



binscatter weeklyρ_2_f NWFCA , ytitle("Future Weekly Correlation of 2Factor Daily Residuals") nquantiles(20) by (sgroup) legend(pos(2) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(T S) rd(-1  1)
graph export wcorr2.eps,replace
graph export wcorr2.png,replace


binscatter weeklyρ_4_f NWFCA ,  ytitle("Future Weekly Correlation of 4Factor Daily Residuals") nquantiles(20) by (sgroup) legend(pos(3) ring(0) col(1)label(1 "Separate Group") label(2 "Same Group") ) msymbol(T S) rd(-1  1)

graph export wcorr4.eps,replace
graph export wcorr4.png,replace



binscatter weeklyρ_5_f NWFCA , ytitle("Future Weekly Correlation of 5Factor Daily Residuals") nquantiles(20) by (sgroup) legend(pos(1) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(T S) rd(-1  1)
graph export wcorr5.eps,replace
graph export wcorr5.png,replace


)




eststo v00: quietly reg weeklyρ_4_f NWFCA , cluster(id)

eststo v0: quietly reg weeklyρ_4_f NWFCA NWFCA2 , cluster(id)

eststo v1: quietly reg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4 , cluster(id)

eststo v2: quietly reg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4  sgroup weeklysamesize , cluster(id)

eststo v3: quietly reg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4  sgroup weeklysize1 weeklysize2 , cluster(id)

eststo v4: quietly reg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4  sgroup weeklysamesize wsize1size2 , cluster(id)

eststo v5: quietly reg weeklyρ_4_f NWFCA  NWFCA2 weeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 , cluster(id)



esttab v00 v0 v1 v2 v3 v4 v5, drop(_cons) nomtitle label ,using wresult1.tex ,replace


xtset id t_week  


eststo v00: quietly asreg weeklyρ_4_f NWFCA , fmb

eststo v0: quietly asreg weeklyρ_4_f NWFCA NWFCA2 , fmb

eststo v1: quietly asreg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4 , fmb

eststo v2: quietly asreg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4  sgroup weeklysamesize , fmb

eststo v3: quietly asreg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4  sgroup weeklysize1 weeklysize2 , fmb

eststo v4: quietly asreg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4  sgroup weeklysamesize wsize1size2 , fmb

eststo v5: quietly asreg weeklyρ_4_f NWFCA NWFCA2 weeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 , fmb


esttab v00 v0 v1 v2 v3 v4 v5,drop(_cons) label nomtitle ,using wresult2.tex ,replace



///Part II:

eststo v00: quietly reg weeklyρ_2_f NWFCA , cluster(id)

eststo v0: quietly reg weeklyρ_2_f NWFCA NWFCA2 , cluster(id)

eststo v1: quietly reg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2 , cluster(id)

eststo v2: quietly reg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2  sgroup weeklysamesize , cluster(id)

eststo v3: quietly reg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2  sgroup weeklysize1 weeklysize2 , cluster(id)

eststo v4: quietly reg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2  sgroup weeklysamesize wsize1size2 , cluster(id)

eststo v5: quietly reg weeklyρ_2_f NWFCA  NWFCA2 weeklyρ_2  sgroup weeklysize1 weeklysize2 wsize1size2 , cluster(id)



esttab v00 v0 v1 v2 v3 v4 v5, drop(_cons) nomtitle label ,using w2result1.tex ,replace



eststo v00: quietly asreg weeklyρ_2_f NWFCA , fmb

eststo v0: quietly asreg weeklyρ_2_f NWFCA NWFCA2 , fmb

eststo v1: quietly asreg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2 , fmb

eststo v2: quietly asreg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2  sgroup weeklysamesize , fmb

eststo v3: quietly asreg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2  sgroup weeklysize1 weeklysize2 , fmb

eststo v4: quietly asreg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2  sgroup weeklysamesize wsize1size2 , fmb

eststo v5: quietly asreg weeklyρ_2_f NWFCA NWFCA2 weeklyρ_2  sgroup weeklysize1 weeklysize2 wsize1size2 , fmb


esttab v00 v0 v1 v2 v3 v4 v5,drop(_cons) label nomtitle ,using w2result2.tex ,replace



///Part III:

eststo v00: quietly reg weeklyρ_5_f NWFCA , cluster(id)

eststo v0: quietly reg weeklyρ_5_f NWFCA NWFCA2 , cluster(id)

eststo v1: quietly reg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5 , cluster(id)

eststo v2: quietly reg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5  sgroup weeklysamesize , cluster(id)

eststo v3: quietly reg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5  sgroup weeklysize1 weeklysize2 , cluster(id)

eststo v4: quietly reg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5  sgroup weeklysamesize wsize1size2 , cluster(id)

eststo v5: quietly reg weeklyρ_5_f NWFCA  NWFCA2 weeklyρ_5  sgroup weeklysize1 weeklysize2 wsize1size2 , cluster(id)



esttab v00 v0 v1 v2 v3 v4 v5, drop(_cons) nomtitle label ,using w5result1.tex ,replace



eststo v00: quietly asreg weeklyρ_5_f NWFCA , fmb

eststo v0: quietly asreg weeklyρ_5_f NWFCA NWFCA2 , fmb

eststo v1: quietly asreg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5 , fmb

eststo v2: quietly asreg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5  sgroup weeklysamesize , fmb

eststo v3: quietly asreg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5  sgroup weeklysize1 weeklysize2 , fmb

eststo v4: quietly asreg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5  sgroup weeklysamesize wsize1size2 , fmb

eststo v5: quietly asreg weeklyρ_5_f NWFCA NWFCA2 weeklyρ_5  sgroup weeklysize1 weeklysize2 wsize1size2 , fmb


esttab v00 v0 v1 v2 v3 v4 v5,drop(_cons) label nomtitle ,using w5result2.tex ,replace


///Part IV:




generate lweeklyρ_4_f = log(1+weeklyρ_4_f) - log(1-weeklyρ_4_f)
generate  lweeklyρ_4 = log(1+weeklyρ_4) -log(1-weeklyρ_4)


bootstrap, reps(1000) seed(1): eststo OLS1 : reg lweeklyρ_4_f NWFCA lweeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 

bootstrap, reps(1000) seed(1):eststo Tobit1 : tobit lweeklyρ_4_f NWFCA lweeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 

bootstrap, reps(1000) seed(1): eststo ML : qreg lweeklyρ_4_f NWFCA lweeklyρ_4  sgroup weeklysize1 weeklysize2 wsize1size2 


esttab OLS1 Tobit1 ML ,drop(_cons) label nomtitle ,using WOresult.tex ,replace