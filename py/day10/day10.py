#
# Advent of Code 2024, Day 10 - Hoof It
#

import numpy as np

# Files.
test_file = 'test10.txt'
input_file = 'input10.txt'

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	num_y = len(lines)
	num_x = len(lines[0])
	grid = np.zeros((num_x, num_y), dtype=np.uint8)
	ord_zero = ord('0')
	for y in range(num_y):
		line = lines[y]
		for x in range(num_x):
			grid[x, y] = ord(line[x]) - ord_zero
	return (grid, num_x, num_y)

def valid_coord(value, max_value):
	return value >= 0 and value < max_value

def find_next_step(pos, grid):
	(g, num_x, num_y) = grid
	(x0,y0) = pos
	h1 = g[x0,y0] + 1
	result = []
	for (dx,dy) in [(-1,0),(1,0),(0,-1),(0,1)]:
		(x1,y1) = (x0 + dx, y0 + dy)
		if valid_coord(x1, num_x) and valid_coord(y1, num_y):
			if g[x1,y1] == h1:
				result.append((x1,y1))
	return result

def find_trails(grid):
	(g, num_x, num_y) = grid
	trails = []
	# Find starting points.
	for y in range(num_y):
		for x in range(num_x):
			if g[x,y] == 0:
				trails.append([(x,y)])

	# Extend trails where possible.
	i = 0
	while i < len(trails):
		trail = trails[i]
		(x,y) = trail[-1]
		if g[x,y] == 9:
			i += 1
			continue
		else:
			steps = find_next_step((x,y), grid)
			num_steps = len(steps)
			if num_steps == 0:
				del trails[i]
				continue
			elif num_steps == 1:
				trails[i].append(steps[0])
			else:
				for p in steps[1:]:
					t = trail.copy()
					t.append(p)
					trails.append(t)
				trails[i].append(steps[0])

	# Return finished trails
	return trails

def trailhead_scores(trails):
	endpoints = [(t[0],t[-1]) for t in trails]
	trailheads = {}
	for (sp,ep) in endpoints:
		if sp not in trailheads:
			trailheads[sp] = set()
		trailheads[sp].add(ep)
	scores = {sp:len(epl) for (sp,epl) in trailheads.items()}
	return scores

def part1_for(file_name):
	lines = read_input(file_name)
	grid = process_lines(lines)
	trails = find_trails(grid)
	scores = trailhead_scores(trails)
	print("Trailhead scores: ", scores)
	result = sum(scores.values())
	return result

def trailhead_ratings(trails):
	starts = [t[0] for t in trails]
	ratings = {}
	for s in starts:
		if s in ratings:
			ratings[s] += 1
		else:
			ratings[s] = 1
	return ratings

def part2_for(file_name):
	lines = read_input(file_name)
	grid = process_lines(lines)
	trails = find_trails(grid)
	ratings = trailhead_ratings(trails)
	print("Trailhead ratings: ", ratings)
	result = sum(ratings.values())
	return result

# Main processing.
print('Advent of Code 2024 - Day 10, Part 1.')
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
