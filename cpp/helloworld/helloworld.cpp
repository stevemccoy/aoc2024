#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstring>
#include <set>
#include <chrono>

#include "common.h"

using namespace std;
using namespace std::chrono;

// Most naive prime search algorithm.
void naive_factoring(number limit, std::set<number>& primes)
{
	primes.clear();
    primes.insert(2);
    for (unsigned i = 3; i <= limit; i++) {
        bool isPrime = true;
        for (unsigned p : primes) {
            if (i % p == 0) {
                isPrime = false;
                break;
            }
        }
        if (isPrime) {
            primes.insert(i);
        }
    }
}

// Most naive prime search algorithm.
void naive2_factoring(number limit, std::set<number>& primes)
{
	primes.clear();
    primes.insert(2);
    for (unsigned i = 3; i <= limit; i += 2) {
        bool isPrime = true;
        for (unsigned p : primes) {
            if (i % p == 0) {
                isPrime = false;
                break;
            }
        }
        if (isPrime) {
            primes.insert(i);
        }
    }
}

void prime_sieve1(number limit, std::set<number>& primes)
{
	primes.clear();
	bool* sieve = new bool[limit];
	for (number i = 0; i < limit; i++) {
		sieve[i] = true;
	}
	// Cross out multiples of 2 or higher prime numbers.
	for (number f = 2; f < limit; f++) {
		if (sieve[f]) {
			primes.insert(f);
			for (number m = 2 * f; m < limit; m += f) {
				sieve[m] = false;
			}
		}
	}
	delete[] sieve;
}

void prime_sieve2(number limit, std::set<number>& primes)
{
	primes.clear();
    char *sieve = new char[limit];
    memset(sieve, 1, limit);
	// Cross out multiples of 2 or higher prime numbers.
	for (number f = 2; f < limit; f++) {
		if (sieve[f]) {
			primes.insert(f);
			for (number m = 2 * f; m < limit; m += f) {
				sieve[m] = false;
			}
		}
	}
	delete[] sieve;
}

bool read_primes(const std::string& filename, std::set<number>& primes)
{
	std::ifstream infile(filename, std::ifstream::in);
	number p;
	std::string line;
	std::vector<int> totals;
	int amount = 0, total = 0, max_total = 0;
	while (!infile.eof()) {
		infile >> p;
		primes.insert(p);
	}
	infile.close();
	return true;
}

bool write_primes(const std::string& filename, const std::set<number>& primes)
{
	std::ofstream outfile(filename, std::ofstream::out);
	for (auto p : primes) {
		outfile << p << std::endl;
	}
	outfile.close();
	return true;
}

// Test the speed of running function.
unsigned time_execution(void (*funcpointer) (number, std::set<number>&), number limit, std::set<number>& primes) {
    auto start = chrono::high_resolution_clock::now();
    
    funcpointer(limit, primes);

    auto stop = chrono::high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    return duration.count();
}

unsigned average_time(void (*funcpointer) (number, std::set<number>&), number limit) {
    unsigned total = 0;
    std::set<number> primes;
    for (int i = 0; i < 10; i++) {
        total += time_execution(funcpointer, limit, primes);
    }
    return total / 10;
}

int main()
{
    vector<string> msg {"Hello", "C++", "World", "from", "VS Code", "and the C++ extension!"};
    
    for (const string& word : msg)
    {
        cout << word << " ";
    }
    cout << endl;

    number limit = 1000000;
    std::set<number> primes;
    int ms = 0;

    read_primes("primes.txt", primes);

    cout << "Args limit = " << limit << endl;

    // cout << "Timing naive prime factorisation:\n";
    // ms = time_execution(naive_factoring, limit, primes);
    // cout << "Resulting time = " << ms << " ms" << endl;

    // cout << "Timing naive2 prime factorisation:\n";
    // ms = time_execution(naive2_factoring, limit, primes);
    // cout << "Resulting time = " << ms << " ms" << endl;

    // cout << "Timing sieve1 prime factorisation:\n";
    // ms = average_time(prime_sieve1, limit);
    // cout << "Resulting time = " << ms << " ms" << endl;

    cout << "Timing sieve2 prime factorisation:\n";
    ms = average_time(prime_sieve2, limit);
    cout << "Resulting time = " << ms << " ms" << endl;
}

