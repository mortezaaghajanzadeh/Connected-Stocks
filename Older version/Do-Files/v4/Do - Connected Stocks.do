clear 
cls
import delimited "C:\Project\Connected Stocks\NormalzedFCAP3.1.csv", encoding(UTF-8) 

cd "C:\Project\Connected Stocks\Final Report"

label define sgroup 0 "No" 1 "Yes"




label values sgroup sgroup

label variable weeklysize1 "WSize1"
label variable weeklysize2 "WSize2"
label variable weeklyρ_4_f "WForwardCorr"
label variable weeklyρ_4 "WCorr"
label variable weeklysamesize "WSamesize"

label variable monthlysize1 "MSize1"
label variable monthlysize2 "MSize2"
label variable monthlyρ_4_f "MForwardCorr"
label variable monthlyρ_4 "MCorr"
label variable monthlysamesize "MSamesize"




rename fcap NFCAP
rename monthlyfcap NMFCAP

rename v60 NFCA
rename v61 NWFCA
rename v62 NMFCA

rename fca FCA

generate size1size2 =  size1 * size2


summ id

xtset id t 

eststo v0: quietly asreg weeklyρ_4_f NFCA , fmb

eststo v1: quietly asreg weeklyρ_4_f NFCA weeklyρ_4 , fmb

eststo v2: quietly asreg weeklyρ_4_f NFCA weeklyρ_4  sgroup samesize , fmb

eststo v3: quietly asreg weeklyρ_4_f NFCA weeklyρ_4  sgroup size1 size2 , fmb

eststo v4: quietly asreg weeklyρ_4_f NFCA weeklyρ_4  sgroup samesize size1size2 , fmb

eststo v5: quietly asreg weeklyρ_4_f NFCA weeklyρ_4  sgroup size1 size2 size1size2 , fmb

esttab v0 v1 v2 v3 v4 v5,drop(_cons) label nomtitle  ,using wdfamaresult.tex ,replace




eststo v0: quietly asreg monthlyρ_4_f NFCA , fmb

eststo v1: quietly asreg monthlyρ_4_f NFCA monthlyρ_4 , fmb

eststo v2: quietly asreg monthlyρ_4_f NFCA monthlyρ_4  sgroup samesize , fmb

eststo v3: quietly asreg monthlyρ_4_f NFCA monthlyρ_4  sgroup size1 size2 , fmb

eststo v4: quietly asreg monthlyρ_4_f NFCA monthlyρ_4  sgroup samesize size1size2 , fmb

eststo v5: quietly asreg monthlyρ_4_f NFCA monthlyρ_4  sgroup size1 size2 size1size2 , fmb

esttab v0 v1 v2 v3 v4 v5,drop(_cons) label nomtitle  ,using mdfamaresult.tex ,replace








//egen tag = tag(id)
//egen distinct = total(tag), by(t)
//su distinct





//drop year
//gen year = floor(jalalidate/10000)

//sort id year , stable

//drop dup
//quietly by id year : gen dup = cond(_N==1,0,_n)
//drop if dup > 1









//sort id dup
//sort year
//by year: sum(dup)



