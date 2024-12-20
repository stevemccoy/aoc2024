#
# Advent of Code 2024, Day 8 - Resonant Collinearity
#

import numpy as np

# Files.
test_file = 'test8.txt'
input_file = 'input8.txt'

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

def find_frequencies(grid):
	(g, num_x, num_y) = grid
	fset = {}
	f_dot = ord('.')
	for x in range(num_x):
		for y in range(num_y):
			f = g[x, y]
			if f != f_dot:
				if f not in fset:
					fset[f] = [(x,y)]
				else:
					fset[f].append((x,y))
	return fset

def count_antinodes(grid, part_number):
	(_, num_x, num_y) = grid
	# Detect where the transmitters and frequencies are.
	frequencies = find_frequencies(grid)
	# Needs to be a distinct set of positions.
	antinodes = set()
	for f in frequencies.keys():
		antennas = frequencies[f]
		n = len(antennas)
		if n > 1:
			# Look at each pair within this set and predict the antinode positions.
			for i in range(n):
				a = antennas[i]
				for j in range(i + 1, n):
					b = antennas[j]
					(dx,dy) = (b[0] - a[0], b[1] - a[1])
					if part_number == 1:
						for n1 in [(b[0] + dx, b[1] + dy), (a[0] - dx, a[1] - dy)]:
							if valid_coord(n1[0], num_x) and valid_coord(n1[1], num_y):
								antinodes.add(n1)
					elif part_number == 2:
						k = 0
						more = True
						while more:							
							more = False
							for n1 in [(b[0] + k * dx, b[1] + k * dy), (a[0] - k * dx, a[1] - k * dy)]:
								if valid_coord(n1[0], num_x) and valid_coord(n1[1], num_y):								
									antinodes.add(n1)
									more = True
							k += 1
	return len(antinodes)

def part1_for(file_name):
	lines = read_input(file_name)
	grid = process_lines(lines)
	result = count_antinodes(grid, 1)
	return result

def part2_for(file_name):
	lines = read_input(file_name)
	grid = process_lines(lines)
	result = count_antinodes(grid, 2)
	return result

# Main processing.
print('Advent of Code 2024 - Day 8, Part 1.')
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
