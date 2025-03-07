#pragma once
#include <vector>
#include <map>
#include "Node.h"

class Edge
{
public:
	Edge(NodePtr s, Cost c, NodePtr d) : m_src(s), m_cost(c), m_dest(d) {}
	virtual ~Edge() {}

	NodePtr src() const { return m_src; }
	Cost cost() const { return m_cost; }
	NodePtr dest() const { return m_dest; }

private:
	NodePtr m_src;
	Cost	m_cost;
	NodePtr m_dest;
};

typedef std::shared_ptr<class Edge> EdgePtr;

class Graph
{
public:
	Graph() {}
	virtual ~Graph() {}

	// Grab a new (not previously used) node Id in this graph.
	Identifier getNewNodeId();

	// Add a new edge to the graph, between pre-existing nodes.
	bool add_edge(Identifier s, Cost c, Identifier d);

	// Add a new node to the graph (returns NULL if id already there).
	NodePtr add_node(Identifier id);

	// Find specific node in the graph (returns NULL if id not in graph).
	NodePtr lookup_node(Identifier id);

	size_t from_source(Identifier n, std::vector<EdgePtr>& result);
	size_t to_dest(Identifier n, std::vector<EdgePtr>& result);

	std::map<Identifier, NodePtr> nodes;

private:
	// Used by getNewNodeId() above.
	static Identifier nextNodeId;

	std::vector<EdgePtr> edges;
	std::multimap<Identifier, EdgePtr> fwd_index;
	std::multimap<Identifier, EdgePtr> bwd_index;
};

typedef std::shared_ptr<class Graph> GraphPtr;
