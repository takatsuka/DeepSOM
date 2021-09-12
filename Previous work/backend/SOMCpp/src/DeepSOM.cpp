#include "DeepSOM.hpp"

#include <deque>
#include <functional>
#include <memory>
#include <queue>
#include <type_traits>
#include <vector>
#include <stack>
#include <iostream>
#include "Eigen/Dense"
#include "Map2d.hpp"
#include "MapHex.hpp"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::MatrixXd;
using Eigen::RowVectorXd;
using Eigen::VectorXd;
using namespace std;

DeepSOM::DeepSOM(int t_lim)
    : node_num{0}, t_lim{t_lim} {
}

void DeepSOM::ts_dfs(int cur, vector<bool>& visited, vector<int>& ans) {
    visited[cur] = 1;
    for (int neigh : this->nodes[cur].to) {
        if (!visited[neigh])
            this->ts_dfs(neigh, visited, ans);
    }
    ans.push_back(cur);
}

vector<int> DeepSOM::topological_sort() {
    vector<bool> visited(this->node_num, false);
    vector<int> ans;
    ans.reserve(this->node_num);
    for (int i = 0; i < this->node_num; ++i) {
        if (!visited[i])
            this->ts_dfs(i, visited, ans);
    }
    reverse(ans.begin(), ans.end());
    return ans;
}

void DeepSOM::batch_train(vector<VectorXd>& datas, function<void(DeepSOM& deep_som, int t)> post_cb) {
    // Obtain order of node traversal so that dependencies are resolved
    vector<int> order = this->topological_sort();
    for (int t = 0; t < this->t_lim; t++) {
        for(int node : order){
            // Train each node in order
            this->nodes[node].batch_iter(datas, t);
        }
        post_cb(*this, t);
    }
}

void DeepSOM::batch_train_block(vector<VectorXd>& datas, function<void(DeepSOM& deep_som, int t)> post_cb) {
    // Obtain order of node traversal so that dependencies are resolved
    vector<int> order = this->topological_sort();
    for (int i = 0; i < (int)order.size(); i++) {
        // Train each node in order
        this->nodes[order[i]].batch_block(datas);
        post_cb(*this, i);
    }
}

VectorXd DeepSOM::test(VectorXd& to_test, function<VectorXd(SOM&, VectorXd&)> get_output) {
    // Input data used to calculate how the to_test changes to be the input of the given node
    vector<VectorXd> input_data(this->node_num);
    // Obtain order of node traversal so that dependencies are resolved
    vector<int> order = this->topological_sort();
    for(int node : order){
        DeepSOM::Node& cur_node = this->nodes[node];
        if (cur_node.froms.size() == 0) {
            // The case of leaf nodes
            input_data[cur_node.id_v] = cur_node.get_data(to_test);
        } else {
            // The case of inner nodes
            vector<VectorXd> from_outs;
            from_outs.reserve(cur_node.froms.size());
            for (int from : cur_node.froms) {
                from_outs.emplace_back(cur_node.get_output(*cur_node.nodes[from].som, input_data[cur_node.nodes[from].id_v]));
            }
            input_data[cur_node.id_v] = cur_node.combine(from_outs);
        }
    }
    // Root is assumed to be the last in the order
    int root = order.back();
    // Tranform the input of the root to the output
    return get_output(*this->nodes[root].som, input_data[root]);
}

vector<VectorXd> DeepSOM::test_inputs(VectorXd& to_test) {
    // Input data used to calculate how the to_test changes to be the input of the given node
    vector<VectorXd> input_data(this->node_num);
    // Obtain order of node traversal so that dependencies are resolved
    vector<int> order = this->topological_sort();
    for(int node : order){
        DeepSOM::Node& cur_node = this->nodes[node];
        if (cur_node.froms.size() == 0) {
            // The case of leaf nodes
            input_data[cur_node.id_v] = cur_node.get_data(to_test);
        } else {
            // The case of inner nodes
            vector<VectorXd> from_outs;
            from_outs.reserve(cur_node.froms.size());
            for (int from : cur_node.froms) {
                from_outs.emplace_back(cur_node.get_output(*cur_node.nodes[from].som, input_data[cur_node.nodes[from].id_v]));
            }
            input_data[cur_node.id_v] = cur_node.combine(from_outs);
        }
    }
    return input_data;
}

int DeepSOM::add_SOM(SOM* som){
    this->nodes.emplace_back(this->node_num,
                             this->nodes,
                             unique_ptr<SOM>(som));
    return node_num++;
}

void DeepSOM::add_link(int from, int to) {
    nodes[to].froms.push_back(from);
    nodes[from].to.push_back(to);
}

void DeepSOM::set_combine(int target, function<VectorXd(vector<VectorXd>&)> combine) {
    nodes[target].combine = combine;
}

void DeepSOM::set_get_data(int target, function<VectorXd(VectorXd&)> get_data) {
    nodes[target].get_data = get_data;
}

void DeepSOM::set_get_output(int target, function<VectorXd(SOM&, VectorXd&)> get_output) {
    nodes[target].get_output = get_output;
}

void DeepSOM::set_train_cb(int target, function<void(SOM& som, int t)> train_cb){
    nodes[target].train_cb = train_cb;
}

SOM& DeepSOM::get_SOM(int target) const{
    return *this->nodes[target].som;
}

void DeepSOM::link_from_adj(vector<vector<int>>& adj){
    for (int i = 0; i < (int)adj.size(); i++){
        for(int to : adj[i]){
            this->add_link(i, to);
        }
    }
}

vector<vector<int>> DeepSOM::get_adj() const{
    vector<vector<int>> adj;
    for (int i = 0; i < this->node_num; i++){
        adj.push_back(this->nodes[i].to);
    }
    return adj;
}

int DeepSOM::get_root() const{
    // Another way to get root, which is simply the node with no to
    for (int i = 0; i < this->node_num; i++){
        if (this->nodes[i].to.size() == 0) {
            return i;
        }
    }
    return -1;
}

int DeepSOM::get_t_lim() const{
    return this->t_lim;
}

void DeepSOM::replace_som(int target, SOM* replace){
    this->nodes[target].som = unique_ptr<SOM>(replace);
}

int DeepSOM::get_node_num() const{
    return this->node_num;
}


DeepSOM::Node::Node(int id_v, vector<DeepSOM::Node>& nodes, unique_ptr<SOM> som)
    : nodes{nodes}, id_v{id_v}, som{move(som)} {
}

DeepSOM::Node::~Node() {
    this->som.reset();
}

void DeepSOM::Node::batch_iter(vector<VectorXd>& datas, int t) {
    // Clear previous data
    this->transformed_data.clear();
    this->transformed_data.reserve(datas.size());
    if (this->froms.size() == 0) {
        // The case of leaf nodes
        // Transform the data and cache it
        for (VectorXd& data : datas) {
            this->transformed_data.emplace_back(this->get_data(data));
        }
    } else {
        // The case of inner nodes
        for (int i = 0; i < (int)datas.size(); i++) {
            vector<VectorXd> from_outs;
            from_outs.reserve(this->froms.size());
            // Get output from all predecessors
            for (int from : this->froms) {
                from_outs.emplace_back(this->get_output(*this->nodes[from].som, this->nodes[from].transformed_data[i]));
            }
            // Merge predecessor data and cache it
            this->transformed_data.emplace_back(this->combine(from_outs));
        }
    }
    // Initialise nodes if required
    if (t == 0) {
        this->som->node_initialisation(this->transformed_data);
    }
    // Train one iteration of the current SOM based on the transformed input
    this->som->batch_train_iter(this->transformed_data, t);
    // Callback if present
    if(this->train_cb){
        this->train_cb(*this->som, t);
    }
}

void DeepSOM::Node::batch_block(vector<VectorXd>& datas) {
    // Clear previous data
    this->transformed_data.clear();
    this->transformed_data.reserve(datas.size());
    // Initialise data
    if (this->froms.size() == 0) {
        // Transform the data and cache it
        for (VectorXd& data : datas) {
            this->transformed_data.emplace_back(this->get_data(data));
        }
    } else {
        for (int i = 0; i < (int)datas.size(); i++) {
            vector<VectorXd> from_outs;
            from_outs.reserve(this->froms.size());
            // Get output from all predecessors
            for (int from : this->froms) {
                from_outs.emplace_back(this->get_output(*this->nodes[from].som, this->nodes[from].transformed_data[i]));
            }
            // Merge predecessor data and cache it
            this->transformed_data.emplace_back(this->combine(from_outs));
        }
    }
    if(this->train_cb){
        this->som->batch_train(this->transformed_data, this->train_cb);
    }else{
        this->som->batch_train(this->transformed_data);
    }
    
}