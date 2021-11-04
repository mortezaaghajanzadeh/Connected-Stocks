/*Grapghs*/



binscatter monthlyρ_5_f MFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) xscale(log) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("FCA") title("Common Pairs") 
graph export mcorr50.eps,replace
graph export mcorr50.png,replace

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

eststo v1: quietly asreg monthlyρ_turn_f  NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v2: quietly asreg monthlyρ_turn_f NMFCA monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v3: quietly asreg monthlyρ_turn_f  sbgroup  , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v4: quietly asreg monthlyρ_turn_f sbgroup  monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v5: quietly asreg monthlyρ_turn_f NMFCA sbgroup , fmb newey(4) 
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v6: quietly asreg monthlyρ_turn_f NMFCA sbgroup monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace

eststo v7: quietly asreg monthlyρ_turn_f NMFCA sbgroup NMFCAG, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v8: quietly asreg monthlyρ_turn_f NMFCA sbgroup NMFCAG monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v9: quietly asreg monthlyρ_turn_f NMFCA sbgroup NMFCAG monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
estadd loc GroupFE "Yes" , replace
estadd loc controll "Yes" , replace



esttab   v3 v4 v1 v2 /*v5*/ v6 /*v7*/ v8 v9 ,nomtitle label   s( N GroupFE controll r2 ,  lab("Observations" "Group Effect" "Controls" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(sbgroup NMFCA  NMFCAG )  mgroups("Dependent Variable: Future Monthly Correlation of Delta turnover"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-turnover.tex ,replace


/**/




/* Imbalance*/

eststo v1 :  quietly asreg monthlyρ_5_f NMFCA     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup  , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace

eststo v2 :  quietly asreg monthlyρ_5_f NMFCA     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd  , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace

eststo v3 :  quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace

eststo v4 :  quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace

eststo v5 :  quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA gdummy0-gdummy47, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "Yes" , replace

eststo v6 :  quietly asreg monthlyρ_5_f    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup  , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace

eststo v7 :  quietly asreg monthlyρ_5_f  NMFCA  sgroup monthlysamesize monthlysamebm monthlycrossownership  lowimbalancestd  if sbgroup == 1  , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Same Groups" , replace
estadd loc GroupFE "No" , replace

esttab   v1 v2 v3 v6  v7  v4 v5, nomtitle label   keep(NMFCA sbgroup lowimbalancestd ImbalanceSbgroup  ) order(NMFCA sbgroup) s( N GroupFE  subsample controll r2 ,  lab("Observations" "Group Effect" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )


esttab   v1 v2 v3 v6  v7  v4 v5, nomtitle label   keep(NMFCA sbgroup lowimbalancestd ImbalanceSbgroup  ) order(NMFCA sbgroup) s( N GroupFE  subsample controll r2 ,  lab("Observations" "Group Effect" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Imbalance.tex ,replace

/**/



/* bigbusinessgroup*/

eststo v1: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "All" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership bigbusinessgroup bigbusinessgroupSgroup, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace
estadd loc SubSample "All" , replace

esttab   v1 v2  , nomtitle label   keep(NMFCA sbgroup bigbusinessgroup bigbusinessgroupSgroup   ) order(NMFCA sbgroup) s( N GroupFE  subsample controll r2 ,  lab("Observations" "Group Effect" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )

/**/

eststo v2: quietly asreg monthlyρ_5_f NMFCA   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

eststo v1: quietly asreg monthlyρ_5_f NMFCAP  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)


eststo v3: quietly asreg monthlyρ_5_f NMFCAP NMFCAPG  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
eststo v4: quietly asreg monthlyρ_5_f NMFCA NMFCAG sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

esttab v1 v3 v2  v4 , label star(* 0.10 ** 0.05 *** 0.01) keep( NMFCAP NMFCAPG NMFCAG NMFCA   sbgroup) order( NMFCAP NMFCAPG NMFCAG NMFCA   sbgroup) s(N r2)

