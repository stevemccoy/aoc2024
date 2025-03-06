#include "Path.h"

NodePtr Path::start() const
{
    PathPtr p = m_path;
    while (p->path() != nullptr) {
        p = p->path();
    }
    return p->end();
}

bool Path::visits_node(Identifier id) const
{
    if (m_node->id() == id) {
        return true;
    }
    PathPtr p = m_path;
    while (p != nullptr) {
        if (p->end()->id() == id) {
            return true;
        }
        p = p->path();
    }
    return false;
}
