  
 gen interaction = samebgchange * becomesamebg
 
 
 xtset id  t_month
 
eststo v1 : quietly  asreg monthlyρ_5_f  sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership  becomesamebg   , fmb newey(4) 
  
eststo v2 :  quietly asreg monthlyρ_5_f  sbgroup  sgroup monthlysamesize monthlysamebm monthlycrossownership  /*becomesamebg samebgchange*/ interaction  , fmb newey(4) 
    
esttab v1 v2
xtreg monthlyρ_5_f   monthlysamesize monthlysamebm monthlycrossownership  /*becomesamebg samebgchange*/ interaction  , fe


reg monthlyρ_5_f   monthlysamesize monthlysamebm monthlycrossownership  /*becomesamebg samebgchange*/ interaction  i.t_month  , cluste(id)



reg monthlyρ_5_f NMFCA monthlyρ_5  monthlysamesize monthlysamebm monthlycrossownership   samebgchange##becomesamebg i.t_month gdummy0-gdummy47 if changedbg == 1,robust

reg monthlyρ_5_f NMFCA monthlyρ_5  monthlysamesize monthlysamebm monthlycrossownership   samebgchange i.t_month gdummy0-gdummy47 if changedbg == 1,robust


summ becomesamebg