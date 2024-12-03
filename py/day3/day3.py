#
# Advent of Code 2024, Day 3 - Mull It Over
#

import re

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def part1_for(file_name):
	lines = read_input(file_name)
	pattern = re.compile(r'mul\((?P<lhs>\d+),(?P<rhs>\d+)\)')
	count = 0
	for line in lines:
		for m in pattern.findall(line):
			left = int(m[0])
			right = int(m[1])
			count += (left * right)
	return count

def part2_for(file_name):
	lines = read_input(file_name)
	mul_pattern		= re.compile( r'mul\((?P<lhs>\d+),(?P<rhs>\d+)\)' )
	do_pattern 		= re.compile( r'do\(\)' )
	dont_pattern 	= re.compile( r'don\'t\(\)' )
	count = 0
	enabled = 1
	for line in lines:
		spos = 0
		line_length = len(line)

		while spos < line_length:
			mdo = do_pattern.search(line, spos)
			mdont = dont_pattern.search(line, spos)
			mmul = mul_pattern.search(line, spos)

			if not mmul:
				break

			mdospan 	= (line_length,line_length) if not mdo else mdo.span()
			mdontspan 	= (line_length,line_length) if not mdont else mdont.span()
			mmspan 		= mmul.span()

			if enabled:
				if mmspan[0] < mdontspan[0]:
					d = mmul.groupdict()
					left = int(d['lhs'])
					right = int(d['rhs'])
					count += (left * right)
					spos = mmspan[1]
				elif mdontspan[0] < mdospan[0]:
					enabled = 0
					spos = mdontspan[1]
				else:
					spos = mdospan[1]
			else:
				if mdospan[0] < mdontspan[0]:
					enabled = 1
					spos = mdospan[1]
				else:
					spos = mdontspan[1]
	return count

# Files.
test_file_a = 'test3a.txt'
test_file_b = 'test3b.txt'
input_file = 'input3.txt'

# Main processing.
print('Advent of Code 2024 - Day 3, Part 1.')
print('Running test...')
count = part1_for(test_file_a)
print(f"Result is {count}")

print('Running full input...')
count = part1_for(input_file)
print(f"Result is {count}")

print('Part 2.')
print('Running test...')
count = part2_for(test_file_b)
print(f"Result is {count}")

print('Running full input...')
count = part2_for(input_file)
print(f"Result is {count}")

print("Done")
