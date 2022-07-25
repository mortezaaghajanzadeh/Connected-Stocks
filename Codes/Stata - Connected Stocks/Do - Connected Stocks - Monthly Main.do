


xi: asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4) 

xi: asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership  monthlysize1 monthlysize2 msize1size2  , fmb newey(4) 


// replace NMFCA = NMFCAP
// replace NMFCAG = NMFCAPG

/*NMFCA*/
{
	eststo clear

	eststo v1: quietly asreg monthlyρ_5_f  NMFCA , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace
	

	eststo v2: quietly asreg monthlyρ_5_f NMFCA  sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/ , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace

	eststo v3: quietly asreg monthlyρ_5_f  sbgroup  , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace

	eststo v4: quietly asreg monthlyρ_5_f sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace


	eststo v5: quietly asreg monthlyρ_5_f NMFCA sbgroup , fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace

	eststo v6: quietly asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace
	
	eststo v61: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/ i.PairType , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "Yes" , replace
	

	eststo v7: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace

	eststo v8: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/ i.PairType , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "Yes" , replace


	eststo v9: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/ gdummy0-gdummy47 i.PairType , fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "Yes" , replace
	


	eststo v10: xi: quietly asreg monthlyρ_5_f NMFCA     sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/ i.PairType if sbgroup == 1 , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "SameGroup" , replace
	estadd loc Pairtypr "Yes" , replace
	
	eststo v11: xi: quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType /*monthlysize1 monthlysize2 msize1size2*/ if sbgroup == 0, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "Others" , replace
	estadd loc Pairtypr "Yes" , replace
	

	esttab    v1 v2 v3 v4 /*v5*/ v6 v61   ,nomtitle label   s(  /*SubSample GroupFE controll*/ Pairtypr N  r2 /*r2*/ ,  lab(/*"Sub-sample" "Group Effect" "Controls"*/  "Size Control" "Observations"  /*"$ R^2 $"*/))   keep(NMFCA sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership _cons /*monthlysize1 monthlysize2 msize1size2*/) postfoot("\hline\hline  \end{tabular}}")  /*prehead("{\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi} \begin{tabular}{l*{6}{c}} \hline   \addlinespace[1ex]  \multicolumn{7}{c}{Panel A: The main analysis   } \\   \addlinespace[1ex] \hline  \addlinespace[1ex]") */ compress order(NMFCA sbgroup     ) mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )
		
	esttab v10 v11 /*v7*/ v8 v9 ,nomtitle label   s( SubSample GroupFE /*controll*/ N /*Pairtypr r2*/ ,  lab( "Sub-sample" "Business Group FE" "Observations" /*"Controls" "Size Control" "$ R^2 $"*/))   keep(NMFCA sbgroup NMFCAG) compress order(NMFCA sbgroup     ) mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )
 	

	
	
}


	
	
	
	
	esttab    v1 v2 v3 v4 /*v5*/ v6 v61   ,nomtitle label   s(  /*SubSample GroupFE controll*/ Pairtypr N  /*r2*/ ,  lab(/*"Sub-sample" "Group Effect" "Controls"*/  "Size Control" "Observations"  /*"$ R^2 $"*/))   keep(NMFCA sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/ _cons) postfoot("\hline\hline  \end{tabular}}")/*prehead("{\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi} \begin{tabular}{l*{6}{c}} \hline   \addlinespace[1ex]  \multicolumn{7}{c}{Panel A: The main analysis   } \\   \addlinespace[1ex] \hline  \addlinespace[1ex]") */   order(NMFCA sbgroup   sgroup monthlysamebm ) mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using mresult2part1-slide.tex ,replace
	

	
	
		esttab v10 v11 /*v7*/ v8 v9 ,nomtitle label   s( SubSample GroupFE /*controll*/ N /*Pairtypr r2*/ ,  lab( "Sub-sample" "Business Group FE" "Observations" /*"Controls" "Size Control" "$ R^2 $"*/))   keep(NMFCA sbgroup NMFCAG) compress order(NMFCA sbgroup     ) /*prehead("{ \def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}  \begin{tabular}{l*{4}{c}}   \addlinespace[2ex]  \multicolumn{5}{c}{Panel B: The relation between common ownership and business group}\\ \hline \addlinespace[1ex]")*/ mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ), using mresult2part2-slide.tex ,replace

		
				esttab v10 v11 /*v7*/ v8 v9 ,nomtitle label   s( SubSample GroupFE /*controll*/ N /*Pairtypr r2*/ ,  lab( "Sub-sample" "Business Group FE" "Observations" /*"Controls" "Size Control" "$ R^2 $"*/))   keep(NMFCA sbgroup NMFCAG   sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/ _cons) compress order(NMFCA sbgroup    NMFCAG ) /*prehead("{ \def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}  \begin{tabular}{l*{4}{c}}   \addlinespace[2ex]  \multicolumn{5}{c}{Panel B: The relation between common ownership and business group}\\ \hline \addlinespace[1ex]")*/ mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ), using mresult2part2-Appendix.tex ,replace



{ /*Define Q3*/
	replace median = 0 if forthquarter != 1
	replace median = 1 if forthquarter == 1

	replace NMFCAM = NMFCA * median

	label variable median "$ (\text{MFCAP} > \text{75th Percentile}) $ "
	
	label variable NMFCAM " $ (\text{MFCAP} > \text{75th Percentile}) \times {\text{MFCAP} ^*}  $ "

	replace sbgroupM = sbgroup * median
	label variable sbgroupM " $ (\text{MFCAP} > \text{75th Percentile}) \times {\text{SameGroup}} $ "



	replace NMFCAGM = sbgroup * NMFCA * median
	label variable NMFCAGM " $ (\text{MFCAP} > \text{75th Percentile}) \times  (\text{MFCAP}^*) \times {\text{SameGroup}} $ "


	replace holder_actM = holder_act * median
	label variable holder_actM " $ (\text{MFCAP}> Q3[\text{MFCAP}]) \times {\text{ActiveHolder} }  $ "

	replace spositionM = sposition * median

	label variable spositionM " $ (\text{MFCAP}> Q3[\text{MFCAP}]) \times {\text{Same Position} }  $ "


	corr monthlyρ_5_f monthlyρ_5  NMFCA median NMFCAM   NMFCAG NMFCAGM sbgroup  sgroup monthlysamesize monthlysamebm 


}


 foreach v of varlist   monthlycrossownership monthlyρ_5 {
	
	capture drop  `v'percent
	gen `v'percent = `v' * 100

}



label define median 0 "Others" 1 "ForthQuarter"


capture drop Pairs
gen Pairs = median
label values Pairs median

tabout  sbgroup sgroup Pairs using table13.tex, c(mean monthlyρ_5percent mean sbgroup mean sgroup mean monthlysamebm   mean monthlysamesize  mean monthlycrossownershippercent  ) clab( "Comovement" "SameGroup" SameInd. "SameBM"  "SameSize"  "CrossOwner."  ) sum  f(2p 2c 2c 2c 2c 2p ) rep style(tex)  ptotal(single) npos(tufte) cl2(2-7) cltr2(lr) topf(top.tex) botf(bot.tex) topstr(1.3\textwidth) botstr(auto.dta) 





{/*NMFCA Dummy*/

	eststo v0: quietly asreg monthlyρ_5_f  sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "All" , replace

	eststo v1: quietly asreg monthlyρ_5_f median sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "All" , replace
	
		eststo v11: quietly asreg monthlyρ_5_f median sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "All" , replace

/*
	eststo v11: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup i.PairType if forthquarter == 1, fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v111: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup sgroup i.PairType if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v2: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType  if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	*/

	eststo v21: xi: quietly asreg monthlyρ_5_f median   sgroup monthlysamesize monthlysamebm monthlycrossownership if (sbgroup == 1 ), fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "SameGroup" , replace
	
		eststo v3: xi: quietly asreg monthlyρ_5_f median   sgroup monthlysamesize monthlysamebm monthlycrossownership if (sbgroup == 0 ), fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "Others" , replace

	eststo v4: xi: quietly asreg monthlyρ_5_f median sbgroup sbgroupM  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "All" , replace
	
		eststo v5: xi: quietly asreg monthlyρ_5_f median  sbgroup sbgroupM  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType gdummy0-gdummy47 , fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "All" , replace



esttab   v0 v1 v11/* v111   v2*/ v21 v3 v4 v5, nomtitle label   s( SubSample Control GroupFE /*Pairtypr*/ N  /*r2*/ ,  lab("Sub-sample" "Controls" "Business Group FE" "Observations" /*"Size Control" "$ R^2 $"*/))  keep(sbgroup median  sbgroupM) order(sbgroup median  sbgroupM) compress mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))


}

esttab   v0 v1 v11/* v111   v2*/ v21 v3 v4 v5, nomtitle label   s( SubSample Control GroupFE /*Pairtypr*/ N  /*r2*/ ,  lab("Sub-sample" "Controls" "Business Group FE" "Observations" /*"Size Control" "$ R^2 $"*/))  keep(sbgroup median  sbgroupM) order(sbgroup median  sbgroupM) compress mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span})),using QTimemresult2subsample-slide.tex ,replace

corr sbgroup median  sbgroupM

esttab   v0 v1 v11/* v111   v2*/ v21 v3 v4 v5, nomtitle label   s( SubSample Control GroupFE /*Pairtypr*/ N  /*r2*/ ,  lab("Sub-sample" "Controls" "Business Group FE" "Observations" /*"Size Control" "$ R^2 $"*/)) keep(NMFCA sbgroup NMFCAG   sgroup monthlysamesize monthlysamebm monthlycrossownership /*monthlysize1 monthlysize2 msize1size2*/ _cons) order(sbgroup NMFCA  NMFCAG ) compress mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span})) ,using QTimemresult2subsample-Appendix.tex ,replace







corr sbgroup NMFCA  NMFCAG if forthquarter == 1 

/* Turn over*/

{
	eststo clear

	eststo v1: quietly asreg monthlyρ_turn_f  NMFCA  , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc subsample "All" , replace

	eststo v2: quietly asreg monthlyρ_turn_f NMFCA monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc subsample "All" , replace


	eststo v3: quietly asreg monthlyρ_turn_f  sbgroup  , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc subsample "All" , replace

	eststo v4: quietly asreg monthlyρ_turn_f sbgroup  monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc subsample "All" , replace

/*
	eststo v5: quietly asreg monthlyρ_turn_f NMFCA sbgroup , fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
*/
	eststo v6: quietly asreg monthlyρ_turn_f NMFCA sbgroup monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc subsample "All" , replace
/*
	eststo v7: quietly asreg monthlyρ_turn_f NMFCA sbgroup NMFCAG, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
*/
	eststo v8: quietly asreg monthlyρ_turn_f NMFCA   monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1 , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc subsample "SameGroup" , replace


	eststo v9: quietly asreg monthlyρ_turn_f NMFCA   monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 0 , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc subsample "Others" , replace
	
	eststo v10: quietly asreg monthlyρ_turn_f NMFCA  sbgroup monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership NMFCAG, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc subsample "All" , replace
	
		eststo v11: quietly asreg monthlyρ_turn_f NMFCA  sbgroup monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership NMFCAG gdummy0-gdummy47, fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc controll "Yes" , replace
	estadd loc subsample "All" , replace



	esttab   /*v3*/ v4 /*v1*/ v2 /*v5*/ v6 /*v7*/ v8 v9 v10 v11,nomtitle label   s( /*controll*/ subsample GroupFE  N   ,  lab(/*"Controls"*/ "Sub-sample" "Business Group FE""Observations"   ))   keep(NMFCA sbgroup NMFCAG) compress order(sbgroup NMFCA NMFCAG  )  mgroups("Dependent Variable:  Future Monthly Correlation of Delta turnover"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )
	


}
	
	
	

	
	esttab   /*v3*/ v4 /*v1*/ v2 /*v5*/ v6 /*v7*/ v8 v9 v10 v11,nomtitle label   s( /*controll*/ subsample GroupFE  N   ,  lab(/*"Controls"*/ "Sub-sample" "Business Group FE""Observations"   ))   keep(NMFCA sbgroup NMFCAG)  postfoot("\hline\hline  \end{tabular}}")	/*prehead("{\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi} \begin{tabular}{l*{7}{c}} \hline   \addlinespace[1ex]  \multicolumn{8}{c}{Panel A: Correlation of $ \Delta \text{TurnOver} $ and interested variables  } \\   \addlinespace[1ex] \hline  \addlinespace[1ex]") order(sbgroup NMFCA NMFCAG  ) */ mgroups("Dependent Variable:  Monthly Correlation of Delta turnover"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-turnover.tex ,replace

		esttab   /*v3*/ v4 /*v1*/ v2 /*v5*/ v6 /*v7*/ v8 v9 v10 v11,nomtitle label   s( /*controll*/ subsample GroupFE  N   ,  lab(/*"Controls"*/ "Sub-sample" "Business Group FE""Observations"   ))   keep(NMFCA sbgroup NMFCAG NMFCA sbgroup NMFCAG   sgroup monthlysamesize monthlysamebm monthlycrossownership  _cons) order(sbgroup NMFCA NMFCAG) postfoot("\hline\hline  \end{tabular}}") mgroups("Dependent Variable:  Monthly Correlation of Delta turnover"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-turnover-Appendix.tex ,replace

	
	
	
	
	
	
	
{ /*Turn on Co Movement*/

eststo clear

eststo v1 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f , fmb newey(4)
estadd loc controll "No" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace


eststo v2 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace


eststo v3 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "Yes" , replace

eststo v4 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f   sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1 , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "SameGroup" , replace
estadd loc GroupFE "No" , replace

eststo v5 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f   sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 0 , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Others" , replace
estadd loc GroupFE "No" , replace

eststo v6 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f  sbgroup sgroup turnSbgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace

eststo v7 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f  sbgroup sgroup turnSbgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "Yes" , replace



esttab   v1 v2 v3 v4 v5 /*v6 v7*/, nomtitle  label  keep(monthlyρ_turn_f monthlyρ_5 /*sbgroup turnSbgroup*/ ) order(monthlyρ_turn_f) s( controll subsample   GroupFE   N  ,  lab( "Control" "Sub-sample" "Business Group FE" "Observations")) compress mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))


 


}

esttab   v1 v2  v4 v5 v3/*v6 v7*/, nomtitle  label  keep(monthlyρ_turn_f monthlyρ_5 /*sbgroup turnSbgroup*/ ) order(monthlyρ_turn_f) s( controll subsample   GroupFE   N  ,  lab( "Control" "Sub-sample" "Business Group FE" "Observations"))  /*prehead("{\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi} \begin{tabular}{l*{5}{c}} \hline   \addlinespace[1ex]  \multicolumn{6}{c}{Panel B: Correlation of $ \Delta \text{TurnOver} $ and Comovement } \\   \addlinespace[1ex] \hline  \addlinespace[1ex]") */ mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))  ,using turncomovement.tex ,replace

esttab   v1 v2  v4 v5 v3/*v6 v7*/, nomtitle  label  keep(monthlyρ_turn_f monthlyρ_5      sgroup monthlysamesize monthlysamebm monthlycrossownership _cons /*sbgroup turnSbgroup*/ ) order(monthlyρ_turn_f) s( controll subsample   GroupFE   N  ,  lab( "Control" "Sub-sample" "Business Group FE" "Observations")) mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))  ,using turncomovement-Appendix.tex ,replace
	
	
	
	

{/*LowRes*/

	eststo clear
	
	eststo v1 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup   i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "No" , replace

	eststo v2 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowres gsize_y gsize_x  i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace

	eststo v3 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowres Grouplowres gsize_y gsize_x  i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace
	
	eststo v6 :  xi: quietly asreg monthlyρ_5_f /*NMFCA  NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowres Grouplowres i.PairType gdummy0-gdummy47  , fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "Yes" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "No" , replace
	
	eststo v7 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership   lowres  gsize_y gsize_x  i.PairType if sbgroup == 1, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "SameGroup" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace
	
		eststo v8 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership   lowres  gsize_y gsize_x  i.PairType if sbgroup == 0, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Others" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace
	
	
	
	
esttab   v1 v2  v7 v8 v3 v6 , nomtitle  label  keep(/*NMFCA */ sbgroup lowres Grouplowres/*  trunresstd_x trunresstd_y xx */) order(/*NMFCA */ sbgroup lowres /*Grouplowres NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA trunresstd_x trunresstd_y xx*/ ) s( /*GroupSizeFE*/ subsample GroupFE      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" "Business Group FE" "Observations")) compress mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
}

esttab   v1 v2  v7 v8 v3 v6 , nomtitle  label  keep(/*NMFCA */ sbgroup lowres Grouplowres/*  trunresstd_x trunresstd_y xx */) order(/*NMFCA */ sbgroup lowres /*Grouplowres NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA trunresstd_x trunresstd_y xx*/ ) s( /*GroupSizeFE*/ subsample GroupFE      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" "Business Group FE" "Observations"))  postfoot("\hline\hline  \end{tabular}}")/*prehead("{\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi} \begin{tabular}{l*{6}{c}} \hline   \addlinespace[1ex]  \multicolumn{7}{c}{Panel A: Low Turnover residual std groups and Comovement } \\   \addlinespace[1ex] \hline  \addlinespace[1ex]")*/ compress mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span})),using LowRes.tex ,replace
	

	
esttab   v1 v2  v7 v8 v3 v6 , nomtitle  label  keep(/*NMFCA */ sbgroup lowres Grouplowres   sgroup monthlysamesize monthlysamebm monthlycrossownership  _cons) order( sbgroup lowres Grouplowres ) s( /*GroupSizeFE*/ subsample GroupFE      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" "Business Group FE" "Observations"))  postfoot("\hline\hline  \end{tabular}}") compress mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span})),using LowRes-Appendix.tex ,replace	
	
corr sbgroup lowres Grouplowres
	

	
	
{/* Imbalance*/
	


	eststo v1 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup   i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "No" , replace

	eststo v2 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd /*gsize_y gsize_x*/  i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace

	eststo v3 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup  /*gsize_y gsize_x*/ i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace
	
	
	
		eststo v4 :  xi: quietly asreg monthlyρ_5_f /*NMFCA  NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership   lowimbalancestd    i.PairType  if sbgroup==1  , fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "SameGroup" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "No" , replace
	
			eststo v5 :  xi: quietly asreg monthlyρ_5_f /*NMFCA  NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership   lowimbalancestd    i.PairType if sbgroup==0  , fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Others" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "No" , replace

		eststo v6 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup  /*gsize_y gsize_x*/ i.PairType gdummy0-gdummy47, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "Yes" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace


				esttab   v1 v2 v4 v5 v3 v6  /*v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup  /*ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA insimbalance_value_x insimbalance_value_y yy*/) order(/*NMFCA */ sbgroup lowimbalancestd /*ImbalanceSbgroup NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCAinsimbalance_value_x insimbalance_value_y yy*/) s( /*GroupSizeFE*/ subsample GroupFE      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" "Business Group FE" "Observations"))compress mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) 

	/**/
	
}


	
	
				esttab   v1 v2 v4 v5 v3 v6  /*v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup  /*ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA insimbalance_value_x insimbalance_value_y yy*/) order(/*NMFCA */ sbgroup lowimbalancestd /*ImbalanceSbgroup NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCAinsimbalance_value_x insimbalance_value_y yy*/) s( /*GroupSizeFE*/ subsample GroupFE      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" "Business Group FE" "Observations"))  /*prehead("{\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi} \begin{tabular}{l*{6}{c}} \hline   \addlinespace[1ex]  \multicolumn{7}{c}{Panel B: Low Imbalance std groups and Comovement } \\   \addlinespace[1ex] \hline  \addlinespace[1ex]") */mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Imbalance.tex ,replace
				
				
				
	esttab   v1 v2 v4 v5 v3 v6  /*v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership  _cons ) order(sbgroup lowimbalancestd ImbalanceSbgroup) s( /*GroupSizeFE*/ subsample GroupFE      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" "Business Group FE" "Observations"))  mgroups("Dependent Variable:  Future Pairs's Comovement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Imbalance-Appendix.tex ,replace

summ  sbgroup lowimbalancestd ImbalanceSbgroup
 corr sbgroup lowimbalancestd ImbalanceSbgroup







