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
	
	
	
	/* Models */
{
	capture drop tempt5
	gen tempt5 = f.monthlyρ_5
	label variable tempt5 " 4Factor + Industry"
	eststo v1: quietly xi: asreg tempt5 NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4) 

	capture drop tempt4
	gen tempt4 = f.monthlyρ_4
	label variable tempt4 " 4Factor "
	eststo v2: quietly xi: asreg tempt4 NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4) 

	capture drop tempt2
	gen tempt2 = f.monthlyρ_2
	label variable tempt2 " CAPM + Industry"
	eststo v3: quietly xi: asreg tempt2 NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4) 

	capture drop tempt6
	gen tempt6 = f.monthlyρ_residual_bench
	label variable tempt6 " Benchmark"
	eststo v4: quietly xi: asreg tempt6 NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4) 




	esttab v3 v2 v1 v4,label  s(N r2 , label("Observations"  "$ R^2 $")) ,using mresult2AllModels.tex ,replace
		
	
}
