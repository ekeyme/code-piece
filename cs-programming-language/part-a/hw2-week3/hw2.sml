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
	

fun card_color(card) =
	case card of 
		  (Clubs, _) => Black
		| (Spades, _) => Black
		| (Hearts, _) => Red
		| (Diamonds, _) => Red


fun card_value(card) =
	case card of
		  (_, Num(v)) => v
		| (_, Ace) => 11
		| (_, Jack) => 10
		| (_, Queen) => 10
		| (_, King) => 10


fun remove_card(cards, card_to_remove: card, e) =
	case cards of
		  [] => raise e
		| card::cards' => if card_to_remove = card
						  then cards'
						  else card::remove_card(cards', card_to_remove, e)


fun all_same_color(cards) =
	case cards of
		  [] => true
		| card::[] => true
		| card1::(card2::cards') => card_color(card1) = card_color(card2) andalso all_same_color(card2::cards')


fun sum_cards(cards) =
	let
		fun aux(cards, sum) =
			case cards of
				  [] => sum
				| card::cards' => aux(cards', card_value(card)+sum)
	in
		aux(cards, 0)
	end


fun score(cards, goal) =
	let
		val sum = sum_cards(cards)
		val pscore = if sum > goal then 3 * (sum - goal) else goal - sum
	in
		if all_same_color(cards) then pscore div 2 else pscore
	end


fun officiate(card_list, moves, goal) =
	let
		fun play_next(card_list, moves, held_cards) =
			if sum_cards(held_cards) > goal
			then (card_list, moves, held_cards)
			else
				case (card_list, moves) of
					  ([], _) => (card_list, moves, held_cards) (*no more card in card-list*)
					| (_, []) => (card_list, moves, held_cards) (*no more move*)
					| (card::card_list', Draw::moves') => play_next(card_list', moves', card::held_cards)
					| (card::_, Discard(card_to_remove)::moves') => play_next(card_list, moves', remove_card(held_cards, card_to_remove, IllegalMove))
	in
		score(#3 (play_next(card_list, moves, [])), goal)
	end
