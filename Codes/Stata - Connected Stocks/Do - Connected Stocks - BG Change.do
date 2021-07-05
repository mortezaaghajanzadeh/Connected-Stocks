  
 gen interaction = samebgchange * becomesamebg
 
 
 xtset t_month id
 
eststo v1 : quietly  asreg monthlyρ_5_f MFCA monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership  becomesamebg   , fmb newey(4) 
  
eststo v2 :  quietly asreg monthlyρ_5_f MFCA monthlyρ_5  sgroup monthlysamesize monthlysamebm monthlycrossownership  becomesamebg samebgchange interaction  , fmb newey(4) 
    
esttab v1 v2





reg monthlyρ_5_f NMFCA monthlyρ_5  monthlysamesize monthlysamebm monthlycrossownership   samebgchange##becomesamebg i.t_month gdummy0-gdummy47 if changedbg == 1,robust

reg monthlyρ_5_f NMFCA monthlyρ_5  monthlysamesize monthlysamebm monthlycrossownership   samebgchange i.t_month gdummy0-gdummy47 if changedbg == 1,robust

