#
# Advent of Code 2024, Day 1 - Historian Hysteria
#

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def part1_for(file_name):
	lines = read_input(file_name)
	sl = [line.split() for line in lines]
	lefts = [int(s[0]) for s in sl]
	lefts.sort()
	rights = [int(s[1]) for s in sl]
	rights.sort()
	dl = [abs(z[0] - z[1]) for z in zip(lefts, rights)]
	sum_distances = sum(dl)
	return sum_distances

def part2_for(file_name):
	lines = read_input(file_name)
	sl = [line.split() for line in lines]
	lefts = [int(s[0]) for s in sl]
	rights = [int(s[1]) for s in sl]
	score = 0
	for a in lefts:
		score += a * rights.count(a)
	return score

# Files.
test_file = 'test1.txt'
input_file = 'input1.txt'

# Main processing.
print('Advent of Code 2024 - Day 1, Part 1.')
print('Running test...')
count = part1_for(test_file)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file)
print(f"Result is {count}")

print('Part 2.')
print('Running test...')
score = part2_for(test_file)
print(f"Result is {score}")

print('Running full input...')
score = part2_for(input_file)
print(f"Result is {score}")

print("Done")
