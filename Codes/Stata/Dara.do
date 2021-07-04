clear
cls
import delimited "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\DaraWeeklyNormalzedFCAP1.1.csv", encoding(UTF-8)
cd "G:\Dropbox\Dropbox\Connected Stocks\Final Report"

summ wperiod

drop if wperiod <-20
drop if wperiod >10



scatter weeklyρ_5 wperiod  , xline(0) msymbol(Oh) msize(vsmall) || mband weeklyρ_5 wperiod ,legen(label(2 "Median") label(3  "Mean") order(2))ytitle("Future fortnightly Correlation of " " 4Factor+Industry Daily Residuals")note("Note: This figure graphs the time seris of correlation of daily 4Factor+Industry residuals""in fortnight t") 






ciplot weeklyρ_5, by(wperiod) 


egen mean = mean(weeklyρ_5) , by(wperiod)



graph bar mean , over(wperiod)

twoway line mean wperiod , sort

help mean

twoway 



sum period








graph export HekmatS.eps,replace
graph export HekmatS.png,replace


generate event = 0
replace event = 1 if period >= 0 
 


 
 
binscatter weeklyρ_5 fca ,by(event) nq(10)legend(label(1 "Before merge") label(2 "After merge")) xtitle("FCA") ytitle("Future fortnightly Correlation of " " 4Factor+Industry Daily Residuals")  msymbol(S O )   line(qfit)  title("Hekmat Merge") note("Note: This figure graphs the correlation of daily 4Factor+Industry residuals in fortnight t+1"" against  our measure of institutional connectedness.") xtitle("FCA")
graph export HekmatB.eps,replace
graph export HekmatB.png,replace

reg weeklyρ_5_f v73 event 




