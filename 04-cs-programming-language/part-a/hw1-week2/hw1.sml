(* Homework of week 1*)

(* 
1. Write a function is_older that takes two dates and evaluates to true or false. It evaluates to true if the first argument is a date that comes before the second argument. (If the two dates are the same, the result is false.) *)
fun is_older(date1 : (int * int * int), date2 : (int * int * int)) =
	(*simple solution*)
	(*372 * (#1 date1) + 31 * (#2 date1) + (#3 date1) < 372 * (#1 date2) + 31 * (#2 date2) + (#3 date2)*)
	if (#1 date2) = (#1 date1)
	then
		if (#2 date2) = (#2 date1)
		then
			(#3 date2) > (#3 date1)
		else
			(#2 date2) > (#2 date1)
	else
		(#1 date2) > (#1 date1)


(*
2. Write a function number_in_month that takes a list of dates and a month (i.e., an int) and returns how many dates in the list are in the given month.*)
fun number_in_month(dates : (int * int * int) list, m : int) =
	let
		fun number_in_fixed_month(dates : (int * int * int) list) =
			if null dates
			then 0
			else
				(if (#2 (hd dates)) = m then 1 else 0) + number_in_fixed_month(tl dates)
	in
		number_in_fixed_month(dates)
	end
		


(*
3. Write a function number_in_months that takes a list of dates and a list of months (i.e., an int list) and returns the number of dates in the list of dates that are in any of the months in the list of months. Assume the list of months has no number repeated. Hint: Use your answer to the previous problem.*)
fun number_in_months(dates : (int * int * int) list, ms : int list) = 
	if null ms
	then 0
	else
		number_in_month(dates, (hd ms)) + number_in_months(dates, (tl ms))


(*
4. Write a function dates_in_month that takes a list of dates and a month (i.e., an int) and returns a list holding the dates from the argument list of dates that are in the month. The returned list should contain dates in the order they were originally given.*)
fun dates_in_month(dates : (int * int * int) list, m : int) =
	let
		fun dates_in_fixed_month(dates : (int * int * int) list) =
			if null dates
			then []
			else
				if (#2 (hd dates)) = m
				then
					(hd dates) :: dates_in_fixed_month(tl dates)
				else
					dates_in_fixed_month(tl dates)

	in
		dates_in_fixed_month(dates)
	end


(*
5. Write a function dates_in_months that takes a list of dates and a list of months (i.e., an int list) and returns a list holding the dates from the argument list of dates that are in any of the months in the list of months. Assume the list of months has no number repeated. Hint: Use your answer to the previous problem and SML’s list-append operator (@).*)
fun dates_in_months(dates : (int * int * int) list, ms : int list) =
	if null ms
	then []
	else dates_in_month(dates, (hd ms)) @ dates_in_months(dates, (tl ms))


(*
6. Write a function get_nth that takes a list of strings and an int n and returns the nth element of the list where the head of the list is 1st. Do not worry about the case where the list has too few elements: your function may apply hd or tl to the empty list in this case, which is okay.*)
fun get_nth(strs : string list, n : int) =
	let 
		val n = n - 1
	in
		if n = 0
		then
			hd strs
		else
			get_nth((tl strs), n)
	end


(*
7. Write a function date_to_string that takes a date and returns a string of the form January 20, 2013 (for example). Use the operator ^ for concatenating strings and the library function Int.toString for converting an int to a string. For producing the month part, do not use a bunch of conditionals. Instead, use a list holding 12 strings and your answer to the previous problem. For consistency, put a comma following the day and use capitalized English month names: January, February, March, April, May, June, July, August, September, October, November, December.*)
fun date_to_string(date : (int * int * int)) =
	let
		val ms = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		val month = get_nth(ms, (#2 date))

	in
		month ^ " " ^ Int.toString(#3 date) ^ ", " ^ Int.toString(#1 date)
	end


(*
8. Write a function number_before_reaching_sum that takes an int called sum, which you can assume is positive, and an int list, which you can assume contains all positive numbers, and returns an int. You should return an int n such that the first n elements of the list add to less than sum, but the first n + 1 elements of the list add to sum or more. Assume the entire list sums to more than the passed in value; it is okay for an exception to occur if this is not the case.*)
fun number_before_reaching_sum(sum : int, xs : int list) =
	let 
		val sum = sum - (hd xs)
		val xs = tl xs
	in
		if sum > 0
		then
			1 + number_before_reaching_sum(sum, xs)
		else
			0
	end


(*
9. Write a function what_month that takes a day of year (i.e., an int between 1 and 365) and returns what month that day is in (1 for January, 2 for February, etc.). Use a list holding 12 integers and your answer to the previous problem.*)
val days_in_each_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
fun what_month(day_of_year : int) =
	number_before_reaching_sum(day_of_year, days_in_each_month) + 1


(*
10. Write a function month_range that takes two days of the year day1 and day2 and returns an int list [m1,m2,...,mn] where m1 is the month of day1, m2 is the month of day1+1, ..., and mn is the month of day day2. Note the result will have length day2 - day1 + 1 or length 0 if day1>day2.*)
fun month_range(day1 : int, day2 : int) =
	if day1 > day2
	then []
	else
		let
			fun month_range2(day : int) =
				if day = day2
				then
					[what_month(day)]
				else
					what_month(day) :: month_range2(day+1)
		in
			month_range2(day1)
		end


(*
11. Write a function oldest that takes a list of dates and evaluates to an (int*int*int) option. It evaluates to NONE if the list has no dates and SOME d if the date d is the oldest date in the list.*)
fun oldest(dates : (int * int * int) list) =
	if null dates
	then NONE
	else
		let
			(*focus on non-empty dates*)
			fun oldest_nonempty(dates : (int * int * int) list) =
				if null (tl dates)
				then hd dates
				else
					let 
						val date = hd dates
						val oldest_date_in_tl_dates = oldest_nonempty(tl dates)
					in
						if is_older(date, oldest_date_in_tl_dates)
						then date
						else oldest_date_in_tl_dates
					end
		in
			SOME (oldest_nonempty(dates))
		end


(*
12. Challenge Problem: Write functions number_in_months_challenge and dates_in_months_challenge that are like your solutions to problems 3 and 5 except having a month in the second argument multiple times has no more effect than having it once. (Hint: Remove duplicates, then use previous work.)*)
fun list_uniq(xs : int list) =
	let
		fun in_list(x : int, xs : int list) = 
			if null xs
			then false
			else
				if x = (hd xs) then true else in_list(x, (tl xs))
	in
		if null xs
		then []
		else
			if in_list((hd xs), (tl xs))
			then
				list_uniq(tl xs)
			else
				(hd xs) :: list_uniq(tl xs)
	end


fun number_in_months_challenge(dates : (int * int *int) list, ms : int list) =
	number_in_months(dates, list_uniq(ms))


fun dates_in_months_challenge(dates : (int * int *int) list, ms : int list) =
	dates_in_months(dates, list_uniq(ms))


(*
13. Challenge Problem: Write a function reasonable_date that takes a date and determines if it describes a real date in the common era. A “real date” has a positive year (year 0 did not exist), a month between 1 and 12, and a day appropriate for the month. Solutions should properly handle leap years. Leap years are years that are either divisible by 400 or divisible by 4 but not divisible by 100. (Do not worry about days possibly lost in the conversion to the Gregorian calendar in the Late 1500s.)*)
fun reasonable_date(date : (int * int * int)) =
	let
		val year = #1 date
		val month = #2 date
		val day = #3 date
	in
		if year < 1
		then false
		else
			if month < 1 orelse month > 12
			then false
			else
				let
					fun get_nth(xs : int list, n : int) = 
						let 
							val n = n - 1
						in
							if n = 0
							then
								hd xs
							else
								get_nth((tl xs), n)
						end
					val days_in_each_month = 
							if (year mod 400) = 0 orelse ((year mod 4) = 0 andalso (year mod 100) <> 0)
							then [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
							else [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
					val max_day_in_month = get_nth(days_in_each_month, month)
				in
					if day < 1 orelse day > max_day_in_month
					then false
					else true
				end
	end
