

 




eststo v0: quietly asreg monthlyρ_6_f  NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v1: quietly asreg monthlyρ_6_f NMFCA  monthlyρ_6 , fmb newey(4)
estadd loc GroupFE "No" , replace


eststo v11: quietly asreg monthlyρ_6_f NMFCA  monthlyρ_6 sgroup, fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v111: quietly asreg monthlyρ_6_f NMFCA  monthlyρ_6 sbgroup sgroup, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v13: quietly asreg monthlyρ_6_f NMFCA  monthlyρ_6 sbgroup NMFCAG sgroup, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v2: quietly asreg monthlyρ_6_f NMFCA monthlyρ_6 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v3: quietly asreg monthlyρ_6_f NMFCA monthlyρ_6 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace



esttab   v0 v1 v11 v111   v13  v2 v3 , nomtitle label   s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $"))  keep(NMFCA monthlyρ_6 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership ) order(NMFCA NMFCAG sbgroup) compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry + Bgroup Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult6.tex ,replace



eststo v00: quietly asreg monthlyρ_6_f NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v0: quietly asreg monthlyρ_6_f  NMFCA NMFCAM , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v1: quietly asreg monthlyρ_6_f NMFCA NMFCAM monthlyρ_6 , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v11: quietly asreg monthlyρ_6_f NMFCA NMFCAM monthlyρ_6 sbgroup  , fmb newey(4) 
estadd loc GroupFE "No" , replace





eststo v2: quietly asreg monthlyρ_6_f NMFCA NMFCAM monthlyρ_6    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v3: quietly asreg monthlyρ_6_f NMFCA NMFCAM monthlyρ_6    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership  gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace


esttab v00 v0 v1 v11   v2 v3, nomtitle label  s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $")) keep(NMFCA NMFCAM monthlyρ_6    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership) order(NMFCA NMFCAM sbgroup) compress mgroups("Dep. Variable: Future Monthly Corr. of 4F+Ind. + Bgroup Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Qmresult6.tex ,replace



