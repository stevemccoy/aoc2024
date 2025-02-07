#
# Advent of Code 2024, Day 20 - Race Condition
#

import numpy as np

# Files.
test_file = 'test20.txt'
input_file = 'input20.txt'

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
	global max_distance
	start = None
	goal = None
	num_y = len(lines)
	num_x = len(lines[0])
	max_distance = num_x * num_y * 1000
	grid = np.zeros((num_x, num_y), np.int8)
	for y in range(num_y):
		line = lines[y]
		for x in range(num_x):
			ch = line[x]
			if ch == 'S':
				start = (x,y,'e')
				ch = '.'
			elif ch == 'E':
				goal = (x,y,'e')
				ch = '.'
			grid[x,y] = ord(ch)
	return (grid, (num_x, num_y), start, goal)

# Possible moves and costs: (fwd,1),(left,1000),(right,1000)
def moves(state, grid):
	cdot = ord('.')
	headings = ['n','e','s','w']
	deltas = {'n':(0,-1), 'e':(1,0), 's':(0,1), 'w':(-1,0)}

	result = []
	(x,y,h) = state
	poss_directions = {}
	for hdg in headings:
		(dx,dy) = deltas[hdg]
		if grid[x + dx, y + dy] == cdot:
			poss_directions[hdg] = (x + dx, y + dy, hdg)
	
	if h in poss_directions:
		result.append(('fwd', 1, poss_directions[h]))

	for i in range(4):
		if headings[i] == h:
			j = i - 1 if i > 0 else 3
			k = i + 1 if i < 3 else 0
			if headings[j] in poss_directions:
				result.append(('left', 1000, (x,y,headings[j])))
			if headings[k] in poss_directions:
				result.append(('right', 1000, (x,y,headings[k])))
			break
	
	return result

def valid_coord(value, max_value):
	return value >= 0 and value < max_value

# Find neighbouring points in the grid that are within bounds and empty (accessible).
def find_neighbours(pos, grid):
	return moves(pos, grid)

# Lookup where the node appears in the queue structure.
def node_in_queue(node, queue):
	for k,v in queue.items():
		if node in v:
			return (node, k)
	return False

def path_from_prev(prev, target):
	path = [target]
	u = target
	while u in prev and len(prev[u]) > 0:
		u = prev[u][0]
		path.insert(0, u)
	return path

# Unroll the paths from the given map of previous nodes.
def paths_from_prev(prev, target):
	p = path_from_prev(prev, target)
	paths = [p]
	# if target in prev and len(prev[target]) > 0:
	# 	for u in prev[target]:
	# 		for path in paths_from_prev(prev, u):
	# 			path.append(target)
	# 			paths.append(path)
	# else:
	# 	paths.append([target])
	return paths

def is_node_goal(node, goal):
	(xn,yn,_) = node
	(xg,yg,_) = goal
	return xn == xg and yn == yg

# Find ALL Shortest paths using Dijkstra's algorithm.
def shortest_paths(start, finish, dim, grid):
	global max_distance
	# Queue to be sorted (ascending) by distance from start node.
	(num_x,num_y) = dim
	# Populate initial distances list.
	all_nodes = []
	prev = dict()
	for x in range(num_x):
		for y in range(num_y):
			if grid[x,y] == ord('.'):
				for h in ['n','e','s','w']:
					all_nodes.append((x,y,h))
					# prev[(x,y,h)] = None

	all_nodes.remove(start)
	# Set up priority order queue.
	q = dict()
	q[max_distance] = all_nodes
	q[0] = [start]
	# Look at paths from start of increasing length.
	g = 0
	shortest_path_cost = 0
	while len(q) > 0:
		# Get minimum distance node out of q.
		while g not in q:
			g += 1
		# If we reach infinity there's no path there.
		if g >= max_distance:
			break
		# Quit if all shortest paths found.
		if shortest_path_cost and g > shortest_path_cost:
			paths = []
			for h in ['n','e','s','w']:
				u = (finish[0], finish[1], h)
				paths1 = [p for p in paths_from_prev(prev, u) if p[0] == start]
				paths = paths + paths1
			return (None,None) if len(paths) == 0 else (paths,shortest_path_cost)
		# Remove shortest path node.
		nodes = q[g]
		if len(nodes) == 0:
			del q[g]
			g += 1
			continue
		u = nodes.pop()
		# Update the queue.
		if len(nodes) > 0:
			q[g] = nodes
		else:
			del q[g]
		# Detect goal node.
		if is_node_goal(u, finish):
			shortest_path_cost = g
			continue
		# Explore from u to neighbouring nodes.
		neighbours = find_neighbours(u, grid)
		for (m, c, v) in neighbours:
			# Make sure v is still in q:
			in_queue = node_in_queue(v, q)
			if in_queue:
				alt = g + c
				d = in_queue[1]		# Previously recorded distance.
				if alt <= d:
					q[d].remove(v)
					if alt in q:
						q[alt].append(v)
					else:
						q[alt] = [v]
					if v not in prev:
						prev[v] = [u]
					else:
						prev[v].append(u)
	return (None,None)

def trace_timings(path):
	locations = {}
	cost = 0
	for (x,y,_) in path:
		if (x,y) not in locations:
			locations[(x,y)] = cost
			cost += 1
	return locations

def distance(p1, p2):
	(x1,y1) = p1
	(x2,y2) = p2
	d = abs(x1 - x2) + abs(y1 - y2)
	return d

def find_complex_cheats(timings, grid, dim):
	cheats = {}
	cdot = ord('.')
	(num_x, num_y) = dim
	for (x1,y1) in timings.keys():
		cost1 = timings[(x1,y1)]

		for dy in range(0, 21):
			for x2 in range(x1 - 20 + dy, x1 + 21 - dy, 1):
				if not valid_coord(x2, num_x):
					continue
				if dy == 0 and x2 == x1:
					continue

				for y2 in [y1 - dy, y1 + dy]:
					if valid_coord(y2, num_y) and grid[x2, y2] == cdot:
						if (x2,y2) in timings:
							cost2 = timings[(x2,y2)]
							saving = (cost2 - cost1 - distance((x1,y1), (x2,y2)))
							if saving > 0:
								cheats[(x1,y1,x2,y2)] = saving
	return cheats

def find_simple_cheats(timings, grid, dim):
	cheats = {}
	cwall = ord('#')
	cdot = ord('.')
	(num_x, num_y) = dim
	for (x1,y1) in timings.keys():
		cost1 = timings[(x1,y1)]
		if x1 > 1 and grid[x1 - 1, y1] == cwall:
			(x2,y2) = (x1 - 2,y1)
			if grid[x2,y2] == cdot:
				if (x2,y2) in timings:
					cost2 = timings[(x2,y2)]
					saving = (cost2 - cost1 - 2)
					if saving > 0:
						cheats[(x1,y1,'w')] = saving

		if x1 < (num_x - 2) and grid[x1 + 1, y1] == cwall:
			(x2,y2) = (x1 + 2,y1)
			if grid[x2,y2] == cdot:
				if (x2,y2) in timings:
					cost2 = timings[(x2,y2)]
					saving = (cost2 - cost1 - 2)
					if saving > 0:
						cheats[(x1,y1,'e')] = saving

		if y1 > 1 and grid[x1, y1 - 1] == cwall:
			(x2,y2) = (x1,y1 - 2)
			if grid[x2,y2] == cdot:
				if (x2,y2) in timings:
					cost2 = timings[(x2,y2)]
					saving = (cost2 - cost1 - 2)
					if saving > 0:
						cheats[(x1,y1,'n')] = saving

		if y1 < (num_y - 2) and grid[x1, y1 + 1] == cwall:
			(x2,y2) = (x1,y1 + 2)
			if grid[x2,y2] == cdot:
				if (x2,y2) in timings:
					cost2 = timings[(x2,y2)]
					saving = (cost2 - cost1 - 2)
					if saving > 0:
						cheats[(x1,y1,'s')] = saving

	return cheats

def saving_frequencies(cheats):
	frequencies = {}
	for saving in cheats.values():
		if saving not in frequencies:
			frequencies[saving] = 1
		else:
			frequencies[saving] += 1
	return frequencies

def part1_for(file_name):
	lines = read_input(file_name)
	(grid, (num_x, num_y), start, goal) = process_lines(lines)
	(paths,cost) = shortest_paths(start, goal, (num_x, num_y), grid)
	timings = trace_timings(paths[0])
	cheats = find_simple_cheats(timings, grid, (num_x, num_y))
	freq = saving_frequencies(cheats)
	count = 0
	for (s,f) in freq.items():
		print(f'{f} cheats save {s} picoseconds')
		if s >= 100:
			count += f
	return count

def part2_for(file_name, limit):
	lines = read_input(file_name)
	(grid, (num_x, num_y), start, goal) = process_lines(lines)
	(paths,cost) = shortest_paths(start, goal, (num_x, num_y), grid)
	timings = trace_timings(paths[0])
	cheats = find_complex_cheats(timings, grid, (num_x, num_y))
	freq = saving_frequencies(cheats)
	count = 0
	for (s,f) in freq.items():
		print(f'{f} cheats save {s} picoseconds')
		if s >= limit:
			count += f
	return count

# Main processing.
print('Advent of Code 2024 - Day 20, Part 1.')
print('Running test...')
count = part1_for(test_file)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file)
print(f"Result is {count}")

print('Part 2.')
print('Running test...')
count = part2_for(test_file, 50)
print(f"Result is {count}")

print('Running full input...')
count = part2_for(input_file, 100)
print(f"Result is {count}")

print("Done")
