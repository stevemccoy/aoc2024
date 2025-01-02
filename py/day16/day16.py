#
# Advent of Code 2024, Day 16 - Reindeer Maze
#

import numpy as np
import re

# Files.
test_file_a = 'test16a.txt'
test_file_b = 'test16b.txt'
input_file = 'input16.txt'

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

# Unroll the path from the given map of previous nodes.
def path_from_prev(prev, target):
	s = []
	u = target
	if u in prev:
		while u:
			s.insert(0, u)
			u = prev[u]
	return s

def is_node_goal(node, goal):
	(xn,yn,_) = node
	(xg,yg,_) = goal
	return xn == xg and yn == yg

# Shortest path using Dijkstra's algorithm.
def shortest_path(start, finish, dim, grid):
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
					prev[(x,y,h)] = None

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
		if g >= max_distance:
			break
		# Remove shortest path node.
		nodes = q[g]
		if len(nodes) == 0:
			del q[g]
			g += 1
			continue
		u = nodes.pop()
		# Detect goal node.
		if is_node_goal(u, finish):
			path = path_from_prev(prev, u)
			return None if len(path) == 0 else (path,g)
		# Update the queue.
		if len(nodes) > 0:
			q[g] = nodes
		else:
			del q[g]
		
		# Explore from u to neighbouring nodes.
		neighbours = find_neighbours(u, grid)
		for (m, c, v) in neighbours:
			# Make sure v is still in q:
			in_queue = node_in_queue(v, q)
			if in_queue:
				alt = g + c
				d = in_queue[1]		# Previously recorded distance.
				if alt < d:
					q[d].remove(v)
					if alt in q:
						q[alt].append(v)
					else:
						q[alt] = [v]
					prev[v] = u
	return None

def display_grid():
	print("Grid:")
	for y in range(num_y):
		line = ''
		for x in range(num_x):
			line += chr(g_grid[x,y])
		print(line)

def part1_for(file_name):
	lines = read_input(file_name)
	(grid, (num_x, num_y), start, goal) = process_lines(lines)
	(path,cost) = shortest_path(start, goal, (num_x, num_y), grid)
	path_length =  len(path) - 1
	return cost

def part2_for(file_name):
	score = 0
	return score

# Main processing.
print('Advent of Code 2024 - Day 15, Part 1.')
print('Running small test...')
count = part1_for(test_file_a)
print(f"Result is {count}")

print('Running bigger test...')
count = part1_for(test_file_b)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file)
print(f"Result is {count}")

# print('Part 2.')
# print('Running small test...')
# count = part2_for(test_file_a)
# print(f"Result is {count}")

# print('Running bigger test...')
# count = part2_for(test_file_b)
# print(f"Result is {count}")

# print('Running full input...')
# count = part2_for(input_file)
# print(f"Result is {count}")

print("Done")
