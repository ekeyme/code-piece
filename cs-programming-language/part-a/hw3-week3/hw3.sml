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
	  | TupleP ps         => List.foldl (fn (p,i) => (r p) + i) 0 ps
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
				| x::xs' => case f(x) of
								  NONE => []
								| SOME vs => acc @ vs
  	in
  		
	end