cls
clear
import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\Earnings.csv", encoding(UTF-8) 


cd "D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

xtset  t id

generate  earning = earning1
generate  earning_group = earning1_group
generate  earning_ind = earning1_ind
generate  earning_market = earning1_market

eststo v1 : quietly asreg v34  earning earning_group earning_ind earning_market  , fmb newey(4)

replace  earning = earning2
replace  earning_group = earning2_group
replace  earning_ind = earning2_ind
replace  earning_market = earning2_market

eststo v2 :  quietly asreg v34  earning earning_group earning_ind earning_market  , fmb newey(4)

replace  earning = earning4
replace  earning_group = earning4_group
replace  earning_ind = earning4_ind
replace  earning_market = earning4_market

eststo v3 : quietly asreg v34  earning earning_group earning_ind earning_market  , fmb newey(4)

esttab v1 v2 v3