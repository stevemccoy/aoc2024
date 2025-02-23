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

// Long number for the counts.
typedef unsigned long long number;

const string WHITESPACE = " \n\r\t\f\v";

static int bound_available_index = 0;
static std::map<int, std::map<string, number>> available_index;
static std::set<string> impossibles;

number is_in_index(int ns, const string& s) {
    return (available_index.contains(ns) ? available_index[ns][s] : 0);
}

void add_to_index(const string& s, number count) {
    int ns = s.size();
    if (ns > bound_available_index) {
        bound_available_index = ns;
    }
    available_index[ns][s] += count;
}

void clear_indices() {
    available_index.clear();
    bound_available_index = 0;
    impossibles.clear();
}

string ltrim(const string& s) {
    size_t start = s.find_first_not_of(WHITESPACE);
    return (start == string::npos) ? "" : s.substr(start);
}

string rtrim(const string& s) {
    size_t end = s.find_last_not_of(WHITESPACE);
    return (end == string::npos) ? "" : s.substr(0, end + 1);
}

string trim(const string& s) {
    return rtrim(ltrim(s));
}

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

set<string> process_available(const string& line) {
    clear_indices();
    vector<string> splits = split_delim(line, ',');
    set<string> result;
    for (auto r : splits) {
        string s = trim(r);
        add_to_index(s, 1);
        result.insert(s);
    }
    return result;
}

vector<string> process_required(const std::vector<std::string>& lines) {
    bool firstLineSeen = false;
    std::vector<string> result;
    for (auto line : lines) {
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

bool can_make_from_available(const string& prev_token, const string& required) {
    int nr = required.size();
    if ((nr == 0) || is_in_index(nr, required)) {
        return true;
    }
    if (impossibles.contains(required)) {
        return false;
    }
    if (nr > bound_available_index) {
        nr = bound_available_index;
    }
    for (int na = nr; na > 0; na--) {
        string s = required.substr(0, na);
        if (!impossibles.contains(s) && is_in_index(na, s)) {
            add_to_index(prev_token + s, 1);
            string r = required.substr(na);
            if (can_make_from_available(s, r)) {
                add_to_index(r, 1);
                return true;
            }
        }
    }
    impossibles.insert(required);
    return false;
}

// Need to clear indices and repopulate with available strings before calling this for each of the required patterns.
number count_ways_to_make_from_available(const string& required) {
    int nr = required.size();
    if (nr == 0) {
        return 1;
    }
    number n = is_in_index(nr, required);
    if (n > 0) {
        return n;
    }
    if (impossibles.contains(required)) {
        return 0;
    }
    if (nr > bound_available_index) {
        nr = bound_available_index;
    }
    number total_count = 0;
    for (int na = nr; na > 0; na--) {
        string s = required.substr(0, na);
        if (!impossibles.contains(s)) {
            number cs = is_in_index(na, s);
            if (cs > 0) {
                //   add_to_index(prev_token + s, 1);
                string r = required.substr(na);
                number cr = count_ways_to_make_from_available(r);
                total_count += (cs * cr);
            }
        }
    }
    if (total_count > 0) {
        add_to_index(required, total_count);
    }
    else {
        impossibles.insert(required);
    }
    return total_count;
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
    for (auto req : required) {
        count++;
        cout << "Required: " << req;
        if (can_make_from_available("", req)) {
            cout << " - Success" << endl;
            successes++;
        }
        else {
            cout << " - Fail" << endl;
        }
    }

    cout << "Summary: " << successes << " out of " << count << " designs are possible." << endl;

    cout << "Part 2." << endl;
    number total = 0;
    process_available(lines[0]);

    ofstream out_counts;
    out_counts.open("counts.csv");
    for (auto r : required) {
//        cout << "Required: " << r << " = ";
        count = count_ways_to_make_from_available(r);
        total += count;
        out_counts << count << endl;
//        cout << count << endl;
//        cout << count << " ways." << endl;
    }
    out_counts.close();

    cout << "Total number of ways to make designs = " << total << endl;     
    // NOT 63.
    // NOT 488062108 (too low).
    // NOT 6,223,895,674,012 (too low).
    // NOT 6,758,341,981,715,612
    // NOT 5,371,816,338,089,690


    cout << "Done." << endl;
    return 0;
}
