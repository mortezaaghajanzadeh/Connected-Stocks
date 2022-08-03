



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


/*
BigGroupCap BigGroupTotalCFR BigGroupUoCap



eststo v0 : asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm , fmb newey(4)  

eststo v1 :asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm if (monthlyρ_5_f != 1) & (monthlyρ_5_f != -1), fmb newey(4)  

eststo v2 :asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm if (monthlyρ_5_f != 1) & (monthlyρ_5_f != -1) & (monthlyρ_5 != 1) &  (monthlyρ_5 != 1), fmb newey(4)  


esttab v0 v1 v2

*/




asreg monthlyρ_5_f NMFCA  monthlyρ_5 Up Down sDown sUp sgroup monthlysamesize monthlysamebm ,  fmb newey(4) first  save(FirstStage)



cor monthlyρ_5_f NMFCA median NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5



/*NMFCA*/

eststo v0: quietly asreg monthlyρ_5_f  NMFCA , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


eststo v11: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sgroup, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v111: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup sgroup, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v13: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 sbgroup NMFCAG sgroup, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership gdummy0-gdummy47, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

/*

eststo v3: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 holder_act NMFCAA sbgroup NMFCAG sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 holder_act NMFCAA sbgroup NMFCAG sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f NMFCA monthlyρ_5 holder_act NMFCAA sbgroup NMFCAG sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction  "Yes" , replace

*/



esttab   v0 v1 v11 v111   v13  v2 v3 , nomtitle label  n r2  keep(NMFCA monthlyρ_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm monthlycrossownership ) order(NMFCA NMFCAG sbgroup) compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-slide.tex ,replace


/*
esttab   v0 v1 v11 v111   v13  v2 , nomtitle label  n r2   compress addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (Four lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" )mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2.tex ,replace
*/




/*Down Market */


eststo v2: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5 sbgroup NMFCAG sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v31: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5  NMFCAG  sDown  sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v311: quietly asreg monthlyρ_5_f NMFCA monthlyρ_5  NMFCAG  sDown sUp  sgroup monthlysamesize monthlysamebm monthlycrossownership , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v32: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5 Up Down sDown sUp sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v30: quietly asreg monthlyρ_5_f NMFCA  monthlyρ_5  Up Down  sDown  sbgroup sgroup monthlysamesize monthlysamebm monthlycrossownership, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace




esttab  v2  v31  v30 , nomtitle label keep(NMFCA NMFCAG sDown Down Up  sbgroup) order(NMFCA NMFCAG sbgroup) n r2    compress  mgroups("Fu. Monthly Cor. of 4F+Ind. Residuals", pattern(1)  prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Down-slide1.tex ,replace 

esttab  v2   v311  v32 , nomtitle label keep(NMFCA NMFCAG sDown Down Up sUp sbgroup) order(NMFCA NMFCAG sbgroup) n r2    compress  mgroups("Fu. Monthly Cor. of 4F+Ind. Residuals", pattern(1)  prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Down-slide2.tex ,replace




/*
esttab  v2  v31 v311 v30 v32 , nomtitle label keep(NMFCA NMFCAG sDown Down Up sUp sbgroup) order(NMFCA NMFCAG sbgroup) n r2   compress  mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals", pattern(1)  prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using mresult2Down.tex ,replace
*/




/*NMFCAM*/

eststo v00: quietly asreg monthlyρ_5_f NMFCA ,  fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v0: quietly asreg monthlyρ_5_f  NMFCA NMFCAM ,  fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 ,  fmb newey(4)  
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


eststo v11: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 sbgroup  ,  fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership,  fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


/*
eststo v3: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5  holder_act   sbgroup  sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5  holder_act   sbgroup   sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM monthlyρ_5  holder_act  sbgroup   sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
*/

esttab v00 v0 v1 v11    v2, nomtitle label  n r2 compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Mmresult2-slide.tex ,replace

/*
esttab v00 v0 v1 v11     v2, nomtitle label  n r2 compress   addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (four lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" )mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Mmresult2.tex ,replace
*/
/**/


eststo v0: quietly  asreg monthlyρ_5_f  NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5,  fmb newey(4)  
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly  asreg monthlyρ_5_f  NMFCA NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5,  fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace



eststo v2: quietly  asreg monthlyρ_5_f  NMFCA NMFCAM NMFCAG    sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5,  fmb newey(4)  
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


 eststo v3: quietly  asreg monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

 eststo v4: quietly  asreg monthlyρ_5_f NMFCA  NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5,  fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

 eststo v5: quietly  asreg monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5,  fmb newey(4)  
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

esttab   v0 v1 v2  v4 v5 v3   , nomtitle label  r2 n compress  keep(NMFCA NMFCAM NMFCAG NMFCAGM    )  mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using Mmresult3-slide.tex ,replace

esttab   v0 v1 v2  v4 v3   , nomtitle label  r2 n  keep(NMFCA NMFCAM NMFCAG NMFCAGM   ) compress addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (four lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Mmresult3.tex ,replace



/***/

 eststo v0: quietly reg monthlyρ_5_f NMFCA NMFCAM   sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if month_of_year != 2 , cluster(t)
 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace
estadd loc EndOfYear "No" , replace

 eststo v01: quietly  reg monthlyρ_5_f NMFCA NMFCAM   sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm    monthlyρ_5 if month_of_year == 2 , robust
estadd loc Controls "No" , replace 
estadd loc Interaction "No" , replace
estadd loc EndOfYear "Yes" , replace




eststo v1: quietly reg monthlyρ_5_f NMFCA NMFCAM sbgroup NMFCAG    sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2  monthlyρ_5  if month_of_year != 2  , robust
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
estadd loc EndOfYear "No" , replace

eststo v11: quietly reg monthlyρ_5_f NMFCA NMFCAM sbgroup NMFCAG   sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2  monthlyρ_5 if month_of_year == 2 , robust
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
estadd loc EndOfYear "Yes" , replace

/**/
eststo v20: quietly   xtfmb monthlyρ_5_f NMFCA NMFCAM   sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if month_of_year != 2 
 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace
estadd loc EndOfYear "No" , replace

 eststo v201: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM   sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if month_of_year == 2
estadd loc Controls "No" , replace 
estadd loc Interaction "No" , replace
estadd loc EndOfYear "Yes" , replace




eststo v21: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup NMFCAG      sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2  monthlyρ_5  if month_of_year != 2 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
estadd loc EndOfYear "No" , replace

eststo v211: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup NMFCAG     sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2  monthlyρ_5 if month_of_year == 2 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace
estadd loc EndOfYear "Yes" , replace




esttab  v0 v01  v1 v11 v20 v201 v21 v211, nomtitle label  r2 s(Controls Interaction EndOfYear N r2) drop (sgroup monthlysamesize monthlysamebm monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  compress mgroups("OLS-Robust" "FM"   , pattern(1 0 0 0 1 0 0 0 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using MmresultIdent-slide.tex ,replace

esttab  v0 v01  v1 v11 v20 v201 v21 v211, nomtitle label  r2 s(Controls Interaction EndOfYear N r2) drop (sgroup monthlysamesize monthlysamebm monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  compress mgroups("OLS-Robust" "FM"   , pattern(1 0 0 0 1 0 0 0 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )   addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) ,using MmresultIdent.tex ,replace



/****/




binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("FCA*")  title("Common Pairs") by(PairType)

summ PairType


 eststo v0: quietly  xtfmb monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm    monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


 eststo Bv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Bv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace


 eststo Sv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Sv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace



eststo SBv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0 , lag(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo SBv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace



esttab v0 v1 Bv0 Bv1 SBv0 SBv1 Sv0 Sv1   , nomtitle label n r2  compress order(NMFCA NMFCAM sbgroup  NMFCAG holder_act NMFCAA  sgroup) keep(NMFCA NMFCAM sbgroup  NMFCAG holder_act NMFCAA  sgroup) mgroups("All Firms" "Big Firms" "Big \& Small Firms" "Small Firms"   , pattern(1 0 1 0 1 0 1 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	,using Mmresult4-slide.tex ,replace 




/*ln(MFCA)*/

eststo v0: quietly xtfmb monthlyρ_5_f  lnMFCA , lag(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f lnMFCA  monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


eststo v11: quietly xtfmb monthlyρ_5_f lnMFCA  monthlyρ_5 sbgroup, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v111: quietly xtfmb monthlyρ_5_f lnMFCA  monthlyρ_5 sbgroup lnMFCAG, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v13: quietly xtfmb monthlyρ_5_f lnMFCA  monthlyρ_5  sbgroup lnMFCAG sgroup, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v2: quietly xtfmb monthlyρ_5_f lnMFCA monthlyρ_5  sbgroup lnMFCAG  sgroup monthlysamesize monthlysamebm , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace






esttab   v0 v1 v11 v111     v13  v2 , nomtitle label  n r2    compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using lnmresult2-slide.tex ,replace



esttab   v0 v1 v11 v111     v13  v2 , nomtitle label  n r2    compress mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (Four lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ),using lnmresult2.tex ,replace






/*NMFCAP*/

eststo v0: quietly asreg monthlyρ_5_f  NMFCAP , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCAP  monthlyρ_5 , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace



eststo v11: quietly asreg monthlyρ_5_f NMFCAP  monthlyρ_5 sbgroup, fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v111: quietly asreg monthlyρ_5_f NMFCAP  monthlyρ_5 sbgroup NMFCAPG, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v13: quietly asreg monthlyρ_5_f NMFCAP  monthlyρ_5  sbgroup NMFCAPG sgroup, fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v2: quietly asreg monthlyρ_5_f NMFCAP monthlyρ_5  sbgroup NMFCAPG  sgroup monthlysamesize monthlysamebm , fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCAP monthlyρ_5  sbgroup NMFCAPG  sgroup monthlysamesize monthlysamebm  gdummy0-gdummy47, fmb newey(4)


/*
eststo v3: quietly xtfmb monthlyρ_5_f NMFCAP monthlyρ_5 holder_act NMFCAPA sbgroup NMFCAPG sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f NMFCAP monthlyρ_5 holder_act NMFCAPA sbgroup NMFCAPG sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction  "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f NMFCAP monthlyρ_5 holder_act NMFCAPA sbgroup NMFCAPG sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction  "Yes" , replace

*/



esttab   v0 v1 v11 v111   v13   v2 v3, nomtitle label   n r2  keep(NMFCAP monthlyρ_5  sbgroup NMFCAPG  sgroup monthlysamesize monthlysamebm) order(NMFCAP NMFCAPG sbgroup) compress   mgroups("Dependent Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2Polk-slide.tex ,replace







/**/




 
replace median = 0 if Q <=3
replace median = 1 if Q  == 4

replace NMFCAM = NMFCA * median

label variable NMFCAM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{FCA} ^*}  $ "

replace sbgroupM = sbgroup * median
label variable sbgroupM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{SameGroup}} $ "



replace NMFCAGM = sbgroup * NMFCA * median
label variable NMFCAGM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times  (\text{FCA}^*) \times {\text{SameGroup}} $ "


replace holder_actM = holder_act * median
label variable holder_actM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{ActiveHolder} }  $ "

replace spositionM = sposition * median

label variable spositionM " $ (\text{FCA}^* > Q3[\text{FCA}^*]) \times {\text{Same Position} }  $ "


corr monthlyρ_5_f monthlyρ_5  NMFCA median NMFCAM   NMFCAG NMFCAGM sbgroup  sgroup monthlysamesize monthlysamebm 





eststo v00: quietly asreg monthlyρ_5_f NMFCA , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v0: quietly asreg monthlyρ_5_f  NMFCA NMFCAM , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 , fmb newey(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v11: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5 sbgroup  , fmb newey(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace





eststo v2: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm , fmb newey(4)

estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v3: quietly asreg monthlyρ_5_f NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm  gdummy0-gdummy47, fmb newey(4)


esttab v00 v0 v1 v11   v2 v3, nomtitle label  n r2 keep(NMFCA NMFCAM monthlyρ_5    sbgroup  sgroup monthlysamesize monthlysamebm) order(NMFCA NMFCAM sbgroup) compress mgroups("Dep. Variable: Future Monthly Corr. of 4F+Ind. Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Qmresult2-slide.tex ,replace


/**/


eststo v0: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAM sbgroup     sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(4) 


eststo v1: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(4) 


eststo v11: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAGM  sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(4) 


eststo v2: quietly  xtfmb monthlyρ_5_f  NMFCA NMFCAM NMFCAG    sbgroup     sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(4) 


 eststo v3: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(4) 

 eststo v4: quietly  xtfmb monthlyρ_5_f NMFCA  NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(4) 
 

 eststo v5: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(4) 
 
 
 

esttab   v0 v1 v11 v2  v4 v5 v3   , nomtitle label  r2 n compress  keep(NMFCA NMFCAM NMFCAG NMFCAGM) mgroups("Dep. Variable: Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using Qmresult3-slide.tex ,replace

esttab   v0 v1 v2  v4 v3   , nomtitle label  r2 n   keep(NMFCA NMFCAM NMFCAG NMFCAGM    ) compress addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (four lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ) mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Qmresult3.tex ,replace



/*****/




 eststo v0: quietly  xtfmb monthlyρ_5_f NMFCA  sbgroup  NMFCAG  sgroup monthlysamesize monthlysamebm    monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

 eststo v2: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5, lag(4) 


 eststo Bv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Bv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo Bv2: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup holder_act  sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 2  , lag(4) 


 eststo Sv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo Sv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo Sv2: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 1  , lag(5) 



eststo SBv0: quietly  xtfmb monthlyρ_5_f NMFCA    sbgroup  NMFCAG    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0 , lag(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo SBv1: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM sbgroup    sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0 , lag(4) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

 eststo SBv2: quietly  xtfmb monthlyρ_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρ_5 if PairType == 0  , lag(4) 



esttab v0 v1 v2 Bv0 Bv1 Bv2 SBv0 SBv1 SBv2 Sv0 Sv1 Sv2  , nomtitle label n r2  compress order(NMFCA NMFCAM sbgroup  NMFCAG NMFCAGM sgroup) keep(NMFCA NMFCAM sbgroup  NMFCAG  NMFCAGM sgroup)  mgroups("All Firms" "Big Firms" "Big \& Small Firms" "Small Firms"   , pattern(1 0 0 1 0 0 1 0 0 1 0 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	,using Qmresult4-slide.tex ,replace 





/*

/* Same group */





eststo sv10: quietly xtfmb monthlyρ_5_f  NMFCA if sbgroup == 1 ,  lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


eststo sv11: quietly xtfmb monthlyρ_5_f  NMFCA NMFCAM if sbgroup == 1 ,  lag(5)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace


eststo sv20: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 holder_act sposition2 sgroup monthlysamesize monthlysamebm if sbgroup == 1 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo sv21: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM  monthlyρ_5 holder_act sposition2 sgroup monthlysamesize monthlysamebm  if sbgroup == 1 , lag(5) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo sv30: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 holder_act sposition2 sgroup  monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2 if sbgroup == 1 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

eststo sv31: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM  monthlyρ_5 holder_act sposition2 sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2 if sbgroup == 1 , lag(5) 
estadd loc Controls "Yes" , replace
estadd loc Interaction "Yes" , replace

esttab sv10 sv11 sv20 sv21 sv30 sv31, nomtitle s(Controls Interaction N r2 )    drop ( monthlyρ_5 monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  ,using Mmresult2Samegroup-slide.tex ,replace

esttab sv10 sv11 sv20 sv21 sv30 sv31, nomtitle  s(Controls Interaction N r2) label drop ( monthlyρ_5 monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ),using Mmresult2Samegroup.tex ,replace


/* Not Same group */



eststo v10: quietly xtfmb monthlyρ_5_f  NMFCA if sbgroup == 0 ,  lag(5)
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace


eststo v11: quietly xtfmb monthlyρ_5_f  NMFCA NMFCAM if sbgroup == 0 ,  lag(5)
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace


eststo v20: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 holder_act sposition2 sgroup monthlysamesize monthlysamebm if sbgroup == 0 , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v21: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM  monthlyρ_5 holder_act sposition2 sgroup monthlysamesize monthlysamebm  if sbgroup == 0 , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v30: quietly xtfmb monthlyρ_5_f NMFCA  monthlyρ_5 holder_act sposition2 sgroup  monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2 if sbgroup == 0 , lag(5) 
estadd loc Value "Yes" , replace
estadd loc Interaction "Yes" , replace



eststo v31: quietly xtfmb monthlyρ_5_f NMFCA NMFCAM  monthlyρ_5 holder_act sposition2 sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2 if sbgroup == 0 , lag(5) 
estadd loc Value "Yes" , replace
estadd loc Interaction "Yes" , replace

esttab v10 v11 v20 v21 v30 v31, nomtitle s(Value Interaction N r2)  label drop ( monthlyρ_5 monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  ,using Mmresult2NotSamegroup-slide.tex ,replace

esttab v10 v11 v20 v21 v30 v31, nomtitle    s(Value Interaction N r2) label drop ( monthlyρ_5 monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)   addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ),using Mmresult2NotSamegroup.tex ,replace


/*Aggregate*/
esttab v10 v11 v20 v21 v30 v31 sv10 sv11 sv20 sv21 sv30 sv31  ,nomtitle label  r2 s(Value Interaction N r2)   drop (sgroup monthlysamesize monthlysamebm monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  mgroups("Different Group" "Same Group"   , pattern(1 0 0 0 0 0 1 0 0 0 0 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )	,using Mmresult2bothSamegroup-slide.tex ,replace 



/*Compare*/

suest sv1 v1 

Simultaneous results for sv1 ,v1 


test [sv1]NMFCAM = [v1]NMFCAM
*/
/*
/*NMFCA2*/

eststo v00: quietly xtfmb monthlyρ_5_f NMFCA , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace
eststo v0: quietly xtfmb monthlyρ_5_f  NMFCA NMFCA2 , lag(5)
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v2: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 holder_act sbgroup monthlysamesize monthlysamebm , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "No" , replace

eststo v3: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 holder_act sbgroup sgroup monthlysize1 monthlysize2 monthlybm1 monthlybm2 , lag(5) 
estadd loc Value "Yes" , replace
estadd loc Interaction "No" , replace

eststo v4: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 holder_act sbgroup sgroup monthlysamesize  monthlysamebm msbm1bm2 msize1size2 , lag(5) 
estadd loc Value "No" , replace
estadd loc Interaction "Yes" , replace

eststo v5: quietly xtfmb monthlyρ_5_f NMFCA NMFCA2 monthlyρ_5 holder_act sbgroup sgroup monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2  msbm1bm2 , lag(5) 
estadd loc Value "Yes" , replace
estadd loc Interaction "Yes" , replace

esttab v00 v0 v1  v3 v5 v4  v2, nomtitle label  r2 s(Value Interaction N r2) drop (monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  ,using mresult2-slide.tex ,replace

esttab v00 v0 v1  v3 v5 v4  v2, nomtitle label  r2 s(Value Interaction N r2) drop (monthlysize1 monthlysize2 msize1size2 monthlybm1 monthlybm2 msbm1bm2)  addnotes("This table reports Fama and MacBeth (1973) estimates of monthly cross-sectional" " regressions forecasting the correlation of daily 4Factor+Industry residuals in month t + 1 for each pairs." "The independent variables are updated monthly and include our measure of institutional connectedness," " FCA and a series of controls at time t." "We measure the negative of the absolute value of the difference in size ranking across the two stocks in the pair $ \text{Samesize}_{ij,t} $." "We also capture the similarity in business group by dummy of sgroup." "Independent variables which  we denote with * are rank-transformed and normalized to have unit standard deviation." " We calculate Newey and West (1987) standard errors (five lags) of the Fama and MacBeth (1973) estimates " " that take into account autocorrelation in the cross-sectional slopes" ),using mresult2.tex ,replace

*/










