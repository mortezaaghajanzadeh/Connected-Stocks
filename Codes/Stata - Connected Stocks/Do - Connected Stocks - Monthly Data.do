cls
clear
import delimited "E:\RA_Aghajanzadeh\Data\Connected_Stocks\MonthlyNormalzedFCAP9.2.csv", encoding(UTF-8) 
// import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\MonthlyNormalzedFCAP9.2.csv", encoding(UTF-8) 

cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Final Report\Output" 
// cd "C:\Users\RA_Aghajanzadeh\Dropbox\Connected Stocks\Connected-Stocks\Final Report"

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


label variable lowimbalancestd "Low Imbalance std"

gen ImbalanceSbgroup = lowimbalancestd * sbgroup

label variable ImbalanceSbgroup  " $ \text{Low Imbalance std} \times {\text{SameGroup} } $ "

gen ImbalanceSbgroupFCA = lowimbalancestd * sbgroup * nmfca

label variable ImbalanceSbgroupFCA  " $ \text{Low Imbalance std} \times {\text{SameGroup} } \times \text{FCA}^*  $ "


label variable sbgroup "Same Group"

rename nmfca NMFCA

label variable NMFCA "$ \text{FCA*} $"


gen ImbalanceNMFCA = lowimbalancestd * NMFCA

label variable ImbalanceNMFCA  " $ \text{Low Imbalance std} \times {\text{FCA}^* } $ "



generate msize1size2 =  monthlysize1 * monthlysize2
label variable msize1size2 "$ Size1 \times Size2 $"


rename nmfca2 NMFCA2




label variable NMFCA2 "$ \text{QuardaticTr}(\text{FCA}^ *) $"

generate lnMFCA = ln(MFCA)
label variable lnMFCA "$\ln(FCA)$"

generate msbm1bm2 =  monthlybm1 * monthlybm2

label variable msbm1bm2 "$ BookToMarketMarket_1 \times BookToMarketMarket_2 $"
label variable monthlysamebm "SameBookToMarket"
label variable monthlybm1 "$ BookToMarketMarket_1 $"

label variable monthlybm2 "$ BookToMarketMarket_2 $"

egen median = median(NMFCA)

replace median = 1 if NMFCA > median
replace median = 0 if median != 1 

gen NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times {\text{FCA} ^*}  $ "

gen sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times {\text{SameGroup} }  $ "

gen NMFCAG = sbgroup * NMFCA
label variable NMFCAG " $ (\text{FCA}^*) \times {\text{SameGroup} }  $ "

generate Down = NMFCA * bearish * sbgroup
label variable Down "$ (\text{FCA}^*) \times {\text{Bearish Market}} \times {\text{SameGroup} }  $ "






generate Up = NMFCA * bullish * sbgroup

label variable Up "$ (\text{FCA}^*) \times {\text{Bullish Market}} \times {\text{SameGroup} }  $ "



label variable bearish "Bearish Market"
label variable bullish "Bullish Market"

gen NMFCAGM = sbgroup * NMFCA * median
label variable NMFCAGM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times  (\text{FCA}^*) \times {\text{SameGroup} }  $ "




gen NMFCAA = holder_act * NMFCA

label variable NMFCAA " $ (\text{FCA}^*) \times {\text{ActiveHolder} }  $ "


gen holder_actM = holder_act * median
label variable holder_actM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times {\text{ActiveHolder} }  $ "

gen spositionM = sposition * median

label variable spositionM " $ (\text{FCA}^* > Median[\text{FCA}^*]) \times {\text{Same Position} }  $ "



/**/


summ bearish bullish

generate lnMFCAP = ln(monthlyfcap)
label variable lnMFCAP "$\ln(FCAP)$"

generate lnMFCAG = lnMFCA * sbgroup
label variable lnMFCAG "$ (\ln(FCA)) \times {\text{SameGroup} }  $ "


generate lnMFCAA = lnMFCA * holder_act
label variable lnMFCAA "$ (\ln(FCA)) \times {\text{ActiveHolder} }  $ "

generate lnDown = lnMFCA * bearish * sbgroup
label variable lnDown "$ (\ln(FCA)) \times {\text{Bearish Market} } \times {\text{SameGroup} }  $ "

generate lnUp = lnMFCA * bullish * sbgroup
label variable lnUp "$ (\ln(FCA)) \times {\text{Bullish Market} } \times {\text{SameGroup} }  $ "


generate sDown = bearish * sbgroup
label variable sDown "$ {\text{Bearish Market} } \times {\text{SameGroup} }  $ "

generate sUp = bullish * sbgroup
label variable sUp "$ {\text{Bullish Market} } \times {\text{SameGroup} }  $ "

gen PairType = 0

summ grank_x

replace PairType = 1  if grank_x <5 & grank_y<5
replace PairType = 2  if grank_x >=5 & grank_y>=5

label define PairType 0 "Hybrid" 1 "Small" 2 "Large"



label values PairType PairType
label variable PairType "PairType"


xtile  Q = MFCA, nq(4)


drop if monthlyfcapf >1
drop if fcapf >1


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


foreach v of varlist  gdummy0-gdummy47 {

	gen SG`v' = sbgroup * `v'

}
foreach v of varlist  gdummy0-gdummy47 {

	gen FCA`v' = NMFCA * `v'

}
foreach v of varlist  gdummy0-gdummy47 {

	gen SGFCA`v' = sbgroup * NMFCA * `v'

}


replace monthlycrossownership = monthlycrossownership/100



 label variable monthlycrossownership "CrossOwnership"


 asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership   , fmb newey(4)

cor  monthlyρ_5_f NMFCA monthlyρ_5  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup 

cor NMFCAG NMFCA sbgroup

reg MFCA c.t_month##sbgroup ,robust

