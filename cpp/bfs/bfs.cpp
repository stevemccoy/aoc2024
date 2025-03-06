// bfs.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <cstdint>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <algorithm>

#include "Graph.h"
#include "Path.h"
#include "SearchDefinition.h"

static bool is_goal(NodePtr n, Identifier id) {
    return n->id() == id;
}

static std::map<NodePtr, Cost> get_neighbours(Graph& g, NodePtr from) {

}

static Identifier ident_from_location(size_t x, size_t y, size_t num_x) {
    return (y * num_x + x);
}

// Path comparator for open list (using lambda).
struct PathCompare
{
    bool operator()(const PathPtr p1, const PathPtr p2) const /* noexcept */
    {
        return (p1->cost() < p2->cost());
    }
};

static void breadth_first_search(
    GraphPtr& gp, 
    Identifier startId, 
    Identifier goalId,
    std::vector<PathPtr>& pathList) 
{
    // Define:
        // Graph to be searched.
        // Start position.
        // Goal test.
        // How to generate neighbours.
    // Maintain: 
        // Path lists in process
        // Open list of paths to be extended.

    // Resulting list of completed paths.
    pathList.clear();
    
    // Open queue must be ordered to provide node in order of smallest cost first.
    std::multiset<PathPtr, PathCompare> open_paths;
    // Set up start and goal nodes.
    NodePtr startNode = gp->lookup_node(startId);
    PathPtr path(new Path(startNode, 0));
    open_paths.insert(path);

    bool goalFound = false;
    std::vector<EdgePtr> neighbour_edges;
    Cost shortestPathCost = 0;

    while (!open_paths.empty()) {
        // Remove shortest path so far from open list.
        auto pp = open_paths.begin();
        path = *pp;
        open_paths.erase(pp);

        NodePtr en = path->end();
        Cost pc = path->cost();
        if (is_goal(en, goalId)) {
            if (shortestPathCost == 0) {
                shortestPathCost = pc;
            }
            else if (pc > shortestPathCost) {
                break;
            }
            goalFound = true;
            pathList.push_back(path);
        }

        // Expand non-visited neighbours.
        if (gp->from_source(en->id(), neighbour_edges)) {
            for (auto& ei : neighbour_edges) {
                if (!path->visits_node(ei->dest()->id())) {
                    PathPtr p2(new Path(path, ei->dest(), ei->cost()));
                    open_paths.insert(p2);
                }
            }
        }
    }
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

static bool setup_search(const std::vector<std::string>& lines, SearchDefinition& searchDef) {

    size_t num_y = lines.size();
    size_t num_x = lines[0].size();
    searchDef.num_x = num_x;
    searchDef.num_y = num_y;

    GraphPtr gp(new Graph());

    for (auto y = 0; y < num_y; y++) {
        std::string line = lines[y];
        if (line.size() < num_x) {
            continue;
        }
        NodePtr prevNode = nullptr;
        for (auto x = 0; x < num_x; x++) {
            char ch = line[x];
            if ((ch == '.')||(ch == 'S')||(ch == 'E')) {
                // New node for this location.
                Identifier id = gp->getNewNodeId();
                NodePtr n = gp->add_node(id);
                NodeMetaData nmd = { id, x, y, '*' };
                searchDef.setNodeMetaData(id, nmd);
                // Start and finish points in search.
                if (ch == 'S') {
                    searchDef.startId = id;
                }
                if (ch == 'E') {
                    searchDef.goalId = id;
                }
                // Add edges if valid.
                if (prevNode) {
                    gp->add_edge(prevNode->id(), 1, id);
                }
                Identifier lastRowNodeId = searchDef.lookupIdByContents(x, y - 1);
                if (lastRowNodeId) {
                    NodePtr lastRowNode = gp->lookup_node(lastRowNodeId);
                    if (lastRowNode != nullptr) {
                        gp->add_edge(lastRowNodeId, 1, id);
                    }
                }
                // Remember node for next one along.
                prevNode = n;
            }
            else {
                // Forget previous node for edges if this one not visitable.
                prevNode = nullptr;
            }
        }
    }
    searchDef.graph = gp;
    return true;
}

int main()
{
    std::cout << "Hello World!\n";
    std::cout << "Advent of Code 2024, Day 16 - Reindeer Maze" << std::endl;

    std::vector<std::string> lines = read_input_file("test16a.txt");
    SearchDefinition searchDef;
    if (!setup_search(lines, searchDef)) {
        std::cerr << "Failed to set up search from input file." << std::endl;
        return 1;
    }

    std::vector<PathPtr> pathList;
    breadth_first_search(searchDef.graph, searchDef.startId, searchDef.goalId, pathList);

}
