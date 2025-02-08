%
% Advent of Code 2024, Day 19 - Linen Layout
%

:- use_module(library(clpfd)).
:- working_directory(_, 'c:/users/stephen.mccoy/github/aoc2024/pl/day19/').

:- dynamic available/1, required/1.

% DCG for input file.

identifier_code(C) --> [C],
	{	code_type(C, alpha)
	}.

identifier_codes([HC | TC]) --> identifier_code(HC), identifier_codes(TC).
identifier_codes([C]) --> identifier_code(C).

towel(Codes) --> identifier_codes(Codes).

valid_towel(Name) --> towel(Name),
	{ available(Name) }.

valid_design([N1]) --> valid_towel(N1).
valid_design([N1 | T1]) --> valid_towel(N1), valid_design(T1).


available_line --> towel(T1), !, available_line_cont,
	{	available(T1)
		;
		assertz(available(T1))
	}.

available_line_cont --> ", ", !, available_line.
available_line_cont --> {}.

input_line --> towel(T1), !,
	{ assertz(required(T1)) }.

% Read the input file.

read_available_patterns(Stream) :-
	read_line_to_string(Stream, String),
	string_codes(String, Chars),
	phrase(available_line, Chars, []).

read_input_line(Stream) :- 
	read_line_to_string(Stream, String),
	(
	  String = ""
	  ;
	  String \== end_of_file,
  	  assertz(required(String))
    ).

read_input_lines(Stream) :-
	read_input_line(Stream),
	!,
	read_input_lines(Stream).
read_input_lines(_).

read_input_data(FileName) :-
	retractall(available(_)),
	retractall(required(_)),
	open(FileName, read, Stream),
	read_available_patterns(Stream),
	!,
	read_input_lines(Stream),
	close(Stream).

% List concatenation.
conc([], L, L).
conc([H | Tail], L1, [H | L2]) :-
	conc(Tail, L1, L2).

% S is a sub-sequence of L.	
sublist(S, L, Before, After) :-
	conc(Before, L2, L),
	conc(S, After, L2).

% Check the required patterns.

validate_design(RL, AL1, [A1 | Rest]) :-
	RL \== [],
	findall(Entry, (member(A2, AL1),sublist(A2, RL, Before2, After2), Entry = [A2, Before2, After2]), AL2),
	member([A1, Before1, After1], AL2),
	validate_design(Before1, AL2, T1),
	validate_design(After1, AL2, T2),
	conc(T1, T2, Rest).
validate_design([], _, []).

validate_list([R1 | T1], AL1, [R1 | T2], T3) :-
	string_codes(R1, CL1),
	validate_design(CL1, AL1, _),
	!,
	format('Valid:   ~w\n', [R1]),
	validate_list(T1, AL1, T2, T3).
validate_list([R1 | T1], AL1, T2, [R1 | T3]) :-
	format('Invalid: ~w\n', [R1]),
	validate_list(T1, AL1, T2, T3).
validate_list([], _, [], []).

validate_required(Valid, Invalid) :-
	findall(RC, (required(R), string_codes(R, RC)), RL),
	findall(AC, (available(AC)), AL1),
	validate_list(RL, AL1, Valid, Invalid).

day19_part1(FileName) :-
	writeln("Advent of Code 2024, Day 19, Part 1:"),
	read_input_data(FileName),
	validate_required(VL, _),
	length(VL, Total),
	format('Total number of possible designs = ~w\n', [Total]).

