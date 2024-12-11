#
# Advent of Code 2024, Day 7 - Bridge Repair
#

import numpy as np
import re

# Files.
test_file = 'test7.txt'
input_file = 'input7.txt'

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	result = []
	for line in lines:
		line = line.strip()
		temp = line.split(':')
		target = int(temp[0])
		args = [int(v) for v in temp[1].strip().split(' ')]
		result.append((target, args))
	return result

def oplist(code, num_ops, allowed_ops):
	result = []
	base = len(allowed_ops)
	while code != 0:
		r = code % base
		result.append(allowed_ops[r])
		code = code // base
	while len(result) < num_ops:
		result.append(allowed_ops[0])
	return result

def evaluate(args, ops):
	x = args[0]
	for i in range(len(args) - 1):
		y = args[i + 1]
		if ops[i] == '+':
			x += y
		elif ops[i] == '*':
			x *= y
		elif ops[i] == '||':
			x = int(str(x) + str(y))
		else:
			print('Unknown operation ', ops[i])
			return False
	return x

def solve(problem, allowed_ops):
	(target, args) = problem
	n = (len(allowed_ops)) ** (len(args) - 1)
	for i in range(n):
		ops = oplist(i, len(args) - 1, allowed_ops)
		e = evaluate(args, ops)
		if e == target:
			return True
	return False

def part1_for(file_name):
	lines = read_input(file_name)
	problems = process_lines(lines)
	result = 0
	for problem in problems:
		if solve(problem, ['+', '*']):
			t = problem[0]
			result += t
	return result

def part2_for(file_name):
	lines = read_input(file_name)
	problems = process_lines(lines)
	result = 0
	for problem in problems:
		if solve(problem, ['+', '*', '||']):
			t = problem[0]
			result += t
	return result

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
