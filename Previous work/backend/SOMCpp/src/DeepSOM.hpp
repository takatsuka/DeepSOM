#pragma once

#include <functional>
#include <memory>
#include <vector>

#include "Eigen/Dense"
#include "Map2d.hpp"
#include "MapHex.hpp"
#include "Node.hpp"
#include "SOM.hpp"

using Eigen::MatrixXd;
using Eigen::RowVectorXd;
using Eigen::VectorXd;
using namespace std;

/** @brief Implementation of a network of interconnected SOMs.
 * 
 *  A network of SOMs are created and trained. The SOMs must be organised as a directed acyclic graph.
 *  There should only be only 1 root SOM. The leaf SOMs take data from the input data, while inner SOMs take 
 *  data from the predecessor SOMs. 3 functions are defined:
 * 
 *  1. get_data: Used by leaf SOMs to manipulate the whole dataset to obtain the input used by that SOM
 *  2. get_output: Used by inner SOMs to obtain the output from predecessor SOMs.
 *  3. combine: Used by inner SOMS to combine the output obtained from predecessor SOMs.
 */
class DeepSOM {
   public:

    /** @brief DeepSOM constructor.
     * 
     * @param t_lim Number of training iterations.
     */
    DeepSOM(int t_lim);

    /** @brief Move constructor deleted to avoid memory issues.
     */
    DeepSOM(DeepSOM&&) = delete;

    /** @brief Train DeepSOM on the given dataset where each SOM is trained in batches.
     * 
     * SOM::batch_train is used to train each individual SOM. The entire network is trained iteration by iteartion,
     * i.e. 1 iteration on the leaf nodes, then 1 iteration on the inner nodes, etc. 
     * 
     * @param datas Complete training dataset vector.
     * @param post_cb Optional callback after each iteration.
     */
    void batch_train(vector<VectorXd>& datas, function<void(DeepSOM& deep_som, int t)> post_cb = [](DeepSOM& som, int t){});

    void batch_train_block(vector<VectorXd>& datas, function<void(DeepSOM& deep_som, int t)> post_cb = [](DeepSOM& som, int t){});

    /** @brief For a given vector, obtains the compressed output vector
     * 
     * As the there is no get_output targetting the root node, the function needs to be provided
     * 
     * @param to_test The input vector to be compressed.
     * @param get_output Way to obtain the result from the last node.
     * @return The compressed vector.
     */
    VectorXd test(VectorXd& to_test, function<VectorXd(SOM&, VectorXd&)> get_output);


    /** @brief For a given vector, obtains the input to each node
     * 
     * @param to_test The input vector to be compressed.
     * @return A list of vectors, representing the inputs.
     */
    vector<VectorXd> test_inputs(VectorXd& to_test);

    /** @brief Create a node in the network.
     * 
     * A new node is created in the network by passing in the parameters of the SOM object. The type
     * of the SOM must also be provided in the template arguments. This is done due to the lack of a
     * copy constructor and move constructor for the SOM. 
     * 
     * The create node is disconnected, and needs to be linked up later. A unique identifer of the node
     * is returned.
     * 
     * @param args The parameters of the SOM.
     * @return A unique identifier of the created node.
     */
    template <typename T, typename... Ts>
    int add_SOM(Ts&&... args);

    /** @brief Create a node in the network.
     * 
     * A new node is created in the network by passing in a heap-allocated SOM. The ownership of the SOM
     * is taken by a unique_ptr afterwards.
     * 
     * The create node is disconnected, and needs to be linked up later. A unique identifer of the node
     * is returned.
     * 
     * @param som The SOM.
     * @return A unique identifier of the created node.
     */
    int add_SOM(SOM* som);

    /** @brief Create a directed edge between 2 SOMs.
     * 
     * Creates a directed edge between 2 SOMs. The SOMs are identified by the identifiers that are returned
     * when the SOM is created. A edge from the first parameter is created to the second parameter.
     * 
     * @param from The edge's starting SOM.
     * @param to The edge's ending SOM.
     */
    void add_link(int from, int to);

    /** @brief Specifies the combine function for a given SOM.
     * 
     * Specified the combine function for a given SOM. The SOM is identified by the identifier that is returned
     * when the SOM is created. The combine function should take in a vector of VectorXd and return a single
     * VectorXd.
     * 
     * @param target The SOM.
     * @param combine The combine function.
     */
    void set_combine(int target, function<VectorXd(vector<VectorXd>&)> combine);

    /** @brief Specifies the get_data function for a given SOM.
     * 
     * Specified the get_data function for a given SOM. The SOM is identified by the identifier that is returned
     * when the SOM is created. The get_data function should take in a single VectorXd and return a single
     * VectorXd.
     * 
     * @param target The SOM.
     * @param get_data The get_data function.
     */
    void set_get_data(int target, function<VectorXd(VectorXd&)> get_data);

    /** @brief Specifies the get_output function for a given SOM.
     * 
     * Specified the get_output function for a given SOM. The SOM is identified by the identifier that is returned
     * when the SOM is created. The get_output function should take in a SOM and a VectorXd and return a single
     * VectorXd.
     * 
     * @param target The SOM.
     * @param get_output The get_output function.
     */
    void set_get_output(int target, function<VectorXd(SOM&, VectorXd&)> get_output);

    /** @brief Specifies the callback function for a given SOM during training.
     * 
     * Specified the callback function for a given SOM. The SOM is identified by the identifier that is returned
     * when the SOM is created. The callback should take in a SOM and the iteration number. This function is optional
     * and will be called at the end of each training iteration of the specified SOM.
     * 
     * @param target The SOM.
     * @param train_cb The callback.
     */
    void set_train_cb(int target, function<void(SOM& som, int t)> train_cb);

    /** @brief Gets the SOM at the given target.
     * 
     * @param target The SOM.
     * @return The underlying SOM.
     */
    SOM& get_SOM(int target) const;

    /** @brief Creates the network based on a adjacency matrix.
     * 
     * @param adj The adjacency matrix.
     */
    void link_from_adj(vector<vector<int>>& adj);

    /** @brief Gets the adjacency matrix of the network.
     * 
     * @return The adjacency matrix.
     */
    vector<vector<int>> get_adj() const;

    /** @brief Gets the index of the root SOM.
     * 
     * @return The root SOM's index.
     */
    int get_root() const;

    /** @brief Return the DeepSOM's number of training iterations.
     * 
     * @return Integer representing number of training iterations of DeepSOM.
     */
    int get_t_lim() const;

    /** @brief Replaces a SOM in the network with another SOM.
     * 
     * @param target The SOM.
     * @param replace The SOM to be replaced with.
     */
    void replace_som(int target, SOM* replace);

    /** @brief Return the SOM's number of nodes.
     * 
     * @return Integer representing number of nodes of SOM.
     */
    int get_node_num() const;

   private:

    /** @brief An internal representation of the Nodes of the DeepSOM network.
     */
    struct Node {
        /** @brief Node constructor.
         * 
         * @param id_v The unique identifier of the node.
         * @param nodes The list of all nodes.
         * @param som The SOM.
         */
        Node(int id_v, vector<DeepSOM::Node>& nodes, unique_ptr<SOM> som);

        /** @brief Default move constructor.
         */
        Node(Node&& n) = default;

        /** @brief Node destructor.
         */
        ~Node();

        /** @brief Trains one iteration of the underlying SOM.
         * 
         * @param datas The unmodified input data. Is not used for inner nodes.
         * @param t Current iteration number.
         */
        void batch_iter(vector<VectorXd>& datas, int t);

        void batch_block(vector<VectorXd>& datas);

        /** @brief The underlying reference to the list of nodes.
         */
        vector<DeepSOM::Node>& nodes;

        /** @brief The unique identifier.
         */
        int id_v;

        /** @brief The SOM stored at the node.
         */
        unique_ptr<SOM> som;

        /** @brief The callback function for training.
         */
        function<void(SOM& som, int t)> train_cb;

        /** @brief The get_data function.
         */
        function<VectorXd(VectorXd&)> get_data;

        /** @brief The training data at the current stage.
         */
        vector<VectorXd> transformed_data;

        /** @brief The combine function.
         */
        function<VectorXd(vector<VectorXd>&)> combine;

        /** @brief The get_output function.
         */
        function<VectorXd(SOM&, VectorXd&)> get_output;

        /** @brief The list of predecessors.
         */
        vector<int> froms;

        /** @brief The list of successors.
         */
        vector<int> to;
    };

    /** @brief Support DFS for topological sort
     * 
     * @param cur The current node to iterate over
     * @param visited An array tallying visitation records
     * @param ans The answer array
     */
    void ts_dfs(int cur, vector<bool>& visited, vector<int>& ans);

    /** @brief Sorts the nodes topologically and returns the outcome.
     * 
     * @return the order of the nodes
     */
    vector<int> topological_sort();

    /** @brief Count of nodes in SOM, used for Node id.
     */
    int node_num;

    /** @brief Number of training iterations.
     */
    int t_lim;

    /** @brief Internal storage of the nodes. Stored in column major order.
     */
    vector<DeepSOM::Node> nodes;
};

template <typename T, typename... Ts>
int DeepSOM::add_SOM(Ts&&... args) {
    static_assert(is_base_of<SOM, T>::value, "type parameter of must derive from SOM");
    this->nodes.emplace_back(this->node_num,
                             this->nodes,
                             unique_ptr<SOM>(new T(forward<Ts>(args)...)));
    return node_num++;
}