%
% Advent of Code 2024, Day 17: Chronospatial Computer
%

:- use_module(library(clpfd)).
:- working_directory(_, 'c:/users/stephen.mccoy/github/aoc2024/pl/day17/').

:- dynamic available/1, required/1.

% Required output from part 2.
required_output([2,4,1,1,7,5,0,3,4,7,1,6,5,5,3,0]).

num_bits_solution(63).


transform(A, Mask, Out) :-
	B1 #= (A /\ 7) xor 1,
	NBits #= B1 + 3,
	Mask #= 2 ^ NBits - 1,
	C #= A >> B1,
	B2 #= (B1 xor C) xor 6,
	Out #= (B2 /\ 7).

% Not sure this is correct, when mask is 0 and carry is not,
% what should happen?

t2(A, InCarry, InMask, OutCarry, OutMask, Out) :-
	InCarry #= (A /\ InMask),
	B1 #= (A /\ 7) xor 1,
	OutMask #= 2 ^ B1 - 1,
	C #= A >> B1,
	B2 #= (B1 xor C) xor 6,
	Out #= (B2 /\ 7),
	OutCarry #= A >> 3.

masking(0, 0).
masking(Value, Mask) :-
	NB in 1..64,
	Value #< 2 ^ NB,
	MB #= NB - 1,
	Value #>= 2 ^ MB,
	Mask #= 2 ^ NB - 1,
	indomain(Mask).

mask_for(BitShift, Carry, Mask) :-
	BitShift #< 1,
	masking(Carry, Mask).
mask_for(BitShift, Carry, Mask) :-
	BitShift #> 0,
	Mask1 #= 2 ^ BitShift - 1,
	masking(Carry, Mask2),
	Mask #= Mask1 \/ Mask2.

t3(A1, Carry, Mask, OutCarry, OutMask, Out1) :-
	Carry #= (A1 /\ Mask),
	B1 in 0..7,
	A1 #= (8 * OutCarry) + B1,
	B2 #= (B1 xor 1),
	B2 #>= 0,
	mask_for(B2 - 3, OutCarry, OutMask),
	C #= A1 >> B2,
	B3 #= (B2 xor C) xor 6,
	Out1 #= (B3 /\ 7).

o4(InCarry, [], InCarry, _, []).
o4(A, [In1 | InTail], InCarry, InMask, [Out1 | OutTail]) :-
	t3(A1, InCarry, InMask, OutCarry, OutMask, Out1),
	o4(A2, InTail, OutCarry, OutMask, OutTail),
	In1 #= A1 mod 8,
	A #= (A2 * 8) + In1.

o2(A, [], A, _, []).
o2(A1, [In1 | InTail], InCarry, InMask, [Out1 | OutTail]) :-
	t2(A1, InCarry, InMask, OutCarry, OutMask, Out1),
	In1 #= (A1 /\ 7),
	A2 #= (A1 >> 3),
	o2(A2, InTail, OutCarry, OutMask, OutTail).

% o3(A, InList, OutList) :-
make_options(OutRequired, InCarry, InMask, InOptions) :-
	A in 1..511,
	t2(A, InCarry, InMask, OutCarry, OutMask, OutRequired),
	findall((A,OutCarry,OutMask), indomain(A), InOptions).

o3([Carry], Carry, Mask, Carry, Mask, []).
o3([In1 | InTail], InCarry, InMask, OutCarry, OutMask, [Out1 | OutTail]) :-
	make_options(Out1, InCarry, InMask, InOptions),
	member((A1, OC, OM), InOptions),
	In1 is (A1 /\ 7),
	o3(InTail, OC, OM, OutCarry, OutMask, OutTail).

a_value([A], A).
a_value([A1 | Tail1], A) :-
	a_value(Tail1, A2),
	A is (A2 * 8) + A1.


% Need to solve each section and explore them in ascending order of A,
% to get a minimum 
% value for the chaining of the sections.
% Work in Progress...

% [2,4,1,1,7,5,0,3,4,7,1,6,5,5,3,0]

s1(InList1, A1, InList2, A2, Carry2, Mask2) :-
	o3(InList1, 0, 0, Carry1, Mask1, [2,4,1]), a_value(InList1, A1),
	o3(InList2, Carry1, Mask1, Carry2, Mask2, [1,7,5]), a_value(InList2, A2).

solve(A, InList, OutList) :-
	num_bits_solution(NBMax),
	UpperLimit is (2 << NBMax),
	length(OutList, N1),
	N2 is N1 * 3,
	LowerLimit is (1 << N2),
	A in LowerLimit..UpperLimit,
	o3(InList, 0, 0, _, _, OutList),
	labeling([min(A)],[A]).

iterate(0, []).
iterate(A, [Out | Tail]) :-
	A #> 0,
	transform(A, _, Out),
	A2 #= A >> 3,
	iterate(A2, Tail).

convert([], 0).
convert([A | Tail], V) :-
	convert(Tail, TV),
	V #= A + TV * 8.

overall([A], [Out1]) :-
	transform(A, _, Out1).

overall([I1,I2], [Out1, Out2]) :-
	A #= I1 + 8 * I2,
	transform(A, _, Out1),
	overall([I2], [Out2]).

overall([I1,I2,I3 | InTail], [Out1 | OutTail]) :-
	A #= I1 + 8 * I2 + 64 * I3,
	transform(A, _, Out1),
	overall([I2,I3 | InTail], OutTail).

