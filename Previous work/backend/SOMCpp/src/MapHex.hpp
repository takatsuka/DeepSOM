#pragma once

#include <vector>

#include "Eigen/Dense"
#include "Map2d.hpp"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::VectorXd;
using namespace std;

/** @brief Concrete SOM with 2d hex connectivity.
 * 
 * This is a concrete SOM class that implements all necessary functions required.
 * It inherits off the Map2d class, which implements the majority of the functions.
 * This class serves to define the hex based connection between nodes.
 */
class MapHex : public Map2d {
   public:
    /** Class Sets values necessary for the training step and set up grid based connections.
     * Lengths is based on the standard offset coordinates for hex grids.
     * 
     * For full explanation, see Map2d::Map2d.
     */
    MapHex(int t_lim, int inp_dim, vector<int> lengths, int sigma = 0, double l = 0, double alpha = 0.5);

   private:
    /** @brief Given the position of the a node in the hex grid, calculate its topological coordinates.
     * 
     * Given the position of the a node in the hex grid, calculate its topological coordinates.
     * 
     * @param col_i the column index of the node.
     * @param row_i the row index of the node.
     */
    VectorXd topo_coord_calc(int col_i, int row_i);
};