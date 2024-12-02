#include <cstdio>
#include <iostream>
#include <cmath>
#include <map>
#include<fstream>
#include<string>
#include<vector>

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

class Pos
{
public:
    int x;
    int y;

    void move(int dx, int dy) {
        x += dx;
        y += dy;
    }
};

bool operator<(const Pos& p1, const Pos& p2) {
    return (p1.x == p2.x ? (p1.y < p2.y) : (p1.x < p2.x));
}

// Part 1.
Pos head = { 100, 100 };
Pos tail = { 100, 100 };

// Part 2. Need to simulate a rope of 10 links.
Pos rope[10];

std::map<Pos, int> trail;

void link_to_follow(Pos& h, Pos& t) {
    int dx = h.x - t.x;
    int dy = h.y - t.y;
    if ((dx < -1) || (dx > 1) || (dy < -1) || (dy > 1)) {
        dx = (dx < 0 ? -1 : (dx > 0 ? 1 : 0));
        dy = (dy < 0 ? -1 : (dy > 0 ? 1 : 0));
        t.move(dx, dy);
    }
}

void move_head(int dx, int dy, bool isPart2) {
    if (isPart2) {
        rope[0].x += dx;
        rope[0].y += dy;
        for (int i = 1; i < 10; i++) {
            link_to_follow(rope[i-1], rope[i]);
        }
        trail[rope[9]]++;
    }
    else {
        head.x += dx;
        head.y += dy;
        link_to_follow(head, tail);
        trail[tail]++;
    }
}

void make_move(char direction, int distance, bool isPart2) {
    switch (direction) {
    case 'U': 
        while (distance--) {
            move_head(0, -1, isPart2);
        }
        break;
    case 'D':        
        while (distance--) {
            move_head(0, 1, isPart2);
        }
        break;
    case 'L': 
        while (distance--) {
            move_head(-1, 0, isPart2);
        }
        break;
    case 'R':
        while (distance--) {
            move_head(1, 0, isPart2);
        }
        break;
    }
//    std::cout << "Head: " << head.x << ", " << head.y << std::endl;
//    std::cout << "Tail: " << tail.x << ", " << tail.y << std::endl;
}

void reset_path() {
    trail.clear();
    head = { 100, 100 };
    tail = { 100, 100 };
    for (int i = 0; i < 10; i++) {
        rope[i] = { 100, 100 };
    }
    trail[tail]++;
}

void make_moves(const std::vector<std::string>& moves, bool isPart2) {
    reset_path();
    char direction = ' ';
    int distance = 0;
    for (auto line : moves) {
        sscanf_s(line.c_str(), "%c %d", &direction, 1, &distance);
        make_move(direction, distance, isPart2);
    }
}

int main()
{
    std::cout << "Advent of Code 2022\nDay 9 -  Part 1." << std::endl;
    std::cout << "Test:" << std::endl;
    auto lines = read_input_file("test9.txt");
    make_moves(lines, false);
    std::cout << "Tail has been to " << trail.size() << " locations." << std::endl;

    std::cout << "Trial:" << std::endl;
    lines = read_input_file("day9.txt");
    make_moves(lines, false);
    std::cout << "Tail has been to " << trail.size() << " locations." << std::endl;

    std::cout << "Part 2.\nTest:" << std::endl;
    lines = read_input_file("test92.txt");
    make_moves(lines, true);
    std::cout << "Tail has been to " << trail.size() << " locations." << std::endl;

    std::cout << "Trial:" << std::endl;
    lines = read_input_file("day9.txt");
    make_moves(lines, true);
    std::cout << "Tail has been to " << trail.size() << " locations." << std::endl;
}
