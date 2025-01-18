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

def part2_for(file_name, seed):
	lines = read_input(file_name)
	(registers0, program) = process_lines(lines)
	a = seed
	while True:
		registers = registers0.copy()
		registers['A'] = a
		if exec_and_match_program(program, registers):
			print('Program', program, '\ngenerated itself for seed value of A=', a)
			break
		a += 1
	return a

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
count = part2_for(test_file_b, 0)
print(f"Result is {count}")

print('Running full input...')
count = part2_for(input_file, 35184372088832)
print(f"Result is {count}")

print("Done")
