




/*Group dummy*/
 

	/*
eststo v0: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm  gdummy0-gdummy47 FCAgdummy0-FCAgdummy47 SGFCAgdummy0-SGFCAgdummy47  SGgdummy0-SGgdummy47 , fmb newey(4)  

esttab v0 , drop(NMFCA monthlyρ_5  sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm) nostar  wide nostar noparentheses


esttab v0 ,label keep(NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm)
*/

eststo v1: quietly asreg monthlyρ_5_f  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm  gdummy0-gdummy47 SGgdummy0-SGgdummy47 , fmb newey(4)  

eststo v1: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm  gdummy0-gdummy47 FCAgdummy0-FCAgdummy47 SGFCAgdummy0-SGFCAgdummy47 SGgdummy0-SGgdummy47 , fmb newey(4)  



esttab v1 , drop(monthlyρ_5  sbgroup   sgroup monthlysamesize monthlysamebm) nostar  wide nostar noparentheses label


esttab v1 ,label keep(NMFCA monthlyρ_5 sbgroup  sgroup monthlysamesize monthlysamebm)

/* Other */


  

gen InvInGroupSb = sbgroup *  invingroup_x 
label variable InvInGroupSb " $ \text{Inv. in group}  \times {\text{SameGroup} } $ "

gen InvInGroupFCA = InvInGroupSb * NMFCA
label variable InvInGroupFCA " $ (\text{FCA}^*) \times {\text{Inv. in group} } \times {\text{SameGroup} } $ "






gen BankGroupSb = sbgroup *  bankinguo_x 
label variable BankGroupSb " $ \text{Bank is Uo}   \times {\text{SameGroup} } $ "

gen BankGroupFCA = BankGroupSb * NMFCA
label variable BankGroupFCA " $ (\text{FCA}^*) \times {\text{Bank is Uo} } \times {\text{SameGroup} } $ "




gen BankInGroupSb = sbgroup * bankingroup_x
label variable BankInGroupSb " $ {\text{Bank in group}  } \times {\text{SameGroup}}  $ "




gen BankInGroupFCA = BankInGroupSb * NMFCA
label variable BankInGroupFCA " $ (\text{FCA}^*) \times {\text{Bank in group} }  \times {\text{SameGroup}}$ "

label variable invingroup " $ \text{Inv. in group}  $ "
label variable bankgroup " $ \text{Bank is Uo}  $ "
label variable  bankingroup " $  {\text{Bank in group} } $ "




corr  NMFCA  sbgroup NMFCAG invingroup  InvInGroupSb InvInGroupFCA bankgroup BankGroupSb BankGroupFCA bankingroup BankInGroupSb BankInGroupFCA


eststo v0: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize , lag(4) 

/*
eststo v10: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize invingroup , lag(4)

eststo v101: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize invingroup InvInGroupSb, lag(4)

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize invingroup  InvInGroupSb InvInGroupFCA, lag(4) 
*/

eststo v20: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankgroup , lag(4) 

eststo v201: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankgroup BankGroupSb, lag(4) 

eststo v2: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankgroup BankGroupSb BankGroupFCA, lag(4) 


eststo v30: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankingroup , lag(4) 

eststo v301: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankingroup BankInGroupSb , lag(4) 

eststo v3: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankingroup BankInGroupSb BankInGroupFCA , lag(4) 

eststo v40: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize  bankgroup bankingroup  , lag(4) /*invingroup*/

eststo v401: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize  bankgroup BankGroupSb bankingroup BankInGroupSb  , lag(4) /*invingroup InvInGroupSb*/

eststo v4: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize  bankgroup BankGroupSb BankGroupFCA bankingroup BankInGroupSb BankInGroupFCA , lag(4) /*invingroup  InvInGroupSb InvInGroupFCA*/



esttab v0  v20 v201 v2 v30 v301 v3  v40 v401 v4   , nomtitle label  n r2   compress  keep( NMFCA sbgroup NMFCAG   bankgroup BankGroupSb BankGroupFCA bankingroup BankInGroupSb BankInGroupFCA ) order(NMFCA sbgroup NMFCAG bankgroup BankGroupSb BankGroupFCA bankingroup BankInGroupSb BankInGroupFCA   invingroup  InvInGroupSb InvInGroupFCA ) mgroups("De. Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2BankIn-slide.tex ,replace /*v10 v101 v1*/ /*invingroup  InvInGroupSb InvInGroupFCA */




xtfmb monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize invingroup  InvInGroupSb InvInGroupFCA bankgroup BankGroupSb BankGroupFCA bankingroup BankInGroupSb BankInGroupFCA , lag(4)


/**/

replace bankingroup =1 if bankgroup ==1



label variable  bankingroup " $  {\text{Bank in group} } $ "

replace BankInGroupFCA = BankInGroupSb * NMFCA
label variable BankInGroupFCA " $ (\text{FCA}^*) \times {\text{Bank in group} }  \times {\text{SameGroup}}$ "

replace BankInGroupSb = sbgroup * bankingroup_x
label variable BankInGroupSb " $ {\text{Bank in group}  } \times {\text{SameGroup}}  $ "


eststo v0: asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)

eststo v30: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankingroup , fmb newey(4)

eststo v301: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankingroup BankInGroupSb , fmb newey(4)

eststo v3: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sbgroup NMFCAG  sgroup monthlysamesize bankingroup BankInGroupSb BankInGroupFCA , fmb newey(4)

esttab v0 v30 v301 v3 , nomtitle label  n r2   compress  keep( NMFCA sbgroup NMFCAG  bankingroup BankInGroupSb BankInGroupFCA ) order(NMFCA sbgroup NMFCAG  bankingroup BankInGroupSb BankInGroupFCA ) mgroups("De. Variable:Future  Corr. of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2BankIn.tex,replace



/* GRoup Cluster*/



gen NMFCABigNumber = NMFCA * BigGroupNumber
gen NMFCABigCap = NMFCA * BigGroupCap
gen NMFCATotalCFR = NMFCA * BigGroupTotalCFR
gen NMFCAUoCap = NMFCA * BigGroupUoCap

xtset   id t_month





eststo v0: asreg monthlyρ_5_f  NMFCA  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm  BigGroupNumber  , fmb newey(4)  

eststo v01: asreg monthlyρ_5_f  NMFCA  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm NMFCABigNumber BigGroupNumber  , fmb newey(4)  



eststo v1: asreg monthlyρ_5_f  NMFCA  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm  BigGroupCap  , fmb newey(4) 

eststo v11: asreg monthlyρ_5_f  NMFCA  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm NMFCABigCap BigGroupCap  , fmb newey(4) 



eststo v2: asreg monthlyρ_5_f  NMFCA  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm  BigGroupTotalCFR  , fmb newey(4) 

eststo v21: asreg monthlyρ_5_f  NMFCA  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm NMFCATotalCFR BigGroupTotalCFR  , fmb newey(4) 


eststo v3: asreg monthlyρ_5_f  NMFCA  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm  BigGroupUoCap  , fmb newey(4) 

eststo v31: asreg monthlyρ_5_f  NMFCA  monthlyρ_5   sbgroup  sgroup monthlysamesize monthlysamebm NMFCAUoCap BigGroupUoCap  , fmb newey(4) 

esttab v0 v01 v1 v11 v2 v21 v3 v31 
   


eststo v1: asreg monthlyρ_5_f NMFCA monthlyρ_5    sgroup monthlysamesize monthlysamebm if BigGroupNumber == 0   , fmb newey(4)  

eststo v2: asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm   if BigGroupNumber == 1  , fmb newey(4)  

esttab  v1 v2







