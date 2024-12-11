#
# Advent of Code 2024, Day 11 - Plutonian Pebbles
#

import numpy as np
import re

# Files.
test_file = 'test11.txt'
input_file = 'input11.txt'

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	return lines[0].split()

def next_step(vs):
	if vs == '0':
		return ['1']
	elif len(vs) % 2 == 0:
		i = len(vs) // 2
		result = [int(vs[:i]), int(vs[i:])]
		return [str(i) for i in result]
	else:
		return [str(int(vs) * 2024)]

def evolve_list(values):
	result = []
	for v in values:
		result += next_step(v)
	return result

def evolve_dict(d):
	result = dict()
	for v1,m1 in d.items():
		v2_list = next_step(v1)
		for v2 in v2_list:
			if v2 in result:
				result[v2] += m1
			else:
				result[v2] = m1
	return result

def stone_count(d):
	return sum([ct for ct in d.values()])

def part1_for(file_name):
	num_generations = 25
	lines = read_input(file_name)
	stones = process_lines(lines)
	for gen in range(num_generations):
		# print(gen, len(stones))
		stones = evolve_list(stones)
	return len(stones)

def part2_for(file_name):
	num_generations = 75
	lines = read_input(file_name)
	stone_list = process_lines(lines)
	stone_dict = {}
	for v in stone_list:
		if v in stone_dict:
			stone_dict[v] += 1
		else:
			stone_dict[v] = 1
	for gen in range(num_generations):
		# print(gen, stone_count(stone_dict))
		stone_dict = evolve_dict(stone_dict)
	return stone_count(stone_dict)

# Main processing.
print('Advent of Code 2024 - Day 11, Part 1.')
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
