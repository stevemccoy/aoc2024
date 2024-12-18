#
# Advent of Code 2024, Day 6 - RAM Run
#

import numpy as np

# Files.
test_file = 'test18.txt'
input_file = 'input18.txt'

# Infinity distance.
max_distance = 70 * 70

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

# Populate grid with num_bytes entries for currupt memory locations.
def process_lines(lines, num_x, num_y, num_bytes):
	grid = np.zeros((num_x, num_y), dtype=np.uint8)
	n = 0
	for line in lines:
		if len(line) > 0 and n < num_bytes:
			(xs,ys) = line.split(',')
			(x,y) = (int(xs),int(ys))
			grid[x,y] = 1
			n += 1
	return grid

def valid_coord(value, max_value):
	return value >= 0 and value < max_value

# Find neighbouring points in the grid that are within bounds and empty (accessible).
def find_neighbours(pos, dim, grid):
	result = []
	(x0,y0) = pos
	(num_x,num_y) = dim
	for (dx,dy) in [(-1,0),(0,-1),(0,1),(1,0)]:
		(x1,y1) = (x0 + dx, y0 + dy)
		if valid_coord(x1, num_x) and valid_coord(y1, num_y) and grid[x1, y1] == 0:
			result.append((x1,y1))
	return result

# Lookup where the node appears in the queue structure.
def node_in_queue(node, queue):
	for k,v in queue.items():
		if node in v:
			return (node, k)
	return False

# Unroll the path from the given map of previous nodes.
def path_from_prev(prev, source, target):
	s = []
	u = target
	if prev[u] or u == source:
		while u:
			s.insert(0, u)
			u = prev[u]
	return s

# Shortest path using Dijkstra's algorithm.
def shortest_path(start, finish, dim, grid):
	# Queue to be sorted (ascending) by distance from start node.
	(num_x,num_y) = dim
	# Populate initial distances list.
	all_nodes = []
	prev = dict()
	for x in range(num_x):
		for y in range(num_y):
			if grid[x,y] == 0:
				all_nodes.append((x,y))
				prev[(x,y)] = None

	all_nodes.remove(start)
	q = dict()
	q[max_distance] = all_nodes
	q[0] = [start]
	# Look at paths from start of increasing length.
	g = 0
	while len(q) > 0:
		# Get minimum distance node out of q.
		while g not in q:
			g += 1
		# If we reach infinity there's no path there.
		if g == max_distance:
			break
		# Remove shortest path node.
		nodes = q[g]
		if len(nodes) == 0:
			del q[g]
			g += 1
			continue
		u = nodes.pop()
		# Detect goal node.
		if u == finish:
			path = path_from_prev(prev, start, finish)
			return None if len(path) == 0 else path
		# Update the queue.
		if len(nodes) > 0:
			q[g] = nodes
		else:
			del q[g]
		
		# Explore from u to neighbouring nodes.
		neighbours = find_neighbours(u, dim, grid)
		for v in neighbours:
			# Make sure v is still in q:
			in_queue = node_in_queue(v, q)
			if in_queue:
				alt = g + 1
				d = in_queue[1]		# Previously recorded distance.
				if alt < d:
					q[d].remove(v)
					if alt in q:
						q[alt].append(v)
					else:
						q[alt] = [v]
					prev[v] = u
	return None

def part1_for(file_name, num_x, num_y, num_bytes):
	lines = read_input(file_name)
	grid = process_lines(lines, num_x, num_y, num_bytes)
	start = (0,0)
	finish = (num_x - 1, num_y - 1)
	path = shortest_path(start, finish, (num_x, num_y), grid)
	path_length = len(path) - 1
	return path_length

def part2_for(file_name, num_x, num_y, num_bytes):
	lines = read_input(file_name)
	grid = process_lines(lines, num_x, num_y, num_bytes)
	start = (0,0)
	finish = (num_x - 1, num_y - 1)
	path = shortest_path(start, finish, (num_x, num_y), grid)	
	for i in range(num_bytes, len(lines)):
		(xs,ys) = lines[i].split(',')
		(x,y) = (int(xs),int(ys))
		grid[x,y] = 1
		if (x,y) in path:
			path = shortest_path(start, finish, (num_x, num_y), grid)
			if path is None:
				return f"{xs},{ys}"
	return "not found"

# Main processing.
print('Advent of Code 2024 - Day 18, Part 1.')
print('Running test...')
count = part1_for(test_file, 7, 7, 12)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file, 71, 71, 1024)
print(f"Result is {count}")

print('Part 2.')
print('Running test...')
count = part2_for(test_file, 7, 7, 12)
print(f"Result is {count}")

print('Running full input...')
count = part2_for(input_file, 71, 71, 1024)
print(f"Result is {count}")

print("Done")
