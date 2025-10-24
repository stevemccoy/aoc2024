/*
    Advent of Code 2024 - Day 1 : Historian Hysteria

*/

#include <stdio.h>
#include <stdlib.h>

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstring>
#include <set>
#include <chrono>

using namespace std;

const char* CHALLENGE_TITLE = "Historian Hysteria";
const int CHARS_PER_LINE = 1024;

int main() {
    printf("Advent of Code 2024 - Day 1\n");
    printf("Day 1 - %s\n\n", CHALLENGE_TITLE);

    vector<string> msg {"Hello", "C++", "World", "from", "VS Code", "and the C++ extension!"};

    set<string> available;
    if (available.contains("hello")) {
        cout << "Hello found." << endl;
    }
    
    for (const string& word : msg)
    {
        cout << word << " ";
    }
    cout << endl;

    const char *file_name = "test1.txt";
    return 0;

    // Open input file.
    FILE *fp = fopen(file_name, "r");
    if (fp == NULL) {
        printf("Error - unable to open file: %s\nQuitting...\n", file_name);
        exit(-1);
    }

    char buffer[CHARS_PER_LINE];
    *buffer = '\0';

    while (fgets(buffer, CHARS_PER_LINE, fp) != NULL) {
        printf("|%s|\n", buffer);
    }

    // Close input file.
    fclose(fp);

    return 0;
}
