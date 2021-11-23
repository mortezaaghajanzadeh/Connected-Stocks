{ /*Data*/
		cls
		clear
		import delimited "E:\RA_Aghajanzadeh\Data\Connected_Stocks\MonthlyNormalzedAllFCAP9.2.csv", encoding(UTF-8) 
		// import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\MonthlyNormalzedAllFCAP9.2.csv", encoding(UTF-8) 

		cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Report\Output" 
		// cd "D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report\Output"

		label define sgroup 0 "No" 1 "Yes"

		gen PairType = 0

		summ grank_x

		replace PairType = 1  if grank_x <5 & grank_y<5
		replace PairType = 2  if grank_x >=5 & grank_y>=5

		label define PairType 0 "Hybrid" 1 "Small" 2 "Large"



		label values PairType PairType
		label variable PairType "PairType"

		label values sgroup sgroup
		label variable sgroup "SameIndustry"

		label values sbgroup sgroup
		label variable sbgroup "SameGroup"

		label values sposition sgroup
		label variable sposition "SamePosition"

		gen positiondif = abs(position_x - position_y)

		label variable positiondif "PositionDifference"


		gen positiondif2 = positiondif * sbgroup
		 label variable positiondif2 " $ \text{SameGroup} \times \text{PositionDifference} $ "

		 gen sposition2 = sposition * sbgroup
		  label variable sposition2 " $ \text{SameGroup} \times \text{SamePosition} $"






		label values  sametype sgroup 
		label variable sametype "SameType"
		 

		label values holder_act sgroup 
		label variable holder_act "ActiveHolder"


		label variable monthlysize1 "Size1"
		label variable monthlysize2 "Size2"
		label variable monthlyρ_4_f "ForwardCorr"
		label variable monthlyρ_2 " $ {\rho_t} $ "
		label variable monthlyρ_4 " $ {\rho_t} $ "
		label variable monthlyρ_5 " $ {\rho_t} $ "
		label variable monthlyρ_6 " $ {\rho_t} $ "
		label variable monthlyρlag_5 " $ {\rho_t} $ "



		label variable monthlysamesize "SameSize"

		summarize monthlyfca  monthlyfcap

		rename monthlyfca MFCA

		rename monthlyfcap NMFCAP

		label variable NMFCAP "$ \text{FCAP*} $"

		gen NMFCAPG = sbgroup * NMFCAP

		label variable NMFCAPG " $ (\text{FCAP}^*) \times {\text{SameGroup} }  $ "

		gen NMFCAPA = holder_act * NMFCAP

		label variable NMFCAPA " $ (\text{FCAP}^*) \times {\text{ActiveHolder} }  $ "





		rename nmfca NMFCA


		generate msize1size2 =  monthlysize1 * monthlysize2
		label variable msize1size2 "$ Size1 \times Size2 $"


		generate NMFCA2 = NMFCA * NMFCA


		label variable NMFCA "$ \text{MFCAP*} $"


		label variable NMFCA2 "$ { \text{MFCAP}^ * } ^ 2$"



		generate msbm1bm2 =  monthlybm1 * monthlybm2

		label variable msbm1bm2 "$ BookToMarketMarket_1 \times BookToMarketMarket_2 $"
		label variable monthlysamebm "SameBookToMarket"
		label variable monthlybm1 "$ BookToMarketMarket_1 $"

		label variable monthlybm2 "$ BookToMarketMarket_2 $"






		drop if monthlyfcapf >1
		drop if fcapf >1


		xtset id t_month  





		replace monthlycrossownership = monthlycrossownership/100
		label variable monthlycrossownership "CrossOwnership"



		summ forthquarter if forthquarter != 1



}

			foreach var in NMFCAGM NMFCAM sbgroupM NMFCAG median {
					capture drop `var'
				}
				
{				
		gen median = 0 

		replace median = 1 if forthquarter == 1
		replace median = 0 if forthquarter != 1





		label variable median " $ (\text{MFCAP} > Q3[\text{MFCAP}]) $ "

		gen NMFCAM = NMFCA * median

		label variable NMFCAM " $ (\text{MFCAP} > Q3[\text{MFCAP}]) \times {\text{MFCAP} ^*}  $ "

		gen sbgroupM = sbgroup * median
		label variable sbgroupM " $ (\text{MFCAP} > Q3[\text{MFCAP}]) \times {\text{SameGroup} }  $ "

		gen NMFCAG = sbgroup * NMFCA
		label variable NMFCAG " $ (\text{MFCAP}^*) \times {\text{SameGroup} }  $ "

		gen NMFCAGM = sbgroup  * median
		label variable NMFCAGM " $ (\text{MFCAP} > Q3[\text{MFCAP}]) \times  {\text{SameGroup} }  $ "


		summ MFCA if median == 1

		summ monthlyfcapf if monthlyfcapf>0



}






rename NMFCA vv
rename NMFCAGM mvv

/*
eststo v1 : quietly asreg monthlyρ_5_f median   monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace
*/

 
eststo v3 : xi: quietly asreg monthlyρ_5_f vv  NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership  i.PairType , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v4 : xi: quietly asreg monthlyρ_5_f  sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership  i.PairType , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

/*
eststo v5 : quietly asreg monthlyρ_5_f median sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace





 eststo v6: quietly asreg monthlyρ_5_f median  sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace


 eststo v61: quietly asreg monthlyρ_5_f median  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 0   , fmb newey(4) 
estadd loc subSample "Others" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace
*/

eststo v7: xi: quietly asreg monthlyρ_5_f vv sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v71: xi: quietly asreg monthlyρ_5_f vv sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType if sbgroup == 0   , fmb newey(4) 
estadd loc subSample "Others" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v8 : xi: quietly asreg monthlyρ_5_f vv  NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership  i.PairType gdummy0-gdummy47 , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "Yes" , replace


eststo v9 : xi: quietly asreg monthlyρ_5_f vv sgroup monthlysamesize monthlysamebm monthlycrossownership i.PairType, fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace


eststo v10 : xi: quietly asreg monthlyρ_5_f vv sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership  i.PairType , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace


 /*
eststo v11 : quietly asreg monthlyρ_5_f median  mvv  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace


eststo v12: quietly asreg monthlyρ_5_f median  mvv  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   gdummy0-gdummy47 , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "Yes" , replace

eststo v13 : quietly asreg monthlyρ_5_f median sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace
*/

esttab  v4 v9  v10 v7 v71 v3 v8 /* v13 v1 v5  v6 v61 v11  v12 */ ,  nomtitle  label  s( controll subSample GroupFE  N  ,  lab( "Controls" "Sub-Sample" "Business Group FE"  "Observations" )) keep(/*median */ NMFCAG sbgroup vv /*mvv*/) order(sbgroup vv NMFCAG median mvv )  compress  mgroups("Dependent Variable: Future Pairs' co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using Q3mresultAllPairs.tex ,replace


rename  vv NMFCA
rename mvv NMFCAGM 

correlate  median  NMFCAGM sbgroup
/****/

/*BigSmall*/



 eststo v0: quietly  asreg monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4) 
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

esttab v0 Bv0 Bv1  SBv0 SBv1 Sv0 Sv1 v1  , nomtitle label  s( N Controls  SubSample FE r2 ,  lab("Observations" "Controls" "Sub-sample" "Pair Size FE" "$ R^2 $"))   compress order(sbgroup NMFCA  NMFCAG ) keep(NMFCA  sbgroup  NMFCAG  ) mgroups("Dependent Variable: Future Monthly Correlation of 4F+Ind. Res."   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Qmresult4-AllPairs.tex ,replace 




/**/






binscatter monthlyρ_5_f NMFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(20) by (sbgroup) legend(pos(4) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("FCA*") title("All Pairs")  msymbol(Th S) 
graph export mcorr5BigSameG-AllPairs.eps,replace
graph export mcorr5BigSameG-AllPairs.png,replace


/*


asreg monthlyρ_5_f median sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership monthlyρ_turn monthlyρ_5 , fmb newey(4)






/**/

gen medianm = 0
replace medianm = 1 if secondquarter == 1



label variable medianm " $ (\text{FCA} > Median[\text{FCA}]) $ "

replace NMFCAM = NMFCA * medianm

label variable NMFCAM " $ (\text{FCA} > Median[\text{FCA}]) \times {\text{FCA} ^*}  $ "

replace sbgroupM = sbgroup * medianm
label variable sbgroupM " $ (\text{FCA} > Median[\text{FCA}]) \times {\text{SameGroup} }  $ "

replace NMFCAGM = sbgroup  * medianm
label variable NMFCAGM " $ (\text{FCA} > Median[\text{FCA}]) \times  {\text{SameGroup} }  $ "



eststo mv1 : quietly asreg monthlyρ_5_f medianm   monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
eststo mv3 : quietly asreg monthlyρ_5_f medianm  NMFCAGM monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo mv4 : quietly asreg monthlyρ_5_f monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo mv5 : quietly asreg monthlyρ_5_f medianm   monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
 eststo mv6: quietly asreg monthlyρ_5_f medianm   monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

 eststo mv7: quietly asreg monthlyρ_5_f NMFCA   monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

esttab  mv4 mv5 mv1 mv6 mv7 mv3 ,  nomtitle  label  s( N subSample controll r2 ,  lab("Observations" "Sub Sample" "Controls" "$ R^2 $")) order(medianm   sbgroup NMFCAGM NMFCA) keep(median  NMFCAGM sbgroup NMFCA) compress  mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Q2mresultAllPairs.tex ,replace

/**/


gen medianc = 0 
replace medianc = 1 if MFCA > 0



label variable medianc " Common Ownership "

replace NMFCAM = NMFCA * medianc

label variable NMFCAM " $ \text{Common Ownership} \times {\text{FCA} ^*}  $ "

replace sbgroupM = sbgroup * medianc
label variable sbgroupM " $ \text{Common Ownership} \times {\text{SameGroup} }  $ "

replace NMFCAGM = sbgroup  * medianc
label variable NMFCAGM " $ \text{Common Ownership} \times  {\text{SameGroup} }  $ "



eststo cv1 : quietly asreg monthlyρ_5_f medianc   monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
eststo cv3 : quietly asreg monthlyρ_5_f medianc  NMFCAGM monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo cv4 : quietly asreg monthlyρ_5_f monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

eststo cv5 : quietly asreg monthlyρ_5_f medianc   monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace

 
 eststo cv6: quietly asreg monthlyρ_5_f medianc   monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

 eststo cv7: quietly asreg monthlyρ_5_f NMFCA   monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace

esttab  cv4 cv5 cv1 cv6 cv7 cv3 ,  nomtitle  label  s( N subSample controll r2 ,  lab("Observations" "Sub Sample" "Controls" "$ R^2 $")) order(medianc   sbgroup NMFCAGM NMFCA) keep(medianc  NMFCAGM sbgroup NMFCA) compress  mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using mresultAllPairs.tex ,replace




