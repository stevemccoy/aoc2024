#
# Advent of Code 2024, Day 24 - Crossed Wires
#

# Files.
test_file = 'test24.txt'
input_file = 'input24.txt'

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	# Section - initial wire states.
	i = 0
	wires = {}
	while i < len(lines):
		p = lines[i].split(':')
		if len(p) != 2:
			break
		wires[p[0].strip()] = int(p[1].strip())
		i += 1

	# Section - gates.
	gates_bwd = {}
	gates_fwd = {}

	while i < len(lines):
		p1 = lines[i].split('->')
		i += 1
		if len(p1) != 2:
			continue
		out = p1[1].strip()
		p2 = p1[0].strip().split(' ')
		if len(p2) != 3:
			continue
		in1 = p2[0].strip()
		in2 = p2[2].strip()
		op = p2[1].strip()
		gates_bwd[out] = (op, in1, in2)
		for in3 in [in1,in2]:
			if in3 not in gates_fwd:
				gates_fwd[in3] = []
			gates_fwd[in3].append((op,out))
	
	return wires, gates_fwd, gates_bwd

def propagate(wires, fwd, bwd):
	todo = [p for p in wires.items()]
	while len(todo) > 1:
		(wn,wv) = todo.pop(0)
		if wn in fwd:
			for (op,out) in fwd[wn]:
				(_, in1, in2) = bwd[out]
				if in1 in wires and in2 in wires:
					if op == "AND":
						wires[out] = (1 if wires[in1] and wires[in2] else 0)
					elif op == "OR":
						wires[out] = (1 if wires[in1] or wires[in2] else 0)
					elif op == "XOR":
						wires[out] = (1 if (wires[in1] and not wires[in2]) or (wires[in2] and not wires[in1]) else 0)
					else:
						print("Error - unrecognized op: ", op)
						return None
					todo.append((out, wires[out]))
	return wires

def register_bits(wires, prefix):
	i = 0
	names = []
	while True:
		name = "{p}{v:02d}".format(p = prefix, v = i)
		if name not in wires:
			break
		names.append(name)
		i += 1
	bits = [wires[wn] for wn in names]
	return bits

def result_from_bits(bits):
	result = 0
	i = 1
	for b in bits:
		if b:
			result += i
		i *= 2
	return result

def register_value(wires, name):
	bits = register_bits(wires, name)
	return result_from_bits(bits)

def bits_from_value(value):
	bits = []
	while value > 0:
		bits.append(1 if value % 2 else 0)
		value = value // 2
	return bits

def part1_for(file_name):
	lines = read_input(file_name)
	wires, fwd, bwd = process_lines(lines)
	wires2 = propagate(wires, fwd, bwd)
	bits = register_bits(wires2, 'z')
	result = result_from_bits(bits)
	return result

def print_tree(indent, wn, bwd):
	s = ""
	if wn in bwd:
		(op, in1, in2) = bwd[wn]
		s = (' ' * indent) + wn + '<-' + op[0] + ':' + print_tree(indent + 2, in1, bwd) + '\n'
		s = s + (' ' * indent) + '      :' + print_tree(indent+2, in2, bwd)
		return s
	else:
		return wn
	
# Find the wires which given output depends on, with their actual values.
def dependency_set(out, wires, bwd):
	results = {out: wires[out]}
	if out in bwd:
		(op, in1, in2) = bwd[out]
		for in3 in [in1, in2]:
			for k,v in dependency_set(in3, wires, bwd).items():
				results[k] = v
	return results

#
# Find 4 pairs of gates whose outputs can be swapped so that target output is achieved.
#
def find_swaps(wires, actual, target, bwd):
	# Find output wires that are in error.
	errors = {}
	for i in range(len(actual)):
		if actual[i] != target[i]:
			name = "z{v:02d}".format(v = i)
			errors[name] = wires[name]
	
	# Determine dependencies of these output wires on other wires in network.
	deps = {out1:dependency_set(out1, wires, bwd) for out1 in errors}
	for o1 in deps:
		count = 0
		for o2 in deps:
			if o1 != o2:
				if 

		
	dep_counts 

	pass

def part2_for(file_name):
	lines = read_input(file_name)
	wires, fwd, bwd = process_lines(lines)
	wires2 = propagate(wires, fwd, bwd)
	xbits = register_bits(wires2, 'x')
	ybits = register_bits(wires2, 'y')
	zbits = register_bits(wires2, 'z')
	xvalue = result_from_bits(xbits)
	yvalue = result_from_bits(ybits)
	zvalue = xvalue + yvalue
	zbits_target = bits_from_value(zvalue)

	find_swaps(wires2, zbits, zbits_target, bwd)

	# print("Outputs in error: ", errors)
	# for (op1,ov1) in errors.items():
	# 	print("Bwd", op1, "(", ov1, ") ->", bwd[op1])

	# h1 = {i1 for o1 in errors for i1 in bwd[o1][1:] if not i1.startswith('x') and not i1.startswith('y')}
	# print("H1 layer", h1)
	result = 0
	return result

# Main processing.
print('Advent of Code 2024 - Day 24, Part 1.')
print('Running test...')
count = part1_for(test_file)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file)
print(f"Result is {count}")

print('Part 2.')
print('Running full input...')
count = part2_for(input_file)
print(f"Result is {count}")

print("Done")
