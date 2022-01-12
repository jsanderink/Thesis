clear
import delimited "switched_vs_not_switched.csv"
set more off
 

		//INTERVAL VARIABLE
// check for normality
swilk interval if group=="switched" //normality rejected
sktest interval if group=="switched" //normality rejected

swilk interval if group=="not_switched" //normality rejected
sktest interval if group=="not_switched" //normality supported
//
//Normality is rejected so ranksum and/or median
ranksum interval, by(group) exact //p=0.87
median interval, by(group)  //p=0.62
//****************************************************************************//
		//STARS VARIABLE
swilk stars if group=="switched" //normality rejected
sktest stars if group=="switched" //normality rejected

swilk stars if group=="not_switched" //normality rejected
sktest stars if group=="not_switched" //normality rejected


//Normality is rejected so ranksum and/or median
ranksum stars, by(group) exact //p=0.23
median stars, by(group)  //p=0.66
//****************************************************************************//
		//SCORE VARIABLE
swilk score if group=="switched" //normality rejected
sktest score if group=="switched" //normality supported

swilk score if group=="not_switched" //normality rejected
sktest score if group=="not_switched" //normality rejected


//Normality is rejected so ranksum and/or median
ranksum score, by(group) exact //p=0.02
median score, by(group)  //p=0.05

//****************************************************************************//
		//CLIPPY VARIABLE
swilk clippy if group=="switched" //normality rejected
sktest clippy if group=="switched" //normality rejected

swilk clippy if group=="not_switched" //normality rejected
sktest clippy if group=="not_switched" //normality rejected


//Normality is rejected so ranksum and/or median
ranksum clippy, by(group) exact //p=0.26
median clippy, by(group)  //p=0.42
//****************************************************************************//
		//BLOCK_TRY_COUNTER VARIABLE
swilk block_try_counter if group=="switched" //normality rejected
sktest block_try_counter if group=="switched" //normality rejected

swilk block_try_counter if group=="not_switched" //normality rejected
sktest block_try_counter if group=="not_switched" //normality rejected


//Normality is rejected so ranksum and/or median
ranksum block_try_counter, by(group) exact //p=0.01
median block_try_counter, by(group)  //p=0.01 
//****************************************************************************//