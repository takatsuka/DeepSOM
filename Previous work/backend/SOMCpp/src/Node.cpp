#include "Node.hpp"

#include <vector>

#include "Eigen/Dense"

using Eigen::VectorXd;
using namespace std;

Node::Node(const VectorXd& topo_coord, int id_v, const VectorXd& init_pos)
    : topo_coord{topo_coord}, position{init_pos}, id_v{id_v} {
}

void Node::set_pos(const VectorXd& loc) {
    this->position = loc;
}

void Node::add_pos(const VectorXd& delta) {
    this->position += delta;
}

void Node::mul_pos(double scalar) {
    this->position *= scalar;
}

const VectorXd& Node::get_pos() const {
    return this->position;
}

const VectorXd& Node::get_topo() const {
    return this->topo_coord;
}

const int Node::get_id() const {
    return this->id_v;
}

void Node::add_neighbor(Node* neighbor) {
    this->neighbors.push_back(neighbor);
}

const vector<Node*>& Node::get_neighbors() const{
    return this->neighbors;
}