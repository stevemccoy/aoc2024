#
# Advent of Code 2024, Day 22 - Monkey Market
#

# Files.
test_file = 'test22.txt'
input_file = 'input22.txt'

# Global variables.

# Read the contents of the given file.
def read_input(file_name):
	with open(file_name, 'r') as f:
		return [line.strip() for line in f if len(line) > 0]
	return False

def mix_in(secret, value):
	return secret ^ value

def prune(secret):
	return secret % 16777216

def next_secret(secret):
	m2 = mix_in(secret, secret * 64)
	secret = prune(m2)
	m4 = mix_in(secret, (secret // 32))
	secret = prune(m4)
	m6 = mix_in(secret, secret * 2048)
	secret = prune(m6)
	return secret

def initial_secrets(lines):
	secrets = []
	for line in lines:
		secrets.append(int(line))
	return secrets

def evolve_steps(secrets, nsteps):
	for s in range(nsteps):
		secrets = [next_secret(s) for s in secrets]
	return secrets

def buyer_history(start, nsteps):
	secrets = {0:start}
	prices = {}
	deltas = {}
	s = start
	prev_price = start % 10
	for i in range(1, nsteps + 1):
		s = next_secret(s)
		secrets[i] = s
		p = s % 10
		prices[i] = p
		deltas[i] = p - prev_price
		prev_price = p
	return (secrets, prices, deltas)

def setup_buyers(starts, nsteps):
	buyers = {}
	for i in range(len(starts)):
		buyers[i] = buyer_history(starts[i], nsteps)
	return buyers

def sell_when(changes, buyers):
	amount = 0
	nc = len(changes)
	for b in buyers:
		(_,prices,deltas) = buyers[b]
		for i in deltas:
			if deltas[i] == changes[0]:
				found = True
				for j in range(nc):
					if ((i + j) not in deltas) or (changes[j] != deltas[i + j]):
						found = False
						break
				if found:
					amount += prices[i + nc - 1]
					break
	return amount

def best_amount(buyers):
	delta_univ = [i for i in range(-9, 10)]
	amount = 0
	for i in delta_univ:
		for j in delta_univ:
			for k in delta_univ:
				for m in delta_univ:
					changes = [i,j,k,m]
					a = sell_when(changes, buyers)
					if a > amount:
						amount = a
	return amount

def part1_for(file_name):
	lines = read_input(file_name)
	secrets = initial_secrets(lines)
	buyers = setup_buyers(secrets, 2000)
	amount = best_amount(buyers)
	return amount

def part2_for(file_name):
	lines = read_input(file_name)
	secrets = initial_secrets(lines)
	secrets = evolve_steps(secrets, 2000)
	result = sum(secrets)
	return result

# Main processing.
print('Advent of Code 2024 - Day 22, Part 1.')
print('Running test...')
count = part1_for(test_file)
print(f"Result is {count}")

# print('Running full input...')
# count = part1_for(input_file)
# print(f"Result is {count}")

# print('Part 2.')
# print('Running test...')
# count = part2_for(test_file)
# print(f"Result is {count}")

# print('Running full input...')
# count = part2_for(input_file)
# print(f"Result is {count}")

print("Done")
