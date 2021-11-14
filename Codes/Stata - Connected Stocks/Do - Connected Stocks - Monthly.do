
asreg monthlyρ_4_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership if monthlyρ_5_f != 1 & monthlyρ_5_f != -1, fmb newey(4)

gen xxx = ln(monthlyρ_5_f/(1-monthlyρ_5_f))

asreg xxx NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)



eststo v1: asreg monthlyρ_5_f NMFCAP  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
eststo v2: asreg monthlyρ_5_f NMFCA   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

eststo v3: asreg monthlyρ_5_f NMFCAP NMFCAPG  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
eststo v4: asreg monthlyρ_5_f NMFCA NMFCAG sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

esttab v1 v2 v3 v4 

summ MFCA monthlyfcapf

cor NMFCA NMFCAP sbgroup NMFCAG NMFCAPG

/*

eststo v0 : asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)


eststo v1 :asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm  , fmb newey(4) 

 
esttab v0 v1 


eststo v0 : xtfmb monthlyρlag_5_f NMFCA monthlyρlag_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm , lag(4) 

eststo v1 : xtfmb monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm , lag(4) 

eststo v2 : xtfmb monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm , lag(4) 

eststo v3 : xtfmb monthlyρ_5 NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm , lag(4) 


esttab v0 v1 v2 v3

asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm  if sbgroup == 1   , fmb newey(4)  


asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5   sgroup monthlysamesize monthlysamebm  if sbgroup == 1   , fmb newey(4)  

binscatter monthlyρ_5_f NMFCA if sbgroup == 1 , n(100) rd(0)




asreg monthlyρ_5_f NMFCA  monthlyρ_5 Up Down sDown sUp sgroup monthlysamesize monthlysamebm ,  fmb newey(4) first  save(FirstStage)

*/

cor monthlyρ_5_f NMFCA median NMFCAM NMFCAG NMFCAGM sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5



/**/




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
/*Quadratic*/
{
/*NMFCA*/
// eststo clear
//
// eststo v1: quietly asreg monthlyρ_5_f  NMFCA2 , fmb newey(4)
// estadd loc GroupFE "No" , replace
// estadd loc controll "No" , replace
//
// eststo v2: quietly asreg monthlyρ_5_f NMFCA2 monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
// estadd loc GroupFE "No" , replace
// estadd loc controll "Yes" , replace
//
//
// eststo v3: quietly asreg monthlyρ_5_f  sbgroup  , fmb newey(4)
// estadd loc GroupFE "No" , replace
// estadd loc controll "No" , replace
//
// eststo v4: quietly asreg monthlyρ_5_f sbgroup  monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
// estadd loc GroupFE "No" , replace
// estadd loc controll "Yes" , replace
//
//
// eststo v5: quietly asreg monthlyρ_5_f NMFCA2 sbgroup , fmb newey(4) 
// estadd loc GroupFE "No" , replace
// estadd loc controll "No" , replace
//
// eststo v6: quietly asreg monthlyρ_5_f NMFCA2 sbgroup monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
// estadd loc GroupFE "No" , replace
// estadd loc controll "Yes" , replace
//
// eststo v7: quietly asreg monthlyρ_5_f NMFCA2 sbgroup NMFCAG, fmb newey(4)
// estadd loc GroupFE "No" , replace
// estadd loc controll "No" , replace
//
// eststo v8: quietly asreg monthlyρ_5_f NMFCA2 sbgroup NMFCAG monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
// estadd loc GroupFE "No" , replace
// estadd loc controll "Yes" , replace
//
//
// eststo v9: quietly asreg monthlyρ_5_f NMFCA2 sbgroup NMFCAG monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
// estadd loc GroupFE "Yes" , replace
// estadd loc controll "Yes" , replace
//
//
//
// esttab  v1 v2 v3 v4 v5 v6 v7 v8 v9 ,nomtitle label   s( N GroupFE controll r2 ,  lab("Observations" "Group Effect" "Controls" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(NMFCA sbgroup NMFCAG ) 
//
//
// mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Quadraticmresult2-slide.tex ,replace
//
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
	

	/*
	eststo v4 :  xi: quietly asreg monthlyρ_5_f NMFCA   NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA lowimbalancestdFCA  i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	
	eststo v5 :  xi: quietly asreg monthlyρ_5_f NMFCA  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA lowimbalancestdFCA gdummy0-gdummy47  i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "Yes" , replace
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
	*/
	
	esttab   v1 v2 v3 v6 /* v7 v8 v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA*/ ) order(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA*/) s( N GroupFE FE  subsample controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )


	esttab   v1 v2 v3 v6 /* v7 v8 v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA*/ ) order(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA*/) s( N GroupFE FE  subsample controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Imbalance.tex ,replace

	/**/
	
}

 



/*Bullish/Bearish */

{ 
eststo v1: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType, fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample  "Total" , replace
estadd loc FE "Yes" , replace
estadd loc method "FM" , replace

eststo v2: xi: quietly asreg monthlyρ_5_f NMFCA   NMFCAG bearish bullish   sDown sUp  sgroup monthlysamesize monthlysamebm monthlycrossownership sbgroup i.PairType, fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample  "Total" , replace
estadd loc FE "Yes" , replace
estadd loc method "FM" , replace

eststo v3: xi: quietly asreg monthlyρ_5_f NMFCA NMFCAG   Up Down sDown sUp DownFCA UpFCA sgroup monthlysamesize monthlysamebm monthlycrossownership  bearish bullish sbgroup i.PairType, fmb newey(4)
estadd loc Controls "Yes" , replace 
estadd loc subsample  "Total" , replace
estadd loc FE "Yes" , replace
estadd loc method "FM" , replace

eststo v4: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if bearish == 1 , fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample  "Bearish Market" , replace
estadd loc FE "Yes" , replace
estadd loc method "FM" , replace

eststo v5: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if bullish == 1 , fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample  "Bullish Market" , replace
estadd loc FE "Yes" , replace
estadd loc method "FM" , replace

eststo v6: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if bullish == 0 & bullish ==0 , fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample  "Normal Market" , replace
estadd loc FE "Yes" , replace
estadd loc method "FM" , replace



eststo v7: xtreg monthlyρ_5_f NMFCA NMFCAG   Up Down sDown sUp DownFCA UpFCA sgroup monthlysamesize monthlysamebm monthlycrossownership  bearish bullish  , fe
estadd loc Controls "Yes" , replace
estadd loc subsample  "All" , replace
estadd loc FE "No" , replace
estadd loc method "FE" , replace

esttab v1 v2 v3 v4 v5 v6 v7, nomtitle label  s( N Controls FE subsample method r2 ,  lab("Observations" "Controls" "Pari Size FE" "SubSample" "Method" "$ R^2$"))  keep(NMFCA NMFCAG sDown Down Up sUp  DownFCA UpFCA sbgroup bearish bullish ) order(sbgroup NMFCA NMFCAG bearish bullish   sDown sUp DownFCA UpFCA ) n r2    compress  mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals", pattern(1)  prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span})) ,using mresult2Down-slide2.tex ,replace

}




/*NMFCA Just after Q2*/

{eststo v0: quietly asreg monthlyρ_5_f  NMFCA if median == 1 , fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 if median == 1, fmb newey(4)
estadd loc GroupFE "No" , replace


eststo v11: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sgroup if median == 1, fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v111: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup sgroup if median == 1, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership if median == 1, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 if median == 1, fmb newey(4)
estadd loc GroupFE "Yes" , replace




esttab   v0 v1 v11 v111   v2 v3 , nomtitle label   s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $"))  keep(NMFCA monthlyρ_5 sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership ) order(NMFCA sbgroup) compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Qmresult2subsanple-slide.tex ,replace

}




/*NMFCAMQ3*/
{ 
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





eststo v00: quietly asreg monthlyρ_5_f NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v0: quietly asreg monthlyρ_5_f  NMFCA NMFCAM , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v11: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 sbgroup  , fmb newey(4) 
estadd loc GroupFE "No" , replace


eststo v2: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership  gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace


esttab v00 v0 v1 v11   v2 v3, nomtitle label s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $")) keep(NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership) order(NMFCA NMFCAM sbgroup) compress mgroups("Dep. Variable: Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Qmresult2-slide.tex ,replace


/**/


eststo v0: quietly  asreg monthlyρ_5_f  NMFCA NMFCAM sbgroup     sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 


eststo v1: quietly  asreg monthlyρ_5_f  NMFCA NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 


eststo v11: quietly  asreg monthlyρ_5_f  NMFCA NMFCAGM  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 


eststo v2: quietly  asreg monthlyρ_5_f  NMFCA NMFCAM NMFCAG    sbgroup     sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 


 eststo v3: quietly  asreg monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 

 eststo v4: quietly  asreg monthlyρ_5_f NMFCA  NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 
 

 eststo v5: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 
 
 
 

esttab   v0 v1 v11 v2  v4 v5 v3   , nomtitle label  r2 n compress  keep(NMFCA NMFCAM NMFCAG NMFCAGM) mgroups("Dep. Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using Qmresult3-slide.tex ,replace

esttab   v0 v1 v2  v4 v3   , nomtitle label  r2 n   keep(NMFCA NMFCAM NMFCAG NMFCAGM    ) compress addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (four lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Qmresult3.tex ,replace




/**/


eststo v00: quietly asreg monthlyρ_5_f NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v0: quietly asreg monthlyρ_5_f  NMFCA NMFCAM , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v11: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 sbgroup  , fmb newey(4) 
estadd loc GroupFE "No" , replace


eststo v2: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership  gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace


esttab v00 v0 v1 v11   v2 v3, nomtitle label s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $")) keep(NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership) order(NMFCA NMFCAM sbgroup) compress  mgroups("Dep. Variable: Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using QTimemresult2-slide.tex ,replace


/**/

/*
eststo v0: quietly  asreg monthlyρ_5_f  NMFCA NMFCAM sbgroup     sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 


eststo v1: quietly  asreg monthlyρ_5_f  NMFCA NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 


eststo v11: quietly  asreg monthlyρ_5_f  NMFCA NMFCAGM  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 


eststo v2: quietly  asreg monthlyρ_5_f  NMFCA NMFCAM NMFCAG    sbgroup     sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 


 eststo v3: quietly  asreg monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 

 eststo v4: quietly  asreg monthlyρ_5_f NMFCA  NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 
 

 eststo v5: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 
 
 
 

esttab   v0 v1 v11 v2  v4 v5 v3   , nomtitle label  r2 n compress  keep(NMFCA NMFCAM NMFCAG NMFCAGM) mgroups("Dep. Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using QTimemresult3-slide.tex ,replace
*/

}
{/*NMFCA Just after Q3*/


	eststo v0: xi: quietly asreg monthlyρ_5_f  sbgroup i.PairType if forthquarter == 1 , fmb newey(4) 
	estadd loc GroupFE "No" , replace
		estadd loc Pairtypr "Yes" , replace

	eststo v1: xi: quietly asreg monthlyρ_5_f NMFCA i.PairType if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v11: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup i.PairType if forthquarter == 1, fmb newey(4) 
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v111: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup sgroup i.PairType if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v2: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v21: xi: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Pairtypr "Yes" , replace

	eststo v3: xi: quietly asreg monthlyρ_5_f NMFCA  sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 i.PairType if forthquarter == 1, fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc Pairtypr "Yes" , replace




	esttab   v0 v1 v11 v111   v2 v21 v3 , nomtitle label   s( N GroupFE Pairtypr r2 ,  lab("Observations" "Group FE" "PairType Control" "$ R^2 $"))  keep(NMFCA sbgroup NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership ) order(sbgroup NMFCA  NMFCAG sgroup ) compress mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using QTimemresult2subsample-slide.tex ,replace
}




/*BigSmall*/


{ eststo v0: quietly  asreg monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc SubSample "All Firms" , replace
estadd loc FE "No" , replace

 eststo Bv0: quietly  asreg monthlyρ_5_f NMFCA  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership  if PairType == 2, fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc SubSample "Large Firms" , replace
estadd loc FE "No" , replace

 eststo Bv1: quietly  asreg monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership  if PairType == 2, fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc SubSample "Large Firms" , replace
estadd loc FE "No" , replace

 eststo Sv0: quietly  asreg monthlyρ_5_f NMFCA  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership  if PairType == 1, fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc SubSample "Small Firms" , replace
estadd loc FE "No" , replace

 eststo Sv1: quietly  asreg monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership  if PairType == 1, fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc SubSample "Small Firms" , replace
estadd loc FE "No" , replace

 eststo SBv0: quietly  asreg monthlyρ_5_f NMFCA  sbgroup    sgroup monthlysamesize monthlysamebm monthlycrossownership  if PairType == 0, fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc SubSample "Hybrid Firms" , replace
estadd loc FE "No" , replace

 eststo SBv1: quietly  asreg monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership  if PairType == 0, fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc SubSample "Hybrid Firms" , replace
estadd loc FE "No" , replace

eststo v1: xi: quietly  asreg monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType , fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc SubSample "All Firms" , replace
estadd loc FE "Yes" , replace

/*
eststo v1: quietly asreg monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm  monthlycrossownership  , fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

 eststo v2: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4) 

 eststo Bv0: quietly  asreg monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm  monthlycrossownership   if PairType == 2, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Bv1: quietly asreg monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm monthlycrossownership  if PairType == 2 , fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo Bv2: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup holder_act  sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5 if PairType == 2  , fmb newey(4) 


 eststo Sv0: quietly  asreg monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm  monthlycrossownership  if PairType == 1, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Sv1: quietly asreg monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm  monthlycrossownership   if PairType == 1 , fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo Sv2: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership   if PairType == 1  , fmb newey(5) 



eststo SBv0: quietly  asreg monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm  monthlycrossownership   if PairType == 0 , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo SBv1: quietly asreg monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm  monthlycrossownership   if PairType == 0 , fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo SBv2: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership    if PairType == 0  , fmb newey(4) 
*/

/*
esttab v0 /*v1 v2*/ Bv0 /*Bv1 Bv2*/ SBv0 /*SBv1 SBv2*/ Sv0 /*Sv1 Sv2*/ v1  , nomtitle label n r2  compress order(NMFCA NMFCAG NMFCAM    NMFCAGM sbgroup sgroup) keep(NMFCA NMFCAM sbgroup  NMFCAG  NMFCAGM sgroup)  mgroups("All Firms" "Big Firms" "Big \& Small Firms" "Small Firms"   , pattern(1 0 0 1 0 0 1 0 0 1 0 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	,using Qmresult4-slide.tex ,replace 
*/

esttab v0 Bv0 Bv1  SBv0 SBv1 Sv0 Sv1 v1  , nomtitle label  s( N Controls  SubSample FE r2 ,  lab("Observations" "Controls" "Sub-sample" "Pair Size FE" "$ R^2 $"))   compress order(sbgroup NMFCA  NMFCAG  FE) keep(NMFCA  sbgroup  NMFCAG  ) mgroups("Dependent Variable: Future Monthly Correlation of 4F+Ind. Res."   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Qmresult4-slide.tex ,replace 

}




/* Turn over*/

{
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



esttab   v3 v4 v1 v2 /*v5*/ v6 /*v7*/ v8 v9 ,nomtitle label   s( N GroupFE controll r2 ,  lab("Observations" "Group Effect" "Controls" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(sbgroup NMFCA  NMFCAG )  mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-turnover.tex ,replace

}


/*HighBeta*/

{
	eststo v1 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup   i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace

	eststo v2 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */     sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup highbeta   i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace

	eststo v3 :  xi: quietly asreg monthlyρ_5_f /*NMFCA */    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup highbeta Grouphighbeta  i.PairType, fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "No" , replace
	estadd loc FE "Yes" , replace
	
	eststo v6 :  xi: quietly asreg monthlyρ_5_f /*NMFCA  NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup highbeta Grouphighbeta   i.PairType gdummy0-gdummy47  , fmb newey(4)
	estadd loc controll "Yes" , replace
	estadd loc subsample "Total" , replace
	estadd loc GroupFE "Yes" , replace
	estadd loc FE "Yes" , replace
	
	esttab   v1 v2 v3 v6 /* v7 v8 v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup highbeta Grouphighbeta /*ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA*/ ) order(/*NMFCA */ sbgroup highbeta Grouphighbeta /*NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA*/) s( N GroupFE FE  subsample controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )


	esttab   v1 v2 v3 v6 /* v7 v8 v4 v5*/, nomtitle  label  keep(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*ImbalanceSbgroupFCA NMFCAG lowimbalancestdFCA*/ ) order(/*NMFCA */ sbgroup lowimbalancestd ImbalanceSbgroup /*NMFCAG lowimbalancestdFCA ImbalanceSbgroupFCA*/) s( N GroupFE FE  subsample controll r2 ,  lab("Observations" "Group Effect" "Pair Size FE" "Sub-sample" "Controls" "$ R^2 $"))compress mgroups("Dependent Variable: Future Pairs's co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using HighBeta.tex ,replace
}


/*BigBusiness group*/
{
eststo clear

eststo v1: xi: quietly asreg monthlyρ_5_f monthlyρ_5 /*NMFCA*/ sbgroup /*NMFCAG*/ sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn i.PairType, fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc FE "Yes" , replace
estadd loc subsample "All" , replace

/*eststo v2: xi: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn i.PairType  bigbusinessgroup bigbusinessgroupSgroup bigbusinessgroupFCA NMFCAG bigbusinessgroupSgroupFCA, fmb newey(4)
estadd loc Controls "Yes" , replace
estadd loc subsample "All" , replace
estadd loc FE "Yes" , replace*/

eststo v2: xi: quietly asreg monthlyρ_5_f /*NMFCA*/ monthlyρ_5 sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn i.PairType  bigbusinessgroup  /*NMFCAG*/ bigbusinessgroupTurn Turnsbgroup bigbusinessgroupSgroupTurn bigbusinessgroupSgroup, fmb newey(4)
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


esttab v1  v2 v3 v4 ,nomtitle label   s( N Controls FE subsample r2 ,  lab("Observations" "Controls" "Pari Size FE" "SubSample" "$ R^2$"))   keep(/*NMFCA*/ sbgroup /*NMFCAG*/ bigbusinessgroup /*  bigbusinessgroupFCA*/ bigbusinessgroupSgroup /*bigbusinessgroupSgroupFCA */ monthlyρ_turn monthlyρ_5 bigbusinessgroupTurn Turnsbgroup bigbusinessgroupSgroupTurn ) compress order(sbgroup /*NMFCA  NMFCAG*/ monthlyρ_turn monthlyρ_5 Turnsbgroup  bigbusinessgroup bigbusinessgroupSgroup) 



esttab v1  v2 v3 v4 ,nomtitle label   s( N Controls FE subsample r2 ,  lab("Observations" "Controls" "Pari Size FE" "SubSample" "$ R^2$"))   keep(/*NMFCA*/ sbgroup /*NMFCAG*/ bigbusinessgroup /*  bigbusinessgroupFCA*/ bigbusinessgroupSgroup /*bigbusinessgroupSgroupFCA */ monthlyρ_turn monthlyρ_5 bigbusinessgroupTurn Turnsbgroup bigbusinessgroupSgroupTurn ) compress order(sbgroup /*NMFCA  NMFCAG*/ monthlyρ_turn monthlyρ_5 Turnsbgroup  bigbusinessgroup bigbusinessgroupSgroup)  mgroups("Dep. Var.: Future Monthly Cor.  of 4F+Ind. Res."   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-BigBusinessGroup.tex ,replace
}


/*ّFive Lag*/
{
 eststo v0: quietly asreg monthlyρ_5_f  NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc FiveLag "0" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc FiveLag "0" , replace


eststo v11: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sgroup, fmb newey(4) 
estadd loc GroupFE "No" , replace
estadd loc FiveLag "0" , replace

eststo v111: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup sgroup, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc FiveLag "0" , replace

eststo v13: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup NMFCAG sgroup, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc FiveLag "0" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc FiveLag "0" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace
estadd loc FiveLag "0" , replace

eststo v4 : quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 monthlyρ_5_1-monthlyρ_5_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(5)
estadd loc GroupFE "No" , replace
estadd loc FiveLag "5" , replace

eststo v5: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 monthlyρ_5_1-monthlyρ_5_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace
estadd loc FiveLag "5" , replace

esttab   v0 v1 v11 v111   v13  v2 v4  v3 v5, nomtitle label   s( N GroupFE FiveLag r2 ,  lab("Observations" "Group FE" "Number of lag" "$ R^2 $"))  keep(NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership )drop( monthlyρ_5_1 monthlyρ_5_2 monthlyρ_5_3  monthlyρ_5_4 monthlyρ_5_5) order(NMFCA NMFCAG sbgroup) compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )

,using mresult2-5Lag-slide.tex ,replace
}


/*ln(MFCA)*/
{
eststo v0: quietly asreg monthlyρ_5_f  lnMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v1: quietly asreg monthlyρ_5_f lnMFCA  monthlyρ_5 , fmb newey(4) 
estadd loc GroupFE "No" , replace


eststo v11: quietly asreg monthlyρ_5_f lnMFCA  monthlyρ_5 sbgroup, fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v111: quietly asreg monthlyρ_5_f lnMFCA  monthlyρ_5 sbgroup lnMFCAG, fmb newey(4) 
estadd loc GroupFE "No" , replace


eststo v13: quietly asreg monthlyρ_5_f lnMFCA  monthlyρ_5  sbgroup lnMFCAG sgroup, fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v2: quietly asreg monthlyρ_5_f lnMFCA monthlyρ_5  sbgroup lnMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4) 
estadd loc GroupFE "Yes" , replace



esttab   v0 v1 v11 v111     v13  v2 , nomtitle label s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $"))    compress order(lnMFCA lnMFCAG monthlyρ_5  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership) mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using lnmresult2-slide.tex ,replace
}



/*NMFCAP*/
{
	capture drop vv
	capture drop Gvv
	gen vv =   NMFCAP
	gen  Gvv = NMFCAPG
  
	eststo v0: quietly asreg monthlyρ_5_f  vv , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace
	
	eststo v1: quietly asreg monthlyρ_5_f  vv sbgroup, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace
	
	eststo v2: quietly asreg monthlyρ_5_f  vv sbgroup Gvv , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace
	
	eststo v3: quietly asreg monthlyρ_5_f  vv sbgroup Gvv sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Sum" , replace
	
	eststo v4: quietly asreg monthlyρ_5_f  vv sbgroup Gvv sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc Measure "Sum" , replace
	
	replace vv = NMFCA
	replace  Gvv = NMFCAG
	
	eststo v01: quietly asreg monthlyρ_5_f  vv , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Quadratic" , replace
	
	eststo v11: quietly asreg monthlyρ_5_f  vv sbgroup, fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Quadratic" , replace
	
	eststo v21: quietly asreg monthlyρ_5_f  vv sbgroup Gvv , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Quadratic" , replace
	
	eststo v31: quietly asreg monthlyρ_5_f  vv sbgroup Gvv sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
	estadd loc GroupFE "No" , replace
	estadd loc Measure "Quadratic" , replace

	eststo v41: quietly asreg monthlyρ_5_f  vv sbgroup Gvv sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
	estadd loc GroupFE "Yes" , replace
	estadd loc Measure "Quadratic" , replace

	label variable vv "Common Ownership Measure"
	label variable Gvv " $ \text{\small Common Ownership Measure} \times {\text{SameGroup} }$ "

esttab   v0 v01 v1 v11 v2 v21 v3 v31 v4 v41, nomtitle label   s( N GroupFE Measure r2 ,  lab("Observations" "Group FE" "Measurement" "$ R^2 $"))  keep(vv sbgroup Gvv  sgroup monthlysamesize monthlysamebm monthlycrossownership) order(vv sbgroup Gvv) compress   mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Polk-slide.tex ,replace
}
