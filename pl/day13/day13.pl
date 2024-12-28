%
% Advent of Code 2024 - Day 13, Claw Contraption
%
% Cribbed from AOC 2023 Day 19.
% 

:- use_module(library(clpfd)).
:- working_directory(_, 'c:/users/stephen.mccoy/github/aoc2024/pl/day13/').

:- dynamic machine/3.

% DCG for input file.

digit(D) --> [D],
	{	code_type(D, digit)
	}.

digits([D | Tail]) --> digit(D), !, digits(Tail).
digits([]) --> [].

integer(F) --> digits(Digits),
	{	number_codes(F, Digits)
	}.

button_a_line(BAX, BAY) --> "Button A: X+", integer(BAX), ", Y+", integer(BAY).
button_b_line(BBX, BBY) --> "Button B: X+", integer(BBX), ", Y+", integer(BBY).
prize_line(PX,PY) --> "Prize: X=", integer(PX), ", Y=", integer(PY).

machine_def_block --> button_a_line(BAX, BAY), " ", button_b_line(BBX, BBY), " ", 
	prize_line(PX,PY),
	{ assertz(machine([BAX,BAY],[BBX,BBY],[PX,PY])) }.

% Read the input file.

read_machine_block(Stream) :-
	read_line_to_string(Stream, Line1),
	read_line_to_string(Stream, Line2),
	read_line_to_string(Stream, Line3),
	read_line_to_string(Stream, _),
	string_concat(Line1, " ", T1),
	string_concat(Line2, " ", T2),
	string_concat(T1, T2, T3),
	string_concat(T3, Line3, String),
	( String = ""
	  ;
      ( string_codes(String, Chars),
        phrase(machine_def_block, Chars, [])
      )
    ).

read_input_lines(Stream) :-
	read_machine_block(Stream),
	!,
	read_input_lines(Stream).
read_input_lines(_).

read_input_data(FileName) :-
	retractall(machine(_,_,_)),
	open(FileName, read, Stream),
	read_input_lines(Stream),
	close(Stream).

% Solve the problem.

claw_solution_part1([BAX, BAY], [BBX, BBY], [PX, PY], NA, NB, Cost) :-
	[NA,NB] ins 0..100,
	PX #= NA * BAX + NB * BBX,
	PY #= NA * BAY + NB * BBY,
	Cost #= NA * 3 + NB.

claw_solution_part2([BAX, BAY], [BBX, BBY], [PX, PY], NA, NB, Cost) :-
	BigNumber = 10000000000000,
	PXP #= PX + BigNumber,
	PYP #= PY + BigNumber,
	NAL #= max(div(PXP, BAX), div(PYP, BAY)),
	NBL #= max(div(PXP, BBX), div(PYP, BBY)),
	NA in 0..NAL,
	NB in 0..NBL,
	PXP #= NA * BAX + NB * BBX,
	PYP #= NA * BAY + NB * BBY,
	Cost #= NA * 3 + NB.

part1(FileName) :-
	writeln("Advent of Code 2024, Day 13, Part 1:"),
	read_input_data(FileName),
	findall(Cost, (machine(A,B,P), claw_solution_part1(A,B,P,_,_,Cost)), CL),
	format('Machine costs: ~w\n', [CL]),
	sum_list(CL, Sum),
	format('Total Cost = ~w\n', [Sum]).

part2(FileName) :-
	writeln("Advent of Code 2024, Day 13, Part 2:"),
	read_input_data(FileName),
	findall(Cost, (machine(A,B,P), claw_solution_part2(A,B,P,_,_,Cost)), CL),
	format('Machine costs: ~w\n', [CL]),
	sum_list(CL, Sum),
	format('Total Cost = ~w\n', [Sum]).
