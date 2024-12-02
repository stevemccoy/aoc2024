#include <vector>
#include <fstream>
#include <string>

using namespace std;

vector<string> read_input_file(const char* file_name) {
    vector<string> result;
    ifstream infile(file_name, ifstream::in);
    string line;
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


static void tokenize(std::string const& str, const char delim, std::vector<std::string>& out) {
    size_t start;
    size_t end = 0;
    while ((start = str.find_first_not_of(delim, end)) != std::string::npos) {
        end = str.find(delim, start);
        out.push_back(str.substr(start, end - start));
    }
}

// Where lines are a grid of characters.
void setupGrid(const vector<string>& lines) {
    num_rows = lines.size();
    num_cols = lines[0].size();
    if (grid != nullptr) {
        delete[] grid;
        grid = nullptr;
    }

    size_t num_chars = num_cols * num_rows * sizeof(char);
    grid = new char[num_chars];
    memset(grid, 0, num_chars);

    int r = 0, c = 0;
    for (auto& line : lines) {
        c = 0;
        for (auto ch : line) {
            set(c++, r, ch);
        }
        r++;
    }
}

// Pull space delimited list of integers out of given string.
vector<int> extract_numbers(string s) {
    vector<int> result;
    int n = 0;
    for (auto& ns : split_delim(s, ' ')) {
        if (sscanf_s(ns.c_str(), "%d", &n) > 0) {
            result.push_back(n);
        }
    }
    return result;
}


int manhattan_distance(int from_x, int from_y, int to_x, int to_y) {
    return (abs(from_x - to_x) + abs(from_y - to_y));
}

void part1(const char* fileName) {
    auto lines = read_input_file(fileName);
    int sum = 0;
    for (string line : lines) {
        // Do domething.
    }
    cout << "Result is " << sum << endl;
}

void part2(const char* fileName) {
    auto lines = read_input_file(fileName);
    int sum = 0;
    for (string line : lines) {
        // Do domething.
    }
    cout << "Result is " << sum << endl;
}

int main()
{
    cout << "Advent of Code 2024.\n";
    cout << "Day XX: Title and Description Here" << endl;

    cout << "Part 1. Test Input..." << endl;
    part1("input/testXX.txt");
    cout << "Part 1. Actual Input..." << endl;
    part1("input/inputXX.txt");
    cout << "Part 2. Test Input..." << endl;
    part2("input/testXX.txt");
    cout << "Part 2. Actual Input..." << endl;
    part2("input/inputXXX.txt");

    cout << "Finished - Bye." << endl;
}
