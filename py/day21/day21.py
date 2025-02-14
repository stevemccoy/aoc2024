#
# Advent of Code 2024, Day 21 - Keypad Conundrum
#

import numpy as np

# Files.
test_file = 'test21.txt'
input_file = 'input21.txt'

# Global variables.
num_keypad = {'7':(0,0),'8':(1,0),'9':(2,0),
			  '4':(0,1),'5':(1,1),'6':(2,1),
			  '1':(0,2),'2':(1,2),'3':(2,2),
		  	  ' ':(0,3),'0':(1,3),'A':(2,3)
}

# Lookup for what to do to get from one numeric key to another, by using directional keypad.
num_keypad_transits = []

# Directional keyboard sequences.
dir_keypad_transits = [
	('^', 'A', '>'), ('^', '<', 'v<'), ('^', 'v', 'v'), ('^', '>', 'v>'), # ('^', '>', '>v'),
	('A', '^', '<'), ('A', '<', 'v<<'), # ('A', '<', '<v<'), 
	('A', 'v', 'v<'), # ('A', 'v', '<v'), 
	('A', '>', 'v'),
	('<', 'A', '>>^'), # ('<', 'A', '>^>'), 
	('<', '^', '>^'), ('<', 'v', '>'), ('<', '>', '>>'),
	('v', 'A', '>^'), # ('v', 'A', '^>'), 
	('v', '^', '^'), ('v', '<', '<'), ('v', '>', '>'),
	('>', 'A', '^'), # ('>', '^', '^<'), 
	('>', '^', '<^'), ('>', '<', '<<'), ('>', 'v', '<')
]

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def compile_num_keypad_transits():
	global num_keypad
	global num_keypad_transits

	# Transits should be in min number of straight lines
	# Transits must avoid (0,3) = ' '
	# Preference order for end of sub-sequence: >, ^, v, <

	result = []
	numkeys = [k for k in num_keypad if k != ' ']
	(ax,ay) = num_keypad[' ']		# Avoid!
	for k1 in numkeys:
		(x1,y1) = num_keypad[k1]
		for k2 in numkeys:
			if k1 == k2:
				continue
			(x2,y2) = num_keypad[k2]
			(x,y) = (x1,y1)
			kl = []
			# Avoid the blank space.
			if y == ay and x2 == ax:
				while y != y2:
					y -= 1
					kl.append('^')
			elif x == ax and y2 == ay:
				while x != x2:
					x += 1
					kl.append('>')
			# Which way to go first now?
			opx = ('>' if x < x2 else '<' if x > x2 else '')
			opy = ('^' if y > y2 else 'v' if y < y2 else '')
			if opx != '' and opy != '':
				if opx == '<':
					# '<' should go first if needed.
					while x != x2:
						x -= 1
						kl.append('<')
				else:
					# Otherwise, do '^' or 'v' before '>' (to finish on '>' button)
					while y != y2:
						y += (1 if y < y2 else -1)
						kl.append(opy)

			# Correct remaining y error, then x now...
			while y != y2:
				dy = 1 if y < y2 else -1
				y += dy
				kl.append('^' if dy < 0 else 'v')

			while x != x2:
				dx = 1 if x < x2 else -1
				x += dx
				kl.append('<' if dx < 0 else '>')

			ks = ''.join(kl)
			result.append((k1, k2, ks))
			
	num_keypad_transits = result

def lookup_num_transit(from_key, to_key):
	global num_keypad_transits
	for (f1, t1, ks) in num_keypad_transits:
		if f1 == from_key and t1 == to_key:
			return ks
	return None

def lookup_dir_transit(from_key, to_key):
	global dir_keypad_transits
	for (f1, t1, ks) in dir_keypad_transits:
		if f1 == from_key and t1 == to_key:
			return ks
	return None

# directional keystrokes needed to produce required door code.
# Assume initially at 'A' key.
def robot1(code):
	pos = 'A'
	seq = []
	for dest in code:
		if pos != dest:
			s = lookup_num_transit(pos, dest)
			seq.append(s)
		seq.append('A')
		pos = dest
	return seq

def robot2(code):
	# Sequence to control robot 1.
	r1sequence = robot1(code)
	r1string = ''.join(r1sequence)
	# Robot 2 sequence.
	pos = 'A' 
	seq = []
	for dest in r1string:
		if pos != dest:
			s = lookup_dir_transit(pos, dest)
			seq.append(s)
		seq.append('A')
		pos = dest
	return seq

def robot3(code):
	# Sequence to control robot 2.
	r2sequence = robot2(code)
	r2string = ''.join(r2sequence)
	# Robot 3 sequence.
	pos = 'A'
	seq = []
	for dest in r2string:
		if pos != dest:
			s = lookup_dir_transit(pos, dest)
			seq.append(s)
		seq.append('A')
		pos = dest
	return seq

# Directional keypad input string to make a robot perform
# the string of operations given in output string.
def robot_control_string(output):
	pos = 'A'
	seq = []
	for dest in output:
		if pos != dest:
			s = lookup_dir_transit(pos, dest)
			seq.append(s)
		seq.append('A')
		pos = dest
	return ''.join(seq)

def plan_keys(plan):
	return sum([plan[k] * len(k) for k in plan])

def robotN(code, n_robots):
	# Numeric keypad actions.
	r1sequence = robot1(code)
	actions = ''.join(r1sequence)
	print(f"Final robot input is {len(actions)} chars.\n'{actions}'")
	recipes = {'A':'A'}

	# Create plan for these actions.
	blocks = [step + 'A' for step in actions[:-1].split('A')]
	plan1 = {}
	plan2 = {}

	for b in blocks:
		if b in plan1:
			plan1[b] += 1
		else:
			plan1[b] = 1

	for ri in range(n_robots):
		# Break out parts of plan so far.
		for a in plan2:
			acount = plan2[a]
			for br in a[:-1].split('A'):
				bf = br + 'A'
				if bf in plan1:
					plan1[bf] += acount
				else:
					plan1[bf] = acount

		plan2 = {}
		for b1 in plan1:
			if b1 in recipes:
				b2 = recipes[b1]
			else:
				b2 = robot_control_string(b1)
				recipes[b1] = b2

			if b2 in plan2:
				plan2[b2] += plan1[b1]
			else:
				plan2[b2] = plan1[b1]
		
		plan1 = {}

	return plan2

def control_string(code):
	seq = robot3(code)
	sls = ''.join(seq)
	return sls

def complexity(code, control_string):
	numpart = int(code[:-1])
	numchars = len(control_string)
	return numchars * numpart

def part1_for(file_name):
	lines = read_input(file_name)
	compile_num_keypad_transits()
	score = 0
	for line in lines:
		code = line.strip()
		c_string = control_string(code)
		c_score = complexity(code, c_string)
		print(f'Code {code} has complexity {c_score} for {len(c_string)} buttons {c_string}')
		score += c_score
	return score

def plan_complexity(code, plan):
	numpart = int(code[:-1])
	nc = 0
	for b in plan:
		nc += plan[b] * len(b)
	return nc * numpart

def part2_for(file_name):
	lines = read_input(file_name)
	compile_num_keypad_transits()
	score = 0
	for line in lines:
		code = line.strip()
		plan = robotN(code, 25)
		c_score = plan_complexity(code, plan)
		print(f'Code {code} has complexity {c_score}')
		score += c_score
	return score

# 159907381897160 too low (24 rbt)
# 314444784819888 too high (25 rbt)
# 410660523597582 too high (25 rbt)


# Main processing.
print('Advent of Code 2024 - Day 21, Part 1.')
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
