#pragma once

#include "Eigen/Dense"
#include "Node.hpp"

const double epsilon = 0.005;

using Eigen::VectorXd;

VectorXd plane_normal(VectorXd& v1, VectorXd& v2, VectorXd& v3);

double torsion(Node& center);