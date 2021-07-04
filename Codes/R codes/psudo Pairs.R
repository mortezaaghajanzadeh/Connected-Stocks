


link <- "H:/Economics/Finance(Prof.Heidari-Aghajanzadeh)/Data/Psudo/"

name <-paste(link , "RGWeeklyNormalzedFCAP5.1" , ".csv", sep="")
df <- read.csv(name)
View(df)
fpmg <- pmg(investment ~ mvalue + kstock, grunfeld_copy, index=c("YEAR","FIRM"))