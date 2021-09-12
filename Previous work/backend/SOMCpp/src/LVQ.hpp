#pragma once

#include <vector>

#include "Eigen/Dense"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::VectorXd;
using namespace std;

/** @brief Implementation of a LVQ classifier.
 * 
 * Given some input data and its corresponding classes, provides a classifier based
 * on LVQ. Classes are numerical and increments from 0. test and train methods are exposed.
 */
class LVQ {
   public:
    /** @brief LVQ constructor. 
     * 
     * Creates an LVQ. The number of nodes created is equal to the number of classes.
     * 
     * @param t_lim Number of training iterations.
     * @param inp_dim Dimensionality (number of attributes) of dataset.
     * @param total_class Total number of classes. 
     * @param alpha Initial learning rate.
     * @param l Lambda: Time constant for learning rate and neighbor radius.
     *          0 results in 0.8 * t_lim.
     */
    LVQ(int t_lim, int inp_dim, int total_class, double alpha = 0.5, double l = 0);

    /** @brief LVQ trainer.
     * 
     * Given some data, trains the LVQ. Note that the classes of the data must start from 0
     * and be less than the total number of classes. Node initialisation is also performed,
     * hence it is not recommended to run train multiple times.
     * 
     * @param datas The data to be provided. The first element of each observation is the class,
     * while the second is the coordinates.
     */
    void train(vector<pair<int, VectorXd>>& datas);

    /** @brief LVQ tester.
     * 
     * Given a data, returns the class.
     * 
     * @param to_test The data to be tested.
     * @return The predicted class of the vector.
     */
    int test(const VectorXd& to_test);

   private:
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
    double learning_rate(int t);

    /** @brief Create a Node object with give topological coordinates and feature space position.
     * 
     * @param init_pos Initial node position within the feature space.
     * @return New Node object.
     */
    Node new_node(const VectorXd& init_pos = VectorXd{});

    /** @brief Compute Square of Euclidean distance between two vectors.
     * 
     * @param v1 First vector.
     * @param v2 Second vector.
     * @return Square of Euclidean distance between v1 and v2.
     */
    double distance_sqr(const VectorXd& v1, const VectorXd& v2);

    /** @brief Initialises feature space posiitons of all nodes.
     * 
     * Initialise feature space posiitons of all nodes.
     * 
     * Remains virtual, to be implemented by child class.
     * 
     * @param datas Node positions are initialised according to this.
     */
    void node_initialisation(vector<pair<int, VectorXd>>& datas);

    /** @brief Method returning closest node to input vector by Euclidean distance (best matching unit, BMU).
     * 
     * @param inp_vec Vector for which BMU should be found.
     * @return Reference to Node that is the best matching unit.
     */
    pair<int, Node>& find_bmu(const VectorXd& inp_vec);

    /** @brief Internal storage of the nodes. First element is the class, second element is the node itself.
     */
    vector<pair<int, Node>> nodes;

    /** @brief Number of training iterations.
     */
    int t_lim;
    
    /** @brief Input dimension, number of attributes for dataset.
     */
    int inp_dim;

    /** @brief Number of classes.
     */
    int total_class;

    /** @brief Count of nodes in SOM, used for Node id.
     */
    int node_num;

    /** @brief Internal storage of alpha.
     */
    double alpha;

    /** @brief Internal storage of l.
     */
    double l;
};