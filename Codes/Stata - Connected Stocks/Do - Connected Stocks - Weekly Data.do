cls
clear
import delimited "E:\RA_Aghajanzadeh\Data\Connected_Stocks\WeeklyNormalzedFCAP9.2.csv", encoding(UTF-8) 


cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Report\Output"

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

label variable NWFCAPA " $ \text{FCAP}^* \times {\text{ActiveHolder} }  $ "

gen NWFCAG = sbgroup * nwfca

label variable NWFCAG " $ \text{MFCAP}^* \times {\text{ActSameGroupiveHolder} }  $ "




rename nwfca NWFCA



generate wsize1size2 =  weeklysize1 * weeklysize2
label variable wsize1size2 "$ Size1 \times Size2 $"


generate NWFCA2 = NWFCA * NWFCA


label variable NWFCA "$ \text{MFCAP}^*} $"


label variable NWFCA2 "$ { \text{MFCAP}^* } ^ 2$"

generate lnWFCA = ln(WFCA)
label variable lnWFCA "$\ln(FCA)$"

generate wsbm1bm2 =  weeklybm1 * weeklybm2

label variable wsbm1bm2 "$ BookToMarketMarket_1 \times BookToMarketMarket_2 $"
label variable weeklysamebm "SameBookToMarket"
label variable weeklybm1 "$ BookToMarketMarket_1 $"

label variable weeklybm2 "$ BookToMarketMarket_2 $"



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





replace weeklycrossownership = weeklycrossownership/100



 label variable weeklycrossownership "CrossOwnership"
 

 
 {
 

rename NWFCA vv



 
eststo v3 : xi: quietly asreg weeklyρ_5_f vv  NWFCAG  sbgroup   sgroup weeklysamesize weeklysamebm weeklycrossownership  i.PairType , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v4 : xi: quietly asreg weeklyρ_5_f  sbgroup sgroup weeklysamesize weeklysamebm weeklycrossownership  i.PairType , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace



eststo v7: xi: quietly asreg weeklyρ_5_f vv sgroup weeklysamesize weeklysamebm weeklycrossownership i.PairType if sbgroup == 1   , fmb newey(4) 
estadd loc subSample "SameGroups" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v71: xi: quietly asreg weeklyρ_5_f vv sgroup weeklysamesize weeklysamebm weeklycrossownership i.PairType if sbgroup == 0   , fmb newey(4) 
estadd loc subSample "Others" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v8 : xi: quietly asreg weeklyρ_5_f vv  NWFCAG  sbgroup   sgroup weeklysamesize weeklysamebm weeklycrossownership  i.PairType gdummy0-gdummy47 , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "Yes" , replace


eststo v9 : xi: quietly asreg weeklyρ_5_f vv sgroup weeklysamesize weeklysamebm weeklycrossownership i.PairType, fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace


eststo v10 : xi: quietly asreg weeklyρ_5_f vv sbgroup  sgroup weeklysamesize weeklysamebm weeklycrossownership  i.PairType , fmb newey(4)
estadd loc subSample "Total" , replace
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace



esttab  v9 v4   v10 v7 v71 v3 v8 ,  nomtitle  label  s( /*controll*/ subSample GroupFE  N  ,  lab(/*"Controls"*/  "Sub-Sample" "Business Group FE" "Observations" )) keep( NWFCAG sbgroup vv ) order( vv sbgroup NWFCAG /*median mvv*/ )  compress  mgroups("Dependent Variable: Future Pairs' co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  


esttab  v9 v4   v10 v7 v71 v3 v8 ,  nomtitle  label  s( /*controll*/ subSample GroupFE  N  ,  lab(/*"Controls"*/  "Sub-Sample" "Business Group FE" "Observations" )) keep( NWFCAG sbgroup vv ) order( vv sbgroup NWFCAG /*median mvv*/ )  compress  mgroups("Dependent Variable: Future Pairs' co-movement"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )   ,using wresult.tex ,replace

 }


 
 xi: asreg weeklyρ_5_f vv sbgroup  sgroup weeklysamesize weeklysamebm weeklycrossownership  i.PairType , fmb newey(4)
