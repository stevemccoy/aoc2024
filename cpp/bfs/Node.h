#pragma once
#include <memory>
#include "common.h"

class Node
{
public:
	Node(Identifier id) : m_id(id) {}
	virtual ~Node() {}

	Identifier id() const { return m_id; }
	
private:
	Identifier m_id;
};

typedef std::shared_ptr<Node> NodePtr;
