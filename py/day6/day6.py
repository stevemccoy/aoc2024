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

# Return path, and indicator if cycle found.
def trace_path(start, h, dim, grid):
	(x1,y1) = start
	(num_x, num_y) = dim
	path = {(x1,y1,h)}
	block = ord('#')
	while True:
		if h == 0:
			y2 = y1 - 1
			if not valid_coord(y2, num_y):
				return path,False
			elif grid[x1, y2] == block:
				h = (h + 1) % 4
				continue
			else:
				y1 = y2
		elif h == 1:
			x2 = x1 + 1
			if not valid_coord(x2, num_x):
				return path,False
			elif grid[x2, y1] == block:
				h = (h + 1) % 4
				continue
			else:
				x1 = x2
		elif h == 2:
			y2 = y1 + 1
			if not valid_coord(y2, num_y):
				return path,False
			elif grid[x1,y2] == block:
				h = (h + 1) % 4
				continue
			else:
				y1 = y2
		elif h == 3:
			x2 = x1 - 1
			if not valid_coord(x2, num_x):
				return path,False
			elif grid[x2,y1] == block:
				h = (h + 1) % 4
				continue
			else:
				x1 = x2
		else:
			print("Error - illegal value for heading h=", h)
			break

		# Detect cycles in the path.
		if (x1,y1,h) in path:
			return path,True
		else:
			path.add((x1,y1,h))

	return {},False

def distinct_locations(path):
	return {(x,y) for (x,y,_) in path}

def part1_for(file_name):
	lines = read_input(file_name)
	grid = process_lines(lines)
	(x,y) = find_guard(grid)
	(g, num_x, num_y) = grid
	path,_ = trace_path((x,y), 0, (num_x, num_y), g)
	visits = distinct_locations(path)
	result = len(visits)
	return result

def find_cycle_obstacle_points(path, start, grid):
	(g, num_x, num_y) = grid
	result = {}
	for change in path:
		(x,y,_) = change
		g[x, y] = ord('#')
		_,cycle_flag = trace_path(start, 0, (num_x, num_y), g)
		if cycle_flag and (x,y) != start:
			result[(x,y)] = 1
		g[x,y] = ord('.')
	return result

def part2_for(file_name):
	lines = read_input(file_name)
	grid = process_lines(lines)
	(x,y) = find_guard(grid)
	(g, num_x, num_y) = grid
	path,_ = trace_path((x,y), 0, (num_x, num_y), g)
	obstacles = find_cycle_obstacle_points(path, (x,y), grid)
	count = len(obstacles)
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

print('Part 2.')
print('Running test...')
count = part2_for(test_file)
print(f"Result is {count}")

print('Running full input...')
count = part2_for(input_file)
print(f"Result is {count}")

print("Done")
