#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

std::vector<int> f(const long long n) {
    std::vector<int> output;
    long long a = n;
    long long b = 0;
    long long c = 0;
    do{
        b = a % 8;
        b = b ^ 1;
        c = a / static_cast<long long>(std::pow(2,b));
        a = a / 8;
        b = (b ^ c) ^ 6;
        for (const auto ele : std::to_string(b % 8)) {
            output.push_back(ele - '0');
        }
    } while (a!=0);
    return output;
}

bool util (long long n, const std::vector<int>& program) {
    if (f(n) == program) {
        std::cout << n << '\n';
        return true;
    }
    n = n << 3;
    for (int i = 0; i < 8; i++) {
        const auto output = f(n);
        bool same = true;
        for (int i = 0; i < output.size(); i++) {
            same = same && output[i] == program[program.size() - output.size() + i];
        }
        if (same && util(n, program)) return true;
        n++;
    }
    return false;
}

int main(int argc, char* argv[]) {
    std::string input = "input17.txt";
    if (argc > 1) {
        input = argv[1];
    }
    std::ifstream file(input);
    std::string line;

    for (int i = 0; i < 5; i++) std::getline(file, line);
    std::vector<int> program;
    std::size_t start = 9;
    std::size_t end = line.find(',', start);
    while(end != std::string::npos) {
        program.push_back(std::stoi(line.substr(start, end - start)));
        start = end + 1;
        end = line.find(',', start);
    }
    program.push_back(std::stoi(line.substr(start, line.size() - start)));
    util(0, program);
}
