cls
clear
import delimited "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\LastMonthlyNormalzedFCAP6.1.csv", encoding(UTF-8) 


cd "G:\Dropbox\Dropbox\Connected Stocks\Final Report"

label define sgroup 0 "No" 1 "Yes"



label values sgroup sgroup
label variable sgroup "SameIndustry"

label values sbgroup sgroup
label variable sbgroup "SameGroup"

label values sposition sgroup
label variable sposition "SamePosition"

gen positiondif = abs(position_x - position_y)

label variable positiondif "PositionDifference"


gen positiondif2 = positiondif * sbgroup
 label variable positiondif2 " $ \text{SameGroup} \times \text{PositionDifference} $ "

 gen sposition2 = sposition * sbgroup
  label variable sposition2 " $ \text{SameGroup} \times \text{SamePosition} $"


gen sameGRank = 0
replace sameGRank = 1 if grank_x == grank_y

label variable sameGRank "SameGRank"



label values  sametype sgroup 
label variable sametype "SameType"
 

label values holder_act sgroup 
label variable holder_act "ActiveHolder"


label variable monthlysize1 "Size1"
label variable monthlysize2 "Size2"
label variable monthlyρ_4_f "ForwardCorr"
label variable monthlyρ_2 " $ {\rho_t} $ "
label variable monthlyρ_4 " $ {\rho_t} $ "
label variable monthlyρ_5 " $ {\rho_t} $ "
label variable monthlysamesize "SameSize"



rename monthlyfca MFCA

rename monthlyfcap NMFCAP

label variable NMFCAP "$ \text{FCAP*} $"

gen NMFCAPG = sbgroup * NMFCAP

label variable NMFCAPG " $ (\text{FCAP}^*) \times {\text{SameGroup} }  $ "

gen NMFCAPA = holder_act * NMFCAP

label variable NMFCAPA " $ (\text{FCAP}^*) \times {\text{ActiveHolder} }  $ "


drop if MFCA >1

rename v95 NMFCA



generate msize1size2 =  monthlysize1 * monthlysize2
label variable msize1size2 "$ Size1 \times Size2 $"


generate NMFCA2 = NMFCA * NMFCA


label variable NMFCA "$ \text{FCA*} $"


label variable NMFCA2 "$ { \text{FCA}^ * } ^ 2$"

generate lnMFCA = ln(MFCA)
label variable lnMFCA "$\ln(FCA)$"

generate msbm1bm2 =  monthlybm1 * monthlybm2

label variable msbm1bm2 "$ BookToMarketMarket_1 \times BookToMarketMarket_2 $"
label variable monthlysamebm "SameBookToMarket"
label variable monthlybm1 "$ BookToMarketMarket_1 $"

label variable monthlybm2 "$ BookToMarketMarket_2 $"

egen median = median(NMFCA)

replace median = 1 if NMFCA > median
replace median = 0 if median != 1 

gen NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times {\text{FCA} ^*}  $ "

gen sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times {\text{SameGroup} }  $ "

gen NMFCAG = sbgroup * NMFCA
label variable NMFCAG " $ (\text{FCA}^*) \times {\text{SameGroup} }  $ "

generate Down = NMFCA * negative * sbgroup
label variable Down "$ (\text{FCA}^*) \times {\text{Down Market}} \times {\text{SameGroup} }  $ "


generate positive = 1
replace positive = 0 if negative == 1




generate Up = NMFCA * positive * sbgroup

label variable Up "$ (\text{FCA}^*) \times {\text{Up Market}} \times {\text{SameGroup} }  $ "



label variable negative "Down Market"
label variable positive "Up Market"

gen NMFCAGM = sbgroup * NMFCA * median
label variable NMFCAGM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times  (\text{FCA}^*) \times {\text{SameGroup} }  $ "




gen NMFCAA = holder_act * NMFCA

label variable NMFCAA " $ (\text{FCA}^*) \times {\text{ActiveHolder} }  $ "


gen holder_actM = holder_act * median
label variable holder_actM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times {\text{ActiveHolder} }  $ "

gen spositionM = sposition * median

label variable spositionM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times {\text{Same Position} }  $ "



/**/

generate lnMFCAP = ln(monthlyfcap)
label variable lnMFCAP "$\ln(FCAP)$"

generate lnMFCAG = lnMFCA * sbgroup
label variable lnMFCAG "$ (\ln(FCA)) \times {\text{SameGroup} }  $ "


generate lnMFCAA = lnMFCA * holder_act
label variable lnMFCAA "$ (\ln(FCA)) \times {\text{ActiveHolder} }  $ "

generate lnDown = lnMFCA * negative * sbgroup
label variable lnDown "$ (\ln(FCA)) \times {\text{Down Market} } \times {\text{SameGroup} }  $ "

generate lnUp = lnMFCA * positive * sbgroup
label variable lnUp "$ (\ln(FCA)) \times {\text{Up Market} } \times {\text{SameGroup} }  $ "


generate sDown = negative * sbgroup
label variable sDown "$ {\text{Down Market} } \times {\text{SameGroup} }  $ "

generate sUp = positive * sbgroup
label variable sUp "$ {\text{Up Market} } \times {\text{SameGroup} }  $ "

gen PairType = 0
replace PairType = 1  if grank_x <5 & grank_y<5
replace PairType = 2  if grank_x >=5 & grank_y>=5

label define PairType 0 "Hybrid" 1 "Small" 2 "Big"



label values PairType PairType
label variable PairType "PairType"


xtile  Q = NMFCA, nq(4)


drop if monthlyfcapf >1
drop if fcapf >1
drop if weeklyfcapf >1

xtset id t_month  


/******/




/***/


twoway histogram MFCA ,color(navy*.5) bin(20)  || kdensity MFCA ,title("Density of FCA") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistFCA.eps,replace
graph export MHistFCA.png,replace


twoway histogram monthlyfcapf ,color(navy*.5) bin(20)  || kdensity monthlyfcapf ,title("Density of FCAP") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistFCAP.eps,replace
graph export MHistFCAP.png,replace


twoway histogram NMFCA ,color(navy*.5) bin(20)  || kdensity NMFCA ,title("Density of FCA*") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistNFCA.eps,replace
graph export MHistNFCA.png,replace


twoway histogram NMFCAP ,color(navy*.5) bin(20)  || kdensity NMFCAP ,title("Density of FCAP*") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistNFCAP.eps,replace
graph export MHistNFCAP.png,replace


twoway histogram lnMFCA ,color(navy*.5) bin(20)  || kdensity lnMFCA ,title("Density of ln(FCA)") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistlnFCA.eps,replace
graph export MHistlnFCA.png,replace

twoway histogram lnMFCAP ,color(navy*.5) bin(20)  || kdensity lnMFCAP ,title("Density of ln(FCAP)") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistlnFCAP.eps,replace
graph export MHistlnFCAP.png,replace






 

 /*
binscatter monthlyρ_2_f NMFCA,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) by (sgroup) legend(pos(4) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) note("Note: This figure graphs the correlation of daily CAPM+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCA*")title("Common Pairs")
graph export mcorr2g.eps,replace
graph export mcorr2g.png,replace
*/
/*
binscatter monthlyρ_4_f NMFCA ,ytitle("Future monthly Correlation of " " 4Factor Daily Residuals")   nquantiles(100) by (sgroup) legend(pos(3) ring(0) col(1)label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) note("This figure graphs the correlation of daily 4Factor residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCA*") title("Common Pairs")

graph export mcorr4g.eps,replace
graph export mcorr4g.png,replace
*/



binscatter monthlyρ_5_f NMFCAP, ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCAP*")title("Common Pairs")
graph export mcorr5Polk.eps,replace
graph export mcorr5Polk.png,replace



binscatter monthlyρ_5_f NMFCA, ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) by (sgroup) legend(pos(4) ring(0) col(1) label(1 "Separate Industry") label(2 "Same Industry") ) msymbol(Th S)  note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCA*")title("Common Pairs")
graph export mcorr5g.eps,replace
graph export mcorr5g.png,replace


binscatter monthlyρ_5_f NMFCA, ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) by (sbgroup) legend(pos(4) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S)  note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCA*")title("Common Pairs")
graph export mcorr5bg.eps,replace
graph export mcorr5bg.png,replace

binscatter monthlyρ_5_f NMFCA, ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("FCA*") line(qfit)title("Common Pairs")
graph export mcorr5.eps,replace
graph export mcorr5.png,replace


binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("FCA*")  title("Common Pairs") 
graph export mcorr5l.eps,replace
graph export mcorr5l.png,replace





egen median2 = median(NMFCA)
summ median2


binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in median") xtitle("FCA*")  title("Common Pairs") rd(-.0554378)
graph export mcorr5lrd.eps,replace
graph export mcorr5lrd.png,replace

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in median") xtitle("FCA*")  title("Common Pairs") rd(-.0554378) by(holder_act)  legend( ring(1) col(2) label(2 "Active Holder") label(1 "Passive Holder") ) msymbol(Th S) 

graph export mcorr5lrda.eps,replace
graph export mcorr5lrda.png,replace

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in median") xtitle("FCA*")  title("Common Pairs") rd(-.0554378) by(sbgroup)  legend( ring(1) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) 
graph export mcorr5lrdbg.eps,replace
graph export mcorr5lrdbg.png,replace



/**/
by(Q): 

sum NMFCA if Q == 4

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in fourth quarter") xtitle("FCA*")  title("Common Pairs") rd(0.7863524)
graph export Qmcorr5lrd.eps,replace
graph export Qmcorr5lrd.png,replace

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in fourth quarter") xtitle("FCA*")  title("Common Pairs") rd(0.7863524) by(holder_act)  legend( ring(1) col(2) label(2 "Active Holder") label(1 "Passive Holder") ) msymbol(Th S) 

graph export Qmcorr5lrda.eps,replace
graph export Qmcorr5lrda.png,replace

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in fourth quarter") xtitle("FCA*")  title("Common Pairs") rd(0.7863524) by(sbgroup)  legend( ring(1) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) 
graph export Qmcorr5lrdbg.eps,replace
graph export Qmcorr5lrdbg.png,replace

/**/
binscatter monthlyρ_5_f NMFCA,  ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.")xtitle("FCA*")  title("Common Pairs") by(holder_act)  legend( ring(1) col(2) label(2 "Active Holder") label(1 "Passive Holder") ) msymbol(Th S) line(qfit)

graph export mcorr5a.eps,replace
graph export mcorr5a.png,replace


binscatter monthlyρ_5_f MFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) xscale(log) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("FCA") title("Common Pairs") legend( ring(0) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S)  by(sbgroup)
graph export mcorr50bg.eps,replace
graph export mcorr50bg.png,replace



binscatter monthlyρ_5_f MFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) xscale(log) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("FCA") title("Common Pairs") 
graph export mcorr50.eps,replace
graph export mcorr50.png,replace



binscatter monthlyρ_5_f lnMFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("Ln(FCA)") title("Common Pairs")
graph export mcorr50Ln.eps,replace
graph export mcorr50Ln.png,replace


binscatter monthlyρ_5_f lnMFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("Ln(FCA)") title("Common Pairs") legend( ring(0) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S)  by(sbgroup)
graph export mcorr50LnSb.eps,replace
graph export mcorr50LnSb.png,replace








/*ln(MFCA)*/

eststo v0: quietly xtfmb monthlyρ_5_f  lnMFCA , lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f lnMFCA  monthlyρ_5 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


eststo v11: quietly xtfmb monthlyρ_5_f lnMFCA  monthlyρ_5 sbgroup, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v111: quietly xtfmb monthlyρ_5_f lnMFCA  monthlyρ_5 sbgroup lnMFCAG, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v13: quietly xtfmb monthlyρ_5_f lnMFCA  monthlyρ_5  sbgroup lnMFCAG sgroup, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v2: quietly xtfmb monthlyρ_5_f lnMFCA monthlyρ_5  sbgroup lnMFCAG  sgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


/*
eststo v3: quietly xtfmb monthlyρ_5_f lnMFCA monthlyρ_5 holder_act lnMFCAA sbgroup lnMFCAG sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f lnMFCA monthlyρ_5 holder_act lnMFCAA sbgroup lnMFCAG sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f lnMFCA monthlyρ_5 holder_act lnMFCAA sbgroup lnMFCAG sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction  "Yes" , replace

*/



esttab   v0 v1 v11 v111     v13  v2 , nomtitle label  n r2    compress mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using lnmresult2-slide.tex ,replace



esttab   v0 v1 v11 v111     v13  v2 , nomtitle label  n r2    compress mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ),using lnmresult2.tex ,replace







/*NMFCA*/

eststo v0: quietly xtfmb monthlyρ_5_f  NMFCA , lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


eststo v11: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v111: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup NMFCAG, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v13: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup NMFCAG sgroup, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v2: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

/*

eststo v3: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 holder_act NMFCAA sbgroup NMFCAG sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 holder_act NMFCAA sbgroup NMFCAG sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 holder_act NMFCAA sbgroup NMFCAG sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction  "Yes" , replace

*/



esttab   v0 v1 v11 v111   v13  v2 , nomtitle label  n r2   compress   mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-slide.tex ,replace



esttab   v0 v1 v11 v111   v13  v2 , nomtitle label  n r2   compress addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" )mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2.tex ,replace



xtset id t_month    

xtreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm i.t_month ,fe 



xtfmb monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm  , lag(5)


regress monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm 

/*Down Market */


eststo v2: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG sgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v31: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5  NMFCAG  sDown sUp sgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v32: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5  Down Up sDown sUp sgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


/*
eststo v5: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG holder_act NMFCAA sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction  "Yes" , replace



eststo v61: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG holder_act NMFCAA sDown sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction  "Yes" , replace

eststo v62: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 sbgroup  holder_act NMFCAA  Down sDown sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction  "Yes" , replace

*/

esttab  v2 v31   v32 , nomtitle label keep(NMFCA NMFCAG sDown Down Up sUp )  n r2  compress  mgroups("Future Corr. of 4F+Ind. Residuals", pattern(1)  prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Down-slide.tex ,replace

esttab  v2 v31   v32 , nomtitle label keep(NMFCA NMFCAG sDown Down)  n r2  compress  mgroups("Future Corr. of 4F+Ind. Residuals", pattern(1)  prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using mresult2Down.tex ,replace





/*NMFCAM*/

eststo v00: quietly xtfmb monthlyρ_5_f NMFCA , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v0: quietly xtfmb monthlyρ_5_f  NMFCA NMFCAM , lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


eststo v11: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 sbgroup  , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v2: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


regress monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm 

/*
eststo v3: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5  holder_act   sbgroup  sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5  holder_act   sbgroup   sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5  holder_act  sbgroup   sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
*/

esttab v00 v0 v1 v11    v2, nomtitle label  n r2 compress mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Mmresult2-slide.tex ,replace


esttab v00 v0 v1 v11     v2, nomtitle label  n r2 compress   addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" )mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Mmresult2.tex ,replace

/**/


eststo v0: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace



eststo v2: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAM NMFCAG    sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


 eststo v3: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

 eststo v4: quietly  xtfmb monthlyρ_5_f NMFCA  NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

 eststo v5: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

esttab   v0 v1 v2  v4 v5 v3   , nomtitle label  r2 n compress  keep(NMFCA NMFCAM NMFCAG NMFCAGM    )  mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using Mmresult3-slide.tex ,replace

esttab   v0 v1 v2  v4 v3   , nomtitle label  r2 n  keep(NMFCA NMFCAM NMFCAG NMFCAGM NMFCAA   ) compress addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Mmresult3.tex ,replace



/***/

 eststo v0: quietly reg monthlyρ_5_f NMFCA NMFCAM   sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if month_of_year != 2 , cluster(t)
 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace
estadd loc EndOfYear "No" , replace

 eststo v01: quietly  reg monthlyρ_5_f NMFCA NMFCAM   sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm    monthlyρ_5 if month_of_year == 2 , robust
estadd loc Controls "No" , replace 
estadd loc Interaction "No" , replace
estadd loc EndOfYear "Yes" , replace




eststo v1: quietly reg monthlyρ_5_f NMFCA NMFCAM sbgroup NMFCAG    sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2  monthlyρ_5  if month_of_year != 2  , robust
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
estadd loc EndOfYear "No" , replace

eststo v11: quietly reg monthlyρ_5_f NMFCA NMFCAM sbgroup NMFCAG   sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2  monthlyρ_5 if month_of_year == 2 , robust
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
estadd loc EndOfYear "Yes" , replace

/**/
eststo v20: quietly   xtfmb monthlyρ_5_f NMFCA NMFCAM   sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if month_of_year != 2 
 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace
estadd loc EndOfYear "No" , replace

 eststo v201: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM   sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if month_of_year == 2
estadd loc Controls "No" , replace 
estadd loc Interaction "No" , replace
estadd loc EndOfYear "Yes" , replace




eststo v21: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup NMFCAG      sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2  monthlyρ_5  if month_of_year != 2 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
estadd loc EndOfYear "No" , replace

eststo v211: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup NMFCAG     sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2  monthlyρ_5 if month_of_year == 2 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
estadd loc EndOfYear "Yes" , replace




esttab  v0 v01  v1 v11 v20 v201 v21 v211, nomtitle label  r2 s(Controls Interaction EndOfYear N r2) drop (sgroup monthlysamesize monthlysamebm monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  compress mgroups("OLS-Robust" "FM"   , pattern(1 0 0 0 1 0 0 0 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using MmresultIdent-slide.tex ,replace

esttab  v0 v01  v1 v11 v20 v201 v21 v211, nomtitle label  r2 s(Controls Interaction EndOfYear N r2) drop (sgroup monthlysamesize monthlysamebm monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  compress mgroups("OLS-Robust" "FM"   , pattern(1 0 0 0 1 0 0 0 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )   addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) ,using MmresultIdent.tex ,replace



/****/




binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("FCA*")  title("Common Pairs") by(PairType)



 eststo v0: quietly  xtfmb monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm    monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


 eststo Bv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Bv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace


 eststo Sv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Sv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace



eststo SBv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0 , lag(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo SBv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace



esttab v0 v1 Bv0 Bv1 SBv0 SBv1 Sv0 Sv1   , nomtitle label n r2  compress order(NMFCA NMFCAM sbgroup  NMFCAG holder_act NMFCAA  sgroup) keep(NMFCA NMFCAM sbgroup  NMFCAG holder_act NMFCAA  sgroup) mgroups("All Firms" "Big Firms" "Big \& Small Firms" "Small Firms"   , pattern(1 0 1 0 1 0 1 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	,using Mmresult4-slide.tex ,replace 



/*NMFCAP*/

eststo v0: quietly xtfmb monthlyρ_5_f  NMFCAP , lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCAP  monthlyρ_5 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v11: quietly xtfmb monthlyρ_5_f NMFCAP  monthlyρ_5 sbgroup, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v111: quietly xtfmb monthlyρ_5_f NMFCAP  monthlyρ_5 sbgroup NMFCAPG, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v13: quietly xtfmb monthlyρ_5_f NMFCAP  monthlyρ_5  sbgroup NMFCAPG sgroup, lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v2: quietly xtfmb monthlyρ_5_f NMFCAP monthlyρ_5  sbgroup NMFCAPG  sgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


/*
eststo v3: quietly xtfmb monthlyρ_5_f NMFCAP monthlyρ_5 holder_act NMFCAPA sbgroup NMFCAPG sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f NMFCAP monthlyρ_5 holder_act NMFCAPA sbgroup NMFCAPG sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f NMFCAP monthlyρ_5 holder_act NMFCAPA sbgroup NMFCAPG sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction  "Yes" , replace

*/



esttab   v0 v1 v11 v111   v13   v2 , nomtitle label   n r2   compress   mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Polk-slide.tex ,replace



esttab  v0 v1 v11 v111   v13  v2, nomtitle label  r2 s(Controls Interaction N r2)  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" )mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Polk.tex ,replace




/**/




 
replace median = 0 if Q <=3
replace median = 1 if Q  == 4

replace NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{FCA} ^*}  $ "

replace sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{SameGroup}} $ "



replace NMFCAGM = sbgroup * NMFCA * median
label variable NMFCAGM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times  (\text{FCA}^*) \times {\text{SameGroup}} $ "


replace holder_actM = holder_act * median
label variable holder_actM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{ActiveHolder} }  $ "

replace spositionM = sposition * median

label variable spositionM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{Same Position} }  $ "


corr monthlyρ_5_f NMFCA NMFCAM monthlyρ_5  holder_act  sbgroup  sgroup monthlysamesize monthlysamebm 




eststo v00: quietly xtfmb monthlyρ_5_f NMFCA , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v0: quietly xtfmb monthlyρ_5_f  NMFCA NMFCAM , lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v11: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 sbgroup  , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace





eststo v2: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


esttab v00 v0 v1 v11     v2, nomtitle label  n r2 compress mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Qmresult2-slide.tex ,replace


esttab v00 v0 v1 v11    v2, nomtitle label  n r2 compress   addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" )mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Qmresult2.tex ,replace

/**/


eststo v0: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAM sbgroup     sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 


eststo v1: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 




eststo v2: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAM NMFCAG    sbgroup     sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 


 eststo v3: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 

 eststo v4: quietly  xtfmb monthlyρ_5_f NMFCA  NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 
 

 eststo v5: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 
 
 
 

esttab   v0 v1 v2  v4 v5 v3   , nomtitle label  r2 n compress  keep(NMFCA NMFCAM NMFCAG NMFCAGM    ) mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using Qmresult3-slide.tex ,replace

esttab   v0 v1 v2  v4 v3   , nomtitle label  r2 n   keep(NMFCA NMFCAM NMFCAG NMFCAGM    ) compress addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Qmresult3.tex ,replace



/*****/




 eststo v0: quietly  xtfmb monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm    monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

 eststo v2: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(5) 


 eststo Bv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Bv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo Bv2: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup holder_act  sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2  , lag(5) 


 eststo Sv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Sv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
 eststo Sv2: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup  NMFCAG sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1  , lag(5) 



eststo SBv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0 , lag(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo SBv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo SBv2: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0  , lag(5) 



esttab v0 v1 v2 Bv0 Bv1 Bv2 SBv0 SBv1 SBv2 Sv0 Sv1 Sv2  , nomtitle label n r2  compress order(NMFCA NMFCAM sbgroup  NMFCAG NMFCAGM sgroup) keep(NMFCA NMFCAM sbgroup  NMFCAG  NMFCAGM sgroup)  mgroups("All Firms" "Big Firms" "Big \& Small Firms" "Small Firms"   , pattern(1 0 0 1 0 0 1 0 0 1 0 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	,using Qmresult4-slide.tex ,replace 





/*

/* Same group */





eststo sv10: quietly xtfmb monthlyρ_5_f  NMFCA if sbgroup == 1 ,  lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


eststo sv11: quietly xtfmb monthlyρ_5_f  NMFCA NMFCAM if sbgroup == 1 ,  lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


eststo sv20: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 holder_act sposition2 sgroup monthlysamesize monthlysamebm if sbgroup == 1 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo sv21: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM  monthlyρ_5 holder_act sposition2 sgroup monthlysamesize monthlysamebm  if sbgroup == 1 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo sv30: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 holder_act sposition2 sgroup  monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2 if sbgroup == 1 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

eststo sv31: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM  monthlyρ_5 holder_act sposition2 sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2 if sbgroup == 1 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

esttab sv10 sv11 sv20 sv21 sv30 sv31, nomtitle s(Controls Interaction N r2 )    drop ( monthlyρ_5 monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  ,using Mmresult2Samegroup-slide.tex ,replace

esttab sv10 sv11 sv20 sv21 sv30 sv31, nomtitle  s(Controls Interaction N r2) label drop ( monthlyρ_5 monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ),using Mmresult2Samegroup.tex ,replace


/* Not Same group */



eststo v10: quietly xtfmb monthlyρ_5_f  NMFCA if sbgroup == 0 ,  lag(5)
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace


eststo v11: quietly xtfmb monthlyρ_5_f  NMFCA NMFCAM if sbgroup == 0 ,  lag(5)
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace


eststo v20: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 holder_act sposition2 sgroup monthlysamesize monthlysamebm if sbgroup == 0 , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v21: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM  monthlyρ_5 holder_act sposition2 sgroup monthlysamesize monthlysamebm  if sbgroup == 0 , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v30: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 holder_act sposition2 sgroup  monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2 if sbgroup == 0 , lag(5) 
estadd loc Value "Yes" , replace
estadd loc Interaction "Yes" , replace



eststo v31: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM  monthlyρ_5 holder_act sposition2 sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2 if sbgroup == 0 , lag(5) 
estadd loc Value "Yes" , replace
estadd loc Interaction "Yes" , replace

esttab v10 v11 v20 v21 v30 v31, nomtitle s(Value Interaction N r2)  label drop ( monthlyρ_5 monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  ,using Mmresult2NotSamegroup-slide.tex ,replace

esttab v10 v11 v20 v21 v30 v31, nomtitle    s(Value Interaction N r2) label drop ( monthlyρ_5 monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)   addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ),using Mmresult2NotSamegroup.tex ,replace


/*Aggregate*/
esttab v10 v11 v20 v21 v30 v31 sv10 sv11 sv20 sv21 sv30 sv31  ,nomtitle label  r2 s(Value Interaction N r2)   drop (sgroup monthlysamesize monthlysamebm monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  mgroups("Different Group" "Same Group"   , pattern(1 0 0 0 0 0 1 0 0 0 0 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	,using Mmresult2bothSamegroup-slide.tex ,replace 



/*Compare*/

suest sv1 v1 

Simultaneous results for sv1 ,v1 


test [sv1]NMFCAM = [v1]NMFCAM
*/
/*
/*NMFCA2*/

eststo v00: quietly xtfmb monthlyρ_5_f NMFCA , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace
eststo v0: quietly xtfmb monthlyρ_5_f  NMFCA NMFCA2 , lag(5)
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v2: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 holder_act sbgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v3: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 holder_act sbgroup sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Value "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 holder_act sbgroup sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 holder_act sbgroup sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Value "Yes" , replace
estadd loc Interaction "Yes" , replace

esttab v00 v0 v1  v3 v5 v4  v2, nomtitle label  r2 s(Value Interaction N r2) drop (monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  ,using mresult2-slide.tex ,replace

esttab v00 v0 v1  v3 v5 v4  v2, nomtitle label  r2 s(Value Interaction N r2) drop (monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ),using mresult2.tex ,replace

*/










