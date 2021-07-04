

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

cor monthlyρ_5_f NMFCA median NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5



/**/

eststo v0: quietly asreg monthlyρ_5_f NMFCA if sbgroup == 1, fmb newey(4)
estadd loc SubSample "SameGroup" , replace
eststo v1: quietly asreg monthlyρ_5_f NMFCA  if sbgroup == 0, fmb newey(4)
estadd loc SubSample "Others" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership if sbgroup == 1, fmb newey(4)
estadd loc SubSample "SameGroup" , replace
eststo v3: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership   if sbgroup == 0, fmb newey(4)
estadd loc SubSample "Others" , replace


esttab v0 v1 v2 v3  , nomtitle label n r2  compress s( N SubSample  r2 ,  lab("Observations" "Sub-sample"  "$ R^2 $")) mgroups("Future Monthly Corr. of 4F+Industry Res."   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using subsampleBGmresult-slide.tex ,replace

/*NMFCA*/
eststo clear

eststo v1: quietly asreg monthlyρ_5_f  NMFCA , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v3: quietly asreg monthlyρ_5_f  sbgroup  , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v4: quietly asreg monthlyρ_5_f sbgroup  monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v5: quietly asreg monthlyρ_5_f NMFCA sbgroup , fmb newey(4) 
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v6: quietly asreg monthlyρ_5_f NMFCA sbgroup monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace

eststo v7: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v8: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v9: quietly asreg monthlyρ_5_f NMFCA sbgroup NMFCAG monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
estadd loc GroupFE "Yes" , replace
estadd loc controll "Yes" , replace



esttab  v1 v2 v3 v4 v5 v6 v7 v8 v9 ,nomtitle label   s( N GroupFE controll r2 ,  lab("Observations" "Group Effect" "Controls" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(NMFCA sbgroup NMFCAG ) mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-slide.tex ,replace
/*Quadratic*/

/*NMFCA*/
eststo clear

eststo v1: quietly asreg monthlyρ_5_f  NMFCA2 , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA2 monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v3: quietly asreg monthlyρ_5_f  sbgroup  , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v4: quietly asreg monthlyρ_5_f sbgroup  monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v5: quietly asreg monthlyρ_5_f NMFCA2 sbgroup , fmb newey(4) 
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v6: quietly asreg monthlyρ_5_f NMFCA2 sbgroup monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace

eststo v7: quietly asreg monthlyρ_5_f NMFCA2 sbgroup NMFCAG, fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "No" , replace

eststo v8: quietly asreg monthlyρ_5_f NMFCA2 sbgroup NMFCAG monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc GroupFE "No" , replace
estadd loc controll "Yes" , replace


eststo v9: quietly asreg monthlyρ_5_f NMFCA2 sbgroup NMFCAG monthlyρ_5 sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 , fmb newey(4)
estadd loc GroupFE "Yes" , replace
estadd loc controll "Yes" , replace



esttab  v1 v2 v3 v4 v5 v6 v7 v8 v9 ,nomtitle label   s( N GroupFE controll r2 ,  lab("Observations" "Group Effect" "Controls" "$ R^2 $"))   keep(NMFCA sbgroup NMFCAG) compress order(NMFCA sbgroup NMFCAG ) 


mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Quadraticmresult2-slide.tex ,replace





 /*ّFive Lag*/
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

esttab   v0 v1 v11 v111   v13  v2 v4  v3 v5, nomtitle label   s( N GroupFE FiveLag r2 ,  lab("Observations" "Group FE" "Number of lag" "$ R^2 $"))  keep(NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership )drop( monthlyρ_5_1 monthlyρ_5_2 monthlyρ_5_3  monthlyρ_5_4 monthlyρ_5_5) order(NMFCA NMFCAG sbgroup) compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-5Lag-slide.tex ,replace




/*Bullish/Bearish */


eststo v2: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v31: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5  NMFCAG  sDown  sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v311: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5  NMFCAG  sDown sUp  sgroup monthlysamesize monthlysamebm monthlycrossownership sbgroup  , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v32: quietly asreg monthlyρ_5_f NMFCA   monthlyρ_5 Up Down sDown sUp sgroup monthlysamesize monthlysamebm monthlycrossownership sbgroup, fmb newey(4)
estadd loc Controls "No" , replace 
estadd loc Interaction  "No" , replace



eststo v30: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5  Up Down  sDown  sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace




esttab  v2  v31  v30 , nomtitle label keep(NMFCA NMFCAG sDown Down Up  sbgroup) order(NMFCA NMFCAG sbgroup) n r2    compress  mgroups("Fu. Monthly Cor. of 4F+Ind. Residuals", pattern(1)  prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Down-slide1.tex ,replace 

esttab  v2   v311  v32 , nomtitle label keep(NMFCA NMFCAG sDown Down Up sUp sbgroup) order(NMFCA NMFCAG sbgroup) n r2    compress  mgroups("Fu. Monthly Cor. of 4F+Ind. Residuals", pattern(1)  prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Down-slide2.tex ,replace





/*ln(MFCA)*/

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






/*NMFCAP*/

eststo v0: quietly asreg monthlyρ_5_f  NMFCAP , fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCAP  monthlyρ_5 , fmb newey(4)
estadd loc GroupFE "No" , replace



eststo v11: quietly asreg monthlyρ_5_f NMFCAP  monthlyρ_5 sbgroup, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v111: quietly asreg monthlyρ_5_f NMFCAP  monthlyρ_5 sbgroup NMFCAPG, fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v13: quietly asreg monthlyρ_5_f NMFCAP  monthlyρ_5  sbgroup NMFCAPG sgroup, fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCAP monthlyρ_5  sbgroup NMFCAPG  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCAP monthlyρ_5  sbgroup NMFCAPG  sgroup monthlysamesize monthlysamebm  monthlycrossownership gdummy0-gdummy47, fmb newey(4)
estadd loc GroupFE "Yes" , replace


esttab   v0 v1 v11 v111   v13   v2 v3, nomtitle label   s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $"))  keep(NMFCAP monthlyρ_5  sbgroup NMFCAPG  sgroup monthlysamesize monthlysamebm monthlycrossownership) order(NMFCAP NMFCAPG sbgroup) compress   mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Polk-slide.tex ,replace







/*NMFCAMQ3*/

 
replace median = 0 if Q <=3
replace median = 1 if Q  == 4

replace NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA} > Q3[\text{FCA}]) \times {\text{FCA} ^*}  $ "

replace sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA} > Q3[\text{FCA}]) \times {\text{SameGroup}} $ "



replace NMFCAGM = sbgroup * NMFCA * median
label variable NMFCAGM " $ (\text{FCA} > Q3[\text{FCA}]) \times  (\text{FCA}^*) \times {\text{SameGroup}} $ "


replace holder_actM = holder_act * median
label variable holder_actM " $ (\text{FCA}> Q3[\text{FCA}]) \times {\text{ActiveHolder} }  $ "

replace spositionM = sposition * median

label variable spositionM " $ (\text{FCA}> Q3[\text{FCA}]) \times {\text{Same Position} }  $ "


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


/*NMFCA Just after Q3*/

eststo v0: quietly asreg monthlyρ_5_f  NMFCA if median == 1 , fmb newey(4) 
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




/**/

replace median = forthquarter 

replace NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA} > Q3[\text{FCA}]) \times {\text{FCA} ^*}  $ "

replace sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA} > Q3[\text{FCA}]) \times {\text{SameGroup}} $ "



replace NMFCAGM = sbgroup * NMFCA * median
label variable NMFCAGM " $ (\text{FCA} > Q3[\text{FCA}]) \times  (\text{FCA}^*) \times {\text{SameGroup}} $ "


replace holder_actM = holder_act * median
label variable holder_actM " $ (\text{FCA}> Q3[\text{FCA}]) \times {\text{ActiveHolder} }  $ "

replace spositionM = sposition * median

label variable spositionM " $ (\text{FCA}> Q3[\text{FCA}]) \times {\text{Same Position} }  $ "



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


eststo v0: quietly  asreg monthlyρ_5_f  NMFCA NMFCAM sbgroup     sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 


eststo v1: quietly  asreg monthlyρ_5_f  NMFCA NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 


eststo v11: quietly  asreg monthlyρ_5_f  NMFCA NMFCAGM  sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 


eststo v2: quietly  asreg monthlyρ_5_f  NMFCA NMFCAM NMFCAG    sbgroup     sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 


 eststo v3: quietly  asreg monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 

 eststo v4: quietly  asreg monthlyρ_5_f NMFCA  NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5, fmb newey(4) 
 

 eststo v5: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 
 
 
 

esttab   v0 v1 v11 v2  v4 v5 v3   , nomtitle label  r2 n compress  keep(NMFCA NMFCAM NMFCAG NMFCAGM) mgroups("Dep. Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using QTimemresult3-slide.tex ,replace


/*NMFCA Just after Q3*/

eststo v0: quietly asreg monthlyρ_5_f  NMFCA if forthquarter == 1 , fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 if forthquarter == 1, fmb newey(4)
estadd loc GroupFE "No" , replace


eststo v11: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sgroup if forthquarter == 1, fmb newey(4) 
estadd loc GroupFE "No" , replace

eststo v111: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup sgroup if forthquarter == 1, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership if forthquarter == 1, fmb newey(4)
estadd loc GroupFE "No" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47 if forthquarter == 1, fmb newey(4)
estadd loc GroupFE "Yes" , replace




esttab   v0 v1 v11 v111   v2 v3 , nomtitle label   s( N GroupFE r2 ,  lab("Observations" "Group FE" "$ R^2 $"))  keep(NMFCA monthlyρ_5 sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership ) order(NMFCA sbgroup) compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using QTimemresult2subsanple-slide.tex ,replace


corr monthlyρ_5_f NMFCA monthlyρ_5 sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership  if median == 1





/*BigSmall*/




 eststo v0: quietly  asreg monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5 , fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5 , fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

 eststo v2: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5, fmb newey(4) 


 eststo Bv0: quietly  asreg monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5 if PairType == 2, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Bv1: quietly asreg monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5 if PairType == 2 , fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo Bv2: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup holder_act  sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5 if PairType == 2  , fmb newey(4) 


 eststo Sv0: quietly  asreg monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5 if PairType == 1, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Sv1: quietly asreg monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5 if PairType == 1 , fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo Sv2: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5 if PairType == 1  , fmb newey(5) 



eststo SBv0: quietly  asreg monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5 if PairType == 0 , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo SBv1: quietly asreg monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm  monthlycrossownership  monthlyρ_5 if PairType == 0 , fmb newey(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo SBv2: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm monthlycrossownership   monthlyρ_5 if PairType == 0  , fmb newey(4) 



esttab v0 v1 v2 Bv0 Bv1 Bv2 SBv0 SBv1 SBv2 Sv0 Sv1 Sv2  , nomtitle label n r2  compress order(NMFCA NMFCAG NMFCAM    NMFCAGM sbgroup sgroup) keep(NMFCA NMFCAM sbgroup  NMFCAG  NMFCAGM sgroup)  mgroups("All Firms" "Big Firms" "Big \& Small Firms" "Small Firms"   , pattern(1 0 0 1 0 0 1 0 0 1 0 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	,using Qmresult4-slide.tex ,replace 




/* Imbalance*/

eststo v1 :  quietly asreg monthlyρ_5_f NMFCA monthlyρ_5    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup  , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v2 :  quietly asreg monthlyρ_5_f NMFCA monthlyρ_5    sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd  , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v3 :  quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v4 :  quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace

eststo v5 :  quietly asreg monthlyρ_5_f NMFCA monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup ImbalanceSbgroupFCA gdummy0-gdummy47, fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc GroupFE "Yes" , replace

eststo v6 :  quietly asreg monthlyρ_5_f  monthlyρ_5   sgroup monthlysamesize monthlysamebm monthlycrossownership  sbgroup lowimbalancestd ImbalanceSbgroup  , fmb newey(4)
estadd loc controll "Yes" , replace
estadd loc GroupFE "No" , replace



esttab   v1 v2 v3 v6 v4 v5 , nomtitle label   keep(NMFCA sbgroup lowimbalancestd ImbalanceSbgroup ) order(NMFCA sbgroup) s( N GroupFE controll r2 ,  lab("Observations" "Group Effect" "Controls" "$ R^2 $"))compress mgroups("Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Imbalance.tex ,replace




