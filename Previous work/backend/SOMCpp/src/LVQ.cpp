#include "LVQ.hpp"

#include "Eigen/Dense"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::MatrixXd;
using Eigen::RowVectorXd;
using Eigen::VectorXd;
using namespace std;

LVQ::LVQ(int t_lim, int inp_dim, int total_class, double alpha, double l)
    : t_lim{t_lim}, inp_dim{inp_dim}, total_class{total_class}, node_num{0}, alpha{alpha}, l{l} {
    // Reconfigure variables in the case of default
    if (this->l == 0) {
        this->l = this->t_lim * 0.8;
    }
    // Create nodes
    for (int i = 0; i < total_class; i++){
        this->nodes.emplace_back(i, this->new_node());
    }
}

void LVQ::train(vector<pair<int, VectorXd>>& datas) {
    this->node_initialisation(datas);
    for (int t = 0; t < this->t_lim; t++){
        vector<VectorXd> to_changes(this->node_num, VectorXd::Zero(this->inp_dim));
        vector<int> nums(this->node_num);
        double cur_learning_rate = this->learning_rate(t);
        assert(cur_learning_rate >= 0);
        for (pair<int, VectorXd>& data : datas) {
            pair<int, Node>& bmu = this->find_bmu(data.second);
            VectorXd to_change = data.second - bmu.second.get_pos();
            to_change *= cur_learning_rate;
            // Move in opposite direction if they are different classes
            if(bmu.first != data.first){
                to_change *= -1;
            }
            nums[bmu.second.get_id()]++;
            assert(!isnan(to_change.array()).any());
            to_changes[bmu.second.get_id()] += to_change;
        }
        for (pair<int, Node>& node : this->nodes) {
            // Avoid division by zero errors
            if (nums[node.second.get_id()] != 0) {
                node.second.add_pos(to_changes[node.second.get_id()] / nums[node.second.get_id()]);
                assert(!isnan(node.second.get_pos().array()).any());
            }
        }
    }
}

void LVQ::node_initialisation(vector<pair<int, VectorXd>>& datas){
    vector<int> nums(this->total_class);
    vector<VectorXd> averages(this->total_class, VectorXd::Zero(this->inp_dim));
    // Sum the location of each class, so an average can be derived
    // Awkward average for numerical stability
    for (pair<int, VectorXd>& data : datas) {
        averages[data.first] = averages[data.first] * (1.0 * nums[data.first] / (nums[data.first] + 1))
                               + data.second / (nums[data.first] + 1);
        nums[data.first]++;
    }
    for (int i = 0; i < this->total_class; i++){
        this->nodes[i].second.set_pos(averages[i]);
    }
}

int LVQ::test(const VectorXd& to_test) {
    // LVQ test defined as the class of the closest neighbor
    return this->find_bmu(to_test).first;
}

double LVQ::distance_sqr(const VectorXd& v1, const VectorXd& v2) {
    return (v1 - v2).squaredNorm();
}

Node LVQ::new_node(const VectorXd& init_pos) {
    // Topological coordinates initialised to (0, 0) as it is not used
    return Node(Eigen::Vector2d(0, 0), this->node_num++, init_pos);
}

double LVQ::learning_rate(int t) {
    return 1.0 * this->alpha * exp(1.0 * -t / this->l);
}

pair<int, Node>& LVQ::find_bmu(const VectorXd& inp_vec) {
    return *min_element(this->nodes.begin(), this->nodes.end(), [&inp_vec, this](const pair<int, Node>& l, const pair<int, Node>& r) {
        return this->distance_sqr(l.second.get_pos(), inp_vec) < this->distance_sqr(r.second.get_pos(), inp_vec);
    });
}