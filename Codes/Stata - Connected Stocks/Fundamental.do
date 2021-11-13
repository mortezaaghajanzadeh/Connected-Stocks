cls
clear
// import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\Earnings.csv", encoding(UTF-8) 
import delimited "E:\RA_Aghajanzadeh\Data\Connected_Stocks\Earnings.csv", encoding(UTF-8) 



// cd "D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Final Report\Output"

xtset  t id

generate  earning = earning1
generate  earning_group = earning1_group
generate  earning_ind = earning1_ind
generate  earning_market = earning1_market

rename v35 r



eststo v1 : quietly asreg r  earning earning_group earning_ind earning_market  , fmb newey(4)
estadd loc Measure "1Q" , replace


replace  earning = earning2
replace  earning_group = earning2_group
replace  earning_ind = earning2_ind
replace  earning_market = earning2_market

eststo v2 :  quietly asreg r  earning earning_group earning_ind earning_market  , fmb newey(4)
estadd loc Measure "2Q" , replace



replace  earning = earning4
replace  earning_group = earning4_group
replace  earning_ind = earning4_ind
replace  earning_market = earning4_market

eststo v3 : quietly asreg r  earning earning_group earning_ind earning_market  , fmb newey(4)
estadd loc Measure "4Q" , replace

label variable earning "Earning"
label variable earning_group " $\text{Earning}_{\text{group}} $ "
label variable earning_ind "$\text{Earning}_{\text{ind}} $"
label variable earning_market "$\text{Earning}_{\text{market}} $"


esttab v1 v2 v3 ,label s( N Measure r2 ,  lab("Observations"  "Earnings Measure" "$ R^2 $")) mgroups("Dependent Variable: Quarterly return"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) 

esttab v1 v2 v3 ,label s( N Measure r2 ,  lab("Observations"  "Earnings Measure" "$ R^2 $")) mgroups("Dependent Variable: Quarterly return"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using mresult2Fundumental.tex ,replace
