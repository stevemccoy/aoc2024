// day22.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

using namespace std;

#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <set>
#include <limits>
#include <algorithm>
#include <inttypes.h>
#include <string>

typedef unsigned long long number;

std::vector<std::string> read_input_file(const char* file_name) {
    std::vector<std::string> result;
    std::ifstream infile(file_name, std::ifstream::in);
    std::string line;
    while (getline(infile, line)) {
        result.push_back(line);
    }
    infile.close();
    return result;
}

std::vector<int> process_lines(std::vector<std::string>& lines) {
    std::vector<int> result;
    int value;
    for (auto line : lines) {
        if (sscanf_s(line.c_str(), "%d", &value) > 0) {
            result.push_back(value);
        }
    }
    return result;
}

vector<string> split_delim(const string& line, char delimiter) {
    vector<string> result;
    size_t startPos = 0, delimPos = line.find_first_of(delimiter);
    while (delimPos != string::npos) {
        string s1 = line.substr(startPos, delimPos - startPos);
        result.push_back(s1);
        startPos = delimPos + 1;
        delimPos = line.find_first_of(delimiter, startPos);
    }
    result.push_back(line.substr(startPos));
    return result;
}

static number mix_in(number secret, number value) {
    return secret ^ value;
}

static number prune(number secret) {
    return secret % 16777216L;
}

static number next_secret(number secret) {
    int m2 = mix_in(secret, secret << 6);
    secret = prune(m2);
    int m4 = mix_in(secret, secret >> 5);
    secret = prune(m4);
    int m6 = mix_in(secret, secret << 11);
    secret = prune(m6);
    return secret;
}

static number* buyer_secrets(number start, int num_steps) {
    number* secrets = new number[num_steps + 1];
    number s = start;
    secrets[0] = s;
    for (int i = 1; i <= num_steps; i++) {
        s = next_secret(s);
        secrets[i] = s;
    }
    return secrets;
}

static int8_t* buyer_price_history(number start, int num_steps, number& secret) {
    int8_t* prices = new int8_t[num_steps + 1];
    number s = start;
    prices[0] = s % 10;
    for (int i = 1; i <= num_steps; i++) {
        s = next_secret(s);
        prices[i] = s % 10;
    }
    secret = s;
    return prices;
}

static int8_t* buyer_price_deltas(int8_t* prices, int num_steps) {
    int8_t* deltas = new int8_t[num_steps + 1];
    deltas[0] = 0;
    for (int i = 1; i <= num_steps; i++) {
        deltas[i] = prices[i] - prices[i - 1];
    }
    return deltas;
}

static int8_t sell_when(
    const int8_t changes[4], 
    const int8_t* prices, 
    const int8_t* deltas, 
    int num_prices) 
{
    int8_t item = changes[0];
    for (int i = 1; i <= num_prices - 3; i++) {
        if (item == deltas[i]) {
            bool match = true;
            for (int j = 1; j < 4; j++) {
                if (changes[j] != deltas[i + j]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                return prices[i + 3];
            }
        }
    }
    return 0;
}

static int total_for_changes(
    const int8_t changes[4], 
    const std::vector<int8_t*>& buyer_prices, 
    const std::vector<int8_t*>& buyer_deltas, 
    int num_prices)
{
    int total = 0;
    int num_buyers = buyer_prices.size();
    for (int i = 0; i < num_buyers; i++) {
        total += sell_when(changes, buyer_prices[i], buyer_deltas[i], num_prices);
    }
    return total;
}

static int best_amount(
    const std::vector<int8_t*>& buyer_prices, 
    const std::vector<int8_t*>& buyer_deltas, 
    int num_prices) 
{
    const int8_t delta_univ[] = {-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    int8_t changes[4]{};
    int best = 0;
    int count = 0;
    int update_count = 10000;
    for (auto i : delta_univ) {
        changes[0] = i;
        for (auto j : delta_univ) {
            changes[1] = j;
            for (auto k : delta_univ) {
                changes[2] = k;
                for (auto m : delta_univ) {
                    changes[3] = m;
                    if (!count--) {
                        printf(
                            "[%hhi,%hhi,%hhi,%hhi]\n", (int)changes[0], (int)changes[1], 
                            (int)changes[2], (int)changes[3]);
                        count = update_count;
                    }
                    int amount = total_for_changes(changes, buyer_prices, buyer_deltas, num_prices);
                    if (amount > best) {
                        best = amount;
                    }
                }
            }
        }
    } 
    return best;
}

int main()
{
    const int num_steps = 2000;

    std::cout << "Advent of Code 2024\nDay 22 - Monkey Market\n";
    std::string fileName = "input22.txt";
    std::vector<int> starts;
    auto lines = read_input_file(fileName.c_str());
    if (lines.size() == 0) {
        std::cerr << "Unable to read input file" << std::endl;
        return 1;
    }
    starts = process_lines(lines);

    std::vector<int8_t*> buyer_prices, buyer_deltas;
    number total_secret = 0L;
    number last_secret = 0;
    for (auto start : starts) {
        number* secrets = buyer_secrets(start, num_steps);
        total_secret += secrets[num_steps];
        int8_t* prices = buyer_price_history(start, num_steps, last_secret);
        buyer_prices.push_back(prices);
        int8_t* deltas = buyer_price_deltas(prices, num_steps);
        buyer_deltas.push_back(deltas);
    }

    printf("Part 1 Solution:\nSum of last secrets = %lld\n", total_secret);

    // 175 too low.
    int best = best_amount(buyer_prices, buyer_deltas, num_steps);
    std::cout << "Part 2 Solution.\nFound best amount = " << best << std::endl;
    std::cout << "Done." << std::endl;
    return 0;
}
