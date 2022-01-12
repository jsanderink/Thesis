cls

clear
import delimited "regres_CE.csv"
set more off

replace cond =  "1" if cond == "experimental"
replace cond =  "0" if cond == "control"

destring cond, replace


// regres on score variable
asdoc reg score nup ndown cond, robust
X
// regres on clippy variable
reg clippy nup ndown cond, robust

// regres on stars variable
reg stars nup ndown cond, robust

// regres on interval variable
reg interval nup ndown cond, robust

// regres on block_try_counter variable
reg block_try_counter nup ndown cond, robust


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
clear
import delimited "regres_sns.csv"
set more off

replace cond =  "1" if cond == "switched"
replace cond =  "0" if cond == "not_switched"

destring cond, replace

// regres on score variable
reg score nup ndown cond, robust

// regres on clippy variable
reg clippy nup ndown cond, robust

// regres on stars variable
reg stars nup ndown cond, robust

// regres on interval variable
reg interval nup ndown cond, robust

// regres on block_try_counter variable
reg block_try_counter nup ndown cond, robust