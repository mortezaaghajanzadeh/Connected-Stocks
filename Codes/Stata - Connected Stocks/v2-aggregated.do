

clear
cls
use "D:\Dropbox\Python Codes\Mohammad\results\aggregated_dead.dta"
xtset id period
gen effect = treatment * Event
replace Location = log(Location)

eststo v1: quietly regress Location treatment Event effect /*i.t*/ 
eststo v2: quietly regress Location treatment Event effect /*i.t*/ if abs(period) < 90
eststo v3: quietly regress Location treatment Event effect /*i.t*/ if abs(period) < 180

esttab    v1 v3 v2   ,nomtitle label  star(* 0.10 ** 0.05 *** 0.01)  b(%5.2f)  
esttab    v1 v3 v2   ,nomtitle label  star(* 0.10 ** 0.05 *** 0.01)  b(%5.2f)  ,using aggregated_dead.csv , replace



clear
use "D:\Dropbox\Python Codes\Mohammad\results\aggregated.dta"
xtset id period
gen effect = treatment * Event
replace Location = log(Location)


eststo v1: quietly regress Location treatment Event effect /*i.t*/ 
eststo v2: quietly regress Location treatment Event effect /*i.t*/ if abs(period) < 90
eststo v3: quietly regress Location treatment Event effect /*i.t*/ if abs(period) < 180

esttab    v1 v3 v2   ,nomtitle label star(* 0.10 ** 0.05 *** 0.01)  b(%5.2f)
esttab    v1 v3 v2  ,nomtitle label star(* 0.10 ** 0.05 *** 0.01)  b(%5.2f), using aggregated.csv , replace

clear
use "D:\Dropbox\Python Codes\Mohammad\results\aggregated_damage.dta"
xtset id period
gen effect = treatment * Event
replace Location = log(Location)

eststo v1: quietly regress Location treatment Event effect /*i.t*/ 
eststo v2: quietly regress Location treatment Event effect /*i.t*/ if abs(period) < 90
eststo v3: quietly regress Location treatment Event effect /*i.t*/ if abs(period) < 180

esttab    v1 v3 v2   ,nomtitle label  star(* 0.10 ** 0.05 *** 0.01)  b(%5.2f)  
esttab    v1 v3 v2   ,nomtitle label  star(* 0.10 ** 0.05 *** 0.01)  b(%5.2f)  ,using aggregated_damage.csv , replace

clear
use "D:\Dropbox\Python Codes\Mohammad\results\aggregated_injuries.dta"
xtset id period
gen effect = treatment * Event
replace Location = log(Location)

eststo v1: quietly regress Location treatment Event effect /*i.t*/ 
eststo v2: quietly regress Location treatment Event effect /*i.t*/ if abs(period) < 90
eststo v3: quietly regress Location treatment Event effect /*i.t*/ if abs(period) < 180

esttab    v1 v3 v2   ,nomtitle label  star(* 0.10 ** 0.05 *** 0.01)  b(%5.2f)  
esttab    v1 v3 v2   ,nomtitle label  star(* 0.10 ** 0.05 *** 0.01)  b(%5.2f)  ,using aggregated_injuries.csv , replace