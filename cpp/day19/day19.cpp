//
// day19.cpp : Linen Layout
//

using namespace std;

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <set>

const string WHITESPACE = " \n\r\t\f\v";

static int bound_available_index = 0;
static std::map<int, std::set<string>> available_index;
static std::set<string> impossibles;

bool is_in_index(int ns, const string& s) {
    return available_index.contains(ns) && available_index[ns].contains(s);
}

void add_to_index(const string& s) {
    int ns = s.size();
    if (ns > bound_available_index) {
        bound_available_index = ns;
    }
    available_index[ns].insert(s);
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
        add_to_index(s);
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
            add_to_index(prev_token + s);
            string r = required.substr(na);
            if (can_make_from_available(s, r)) {
                add_to_index(r);
                return true;
            }
        }
    }
    impossibles.insert(required);
    return false;
}

int count_ways_to_make_from_available(const string& required, const set<string>& available) {
    int count = 0;
    int nr = required.size();
    if (nr == 0) {
        return 1;
    }
    if (impossibles.contains(required)) {
        return 0;
    }
    for (auto a : available) {
        if (required.starts_with(a)) {
            int na = a.size();
            int sc = count_ways_to_make_from_available(required.substr(na), available);
            count += sc;
        }
    }
    return count;
}

int main()
{
    std::cout << "Advent of Code 2024\nDay 19 - Linen Layout\n";
    cout << "Part 1.\n";
    const char* file_name = "input19.txt";
    vector<string> lines = read_input_file(file_name);
    set<string> available = process_available(lines[0]);
    vector<string> required = process_required(lines);

    int count = 0, successes = 0;
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
    int total = 0;
    for (auto r : required) {
        cout << "Required: " << r << " = ";
        count = count_ways_to_make_from_available(r, available);
        total += count;
        cout << count << " ways." << endl;
    }

    cout << "Total number of ways to make designs = " << total << endl;
    cout << "Done." << endl;
    return 0;
}
