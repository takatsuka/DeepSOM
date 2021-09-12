#pragma once

#include <vector>

#include "Eigen/Dense"
#include "Map2d.hpp"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::VectorXd;
using namespace std;


/** @brief Concrete SOM with 2d grid connectivity.
 * 
 * This is a concrete SOM class that implements all necessary functions required.
 * It inherits off the Map2d class, which implements the majority of the functions.
 * This class serves to define the grid based connection between nodes.
 */
class MapRect : public Map2d {
   public:
    // friend void pybind11_init_SOMCpp(pybind11::module &);
    /** Class Sets values necessary for the training step and set up grid based connections.
     * 
     * For full explanation, see Map2d::Map2d.
     */
    MapRect(int t_lim, int inp_dim, vector<int> lengths, int sigma = 0, double l = 0, double alpha = 0.5);
};