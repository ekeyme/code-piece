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
val only_capitals = List.filter (fn x => Char.isUpper(String.sub(x, 0)))


(*problem 2*)
val longest_string1 = List.foldl (fn (x, acc) => if String.size x > String.size acc 
												 then x else acc) ""


(*problem 3*)
val longest_string2 = List.foldl (fn (x, acc) => if String.size x >= String.size acc 
												 then x else acc) ""


(*problem 4*)
fun longest_string_helper f =
	List.foldl (fn (x, acc) => if f(String.size x, String.size acc) then x else acc) ""


val longest_string3 = longest_string_helper (fn (size_x, size_acc) => size_x > size_acc)


val longest_string4 = longest_string_helper (fn (size_x, size_acc) => size_x >= size_acc)


(*problem 5*)
val longest_capitalized = longest_string1 o only_capitals


(*problem 6*)
val rev_string =  String.implode o List.rev o String.explode


(*problem 7*)
fun first_answer f xs =
	case xs of
		  [] => raise NoAnswer
		| x::xs' => case f(x) of 
						  NONE => first_answer f xs' 
						| SOME v => v


(*problem 8*)
fun all_answers f xs =
	let
		fun aux(xs, acc) =
			case xs of
				  [] => SOME acc
				| x::xs' => case f(x) of
								  NONE => NONE
								| SOME vs => aux(xs', (acc @ vs))
  	in
  		aux(xs, [])
	end

(*problem 9a*)
val count_wildcards = g (fn () => 1) (fn _ => 0)


(*problem 9b*)
val count_wild_and_variable_lengths = g (fn () => 1) String.size


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
				| ConstructorP (_, p) => get_all_variable_names p
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
		| (Tuple vs, TupleP ps) => if (List.length vs) = (List.length ps)
								   then all_answers (fn x => match x) (ListPair.zip(vs, ps))
								   else NONE
		| (Constructor(s1, v), ConstructorP(s2, p)) => if s1 = s2 then match(v, p) else NONE
		| _ => NONE


(*problem 12*)
fun first_match v ps =
	(SOME (first_answer (fn x => match (v, x)) ps)) 
	handle NoAnswer => NONE


(*challenge problem*)
fun typecheck_patterns (lst, ps) =
	let
		fun comp_types x =
			case x of
				  (Anything, t) => SOME t
				| (t, Anything) => SOME t
				| (UnitT, UnitT) => SOME UnitT
				| (IntT, IntT) => SOME IntT
				| (Datatype(t1), Datatype(t2)) => 
					if t1 = t2 then SOME (Datatype t1) else NONE
				| (TupleT(ts1), TupleT(ts2)) => 
					if List.length ts1 = List.length ts2
					then let val t_lst = List.map comp_types (ListPair.zip(ts1, ts2)) 
						 in if (List.exists (fn x => x = NONE) t_lst) 
						 	then NONE 
						 	else SOME (TupleT (List.map valOf t_lst))
						 end
					else NONE
				| _ => NONE

		fun find_datatype (cname : string, lst) =
			case lst of
				  [] => raise NoAnswer
				| (name, dtyp, typ)::tail => if cname = name 
											 then (dtyp, typ) 
											 else find_datatype(cname, tail)

		(*infer type from one pattern*)
		fun pattern2type p =
			case p of
				  Wildcard => Anything
				| Variable _ => Anything
				| UnitP => UnitT
				| ConstP _ => IntT
				| TupleP ps => TupleT(List.map pattern2type ps)
				| ConstructorP(cname, p) => 
					let 
						val (dtyp_name, t1) = find_datatype (cname, lst)
						val t2 = pattern2type p
					in
						case comp_types (t1, t2) of
							  NONE => raise NoAnswer
							| SOME _ => (Datatype dtyp_name)
					end
	in
		(List.foldl (
						fn (x, acc) => case acc of NONE => NONE | SOME t => comp_types (x, t)
				    ) (SOME Anything) (List.map pattern2type ps)
		) handle NoAnswer => NONE
	end
