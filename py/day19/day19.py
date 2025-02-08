#
# Advent of Code 2024, Day 19 - Linen Layout
#

import numpy as np

# Files.
test_file = 'test19.txt'
input_file = 'input19.txt'

# Global variables.

# Infinity distance.
max_distance = 70 * 70

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

# Set up the maze, start and goal positions, from input lines.
def process_lines(lines):
	available = [s.strip() for s in lines[0].split(',')]
	required = []
	for line in lines[1:]:
		if len(line) > 0:
			required.append(line.strip())
	return available, required

def can_make(design, available):
	if len(design) == 0:
		return True
	if design in available:
		return True
	for piece in available:
		i = design.find(piece)
		while i != -1:
			left = design[0:i]
			right = design[i + len(piece):]
			if can_make(left, available) and can_make(right, available):
				return True
			i = design.find(piece, i)
	return False

def part1_for(file_name):
	lines = read_input(file_name)
	available, required = process_lines(lines)
	possible = [d for d in required if can_make(d, available)]
	return len(possible)

def part2_for(file_name):
	lines = read_input(file_name)
	return 0

# Main processing.
print('Advent of Code 2024 - Day 19, Part 1.')
print('Running test...')
count = part1_for(test_file)
print(f"Result is {count}")

# print('Running full input...')
# count = part1_for(input_file)
# print(f"Result is {count}")

# print('Part 2.')
# print('Running test...')
# count = part2_for(test_file)
# print(f"Result is {count}")

# print('Running full input...')
# count = part2_for(input_file)
# print(f"Result is {count}")

print("Done")
