/*
* Advent of Code 2021, Day 23 - Part 2.
* 
* Minimum cost search using Dijkstra's algorithm.
*/
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <list>
#include <sstream>
#include <cstring>

// Connections between locations in the State picture (1-based index).
// Must have smaller of two indices as first and larger as second in the pair.
static std::multimap<int, int> connections = {
    {1,2},{2,3},{3,4},{4,5},{5,6},{6,7},
    {3,8},{8,9},{9,10},{10,11},{11,12},{12,13},
    {9,14},{14,15},{15,16},{16,17},{17,18},{18,19},
    {15,20},{20,21},{21,22},{22,23},{23,24},{24,25},
    {21,26},{26,27} };

// Places that must remain unoccupied at all times.
static std::set<int> nonStopLocations = { 3, 9, 15, 21 };

// Which of the locations are home, and for which type.
static std::map<int, char> homeLocations = {
    {4,'a'},{5,'a'},{6,'a'},{7,'a'},
    {10,'b'},{11,'b'},{12,'b'},{13,'b'},
    {16,'c'},{17,'c'},{18,'c'},{19,'c'},
    {22,'d'},{23,'d'},{24,'d'},{25,'d'}
};

// Costs to move each of the types of amphipod.
static std::map<char, int> stepCosts = { {'a', 1},{'b', 10},{'c', 100},{'d', 1000} };

// Names of the location indices (including 0 = none).
static std::vector<const char*> placeNames = {"none",
    "h1", "h2", "ha", "a1", "a2", "a3", "a4", "h3", "hb", "b1", "b2", "b3", "b4", "h4",
    "hc", "c1", "c2", "c3", "c4", "h5", "hd", "d1", "d2", "d3", "d4", "h6", "h7" };

// Encode the state of the search using this class.
class State
{
public:
    std::string Value;
    int g;
    int h;
    int f;

    State(const std::string& v, int c = INT_MAX) : Value(v), g(c), h(0), f(c) {}

    char get(int i) const {
        if (!isIndexValid(i)) {
            throw "Index out of range for State.";
        }
        return Value[i - 1];
    }

    char getUpper(int i) const {
        return toupper(get(i));
    }

    // Consider states the same ignoring any difference in Cost.
    bool operator==(const State& other) const {
        return (Value == other.Value);
    }

    bool isValid() const {
        // Length must be 27.
        if (Value.size() != 27) {
            return false;
        }
        // Prohibited locations must be blank.
        if ((get(3) != '.') || (get(9) != '.') || (get(15) != '.') || (get(21) != '.')) {
            return false;
        }
        // Must be 4 each of a, b, c, d.
        if ((countFinds('a') != 4) || (countFinds('b') != 4) || (countFinds('c') != 4) || (countFinds('d') != 4)) {
            return false;
        }
        return true;
    }

    bool isPackedFor(char t) const {
        bool wantEmpties = true;
        for (auto loc : homeLocations) {
            if (loc.second == t) {
                char ch = get(loc.first);
                if (wantEmpties && (ch != '.')) {
                    wantEmpties = false;
                }
                if (!wantEmpties && ch != t) {
                    return false;
                }
            }
        }
        return true;
    }

    bool isIndexValid(int i) const {
        return ((i >= 1) && (i <= 27));
    }

    std::string toString() const {
        char buffer[80];
        sprintf_s(buffer, "%s - %d / %d / %d", Value.c_str(), g, h, f);
        return buffer;
    }

    void display() const {
        std::cout << "#############" << std::endl;
        std::cout
            << "#" << getUpper(1) << getUpper(2) << getUpper(3)
            << getUpper(8) << getUpper(9)
            << getUpper(14) << getUpper(15)
            << getUpper(20) << getUpper(21)
            << getUpper(26) << getUpper(27) << "#" << std::endl;
        std::cout << "###" << getUpper(4) << "#" << getUpper(10) << "#" << getUpper(16) << "#" << getUpper(22) << "###" << std::endl;
        std::cout << "  #" << getUpper(5) << "#" << getUpper(11) << "#" << getUpper(17) << "#" << getUpper(23) << "#" << std::endl;
        std::cout << "  #" << getUpper(6) << "#" << getUpper(12) << "#" << getUpper(18) << "#" << getUpper(24) << "#" << std::endl;
        std::cout << "  #" << getUpper(7) << "#" << getUpper(13) << "#" << getUpper(19) << "#" << getUpper(25) << "#" << std::endl;
        std::cout << "  #########" << std::endl;
    }

private:
    int countFinds(char t) const {
        int count = 0;
        std::size_t found = Value.find(t);
        while (found != std::string::npos) {
            count++;
            found = Value.find(t, found + 1);
        }
        return count;
    }

};
typedef std::shared_ptr<State> StatePtr;



// Reference copies of each State:
static std::map<std::string, StatePtr> allStates;

static StatePtr find_state(std::string value) {
    auto si = allStates.find(value);
    if (si == allStates.end()) {
        StatePtr sp(new State(value));
        return sp;
    }
    return si->second;
}

// Where we're aiming for.
static StatePtr goalState;

struct StateCompare
{
    bool operator()(const StatePtr s1, const StatePtr s2) const /* noexcept */
    {
        return (s1->f < s2->f);
    }
};

static std::vector<int> connected_locations(int from) {
    std::vector<int> result;
    for (auto p : connections) {
        if (p.first == from) {
            result.push_back(p.second);
        }
        else if (p.second == from) {
            result.push_back(p.first);
        }
    }
    return result;
}

// Check that there is an open path in the given state, from one location to another,
// connected and open between source and destination, and at destination.
static int path_open(StatePtr s, int fromLocation, int toLocation, std::set<int>& avoid, bool needOpenPath) {
    avoid.insert(fromLocation);
    if (fromLocation == toLocation) {
        return 0;
    }
    else {
        auto locs = connected_locations(fromLocation);
        for (auto loc : locs) {
            if (avoid.find(loc) == avoid.end()) {
                if (!needOpenPath || (s->get(loc) == '.')) {
                    int len = path_open(s, loc, toLocation, avoid, needOpenPath);
                    if (len != -1) {
                        return 1 + len;
                    }
                    avoid.erase(loc);
                }
            }
        }
        return -1;
    }
}

static int heuristic(StatePtr s) {
    return 0;
    int total = 0;
    int d = 0;
    std::set<int> avoid;
    for (int loc = 1; loc <= 27; loc++) {
        avoid.clear();
        switch (s->get(loc)) {
        case 'a':
            d = path_open(s, loc, 7, avoid, false);
            break;
        case 'b':
            d = path_open(s, loc, 13, avoid, false) * 10;
            break;
        case 'c':
            d = path_open(s, loc, 19, avoid, false) * 100;
            break;
        case 'd':
            d = path_open(s, loc, 25, avoid, false) * 1000;
            break;
        default:
            d = 0;
            break;
        }
        if (d > 0) {
            total += d;
        }
    }
    return total;
}

// Generate state after given move on given State, populated with the move cost.
static StatePtr do_move(StatePtr s, int fromLocation, int toLocation, int numSteps) {
    std::string value(s->Value);
    int stepCost = stepCosts[s->get(fromLocation)];
    if (s->isIndexValid(fromLocation) && s->isIndexValid(toLocation)) {
        value[toLocation - 1] = value[fromLocation - 1];
        value[fromLocation - 1] = '.';
    }
    auto after = find_state(value);
    after->g = s->g + numSteps * stepCost;
    after->h = heuristic(after);
    after->f = after->g + after->h;
    return after;
}

static std::string describe_move(StatePtr from, StatePtr to) {
    char ch = '.';
    int floc, tloc;
    for (int i = 1; i <= 27; i++) {
        char fchar = from->get(i);
        if (fchar != to->get(i)) {
            if (fchar != '.') {
                ch = fchar;
                floc = i;
            }
            else {
                tloc = i;
            }
        }
    }
    char buffer[80];
    sprintf_s(buffer, "%c: %s -> %s", ch, placeNames[floc], placeNames[tloc]);
    return buffer;
}

// Generate move from given State moving an amphipod into its home burrow.
static StatePtr homing_move(const StatePtr& s, int fromLocation)
{
    char ch = s->get(fromLocation);
    // Where to? Find mouth of the burrow.
    int toLocation = 1;
    for (auto p : homeLocations) {
        if (p.second == ch) {
            toLocation = p.first;
            break;
        }
    }
    // Go in till you hit something.
    while ((homeLocations.find(toLocation) != homeLocations.end())&&(s->get(toLocation) == '.')) {
        toLocation++;
    }
    // Then back up.
    toLocation--;
    // Check the path is navigable (nothing in the way).
    std::set<int> avoid;
    int steps = path_open(s, fromLocation, toLocation, avoid, true);
    if (steps != -1) {
        return do_move(s, fromLocation, toLocation, steps);
    }
    else {
        return nullptr;
    }
}

// Generate the moves of a given amphipod into accessible hallway locations,
static std::vector<StatePtr> hallway_moves(StatePtr s, int fromLocation)
{
    std::vector<StatePtr> result;
    std::set<int> avoid;
    // Scan for accessible destinations.
    for (int loc = 1; loc <= 27; loc++) {
        // Going somewhere that's empty, not a home location and not a prohibited hallway location.
        if ((loc != fromLocation) && (s->get(loc) == '.') && (homeLocations.find(loc) == homeLocations.end())
            && (nonStopLocations.find(loc) == nonStopLocations.end())) {

            avoid.clear();
            int steps = path_open(s, fromLocation, loc, avoid, true);
            if (steps == -1) {
                continue;
            }            
            result.push_back(do_move(s, fromLocation, loc, steps));
        }
    }
    return result;
}

static void getNeighbours(const StatePtr s, std::vector<StatePtr>& neighbours, const std::set<StatePtr>& seen, bool isDebug)
{
    if (isDebug) {
        std::cout << "getNeighbours From: " << s->toString() << std::endl;
    }
    // Get neighbouring states to s, with Cost computed as cost of s + move cost.
    // Do not return any that already have made it into seen list.
    neighbours.clear();
    for (int loc = 1; loc <= 27; loc++) {
        // Something to move?
        char ch = s->get(loc);
        if (ch != '.') {
            // Outside a burrow (i.e. not home for anybody)?  Only option is a homing move.
            if (homeLocations.find(loc) == homeLocations.end()) {
                // Burrow is ready for this type.
                if (s->isPackedFor(ch)) {
                    auto m = homing_move(s, loc);
                    if ((m != nullptr) && (seen.find(m) == seen.end())) {
                        if (isDebug) {
                            std::cout << "Homing: " << describe_move(s, m) << std::endl;
                        }
                        neighbours.push_back(m);
                    }
                }
                continue;
            }
            // Is it already home?
            else if (homeLocations[loc] == ch) {
                // Amphipod is home, but if burrow contains other types, consider moving out 
                // temporarily.
                if (!s->isPackedFor(ch)) {
                    for (auto move : hallway_moves(s, loc)) {
                        if (seen.find(move) == seen.end()) {
                            if (isDebug) {
                                std::cout << "Hallway: " << describe_move(s, move) << std::endl;
                            }
                            neighbours.push_back(move);
                        }
                    }
                }
            }
            // Is it in somebody else's burrow?
            else {
                // Home to home move?
                if (s->isPackedFor(ch)) {
                    auto m = homing_move(s, loc);
                    if ((m != nullptr) && (seen.find(m) == seen.end())) {
                        if (isDebug) {
                            std::cout << "Homing: " << describe_move(s, m) << std::endl;
                        }
                        neighbours.push_back(m);
//                        continue;
                    }
                }
                // Move out to the hallway instead, then.
                auto moves = hallway_moves(s, loc);
                for (auto move : moves) {
                    if (seen.find(move) == seen.end()) {
                        if (isDebug) {
                            std::cout << "Hallway: " << describe_move(s, move) << std::endl;
                        }
                        neighbours.push_back(move);
                    }
                }
            }
        }
    }
}

// Present a menu of successor states and allow the user to select one.
static StatePtr choose_move(const StatePtr& from, const std::vector<StatePtr>& options) {
    std::cout << from->toString() << std::endl;
    int choice = -1;
    for (size_t i = 0; i < options.size(); i++) {

        std::cout << i << ". " << describe_move(from, options[i]) << std::endl;
    }
    std::cout << "Choose : ";
    std::cin >> choice;
    if (choice < 0 || choice >= options.size()) {
        return nullptr;
    }
    return options[choice];
}

static std::list<StatePtr> dijkstra(StatePtr start)
{
    // Initialise vertex priority queue Q.
    std::multiset<StatePtr, StateCompare> Q;
    std::vector<StatePtr> neighbourList;
    std::set<StatePtr> seen;
    std::list<StatePtr> result;

    // Initialise.
    std::map<StatePtr, int> dist;
    std::map<StatePtr, StatePtr> prev;
    start->g = 0;
    start->h = heuristic(start);
    start->f = start->h;
    dist[start] = start->f;
    Q.insert(start);

    while (!Q.empty())
    {
        // Remove minimum distance node from queue.
        auto up = Q.begin();
        auto u = *up;
        Q.erase(up);
//        seen.insert(u);

        std::cout << u->toString() << std::endl;

        // Found the goal state - construct the path vector in the correct order.
        if (u->Value == goalState->Value) {
            while (u != nullptr) {
                result.push_front(u);
                auto tmp = prev.find(u);
                u = ((tmp == prev.end()) ? nullptr : tmp->second);
            }
            return result;
        }

        if (seen.find(u) == seen.end()) {

            // For each neighbour v of u not yet in seen.
            getNeighbours(u, neighbourList, seen, false);
            /*
                    StatePtr v = choose_move(u, neighbourList);
                    if (v == nullptr) {
                        break;
                    }
                    v->display();
            */
            for (auto v : neighbourList) {
/*                if (Q.find(v) == Q.end()) {
                    Q.insert(v);
                }
                prev[v] = u;
*/

                // Maintain record of min distance in dist[].
                if (dist.find(v) == dist.end() || dist[v] > v->f) {
                    dist[v] = v->f;
                }

                prev[v] = u;
                if (Q.find(v) == Q.end())
                {
                    Q.insert(v);
                }

            }

            seen.insert(u);
        }
    }
    // In error, return an empty path?
    return result;
}


int main()
{
    goalState = find_state("...aaaa..bbbb..cccc..dddd..");
    std::cout << "Advent of Code 2021 - Day 23\nPart 2\n" << "Goal State:  " << goalState->Value << std::endl;
    std::cout << (goalState->isValid() ? "validated" : "invalid") << std::endl;

    StatePtr start = find_state("...bdda..ccbd..bbac..daca..");
//    StatePtr start = find_state("...dddd..ccbc..abab..baca..");
    std::cout << "Start State: " << start->Value << std::endl;
    start->display();
    std::cout << (start->isValid() ? "validated" : "invalid") << std::endl;

//    StatePtr s = find_state("cc....ab....cd..babd.bacadd");
//    auto r = dijkstra(s);

    auto result = dijkstra(start);
    if (result.empty()) {
        std::cout << "No path found. Sorry." << std::endl;
    }
    else {
        StatePtr sp = result.back();
        std::cout << "Path found: Cost = " << sp->g << std::endl;
    }
}
