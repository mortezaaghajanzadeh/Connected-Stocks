cls
clear
import delimited "E:\RA_Aghajanzadeh\Data\Connected_Stocks\MonthlyAllPairs_1400_06_28.csv", encoding(UTF-8) 
// import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\MonthlyNormalzedFCAP9.2.csv", encoding(UTF-8) 

cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Final Report\Output" 
// cd "C:\Users\RA_Aghajanzadeh\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

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
label variable monthlyρ_6 " $ {\rho_t} $ "
label variable monthlyρlag_5 " $ {\rho_t} $ "



label variable monthlysamesize "SameSize"

summarize monthlyfca  monthlyfcap

rename monthlyfca MFCA

rename monthlyfcap NMFCAP

label variable NMFCAP "$ \text{FCAP*} $"

gen NMFCAPG = sbgroup * NMFCAP

label variable NMFCAPG " $ (\text{FCAP}^*) \times {\text{SameGroup} }  $ "

gen NMFCAPA = holder_act * NMFCAP

label variable NMFCAPA " $ (\text{FCAP}^*) \times {\text{ActiveHolder} }  $ "




rename nmfca NMFCA



generate msize1size2 =  monthlysize1 * monthlysize2
label variable msize1size2 "$ Size1 \times Size2 $"


generate NMFCA2 = NMFCA * NMFCA


label variable NMFCA "$ \text{FCA*} $"


label variable NMFCA2 "$ { \text{FCA}^ * } ^ 2$"



generate msbm1bm2 =  monthlybm1 * monthlybm2

label variable msbm1bm2 "$ BookToMarketMarket_1 \times BookToMarketMarket_2 $"
label variable monthlysamebm "SameBookToMarket"
label variable monthlybm1 "$ BookToMarketMarket_1 $"

label variable monthlybm2 "$ BookToMarketMarket_2 $"






drop if monthlyfcapf >1
drop if fcapf >1


xtset id t_month  





replace monthlycrossownership = monthlycrossownership/100
label variable monthlycrossownership "CrossOwnership"



gen median = 0
xtile  Q = MFCA if MFCA>0 , nq(4)
replace median = 1 if Q > 3

summ Q median

replace median = v104


label variable median " $ (\text{FCA} > Q3[\text{FCA}]) $ "

gen NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA} > Q3[\text{FCA}]) \times {\text{FCA} ^*}  $ "

gen sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA} > Q3[\text{FCA}]) \times {\text{SameGroup} }  $ "

gen NMFCAG = sbgroup * NMFCA
label variable NMFCAG " $ (\text{FCA}^*) \times {\text{SameGroup} }  $ "

gen NMFCAGM = sbgroup  * median
label variable NMFCAGM " $ (\text{FCA} > Q3[\text{FCA}]) \times  {\text{SameGroup} }  $ "


summ MFCA if median == 1

summ monthlyfcapf if monthlyfcapf>0


eststo v1 : quietly asreg monthlyρ_5_f median   monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
eststo v3 : quietly asreg monthlyρ_5_f median  NMFCAGM  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo v4 : quietly asreg monthlyρ_5_f  sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo v5 : quietly asreg monthlyρ_5_f median sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
 eststo v6: quietly asreg monthlyρ_5_f median  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

 eststo v7: quietly asreg monthlyρ_5_f NMFCA sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

esttab  v4 v5 v1 v6 v7 v3 ,  nomtitle  label  s( N subSample controll r2 ,  lab("Observations" "Sub Sample" "Controls" "$ R^2 $")) order(median   sbgroup NMFCAGM NMFCA) keep(median  NMFCAGM sbgroup NMFCA) compress  mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) 

,using Q3mresultAllPairs.tex ,replace



asreg monthlyρ_5_f NMFCA  sgroup monthlysamesize monthlysamebm monthlycrossownership if MFCA >0 , fmb newey(4)

correlate  median  NMFCAGM sbgroup
/****/



drop median 
egen median = median(MFCA) if MFCA>0

replace median = 1 if MFCA > median
replace median = 0 if median != 1 



label variable median " $ (\text{FCA} > Median[\text{FCA}]) $ "

replace NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA} > Median[\text{FCA}]) \times {\text{FCA} ^*}  $ "

replace sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA} > Median[\text{FCA}]) \times {\text{SameGroup} }  $ "

replace NMFCAGM = sbgroup  * median
label variable NMFCAGM " $ (\text{FCA} > Median[\text{FCA}]) \times  {\text{SameGroup} }  $ "



eststo v1 : quietly asreg monthlyρ_5_f median   monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
eststo v3 : quietly asreg monthlyρ_5_f median  NMFCAGM monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo v4 : quietly asreg monthlyρ_5_f monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo v5 : quietly asreg monthlyρ_5_f median   monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
 eststo v6: quietly asreg monthlyρ_5_f median   monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

 eststo v7: quietly asreg monthlyρ_5_f NMFCA   monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

esttab  v4 v5 v1 v6 v7 v3 ,  nomtitle  label  s( N subSample controll r2 ,  lab("Observations" "Sub Sample" "Controls" "$ R^2 $")) order(median   sbgroup NMFCAGM NMFCA) keep(median  NMFCAGM sbgroup NMFCA) compress  mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Q2mresultAllPairs.tex ,replace

/**/


replace median = 0 
replace median = 1 if MFCA > 0



label variable median " Common Ownership "

replace NMFCAM = NMFCA * median

label variable NMFCAM " $ \text{Common Ownership} \times {\text{FCA} ^*}  $ "

replace sbgroupM = sbgroup * median
label variable sbgroupM " $ \text{Common Ownership} \times {\text{SameGroup} }  $ "

replace NMFCAGM = sbgroup  * median
label variable NMFCAGM " $ \text{Common Ownership} \times  {\text{SameGroup} }  $ "



eststo v1 : quietly asreg monthlyρ_5_f median   monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
eststo v3 : quietly asreg monthlyρ_5_f median  NMFCAGM monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo v4 : quietly asreg monthlyρ_5_f monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo v5 : quietly asreg monthlyρ_5_f median   monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
 eststo v6: quietly asreg monthlyρ_5_f median   monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

 eststo v7: quietly asreg monthlyρ_5_f NMFCA   monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

esttab  v4 v5 v1 v6 v7 v3 ,  nomtitle  label  s( N subSample controll r2 ,  lab("Observations" "Sub Sample" "Controls" "$ R^2 $")) order(median   sbgroup NMFCAGM NMFCA) keep(median  NMFCAGM sbgroup NMFCA) compress  mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using mresultAllPairs.tex ,replace
