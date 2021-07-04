clear
cls
import delimited "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\SepahWeeklyNormalzedFCAP1.1.csv", encoding(UTF-8)
cd "C:\Project\Connected Stocks\Final Report"
drop if period <-200
drop if period >100


scatter weeklyρ_5 period , xline(0) msymbol(Oh) msize(vsmall) title("Hekmat Merge")|| mband weeklyρ_5 period ,legen(label(2 "Median") label(3  "Mean") order(2))ytitle("Future fortnightly Correlation of " " 4Factor+Industry Daily Residuals")note("Note: This figure graphs the time seris of correlation of daily 4Factor+Industry residuals""in fortnight t") 


|| line mean period if tag, sort



ciplot weeklyρ_5, by(period) 


egen mean = mean(weeklyρ_5) , by(period)



graph bar mean , over(period)

twoway line mean period , sort

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




