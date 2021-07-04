cls
clear
import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Connected stocks\Imbalance.csv", encoding(UTF-8) 


cd "D:\Dropbox\Connected Stocks\Final Report"


eststo v1: quietly estpost  ttest insimbalance_count insimbalance_value insimbalance_volume  , by(grouped)


estpost  sum insimbalance_count insimbalance_value insimbalance_volume  , by(grouped)


eststo v1: quietly estpost  ttest imbalance, by(grouped)

esttab v1  ,compress