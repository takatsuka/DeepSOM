#include "Evaluation.hpp"

#include <math.h>

#include <functional>
#include <vector>

#include "Eigen/Dense"
#include "Node.hpp"

using Eigen::VectorXd;

VectorXd plane_normal(VectorXd& v1, VectorXd& v2, VectorXd& v3) {
    VectorXd w1 = (v2 - v1).normalized();
    VectorXd w2 = (w1.dot(v2) / v2.squaredNorm()) * v2;
    VectorXd w3 = (w2.dot(v3) / v3.squaredNorm()) * v3;
    return (w1 - w2 - w3).normalized();
}

double torsion(Node& center) {
    function<bool(Node*, Node*)> sorter = [center](Node* Node_1, Node* Node_2) -> bool {
        VectorXd pos_1 = (Node_1->get_topo() - center.get_topo()).array() + epsilon;
        VectorXd pos_2 = (Node_2->get_topo() - center.get_topo()).array() + epsilon;
        double x_1 = pos_1[0];
        double y_1 = pos_1[1];
        double x_2 = pos_2[0];
        double y_2 = pos_2[1];
        if (y_1 * y_2 < 0) {
            if (y_1 > 0) {
                return true;
            }
            return false;
        }
        if (y_1 * (x_2 - x_1) > 0) {
            return true;
        }
        return false;
    };
    vector<Node*> neighbors = center.get_neighbors();
    int n = neighbors.size();

    sort(neighbors.begin(), neighbors.end(), sorter);
    vector<VectorXd> spindles;
    spindles.reserve(n);
    for (int i = 0; i < n; i++) {
        spindles.push_back(neighbors[i]->get_pos() - center.get_pos());
    }
    double t = 0;
    for (int i = 0; i < n - 1; i++) {
        t += abs(spindles[i].dot(spindles[i + 1]));
    }
    t += abs(spindles[n - 1].dot(spindles[0]));
    return t / n;
}

// double torsion(Node& center) {
//     function<bool(Node&, Node&)> sorter = [center](Node& Node_1, Node& Node_2) -> bool {
//         VectorXd pos_1 = Node_1.get_topo() - center.get_topo() + epsilon;
//         VectorXd pos_2 = Node_2.get_topo() - center.get_topo() + epsilon;
//         double x_1 = pos_1[0];
//         double y_1 = pos_1[1];
//         double x_2 = pos_2[0];
//         double y_2 = pos_2[1];
//         if (y_1 * y_2 < 0) {
//             if (y_1 > 0) {
//                 return true;
//             }
//             return false;
//         }
//         if (y_1 * (x_2 - x_1) > 0) {
//             return true;
//         }
//         return false;
//     };

//     vector<Node*> neighbors = center.get_neighbors();
//     int n = neighbors.size();

//     sort(neighbors.begin(), neighbors.end(), sorter);
//     vector<VectorXd> normals;
//     normals.reserve(n);
//     for (int i = 0; i < n - 1; i++) {
//         normals.push_back(plane_normal(center.get_pos(), neighbors[i].get_pos(), neighbors[i + 1].get_pos()));
//     }
//     normals.push_back(plane_normal(center.get_pos(), neighbors[n - 1].get_pos(), neighbors[0].get_pos()));
//     double t = 0;
//     for (int i = 0; i < n - 1; i++) {
//         t += abs(normals[i].dot(normals[i + 1]));
//     }
//     t += abs(normals[n - 1].dot(normals[0]));
//     t = t / n;
//     return 1 / (1 + t);
// }
