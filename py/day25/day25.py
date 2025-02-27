#
# Advent of Code 2024, Day 25 - Code Chronicle
#

import numpy as np

# Files.
test_file = 'test25.txt'
input_file = 'input25.txt'

# Global variables.

# Size of a schematic block.
num_x = 5
num_y = 7

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def coding(grid):
	return [int(sum(grid[x])) - 1 for x in range(num_x)]

# Read the lock and key schemes from the raw lines.
def process_lines(lines):
	locks = []
	keys = []
	i = 0
	while i <= (len(lines) - num_y):
		grid = np.zeros((num_x, num_y), np.int8)
		for y in range(num_y):
			line = lines[i + y]
			for x in range(num_x):
				ch = line[x]
				grid[x,y] = 1 if ch == '#' else 0
		if grid[0,0]:
			locks.append(coding(grid))
		else:
			keys.append(coding(grid))
		i += num_y
		while i < len(lines) and len(lines[i]) == 0:
			i += 1
	
	return (locks, keys)


def part1_for(file_name):
	lines = read_input(file_name)
	(locks,keys) = process_lines(lines)
	count = 0
	for lock in locks:
		for key in keys:
			match = [lock[i] + key[i] for i in range(num_x)]
			print("Matching key ", key, " to lock ", lock, " result = ", match)
			if all([match[i] <= 5 for i in range(num_x)]):
				print(" - success.")
				count += 1
			else:
				print(" - fail.")
	return count

def part2_for(file_name):
	lines = read_input(file_name)
	(grid, (num_x, num_y), start, goal) = process_lines(lines)
	(paths,cost) = shortest_paths(start, goal, (num_x, num_y), grid)
	nodes = set()
	for p in paths:
		for (x,y,h) in p:
			nodes.add((x,y))
	return len(nodes)

# Main processing.
print('Advent of Code 2024 - Day 25, Part 1.')
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
