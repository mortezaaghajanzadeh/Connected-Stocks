cls
clear
import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\MonthlyZeroGroupAddedv2.csv", encoding(UTF-8) 


cd "D:\Dropbox\Connected Stocks\Final Report"

label define sgroup 0 "No" 1 "Yes"



label values sgroup sgroup
label variable sgroup "SameIndustry"

label values sbgroup sgroup
label variable sbgroup "SameGroup"







label variable monthlysize1 "Size1"
label variable monthlysize2 "Size2"
label variable monthlyρ_4_f "ForwardCorr"
label variable monthlyρ_2 " $ {\rho_t} $ "
label variable monthlyρ_4 " $ {\rho_t} $ "
label variable monthlyρ_5 " $ {\rho_t} $ "
label variable monthlysamesize "SameSize"

summarize monthlyfca  monthlyfcap

rename monthlyfca MFCA

rename monthlyfcap NMFCAP

label variable NMFCAP "$ \text{FCAP*} $"





rename nmfca NMFCA



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

xtile  Q = NMFCA, nq(4)
 
replace median = 0 if Q <=3
replace median = 1 if Q  == 4

generate NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{FCA} ^*}  $ "





label variable median " $ (\text{FCA}^* > Q3[\text{FCA}^*]) $ "



hist MFCA
summ MFCA


summ NMFCA if MFCA  == 0


drop if monthlyfcapf >1
drop if fcapf >1


xtset id t_month  

binscatter  monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(10) by (sbgroup) legend(pos(1) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S)  note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCA*")title("Common Pairs")

graph export zeropBGsampleg.eps,replace
graph export zeropBGsampleg.png,replace


binscatter  monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(20)     note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCA*")title("Common Pairs")

graph export zeropBGsample.eps,replace
graph export zeropBGsample.png,replace




eststo v1: quietly asreg monthlyρ_5_f NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace


eststo v2: quietly asreg monthlyρ_5_f NMFCA   gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace


eststo v3: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v4: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm  gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace


eststo v5: quietly asreg monthlyρ_5_f median sbgroup monthlyρ_5   sgroup monthlysamesize monthlysamebm  , fmb newey(4)
estadd loc GroupFE "No" , replace


eststo v6: quietly asreg monthlyρ_5_f median sbgroup monthlyρ_5   sgroup monthlysamesize monthlysamebm  gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace

eststo v7: quietly asreg monthlyρ_5_f NMFCA  NMFCAM median sbgroup monthlyρ_5   sgroup monthlysamesize monthlysamebm  , fmb newey(4)
estadd loc GroupFE "No" , replace

esttab    v1  v2 v3 v4 v5 v6 v7 , nomtitle label   s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $"))  keep(NMFCA  NMFCAM median monthlyρ_5  sbgroup  sgroup monthlysamesize monthlysamebm ) order(NMFCA sbgroup median NMFCAM )  compress mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using ZeroBGSample.tex ,replace




