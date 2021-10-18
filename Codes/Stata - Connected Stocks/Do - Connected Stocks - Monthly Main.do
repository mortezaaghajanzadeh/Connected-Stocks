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


/**/

eststo v2: quietly asreg monthlyρ_5_f NMFCA   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

eststo v1: quietly asreg monthlyρ_5_f NMFCAP  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)


eststo v3: quietly asreg monthlyρ_5_f NMFCAP NMFCAPG  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
eststo v4: quietly asreg monthlyρ_5_f NMFCA NMFCAG sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

esttab v1 v3 v2  v4 , label star(* 0.10 ** 0.05 *** 0.01) keep( NMFCAP NMFCAPG NMFCAG NMFCA   sbgroup) order( NMFCAP NMFCAPG NMFCAG NMFCA   sbgroup) s(N r2)

