



/*NWFCA*/

eststo v0: quietly asreg weeklyρ_5_f  NWFCA , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v1: quietly asreg weeklyρ_5_f NWFCA  weeklyρ_5 , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


eststo v11: quietly asreg weeklyρ_5_f NWFCA  weeklyρ_5 sgroup, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v111: quietly asreg weeklyρ_5_f NWFCA  weeklyρ_5 sbgroup sgroup, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v13: quietly asreg weeklyρ_5_f NWFCA  weeklyρ_5 sbgroup NWFCAG sgroup, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v2: quietly asreg weeklyρ_5_f NWFCA weeklyρ_5 sbgroup NWFCAG  sgroup weeklysamesize weeklysamebm weeklycrossownership, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v3: quietly asreg weeklyρ_5_f NWFCA weeklyρ_5 sbgroup NWFCAG  sgroup weeklysamesize weeklysamebm weeklycrossownership gdummy0-gdummy47, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace




esttab   v0 v1 v11 v111   v13  v2 v3 , nomtitle label  n r2  keep(NWFCA weeklyρ_5 sbgroup NWFCAG  sgroup weeklysamesize weeklysamebm weeklycrossownership ) order(NWFCA NWFCAG sbgroup) compress mgroups("Dependent Variable: Future weekly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using wresult2-slide.tex ,replace














