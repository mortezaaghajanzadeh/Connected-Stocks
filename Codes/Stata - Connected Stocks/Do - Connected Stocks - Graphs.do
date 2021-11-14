
/***/
summ MFCA monthlyfcap


twoway kdensity MFCA if sbgroup == 0|| kdensity MFCA if sbgroup == 1



/**/

twoway histogram MFCA ,color(navy*.5) bin(20)  || kdensity MFCA ,title("Density of MFCA") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistFCA.eps,replace
graph export MHistFCA.png,replace


twoway histogram monthlyfcapf ,color(navy*.5) bin(20)  || kdensity monthlyfcapf ,title("Density of FCAP") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistFCAP.eps,replace
graph export MHistFCAP.png,replace


twoway histogram NMFCA ,color(navy*.5) bin(20)  || kdensity NMFCA ,title("Density of MFCA*") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistNFCA.eps,replace
graph export MHistNFCA.png,replace


twoway histogram NMFCAP ,color(navy*.5) bin(20)  || kdensity NMFCAP ,title("Density of FCAP*") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistNFCAP.eps,replace
graph export MHistNFCAP.png,replace


twoway histogram lnMFCA ,color(navy*.5) bin(20)  || kdensity lnMFCA ,title("Density of ln(MFCA)") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistlnFCA.eps,replace
graph export MHistlnFCA.png,replace

twoway histogram lnMFCAP ,color(navy*.5) bin(20)  || kdensity lnMFCAP ,title("Density of ln(FCAP)") ytitle("Density" )  legend(label(2 "Kernel Density"))

graph export MHistlnFCAP.eps,replace
graph export MHistlnFCAP.png,replace






 

 /*
binscatter monthlyρ_2_f NMFCA,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) by (sgroup) legend(pos(4) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) note("Note: This figure graphs the correlation of daily CAPM+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCA*")title("Common Pairs")
graph export mcorr2g.eps,replace
graph export mcorr2g.png,replace
*/
/*
binscatter monthlyρ_4_f NMFCA ,ytitle("Future monthly Correlation of " " 4Factor Daily Residuals")   nquantiles(100) by (sgroup) legend(pos(3) ring(0) col(1)label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) note("This figure graphs the correlation of daily 4Factor residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCA*") title("Common Pairs")

graph export mcorr4g.eps,replace
graph export mcorr4g.png,replace
*/



binscatter monthlyρ_5_f NMFCAP, ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("FCAP*")title("Common Pairs")
graph export mcorr5Polk.eps,replace
graph export mcorr5Polk.png,replace



binscatter monthlyρ_5_f NMFCA, ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) by (sgroup) legend(pos(4) ring(0) col(1) label(1 "Separate Industry") label(2 "Same Industry") ) msymbol(Th S)  note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("MFCA*")title("Common Pairs")
graph export mcorr5g.eps,replace
graph export mcorr5g.png,replace


binscatter monthlyρ_5_f NMFCA, ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) by (sbgroup) legend(pos(4) ring(0) col(1) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S)  note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against normalized rank transformed of our measure of institutional connectedness.") xtitle("MFCA*")title("Common Pairs")
graph export mcorr5bg.eps,replace
graph export mcorr5bg.png,replace

binscatter monthlyρ_5_f NMFCA, ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("MFCA*") line(qfit)title("Common Pairs")
graph export mcorr5.eps,replace
graph export mcorr5.png,replace


binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("MFCA*")  title("Common Pairs") 
graph export mcorr5l.eps,replace
graph export mcorr5l.png,replace









binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in median") xtitle("MFCA*")  title("Common Pairs") rd(0)
graph export mcorr5lrd.eps,replace
graph export mcorr5lrd.png,replace

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in median") xtitle("MFCA*")  title("Common Pairs") rd(0) by(holder_act)  legend( ring(1) col(2) label(2 "Active Holder") label(1 "Passive Holder") ) msymbol(Th S) 

graph export mcorr5lrda.eps,replace
graph export mcorr5lrda.png,replace

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in median") xtitle("MFCA*")  title("Common Pairs") rd(0) by(sbgroup)  legend( ring(1) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) 
graph export mcorr5lrdbg.eps,replace
graph export mcorr5lrdbg.png,replace



/**/


sum NMFCA if forthquarter == 1

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in fourth quarter") xtitle("MFCA*")  title("Common Pairs") rd(0.8659935)
graph export Qmcorr5lrd.eps,replace
graph export Qmcorr5lrd.png,replace

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in fourth quarter") xtitle("MFCA*")  title("Common Pairs") rd(0.8659935) by(holder_act)  legend( ring(1) col(2) label(2 "Active Holder") label(1 "Passive Holder") ) msymbol(Th S) 

graph export Qmcorr5lrda.eps,replace
graph export Qmcorr5lrda.png,replace

binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in fourth quarter") xtitle("MFCA*")  title("Common Pairs") rd(0.8659935) by(sbgroup)  legend( ring(1) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) 
graph export Qmcorr5lrdbg.eps,replace
graph export Qmcorr5lrdbg.png,replace

/**/
binscatter monthlyρ_5_f NMFCA,  ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.")xtitle("MFCA*")  title("Common Pairs") by(holder_act)  legend( ring(1) col(2) label(2 "Active Holder") label(1 "Passive Holder") ) msymbol(Th S) line(qfit)

graph export mcorr5a.eps,replace
graph export mcorr5a.png,replace


binscatter monthlyρ_5_f MFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) xscale(log) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("MFCA") title("Common Pairs") legend( ring(0) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S)  by(sbgroup)
graph export mcorr50bg.eps,replace
graph export mcorr50bg.png,replace



binscatter monthlyρ_5_f MFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) xscale(log) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("MFCA") title("Common Pairs") 
graph export mcorr50.eps,replace
graph export mcorr50.png,replace



binscatter monthlyρ_5_f lnMFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("Ln(MFCA)") title("Common Pairs")
graph export mcorr50Ln.eps,replace
graph export mcorr50Ln.png,replace


binscatter monthlyρ_5_f lnMFCA ,ytitle("{&rho} {sub:ij,t+1}") nquantiles(100) note("This figure graphs the correlation of daily 4Factor+Industry residuals in monthh t+1"" against our measure of institutional connectedness.") xtitle("Ln(MFCA)") title("Common Pairs") legend( ring(0) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S)  by(sbgroup)
graph export mcorr50LnSb.eps,replace
graph export mcorr50LnSb.png,replace



binscatter monthlyρ_5_f NMFCA , ytitle("{&rho} {sub:ij,t+1}")  note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness.") xtitle("MFCA*")  title("Common Pairs") by(PairType) legend(col(3))  nquantiles(20)
graph export mcorrPairType.eps,replace
graph export mcorrPairType.png,replace


hist NMFCA  if PairType == 0,xtitle("MFCA*")title("Hybrid")

graph export HybridNMFCAHist.eps,replace
graph export HybridNMFCAHist.png,replace

hist NMFCA  if PairType == 1,xtitle("MFCA*")title("Small")

graph export SmallNMFCAHist.eps,replace
graph export SmallNMFCAHist.png,replace

hist NMFCA  if PairType == 2,xtitle("MFCA*")title("Large")

graph export BigNMFCAHist.eps,replace
graph export BigNMFCAHist.png,replace



binscatter monthlyρ_5_f NMFCA if NMFCA >= 0.8659935 , ytitle("{&rho} {sub:ij,t+1}") nquantiles(20) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in fourth quarter") xtitle("MFCA*")  title("Common Pairs") by(sbgroup)  legend( ring(1) col(2) label(1 "Separate Group") label(2 "Same Group") ) msymbol(Th S) 
graph export Qmcorr5lrdbgsubsample.eps,replace
graph export Qmcorr5lrdbgsubsample.png,replace

binscatter monthlyρ_5_f NMFCA if NMFCA >= 0.8659935 , ytitle("{&rho} {sub:ij,t+1}") nquantiles(40) note("This figure graphs the correlation of daily 4Factor+Industry residuals in month t+1"" against our measure of institutional connectedness. Allow for discontinuity in fourth quarter") xtitle("MFCA*")  title("Common Pairs")  
graph export Qmcorr5subsample.eps,replace
graph export Qmcorr5subsample.png,replace
