%
% Advent of Code 2024, Day 17: Chronospatial Computer
%

:- use_module(library(clpfd)).
:- working_directory(_, 'c:/users/stephen.mccoy/github/aoc2024/pl/day17/').

% Required output from part 2.
required_output([2,4,1,1,7,5,0,3,4,7,1,6,5,5,3,0]).

% Answers:
% 	35184372088832		Too low.

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

tx([Out1, Carry, Mask], [In1, FwdCarry, FwdMask], A) :-
	Carry #= A /\ Mask,
	In1 in 0..7,
	A #= (8 * FwdCarry) + In1,
	B2 #= (In1 xor 1),
	B2 #>= 0,
	mask_for(B2 - 3, FwdCarry, FwdMask),
	C #= (A >> B2),
	B3 #= (B2 xor C) xor 6,
	Out1 #= B3 /\ 7.

ltx([], [C, _], [], C).
ltx([Out1 | OutTail], [Carry, Mask], [In1 | InTail], A1) :-
	tx([Out1, Carry, Mask], [In1, FwdCarry, FwdMask], A1),
	ltx(OutTail, [FwdCarry, FwdMask], InTail, _).

% Solver for top-level Output list.
stx(OutList, InList, A) :-
	length(OutList, NS),
	length(InList, NS),
	InList ins 0..7,
	ltx(OutList, [0,0], InList, A).


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

% ---------------------------------------------------------------------

ty(A, Out) :-
	B1 #= A mod 8,
	B2 #= B1 xor 1,
	C #= A >> B2,
	B3 #= (B2 xor C) xor 6,
	Out #= B3 mod 8.

lty([], []).
lty([Out1 | OutTail], [In1 | InTail]) :-
	In1 in 1..511,
	ty(In1, Out1),
	lty(OutTail, InTail).

my(1,1).
my(2,3).
my(3,7).
my(4,15).
my(5,31).
my(6,63).
my(7,127).
my(8,255).
my(9,511).
my(10,1023).

mby(C, M1) :-
	C #> 0,
	my(NB, M1),
	M1 #>= C,
	MB is NB - 1,
	my(MB, M2),
	M2 #< C.

% C: 0000 0101
% A: 0011 1111
rty([In1], [In1]).
rty([In1, In2 | InTail], [Res1, Res2 | ResTail]) :-
	Res1 in 0..7,
	In1 #= C * 8 + Res1,
	mby(C, M),
	In2 /\ M #= C,
	rty([In2 | InTail], [Res2 | ResTail]).

% sty(OutList, InList)
sty(OutList, InList2) :-
	lty(OutList, InList1),
	rty(InList1, InList2).
	
a_value([A], A).
a_value([A1 | Tail1], A) :-
	a_value(Tail1, A2),
	A #= (A2 * 8) + (A1 mod 8).

tty(InList) :-
	required_output(OutList),
	sty(OutList, InList).
	

