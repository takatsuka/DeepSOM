#include "Map2d.hpp"

#include <time.h>

#include <queue>
#include <random>
#include <set>
#include <vector>
#include <limits>
#include <iostream>

#include "Eigen/Dense"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::MatrixXd;
using Eigen::RowVectorXd;
using Eigen::VectorXd;
using namespace std;

Map2d::Map2d(int t_lim, int inp_dim, vector<int> lengths, int sigma, double l, double alpha)
    : SOM{t_lim, inp_dim}, lengths{lengths}, sigma{sigma}, l{l}, alpha{alpha} {
    // Lengths refers to the dimensions of the SOM
    // Sorted such that the longer lengths are first
    sort(this->lengths.begin(), this->lengths.end(), greater<int>());
    // Reconfigure variables in the case of default
    if (this->sigma == 0) {
        // Initial neighborhood radius in terms of SOM side length
        this->sigma = max(this->lengths[0] * 0.8, 2.0); 
    }
    if (this->l == 0) {
        // Time constant for learning rate and neighborhood decay
        // Higher values lead to slower decay
        this->l = this->t_lim * 0.8;
    }
}

vector<Node>& Map2d::get_nodes() {
    return this->nodes;
}

const vector<Node>& Map2d::get_nodes() const{
    return this->nodes;
}

double Map2d::neighbor_multiplier(Node& best, Node& n2, int t) {
    // Multiplier for magnitude of node position update based on t
    // See plot for details: https://www.desmos.com/calculator/1jl22m61bi
    double dist_sqr = this->distance_sqr(best.get_pos(), n2.get_pos());
    double dist_mult = exp((-1.0 * dist_sqr) / (2 * pow(this->neighbor_size(t), 2)));
    // Exponential decay function 
    // Avoid multiplying by negliglible values
    if (dist_mult < 0.001) {
        return 0;  
    } else {
        return dist_mult;
    }
}

double Map2d::learning_rate(int t) {
    // Learning rate as an exponetial decay function of time
    // See plot for details: https://www.desmos.com/calculator/dakanafh0m
    return 1.0 * this->alpha * exp(1.0 * -t / this->l);
}

double Map2d::neighbor_size(int t) {
    // Radius of neighborhood from best matching unit based on t
    return 1.0 * this->sigma * exp(1.0 * -t / this->l);
}

void Map2d::node_initialisation(vector<VectorXd>& datas) {
    if (this->inp_dim == -1){
        this->inp_dim = datas[0].size();
    }
    // Initialise the position of SOM nodes in the feature space
    // Nodes are initialised based on the first two components of PCA
    // Nodes are then evenly distributed within the space according to their coordinates    
    int n = datas.size();
    int m = this->inp_dim;
    MatrixXd matrix_datas(n, m);
    // Store dataset as a Eigen matrix
    for (int i = 0; i < n; i++) {
        matrix_datas.row(i) = datas[i];
    }
    RowVectorXd centroid = matrix_datas.colwise().mean();
    MatrixXd centered = matrix_datas.rowwise() - centroid;
    // Calculate covariance matrix
    MatrixXd cov_var = (centered.adjoint() * centered).array() / (centered.rows() - 1);
    // Obtained eigen vector and value for covariance
    Eigen::SelfAdjointEigenSolver<MatrixXd> eig_solver(cov_var);
    // The eigen vectors in PCA define the change of basis from the original feature space to the PCA space.
    // Concretely, this is the weighting of each original dataset attribute that contributes to each component.
    MatrixXd eig_vec = eig_solver.eigenvectors();
    // The eigen values in PCA is the variance of the original data explained by the component.
    // The most significant, component has the highest such value, the second has the second highest, and so on.
    VectorXd eig_val = eig_solver.eigenvalues();
    // Indices for principal components (to find best two)
    vector<int> indices(m);
    // Fills indices with increasing values starting at 0
    iota(indices.begin(), indices.end(), 0);
    // Sort indices according to eigen values of principal components
    sort(indices.begin(), indices.end(), [&eig_val](int l, int r) {
        return eig_val[l] > eig_val[r];
    });
    // Stores the maximum and minimum coefficients of the selected PCA components
    vector<pair<double, double>> bounds;
    // Only the first 2 components are selected
    for (int i = 0; i < 2; i++) {
        // Transformation of original data by a principal component
        RowVectorXd dist = centered * eig_vec.col(indices[i]);
        bounds.emplace_back(dist.minCoeff(), dist.maxCoeff());
    }
    // Stores the minimum and maximum topological position of the Nodes
    vector<pair<double, double>> min_max;
    min_max.emplace_back(numeric_limits<double>::max(), numeric_limits<double>::min());
    min_max.emplace_back(numeric_limits<double>::max(), numeric_limits<double>::min());
    for (Node& node : this->get_nodes()){
        VectorXd topo = node.get_topo();
        min_max[0].first = min(min_max[0].first, topo(1));
        min_max[0].second = max(min_max[0].second, topo(1));
        min_max[1].first = min(min_max[1].first, topo(0));
        min_max[1].second = max(min_max[1].second, topo(0));
    }
    // Calculates the range of topological positions
    vector<double> ranges;
    ranges.push_back(min_max[0].second - min_max[0].first);
    ranges.push_back(min_max[1].second - min_max[1].first);
    for (Node& node : this->get_nodes()) {
        // Transform centroid to requires position
        VectorXd to_build = centroid.adjoint();
        VectorXd topo = node.get_topo();
        // Add a multiple of the principal components
        // Multiplier calculated based off location within the group of nodes
        to_build += eig_vec.col(indices[0]) * (bounds[0].first + (1.0 * (topo(1) / ranges[0]) * (bounds[0].second - bounds[0].first)));
        to_build += eig_vec.col(indices[1]) * (bounds[1].first + (1.0 * (topo(0) / ranges[1]) * (bounds[1].second - bounds[1].first)));
        node.set_pos(to_build);
    }
}

int Map2d::topo_translater(int col_i, int row_i) {
    // Stored in column major
    return col_i * this->lengths[0] + row_i;
}

const vector<int>& Map2d::get_lengths() const {
    return this->lengths;
}

bool Map2d::check_coord_valid(int col_i, int row_i){
    return col_i >= 0 && col_i < this->lengths[1] && row_i >= 0 && row_i < this->lengths[0];
}

int Map2d::get_sigma() const{
    return this->sigma;
}

double Map2d::get_l() const{
    return this->l;
}

double Map2d::get_alpha() const{
    return this->alpha;
}