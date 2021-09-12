// #define CATCH_CONFIG_MAIN
#include <algorithm>
#include <iostream>
#include <vector>

#include "SOM_header.hpp"
#include "catch.hpp"

using Eigen::Vector2d;
using Eigen::Vector3d;
using Eigen::VectorXd;

using namespace std;

class SOMTester : public SOM {
   public:
    SOMTester(int t_lim, int inp_dim, vector<int> lengths, int sigma, double l, double alpha)
        : SOM{t_lim, inp_dim}, lengths{lengths}, sigma{sigma}, l{l}, alpha{alpha} {
        vector<Node> testNodes;

        Vector3d init_pos(0, 0, 0);  // position in 3D feature space

        testNodes.emplace_back(Vector2d(0, 0), 0, init_pos);
        testNodes.emplace_back(Vector2d(0, 1), 1, init_pos);
        testNodes.emplace_back(Vector2d(0, 2), 2, init_pos);

        this->nodes = testNodes;
        this->node_num = this->nodes.size();
    }

    vector<Node>& get_nodes() override {
        return this->nodes;
    }
   
    const vector<Node>& get_nodes() const override {
        return this->nodes;
    }

    double neighbor_multiplier(Node& best, Node& n2, int t) override {
        return t;
    }

    double learning_rate(int t) override {
        return t;
    }

    double neighbor_size(int t) override {
        return t;
    }

    void node_initialisation(vector<VectorXd>& datas) override {
        int n = datas.size();  // Number of data points (rows)
        for (int i = 0; i < n; i++) {
            this->nodes[i].set_pos(datas[i]);
        }
    }

    void change_node_pos(int idx, Vector3d newPos) {
        this->nodes[idx].set_pos(newPos);
    }

   protected:
    vector<Node> nodes;
    vector<int> lengths;
    int sigma;
    double l;
    double alpha;
};

SCENARIO("SOM class is implemented by SOMTester", "[som]") {
    GIVEN("Initialised a SOMTester object") {
        SOMTester somTester(3, 3, {1, 3}, 0, 0, 0.5);

        // test constructor
        WHEN("The object somTester is created") {
            THEN("somTester is instance of SOMTester") {
                REQUIRE(instanceof <SOMTester>(somTester) == true);
            }
            THEN("somTester is instance of SOM") {
                REQUIRE(instanceof <SOM>(somTester) == true);
            }
        }
    }
}

SCENARIO("Testing SOM methods - neighbors()", "[som]") {
    GIVEN("Initialised a SOMTester object") {
        SOMTester somTester(3, 3, {1, 3}, 0, 0, 0.5);

        WHEN("Using method neighbors() with node0 and t = 1") {
            Node best(Vector2d(0, 0), 0, Vector3d(0, 0, 0));

            vector<Node*> neighbors = somTester.neighbors(best, 1);

            THEN("Returns a vector of Node references with length 1") {
                Node n = *neighbors[0];

                REQUIRE(neighbors.size() == 1);
                REQUIRE(n.get_id() == 0);
                REQUIRE(n.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(n.get_topo() == Vector2d(0, 0));
            }
        }

        WHEN("Using method neighbors() with node1 and t = 1") {
            Node best(Vector2d(0, 1), 1, Vector3d(0, 0, 0));

            vector<Node*> neighbors = somTester.neighbors(best, 1);

            THEN("Returns a vector of Node references with length 1") {
                Node n = *neighbors[0];

                REQUIRE(neighbors.size() == 1);
                REQUIRE(n.get_id() == 1);
                REQUIRE(n.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(n.get_topo() == Vector2d(0, 1));
            }
        }

        WHEN("Using method neighbors() with node1 and t = 2") {
            Node best(Vector2d(0, 1), 1, Vector3d(0, 0, 0));

            vector<Node*> neighbors = somTester.neighbors(best, 2);

            THEN("Returns a vector of Node references with length 1") {
                Node n = *neighbors[0];

                REQUIRE(neighbors.size() == 1);
                REQUIRE(n.get_id() == 1);
                REQUIRE(n.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(n.get_topo() == Vector2d(0, 1));
            }
        }

        WHEN("Using method neighbors() with node1 and t = 0") {
            Node best(Vector2d(0, 1), 1, Vector3d(0, 0, 0));

            vector<Node*> neighbors = somTester.neighbors(best, 0);

            THEN("Returns a vector of Node references with length 1") {
                Node n = *neighbors[0];

                REQUIRE(neighbors.size() == 1);
                REQUIRE(n.get_id() == 1);
                REQUIRE(n.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(n.get_topo() == Vector2d(0, 1));
            }
        }
    }
}

SCENARIO("Using SOM methods - distance_sqr()", "[som]") {
    GIVEN("Initialised a SOMTester object") {
        SOMTester somTester(3, 3, {1, 3}, 0, 0, 0.5);

        // edge case: same vector
        WHEN("Using method distance_sqr() for the same vector") {
            VectorXd v1(3);
            v1 << 0, 0, 0;

            double distance_sqr = somTester.distance_sqr(v1, v1);

            THEN("Returns squared distance between two points") {
                REQUIRE(distance_sqr == 0);
            }
        }

        // positive case
        WHEN("Using method distance_sqr()") {
            VectorXd v1(3);
            v1 << 0, 0, 0;
            VectorXd v2(3);
            v2 << 0, 0, 1;

            double distance_sqr = somTester.distance_sqr(v1, v2);

            THEN("Returns squared distance between two points") {
                REQUIRE(distance_sqr == 1);
            }
        }

        // positive case
        WHEN("Using method distance_sqr()") {
            VectorXd v1(3);
            v1 << 0, 0, 0;
            VectorXd v2(3);
            v2 << 1, 0, 1;

            double distance_sqr = somTester.distance_sqr(v1, v2);

            THEN("Returns squared distance between two points") {
                REQUIRE(distance_sqr == 2);
            }
        }

        // positive case
        WHEN("Using method distance_sqr()") {
            VectorXd v1(3);
            v1 << 0, 1, 0;
            VectorXd v2(3);
            v2 << 1, 0, 1;

            double distance_sqr = somTester.distance_sqr(v1, v2);

            THEN("Returns squared distance between two points") {
                REQUIRE(distance_sqr == 3);
            }
        }

        // positive case
        WHEN("Using method distance_sqr()") {
            VectorXd v1(3);
            v1 << 0, 0, 0;
            VectorXd v2(3);
            v2 << 1, 1, 1;

            double distance_sqr = somTester.distance_sqr(v1, v2);

            THEN("Returns squared distance between two points") {
                REQUIRE(distance_sqr == 3);
            }
        }

        // positive case
        WHEN("Using method distance_sqr()") {
            VectorXd v1(3);
            v1 << 1, 0, 1;
            VectorXd v2(3);
            v2 << 1, 1, 1;

            double distance_sqr = somTester.distance_sqr(v1, v2);

            THEN("Returns squared distance between two points") {
                REQUIRE(distance_sqr == 1);
            }
        }

        // positive case 2d vector
        WHEN("Using method distance_sqr()") {
            VectorXd v1(2);
            v1 << 0, 0;
            VectorXd v2(2);
            v2 << 4, 5;

            double distance_sqr = somTester.distance_sqr(v1, v2);

            THEN("Returns squared distance between two points") {
                REQUIRE(distance_sqr == 41);
            }
        }
    }
}

SCENARIO("Using SOM methods - new_node()", "[som]") {
    GIVEN("Initialised a SOMTester object") {
        SOMTester somTester(3, 3, {1, 3}, 0, 0, 0.5);

        WHEN("Using method new_node() once") {
            VectorXd v1(2);
            v1 << 0, 3;
            VectorXd v2(3);
            v2 << 0, 0, 0;

            Node n = somTester.new_node(v1, v2);

            THEN("Returns a Node object") {
                REQUIRE(n.get_id() == 3);
                REQUIRE(n.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(n.get_topo() == Vector2d(0, 3));
            }
        }

        WHEN("Using method new_node() twice") {
            VectorXd v1(2);
            v1 << 0, 3;
            VectorXd v2(2);
            v2 << 0, 4;
            VectorXd v3(3);
            v3 << 0, 0, 0;

            Node n1 = somTester.new_node(v1, v3);
            Node n2 = somTester.new_node(v2, v3);

            THEN("Returns two Node objects") {
                REQUIRE(n1.get_id() == 3);
                REQUIRE(n1.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(n1.get_topo() == Vector2d(0, 3));
                REQUIRE(n2.get_id() == 4);
                REQUIRE(n2.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(n2.get_topo() == Vector2d(0, 4));
            }
        }
    }
}

SCENARIO("Using SOM methods - find_bmu()", "[som]") {
    GIVEN("Initialised a SOMTester object") {
        SOMTester somTester(3, 3, {1, 3}, 0, 0, 0.5);

        WHEN("Using method find_bmu() for all nodes with same position") {
            Node bmu = somTester.find_bmu(Vector3d(0, 0, 0));

            THEN("Returns first best matching unit Node") {
                REQUIRE(bmu.get_id() == 0);
                REQUIRE(bmu.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(bmu.get_topo() == Vector2d(0, 0));
            }
        }

        WHEN("Using method find_bmu() for all nodes with different position") {
            somTester.change_node_pos(1, Vector3d(1, 1, 1));

            Node bmu = somTester.find_bmu(Vector3d(2, 2, 2));

            THEN("Returns first best matching unit Node") {
                REQUIRE(bmu.get_id() == 1);
                REQUIRE(bmu.get_pos() == Vector3d(1, 1, 1));
                REQUIRE(bmu.get_topo() == Vector2d(0, 1));
            }
        }

        WHEN("Using method find_bmu() for all nodes with different position") {
            somTester.change_node_pos(1, Vector3d(1, 1, 1));

            Node bmu = somTester.find_bmu(Vector3d(-2, -2, -2));

            THEN("Returns first best matching unit Node") {
                REQUIRE(bmu.get_id() == 0);
                REQUIRE(bmu.get_pos() == Vector3d(0, 0, 0));
                REQUIRE(bmu.get_topo() == Vector2d(0, 0));
            }
        }

        WHEN("Using method find_bmu() with vector of different dimension") {
            THEN("Throws an exception") {
                REQUIRE_THROWS(somTester.find_bmu(Vector2d(2, 2)));
            }
        }
    }
}

SCENARIO("Using SOM methods - find_bmu_k()", "[som]") {
    GIVEN("Initialised a SOMTester object") {
        SOMTester somTester(3, 3, {1, 3}, 0, 0, 0.5);

        WHEN("Using method find_bmu_k() to find 0 closest bmu") {
            vector<Node*> bmus = somTester.find_bmu_k(Vector3d(0, 0, 0), 0);

            THEN("Returns a vector of Node objects of length 0") {
                REQUIRE(bmus.size() == 0);
            }
        }

        WHEN("Using method find_bmu_k() to find 1 closest bmu") {
            vector<Node*> bmus = somTester.find_bmu_k(Vector3d(0, 0, 0), 1);

            THEN("Returns a vector of Node objects of length 1") {
                REQUIRE(bmus.size() == 1);

                Node bmu = *bmus[0];
                REQUIRE((bmu.get_id() == 1 || bmu.get_id() == 2 || bmu.get_id() == 0));
                REQUIRE(bmu.get_pos() == Vector3d(0, 0, 0));
            }
        }

        WHEN("Using method find_bmu_k() to find 2 closest bmu") {
            vector<Node*> bmus = somTester.find_bmu_k(Vector3d(0, 0, 0), 2);

            THEN("Returns a vector of Node objects of length 2") {
                REQUIRE(bmus.size() == 2);

                Node bmu1 = *bmus[0];
                REQUIRE((bmu1.get_id() == 1 || bmu1.get_id() == 2 || bmu1.get_id() == 0));
                REQUIRE(bmu1.get_pos() == Vector3d(0, 0, 0));
                Node bmu2 = *bmus[1];
                REQUIRE((bmu2.get_id() == 1 || bmu2.get_id() == 2 || bmu2.get_id() == 0));
                REQUIRE(bmu2.get_pos() == Vector3d(0, 0, 0));
            }
        }

        WHEN("Using method find_bmu_k() to find 2 closest bmu") {
            vector<Node*> bmus = somTester.find_bmu_k(Vector3d(0, 0, 0), 3);

            THEN("Returns a vector of Node objects of length 3") {
                REQUIRE(bmus.size() == 3);

                Node& bmu1 = *bmus[0];
                REQUIRE((bmu1.get_id() == 1 || bmu1.get_id() == 2 || bmu1.get_id() == 0));
                REQUIRE(bmu1.get_pos() == Vector3d(0, 0, 0));
                Node& bmu2 = *bmus[1];
                REQUIRE((bmu2.get_id() == 1 || bmu2.get_id() == 2 || bmu2.get_id() == 0));
                REQUIRE(bmu2.get_pos() == Vector3d(0, 0, 0));
                Node& bmu3 = *bmus[2];
                REQUIRE((bmu3.get_id() == 1 || bmu3.get_id() == 2 || bmu3.get_id() == 0));
                REQUIRE(bmu3.get_pos() == Vector3d(0, 0, 0));
            }
        }

        // edge case
        WHEN("Using method find_bmu_k() with negative number") {
            THEN("Throws an exception") {
                REQUIRE_THROWS(somTester.find_bmu_k(Vector3d(0, 0, 0), -1));
            }
        }

        // edge case: k is larger than number of nodes in SOM
        WHEN("Using method find_bmu_k() to find 4 closest bmu, more than nodes in SOM") {
            THEN("Throws an exception") {
                REQUIRE_THROWS(somTester.find_bmu_k(Vector3d(0, 0, 0), 4));
            }
        }

        WHEN("Using method find_bmu_k() with nodes at different positions") {
            somTester.change_node_pos(2, Vector3d(0, 0, 0));
            somTester.change_node_pos(0, Vector3d(1, 1, 1));
            somTester.change_node_pos(1, Vector3d(2, 2, 2));

            vector<Node*> bmus = somTester.find_bmu_k(Vector3d(3, 3, 3), 3);

            THEN("Nodes are ordered from closest to furthest") {
                REQUIRE(bmus[0]->get_id() == 1);
                REQUIRE(bmus[0]->get_pos() == Vector3d(2, 2, 2));
                REQUIRE(bmus[0]->get_topo() == Vector2d(0, 1));
                REQUIRE(bmus[1]->get_id() == 0);
                REQUIRE(bmus[1]->get_pos() == Vector3d(1, 1, 1));
                REQUIRE(bmus[1]->get_topo() == Vector2d(0, 0));
                REQUIRE(bmus[2]->get_id() == 2);
                REQUIRE(bmus[2]->get_pos() == Vector3d(0, 0, 0));
                REQUIRE(bmus[2]->get_topo() == Vector2d(0, 2));
            }
        }

        WHEN("Using method find_bmu_k() with nodes at different positions") {
            somTester.change_node_pos(2, Vector3d(0, 0, 0));
            somTester.change_node_pos(0, Vector3d(1, 1, 1));
            somTester.change_node_pos(1, Vector3d(2, 2, 2));

            vector<Node*> bmus = somTester.find_bmu_k(Vector3d(3, 3, 3), 2);

            THEN("Nodes are ordered from closest to furthest") {
                // Node bmu1 = *bmus[0];
                REQUIRE(bmus[0]->get_id() == 1);
                REQUIRE(bmus[0]->get_pos() == Vector3d(2, 2, 2));
                REQUIRE(bmus[0]->get_topo() == Vector2d(0, 1));
                // Node bmu3 = *bmus[2];
                REQUIRE(bmus[1]->get_id() == 0);
                REQUIRE(bmus[1]->get_pos() == Vector3d(1, 1, 1));
                REQUIRE(bmus[1]->get_topo() == Vector2d(0, 0));
            }
        }
    }
}