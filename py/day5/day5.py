#
# Advent of Code 2024, Day 5 - Print Queue
#

import numpy as np
import re

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	# Grab rules and updates
	rules = []
	updates = []
	in_rules = True
	for line in lines:
		if len(line) == 0:
			in_rules = False
			continue
		elif in_rules:
			(lhs,rhs) = line.split('|')
			rules.append((int(lhs),int(rhs)))
		else:
			sl = line.split(',')
			updates.append([int(s) for s in sl])
	return (rules, updates)

def correct_order(update, rules):
	# Check each element.
	for i in range(len(update)):
		before = update[:i]
		elem = update[i]
		after = update[i+1:]
		# Check the rules for this element.
		for r in rules:
			# Does anything in before need to be *after* elem?
			if r[0] == elem and r[1] in before:
				return False
			# Does anything in after need to be *before* elem?
			if r[1] == elem and r[0] in after:
				return False
	return True

def correct_updates(updates, rules):
	result = []
	for u in updates:
		if correct_order(u, rules):
			result.append(u)
	return result

def incorrect_updates(updates, rules):
	result = [u for u in updates if not correct_order(u, rules)]
	return result

def middle_elements(updates):
	return [u[len(u) // 2] for u in updates]

def part1_for(file_name):
	lines = read_input(file_name)
	(rules,updates) = process_lines(lines)
	correct_ones = correct_updates(updates, rules)
	middles = middle_elements(correct_ones)
	result = sum(middles)
	return result

def reordered_update(update, rules):
	# Trivial.
	if len(update) < 2:
		return update
	# Rules affecting this update:
	myrules = [r for r in rules if r[0] in update and r[1] in update]
	if len(myrules) == 0:
		return update
	lefties = {r[0] for r in myrules}
	righties = {r[1] for r in myrules}
	# Split the update elements according to rules.
	firsties = [e for e in lefties if e not in righties]
	lasties = [e for e in righties if e not in lefties]
	middle_elements = [e for e in update if e not in firsties and e not in lasties]
	middles_sorted = reordered_update(middle_elements, myrules)
	result = firsties + middles_sorted + lasties
	return result

def part2_for(file_name):
	lines = read_input(file_name)
	(rules,updates) = process_lines(lines)
	incorrect_ones = incorrect_updates(updates, rules)
	corrected_list = []
	for u in incorrect_ones:
		corrected = reordered_update(u, rules)
		corrected_list.append(corrected)
	me = middle_elements(corrected_list)
	count = sum(me)
	return count

# Files.
test_file = 'test5.txt'
input_file = 'input5.txt'

# Main processing.
print('Advent of Code 2024 - Day 5, Part 1.')
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
