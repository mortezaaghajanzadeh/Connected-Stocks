cls
clear
// import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\TurnOver_1400_06_28.csv", encoding(UTF-8) 

import delimited "E:\RA_Aghajanzadeh\Data\Connected_Stocks\TurnOver_1400_06_28.csv", encoding(UTF-8) 


// cd "D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Final Report\Output"



xtset  t regidyear
gen lnmarketcap = ln(marketcap)
label variable lnmarketcap " $ \ln(\text{size})_{i,t} $ "

label variable deltatrun " $ \Delta \text{TurnOver} $ "

replace return = return * return

label variable deltagroup " $ \Delta \text{TurnOver}_{\text{Group,-i}} $ "
label variable deltamarket " $ \Delta \text{TurnOver}_{\text{Market}} $ "
label variable deltaindustry " $ \Delta \text{TurnOver}_{\text{Industry-i}} $ "



cd "E:\RA_Aghajanzadeh\Data\Connected_Stocks"

quietly asreg deltatrun deltamarket deltagroup deltaindustry lnmarketcap    lagdeltagroup leaddeltagroup lagdeltaindustry leaddeltaindustry lagdeltamarket leaddeltamarket,fmb newey(7) first  save(FirstStageTurnover)

// cd "D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Final Report\Output"

eststo v1: quietly asreg deltatrun deltamarket deltaindustry   , fmb newey(7)
estadd loc weight "-" , replace
estadd loc control "No",replace

eststo v11: quietly asreg deltatrun deltamarket deltaindustry   lnmarketcap lagdeltamarket leaddeltamarket  lagdeltaindustry leaddeltaindustry , fmb newey(7)
estadd loc weight "-" , replace
estadd loc control "Yes",replace



/*
eststo v2: quietly asreg deltatrun deltamarket deltagroup deltaindustry lnmarketcap   , fmb newey(7)
estadd loc weight " $ \text{MC} \times \text{CR} $ " , replace
estadd loc control "No",replace

eststo v21: quietly asreg deltatrun deltamarket deltagroup deltaindustry lnmarketcap    lagdeltagroup leaddeltagroup lagdeltaindustry leaddeltaindustry lagdeltamarket leaddeltamarket, fmb newey(7)
estadd loc weight " $ \text{MC} \times \text{CR} $ " , replace
estadd loc control "Yes",replace
*/




replace deltagroup = delta_justmarketgroup

eststo v3: quietly asreg deltatrun deltamarket deltagroup deltaindustry lnmarketcap   , fmb newey(7)
estadd loc weight " $ \text{MC} $ " , replace
estadd loc control "No",replace

replace lagdeltagroup = lagdelta_justmarketgroup 
replace leaddeltagroup = leaddelta_justmarketgroup

eststo v31: quietly asreg deltatrun deltamarket deltagroup deltaindustry lnmarketcap   lagdeltagroup leaddeltagroup lagdeltaindustry leaddeltaindustry lagdeltamarket leaddeltamarket, fmb newey(7)
estadd loc weight " $ \text{MC} $ " , replace
estadd loc control "Yes",replace

asreg deltatrun deltamarket deltagroup deltaindustry lnmarketcap   lagdeltagroup leaddeltagroup lagdeltaindustry leaddeltaindustry lagdeltamarket leaddeltamarket, fmb newey(7)

  
  

esttab v1 v11 /*v2 v21*/ v3 v31, n r2 label s(  weight control N r2 ,  lab( "Portfo. Weight " "Control" "Observations" "$ R^2 $")) nomtitle keep(deltamarket deltagroup deltaindustry) order(deltamarket  deltaindustry deltagroup ) mgroups("Dependent Variable: $\Delta \text{TurnOver}_{i} $ "   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ) ,using turnover.tex ,replace







/*Amihud Value*/

label variable delta_amihud " $ \Delta \text{Amihud} $ "

label variable delta_amihud_group " $ \Delta \text{Amihud}_{\text{Group}} $ "
label variable delta_amihud_market " $ \Delta \text{Amihud}_{\text{Market}} $ "
label variable delta_amihud_industry " $ \Delta \text{Amihud}_{\text{Industry}} $ "


 


eststo v1: quietly asreg delta_amihud delta_amihud_market lnmarketcap delta_amihud_industry ,fmb newey(7)
estadd loc weight "-" , replace
estadd loc control "No" , replace

eststo v11: quietly asreg delta_amihud delta_amihud_market lnmarketcap delta_amihud_industry mreturn lagmreturn leadmreturn return lagdelta_amihud_market leaddelta_amihud_market  lagdelta_amihud_industry leaddelta_amihud_industry,fmb newey(7)
estadd loc weight "-" , replace
estadd loc control "Yes" , replace

eststo v2: quietly asreg delta_amihud delta_amihud_market delta_amihud_group lnmarketcap delta_amihud_industry ,fmb newey(7)
estadd loc weight " $ \text{MC} \times \text{CR} $ " , replace
estadd loc control "No" , replace

eststo v21: quietly asreg delta_amihud delta_amihud_market delta_amihud_group lnmarketcap delta_amihud_industry mreturn lagmreturn leadmreturn return lagdelta_amihud_market leaddelta_amihud_market lagdelta_amihud_group leaddelta_amihud_group lagdelta_amihud_industry leaddelta_amihud_industry,fmb newey(7)
estadd loc weight " $ \text{MC} \times \text{CR} $ " , replace
estadd loc control "Yes" , replace


// cd "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks"
cd "E:\RA_Aghajanzadeh\Data\Connected_Stocks"

quietly asreg delta_amihud delta_amihud_market delta_amihud_group lnmarketcap delta_amihud_industry mreturn lagmreturn leadmreturn return lagdelta_amihud_market leaddelta_amihud_market leaddelta_amihud_marketgroup lagdelta_amihud_marketgroup lagdelta_amihud_industry leaddelta_amihud_industry,fmb newey(7) first  save(FirstStageAmihud)

// cd "D:\Dropbox\Connected Stocks\Connected-Stocks\Final Report"
cd "E:\RA_Aghajanzadeh\GitHub\Connected-Stocks\Final Report\Output"


replace delta_amihud_group = delta_amihud_justmarketgr

eststo v3: quietly asreg delta_amihud delta_amihud_market delta_amihud_group lnmarketcap delta_amihud_industry  ,fmb newey(7)
estadd loc weight " $ \text{MC} $ " , replace
estadd loc control "No" , replace
 
eststo v31: quietly asreg delta_amihud delta_amihud_market delta_amihud_group lnmarketcap delta_amihud_industry mreturn lagmreturn leadmreturn return lagdelta_amihud_market leaddelta_amihud_market leaddelta_amihud_marketgroup lagdelta_amihud_marketgroup lagdelta_amihud_industry leaddelta_amihud_industry,fmb newey(7)
estadd loc weight " $ \text{MC} $ " , replace
estadd loc control "Yes" , replace
  

  
  

// esttab v1 v11 v2 v21 v3 v31,n r2 label s( N weight control r2 ,  lab("Observations" "Weight " "Control" "$ R^2 $")) nomtitle order(delta_amihud_market delta_amihud_group delta_amihud_industry lnmarketcap) keep(delta_amihud_market delta_amihud_group delta_amihud_industry) mgroups("Dependent Variable: $\Delta \text{Amihud}_{i} $ "   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using Amihud.tex ,replace




/*
/*Amihud Volume*/

label variable delta_amihud_volume " $ \Delta \text{Amihud}_{\text{volume}} $ "

label variable delta_amihud_volumegroup " $ \Delta \text{Amihud}_{\text{volume},\text{Group}} $ "
label variable delta_amihud_volumemarket " $ \Delta \text{Amihud}_{\text{volume},\text{Market}} $ 
label variable delta_amihud_volumeindustry " $ \Delta \text{Amihud}_{\text{volume},\text{Industry}} $ "

eststo v1: quietly asreg delta_amihud_volume delta_amihud_volumemarket delta_amihud_volumeindustry lnmarketcap ,fmb newey(7)
estadd loc weight "-" , replace


eststo v2: quietly asreg delta_amihud_volume delta_amihud_volumemarket delta_amihud_volumegroup lnmarketcap delta_amihud_volumeindustry ,fmb newey(7)
estadd loc weight " $ \text{MC} \times \text{CR} $ " , replace

asreg delta_amihud_volume delta_amihud_volumemarket delta_amihud_volumegroup lnmarketcap delta_amihud_volumeindustry mreturn lagmreturn leadmreturn return  legdelta_amihud_volumemarket leaddelta_amihud_volumemarket legdelta_amihud_volumegroup leaddelta_amihud_volumegroup legdelta_amihud_volumeindustry leaddelta_amihud_volumeindustry,fmb newey(7)




replace delta_amihud_volumegroup = delta_amihud_volume_justmarketgr

eststo v3: quietly asreg delta_amihud_volume delta_amihud_volumemarket delta_amihud_volumegroup lnmarketcap delta_amihud_volumeindustry,fmb newey(7)
estadd loc weight " $ \text{MC} $ " , replace

  



  

esttab v1 v2 v3 ,n r2 label s( N weight  r2 ,  lab("Observations" "Weight " "$ R^2 $")) nomtitle order( delta_amihud_volumemarket delta_amihud_volumegroup delta_amihud_volumeindustry lnmarketcap)  mgroups("Dependent Variable: $\Delta \text{Amihud}_{i} $ "   , pattern(1 ) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using AmihudVolume.tex ,replace



*/


