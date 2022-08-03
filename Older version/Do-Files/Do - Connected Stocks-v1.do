clear
import delimited "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Project\Connected Stocks\NormalzedFCAP3.1.csv", encoding(UTF-8) 


//use "Connected Stocks.dta"


cd "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Project\Connected Stocks\Report"

label define sgroup 0 "No" 1 "Yes"
label values sgroup sgroup



summ 










gen Future4FactorResiduals = ρ4_f

binscatter Future4FactorResiduals fcapf, by (sgroup)  nquantiles(100) controls(size1 size2 samesize ) legend(pos(5) ring(0) col(1)) ytitle("Future Correlation of 4F Residuals")

graph export mygraph.eps,replace
graph export mygraph.png,replace

binscatter Future4FactorResiduals fcapf, nquantiles(100) controls(size1 size2 samesize ) ytitle("Future Correlation of 4F Residuals")
graph export mygraph2.eps,replace
graph export mygraph2.png,replace


rename v22 FCAPF

binscatter Future4FactorResiduals FCAPF, by (sgroup)  nquantiles(100) controls(size1 size2 samesize ) legend(pos(5) ring(0) col(1)) ytitle("Future Correlation of 4F Residuals")

graph export mygraph3.eps,replace
graph export mygraph3.png,replace

binscatter Future4FactorResiduals FCAPF, nquantiles(100) controls(size1 size2 samesize ) ytitle("Future Correlation of 4F Residuals")
graph export mygraph4.eps,replace
graph export mygraph4.png,replace



eststo clear


eststo t2 : reg ρ4_f fcapf ρ_4 sgroup samesize ,cluster(t)

eststo t3 :reg ρ4_f2 fcapf  ρ_4  sgroup samesize ,cluster(t)


eststo id2 : reg ρ4_f fcapf  ρ_4 sgroup samesize ,cluster(id)

eststo id3 :reg ρ4_f2 fcapf  ρ_4 sgroup samesize ,cluster(id)

esttab ,mgroups(Cluster(t) Cluster(id), pattern(1 0 1 0 ) ) ,using example.tex ,replace 


eststo clear



eststo t4 : reg ρ4_f FCAPF ρ_4 sgroup samesize ,cluster(t)

eststo t5 :reg ρ4_f2 FCAPF ρ_4 sgroup samesize ,cluster(t)


eststo id4 : reg ρ4_f FCAPF ρ_4 sgroup samesize ,cluster(id)

eststo id5 :reg ρ4_f2 FCAPF ρ_4 sgroup samesize ,cluster(id)

esttab t2 t3 t4 t5 id2 id3 id4 id5 ,keep(fcapf FCAPF ρ_4 sgroup samesize )mgroups(Cluster(t) Cluster(id), pattern(1 0 0 0 1 0 0 0) ) ,using example01.tex ,replace


///
//booktabs label ///
//mgroups(Cluster(t) Cluster(id), pattern(1 0 0 1 0 0)    ///
//prefix(\multicolumn{@span}{c}{) suffix(})   ///
//span erepeat(\cmidrule(lr){@span})) ///
//alignment(D{.}{.}{-1}) page(dcolumn) nonumber 


eststo clear

eststo t0 :reg ρ4_f fcapf ,cluster(t)

eststo t1 :reg ρ4_f fcapf sgroup ,cluster(t)
eststo t2 :reg ρ4_f fcapf sgroup samesize,cluster(t)

eststo t3 :reg ρ4_f fcapf ρ_4 ,cluster(t)

eststo t5 :reg ρ4_f fcapf ρ_4 sgroup samesize ,cluster(t)

eststo t4 :reg ρ4_f fcapf ρ_4 sgroup c.size1##c.size2 ,cluster(t)

esttab t0 t3  t1 t2 t5  t4,,using example0.tex,replace



eststo clear

eststo t0 :reg ρ4_f FCAPF ,cluster(t)

eststo t1 :reg ρ4_f FCAPF sgroup ,cluster(t)
eststo t2 :reg ρ4_f FCAPF sgroup samesize,cluster(t)

eststo t3 :reg ρ4_f FCAPF ρ_4 ,cluster(t)

eststo t5 :reg ρ4_f FCAPF ρ_4 sgroup samesize ,cluster(t)

eststo t4 :reg ρ4_f FCAPF ρ_4 sgroup c.size1##c.size2 ,cluster(t)

esttab t0 t3  t1 t2 t5  t4,,using example2.tex,replace

// Panel Part

xtset id t 


xtreg ρ4_f FCAPF ρ_4  ,fe

asreg ρ4_f FCAPF ρ_4  , fmb


eststo f1 :xtreg ρ4_f FCAPF ρ_4  c.size1##c.size2 ,fe

eststo f2 :xtreg ρ4_f2 FCAPF ρ_4  c.size1##c.size2 ,fe


eststo f3 :xtreg ρ4_f fcapf ρ_4  c.size1##c.size2 ,fe

eststo f4 :xtreg ρ4_f2 fcapf ρ_4  c.size1##c.size2 ,fe

esttab f1 f2 f3 f4 ,,using example3.tex,replace


replace lρ4_f = log(1+ρ4_f) - log(1-ρ4_f)

summ lρ4_f //if lρ4_f>0
replace lfcapf = log(fcapf)-log(1-fcapf)
replace  lρ4 = log(1+ρ_4) -log(1-ρ_4)




hist ρ_4 ,bcolor(navy) xtitle("Correlation of 4F Residuals")
graph export mygraph5.eps,replace


hist lρ4 ,bcolor(maroon) xtitle("Logistic Transformed Correlation of 4F Residuals")
graph export mygraph6.eps,replace


hist fcapf ,bcolor(navy) xtitle("fcapf")
graph export mygraph7.eps,replace

hist lfcapf,bcolor(maroon) xtitle("Logistic Transformed fcapf")
graph export mygraph8.eps,replace



////



bootstrap, reps(1000) seed(1): eststo OLS1 : reg lρ4_f FCAPF lρ4 sgroup samesize


bootstrap, reps(1000) seed(1): eststo OLS2 : reg lρ4_f fcapf lρ4 sgroup samesize 

bootstrap, reps(1000) seed(1): eststo OLS3 : reg lρ4_f lfcapf lρ4 sgroup samesize 



bootstrap, reps(1000) seed(1):eststo Tobit1 : tobit ρ4_f fcapf ρ_4 sgroup samesize
bootstrap, reps(1000) seed(1): eststo Tobit2 :tobit ρ4_f fcapf lρ4 sgroup samesize
bootstrap, reps(1000) seed(1): eststo Tobit3 : tobit lρ4_f fcapf lρ4 sgroup samesize


bootstrap, reps(1000) seed(1): eststo ML : qreg lρ4_f fcapf ρ_4  sgroup samesize



esttab OLS1 OLS2 OLS3 Tobit1 Tobit2 Tobit3 ML,mgroups(OLS Tobit  ML , pattern(1 0 0 1 0 0 1) )

 ,using example4.tex ,replace

esttab ml1 ml2 ml3 ml4 ,mgroups(qreg sqreg  , pattern(1 0  1 0 ) ) 

