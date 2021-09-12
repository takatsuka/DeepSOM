#include "MapRect.hpp"

#include <time.h>

#include <queue>
#include <random>
#include <set>
#include <vector>
#include <iostream>

#include "Eigen/Dense"
#include "Map2d.hpp"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::MatrixXd;
using Eigen::RowVectorXd;
using Eigen::VectorXd;
using namespace std;

MapRect::MapRect(int t_lim, int inp_dim, vector<int> lengths, int sigma, double l, double alpha)
    : Map2d{t_lim, inp_dim, lengths, sigma, l, alpha} {
    // As usual, lengths is sorted from largest to smallest
    // This ensures that there are more rows than columns
    // Creates the nodes
    this->nodes.reserve(this->lengths[0] * this->lengths[1]);
    for (int col_i = 0; col_i < this->lengths[1]; col_i++){
        for (int row_i = 0; row_i < this->lengths[0]; row_i++){
            this->nodes.emplace_back(this->new_node((VectorXd{2} << col_i, row_i).finished()));
        }
    }
    // Creates connectivity for the nodes.
    for (int col_i = 0; col_i < this->lengths[1]; col_i++) {
        for (int row_i = 0; row_i < this->lengths[0]; row_i++) {
            // Nodes are stored in column-major order, and appropriate node selected
            Node& node = this->nodes[this->topo_translater(col_i, row_i)];
            if (this->check_coord_valid(col_i, row_i - 1)) {
                node.add_neighbor(&this->nodes[this->topo_translater(col_i, row_i - 1)]);
            }
            if (this->check_coord_valid(col_i, row_i + 1)) {
                node.add_neighbor(&this->nodes[this->topo_translater(col_i, row_i + 1)]);
            }
            if (this->check_coord_valid(col_i - 1, row_i)) {
                node.add_neighbor(&this->nodes[this->topo_translater(col_i - 1, row_i)]);
            }
            if (this->check_coord_valid(col_i + 1, row_i)) {
                node.add_neighbor(&this->nodes[this->topo_translater(col_i + 1, row_i)]);
            }
        }
    }
}