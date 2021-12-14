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
	

	esttab    v1 v2 v3 v4 /*v5*/ v6 v61   ,nomtitle label   s(  /*SubSample GroupFE*/ controll Pairtypr N  /*r2*/ ,  lab(/*"Sub-sample" "Group Effect"*/ "Controls" "PairType Control" "Observations"  /*"$ R^2 $"*/))   keep(NMFCA sbgroup) compress order(NMFCA sbgroup     ) mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) 
		
	esttab v10 v11 /*v7*/ v8 v9 ,nomtitle label   s( SubSample GroupFE /*controll*/ N /*Pairtypr r2*/ ,  lab( "Sub-sample" "Business Group FE" "Observations" /*"Controls" "PairType Control" "$ R^2 $"*/))   keep(NMFCA sbgroup NMFCAG) compress order(NMFCA sbgroup     ) mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )
 	

	
	
}




	esttab    v1 v2 v3 v4 /*v5*/ v6 v61   ,nomtitle label   s(  /*SubSample GroupFE*/ controll Pairtypr N  /*r2*/ ,  lab(/*"Sub-sample" "Group Effect"*/ "Controls" "PairType Control" "Observations"  /*"$ R^2 $"*/))   keep(NMFCA sbgroup) compress order(NMFCA sbgroup     ) mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using mresult2part1-slide.tex ,replace
		esttab v10 v11 /*v7*/ v8 v9 ,nomtitle label   s( SubSample GroupFE /*controll*/ N /*Pairtypr r2*/ ,  lab( "Sub-sample" "Business Group FE" "Observations" /*"Controls" "PairType Control" "$ R^2 $"*/))   keep(NMFCA sbgroup NMFCAG) compress order(NMFCA sbgroup     ) mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ), using mresult2part2-slide.tex ,replace



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

	eststo v0: quietly asreg monthlyρ_5_f  sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership if forthquarter == 1 , fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "All" , replace

	eststo v1: quietly asreg monthlyρ_5_f NMFCA sgroup monthlysamesize monthlysamebm monthlycrossownership if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "All" , replace
	
		eststo v11: quietly asreg monthlyρ_5_f NMFCA sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership if forthquarter == 1, fmb newey(4)
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
	/*
	eststo v21: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType  if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace

	eststo v3: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType gdummy0-gdummy47 if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	*/
	eststo v21: xi: quietly asreg monthlyρ_5_f NMFCA   sgroup monthlysamesize monthlysamebm monthlycrossownership if (forthquarter == 1) & (sbgroup == 1 ), fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "SameGroup" , replace
	
		eststo v3: xi: quietly asreg monthlyρ_5_f NMFCA   sgroup monthlysamesize monthlysamebm monthlycrossownership if (forthquarter == 1) & (sbgroup == 0 ), fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace
	estadd loc Control "Yes" , replace
	estadd loc SubSample "Others" , replace
	




esttab   v0 v1 v11/* v111   v2*/ v21 v3 , nomtitle label   s( SubSample Control GroupFE /*Pairtypr*/ N  /*r2*/ ,  lab("Sub-sample" "Controls" "Business Group FE" "Observations" /*"PairType Control" "$ R^2 $"*/))  keep(sbgroup NMFCA  /*NMFCAG*/) order(sbgroup NMFCA  NMFCAG  ) compress mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))


}

esttab   v0 v1 v11 /*v111   v2*/ v21 v3 , nomtitle label   s( SubSample Control GroupFE /*Pairtypr*/ N  /*r2*/ ,  lab("Sub-sample" "Controls" "Business Group FE" "Observations" /*"PairType Control" "$ R^2 $"*/))  keep(sbgroup NMFCA  /*NMFCAG*/) order(sbgroup NMFCA  NMFCAG  ) compress mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using QTimemresult2subsample-slide.tex ,replace

/* Turn over*/

{
	eststo clear

	eststo v1: quietly asreg monthlyρ_turn_f  NMFCA  , fmb newey(4)
	estadd loc GroupFE "All" , replace
	estadd loc controll "No" , replace

	eststo v2: quietly asreg monthlyρ_turn_f NMFCA monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "All" , replace
	estadd loc controll "Yes" , replace


	eststo v3: quietly asreg monthlyρ_turn_f  sbgroup  , fmb newey(4)
	estadd loc GroupFE "All" , replace
	estadd loc controll "No" , replace

	eststo v4: quietly asreg monthlyρ_turn_f sbgroup  monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "All" , replace
	estadd loc controll "Yes" , replace

/*
	eststo v5: quietly asreg monthlyρ_turn_f NMFCA sbgroup , fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
*/
	eststo v6: quietly asreg monthlyρ_turn_f NMFCA sbgroup monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
	estadd loc GroupFE "All" , replace
	estadd loc controll "Yes" , replace
/*
	eststo v7: quietly asreg monthlyρ_turn_f NMFCA sbgroup NMFCAG, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc controll "No" , replace
*/
	eststo v8: quietly asreg monthlyρ_turn_f NMFCA   monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1 , fmb newey(4)
	estadd loc GroupFE "SameGroup" , replace
	estadd loc controll "Yes" , replace


	eststo v9: quietly asreg monthlyρ_turn_f NMFCA   monthlyρ_turn sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 0 , fmb newey(4)
	estadd loc GroupFE "Others" , replace
	estadd loc controll "Yes" , replace



	esttab   v3 v4 v1 v2 /*v5*/ v6 /*v7*/ v8 v9 ,nomtitle label   s( controll GroupFE  N   ,  lab("Controls" "Sub-sample" "Observations"   ))   keep(NMFCA sbgroup ) compress order(sbgroup NMFCA   )  mgroups("Dependent Variable:  Future Monthly Correlation of Delta turnover"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )
	


}
	
		esttab   v3 v4 v1 v2 /*v5*/ v6 /*v7*/ v8 v9 ,nomtitle label   s( controll GroupFE  N   ,  lab("Controls" "Sub-sample" "Observations"   ))   keep(NMFCA sbgroup ) compress order(sbgroup NMFCA   )  mgroups("Dependent Variable:  Future Monthly Correlation of Delta turnover"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using mresult2-turnover.tex ,replace


{/* Imbalance*/
	


	eststo v1 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup   i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "No" , replace

	eststo v2 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd gsize_y gsize_x  i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace

	eststo v3 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup  gsize_y gsize_x i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace
	
	
	
		eststo v7 :  xi: quietly asreg monthlyρ_5_f /*NMFCA  NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership   lowimbalancestd    i.PairType  if sbgroup==1  , fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "SameGroup" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "No" , replace
	
			eststo v8 :  xi: quietly asreg monthlyρ_5_f /*NMFCA  NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership   lowimbalancestd    i.PairType if sbgroup==0  , fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Others" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "No" , replace



				esttab   v1 v2 v7 v8  /*v3 v6 v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd /*ImbalanceSbgroup ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA insimbalance_value_x insimbalance_value_y yy*/) order(/*NMFCA */ sbgroup lowimbalancestd /*ImbalanceSbgroup NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCAinsimbalance_value_x insimbalance_value_y yy*/) s( /*GroupSizeFE*/ subsample /*GroupFE*/      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" /*"Business Group FE"*/ "Observations"))compress mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )

	/**/
	
}

		esttab   v1 v2 v7 v8  /*v3 v6 v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd /*ImbalanceSbgroup ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA insimbalance_value_x insimbalance_value_y yy*/) order(/*NMFCA */ sbgroup lowimbalancestd /*ImbalanceSbgroup NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCAinsimbalance_value_x insimbalance_value_y yy*/) s( /*GroupSizeFE*/ subsample /*GroupFE*/      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" /*"Business Group FE"*/ "Observations"))compress mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Imbalance.tex ,replace

summ  sbgroup lowimbalancestd ImbalanceSbgroup
 corr sbgroup lowimbalancestd ImbalanceSbgroup



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
	estadd loc subsample "SameGroup" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	estadd loc GroupSizeFE "Yes" , replace
	
	
	
	
esttab   v1 v2  v7 v8 /*v3 v6 */, nomtitle  label  keep(/*NMFCA */ sbgroup lowres /*Grouplowres  trunresstd_x trunresstd_y xx */) order(/*NMFCA */ sbgroup lowres /*Grouplowres NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA trunresstd_x trunresstd_y xx*/ ) s( /*GroupSizeFE*/ subsample /*GroupFE*/      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" /*"Business Group FE"*/ "Observations")) compress mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
}

esttab   v1 v2  v7 v8 /*v3 v6 */, nomtitle  label  keep(/*NMFCA */ sbgroup lowres /*Grouplowres  trunresstd_x trunresstd_y xx */) order(/*NMFCA */ sbgroup lowres /*Grouplowres NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA trunresstd_x trunresstd_y xx*/ ) s( /*GroupSizeFE*/ subsample /*GroupFE*/      N  ,  lab( /*"Group Size Effect"*/ "Sub-sample" /*"Business Group FE"*/ "Observations")) compress mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span})),using LowRes.tex ,replace


corr sbgroup lowres Grouplowres

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


eststo v3 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "SameGroup" , replace
estadd loc GroupFE "No" , replace



eststo v4 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 0, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Others" , replace
estadd loc GroupFE "No" , replace


/*eststo v2 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f sbgroup , fmb newey(4)
estadd loc controll "No" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace
*/

eststo v3 : quietly asreg monthlyρ_5_f monthlyρ_5 monthlyρ_turn_f sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc subsample "Total" , replace
estadd loc GroupFE "No" , replace

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



esttab   v1 v2 v3 v4 v5 /*v6 v7*/, nomtitle  label  keep(monthlyρ_turn_f monthlyρ_5 /*sbgroup turnSbgroup*/ ) order(monthlyρ_turn_f) s( controll subsample   GroupFE   N  ,  lab( "Control" "Sub-sample" "Business Group FE" "Observations")) compress mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))


 


}

esttab   v1 v2 v3 v4 v5 /*v6 v7*/, nomtitle  label  keep(monthlyρ_turn_f monthlyρ_5 /*sbgroup turnSbgroup*/ ) order(monthlyρ_turn_f) s( controll subsample   GroupFE   N  ,  lab( "Control" "Sub-sample" "Business Group FE" "Observations")) compress mgroups("Dependent Variable:  Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))  ,using turncomovement.tex ,replace



