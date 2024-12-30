#
# Advent of Code 2024, Day 14 - Restroom Redoubt
#

import numpy as np

# Files.
test_file = 'test14.txt'
input_file = 'input14.txt'

# Global variables.

g_grid = None

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	bots = []
	for line in lines:
		parts = line.split(' ')
		pos = parts[0][2:].split(',')
		vel = parts[1][2:].split(',')
		bots.append(((int(pos[0]),int(pos[1])),(int(vel[0]),int(vel[1]))))
	return bots

def valid_coord(value, max_value):
	return value >= 0 and value < max_value

def simulate_bots(bots, num_x, num_y, num_steps):
	after = []
	for (p,v) in bots:
		(x,y) = p
		(vx,vy) = v
		for i in range(num_steps):
			x = (x + vx) % num_x
			y = (y + vy) % num_y
		after.append(((x,y),(vx,vy)))
	return after

def quadrant_counts(bots, num_x, num_y):
	(q0,q1,q2,q3) = (0,0,0,0)
	x_axis = num_x // 2
	y_axis = num_y // 2
	q0 = q1 = q2 = q3 = 0
	for (pos,_) in bots:
		(x,y) = pos
		if x < x_axis:
			if y < y_axis:
				q0 += 1
			elif y > y_axis:
				q1 += 1
		elif x > x_axis:
			if y < y_axis:
				q2 += 1
			elif y > y_axis:
				q3 += 1
	return (q0,q1,q2,q3)

def tree_counts(bots, num_x, num_y):
	m = 2 * num_y / num_x
	tp = tn = 0
	for (pos,_) in bots:
		(x,y) = pos
		z = abs(x - num_x / 2)
		y0 = m * z
		if y < y0:
			tp += 1
		else:
			tn += 1
	return tp,tn

def part1_for(file_name, test_run):
	lines = read_input(file_name)
	bots = process_lines(lines)
	(num_x,num_y) = (11,7) if test_run else (101,103)
	after = simulate_bots(bots, num_x, num_y, 100)
	qc = quadrant_counts(after, num_x, num_y)
	safety_factor = qc[0] * qc[1] * qc[2] * qc[3]
	result = safety_factor
	return result

def display_bots(bots, num_x, num_y):
	global g_grid
	g_grid = np.zeros((num_x, num_y), dtype=np.int8)
	for b in bots:
		(x,y) = b[0]
		g_grid[x,y] = 1
	for y in range(num_y):
		line = ""
		for x in range(num_x):
			ch = '*' if g_grid[x,y] else ' '
			line += ch
		print(line)

def part2_for(file_name, test_run):
	lines = read_input(file_name)
	bots = process_lines(lines)
	(num_x,num_y) = (11,7) if test_run else (101,103)
	count = 1
	while True:
		bots = simulate_bots(bots, num_x, num_y, 1)
		print(f"Count = {count}")
		display_bots(bots, num_x, num_y)
		tp,tn = tree_counts(bots, num_x, num_y)
		score = tp * 100.0 / len(bots) 
		print('Score:', score)
		if score > 60.0:
			print("Tree?")
			ch = input()
			if ch == "q":
				break
		count += 1
	return count

# Main processing.
print('Advent of Code 2024 - Day 14, Part 1.')
print('Running test...')
count = part1_for(test_file, True)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file, False)
print(f"Result is {count}")

print('Part 2.')
print('Running test...')
count = part2_for(input_file, False)
print(f"Result is {count}")

# print('Running full input...')
# count = part2_for(input_file)
# print(f"Result is {count}")

print("Done")
