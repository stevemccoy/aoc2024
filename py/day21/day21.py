#
# Advent of Code 2024, Day 21 - Keypad Conundrum
#

import itertools

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

# Global variables

# Lookup from directional keypad output code to possible input plans to generate the output: code -> plan*
plan_lookup = {}

# Two level lookup from output code to best possible input 2 levels up.
# code -> plan
plan_lookup2 = {}

# Implementation of OPEN during the search - map each robot level to a number of plans completed to that level,
# each associated with the number of keys at that level:  [level -> (key_count,plan)*]*
open_list = {}

# Record of the shortest number of keys achieved for each robot level: level -> min_key_count
best_keycount = {}

keycount_cache = {}

def clear_global_plans():
	global plan_lookup, plan_lookup2, open_list, best_keycount, keycount_cache
	plan_lookup = {}
	plan_lookup2 = {}
	open_list = {}
	best_keycount = {}
	keycount_cache = {}

# Directional keyboard sequences.
dir_keypad_transits = [
	('^', 'A', '>'), ('^', '<', 'v<'), ('^', 'v', 'v'), 
	('^', '>', 'v>'), # ('^', '>', '>v'),
	('A', '^', '<'), 
	('A', '<', 'v<<'), # ('A', '<', '<v<'),
	('A', 'v', '<v'), # ('A', 'v', 'v<'), 
	('A', '>', 'v'),
	('<', 'A', '>>^'), # ('<', 'A', '>^>'), 
	('<', '^', '>^'), ('<', 'v', '>'), ('<', '>', '>>'),
	('v', 'A', '^>'), # ('v', 'A', '>^'), # 
	('v', '^', '^'), ('v', '<', '<'), ('v', '>', '>'),
	('>', 'A', '^'), 
	('>', '^', '<^'), # ('>', '^', '^<'), 
	('>', '<', '<<'), ('>', 'v', '<')
]

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def permute_keystring(s1):
	perms = list(itertools.permutations(s1))
	return list(set([''.join(p) for p in perms]))

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
			kl = []

			opx = ('>' if x1 < x2 else '<' if x1 > x2 else '')
			opy = ('^' if y1 > y2 else 'v' if y1 < y2 else '')

			kstring = opx * abs(x2 - x1) + opy * abs(y2 - y1)
			ks_options = permute_keystring(kstring)

			kl = []
			for ks in ks_options:
				(x,y) = (x1,y1)
				ok = True
				for k in ks:
					y += 1 if k == 'v' else -1 if k == '^' else 0
					x += 1 if k == '>' else -1 if k == '<' else 0
					if x == ax and y == ay:
						ok = False
						break
				if ok:
					kl.append(ks)
			

			result.append((k1, k2, kl))
			
	num_keypad_transits = result

def lookup_num_transit(from_key, to_key):
	global num_keypad_transits
	for (f1, t1, kl) in num_keypad_transits:
		if f1 == from_key and t1 == to_key:
			for ks in kl:
				yield ks
	return None

def score_num_transit(code):
	score = 0
	nc = 0
	c1 = code[0]
	c2 = None
	for i in range(1, len(code)):
		if code[i] != code[i-1]:
			nc += 1
		if code[i] != c1:
			c2 = code[i]
	score += nc * 10
	order = ['<', 'v', '>', '^', 'A']
	if c2:
		c1seen = False
		for oc in order:
			if oc == c1:
				c1seen = True
			if oc == c2 and not c1seen:
				score += 5
				break
	return score

def lookup_num_transit_best_single(from_key, to_key):
	global num_keypad_transits
	for (f1, t1, kl) in num_keypad_transits:
		if f1 == from_key and t1 == to_key:
			kl2 = sorted(kl, key=score_num_transit)
			return kl2[0]
	return None

def lookup_dir_transit(from_key, to_key):
	global dir_keypad_transits
	for (f1, t1, ks) in dir_keypad_transits:
		if f1 == from_key and t1 == to_key:
			yield ks
	return None

# directional keystrokes needed to produce required door code.
# Assume initially at 'A' key.
def robot1(code):
	pos = 'A'
	options = []
	for dest in code:
		seq = ['A'] if pos == dest else [ks + 'A' for ks in lookup_num_transit(pos, dest)]
		options.append(seq)
		pos = dest	
	for keystring in itertools.product(*options):
		yield ''.join(keystring)

def robot_stack(code, n_robots):
	if n_robots == 0:
		for keys in robot1(code):
			yield keys
	else:
		for req_string in robot_stack(code, n_robots - 1):
			pos = 'A'
			options = []
			for dest in req_string:
				seq = ['A'] if pos == dest else [ks + 'A' for ks in lookup_dir_transit(pos, dest)]
				options.append(seq)
				pos = dest
			for keystring in itertools.product(*options):
				yield ''.join(keystring)

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
		mrs = ''
		mrl = None
		for rs in robot_stack(code, 2):
			if mrl is None or len(rs) < mrl:
				mrl = len(rs)
				mrs = rs
		c_score = complexity(code, mrs)
		# print(f'Code {code} has complexity {c_score} for {len(mrs)} buttons {mrs}')
		score += c_score
	return score

# PART 2 CODE.

# Remove shortest partial plan from the OPEN list at a given level.
def pop_open_plan(level):
	global open_list
	if level in open_list and len(open_list[level]) > 0:
		p = open_list[level][0]
		del open_list[level][0]
		return p
	else:
		return None

# Add given plan with associated key count at the given level, to the OPEN list.
def push_open_plan(level, keycount, plan):
	global open_list
	if level in open_list:
		done = False
		for i in range(len(open_list[level])):
			if open_list[level][i][0] > keycount:
				open_list[level].insert(i, (keycount,plan))
				done = True
				break
		if not done:
			open_list[level].append((keycount,plan))
	else:
		open_list[level] = [(keycount,plan)]

# Plan of input keycodes needed to produce given output code for the numerical keypad.
def robot1_plan(code):
	pos = 'A'
	options = []
	for dest in code:
		seq = ['A'] if pos == dest else [ks + 'A' for ks in lookup_num_transit(pos, dest)]
		options.append(seq)
		pos = dest	
	for keystring in itertools.product(*options):
		plan = {}
		for step in keystring:
			if step in plan:
				plan[step] += 1
			else:
				plan[step] = 1
		yield plan

def robotN_plan(code, n_robots):
	if n_robots == 0:
		yield from robot1_plan(code)
		# for plan in robot1_plan(code):
		# 	yield plan
	else:
		for out_plan in robotN_plan(code, n_robots - 1):
			for step,count in out_plan.items():
				pos = 'A'
				options = []
				for dest in step:
					seq = ['A'] if pos == dest else [ks + 'A' for ks in lookup_dir_transit(pos, dest)]
					options.append(seq)
					pos = dest
				for keystring in itertools.product(*options):
					plan = {}
					for substep in keystring:
						if substep in plan:
							plan[substep] += count
						else:
							plan[substep] = count
					yield plan

# From a single output code to multiple input plans for one robot layer.
def rn_plans_from_output_code(output):
	global plan_lookup

	if output in plan_lookup:
		return plan_lookup[output]
	plans = []
	pos = 'A'
	options = []
	for dest in output:
		seq = ['A'] if pos == dest else [ks + 'A' for ks in lookup_dir_transit(pos, dest)]
		options.append(seq)
		pos = dest
	for keystring in itertools.product(*options):
		plan = {}
		for substep in keystring:
			if substep in plan:
				plan[substep] += 1
			else:
				plan[substep] = 1
		plans.append(plan)
	plan_lookup[output] = plans
	return plans


def multiply_plans(plans, count):
	result = []
	if count != 0:
		for p1 in plans:
			p2 = {i:(c * count) for i,c in p1.items() if c != 0}
			result.append(p2)
	return result

# Take multiple plans, each one for achieving a part of an output plan,
# and merge their steps together into a single plan.
def merge_plan_stages(stages):
	plan = {}
	for stage in stages:
		for step,count in stage.items():
			if step in plan:
				plan[step] += count
			else:
				plan[step] = count
	return plan

# From output plan to input plans.
def rn_plans_from_output_plan(out_plan):
	plans = []
	options = []
	for step,count in out_plan.items():
		step_plans = rn_plans_from_output_code(step)
		options.append(multiply_plans(step_plans, count))
	for plan_seq in itertools.product(*options):
		plan = merge_plan_stages(plan_seq)
		plans.append(plan)
	return plans

def rn_best_plan_from_output_plan(out_plan):
	plan = {}
	step_plans = []
	for step,count in out_plan.items():
		kc,step_plan = best_two_level_plan_for_code(step)
		p = multiply_plans([step_plan], count)
		step_plans.append(p[0])
	plan = merge_plan_stages(step_plans)
	return plan

# Find the best input plan for given output code, given 2 level look-ahead.
def best_two_level_plan_for_code(code):
	global plan_lookup2

	if code in plan_lookup2:
		plan = plan_lookup2[code]
		keys = plan_keycount(plan)
		return keys,plan

	best_plan1 = None
	best_keys1 = None
	for plan1 in rn_plans_from_output_code(code):

		plans = rn_plans_from_output_plan(plan1)
		if len(plans) == 0:
			continue
		
		best_keys2 = plan_keycount(plans[0])
		best_plan2 = plans[0]
		for p in plans[1:]:
			kc = plan_keycount(p)
			if kc < best_keys2:
				best_keys2 = kc
				best_plan2 = p
		
		if best_keys1 is None or best_keys2 < best_keys1:
			best_keys1 = best_keys2
			best_plan1 = plan1
	
	plan_lookup2[code] = best_plan1
	return best_keys1,best_plan1


def plan_complexity(code, plan):
	numpart = int(code[:-1])
	nc = 0
	for b in plan:
		nc += plan[b] * len(b)
	return nc * numpart

def plan_keycount(plan):
	score = 0
	for step,count in plan.items():
		score += len(step) * count
	return score

def expand(frontier_level):
	global open_list
	global best_keycount

	# Repeat:
	# Decide what plan at what level to expand.
	# Expand plan at level l1, storing results at level l2 = l1 + 1.
	# Update min_key_counts if appropriate. Report if changes.
	# Loop

	dcount = 1
	while dcount > 0:
		dcount = 0
		for l1 in range(frontier_level - 1, 0, -1):
			pair = pop_open_plan(l1)
			if pair:
				kc1,plan1 = pair
				l2 = l1 + 1
				if l2 == frontier_level:
					p = rn_best_plan_from_output_plan(plan1)
					kc2 = plan_keycount(p)
					if l2 not in best_keycount or best_keycount[l2] > kc2:
						best_keycount[l2] = kc2
						push_open_plan(l2, kc2, p)
					dcount += 1
				else:
					p = rn_best_plan_from_output_plan(plan1)
					kc2 = plan_keycount(p)
					if l2 not in best_keycount or best_keycount[l2] > kc2:
						best_keycount[l2] = kc2
					push_open_plan(l2, kc2, p)
					dcount += 1
				break

def setup_first_robot_input_plans_all_codes(lines):
	# Tackle all output codes at once.
	code = ''.join(lines)
	# Initialise outputs required from level 1, and associated partial plans at level 1.
	for p1 in robot1_plan(code):
		kc1 = plan_keycount(p1)
		push_open_plan(1, kc1, p1)

# directional keystrokes needed to produce required door code.
# Assume initially at 'A' key.
def robot1_first_solution(code):
	pos = 'A'
	options = []
	for dest in code:
		seq = ['A'] if pos == dest else [lookup_num_transit_best_single(pos, dest) + 'A']
		options.append(seq)
		pos = dest	
	for keystring in itertools.product(*options):
		return ''.join(keystring)

def lookup_dir_transit_first_solution(from_key, to_key):
	global dir_keypad_transits
	for (f1, t1, ks) in dir_keypad_transits:
		if f1 == from_key and t1 == to_key:
			return ks
	return None

def get_key_presses(src, dest, num_robots):
	global keycount_cache

	if (src,dest,num_robots) in keycount_cache:
		return keycount_cache[(src,dest,num_robots)]

	key_presses = 0
	code = 'A' if src == dest else lookup_dir_transit_first_solution(src, dest) + 'A'

	if num_robots == 1:
		key_presses = len(code)
	else:
		pos1 = 'A'
		for pos2 in code:
			count = get_key_presses(pos1, pos2, num_robots - 1)
			key_presses += count
			pos1 = pos2

	keycount_cache[(src,dest,num_robots)] = key_presses
	return key_presses

def part2_for(file_name, num_robot_levels):
	clear_global_plans()
	lines = read_input(file_name)
	compile_num_keypad_transits()

	total_complexity = 0
	for code in lines:
		r1_incode = robot1_first_solution(code)
		numpart = int(code[:-1])

		total_keys = 0
		pos1 = 'A'
		for pos2 in r1_incode:
			count = get_key_presses(pos1, pos2, num_robot_levels)
			total_keys += count
			pos1 = pos2
		
		total_complexity += total_keys * numpart

	return total_complexity

# Incorrect:
# 159907381897160 too low (24 rbt)
# 314444784819888 too high (25 rbt)
# 410660523597582 too high (25 rbt)
# 898090265980 
# 940731047570
# 471057686365026

# ??
# 254726869133992
# 220649974646408

# TARGET: 
# 245881705840972

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
count = part2_for(input_file, 25)
print(f"Result is {count}")

print("Done")
