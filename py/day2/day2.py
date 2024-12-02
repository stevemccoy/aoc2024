#
# Advent of Code 2024, Day 2 - Red-Nosed Reports
#

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def report_safe(line):
	sl = [int(s) for s in line.split()]
	d0 = sl[1] - sl[0]
	n = len(sl)
	for i in range(1,n):
		if d0 > 0 and sl[i] < sl[i-1]:
			return 0
		if d0 < 0 and sl[i] > sl[i-1]:
			return 0
		d = abs(sl[i] - sl[i-1]) 
		if d < 1 or d > 3:
			return 0
	return 1

def fixable(report):
	sl1 = [int(s) for s in report.split()]
	n = len(sl1)
	for i in range(n):
		sl2 = sl1.copy()
		sl2.pop(i)
		if report_safe(" ".join([str(v) for v in sl2])):
			return True
	return False

def part1_for(file_name):
	lines = read_input(file_name)
	count = sum([report_safe(r) for r in lines])
	return count

def part2_for(file_name):
	lines = read_input(file_name)
	count = 0
	for r in lines:
		if report_safe(r) or fixable(r):
			count += 1
	return count

# Files.
test_file = 'test2.txt'
input_file = 'input2.txt'

# Main processing.
print('Advent of Code 2024 - Day 2, Part 1.')
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
