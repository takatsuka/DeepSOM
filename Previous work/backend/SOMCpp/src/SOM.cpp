#include "SOM.hpp"

#include <assert.h>

#include <algorithm>
#include <iostream>
#include <limits>
#include <queue>
#include <random>
#include <vector>

#include "Eigen/Dense"
#include "Node.hpp"

using Eigen::isnan;
using Eigen::VectorXd;
using namespace std;

SOM::SOM(int t_lim, int inp_dim)
    : t_lim{t_lim}, inp_dim{inp_dim}, node_num{0} {
}

vector<Node*> SOM::neighbors(Node& best, int t) {
    int radius = this->neighbor_size(t);
    // Maximum number of neighbors based on a slanted square
    int max_num = 2 * radius * radius + 2 * radius + 1; 
    // Simple BFS
    vector<Node*> result;
    result.reserve(max_num);
    queue<Node*> q;
    vector<bool> traversed(this->node_num);
    int depth = 1;
    int current_num = 1;
    result.push_back(&best);
    traversed[best.get_id()] = 1;
    // Avoid erroneous push when no push is needed
    if (radius != 0) {
        q.push(&best);
    }

    Node* cur;
    bool to_set;
    while (q.size() != 0) {
        cur = q.front();
        q.pop();
        current_num -= 1;
        to_set = current_num == 0;

        for (Node* neighbor : cur->get_neighbors()) {
            if (!traversed[neighbor->get_id()]) {
                if (depth < radius) {
                    q.push(neighbor);
                }
                result.push_back(neighbor);
                traversed[neighbor->get_id()] = 1;
            }
        }
        // Detect if it is last in the current layer
        if (to_set) {
            current_num = q.size();
            depth += 1;
        }
    }
    return result;
}

double SOM::distance_sqr(const VectorXd& v1, const VectorXd& v2) {
    // Return squared Euclidean distance between two vectors
    return (v1 - v2).squaredNorm();
}

void SOM::stochastic_train(vector<VectorXd>& datas, int batch_size) {
    // Train SOM by randomly sampling input vectors in bactches
    // Note: Weights are updated at the end of each batch
    this->node_initialisation(datas);
    vector<int> indices(datas.size());
    iota(indices.begin(), indices.end(), 0);
    vector<int> desired_indices(batch_size);
    // Note: t represents number of batches, not number of input vectors
    for (int t = 0; t < this->t_lim; t++) {  // Training loop
        vector<VectorXd> to_changes(this->node_num, VectorXd::Zero(this->inp_dim));
        vector<int> nums(this->node_num);
        // Randomly select batch_size input vectors and store in desired_indices
        sample(indices.begin(), indices.end(), desired_indices.begin(), batch_size, mt19937{random_device{}()});
        double cur_learning_rate = this->learning_rate(t);
        assert(cur_learning_rate >= 0);
        // Iterate over randomly sampled input vectors
        for (int index : desired_indices) {
            VectorXd data = datas[index];
            Node& bmu = this->find_bmu(data);
            for (Node* neighbor : this->neighbors(bmu, t)) {
                // Modify to_changes for each neighbor of the BMU, inclusive
                VectorXd to_change = data - neighbor->get_pos();  // Temporary
                double multiplier = cur_learning_rate * this->neighbor_multiplier(bmu, *neighbor, t);
                to_change *= multiplier;
                assert(!isnan(to_change.array()).any());
                to_changes[neighbor->get_id()] += to_change;  // Store update
                nums[neighbor->get_id()]++;
            }
        }
        for (Node& node : this->get_nodes()) {  // Update weights post-batch
            if (nums[node.get_id()] != 0) {
                node.add_pos(to_changes[node.get_id()] / nums[node.get_id()]);
                assert(!isnan(node.get_pos().array()).any());
            }
        }
    }
}

void SOM::batch_train(vector<VectorXd>& datas, function<void(SOM& som, int t)> post_cb) {
    this->node_initialisation(datas);
    for (int t = 0; this->batch_train_iter(datas, t); t++) {
        post_cb(*this, t);
    }
}

bool SOM::batch_train_iter(vector<VectorXd>& datas, int t) {
    if (t >= this->t_lim) {
        return false;
    }
    vector<VectorXd> to_changes(this->node_num, VectorXd::Zero(this->inp_dim));
    vector<int> nums(this->node_num);
    double cur_learning_rate = this->learning_rate(t);
    assert(cur_learning_rate >= 0);
    for (VectorXd& data : datas) {  // Iterate over all input vectors
        Node& bmu = this->find_bmu(data);
        for (Node* neighbor : this->neighbors(bmu, t)) {
            // Modify to_changes for each neighbor of the BMU, inclusive
            VectorXd to_change = data - neighbor->get_pos();  // Temporary
            double multiplier = cur_learning_rate * this->neighbor_multiplier(bmu, *neighbor, t);
            to_change *= multiplier;
            assert(!isnan(to_change.array()).any());
            to_changes[neighbor->get_id()] += to_change;  // Store update
            nums[neighbor->get_id()]++;
        }
    }
    for (Node& node : this->get_nodes()) {  // Update all nodes
        // avoid division by 0
        if (nums[node.get_id()] != 0) {
            node.add_pos(to_changes[node.get_id()] / nums[node.get_id()]);
            assert(!isnan(node.get_pos().array()).any());
        }
    }
    t++;
    return true;
}

Node SOM::new_node(const VectorXd& topo_coord, const VectorXd& init_pos) {
    return Node(topo_coord, this->node_num++, init_pos);
}

Node& SOM::find_bmu(const VectorXd& inp_vec) {
    return *min_element(this->get_nodes().begin(), this->get_nodes().end(), [&inp_vec, this](const Node& l, const Node& r) {
        return this->distance_sqr(l.get_pos(), inp_vec) < this->distance_sqr(r.get_pos(), inp_vec);
    });
}

vector<Node*> SOM::find_bmu_k(const VectorXd& inp_vec, int k) {
    eigen_assert(k <= this->node_num && k >= 0);
    auto comparator = [&inp_vec, this](const Node* l, const Node* r) {
        // Greater than is used as C++ uses a max heap
        return this->distance_sqr(l->get_pos(), inp_vec) > this->distance_sqr(r->get_pos(), inp_vec);
    };

    vector<Node*> store;
    store.reserve(this->node_num);
    // Get addresses of nodes
    transform(this->get_nodes().begin(), this->get_nodes().end(), back_inserter(store), [](Node& n) -> Node* { return &n; });
    // Creates heap based on array
    make_heap(store.begin(), store.end(), comparator);
    // End of the array stores the smallest element
    for (int i = 0; i < k; i++) {
        pop_heap(store.begin(), store.end() - i, comparator);
    }
    reverse(store.begin(), store.end());
    store.resize(k);
    return store;
}

int SOM::get_t_lim() const{
    return this->t_lim;
}

int SOM::get_inp_dim() const{
    return this->inp_dim;
}

int SOM::get_node_num() const{
    return this->node_num;
}