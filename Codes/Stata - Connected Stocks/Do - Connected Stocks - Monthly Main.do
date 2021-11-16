/*NMFCA*/
{
	eststo clear

	eststo v1: quietly asreg monthlyρ_5_f  NMFCA , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace
	

	eststo v2: quietly asreg monthlyρ_5_f NMFCA  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace

	eststo v3: quietly asreg monthlyρ_5_f  sbgroup  , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace

	eststo v4: quietly asreg monthlyρ_5_f sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace


	eststo v5: quietly asreg monthlyρ_5_f NMFCA sbgroup , fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace

	eststo v6: quietly asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace
	
	eststo v61: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "Yes" , replace
	

	eststo v7: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "No" , replace

	eststo v8: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "Yes" , replace


	eststo v9: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 i.PairType , fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "Yes" , replace
	
	eststo v91: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 i.PairType, fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "All" , replace
	estadd loc Pairtypr "Yes" , replace



	eststo v10: xi: quietly asreg monthlyρ_5_f NMFCA     sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if sbgroup == 1 , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "SameGroup" , replace
	estadd loc Pairtypr "Yes" , replace
	
	eststo v11: xi: quietly asreg monthlyρ_5_f NMFCA    sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType  if sbgroup == 0, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "Yes" , replace
	estadd loc SubSample "Others" , replace
	estadd loc Pairtypr "Yes" , replace
	

	esttab    v1 v2 v3 v4 /*v5*/ v6 v61   ,nomtitle label   s( N  SubSample GroupFE controll Pairtypr r2 ,  lab("Observations" "Sub-sample" "Group Effect" "Controls" "PairType Control" "$ R^2 $"))   keep(NMFCA sbgroup) compress order(NMFCA sbgroup     ) mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) 	,using mresult2part1-slide.tex ,replace
	
	
	esttab v10 v11 /*v7*/ v8 v9 v91,nomtitle label   s( N  SubSample GroupFE controll Pairtypr r2 ,  lab("Observations" "Sub-sample" "Group Effect" "Controls" "PairType Control" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(NMFCA sbgroup     ) mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	, using mresult2part2-slide.tex ,replace
	
	
}

{ /*Define Q3*/
	replace median = 0 if forthquarter != 1
	replace median = 1 if forthquarter == 1

	replace NMFCAM = NMFCA * median

	label variable NMFCAM " $ (\text{MFCAP} > Q3[\text{MFCAP}]) \times {\text{MFCAP} ^*}  $ "

	replace sbgroupM = sbgroup * median
	label variable sbgroupM " $ (\text{MFCAP} > Q3[\text{MFCAP}]) \times {\text{SameGroup}} $ "



	replace NMFCAGM = sbgroup * NMFCA * median
	label variable NMFCAGM " $ (\text{MFCAP} > Q3[\text{MFCAP}]) \times  (\text{MFCAP}^*) \times {\text{SameGroup}} $ "


	replace holder_actM = holder_act * median
	label variable holder_actM " $ (\text{MFCAP}> Q3[\text{MFCAP}]) \times {\text{ActiveHolder} }  $ "

	replace spositionM = sposition * median

	label variable spositionM " $ (\text{MFCAP}> Q3[\text{MFCAP}]) \times {\text{Same Position} }  $ "


	corr monthlyρ_5_f monthlyρ_5  NMFCA median NMFCAM   NMFCAG NMFCAGM sbgroup  sgroup monthlysamesize monthlysamebm 


}


{/*NMFCA Just after Q3*/

	eststo v0: xi: quietly asreg monthlyρ_5_f  sbgroup i.PairType if forthquarter == 1 , fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v1: xi: quietly asreg monthlyρ_5_f NMFCA  i.PairType if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace


	eststo v11: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup i.PairType if forthquarter == 1, fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v111: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup sgroup i.PairType if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v2: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType  if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v21: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType  if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v3: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType gdummy0-gdummy47 if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc Pairtypr "Yes" , replace




esttab   v0 v1 v11 v111   v2 v21 v3 , nomtitle label   s( N GroupFE Pairtypr r2 ,  lab("Observations" "Group FE" "PairType Control" "$ R^2 $"))  keep(NMFCA sbgroup NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership ) order(sbgroup NMFCA  NMFCAG sgroup ) compress mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using QTimemresult2subsample-slide.tex ,replace
}



/* Turn over*/

{
	eststo clear

	eststo v1: quietly asreg monthlyρ_turn_f  NMFCA  , fmb newey(4)
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

}


/*BigBusiness group*/
{
eststo clear

eststo v1: xi: quietly asreg monthlyρ_5_f monthlyρ_5 /*NMFCA*/ sbgroup /*NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn i.PairType, fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc FE "Yes" , replace
estadd loc subsample "All" , replace



eststo v2: xi: quietly asreg monthlyρ_5_f /*NMFCA*/ monthlyρ_5 sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn i.PairType  bigbusinessgroup  /*NMFCAG*/ bigbusinessgroupTurn Turnsbgroup TurnSgroupbigbusinessgroup bigbusinessgroupSgroup, fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample "All" , replace
estadd loc FE "Yes" , replace



eststo v3: xi: quietly asreg monthlyρ_5_f /*NMFCA*/ monthlyρ_5 sbgroup /*NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn Turnsbgroup i.PairType  if bigbusinessgroup == 1, fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample "Big Groups" , replace
estadd loc FE "Yes" , replace



eststo v4: xi: quietly asreg monthlyρ_5_f /*NMFCA*/ monthlyρ_5 sbgroup /*NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership Turnsbgroup monthlyρ_turn i.PairType if bigbusinessgroup  == 0, fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample "Others" , replace
estadd loc FE "Yes" , replace


eststo v5: xi: quietly asreg monthlyρ_5_f /*NMFCA*/ monthlyρ_5 sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn i.PairType    /*NMFCAG*/  Turnsbgroup , fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample "All" , replace
estadd loc FE "Yes" , replace

esttab v1 v5 v2 v3 v4 ,nomtitle label   s( N Controls FE subsample r2 ,  lab("Observations" "Controls" "Pari Size FE" "SubSample" "$ R^2$"))   keep(/*NMFCA*/ sbgroup /*NMFCAG*/ bigbusinessgroup /*  bigbusinessgroupFCA*/ bigbusinessgroupSgroup /*bigbusinessgroupSgroupFCA */ monthlyρ_turn monthlyρ_5 bigbusinessgroupTurn Turnsbgroup TurnSgroupbigbusinessgroup ) compress order(sbgroup /*NMFCA  NMFCAG*/ monthlyρ_turn monthlyρ_5 Turnsbgroup  bigbusinessgroup bigbusinessgroupSgroup  bigbusinessgroupTurn TurnSgroupbigbusinessgroup) 



esttab v1 v5 v2 v3 v4 ,nomtitle label   s( N Controls FE subsample r2 ,  lab("Observations" "Controls" "Pari Size FE" "SubSample" "$ R^2$"))   keep(/*NMFCA*/ sbgroup /*NMFCAG*/ bigbusinessgroup /*  bigbusinessgroupFCA*/ bigbusinessgroupSgroup /*bigbusinessgroupSgroupFCA */ monthlyρ_turn monthlyρ_5 bigbusinessgroupTurn Turnsbgroup TurnSgroupbigbusinessgroup ) compress order(sbgroup /*NMFCA  NMFCAG*/ monthlyρ_turn monthlyρ_5 Turnsbgroup  bigbusinessgroup bigbusinessgroupSgroup  bigbusinessgroupTurn TurnSgroupbigbusinessgroup)  mgroups("Dependent Variable: Future Pairs's co-movement"  , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-BigBusinessGroup.tex ,replace
}



{/* Imbalance*/
	


	eststo v1 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup   i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace

	eststo v2 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd   i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace

	eststo v3 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup  i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	
	eststo v6 :  xi: quietly asreg monthlyρ_5_f /*NMFCA  NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup   i.PairType gdummy0-gdummy47  , fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "Yes" , replace
	estadd loc FE "Yes" , replace
	

	
	
	esttab   v1 v2 v3 v6 /* v7 v8 v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA*/ ) order(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA*/) s( N GroupFE FE  subsample controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )


	esttab   v1 v2 v3 v6 /* v7 v8 v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA*/ ) order(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA*/) s( N GroupFE FE  subsample controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Imbalance.tex ,replace

	/**/
	
}

 

 
 { /*Iv estimation*/
 

xtset t_month id

eststo v1 : quietly xtreg monthlyρ_5_f monthlyρ_5 sbgroup  monthlycrossownership sgroup  monthlysamesize monthlysamebm  i.PairType gdummy0-gdummy47 ,fe robust
estadd loc FE "Yes" , replace
estadd loc lag "Yes" , replace
estadd loc method "FE" , replace
estadd loc Group "Yes" , replace


eststo v2 : quietly xtreg monthlyρ_turn_f sbgroup monthlyρ_turn   sgroup  monthlysamesize monthlysamebm monthlycrossownership  i.PairType gdummy0-gdummy47,fe robust
estadd loc FE "Yes" , replace
estadd loc lag "Yes" , replace
estadd loc method "FE" , replace
estadd loc Group "Yes" , replace

eststo v3 : quietly xtivreg monthlyρ_5_f sbgroup monthlyρ_5  monthlysamesize monthlysamebm monthlycrossownership i.PairType gdummy0-gdummy47 (monthlyρ_turn_f = sgroup)  , fe 
estadd loc FE "Yes" , replace
estadd loc lag "Yes" , replace
estadd loc method "2sls" , replace
estadd loc Group "Yes" , replace

esttab v2 v1  v3 , label s( N method Group FE lag r2,  lab("Observations" "Method" "Group FE" "Pair Size Control" "Lag of Dep. Var." "$ R^2$ "))keep( sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn_f) nomtitle   order(sgroup monthlyρ_turn_f) mgroups("First Stage" "Reduced form" "Second Stage" , pattern(1 1  1)),using TurnIv.tex ,replace



corr sbgroup  sgroup

xtset id t_month  
 }
 
 
 
 xtivreg monthlyρ_turn_f  sbgroup monthlyρ_turn  monthlysamesize monthlysamebm monthlycrossownership i.PairType gdummy0-gdummy47 ( monthlyρ_5_f = sgroup)  , fe 