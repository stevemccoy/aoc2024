#
# Advent of Code 2024, Day 23 - LAN Party
#

# Files.
test_file = 'test23.txt'
input_file = 'input23.txt'

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def process_lines(lines):
	nodes = dict()
	links = set()
	for line in lines:
		t = line.split('-')
		lhs = t[0]
		rhs = t[1]
		if lhs in nodes:
			nodes[lhs] += 1
		else:
			nodes[lhs] = 1
		if rhs in nodes:
			nodes[rhs] += 1
		else:
			nodes[rhs] = 1
		links.add((lhs,rhs))
	return nodes,links

def connected(n1, n2, links):
	return (n1,n2) in links or (n2,n1) in links

def counted(n1, n2, n3):
	return n1.startswith('t') or n2.startswith('t') or n3.startswith('t')

def find_triples(nodes, links, need_ts):
	cnodes = [n for n in nodes if nodes[n] > 1]
	triples = []
	for n1 in cnodes:
		for n2 in cnodes:
			if connected(n1, n2, links):
				for n3 in cnodes:
					if connected(n1, n3, links) and connected(n2, n3, links):
						if not need_ts or counted(n1,n2,n3):
							snl = sorted([n1,n2,n3])
							if snl not in triples:
								triples.append(snl)
	return triples

def extend_groups(groups, nodes, links):
	done = False
	while not done:
		ngroups = []
		done = True
		for g in groups:
			for n1 in nodes:
				if n1 in g:
					continue
				if all(connected(n2, n1, links) for n2 in g):
					g2 = sorted([n1] + g)
					if g2 not in ngroups:
						ngroups.append(g2)
						done = False
		if len(ngroups) > 0:
			groups = ngroups
	return groups

def largest_group(groups):
	gs = 0
	gi = 0
	for i in range(len(groups)):
		if len(groups[i]) > gs:
			gi = i
			gs = len(groups[i])
	return groups[gi]

def group_password(group):
	return ','.join(sorted(group))

def part1_for(file_name):
	lines = read_input(file_name)
	nodes, links = process_lines(lines)
	triples = find_triples(nodes, links, True)
	return len(triples)

def part2_for(file_name):
	lines = read_input(file_name)
	nodes, links = process_lines(lines)
	triples = find_triples(nodes, links, False)
	groups = extend_groups(triples, nodes, links)
	big_group = largest_group(groups)
	return group_password(big_group)

# Main processing.
print('Advent of Code 2024 - Day 23, Part 1.')
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
