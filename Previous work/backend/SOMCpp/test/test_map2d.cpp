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



class Map2dTester : public Map2d {
   public:
    Map2dTester(int t_lim, int inp_dim, vector<int> lengths, int sigma = 0, double l = 0, double alpha = 0.5)
        : Map2d{t_lim, inp_dim, lengths, sigma, l, alpha} {
        vector<Node> testNodes;

        Vector3d init_pos(0, 0, 0);  // position in 3D feature space

        testNodes.emplace_back(Vector2d(0, 0), 0, init_pos);
        testNodes.emplace_back(Vector2d(0, 1), 1, init_pos);
        testNodes.emplace_back(Vector2d(0, 2), 2, init_pos);

        this->nodes = testNodes;
        this->node_num = this->nodes.size();
    }

    void change_node_pos(int idx, Vector3d newPos) {
        this->nodes[idx].set_pos(newPos);
    }
};


SCENARIO("Map2d class is implemented by Map2dTester", "[Map2d]") {
    GIVEN("Initialised a Map2dTester object") {
        Map2dTester map(1, 3, {1, 3});
        // test constructor
        WHEN("The object Map2dTester is created") {
            THEN("map is instance of Map2dTester") {
                REQUIRE(instanceof <Map2dTester>(map) == true);
            }
            THEN("map is instance of Map2d") {
                REQUIRE(instanceof <Map2d>(map) == true);
            }
            THEN("map is instance of SOM") {
                REQUIRE(instanceof <SOM>(map) == true);
            }
        }
    }
}

SCENARIO("Map2d class is implemented by Map2dTester with defaults", "[Map2d]") {
    GIVEN("Initialised a Map2dTester object") {
        Map2dTester map(1, 3, {1, 3});

        WHEN("Some parameters are unspecified") {
            int sigma = map.get_sigma();
            double l = map.get_l();
            double alpha = map.get_alpha();

            THEN("Unspecified alpha is 0.5") {
                REQUIRE(alpha == 0.5);
            }
            THEN("Unspecified sigma is 2") {
                // cout << map.get_lengths()[0] << endl;
                REQUIRE(sigma == 2);
            }
            THEN("Unspecified l is 0.8") {
                REQUIRE(l == 0.8);
            }
        }
    }
}

SCENARIO("Testing Map2d methods - get_nodes()", "[Map2d]") {
    GIVEN("Initialised a Map2dTester object") {
        Map2dTester map(1, 3, {1, 3});

        WHEN("Using Map2d method get_nodes()") {
            THEN("Returns a vector of Node objects") {
                REQUIRE(map.get_nodes().at(0).get_topo() == Vector2d(0, 0));
                REQUIRE(map.get_nodes().at(1).get_topo() == Vector2d(0, 1));
                REQUIRE(map.get_nodes().at(2).get_topo() == Vector2d(0, 2));
                REQUIRE(map.get_nodes().at(0).get_pos() == Vector3d(0, 0, 0));
                REQUIRE(map.get_nodes().at(1).get_pos() == Vector3d(0, 0, 0));
                REQUIRE(map.get_nodes().at(2).get_pos() == Vector3d(0, 0, 0));
                REQUIRE(map.get_nodes().at(0).get_id() == 0);
                REQUIRE(map.get_nodes().at(1).get_id() == 1);
                REQUIRE(map.get_nodes().at(2).get_id() == 2);
            }
        }
    }
}

SCENARIO("Testing Map2d methods - neighbor_multiplier()", "[Map2d]") {
    GIVEN("Initialised a Map2dTester object") {
        Map2dTester map(1, 3, {1, 3}, 0, 0, 0.5);

        WHEN("Using Map2d method neighbor_multiplier() for 0 dist_sqr") {

            double dist_mult = map.neighbor_multiplier(map.get_nodes()[0], map.get_nodes()[1], 1);

            // double dist_sqr = map.distance_sqr(map.get_nodes()[0].get_pos(), map.get_nodes()[1].get_pos());
            // cout << "dist_sqr: " << dist_sqr << endl;
            // double denom = 2 * pow(map.neighbor_size(1),2);
            // cout << "2 * pow(neighbor_size, 2): " << denom << endl;
            // cout << exp((-1*10000)/denom) << endl;
            // cout << map.get_nodes()[0].get_pos() << endl;
            // cout << map.get_nodes()[1].get_pos() << endl;

            THEN("We can calculate distance multiplier with dist_sqr 0") {
                REQUIRE(dist_mult == 1);
            }
        }
        
        WHEN("Using Map2d method neighbor_multiplier() for large dist_sqr") {

            map.change_node_pos(0, Vector3d(100, 1, 1));

            double dist_mult = map.neighbor_multiplier(map.get_nodes()[0], map.get_nodes()[1], 1);

            // double dist_sqr = map.distance_sqr(map.get_nodes()[0].get_pos(), map.get_nodes()[1].get_pos());
            // cout << "dist_sqr: " << dist_sqr << endl;
            // double denom = 2 * pow(map.neighbor_size(1),2);
            // cout << "2 * pow(neighbor_size, 2): " << denom << endl;
            // cout << exp((-1*10000)/denom) << endl;
            // cout << map.get_nodes()[0].get_pos() << endl;
            // cout << map.get_nodes()[1].get_pos() << endl;

            THEN("We can calculate distance multiplier with dist_sqr 0") {
                REQUIRE(dist_mult == 0);
            }
        }
    }
}

SCENARIO("Testing Map2d methods  - learning_rate()", "[Map2d]") {
    GIVEN("Initialised a Map2dTester object") {
        Map2dTester map(1, 3, {1, 3}, 0, 0, 0.5);

        WHEN("Using method learning_rate(0)") {

            double l = map.learning_rate(0);

            THEN("learning_rate is 0.5") {
                REQUIRE(l == 0.5);
            }
        }
        WHEN("Using overridden method learning_rate(1)") {
            // cout << map.get_l() << endl;
            double l = map.learning_rate(1);

            THEN("get calculated learning_rate") {
                double diff = l - 0.1432523984;
                REQUIRE(abs(diff) < EPSILON);
            }
        }
    }
}


SCENARIO("Testing Map2d methods - neighbor_size()", "[Map2d]") {
    GIVEN("Initialised a Map2dTester object") {
        Map2dTester map(3, 3, {1, 3}, 0, 0, 0.5);

        WHEN("Using method neighbor_size()") {
            double neighborSize = map.neighbor_size(3);

            THEN("get calculated neighborSize") {
                double diff = neighborSize - 0.5730095937;
                REQUIRE(abs(diff) < EPSILON);
            }
        }
    }
}



SCENARIO("Testing Map2d simple methods default", "[Map2d]") {
    GIVEN("Initialised a Map2dTester object") {
        Map2dTester map(3, 3, {1, 3}, 0, 0, 0.5);

        WHEN("Using method get_lengths()") {
            vector<int> topo_translater = map.get_lengths();

            THEN("get lengths vector") {
                REQUIRE(topo_translater[0] == 3);
                REQUIRE(topo_translater[1] == 1);
            }
        }
        
        WHEN("Using method get_sigma()") {
            int sigma = map.get_sigma();

            THEN("get calculated sigma") {
                REQUIRE(sigma == 2);
            }
        }
        WHEN("Using method get_l()") {
            double l = map.get_l();

            THEN("get calculated l") {
                double diff = l - 2.4;
                REQUIRE(abs(diff) < EPSILON);
            }
        }
        WHEN("Using method get_alpha()") {
            double alpha = map.get_alpha();

            THEN("get calculated alpha") {
                REQUIRE(alpha == 0.5);
            }
        }
    }
}

SCENARIO("Testing Map2d simple methods specified values", "[Map2d]") {
    GIVEN("Initialised a Map2dTester object") {
        Map2dTester map(3, 3, {1, 3}, 1, 1, 1);

        WHEN("Using method get_lengths()") {
            vector<int> topo_translater = map.get_lengths();

            THEN("get lengths vector") {
                REQUIRE(topo_translater[0] == 3);
                REQUIRE(topo_translater[1] == 1);
            }
        }

        WHEN("Using method get_sigma()") {
            int sigma = map.get_sigma();

            THEN("get calculated sigma") {
                REQUIRE(sigma == 1);
            }
        }
        WHEN("Using method get_l()") {
            double l = map.get_l();

            THEN("get calculated l") {
                REQUIRE(l == 1);
            }
        }
        WHEN("Using method get_alpha()") {
            double alpha = map.get_alpha();

            THEN("get calculated alpha") {
                REQUIRE(alpha == 1);
            }
        }
    }
}



// SCENARIO("Using SOM virtual methods - node_initialisation()", "[som]") {
//     GIVEN("Initialised a SOMTester object") {
//         SOMTester somTester(3, 3, {1, 3}, 0, 0, 0.5);

//         WHEN("Using overridden method node_initialisation(1)") {
//             double neighborSize = somTester.neighbor_size(1);

//             THEN("Returns a vector of Node objects") {
//                 REQUIRE(neighborSize == 1);
//             }
//         }

//         WHEN("Using overridden method node_initialisation(2)") {
//             double neighborSize = somTester.neighbor_size(2);

//             THEN("Returns a vector of Node objects") {
//                 REQUIRE(neighborSize == 2);
//             }
//         }

//         WHEN("Using overridden method node_initialisation(0)") {
//             double neighborSize = somTester.neighbor_size(0);

//             THEN("Returns a vector of Node objects") {
//                 REQUIRE(neighborSize == 0);
//             }
//         }

//         WHEN("Using overridden method node_initialisation(4) larger than t_lim") {
//             double neighborSize = somTester.neighbor_size(4);

//             THEN("Returns a vector of Node objects") {
//                 REQUIRE(neighborSize == 4);
//             }
//         }
//     }
// }
