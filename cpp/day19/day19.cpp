//
// day19.cpp : Linen Layout
//

using namespace std;

#include <cstdint>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <algorithm>

// Long number for the counts.
typedef unsigned long long number;

const string WHITESPACE = " \n\r\t\f\v";
const number BIG_NUMBER = 1000000000000L;

static int bound_available_given = 0;
static int bound_available_index = 0;
static std::map<int, std::map<string, number>> available_index;
static std::set<string> impossibles;

static number is_in_index(int ns, const string& s) {
    return (available_index.contains(ns) ? available_index[ns][s] : 0);
}

static void add_to_index(const string& s, number count) {
    int ns = s.size();
    if (ns > bound_available_index) {
        bound_available_index = ns;
    }
    available_index[ns][s] += count;
}

static void clear_indices() {
    available_index.clear();
    bound_available_index = 0;
    impossibles.clear();
}

static string ltrim(const string& s) {
    size_t start = s.find_first_not_of(WHITESPACE);
    return (start == string::npos) ? "" : s.substr(start);
}

static string rtrim(const string& s) {
    size_t end = s.find_last_not_of(WHITESPACE);
    return (end == string::npos) ? "" : s.substr(0, end + 1);
}

static string trim(const string& s) {
    return rtrim(ltrim(s));
}

static std::vector<std::string> read_input_file(const char* file_name) {
    std::vector<std::string> result;
    std::ifstream infile(file_name, std::ifstream::in);
    std::string line;
    while (getline(infile, line)) {
        result.push_back(line);
    }
    infile.close();
    return result;
}

static vector<string> split_delim(const string& line, char delimiter) {
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

static bool sort_by_length(string s1, string s2) {
    return s1.size() < s2.size();
}

static vector<string> process_required(const std::vector<std::string>& lines) {
    bool firstLineSeen = false;
    std::vector<string> result;
    for (auto& line : lines) {
        if (!firstLineSeen && line.size() > 0) {
            firstLineSeen = true;
            continue;
        }
        string s = trim(line);
        if (s.size() > 0) {
            result.push_back(s);
        }
    }
    return result;
}

static bool can_make_from_available(const string& prev_token, const string& required, const set<string>& available) {
    int nr = required.size();
    if ((nr == 0) || available.contains(required) || is_in_index(nr, required)) {
        return true;
    }
    if (impossibles.contains(required)) {
        return false;
    }
    for (int na = nr; na > 0; na--) {
        string s = required.substr(0, na);
        if (!impossibles.contains(s)) {
            if (available.contains(s) || is_in_index(na, s)) {
                add_to_index(prev_token + s, 1);
                string r = required.substr(na);
                if (can_make_from_available(s, r, available)) {
                    add_to_index(r, 1);
                    return true;
                }
            }
        }
    }
    impossibles.insert(required);
    return false;
}

static number count_ways(const string& required, const set<string>& available) {
    int nr = required.size();
    if (nr == 0) {
        return 1;
    }
    if (impossibles.contains(required)) {
        return 0;
    }
    number total_count = is_in_index(nr, required);
    if (total_count > 0) {
        return total_count;
    }
    if (nr > bound_available_given) {
        nr = bound_available_given;
    }
    for (int na = nr; na > 0; na--) {
        string s = required.substr(0, na);
        if (!impossibles.contains(s) && available.contains(s)) {
            string r = required.substr(na);
            number cr = count_ways(r, available);
            total_count += cr;
        }
    }
    if (total_count > 0) {
        add_to_index(required, total_count);
    }
    return total_count;
}

static set<string> process_available(const string& line) {
    // Extract available patterns from comma separated line.
    vector<string> splits = split_delim(line, ',');
    vector<string> mid;
    for (auto r : splits) {
        mid.push_back(trim(r));
    }
    // Sort in order of length.
    sort(mid.begin(), mid.end(), sort_by_length);
    bound_available_given = mid.at(mid.size() - 1).size();
    // Now convert available strings to set and return.
    set<string> result;
    result.insert(mid.begin(), mid.end());
    return result;
}

int main()
{
    std::cout << "Advent of Code 2024\nDay 19 - Linen Layout\n";
    cout << "Part 1.\n";
    const char* file_name = "input19.txt";
    vector<string> lines = read_input_file(file_name);
    set<string> available = process_available(lines[0]);
    vector<string> required = process_required(lines);

    number count = 0, successes = 0;
    for (auto& req : required) {
        count++;
        cout << "Required: " << req;
        if (can_make_from_available("", req, available)) {
            cout << " - Success" << endl;
            successes++;
        }
        else {
            cout << " - Fail" << endl;
        }
    }

    cout << "Summary: " << successes << " out of " << count << " designs are possible." << endl;

    cout << "Part 2." << endl;
    number total1 = 0;
    number total2 = 0;

    // Available patterns should not start this section in the index.
    available_index.clear();
    bound_available_index = 0;

    for (auto r : required) {
        cout << "Required: " << r << " = ";
        count = count_ways(r, available);
        total1 += count;
        if (total1 > BIG_NUMBER) {
            number amount = (total1 / BIG_NUMBER);
            total2 = total2 + amount;
            total1 = total1 - (amount * BIG_NUMBER);
        }
        cout << count << " ways." << endl;
    }

    cout << "Total number of ways to make designs = " << total2 << " * " << BIG_NUMBER << " + " << total1 << endl;

    // NOT                          63.
    // NOT                 488,062,108 (too low).
    // NOT           6,223,895,674,012 (too low).
    // NOT       6,758,341,981,715,612
    // NOT       5,371,816,338,089,690
    // NOT  10,086,762,563,478,978,455
    // NOT 913,977,222,175,247,007,639
    // NOT                 534,490,410

    cout << "Done." << endl;
    return 0;
}
