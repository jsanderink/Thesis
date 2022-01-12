clear
import delimited "control_vs_experimental.csv"
set more off
 

		//INTERVAL VARIABLE
// check for normality
swilk interval if group=="experimental" //normality rejected
sktest interval if group=="experimental" //normality supported
//
swilk interval if group=="control" //normality rejected
sktest interval if group=="control" //normality supported
//
//Normality is rejected so ranksum and/or median
ranksum interval, by(group) exact //p=0.48
median interval, by(group)  //p=0.35
// //****************************************************************************//
		//STARS VARIABLE
swilk stars if group=="experimental" //normality rejected
sktest stars if group=="experimental" //normality rejected

swilk stars if group=="control" //normality rejected
sktest stars if group=="control" //normality rejected


// //Normality is rejected so ranksum and/or median
ranksum stars, by(group) exact //p=0.77
median stars, by(group)  //p=0.95
//****************************************************************************//
		//SCORE VARIABLE
swilk score if group=="experimental" //normality rejected
sktest score if group=="experimental" //normality rejected

swilk score if group=="control" //normality rejected
sktest score if group=="control" //normality rejected


// //Normality is rejected so ranksum and/or median
ranksum score, by(group) exact //p=0.047
median score, by(group)  //p=0.075

//****************************************************************************//
		//CLIPPY VARIABLE
swilk clippy if group=="experimental" //normality rejected
sktest clippy if group=="experimental" //normality rejected
//
swilk clippy if group=="control" //normality rejected
sktest clippy if group=="control" //normality rejected
//
//
// //Normality is rejected so ranksum and/or median
ranksum clippy, by(group) exact //p=0.93
median clippy, by(group)  //p=0.86
// //****************************************************************************//
// 		//BLOCK_TRY_COUNTER VARIABLE
swilk block_try_counter if group=="experimental" //normality rejected
sktest block_try_counter if group=="experimental" //normality rejected
//
swilk block_try_counter if group=="control" //normality rejected
sktest block_try_counter if group=="control" //normality rejected
//
//
// //Normality is rejected so ranksum and/or median
ranksum block_try_counter, by(group) exact //p=0.20
median block_try_counter, by(group)  //p=0.20
// //****************************************************************************//

