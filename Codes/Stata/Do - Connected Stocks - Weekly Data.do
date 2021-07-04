cls
clear
import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\WeeklyNormalzedFCAP6.2.csv", encoding(UTF-8) 


cd "D:\Dropbox\Connected Stocks\Final Report"

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


label variable weeklysize1 "Size1"
label variable weeklysize2 "Size2"
label variable weeklyρ_4_f "ForwardCorr"
label variable weeklyρ_2 " $ {\rho_t} $ "
label variable weeklyρ_4 " $ {\rho_t} $ "
label variable weeklyρ_5 " $ {\rho_t} $ "
label variable weeklyρlag_5 " $ {\rho_t} $ "
label variable weeklysamesize "SameSize"

summarize weeklyfca  weeklyfcap

rename weeklyfca WFCA

rename weeklyfcap NWFCAP

label variable NWFCAP "$ \text{FCAP*} $"

gen NWFCAPG = sbgroup * NWFCAP

label variable NWFCAPG " $ (\text{FCAP}^*) \times {\text{SameGroup} }  $ "

gen NWFCAPA = holder_act * NWFCAP

label variable NWFCAPA " $ (\text{FCAP}^*) \times {\text{ActiveHolder} }  $ "




rename nwfca NWFCA



generate wsize1size2 =  weeklysize1 * weeklysize2
label variable wsize1size2 "$ Size1 \times Size2 $"


generate NWFCA2 = NWFCA * NWFCA


label variable NWFCA "$ \text{FCA*} $"


label variable NWFCA2 "$ { \text{FCA}^ * } ^ 2$"

generate lnWFCA = ln(WFCA)
label variable lnWFCA "$\ln(FCA)$"

generate wsbm1bm2 =  weeklybm1 * weeklybm2

label variable wsbm1bm2 "$ BookToMarketMarket_1 \times BookToMarketMarket_2 $"
label variable weeklysamebm "SameBookToMarket"
label variable weeklybm1 "$ BookToMarketMarket_1 $"

label variable weeklybm2 "$ BookToMarketMarket_2 $"



egen median = median(NWFCA)

xtile  Q = NWFCA, nq(4)
 
replace median = 0 if Q <=3
replace median = 1 if Q  == 4

gen NWFCAM = NWFCA * median

label variable NWFCAM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{FCA} ^*}  $ "

gen sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{SameGroup} }  $ "

gen NWFCAG = sbgroup * NWFCA
label variable NWFCAG " $ (\text{FCA}^*) \times {\text{SameGroup} }  $ "



gen NWFCAGM = sbgroup * NWFCA * median
label variable NWFCAGM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times  (\text{FCA}^*) \times {\text{SameGroup} }  $ "




gen NWFCAA = holder_act * NWFCA

label variable NWFCAA " $ (\text{FCA}^*) \times {\text{ActiveHolder} }  $ "


gen holder_actM = holder_act * median
label variable holder_actM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{ActiveHolder} }  $ "

gen spositionM = sposition * median

label variable spositionM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{Same Position} }  $ "



/**/




generate lnWFCAP = ln(weeklyfcap)
label variable lnWFCAP "$\ln(FCAP)$"

generate lnWFCAG = lnWFCA * sbgroup
label variable lnWFCAG "$ (\ln(FCA)) \times {\text{SameGroup} }  $ "


generate lnWFCAA = lnWFCA * holder_act
label variable lnWFCAA "$ (\ln(FCA)) \times {\text{ActiveHolder} }  $ "

gen PairType = 0

summ grank_x

replace PairType = 1  if grank_x <5 & grank_y<5
replace PairType = 2  if grank_x >=5 & grank_y>=5

label define PairType 0 "Hybrid" 1 "Small" 2 "Large"



label values PairType PairType
label variable PairType "PairType"




drop if weeklyfcapf >1
drop if fcapf >1


xtset id t_week  









gen BigGroupNumber = quantilenumber_x  if sbgroup == 1

gen BigGroupCap = quantilegroupmarketcap_x  if sbgroup == 1

gen BigGroupTotalCFR = quantiletotalcfr_x  if sbgroup == 1

gen BigGroupUoCap = quantileuomarketcap_x  if sbgroup == 1


 foreach v of varlist  BigGroupNumber BigGroupCap BigGroupTotalCFR BigGroupUoCap{

 replace `v' = 0 if `v' == 2 | `v' == 1
 replace `v' = 1 if `v' == 4 | `v' == 3

}


summ  BigGroupNumber BigGroupCap BigGroupTotalCFR BigGroupUoCap




foreach v of varlist  gdummy0-gdummy47 {

	gen SG`v' = sbgroup * `v'

}
foreach v of varlist  gdummy0-gdummy47 {

	gen FCA`v' = NWFCA * `v'

}
foreach v of varlist  gdummy0-gdummy47 {

	gen SGFCA`v' = sbgroup * NWFCA * `v'

}


replace weeklycrossownership = weeklycrossownership/100



 label variable weeklycrossownership "CrossOwnership"


