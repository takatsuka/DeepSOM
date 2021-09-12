#include "Map2d.hpp"

#include <time.h>

#include <queue>
#include <random>
#include <set>
#include <vector>

#include "Eigen/Dense"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::MatrixXd;
using Eigen::RowVectorXd;
using Eigen::VectorXd;
using namespace std;

Map2d::Map2d(int t_lim, int inp_dim, int side_len, int sigma = 0, double l = 0, double alpha = 0.5)
    : SOM{t_lim, inp_dim}, side_len{side_len}, sigma{sigma}, l{l}, alpha{alpha} {
        // Note: SOM PAK initial learning rate is 0.05
    srand((unsigned int)time(0));
    this->alpha = alpha;
    if (this->sigma == 0) {  // Starting neighborhood radius (default: 80% of side length)
        this->sigma = max(this->side_len * 0.8, 2.0);
    }
    if (this->l == 0) {  // Time constant for neighbourhood size and learning rate
            // Larger values lead to slower decay (default: 80% of number of iterations)
        //this->l = 3501 * 0.8;
        this->l = this->t_lim * 0.8;  // Conflucting defitions of t_lim for stochastic and batch training
    }
    this->nodes.reserve(side_len * side_len);
    for (int i = 0; i < side_len * side_len; i++) {
        int col_i = i / this->side_len;
        int row_i = i % this->side_len;
        this->nodes.push_back(this->new_node((VectorXd{2} << col_i, row_i).finished()));
    }
    for (int i = 0; i < side_len * side_len; i++) {
        int col_i = i / this->side_len;
        int row_i = i % this->side_len;
        Node& node = this->nodes[this->topo_translater(col_i, row_i)];
        if (col_i != 0) {
            node.add_neighbor(&this->nodes[this->topo_translater(col_i - 1, row_i)]);
        }
        if (col_i != this->side_len - 1) {
            node.add_neighbor(&this->nodes[this->topo_translater(col_i + 1, row_i)]);
        }
        if (row_i != 0) {
            node.add_neighbor(&this->nodes[this->topo_translater(col_i, row_i - 1)]);
        }
        if (row_i != this->side_len - 1) {
            node.add_neighbor(&this->nodes[this->topo_translater(col_i, row_i + 1)]);
        }
    }
}

vector<Node>& Map2d::get_nodes() {
    return this->nodes;
}

double Map2d::neighbor_multiplier(Node& best, Node& n2, int t) {
    double dist_sqr = this->distance_sqr(best.get_pos(), n2.get_pos());
    double dist_mult = exp((-1.0 * dist_sqr) / (2 * pow(this->neighbor_size(t), 2)));
    if (dist_mult < 0.001) {
        return 0;
    } else {
        return dist_mult;
    }
}

double Map2d::learning_rate(int t) {
    return 1.0 * this->alpha * exp(1.0 * -t / this->l);
}

double Map2d::neighbor_size(int t) {
    return this->sigma * exp(1.0 * -t / this->l);
}

void Map2d::node_initialisation(vector<VectorXd>& datas) {
    int n = datas.size();
    int m = datas[0].size();
    MatrixXd matrix_datas(n, m);
    for (int i = 0; i < n; i++) {
        matrix_datas.row(i) = datas[i];
    }
    RowVectorXd centroid = matrix_datas.colwise().mean();
    MatrixXd centered = matrix_datas.rowwise() - centroid;
    MatrixXd cov_var = (centered.adjoint() * centered).array() / (centered.rows() - 1);
    Eigen::SelfAdjointEigenSolver<MatrixXd> eig_solver(cov_var);
    MatrixXd eig_vec = eig_solver.eigenvectors();
    VectorXd eig_val = eig_solver.eigenvalues();
    vector<int> indices(m);
    iota(indices.begin(), indices.end(), 0);
    sort(indices.begin(), indices.end(), [&eig_val](int l, int r) {
        return eig_val[l] > eig_val[r];
    });
    vector<pair<double, double>> bounds;
    for (int i = 0; i < 2; i++){
        RowVectorXd dist = centered * eig_vec.col(indices[i]);
        bounds.push_back(make_pair(dist.minCoeff(), dist.maxCoeff()));
    }
    for (int i = 0; i < this->side_len; i++){ // which row
        for (int j = 0; j < this->side_len; j++){ // which col
            VectorXd to_build = centroid.adjoint();
            to_build += eig_vec.col(indices[0]) * (1.0 * (i - (this->side_len - 1.0) / 2.0) / this->side_len * (bounds[0].second - bounds[0].first));
            to_build += eig_vec.col(indices[1]) * (1.0 * (j - (this->side_len - 1.0) / 2.0) / this->side_len * (bounds[1].second - bounds[1].first));
            this->nodes[this->topo_translater(i, j)].set_pos(to_build);
        }
    }
}


inline int Map2d::topo_translater(int i, int j) {
    return i * this->side_len + j;
}

int Map2d::get_side_len() const {
    return this->side_len;
}