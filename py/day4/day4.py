#
# Advent of Code 2024, Day 4 - Ceres Search
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

def count_words(grid, num_x, num_y, word):
	nc = len(word)
	count = 0
	codes = [ord(c) for c in word]
	for xs in range(num_x):
		for ys in range(num_y):
			if grid[xs, ys] != codes[0]:
				continue
			for (dx,dy) in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
				found = True
				for ci in range(nc):
					(x,y) = (xs + dx * ci, ys + dy * ci)
					if not valid_coord(x, num_x) or not valid_coord(y, num_y) or grid[x, y] != codes[ci]:
						found = False
						break
				if found:
					count += 1
	return count

def count_xmas(grid, num_x, num_y):
	count = 0
	codes = [ord(c) for c in 'MAS']
	for x in range(1,num_x-1):
		for y in range(1,num_y-1):
			if grid[x, y] != codes[1]:
				continue
			c1 = grid[x - 1, y - 1]
			c2 = grid[x + 1, y + 1]
			c3 = grid[x - 1, y + 1]
			c4 = grid[x + 1, y - 1]			
			if (c1,c2) == (codes[0],codes[2]) or (c1,c2) == (codes[2],codes[0]):
				if (c3,c4) == (codes[0],codes[2]) or (c3,c4) == (codes[2],codes[0]):
					count += 1
	return count

def part1_for(file_name):
	lines = read_input(file_name)
	(grid, num_x, num_y) = process_lines(lines)
	count = count_words(grid, num_x, num_y, 'XMAS')
	return count

def part2_for(file_name):
	lines = read_input(file_name)
	(grid, num_x, num_y) = process_lines(lines)
	count = count_xmas(grid, num_x, num_y)
	return count

# Files.
test_file = 'test4.txt'
input_file = 'input4.txt'

# Main processing.
print('Advent of Code 2024 - Day 4, Part 1.')
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
