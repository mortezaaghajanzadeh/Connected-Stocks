/*Grapghs*/



binscatter monthlyρ_5_f MFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) xscale(log) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("FCA") title("Common Pairs") 
graph export mcorr50.eps,replace
graph export mcorr50.png,replace


binscatter monthlyρ_5_f NMFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(20) by(bigbusinessgroupSgroup) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("FCA*") title("Common Pairs") legend(pos(4) ring(0) col(1) label(1 "Big Same Group") label(2 "Others") ) msymbol(Th S) 
graph export mcorr5BigSameG.eps,replace
graph export mcorr5BigSameG.png,replace


/*NMFCA*/
eststo clear

eststo v1: quietly asreg monthlyρ_5_f  NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace
estadd loc SubSample "All" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "All" , replace

eststo v3: quietly asreg monthlyρ_5_f  sbgroup  , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace
estadd loc SubSample "All" , replace

eststo v4: quietly asreg monthlyρ_5_f sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "All" , replace


eststo v5: quietly asreg monthlyρ_5_f NMFCA sbgroup , fmb newey(4) 
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace
estadd loc SubSample "All" , replace

eststo v6: quietly asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "All" , replace

eststo v7: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace
estadd loc SubSample "All" , replace

eststo v8: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "All" , replace


eststo v9: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
estadd loc GroupFE "Yes" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "All" , replace



eststo v10: quietly asreg monthlyρ_5_f NMFCA     sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "SameGroup" , replace
eststo v11: quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership   if sbgroup == 0, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "Others" , replace

esttab   v3 v4 v1 v2 /*v5*/ v6 v10 v11 /*v7*/ v8 v9   ,nomtitle label   s( N  SubSample GroupFE controll r2 ,  lab("Observations" "Sub-sample" "Group Effect" "Controls" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(sbgroup NMFCA    ) mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  star(* 0.10 ** 0.05 *** 0.01) 

esttab   v3 v4 v1 v2 /*v5*/ v6 v10 v11 /*v7*/ v8 v9   ,nomtitle label   s( N  SubSample GroupFE controll r2 ,  lab("Observations" "Sub-sample" "Group Effect" "Controls" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(sbgroup NMFCA    ) mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  star(* 0.10 ** 0.05 *** 0.01) ,using mresult2-slide.tex ,replace


/* Turnover */
eststo clear

eststo v1: quietly asreg monthlyρ_turn_f  NMFCA  , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace
estadd loc FE "No" , replace


eststo v2: xi: quietly asreg monthlyρ_turn_f NMFCA monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc FE "Yes" , replace


eststo v3: quietly asreg monthlyρ_turn_f  sbgroup  , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace
estadd loc FE "No" , replace

eststo v4: xi: quietly asreg monthlyρ_turn_f sbgroup  monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc FE "Yes" , replace

/*
eststo v5: quietly asreg monthlyρ_turn_f NMFCA sbgroup , fmb newey(4) 
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace
estadd loc FE "No" , replace
*/

eststo v6: xi: quietly asreg monthlyρ_turn_f NMFCA sbgroup monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc FE "Yes" , replace

/*
eststo v7: quietly asreg monthlyρ_turn_f NMFCA sbgroup NMFCAG, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace
estadd loc FE "No" , replace
*/
eststo v8: xi: quietly asreg monthlyρ_turn_f NMFCA sbgroup NMFCAG monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc FE "Yes" , replace


eststo v9: xi: quietly asreg monthlyρ_turn_f NMFCA sbgroup NMFCAG monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 i.PairType, fmb newey(4)
estadd loc GroupFE "Yes" , replace
estadd loc controll "Yes" , replace
estadd loc FE "Yes" , replace



esttab   v3 v4 v1 v2 /*v5*/ v6 /*v7*/ v8 v9 ,nomtitle label   s( N GroupFE FE controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Controls" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(sbgroup NMFCA  NMFCAG )  mgroups("Dependent Variable: Future Monthly Correlation of Delta turnover"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-turnover.tex ,replace


/**/




/* Imbalance*/

eststo v1 :  xi: quietly asreg monthlyρ_5_f NMFCA     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup   i.PairType, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace
estadd loc FE "Yes" , replace

eststo v2 :  xi: quietly asreg monthlyρ_5_f NMFCA     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd   i.PairType, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace
estadd loc FE "Yes" , replace

eststo v3 :  xi: quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup  i.PairType, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace
estadd loc FE "Yes" , replace

eststo v4 :  xi: quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA  i.PairType, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace
estadd loc FE "Yes" , replace

eststo v5 :  xi: quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA gdummy0-gdummy47  i.PairType, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "Yes" , replace
estadd loc FE "Yes" , replace

eststo v6 :  xi: quietly asreg monthlyρ_5_f sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup   i.PairType, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace
estadd loc FE "Yes" , replace

eststo v7 :  xi: quietly asreg monthlyρ_5_f  NMFCA  sgroup monthlysamesize monthlysamebm monthlycrossownership  lowimbalancestd i.PairType if sbgroup == 1   , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Same Groups" , replace
estadd loc GroupFE "No" , replace
estadd loc FE "Yes" , replace


eststo v8 :  xi: quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd  ImbalanceSbgroupFCA   i.PairType, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace
estadd loc FE "Yes" , replace

esttab   v1 v2 v3 v6  v7 v8 v4 v5, nomtitle label   keep(NMFCA sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA  ) order(NMFCA sbgroup) s( N GroupFE FE  subsample controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )


esttab   v1 v2 v3 v6  v7 v8 v4 v5, nomtitle label   keep(NMFCA sbgroup lowimbalancestd ImbalanceSbgroup  ImbalanceSbgroupFCA ) order(NMFCA sbgroup) s( N GroupFE FE  subsample controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Imbalance.tex ,replace

/**/








/**/

eststo v2: quietly asreg monthlyρ_5_f NMFCA   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

eststo v1: quietly asreg monthlyρ_5_f NMFCAP  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)


eststo v3: quietly asreg monthlyρ_5_f NMFCAP NMFCAPG  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
eststo v4: quietly asreg monthlyρ_5_f NMFCA NMFCAG sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

esttab v1 v3 v2  v4 , label star(* 0.10 ** 0.05 *** 0.01) keep( NMFCAP NMFCAPG NMFCAG NMFCA   sbgroup) order( NMFCAP NMFCAPG NMFCAG NMFCA   sbgroup) s(N r2)

