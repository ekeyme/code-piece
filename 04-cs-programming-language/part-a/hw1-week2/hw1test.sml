(* Homework1 Simple Test *)
(* These are basic test cases. Passing these tests does not guarantee that your code will pass the actual homework grader *)
(* To run the test, add a new line to the top of this file: use "homeworkname.sml"; *)
(* All the tests should evaluate to true. For example, the REPL should say: val test1 = true : bool *)

use "hw1.sml";

val test1 = is_older ((1,2,3),(2,3,4)) = true

val test2 = number_in_month ([(2012,2,28),(2013,12,1)],2) = 1
val test2_1 = number_in_month ([],2) = 0
val test2_2 = number_in_month ([(2012,2,28),(2013,12,1),(2012,2,28),(2013,2,1)],2) = 3

val test3 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2,3,4]) = 3
val test3_1 = number_in_months ([],[]) = 0
val test3_2 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2]) = 1

val test4 = dates_in_month ([(2012,2,28),(2013,12,1)],2) = [(2012,2,28)]

val test5 = dates_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2,3,4]) = [(2012,2,28),(2011,3,31),(2011,4,28)]

val test6 = get_nth (["hi", "there", "how", "are", "you"], 2) = "there"

val test7 = date_to_string (2013, 6, 1) = "June 1, 2013"

val test8 = number_before_reaching_sum (10, [1,2,3,4,5]) = 3

val test9 = what_month 70 = 3

val test10 = month_range (31, 34) = [1,2,2,2]
val test10_1 = month_range (31, 31) = [1]
val test10_2 = month_range (34, 33) = []

val test11 = oldest([(2012,2,28),(2011,3,31),(2011,4,28)]) = SOME (2011,3,31)
val test11_1 = oldest([]) = NONE
val test11_2 = oldest([(2011,3,31)]) = SOME (2011,3,31)
val test11_3 = oldest([(2011,3,31), (2011,3,31)]) = SOME (2011,3,31)


val test12_1 = list_uniq([]) = []
val test12_2 = list_uniq([1]) = [1]
val test12_3 = list_uniq([1,1,2]) = [1,2]


val test13_1 = reasonable_date((1,12,32)) = false
val test13_2 = reasonable_date((1,2,29)) = false
val test13_3 = reasonable_date((1,2,28)) = true
val test13_4 = reasonable_date((200,2,29)) = false
val test13_5 = reasonable_date((2000,2,29)) = true
