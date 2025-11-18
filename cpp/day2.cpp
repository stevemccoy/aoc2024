/*
    Advent of Code 2024 - Day 2 : Red-Nosed Reports
*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

const char* CHALLENGE_TITLE = "Red-Nosed Reports";
const int CHARS_PER_LINE = 1024;
const int MAX_INPUT_PAIRS = 1024;  /* Actually input is 1000 lines. */

/* The input pairs to be processed. */
int num_pairs = 0;
int lefties[MAX_INPUT_PAIRS], righties[MAX_INPUT_PAIRS];


void process_line(const char* line) {
    bool safe = true;
    int first, second;
    if (sscanf(line, "%d %d", &first, &second) != 2) {
	printf("Badly formatted line data could not be processed.\nExpected 2 integers: %s\n", line);
	return;
    }
    lefties[num_pairs] = first;
    righties[num_pairs] = second;
    num_pairs++;
}

void process_input(const char* file_name) {
    char buffer[CHARS_PER_LINE];
    /* Open input file */
    FILE *fp = fopen(file_name, "r");
    if (fp == NULL) {
	printf("Unable to open input file: %s\n", file_name);
	return;
    }
    /* Reset the arrays for the input pairs. */
    num_pairs = 0;
    /* Process each line in turn. */
    char *line;
    int line_number = 1;
    while ((line = fgets(buffer, CHARS_PER_LINE, fp)) != NULL) {
	/* Ignore leading and trailing white space in the line. */
	while (isspace(*line)) {
	    line++;
	}
	int n = strlen(line);
	while ((n > 0) && isspace(line[n - 1])) {
	    line[n - 1] = '\0';
	    n--;
	}
	/* Do stuff with this line */
/*	printf("%d : |%s|\n", line_number, line);
 */
	process_line(line);
	/* Next line */
	line_number++;
    }
    /* Report if processing errored for some reason. */
    if (ferror(fp) != 0) {
	printf("An error occurred reading input file: %s\nNear input line number %d\n",
	       file_name, line_number);
	return;
    }
    /* Close input file. */
    fclose(fp);
}

int cmp_ints(const void* a, const void* b) {
    int ai = *(const int*)a;
    int bi = *(const int*)b;
    return (ai < bi) ? -1 : ((ai > bi) ? 1 : 0);
}

void sort_pairs() {
    qsort(lefties, num_pairs, sizeof(int), cmp_ints);
    qsort(righties, num_pairs, sizeof(int), cmp_ints);   
}

/* Evaluate the answer to the challenge. */
int evaluate_part1() {
    int score = 0;
    int d = 0;
    for (int i = 0; i < num_pairs; i++) {
	d = lefties[i] - righties[i];
	if (d < 0) {
	    d = -d;
	}
	score += d;
    }
    return score;
}

int evaluate_part2() {
    int score = 0;
    int d = 0;
    for (int i = 0; i < num_pairs; i++) {
	/* Count number of repeats in right list of item in left list. */
	const int* vp = &lefties[i];
	void *fnd = bsearch(vp, righties, num_pairs, sizeof(int), cmp_ints);
	if (fnd != NULL) {
	    int j = -1;
	    for (int* ip = (int*)fnd; *ip == lefties[i]; ip--) {
		j++;
	    }
	    for (int* ip = (int*)fnd; *ip == lefties[i]; ip++) {
		j++;
	    }
	    d = j * lefties[i];
//	    printf("Subscore %d for left %d\n", d, lefties[i]);
	    score += d;
	}
    }
    return score;    
}

void part1(const char* file_name) {
    process_input(file_name);
    sort_pairs();
    int result = evaluate_part1();
    printf("Processed all data. Total summed distance was: %d\n", result);
}

void part2(const char* file_name) {
    process_input(file_name);
    sort_pairs();
    int result = evaluate_part2();
    printf("Processed all data. Total summed distance was: %d\n", result);    
}

int main() {
    printf("Advent of Code 2024\n");
    printf("Day 1 - %s\n\n", CHALLENGE_TITLE);
    printf("Part 1. Test data.\n");
    part1("test1.txt");
/*
    printf("Part 1. Full input data.\n");
    part1("input1.txt");

    printf("Part 2. Test data.\n");
    part2("test1.txt");
    printf("Part 2. Full input data.\n");
    part2("input1.txt");
*/
    return 0;
}
