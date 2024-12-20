#
# Advent of Code 2024, Day 9 - Disk Fragmenter
#

import numpy as np

# Files.
test_file = 'test9.txt'
input_file = 'input9.txt'

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

# Represent the disk state as array of (id, file_blocks, empty_blocks).
def process_lines(lines):
	id = 0
	buffer = ""
	disk = []
	for line in lines:
		buffer = buffer + line
		while len(buffer) > 2:
			fblock = buffer[0:2]
			buffer = buffer[2:]
			disk.append((id, int(fblock[0]), int(fblock[1])))
			id += 1
	if len(buffer) > 0:
		disk.append((id, int(buffer[0]), 0))
	return disk

def defrag_disk(disk):
	# Move blocks from end to start of disk to fill in spaces.
	si = 0
	while True:
		ei = len(disk) - 1
		(eid, efs, ess) = disk[-1]
		# disk[ei] = (eid, efs, 0)
		while si < ei and efs > 0:
			(sid, sfs, sss) = disk[si]
			if sss > 0:
				if efs >= sss:
					disk[si] = (sid, sfs, 0)
					disk.insert(si + 1, (eid, sss, 0))
					efs -= sss
				else:
					disk[si] = (sid, sfs, 0)
					disk.insert(si + 1, (eid, efs, sss - efs))
					efs = 0
				ei += 1
			si += 1

		del disk[-1]
		if efs > 0:
			disk.append((eid, efs, 0))
			break
	return disk

def filesystem_reorg(disk):
	ei = len(disk) - 1
	while ei > 0:
		(eid, efs, ess) = disk[ei]
		edone = False
		for si in range(ei):
			(sid, sfs, sss) = disk[si]
			if sss >= efs:
				disk[si] = (sid, sfs, 0)
				disk.insert(si + 1, (eid, efs, sss - efs))
				ei += 1
				edone = True
				break
		if edone:
			if ei < len(disk) - 1:
				(tid, tfs, tss) = disk[ei -1]
				disk[ei - 1] = (tid, tfs, tss + efs + ess)
			del disk[ei]
		ei -= 1

	return disk

def disk_checksum(disk):
	result = 0
	pos = 0
	for i in range(len(disk)):
		(id, fs, ss) = disk[i]
		for k in range(fs):
			result += pos * id
			pos += 1
		for k in range(ss):
			pos += 1
	return result

def part1_for(file_name):
	lines = read_input(file_name)
	disk0 = process_lines(lines)
	disk1 = defrag_disk(disk0)
	result = disk_checksum(disk1)
	return result

def part2_for(file_name):
	lines = read_input(file_name)
	disk0 = process_lines(lines)
	disk1 = filesystem_reorg(disk0)
	result = disk_checksum(disk1)
	return result

# Main processing.
print('Advent of Code 2024 - Day 9, Part 1.')
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
