#pragma once

#include <vector>

#include "Eigen/Dense"

using Eigen::VectorXd;
using namespace std;



/** @brief Class for SOM nodes.
 * 
 * SOM node class supporting topological coordinates and feature space coordinates. 
 * The node's neighbors are decided based on the topology of the SOM.
 * The feature space coordinate matches the dimensionality of the input vectors.
 */
class Node {
    
   public:
   
    /** @brief Node constructor.
     * 
     * @param topo_coord Topology coordinate of node in SOM.
     * @param id_v Unique node id number starting from 0 for a given SOM.
     * @param init_pos Initial position of node in feature space.
     */
    Node(const VectorXd& topo_coord, int id_v, const VectorXd& init_pos);

    /** @brief Adds a neighbor for node.
     * 
     * @param neighbor The neighbor node to be added.
     */
    void add_neighbor(Node* neighbor);

    /** @brief Sums a vector to current node position.
     * 
     * @param delta The vector to be added to position.
     */
    void add_pos(const VectorXd& delta);
    
    /** @brief Sets node position.
     * 
     * @param loc The vector to set node position to.
     */
    void set_pos(const VectorXd& loc);

    /** @brief Multiplies node position by a scaler.
     * 
     * @param scalar The scaler to multiply the node position by.
     */
    void mul_pos(double scalar);

    /** @brief Returns position of the node.
     * 
     * @return Position vector of the node.
     */
    const VectorXd& get_pos() const;

    /** @brief Returns topology coordinate of the node.
     * 
     * @return Topology coordinate vector of the node.
     */
    const VectorXd& get_topo() const;
    
    /** @brief Returns id of the node.
     * 
     * @return Id of the node.
     */
    const int get_id() const;
    
    /** @brief Returns refeerence to neighbors of the node.
     * 
     * @return Node* vector of neighbors of the node.
     */
    const vector<Node*>& get_neighbors() const;

   private:
    /** @brief Topology coordinate position of node in SOM.
     */
    VectorXd topo_coord;

    /** @brief Position of node in feature space.
     */
    VectorXd position;

    /** @brief Unique node identifier.
     */
    int id_v;

    /** @brief List of neighbors.
     */
    vector<Node*> neighbors;
};
