#include "Graph.h"

// Initial Id for nodes in the Graph.
Identifier Graph::nextNodeId = 1;

Identifier Graph::getNewNodeId()
{
    while (lookup_node(nextNodeId) != nullptr) {
        nextNodeId++;
    }
    return nextNodeId++;
}

bool Graph::add_edge(Identifier s, Cost c, Identifier d)
{
    NodePtr sn = lookup_node(s);
    NodePtr dn = lookup_node(d);
    EdgePtr e(new Edge(sn, c, dn));
    edges.push_back(e);
    fwd_index.insert(std::pair<Identifier, EdgePtr>(s, e));
    bwd_index.insert(std::pair<Identifier, EdgePtr>(d, e));
    return true;
}

NodePtr Graph::add_node(Identifier id)
{
    auto np = nodes.find(id);
    if (np == nodes.end()) {
        NodePtr n(new Node(id));
        nodes[id] = n;
        return n;
    }
    return nullptr;
}

NodePtr Graph::lookup_node(Identifier id)
{
    auto np = nodes.find(id);
    if (np != nodes.end()) {
        return np->second;
    }
    return nullptr;
}

size_t Graph::from_source(Identifier id, std::vector<EdgePtr>& result)
{
    result.clear();
    auto range = fwd_index.equal_range(id);
    for (auto& i = range.first; i != range.second; i++) {
        result.push_back(i->second);
    }
    return result.size();
}

size_t Graph::to_dest(Identifier id, std::vector<EdgePtr>& result)
{
    result.clear();
    auto range = bwd_index.equal_range(id);
    for (auto& i = range.first; i != range.second; i++) {
        result.push_back(i->second);
    }
    return result.size();
}
