#include "MapHex.hpp"

#include <time.h>

#include <queue>
#include <random>
#include <set>
#include <vector>

#include "Eigen/Dense"
#include "Map2d.hpp"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::MatrixXd;
using Eigen::RowVectorXd;
using Eigen::VectorXd;
using namespace std;

MapHex::MapHex(int t_lim, int inp_dim, vector<int> lengths, int sigma, double l, double alpha)
    : Map2d{t_lim, inp_dim, lengths, sigma, l, alpha} {
    // As usual, lengths is sorted from largest to smallest
    // This ensures that there are more rows than columns
    // Creates the nodes
    this->nodes.reserve(this->lengths[0] * this->lengths[1]);
    for (int col_i = 0; col_i < this->lengths[1]; col_i++) {
        for (int row_i = 0; row_i < this->lengths[0]; row_i++) {
            this->nodes.emplace_back(this->new_node(this->topo_coord_calc(col_i, row_i)));
        }
    }
    // Creates connectivity for the nodes.
    for (int col_i = 0; col_i < this->lengths[1]; col_i++) {
        for (int row_i = 0; row_i < this->lengths[0]; row_i++) {
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
            // The connectivity changes depending if it is an even or odd row
            if (row_i & 1) {
                // In the odd case, connect with the next two columns
                if (this->check_coord_valid(col_i + 1, row_i - 1)) {
                    node.add_neighbor(&this->nodes[this->topo_translater(col_i + 1, row_i - 1)]);
                }
                if (this->check_coord_valid(col_i + 1, row_i + 1)) {
                    node.add_neighbor(&this->nodes[this->topo_translater(col_i + 1, row_i + 1)]);
                }
            } else {
                // In the even case, connect with the previous two columns
                if (this->check_coord_valid(col_i - 1, row_i - 1)) {
                    node.add_neighbor(&this->nodes[this->topo_translater(col_i - 1, row_i - 1)]);
                }
                if (this->check_coord_valid(col_i - 1, row_i + 1)) {
                    node.add_neighbor(&this->nodes[this->topo_translater(col_i - 1, row_i + 1)]);
                }
            }
        }
    }
}

VectorXd MapHex::topo_coord_calc(int col_i, int row_i) {
    // Compute topological position based on row and column index
    // Each hex has a radius of 1
    // Arranged in a way such that the pointy part of the hex points up
    double col_c = sqrt(3.0) * (0.5 * (row_i & 1) + col_i);
    double row_c = 1.5 * row_i;
    return (VectorXd{2} << col_c, row_c).finished();
}