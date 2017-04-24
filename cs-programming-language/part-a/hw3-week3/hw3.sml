(* Coursera Programming Languages, Homework 3, Provided Code *)

exception NoAnswer

datatype pattern = Wildcard
		 | Variable of string
		 | UnitP
		 | ConstP of int
		 | TupleP of pattern list
		 | ConstructorP of string * pattern

datatype valu = Const of int
	      | Unit
	      | Tuple of valu list
	      | Constructor of string * valu

fun g f1 f2 p =
    let 
	val r = g f1 f2 
    in
	case p of
	    Wildcard          => f1 ()
	  | Variable x        => f2 x
	  | TupleP ps         => List.foldl (fn (p, i) => (r p) + i) 0 ps
	  | ConstructorP(_,p) => r p
	  | _                 => 0
    end

(**** for the challenge problem only ****)

datatype typ = Anything
	     | UnitT
	     | IntT
	     | TupleT of typ list
	     | Datatype of string

(**** you can put all your code here ****)

(*problem 1*)
fun only_capitals xs =
	List.filter (fn x => Char.isUpper(String.sub(x, 0))) xs


(*problem 2*)
fun longest_string1 xs =
	List.foldl (fn (x, acc) => if String.size x > String.size acc then x else acc) "" xs


(*problem 3*)
fun longest_string2 xs =
	List.foldl (fn (x, acc) => if String.size x >= String.size acc then x else acc) "" xs


(*problem 4*)
fun longest_string_helper f xs =
	List.foldl (fn (x, acc) => if f(String.size x, String.size acc) then x else acc) "" xs


val longest_string3 = longest_string_helper (fn (size_x, size_acc) => size_x > size_acc)


val longest_string4 = longest_string_helper (fn (size_x, size_acc) => size_x < size_acc)


(*problem 5*)
fun longest_capitalized xs =
	longest_string1 (only_capitals xs)


(*problem 6*)
val rev_string =  String.implode o List.rev o String.explode


(*problem 7*)
fun first_answer f xs =
	case xs of
		  [] => raise NoAnswer
		| x::xs' => case f(x) of NONE => first_answer f xs' | SOME v => v


(*problem 8*)
fun all_answers f xs =
	let
		fun aux(xs, acc) =
			case xs of
				  [] => acc
				| x::xs' => case (f(x), acc) of
								  (SOME vs, SOME ys) =>  aux(xs', (SOME (ys @ vs)))
								| _ => NONE
  	in
  		aux(xs, (SOME []))
	end

fun all_answers2 f xs =
	let
		fun helper_fun(x, acc) =
			case (f(x), acc) of
				  (SOME v, SOME acc_v) => SOME (acc_v @ v)
				| _ => NONE
	in
		List.foldl helper_fun (SOME []) xs
	end

(*problem 9a*)
val count_wildcards = g (fn () => 1) (fn s => 0)


(*problem 9b*)
val count_wild_and_variable_lengths = g (fn () => 1) (fn s => String.size s)


(*problem 9c*)
fun count_some_var (val_name, p) =
	g (fn () => 0) (fn s => if s = val_name then 1 else 0) p


(*problem 10*)
fun check_pat p =
	let
		fun get_all_variable_names p =
			case p of
				  Variable s => [s]
				| TupleP ps => List.foldl (fn (p, acc) => 
												(acc @ (get_all_variable_names p))) [] ps
				| _ => []
		fun is_uniq_strings (xs : string list) =
			 case xs of
			 	  [] => true
			 	| x::xs' => not (List.exists (fn y => y = x) xs') andalso is_uniq_strings xs'
	in
		is_uniq_strings (get_all_variable_names p)
	end


(*problem 11*)
fun match (v, p) =
	case (v, p) of
		  (_, Wildcard) => SOME []
		| (v, Variable s) => SOME [(s, v)]
		| (Unit, UnitP) => SOME []
		| (Const x, ConstP y) => if x = y then SOME [] else NONE
		| (Tuple vs, TupleP ps) => if List.size vs = List.size ps
								   then 
								   else NONE
		| (Constructor(s1, v), ConstructorP(s2, p)) => if s1 = s2 then match(v, p) else NONE
		| _ => NONE
