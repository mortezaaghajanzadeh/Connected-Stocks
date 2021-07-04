

eststo v0 : xtfmb monthlyρlag_5_f NMFCA monthlyρlag_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm , lag(4) 




/*NMFCA*/

eststo v0: quietly xtfmb monthlyρlag_5_f  NMFCA , lag(4)
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v1: quietly xtfmb monthlyρlag_5_f NMFCA  monthlyρlag_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace


eststo v11: quietly xtfmb monthlyρlag_5_f NMFCA  monthlyρlag_5 sbgroup, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v111: quietly xtfmb monthlyρlag_5_f NMFCA  monthlyρlag_5 sbgroup NMFCAG, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v13: quietly xtfmb monthlyρlag_5_f NMFCA  monthlyρlag_5 sbgroup NMFCAG sgroup, lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace

eststo v2: quietly xtfmb monthlyρlag_5_f NMFCA monthlyρlag_5 sbgroup NMFCAG  sgroup monthlysamesize monthlysamebm , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction  "No" , replace





esttab   v0 v1 v11 v111   v13  v2 , nomtitle label  n r2   compress mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using mresult2-slide-withLag.tex ,replace


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






eststo v00: quietly xtfmb monthlyρlag_5_f NMFCA , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v0: quietly xtfmb monthlyρlag_5_f  NMFCA NMFCAM , lag(4)
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v1: quietly xtfmb monthlyρlag_5_f NMFCA NMFCAM monthlyρlag_5 , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace

eststo v11: quietly xtfmb monthlyρlag_5_f NMFCA NMFCAM monthlyρlag_5 sbgroup  , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace





eststo v2: quietly xtfmb monthlyρlag_5_f NMFCA NMFCAM monthlyρlag_5    sbgroup  sgroup monthlysamesize monthlysamebm , lag(4) 
estadd loc Controls "No" , replace
estadd loc Interaction "No" , replace




esttab v00 v0 v1 v11     v2, nomtitle label  n r2 compress mgroups("Dependent Variable:Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using Qmresult2-slide-withLag.tex ,replace


/**/


eststo v0: quietly  xtfmb monthlyρlag_5_f  NMFCA NMFCAM sbgroup     sgroup monthlysamesize monthlysamebm    monthlyρlag_5, lag(4) 


eststo v1: quietly  xtfmb monthlyρlag_5_f  NMFCA NMFCAG  sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρlag_5, lag(4) 


eststo v11: quietly  xtfmb monthlyρlag_5_f  NMFCA NMFCAGM  sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρlag_5, lag(4) 


eststo v2: quietly  xtfmb monthlyρlag_5_f  NMFCA NMFCAM NMFCAG    sbgroup     sgroup monthlysamesize monthlysamebm    monthlyρlag_5, lag(4) 


 eststo v3: quietly  xtfmb monthlyρlag_5_f NMFCA NMFCAM NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρlag_5, lag(4) 

 eststo v4: quietly  xtfmb monthlyρlag_5_f NMFCA  NMFCAG NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρlag_5, lag(4) 
 

 eststo v5: quietly  xtfmb monthlyρlag_5_f NMFCA NMFCAM  NMFCAGM    sbgroup   sgroup monthlysamesize monthlysamebm    monthlyρlag_5, lag(4) 
 
 
 

esttab   v0 v1 v11 v2  v4 v5 v3   , nomtitle label  r2 n compress  keep(NMFCA NMFCAM NMFCAG NMFCAGM) mgroups("Future Monthly Correlation of 4F+Industry Residuals"   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) )  ,using Qmresult3-slide-withLag.tex ,replace




