#
# Advent of Code 2024, Day 15 - Warehouse Woes
#

import numpy as np
import re

# Files.
test_file_a = 'test15a.txt'
test_file_b = 'test15b.txt'
input_file = 'input15.txt'

# Global variables.

g_grid = None
num_x = 0
num_y = 0
g_instructions = None

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines1(lines):
	global g_grid, num_x, num_y, g_instructions
	# Parse initial grid state.
	i = 0
	grid_lines = []
	for line in lines:
		if line == "" or re.match("[<>^v]+", line):
			break
		grid_lines.append(line)
		i += 1
	# Convert grid lines to numpy form.
	num_y = len(grid_lines)
	num_x = len(grid_lines[0])
	g_grid = np.zeros((num_x, num_y), np.int8)
	for y in range(num_y):
		line = grid_lines[y]
		for x in range(num_x):
			g_grid[x,y] = ord(line[x])
	# Parse instructions.
	g_instructions = []
	for line in lines[i:]:
		g_instructions.append(line.strip())

def find_robot():
	global g_grid, num_x, num_y
	rc = ord('@')
	for y in range(num_y):
		for x in range(num_x):
			if g_grid[x,y] == rc:
				return (x,y)
	return None

def move_robot(rx, ry, dx, dy):
	cdot = ord('.')
	crob = ord('@')
	cbox = ord('O')
	(x,y) = (rx + dx, ry + dy)
	is_box_seen = False
	while g_grid[x,y] == cbox:
		is_box_seen = True
		(x,y) = (x + dx, y + dy)
	if g_grid[x,y] == cdot:
		g_grid[rx + dx, ry + dy] = crob
		g_grid[rx,ry] = cdot
		if is_box_seen:
			g_grid[x,y] = cbox
		(rx,ry) = (rx + dx, ry + dy)
	return (rx,ry)

def evaluate_boxes1():
	score = 0
	cbox = ord('O')
	for y in range(num_y):
		for x in range(num_x):
			if g_grid[x,y] == cbox:
				score += (y * 100 + x)
	return score

def process_lines2(lines):
	global g_grid, num_x, num_y, g_instructions
	# Parse initial grid state.
	i = 0
	grid_lines = []
	for line in lines:
		if line == "" or re.match("[<>^v]+", line):
			break
		line2 = line.replace('#','##').replace('.','..').replace('O', '[]').replace('@', '@.')
		grid_lines.append(line2)
		i += 1
	# Convert grid lines to numpy form.
	num_y = len(grid_lines)
	num_x = len(grid_lines[0])
	g_grid = np.zeros((num_x, num_y), np.int8)
	for y in range(num_y):
		line = grid_lines[y]
		for x in range(num_x):
			g_grid[x,y] = ord(line[x])
	# Parse instructions.
	g_instructions = []
	for line in lines[i:]:
		g_instructions.append(line.strip())

def move_robot2(rx, ry, dx, dy):
	cdot = ord('.')
	crob = ord('@')
	cbox1 = ord('[')
	cbox2 = ord(']')
	cwall = ord('#')
	(x,y) = (rx + dx, ry + dy)
	# Free move.
	if g_grid[x,y] == cdot:
		g_grid[x, y] = crob
		g_grid[rx,ry] = cdot
		(rx,ry) = (x,y)
	# Horizontal move - same rules as part 1.
	elif dy == 0:
		is_box_seen = False
		while g_grid[x,y] in [cbox1,cbox2]:
			is_box_seen = True
			x += dx
		if g_grid[x,y] == cdot:
			if is_box_seen:
				for x1 in range(x, rx, -dx):
					g_grid[x1,y] = g_grid[x1 - dx, y]
			g_grid[rx + dx, ry + dy] = crob
			g_grid[rx,ry] = cdot
			(rx,ry) = (rx + dx, ry + dy)
	# Vertical move - more complicated.
	elif g_grid[x,y] in [cbox1,cbox2]:
		box_moves = [(x,y)]
		if g_grid[x,y] == cbox2:
			box_moves.append((x - 1, y))
		elif g_grid[x,y] == cbox1:
			box_moves.append((x + 1, y))
		i = 0
		move_ok = True
		while i < len(box_moves):
			(x1,y1) = box_moves[i]
			(x2,y2) = (x1 + dx, y1 + dy)
			if g_grid[x2,y2] == cwall:
				move_ok = False
				break
			elif g_grid[x2,y2] == cbox1:
				box_moves.append((x2, y2))
				box_moves.append((x2 + 1, y2))
			elif g_grid[x2,y2] == cbox2:
				box_moves.append((x2, y2))
				box_moves.append((x2 - 1, y2))
			i += 1
		if move_ok:
			# Move each box vertically and backfill with '.' if needed.
			for (x1,y1) in reversed(box_moves):
				(x2,y2) = (x1 + dx, y1 + dy)
				(x3,y3) = (x1 - dx, y1 - dy)
				g_grid[x2,y2] = g_grid[x1,y1]
				if (x3,y3) not in box_moves:
					g_grid[x1,y1] = cdot

			g_grid[rx + dx, ry + dy] = crob
			g_grid[rx,ry] = cdot
			(rx,ry) = (rx + dx, ry + dy)

	return (rx,ry)

def run_instructions(part_number):
	global g_grid, num_x, num_y, g_instructions
	(rx,ry) = find_robot()
	for iline in g_instructions:
		for icode in iline:
			if icode == '^':
				(dx,dy) = (0,-1)
			elif icode == 'v':
				(dx,dy) = (0,1)
			elif icode == '>':
				(dx,dy) = (1,0)
			elif icode == '<':
				(dx,dy) = (-1,0)
			else:
				print("Error - unrecognized code:", icode)
				return
			(rx,ry) = move_robot(rx,ry,dx,dy) if part_number == 1 else move_robot2(rx,ry,dx,dy)

def display_grid():
	print("Grid:")
	for y in range(num_y):
		line = ''
		for x in range(num_x):
			line += chr(g_grid[x,y])
		print(line)

def evaluate_boxes2():
	score = 0
	cbox = ord('[')
	for y in range(num_y):
		for x in range(num_x):
			if g_grid[x,y] == cbox:
				score += (y * 100 + x)
	return score

def part1_for(file_name):
	lines = read_input(file_name)
	process_lines1(lines)
	run_instructions(part_number=1)
	display_grid()
	score = evaluate_boxes1()
	return score

def part2_for(file_name):
	lines = read_input(file_name)
	process_lines2(lines)
	display_grid()
	run_instructions(part_number=2)
	display_grid()
	score = evaluate_boxes2()
	return score

# Main processing.
print('Advent of Code 2024 - Day 15, Part 1.')
print('Running small test...')
count = part1_for(test_file_a)
print(f"Result is {count}")

print('Running bigger test...')
count = part1_for(test_file_b)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file)
print(f"Result is {count}")

print('Part 2.')
print('Running small test...')
count = part2_for(test_file_a)
print(f"Result is {count}")

print('Running bigger test...')
count = part2_for(test_file_b)
print(f"Result is {count}")

print('Running full input...')
count = part2_for(input_file)
print(f"Result is {count}")

print("Done")
