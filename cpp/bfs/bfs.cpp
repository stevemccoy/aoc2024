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

#include "SearchDefinition.h"
#include "Path.h"

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
    const std::set<Identifier>& goalIds,
    Cost maximumAllowablePathCost,
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
        // Closed list of paths already extended.

    // Resulting list of completed paths.
    pathList.clear();
    
    // Open queue must be ordered to provide node in order of smallest cost first.
    std::multiset<PathPtr, PathCompare> open_paths;
    // Closed nodes.
    std::set<Identifier> closed_nodes;
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
        if (goalIds.find(en->id()) != goalIds.end()) {
            if (shortestPathCost == 0) {
                shortestPathCost = pc;
            }
            else if (pc > shortestPathCost) {
                break;
            }
            goalFound = true;
            pathList.push_back(path);
            // Don't expand neighbours if this is a shortest solution path.
            continue;
        }

        // Expand non-visited neighbours.
        if (gp->from_source(en->id(), neighbour_edges)) {
            for (auto& ei : neighbour_edges) {
                Identifier nid = ei->dest()->id();
                if (closed_nodes.find(nid) == closed_nodes.end()) {
                    if (ei->cost() + pc < maximumAllowablePathCost) {
                        if (!path->visits_node(nid)) {
                            PathPtr p2(new Path(path, ei->dest(), ei->cost()));
                            open_paths.insert(p2);
                        }
                    }
                }
            }
        }

        // Mark this node as visited now.
        closed_nodes.insert(en->id());
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

    const char headings[4] = { 'n', 'e', 's', 'w' };
    const Cost rotation_cost = 1000;
    const Cost move_cost = 1;

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
                // Nodes for each of the possible heading directions.
                NodePtr tempNodes[4];
                for (int hi = 0; hi < 4; hi++) {
                    char h = headings[hi];

                    // New node for this location and heading.
                    Identifier id = gp->getNewNodeId();
                    NodePtr n = gp->add_node(id);
                    NodeMetaData nmd = { id, x, y, h };
                    searchDef.setNodeMetaData(id, nmd);

                    // Start and finish points in search.
                    if ((ch == 'S') && (h == 'e')) {
                        searchDef.startId = id;
                    }
                    if (ch == 'E') {
                        searchDef.goalIds.insert(id);
                    }
                    tempNodes[hi] = n;
                }
                // Add edges for rotations.
                for (int hi = 0; hi < 4; hi++) {
                    Identifier s = tempNodes[hi]->id();
                    Identifier d = tempNodes[(hi + 1) % 4]->id();
                    gp->add_edge(s, rotation_cost, d);
                    gp->add_edge(d, rotation_cost, s);
                }
            }
        }
    }
    // Now add edges for all the legal moves between different locations.
    for (auto& p : gp->nodes) {
        Identifier sid = p.first;
        NodeMetaData nmds = searchDef.lookupNodeById(sid);
        Identifier did = 0;
        switch (nmds.hdg) {
        case 'n':
            did = searchDef.lookupIdByContents(nmds.x, nmds.y - 1, 'n');
            break;
        case 'e':
            did = searchDef.lookupIdByContents(nmds.x + 1, nmds.y, 'e');
            break;
        case 's':
            did = searchDef.lookupIdByContents(nmds.x, nmds.y + 1, 's');
            break;
        case 'w':
            did = searchDef.lookupIdByContents(nmds.x - 1, nmds.y, 'w');
            break;
        }
        if (did) {
            gp->add_edge(sid, move_cost, did);
        }
    }
    // Done.
    searchDef.graph = gp;
    return true;
}

static std::set<Identifier> nodes_visited(const PathPtr& path) {
    std::set<Identifier> result;
    PathPtr p = path;
    while (p != nullptr) {
        result.insert(p->end()->id());
        p = p->path();
    }
    return result;
}

static std::set<Identifier> nodes_visited(const std::vector<PathPtr>& paths) {
    std::set<Identifier> result;
    for (auto& p : paths) {
        auto nvl = nodes_visited(p);
        result.insert(nvl.begin(), nvl.end());
    }
    return result;
}

static bool solve_for(const char* fileName) {

    std::cout << "Part 1." << std::endl;
    std::vector<std::string> lines = read_input_file(fileName);
    SearchDefinition searchDef;
    if (!setup_search(lines, searchDef)) {
        std::cerr << "Failed to set up search from input file " << fileName << std::endl;
        return false;
    }

    std::vector<PathPtr> pathList;
    breadth_first_search(searchDef.graph, searchDef.startId, searchDef.goalIds, 100000L, pathList);
    std::cout << "Lowest score for reindeer path = " << pathList[0]->cost() << std::endl;

    std::cout << "Part 2." << std::endl;
    std::set<Identifier> ids = nodes_visited(pathList);
    std::set<int> locs;
    for (auto& id : ids) {
        auto ndm = searchDef.lookupNodeById(id);
        int v = ndm.y * searchDef.num_x + ndm.x;
        locs.insert(v);
    }

    std::cout << "Number of distinct locations visited = " << locs.size() << std::endl;
    return true;
}

int main()
{
    std::cout << "Advent of Code 2024, Day 16 - Reindeer Maze" << std::endl;
    //solve_for("test16b.txt");
    solve_for("input16.txt");
}
