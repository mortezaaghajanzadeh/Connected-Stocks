/*NMFCAP*/
{
	capture drop vv
	capture drop Gvv
	gen vv =   NMFCAP
	gen  Gvv = NMFCAPG
  
  
	eststo v0: quietly asreg monthlyρ_5_f  vv sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace
	
	eststo v1: quietly asreg monthlyρ_5_f vv sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace
	
	eststo v2: quietly asreg monthlyρ_5_f  vv sbgroup Gvv sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace

	
	eststo v3: quietly asreg monthlyρ_5_f  vv sbgroup /*Gvv*/ sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace
	
	eststo v4: quietly asreg monthlyρ_5_f  vv sbgroup Gvv sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc Measure "Sum" , replace
	
	replace vv = NMFCA
	replace  Gvv = NMFCAG
	
	eststo v01: quietly asreg monthlyρ_5_f  vv sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace
	
	eststo v11: quietly asreg monthlyρ_5_f  vv sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace

	eststo v21: quietly asreg monthlyρ_5_f  vv sbgroup Gvv sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "SQRT" , replace

	
	eststo v31: quietly asreg monthlyρ_5_f  vv sbgroup /*Gvv*/ sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "SQRT" , replace

	eststo v41: quietly asreg monthlyρ_5_f  vv sbgroup Gvv sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc Measure "SQRT" , replace

	label variable vv "Common Ownership Measure"
	label variable Gvv " $ \text{\small Common Ownership Measure} \times {\text{SameGroup} }$ "

	esttab   v0 v01   v1 v11 v2 v21 /*v3 v31*/ v4 v41, nomtitle label   s( N GroupFE Measure r2 ,  lab("Observations" "Group FE" "Measurement" "$ R^2 $"))  keep(vv sbgroup Gvv  /*sgroup monthlysamesize monthlysamebm monthlycrossownership*/) order(vv sbgroup Gvv) compress   mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )
}



	esttab   v0 v01   v1 v11 v2 v21 /*v3 v31*/ v4 v41, nomtitle label   s( N GroupFE Measure r2 ,  lab("Observations" "Group FE" "Measurement" "$ R^2 $"))  keep(vv sbgroup Gvv  /*sgroup monthlysamesize monthlysamebm monthlycrossownership*/) order(vv sbgroup Gvv) compress   mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Polk-slide.tex ,replace