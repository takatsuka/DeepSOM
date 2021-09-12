#pragma once

#include <vector>

#include "Eigen/Dense"
#include "Node.hpp"

using Eigen::VectorXd;
using namespace std;

/** @brief Abstract SOM Class.
 * 
 * This abstract SOM class implements basic SOM training, BMU and distance functions.
 * It is inherited by SOM implementations, such as Map2d.
 * Classes inheriting from this must define their own topology of node linkage as a node's neighbors.
 * They must also define learning rate, a neighborhood function and node initialisation. 
 */
class SOM {
   public:
    friend class DeepSOM;

    /** Abstract SOM class constructor. Sets values necessary for the training step.
     * 
     * @param t_lim Maximum number of iterations from training.
     * @param inp_dim Dimensions of the input data.
     */
    SOM(int t_lim, int inp_dim);

    /** @brief Abstract SOM class destructor.
     */
    virtual ~SOM(){};

    /** @brief Move constructor deleted to avoid memory issues.
     */
    SOM(SOM&&) = delete;

    /** @brief Gets all nodes within the SOM.
     * 
     * Returns a vector of all nodes present in the SOM. Changes to the nodes will be reflected.
     * 
     * Remains virtual, to be implemented by child class.
     * 
     * @return Reference to vector of Nodes within the SOM.
     */
    virtual vector<Node>& get_nodes() = 0;

    /** @brief Gets all nodes within the SOM.
     * 
     * Returns a vector of all nodes present in the SOM. Changes to the nodes will be reflected.
     * 
     * Remains virtual, to be implemented by child class.
     * 
     * @return Reference to vector of Nodes within the SOM.
     */
    virtual const vector<Node>& get_nodes() const = 0;

    /** @brief Gets neighboring nodes for a given Node.
     * 
     * For a given node, uses BFS to search for all nodes within the current neighborhood radius. 
     * Neighborhood radius is calculated based on the current iteration t.
     * 
     * @param best Node of interest.
     * @param t Current iteration number
     * @return Vector of neighboring Node*.
     */
    vector<Node*> neighbors(Node& best, int t);

    /** @brief Returns effect of the node's position relative to the BMU on learning rate.
     * 
     * This multiplier is used to update a neighbor's feature-space position for given Node.
     * Distance multiplier is a function of the two nodes and the current iteration number.
     * 
     * Remains virtual, to be implemented by child class.
     * 
     * @param best BMU.
     * @param n2 Node of interest.
     * @param t Current iteration number

     * @return Multiplier for learning rate.
     */
    virtual double neighbor_multiplier(Node& best, Node& n2, int t) = 0;

    /** @brief Returns learning rate.
     * 
     * Learning rate is a global multiplier for the amount of distance a Node is updated by.
     * It decreases over time.
     * 
     * Remains virtual, to be implemented by child class.
     * 
     * @param t Current iteration number.
     * @return Learning rate.
     */
    virtual double learning_rate(int t) = 0;

    /** @brief Returns neighborhood radius.
     * 
     * Used in neighbor distance multiplier computation and neighbor multipler.
     * 
     * Remains virtual, to be implemented by child class.
     * 
     * @param t Current iteration number.
     * @return Neighborhood radius
     */
    virtual double neighbor_size(int t) = 0;

    /** @brief Compute Square of Euclidean distance between two vectors.
     * 
     * @param v1 First vector.
     * @param v2 Second vector.
     * @return Square of Euclidean distance between v1 and v2.
     */
    double distance_sqr(const VectorXd& v1, const VectorXd& v2);

    /** @brief Train SOM on the given dataset in batches.
     * 
     * A variant of the standard SOM training algorithm where a randomly selected batch 
     * of input vectors are trained on before updating weights of all required nodes. 
     * Batch size can be set to 1 to simulate the basic SOM training algorithm.
     * 
     * @param datas Complete training dataset vector.
     * @param batch_size Size of batches to train in.
     */
    void stochastic_train(vector<VectorXd>& datas, int batch_size);

    /** @brief Train SOM on the given dataset in batches.
     * 
     * A variant of the standard SOM training algorithm where all input vectors are trained on
     * before updating weights of all nodes. 
     * 
     * @param datas Complete training dataset vector for batch train.
     * @param post_cb Optional callback after each iteration.
     */
    void batch_train(vector<VectorXd>& datas, function<void(SOM& som, int t)> post_cb = [](SOM& som, int t){});

    /** @brief Create a Node object with give topological coordinates and feature space position.
     * 
     * @param topo_coord Topological coordiante to be set for new node.
     * @param init_pos Initial node position within the feature space.
     * @return New Node object.
     */
    Node new_node(const VectorXd& topo_coord, const VectorXd& init_pos = VectorXd{});

    /** @brief Method returning closest node to input vector by Euclidean distance (best matching unit, BMU).
     * 
     * @param inp_vec Vector for which BMU should be found.
     * @return Reference to Node that is the best matching unit.
     */
    Node& find_bmu(const VectorXd& inp_vec);

    /** @brief Returns the k closest nodes.
     * 
     * Returns the k closest nodes relative to a vector of interest.
     * Has a runtime of O(n), no matter k.
     * 
     * @param inp_vec Vector for which BMU should be found.
     * @param k K.
     * @return List of Nod* that represent the k closest nodes.
     */
    vector<Node*> find_bmu_k(const VectorXd& inp_vec, int k);

    /** @brief Return the SOM's number of training iterations.
     * 
     * @return Integer representing number of training iterations of SOM.
     */
    int get_t_lim() const;

    /** @brief Return the SOM's input dimensions.
     * 
     * @return Integer representing input dimensions of SOM.
     */
    int get_inp_dim() const;

    /** @brief Return the SOM's number of nodes.
     * 
     * @return Integer representing number of nodes of SOM.
     */
    int get_node_num() const;

   protected:

    /** @brief Number of training iterations.
     */
    int t_lim;
    
    /** @brief Input dimension, number of attributes for dataset.
     */
    int inp_dim;

    /** @brief Count of nodes in SOM, used for Node id.
     */
    int node_num;

    /** @brief Initialises feature space posiitons of all nodes.
     * 
     * Initialise feature space posiitons of all nodes.
     * 
     * Remains virtual, to be implemented by child class.
     * 
     * @param datas Node positions are initialised according to this.
     */
    virtual void node_initialisation(vector<VectorXd>& datas) = 0;

    /** @brief Train SOM in a batch for 1 iterations.
     * 
     * A variant of the standard SOM training algorithm where all input vectors are trained on
     * before updating weights of all nodes. Training is only performed for 1 iteartions. If
     * the current iteration exceeds the limit defined in SOM::SOM(), false is returned.
     * 
     * @param datas Complete training dataset vector for batch train.
     * @param t Current iteration number.
     * @return Whether training occured or not.
     */
    bool batch_train_iter(vector<VectorXd>& datas, int t);

};