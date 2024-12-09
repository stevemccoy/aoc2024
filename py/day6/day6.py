#
# Advent of Code 2024, Day 6 - Guard Gallivant
#

import numpy as np
import re

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	num_y = len(lines)
	num_x = len(lines[0])
	grid = np.zeros((num_x, num_y), dtype=np.uint8)
	for y in range(num_y):
		line = lines[y]
		for x in range(num_x):
			grid[x, y] = ord(line[x])
	return (grid, num_x, num_y)

def valid_coord(value, max_value):
	return value >= 0 and value < max_value

def find_guard(grid):
	(g, num_x, num_y) = grid
	for x in range(num_x):
		for y in range(num_y):
			if g[x, y] == ord('^'):
				return (x,y)
	return False

def trace_path(start, h, dim, grid):
	(x1,y1) = start
	(num_x, num_y) = dim
	path = {start}
	block = ord('#')
	while True:
		if h == 0:
			y2 = y1 - 1
			if not valid_coord(y2, num_y):
				return path
			elif grid[x1, y2] == block:
				h = (h + 1) % 4
				continue
			else:
				y1 = y2
		elif h == 1:
			x2 = x1 + 1
			if not valid_coord(x2, num_x):
				return path
			elif grid[x2, y1] == block:
				h = (h + 1) % 4
				continue
			else:
				x1 = x2
		elif h == 2:
			y2 = y1 + 1
			if not valid_coord(y2, num_y):
				return path
			elif grid[x1,y2] == block:
				h = (h + 1) % 4
				continue
			else:
				y1 = y2
		elif h == 3:
			x2 = x1 - 1
			if not valid_coord(x2, num_x):
				return path
			elif grid[x2,y1] == block:
				h = (h + 1) % 4
				continue
			else:
				x1 = x2
		else:
			print("Error - illegal value for heading h=", h)
			break

		path.add((x1,y1))

	return False

def part1_for(file_name):
	lines = read_input(file_name)
	grid = process_lines(lines)
	(x,y) = find_guard(grid)
	(g, num_x, num_y) = grid
	path = trace_path((x,y), 0, (num_x, num_y), g)
	result = len(path)
	return result

def part2_for(file_name):
	lines = read_input(file_name)
	count = 0
	return count

# Files.
test_file = 'test6.txt'
input_file = 'input6.txt'

# Main processing.
print('Advent of Code 2024 - Day 6, Part 1.')
print('Running test...')
count = part1_for(test_file)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file)
print(f"Result is {count}")

# print('Part 2.')
# print('Running test...')
# count = part2_for(test_file)
# print(f"Result is {count}")

# print('Running full input...')
# count = part2_for(input_file)
# print(f"Result is {count}")

print("Done")
