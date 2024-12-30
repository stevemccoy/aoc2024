#
# Advent of Code 2024, Day 15 - Warehouse Woes
#

import numpy as np
import regex as re

# Files.
test_file = 'test15.txt'
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

def process_lines(lines):
	global g_grid, num_x, num_y, g_instructions
	# Parse initial grid state.
	i = 0
	grid_lines = []
	for line in lines:
		if line == "" or re.match("[<>^v]+"):
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

def run_instructions():
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
			(rx,ry) = move_robot(rx,ry,dx,dy)

def display_grid():
	print("Grid:")
	for y in range(num_y):
		line = [chr(g_grid[x,y]) for x in range(num_x)]
		print(line)

def evaluate_boxes():
	score = 0
	cbox = ord('O')
	for y in range(num_y):
		for x in range(num_x):
			if g_grid[x,y] == cbox:
				score += (y * 100 + x)
	return score

def part1_for(file_name):
	lines = read_input(file_name)
	process_lines(lines)
	run_instructions()
	display_grid()
	score = evaluate_boxes()
	return score

def part2_for(file_name):
	return 0

# Main processing.
print('Advent of Code 2024 - Day 15, Part 1.')
print('Running test...')
count = part1_for(test_file)
print(f"Result is {count}")

# print('Running full input...')
# count = part1_for(input_file, False)
# print(f"Result is {count}")

# print('Part 2.')
# print('Running test...')
# count = part2_for(input_file, False)
# print(f"Result is {count}")

# print('Running full input...')
# count = part2_for(input_file)
# print(f"Result is {count}")

print("Done")
