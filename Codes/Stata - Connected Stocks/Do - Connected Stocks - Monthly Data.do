cls
clear
import delimited "E:\RA_Aghajanzadeh\Data\Connected_Stocks\MonthlyNormalzedFCAP9.3.csv", encoding(UTF-8) 
// import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\MonthlyNormalzedFCAP9.3.csv", encoding(UTF-8) 

cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Report\Output" 
// cd "D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report\Output"

label define sgroup 0 "No" 1 "Yes"



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


gen sameGRank = 0
replace sameGRank = 1 if grank_x == grank_y

label variable sameGRank "SameGRank"


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




label variable monthlyρ_5_1 " $ {\rho_{t-1}} $ "
label variable monthlyρ_5_2 " $ {\rho_{t-2}} $ "
label variable monthlyρ_5_3 " $ {\rho_{t-3}} $ "
label variable monthlyρ_5_4 " $ {\rho_{t-4}} $ "
label variable monthlyρ_5_5 " $ {\rho_{t-5}} $ "

label variable monthlysamesize "SameSize"

summarize monthlyfca  monthlyfcap

rename monthlyfca MFCA

rename monthlyfcap NMFCAP

label variable NMFCAP "$ \text{FCAP*} $"

gen NMFCAPG = sbgroup * NMFCAP

label variable NMFCAPG " $ (\text{FCAP}^*) \times {\text{SameGroup} }  $ "

gen NMFCAPA = holder_act * NMFCAP

label variable NMFCAPA " $ (\text{FCAP}^*) \times {\text{ActiveHolder} }  $ "


label variable lowimbalancestd "LowImbalanceStd"

gen ImbalanceSbgroup = lowimbalancestd * sbgroup

label variable ImbalanceSbgroup  " $ \text{LowImbalanceStd} \times {\text{SameGroup} } $ "

gen ImbalanceSbgroupFCA = lowimbalancestd * sbgroup * nmfca

label variable ImbalanceSbgroupFCA  " $ \text{LowImbalanceStd} \times {\text{SameGroup} } \times \text{MFCAP}^*  $ "


gen lowimbalancestdFCA = lowimbalancestd * nmfca
label variable lowimbalancestdFCA  " $ \text{LowImbalanceStd} \times \text{MFCAP}^*  $ "


label variable sbgroup "SameGroup"

rename nmfca NMFCA

label variable NMFCA "$ \text{MFCAP*} $"


gen ImbalanceNMFCA = lowimbalancestd * NMFCA

label variable ImbalanceNMFCA  " $ \text{LowImbalanceStd} \times {\text{MFCAP}^* } $ "



generate msize1size2 =  monthlysize1 * monthlysize2
label variable msize1size2 "$ \text{Size1} \times \text{Size2} $"


rename nmfca2 NMFCA2




label variable NMFCA2 "$ \text{QuardaticTr}(\text{MFCAP}^ *) $"

generate lnMFCA = ln(MFCA)
label variable lnMFCA "$\ln(MFCAP)$"

generate msbm1bm2 =  monthlybm1 * monthlybm2

label variable msbm1bm2 "$ BM_1 \times BMt_2 $"
label variable monthlysamebm "SameBM"
label variable monthlybm1 "$ BM_1 $"

label variable monthlybm2 "$ BM_2 $"

gen median = 0

replace median = 1 if secondquarter == 1 
replace median = 0 if median != 1 

gen NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{MFCAP}^* > Median[\text{MFCAP}^*]) \times {\text{MFCAP} ^*}  $ "

gen sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{MFCAP}^* > Median[\text{MFCAP}^*]) \times {\text{SameGroup} }  $ "

gen NMFCAG = sbgroup * NMFCA
label variable NMFCAG " $ \text{MFCAP}^* \times {\text{SameGroup} }  $ "

generate Down = NMFCA * bearish * sbgroup
label variable Down "$ \text{MFCAP}^* \times {\text{Bearish Market}} \times {\text{SameGroup} }  $ "






generate Up = NMFCA * bullish * sbgroup

label variable Up "$ \text{MFCAP}^* \times {\text{Bullish Market}} \times {\text{SameGroup} }  $ "



label variable bearish "Bearish Market"
label variable bullish "Bullish Market"

gen NMFCAGM = sbgroup * NMFCA * median
label variable NMFCAGM " $ (\text{MFCAP}^* > Median[\text{MFCAP}^*]) \times  \text{MFCAP}^* \times {\text{SameGroup} }  $ "




gen NMFCAA = holder_act * NMFCA

label variable NMFCAA " $ \text{MFCAP}^* \times {\text{ActiveHolder} }  $ "


gen holder_actM = holder_act * median
label variable holder_actM " $ (\text{MFCAP}^* > Median[\text{MFCAP}^*]) \times {\text{ActiveHolder} }  $ "

gen spositionM = sposition * median

label variable spositionM " $ (\text{MFCAP}^* > Median[\text{MFCAP}^*]) \times {\text{Same Position} }  $ "



/**/


summ bearish bullish

generate lnMFCAP = ln(monthlyfcap)
label variable lnMFCAP "$\ln(FCAP)$"

generate lnMFCAG = lnMFCA * sbgroup
label variable lnMFCAG "$ \ln(MFCAP) \times {\text{SameGroup} }  $ "


generate lnMFCAA = lnMFCA * holder_act
label variable lnMFCAA "$ \ln(MFCAP) \times {\text{ActiveHolder} }  $ "

generate lnDown = lnMFCA * bearish * sbgroup
label variable lnDown "$ \ln(MFCAP) \times {\text{Bearish Market} } \times {\text{SameGroup} }  $ "

generate lnUp = lnMFCA * bullish * sbgroup
label variable lnUp "$ \ln(MFCAP) \times {\text{Bullish Market} } \times {\text{SameGroup} }  $ "


generate sDown = bearish * sbgroup
label variable sDown "$ {\text{Bearish Market} } \times {\text{SameGroup} }  $ "

generate DownFCA = bearish * NMFCA
label variable DownFCA "$ {\text{Bearish Market} } \times \text{MFCAP}^*  $ "

generate sUp = bullish * sbgroup
label variable sUp "$ {\text{Bullish Market} } \times {\text{SameGroup} }  $ "

generate UpFCA = bullish * NMFCA
label variable UpFCA "$ {\text{Bullish Market} } \times \text{MFCAP}^*   $ "

gen PairType = 0

summ grank_x

replace PairType = 1  if grank_x <5 & grank_y<5
replace PairType = 2  if grank_x >=5 & grank_y>=5

label define PairType 0 "Hybrid" 1 "Small" 2 "Large"



label values PairType PairType
label variable PairType "PairType"



drop if monthlyfcapf >1
/*drop if fcapf >1*/


xtset id t_month  









gen BigGroupNumber = quantilenumber_x  if sbgroup == 1

gen BigGroupCap = quantilegroupmarketcap_x  if sbgroup == 1

gen BigGroupTotalCFR = quantiletotalcfr_x  if sbgroup == 1

gen BigGroupUoCap = quantileuomarketcap_x  if sbgroup == 1


 foreach v of varlist  BigGroupNumber BigGroupCap BigGroupTotalCFR BigGroupUoCap{

 replace `v' = 0 if `v' == 2 | `v' == 1
 replace `v' = 1 if `v' == 4 | `v' == 3

}


summ  BigGroupNumber BigGroupCap BigGroupTotalCFR BigGroupUoCap

cor  NMFCA NMFCAM NMFCAG NMFCAGM BigGroupNumber BigGroupCap BigGroupTotalCFR BigGroupUoCap

/*
foreach v of varlist  gdummy0-gdummy47 {

	gen SG`v' = sbgroup * `v'

}
foreach v of varlist  gdummy0-gdummy47 {

	gen FCA`v' = NMFCA * `v'

}
foreach v of varlist  gdummy0-gdummy47 {

	gen SGFCA`v' = sbgroup * NMFCA * `v'

}
*/

replace monthlycrossownership = monthlycrossownership/100



label variable monthlycrossownership "CrossOwnership"
label variable bigbusinessgroup "BigGroup"

gen bigbusinessgroupSgroup = bigbusinessgroup * sbgroup
label variable bigbusinessgroupSgroup "$ {\text{BigGroup} } \times {\text{SameGroup} }  $ "

gen bigbusinessgroupFCA = bigbusinessgroup * NMFCA
label variable bigbusinessgroupFCA "$ {\text{BigGroup} } \times \text{MFCAP}^*  $ "

gen bigbusinessgroupSgroupFCA = bigbusinessgroup * sbgroup * NMFCA
label variable bigbusinessgroupSgroupFCA "$ {\text{BigGroup} } \times {\text{SameGroup} } \times \text{MFCAP}^* $ "



gen bigbusinessgroupTurn = bigbusinessgroup * monthlyρ_turn
label variable bigbusinessgroupTurn "$ {\text{BigGroup} } \times{\rho(\Delta \text{Turnover})_t}  $ "

gen Turnsbgroup = sbgroup * monthlyρ_turn
label variable Turnsbgroup "$ {\text{SameGroup} \times {\rho(\Delta \text{Turnover})_t}$ "

gen TurnSgroupbigbusinessgroup = bigbusinessgroup * sbgroup * monthlyρ_turn
label variable TurnSgroupbigbusinessgroup "$ {\text{BigGroup}}\times{\text{SameGroup}}\times  {\rho(\Delta \text{Turnover})_t} $ "

summ sbgroup if bigbusinessgroupSgroup == 1

summ id


capture drop   highbeta

gen highbeta = 0

replace highbeta = 1 if highbeta_x == 1
replace highbeta = 1 if highbeta_y == 1


label variable highbeta "HighBetaGroup"

gen Grouphighbeta = highbeta * sbgroup
label variable Grouphighbeta "$ {\text{HighBetaGroup} } \times {\text{SameGroup} }  $ "

label variable positivesynch "High Positive direction"

gen Grouphpositivesynch = positivesynch * sbgroup
label variable Grouphpositivesynch "$ {\text{High Positive direction} } \times {\text{SameGroup} }  $ "



capture drop   lowres

gen lowres = 0

replace lowres = 1 if lowres_x == 1
replace lowres = 1 if lowres_y == 1


label variable lowres "LowTurnoverStd"

gen Grouplowres = lowres * sbgroup
label variable Grouplowres "$ {\text{LowTurnoverStd} } \times {\text{SameGroup} }  $ "



capture drop xx
gen xx = sbgroup * trunresstd_x
label variable xx "$ {\text{Group Turnover std} } \times {\text{SameGroup} }  $ "

label variable trunresstd_x " $ {\text{Group Turnover std}_1} $ "
label variable trunresstd_y " $ {\text{Group Turnover std}_2} $ "


capture drop yy
gen yy = sbgroup * insimbalance_value_x
label variable yy "$ {\text{Group Ins Imb std} } \times {\text{SameGroup} }  $ "
label variable insimbalance_value_x " $ {\text{Group Ins Imb std}_1} $ "
label variable insimbalance_value_y " $ {\text{Group Ins Imb std}_2} $ "

gen zz = sbgroup * gsize_x
label variable zz "$ {\text{Group Size} } \times {\text{SameGroup} }  $ "
label variable gsize_x " $ {\text{Group Size}_1} $ "
label variable gsize_y " $ {\text{Group Size}_2} $ "

 

gen turnSbgroup = monthlyρ_turn_f * sbgroup
label variable turnSbgroup " $ \text{SameGroup} \times {\rho(\Delta \text{Turnover})_{t+1}} $ "




foreach var of varlist NMFCA sbgroup NMFCAG monthlyρ_5 monthlyρ_5_f monthlyρ_turn_f{
  summ `var'
  gen `var'std = `var'/r(sd)
  }

label variable monthlyρ_5std " $ {\rho_t} / \sigma $ "
label variable monthlyρ_turn_fstd " $ {\rho(\Delta \text{Turnover})_t} / \sigma $ "
  
summ sbgroupstd


gen rankedFCA = 0

replace rankedFCA = 1 if fcaperncentilerank >0.25

replace rankedFCA = 2 if fcaperncentilerank >0.5

replace rankedFCA = 3 if fcaperncentilerank >0.75



foreach var in samesize2 samesize3 size12 size22 samesize1222 samesize1122 samesize1221{
	capture drop    `var'
}


gen samesize2 = monthlysamesize * monthlysamesize
gen samesize3 = samesize2 * monthlysamesize
gen size12 = monthlysize1 * monthlysize1
gen size22 = monthlysize2 * monthlysize2
gen samesize1222 = size12 * size22
gen samesize1122 = monthlysize1 * size22
gen samesize1221 = size12 * monthlysize2


// replace monthlyρ_5 = monthlyρ_residual_bench

capture drop monthlyρ_5_f
gen monthlyρ_5_f = f.monthlyρ_5





capture drop monthlyρ_4_f
gen monthlyρ_4_f = f.monthlyρ_4


capture drop monthlyρ_turn_f
gen monthlyρ_turn_f = f.monthlyρ_turn
label variable monthlyρ_turn " $ {\rho(\Delta \text{Turnover})_t} $ "
label variable monthlyρ_turn_f " $ {\rho(\Delta \text{Turnover})_{t+1}} $ "




gen m2 = forthquarter * sbgroup


corr m2 forthquarter sbgroup




summ MFCA if forthquarter == 1