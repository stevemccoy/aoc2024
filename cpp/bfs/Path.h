#pragma once
#include "Graph.h"

typedef std::shared_ptr<class Path> PathPtr;

class Path
{
public:
	Path(NodePtr start, Cost c) {
		m_cost = c;
		m_node = start;
		m_path = nullptr;
	}

	Path(PathPtr p, NodePtr n, Cost c) {
		m_node = n;
		m_path = p;
		m_cost = p->cost() + c;
	}

	virtual ~Path() {}

	NodePtr end() const {
		return m_node;
	}

	NodePtr start() const;

	PathPtr path() const { 
		return m_path; 
	}

	Cost cost() const {
		return m_cost;
	}

	bool visits_node(Identifier id) const;

private:
	// Total path cost from start 
	Cost m_cost;
	// End of the path as generated so far.
	NodePtr m_node;
	// Rest of the path.
	PathPtr m_path;
};
