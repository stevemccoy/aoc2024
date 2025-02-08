#
# Advent of Code 2024, Day 17 - Chronospatial Computer
#

# Files.
test_file_a = 'test17a.txt'
test_file_b = 'test17b.txt'
input_file = 'input17.txt'

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	registers = dict()
	program = []
	for line in lines:
		if line.startswith("Register "):
			temp = line[8:].split(':')
			nm = temp[0].strip()
			val = int(temp[1].strip())
			registers[nm] = val
		elif line.startswith("Program:"):
			temp = line[8:].strip().split(',')
			program = [int(c) for c in temp]
	return registers, program

def combo_operand(arg, registers):
	if arg in [0,1,2,3]:
		return arg
	elif arg == 4:
		return registers['A']
	elif arg == 5:
		return registers['B']
	elif arg == 6:
		return registers['C']
	else:
		print('Illegal (reserved) combo operand')
		return False

def exec_step(program, registers, out, pc):
	# Halt if program is done.
	if pc >= len(program):
		return (registers, out, pc, True)
	opcode = program[pc]
	arg = program[pc + 1]

	# adv
	if opcode == 0:
		num = registers['A']
		den = 2 ** combo_operand(arg, registers)
		q = num // den
		registers['A'] = q

	# bxl
	elif opcode == 1:
		result = registers['B'] ^ arg
		registers['B'] = result

	# bst
	elif opcode == 2:
		result = combo_operand(arg, registers) % 8
		registers['B'] = result

	# jnz
	elif opcode == 3:
		if registers['A'] != 0:
			pc = arg
			return (registers, out, pc, False)
	
	# bxc
	elif opcode == 4:
		result = registers['B'] ^ registers['C']
		registers['B'] = result

	# out
	elif opcode == 5:
		result = combo_operand(arg, registers) % 8
		out.append(result)

	# bdv
	elif opcode == 6:
		num = registers['A']
		den = 2 ** combo_operand(arg, registers)
		q = num // den
		registers['B'] = q

	# cdv
	elif opcode == 7:
		num = registers['A']
		den = 2 ** combo_operand(arg, registers)
		q = num // den
		registers['C'] = q

	else:
		print("Unrecognised instruction", opcode)
		exit(1)

	pc += 2
	return (registers, out, pc, False)

def exec_program(program, registers):
	out = []
	pc = 0
	halt_flag = False
	while not halt_flag:
		(registers, out, pc, halt_flag) = exec_step(program, registers, out, pc)
	return out

def exec_and_match_program(program, registers):
	expect = program.copy()
	out = []
	pc = 0
	halt_flag = False
	while not halt_flag:
		(registers, out, pc, halt_flag) = exec_step(program, registers, [], pc)
		for o in out:
			if len(expect) > 0:
				if expect[0] != o:
					return False
				else:
					expect.pop(0)
	return (len(expect) == 0)

def part1_for(file_name):
	lines = read_input(file_name)
	(registers, program) = process_lines(lines)
	out = exec_program(program, registers)
	return ','.join([str(r) for r in out])


p2 = { 0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128, 8:256 }

def custom(arg_a):
	a = arg_a
	b = c = 0
	exp_sequence = [2,4,1,1,7,5,0,3,4,7,1,6,5,5,3,0]

	while a != 0:
		b = (a & 7) ^ 1
		c = (a >> b)
		a = (a >> 3)
		b = (b ^ c) ^ 6
		if b > 7:
			return False
		e = exp_sequence.pop(0)
		if b != e:
			return False
		if len(exp_sequence) == 0:
			break
		
	return arg_a

def output(a):
	return (((a & 7) ^ 1) ^ (a >> ((a & 7) ^ 1)) ^ 6) & 7

def find_input_sequence(exp_outputs, in_options):
	e = exp_outputs[0]
	for in1 in in_options[0]:
		for in2 in in_options[1]:
			for in3 in in_options[2]:
				a = (in3 * 8 + in2) * 8 + in1
				ar = a & 127
				op1 = output(ar)
				if op1 == e:
					pass
					




# 265220867825053 too high.

# def custom_2411750347165530
# Main input file program.
def custom2(arg_a):
	exp_sequence = [2,4,1,1,7,5,0,3,4,7,1,6,5,5,3,0]
	# Backward and forward indexes of the output function.
	bwd = {i:[] for i in range(8)}
	fwd = {}
	for a in range(0, 128):
		e = output(a)
		bwd[e].append(a)
		fwd[a] = e

	binary_table(fwd)
	
	print(f"Expected = {exp_sequence}")

	# Options for each 3 bit output	
	in_options = [bwd[e] for e in exp_sequence]
	ins = find_input_sequence(exp_sequence, in_options)

	a = 0
	for i in reversed(ins):
		a = (a << 3) + i
	print(f"Derived a = {a}")
	bin_string = f"{a:063b}"
	formatted_binary = ' '.join(bin_string[i:i+3] for i in range(0, len(bin_string), 3))
	print(f" = {formatted_binary}")
	arg_a = a

	ns = len(exp_sequence)
	while True:
		a = arg_a
		b = c = 0
		i = 0
		r = True
		while a != 0:

			b = output(a)

			# # bst [a]
			# # bxl 1
			# b = (a & 7) ^ 1
			# # cdv [b]
			# c = (a >> b)
			# # adv 3
			# a = (a >> 3)
			# # bxc
			# # bxl 6
			# b = (b ^ c) ^ 6
			# # out [b % 8]

			e = exp_sequence[i]
			i += 1
			if b != e:
			# if (b & 7) != e:
				r = False
				break
			if i >= ns:
				break

		if r and a == 0 and i >= ns:
			break
			
		arg_a += 1
		
	return arg_a

def custom_035430(arg_a):
	exp_sequence = [0,3,5,4,3,0]
	while True:
		a = arg_a
		b = c = 0
		es = exp_sequence.copy()
		r = True
		while a != 0:
			a = a // 8
			e = es.pop(0)
			if (a & 7) != e:
				r = False
				break
			if len(es) == 0:
				break
		
		if r and a == 0:
			if len(es) == 0:
				break

		arg_a += 1

	return arg_a

def part2_for(file_name, seed, expected):
	lines = read_input(file_name)
	(registers0, program) = process_lines(lines)
	a = seed
	while not custom2(a, expected):
		a += 1
	return a

def binary_table(fwd):
	for i in range(128):
		bin_string = f"{i:08b}"
		formatted_binary = ' '.join(bin_string[i:i+4] for i in range(0, len(bin_string), 4))
		out = fwd[i]
		print(f"{i:4d} -> {i:02x} -> {formatted_binary} --> {out}")

# Main processing.
print('Advent of Code 2024 - Day 17, Part 1.')
print('Running test...')
count = part1_for(test_file_a)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file)
print(f"Result is {count}")

print('Part 2.')
print('Running test...')
count = custom_035430(1)
print(f"Result is {count}")

print('Running full input...')
count = custom2(1 << 46)
print(f"Result is {count}")

print("Done")
