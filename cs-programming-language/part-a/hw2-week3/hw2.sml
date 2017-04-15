(* Dan Grossman, Coursera PL, HW2 Provided Code *)

(* if you use this function to compare two strings (returns true if the same
   string), then you avoid several of the functions in problem 1 having
   polymorphic types that may be confusing *)
fun same_string(s1 : string, s2 : string) =
    s1 = s2

(* put your solutions for problem 1 here *)

(* you may assume that Num is always used with values 2, 3, ..., 10
   though it will not really come up *)
datatype suit = Clubs | Diamonds | Hearts | Spades
datatype rank = Jack | Queen | King | Ace | Num of int 
type card = suit * rank

datatype color = Red | Black
datatype move = Discard of card | Draw 

exception IllegalMove

(* put your solutions for problem 2 here *)
fun all_except_option(s, lst) = 
	case lst of
		  [] => NONE
		| x::xs' => if same_string(x, s) 
					then SOME xs' 
					else case all_except_option(s, xs') of
							  NONE => NONE
							| SOME value => SOME (x::value)


fun get_substitutions1(lst, s) =
	case lst of 
		  [] => []
		| names::lst' => case all_except_option(s, names) of
						 	  NONE => get_substitutions1(lst', s)
						 	| SOME value => value @ get_substitutions1(lst', s)


fun get_substitutions2(lst, s) =
	let
		fun aux(lst, acc) =
			case lst of
				  [] => acc
				| names::lst' => case all_except_option(s, names) of
									  NONE => aux(lst', acc)
									| SOME value => aux(lst', (acc @ value))
	in
		aux(lst, [])
	end


fun similar_names(substition_names, name) =
	let
		val {first=first, middle=middle, last=last} = name
		fun generate_names(substitions) =
			case substitions of
				  [] => []
				| sub::substitions' => {first=sub, middle=middle, last=last}::generate_names(substitions')
	in
		name::generate_names(get_substitutions2(substition_names, first))
	end
	