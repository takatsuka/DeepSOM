#pragma once

#include <vector>

#include "Eigen/Dense"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::VectorXd;
using namespace std;

/** @brief Implementation of SOM in 2D.
 * 
 * Basic 2D SOM with a given side length.
 * SOM training parameters are specified in initialisation.
 * Node position and initialisation is not defined
 * Node initialisation performed based on PCA on input data.
 */
class Map2d : public SOM {
   public:
    /** @brief 2D SOM constructor.
     * 
     * @param t_lim Number of training iterations.
     * @param inp_dim Dimensionality (number of attributes) of dataset.
     * @param lengths Side lengths of the SOM. Will automatically be sorted, and the number of rows will have the larger length.
     * @param sigma Starting radius of neighborhood. 0 results in 0.8 * max(lenghts).
     * @param l Lambda: Time constant for learning rate and neighbor radius.
     *          0 results in 0.8 * t_lim.
     * @param alpha Initial learning rate.
     */
    Map2d(int t_lim, int inp_dim, vector<int> lengths, int sigma = 0, double l = 0, double alpha = 0.2);

    /** @brief Virtual destructor.
     */
    virtual ~Map2d(){};

    /** @brief See SOM::get_nodes.
     */
    vector<Node>& get_nodes() override;

    /** @brief See SOM::get_nodes.
     */
    const vector<Node>& get_nodes() const override;

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

    /** @brief Return the SOM's side length (number of Nodes).
     * 
     * @return Integer representing side length of SOM.
     */
    const vector<int>& get_lengths() const;

    /** @brief Return the SOM's sigma.
     * 
     * @return Integer representing sigma of SOM.
     */
    int get_sigma() const;

    /** @brief Return the SOM's l.
     * 
     * @return Integer representing l of SOM.
     */
    double get_l() const;

    /** @brief Return the SOM's alpha.
     * 
     * @return Integer representing alpha of SOM.
     */
    double get_alpha() const;


   protected:
    /** @brief Internal storage of the nodes. Stored in column major order.
     */
    vector<Node> nodes;

    /** @brief Internal storage of lengths.
     */
    vector<int> lengths;

    /** @brief Internal storage of sigma.
     */
    int sigma;

    /** @brief Internal storage of l.
     */
    double l;

    /** @brief Internal storage of alpha.
     */
    double alpha;

    /** @brief Obtains index of Map2d::nodes based on position in the grid.
     * 
     * Nodes are stored in column major order in Map2d::nodes, thus given a node's position
     * in a grid, it is possible to get its position in Map2d::nodes.
     * 
     * @param col_i the column index of the node.
     * @param row_i the row index of the node.
     * @return Index in Map2d::nodes.
     */
    int topo_translater(int col_i, int row_i);

    /** @brief Checks whether a node with the given coordinate exists.
     * 
     * Checks if the current nodes has been instantiated. 
     * The indices are checked to ensure they are greater than 0 and smaller than the corresponding side length.
     * 
     * @param col_i the column index of the node.
     * @param row_i the row index of the node.
     * @return Whether it is valid or not.
     */
    bool check_coord_valid(int col_i, int row_i);
};