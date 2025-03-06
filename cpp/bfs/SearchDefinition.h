#pragma once
#include <map>
#include "common.h"
#include "Graph.h"

struct NodeMetaData
{
	Identifier id;
	size_t x, y;
	char hdg;
};

class SearchDefinition
{
public:
	NodeMetaData& lookupNodeById(Identifier id) {
		return m_nodeMeta[id];
	}

	Identifier lookupIdByContents(size_t x, size_t y, char h) {
		for (auto& p : m_nodeMeta) {
			if ((p.second.x == x) && (p.second.y == y) && (p.second.hdg == h)) {
				return p.first;
			}
		}
		return 0;
	}

	bool setNodeMetaData(Identifier id, const NodeMetaData& nmd) {
		m_nodeMeta[id] = nmd;
		return true;
	}

	// The search graph itself.
	GraphPtr graph;

	// Start node.
	Identifier startId;

	// Goal node.
	Identifier goalId;

	// Coordinate limits for nodes in search.
	size_t num_x, num_y;

private:
	// Data about each of the identified nodes in the graph.
	std::map<Identifier, NodeMetaData> m_nodeMeta;
};
