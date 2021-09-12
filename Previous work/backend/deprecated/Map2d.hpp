#pragma once

#include <vector>

#include "Eigen/Dense"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::VectorXd;
using namespace std;

/** @brief Implementation of SOM in 2D.
 * 
 * Basic square 2D SOM with a given side length.
 * SOM training parameters are specified in initialisation (constructor).
 */
class Map2d : public SOM {
   public:

    /** @brief 2D SOM constructor.
     * 
     * @param t_lim Number of training iterations.
     * @param inp_dim Dimensionality (number of attributes) of dataset.
     * @param side_len Side length of the SOM.
     * @param sigma Starting radius of neighborhood.
     * @param l Lambda: Time constant for learning rate and neighbor radius.
     * @param alpha Initial learning rate.
     */
    Map2d(int t_lim, int inp_dim, int side_len, int sigma, double l, double alpha);
    
    
    /** @brief See SOM::get_nodes
     */
    vector<Node>& get_nodes() override;
       
    /** @brief See SOM::neighbor_multiplier
     */
    double neighbor_multiplier(Node& best, Node& n2, int t) override;

    /** @brief See SOM::neighbor_multiplier
     */
    double learning_rate(int t) override;

    /** @brief SOM::neighbor_size
     */
    double neighbor_size(int t) override;

    /** @brief See SOM::node_initialisation
     */
    void node_initialisation(vector<VectorXd>& datas) override;

    /** @brief Return the square SOM's side length (number of Nodes).
     * 
     * @return Integer representing side length of SOM.
     */
    int get_side_len() const;

   private:
    vector<Node> nodes;
    int side_len;
    int sigma;
    double l;
    double alpha;
    inline int topo_translater(int i, int j);
};