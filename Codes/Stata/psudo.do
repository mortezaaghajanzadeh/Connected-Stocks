cls
clear
 import excel "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\RandomBusinessGroupResult.xlsx", sheet("Sheet1") firstrow

  cd "G:\Dropbox\Dropbox\Connected Stocks\Final Report"
 
  twoway histogram SBFCA if A == "tstat" ,color(navy*.75)  || kdensity SBFCA if A == "tstat",xlab(0(2)15) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Business Group.")  legend(label(2 "Kernel Density")) title("FCA{sup:*} * SameGroup") xline(1, lwidth(14) lc(gs12))  xline( 2, lcolor(black) lpattern(dash)) 
  
  
graph export BusinessPseudoSBFCA_t.eps,replace
graph export BusinessPseudoSBFCA_t.png,replace

  twoway histogram SBFCA if A == "mean" ,color(navy*.75)  || kdensity SBFCA if A == "mean", ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same ""Business Group.")  legend(label(2 "Kernel Density")) title("FCA{sup:*} * SameGroup")
  
  
graph export BusinessPseudoSBFCA.eps,replace
graph export BusinessPseudoSBFCA.png,replace





  twoway histogram MNMFCA if A == "tstat" ,color(navy*.75)  || kdensity MNMFCA if A == "tstat",xlab(-2(2)8) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Business Group.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} ")  xline(0, lwidth(43) lc(gs12))  xline(-2 2, lcolor(black) lpattern(dash)) 
  
  
  
  
graph export BusinessPseudoMNMFCA_t.eps,replace
graph export BusinessPseudoMNMFCA_t.png,replace



  twoway histogram MNMFCA if A == "mean" ,color(navy*.75)  || kdensity MNMFCA if A == "mean",xlab(-0.005(0.005)0.025) ylab(,angle(0)) ytitle("Density")note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same ""Business Group.")   legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} ")
  
  
  
graph export BusinessPseudoMNMFCA.eps,replace
graph export BusinessPseudoMNMFCA.png,replace


  twoway histogram MNMFCABG if A == "tstat" ,color(navy*.75)  || kdensity MNMFCABG if A == "tstat",xlab(-4(2)10) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Business Group.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} * SameGroup ")  xline(0, lwidth(29) lc(gs12))  xline(-2 2, lcolor(black) lpattern(dash)) 
  
  
  
  
graph export BusinessPseudoMNMFCABG_t.eps,replace
graph export BusinessPseudoMNMFCABG_t.png,replace



  twoway histogram MNMFCABG if A == "mean" ,color(navy*.75)  || kdensity MNMFCABG if A == "mean", xlab(-0.05(0.05)0.125)ylab(,angle(0)) ytitle("Density")  note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same ""Business Group.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} * SameGroup ")
  
  
  
graph export BusinessPseudoMNMFCABG.eps,replace
graph export BusinessPseudoMNMFCABG.png,replace



/********/


cls
clear
 import excel "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\RandomSizeResult.xlsx", sheet("Sheet1") firstrow

  cd "G:\Dropbox\Dropbox\Connected Stocks\Final Report"
 
  twoway histogram SBFCA if A == "tstat" ,color(navy*.75)  || kdensity SBFCA if A == "tstat",xlab(-3.5(1)3.5) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Size.")  legend(label(2 "Kernel Density")) title("FCA{sup:*} * Same Business Group") xline(0, lwidth(65) lc(gs12))  xline(-2 2, lcolor(black) lpattern(dash)) 
  
  
graph export SizePseudoSBFCA_t.eps,replace
graph export SizePseudoSBFCA_t.png,replace

  twoway histogram SBFCA if A == "mean" ,color(navy*.75)  || kdensity SBFCA if A == "mean", ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same Size.")  legend(label(2 "Kernel Density")) title("FCA{sup:*} * SameGroup")
  
  
graph export SizePseudoSBFCA.eps,replace
graph export SizePseudoSBFCA.png,replace





  twoway histogram MNMFCA if A == "tstat" ,color(navy*.75)  || kdensity MNMFCA if A == "tstat",xlab(-4(2)4) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Size.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} ")  xline(0, lwidth(56) lc(gs12))  xline(-2 2, lcolor(black) lpattern(dash)) 
  
  
  
  
graph export SizePseudoMNMFCA_t.eps,replace
graph export SizePseudoMNMFCA_t.png,replace



  twoway histogram MNMFCA if A == "mean" ,color(navy*.75)  || kdensity MNMFCA if A == "mean",xlab(-0.01(0.005)0.01) ylab(,angle(0)) ytitle("Density")note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same Size.")   legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} ")
  
  
  
graph export SizePseudoMNMFCA.eps,replace
graph export SizePseudoMNMFCA.png,replace


  twoway histogram MNMFCABG if A == "tstat" ,color(navy*.75)  || kdensity MNMFCABG if A == "tstat",xlab(-4(1)3) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Size.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} * SameGroup")  xline(0, lwidth(65) lc(gs12))  xline(-2 2, lcolor(black) lpattern(dash)) 
  
  
  
  
graph export SizePseudoMNMFCABG_t.eps,replace
graph export SizePseudoMNMFCABG_t.png,replace



  twoway histogram MNMFCABG if A == "mean" ,color(navy*.75)  || kdensity MNMFCABG if A == "mean", xlab(-0.03(0.01)0.03)ylab(,angle(0)) ytitle("Density")  note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same Size.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} * SameGroup")
  
  
  
graph export SizePseudoMNMFCABG.eps,replace
graph export SizePseudoMNMFCABG.png,replace




/********/


cls
clear
 import excel "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\RandomIndustryResult.xlsx", sheet("Sheet1") firstrow

  cd "G:\Dropbox\Dropbox\Connected Stocks\Final Report"
 
  twoway histogram SBFCA if A == "tstat" ,color(navy*.75)  || kdensity SBFCA if A == "tstat",xlab(-8(2)7) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Industry.")  legend(label(2 "Kernel Density")) title("FCA{sup:*} * Same Business Group") xline(0, lwidth(30) lc(gs12))  xline(-2 2, lcolor(black) lpattern(dash)) 
  
  
graph export IndustryPseudoSBFCA_t.eps,replace
graph export IndustryPseudoSBFCA_t.png,replace

  twoway histogram SBFCA if A == "mean" ,color(navy*.75)  || kdensity SBFCA if A == "mean", ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same Industry.")  legend(label(2 "Kernel Density")) title("FCA{sup:*} * SameGroup")
  
  
graph export IndustryPseudoSBFCA.eps,replace
graph export IndustryPseudoSBFCA.png,replace





  twoway histogram MNMFCA if A == "tstat" ,color(navy*.75)  || kdensity MNMFCA if A == "tstat",xlab(-4(2)4) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Industry.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} ")  xline(0, lwidth(51) lc(gs12))  xline(-2 2, lcolor(black) lpattern(dash)) 
  
  
  
  
graph export IndustryPseudoMNMFCA_t.eps,replace
graph export IndustryPseudoMNMFCA_t.png,replace



  twoway histogram MNMFCA if A == "mean" ,color(navy*.75)  || kdensity MNMFCA if A == "mean",xlab(-0.01(0.005)0.01) ylab(,angle(0)) ytitle("Density")note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same Industry.")   legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} ")
  
  
  
graph export IndustryPseudoMNMFCA.eps,replace
graph export IndustryPseudoMNMFCA.png,replace


  twoway histogram MNMFCABG if A == "tstat" ,color(navy*.75)  || kdensity MNMFCABG if A == "tstat",xlab(-5(1)4) ylab(,angle(0)) ytitle("Density") note("This figure graphs the histogram of t statistics of coefficient of 100 Random Psudo ""pairs from same Industry.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} * SameGroup")  xline(0, lwidth(48) lc(gs12))  xline(-2 2, lcolor(black) lpattern(dash)) 
  
  
  
  
graph export IndustryPseudoMNMFCABG_t.eps,replace
graph export IndustryPseudoMNMFCABG_t.png,replace



  twoway histogram MNMFCABG if A == "mean" ,color(navy*.75)  || kdensity MNMFCABG if A == "mean", xlab(-0.04(0.01)0.03)ylab(,angle(0)) ytitle("Density")  note("This figure graphs the histogram of coefficient of 100 Random Psudo pairs from same Industry.")  legend(label(2 "Kernel Density")) title("(FCA{sup:*} > Q3[FCA{sup:*}]) * FCA{sup:*} * SameGroup")
  
  
  
graph export IndustryPseudoMNMFCABG.eps,replace
graph export IndustryPseudoMNMFCABG.png,replace