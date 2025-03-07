#
# Advent of Code 2024, Day 12 - Garden Groups
#

import numpy as np

# Files.
test_file = 'test12.txt'
input_file = 'input12.txt'

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

def store_region_details(label_string, region_id, region_cells, regions, region_stats):
	area_count = len(region_cells)
	perimeter_count = 2 + len(region_cells) * 2
	regions[region_id] = region_cells
	region_stats[region_id] = (label_string, area_count, perimeter_count)

def distance(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def shared_border(region1, region2):
	border = []
	for p1 in region1:
		for p2 in region2:
			if distance(p1, p2) == 1:
				border.append((p1,p2))
	return border

def initial_label_regions(grid):
	(g, num_x, num_y) = grid
	regions = {}
	region_stats = {}

	label_string = None
	region_id = 0
	region_cells = []
	
	# Find regions from row by row scan.
	for y in range(num_y):
		for x in range(num_x):
			if g[x, y] == label_string:
				# Extend existing region.
				region_cells.append((x,y))
			else:
				if label_string:
					# Store details of finished region.
					store_region_details(label_string, region_id, region_cells, regions, region_stats)
					region_cells = []
				# Make new region.
				label_string = g[x, y]
				region_id += 1
				region_cells.append((x,y))
		# End of the row - store region and start a new row.
		store_region_details(label_string, region_id, region_cells, regions, region_stats)
		region_cells = []
		label_string = None

	# Merge regions on adjacent rows.
	changes = True
	while changes:
		changes = False
		i = 1
		while i <= region_id:
			if i in region_stats:
				# Grab region and find "contact surface" on last row.
				(label1, ac1, pc1) = region_stats[i]

				# Find another region with same label that touches.
				for j in range(i + 1, region_id + 1):
					if j in region_stats:
						(label2, ac2, pc2) = region_stats[j]
						if label2 != label1:
							continue
						rcells2 = regions[j]
						# Find shared perimeter.
						# xs2 = list(map(lambda t: t[0], [c for c in rcells2 if c[1] == y1 + 1 and c[0] in xs1]))
						rcells1 = regions[i]
						xs2 = shared_border(rcells1, rcells2)
						if len(xs2) > 0:
							# Merge into first region.
							changes = True
							regions[i] = rcells1 + rcells2
							(_, ac1, pc1) = region_stats[i]
							region_stats[i] = (label1, ac1 + ac2, pc1 + pc2 - 2 * len(xs2))
							regions[j] = []
							region_stats[j] = (None, 0, 0)
							
				# Scrub any merge victims.
				for k in range(i + 1, region_id + 1):
					if k in region_stats:
						(label3, _, _) = region_stats[k]
						if label3 is None:
							regions.pop(k)
							region_stats.pop(k)
			# Next region.
			i += 1

	return (regions, region_stats)

def neighbours(p, num_x, num_y):
	x0,y0 = p
	result = []
	for dx,dy in [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]:
		(x,y) = (x0 + dx, y0 + dy)
		if valid_coord(x, num_x) and valid_coord(y, num_y):
			result.append((x,y))
	return result

def merge_regions(regions, region_stats):
	change = True
	while change:
		change = False
		for i in region_stats:
			(lab1, _, _) = region_stats[i]
			merge_found = False
			for j in region_stats:
				if merge_found:
					break
				if i >= j:
					continue
				(lab2, area2, perimeter2) = region_stats[j]
				if lab1 != lab2:
					continue
				for p1 in regions[i]:
					if merge_found:
						break
					for p2 in regions[j]:
						if distance(p1, p2) < 2:
							# Merge
							merge_found = True
							change = True
							border_length = len(shared_border(regions[i], regions[j]))
							change = True
							regions[i] = regions[i] + regions[j]
							(_, area1, perimeter1) = region_stats[i]
							region_stats[i] = (lab1, area1 + area2, perimeter1 + perimeter2 - border_length)
							regions[j] = []
							region_stats[j] = (None, 0, 0)
							break
	return (regions, region_stats)

def find_sides(region):
	# Find an "out" region surrounding this one.
	xlist = list([x for x,_ in region])
	ylist = list([y for _,y in region])
	(min_x, max_x) = (min(xlist), max(xlist))
	(min_y, max_y) = (min(ylist), max(ylist))
	other = []
	for x in range(min_x - 1, max_x + 2):
		for y in range(min_y - 1, max_y + 2):
			if not (x,y) in region:
				other.append((x,y))
	# Find the border between "in" and "out".
	border = shared_border(region, other)
	# Now allocate the border segments to "sides".
	sides = []
	while len(border) > 0:
		segment = border.pop()
		((xs,ys), (xo,yo)) = segment
		side = [segment]
		if xs == xo:
			# Horizontal.
			i = 1
			while True:
				s2 = ((xs - i, ys), (xo - i, yo))
				if s2 not in border:
					break
				side.append(s2)
				border.remove(s2)
				i += 1
			i = 1
			while True:
				s2 = ((xs + i, ys), (xo + i, yo))
				if s2 not in border:
					break
				side.append(s2)
				border.remove(s2)
				i += 1
		else:
			# Vertical.
			i = 1
			while True:
				s2 = ((xs, ys - i), (xo, yo - i))
				if s2 not in border:
					break
				side.append(s2)
				border.remove(s2)
				i += 1
			i = 1
			while True:
				s2 = ((xs, ys + i), (xo, yo + i))
				if s2 not in border:
					break
				side.append(s2)
				border.remove(s2)
				i += 1
		sides.append(side)
	return sides

def perimeter_cost(stats):
	total = 0
	total_area = 0
	for i in stats.keys():
		(lab, area, perimeter) = stats[i]
		cost = (area * perimeter)
		print(f"A region [{i}] of {chr(lab)} plants with price {area} * {perimeter} = {cost}")
		total += cost
		total_area += area
	print(f"Total area = {total_area}")
	return total

def distinct_locations(path):
	return {(x,y) for (x,y,_) in path}

def regions_from_input(file_name):
	lines = read_input(file_name)
	grid = process_lines(lines)
	(regions, stats) = initial_label_regions(grid)
	(regions, stats) = merge_regions(regions, stats)
	return (regions, stats)

def part1_for(file_name):
	(regions, stats) = regions_from_input(file_name)
	result = perimeter_cost(stats)
	return result

def part2_for(file_name):
	(regions, stats) = regions_from_input(file_name)
	score = 0
	for k in regions.keys():
		s = find_sides(regions[k])
		(_, a, _) = stats[k]
		score += (a * len(s))
	return score

# Main processing.
print('Advent of Code 2024 - Day 12, Part 1.')
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
