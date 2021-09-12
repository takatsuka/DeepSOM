// #define CATCH_CONFIG_MAIN

#include <algorithm>
#include <vector>

#include "SOM_header.hpp"
#include "catch.hpp"
#include "iostream"

using Eigen::Vector2d;
using Eigen::Vector3d;
using namespace std;

SCENARIO("SOM class is implemented by Map2d", "[MapRect]") {
    GIVEN("Initialised a SOMTester object") {
        MapRect map(1, 1, {4, 4}, 0, 0, 1);
        // test constructor
        WHEN("The object somTester is created") {
            THEN("map is instance of Map2d") {
                REQUIRE(instanceof <Map2d>(map) == true);
            }
            THEN("map is instance of SOM") {
                REQUIRE(instanceof <SOM>(map) == true);
            }
        }
    }
}

SCENARIO("MapRect can be set up correctly", "[MapRect]") {
    GIVEN("Initialise new MapRect with side_len 3") {
        MapRect map(1, 1, {3, 3}, 0, 0, 1);

        WHEN("Map successfully created") {
            int col = map.get_lengths()[0];
            int row = map.get_lengths()[1];
            THEN("Map should have side_len 3") {
                REQUIRE(col == 3);
                REQUIRE(row == 3);
            }

            THEN("Map should have 9 Nodes") {
                REQUIRE(map.get_nodes().size() == 9);
            }

            THEN( "Check each node has correct number of neighbors" ) {
                for (Node node : map.get_nodes()){
                    REQUIRE(node.get_topo().size() == 2);
                    // cout << node.get_topo()[0] << endl;
                    // cout << "=====" << endl;

                    // Corner nodes have 2 neighbors, cast to int
                    if (int(node.get_topo()[0]) % (col - 1) == 0 && int(node.get_topo()[1]) % (row - 1) == 0){
                        REQUIRE(node.get_neighbors().size() == 2);
                    }
                    // Side column nodes have 3 neighbors
                    else if (int(node.get_topo()[0]) % (col - 1) == 0 && int(node.get_topo()[1]) % (row - 1) != 0){
                        REQUIRE(node.get_neighbors().size() == 3);
                    }
                    // Side row nodes have 3 neighbors
                    else if (int(node.get_topo()[0]) % (col - 1) != 0 && int(node.get_topo()[1]) % (row - 1) == 0){
                        REQUIRE(node.get_neighbors().size() == 3);
                    }
                    // Other nodes inside the SOM have 4 neighbors
                    else{
                        REQUIRE(node.get_neighbors().size() == 4);
                    }
                }
            }
        }
    }
}

SCENARIO("Euclidean Distance function works", "[MapRect]") {
    // Positive case
    GIVEN("Two vectors and a map") {
        VectorXd v1(2);
        v1 << 1, 5;
        VectorXd v2(2);
        v2 << -1, 5;
        MapRect map(1, 1, {4, 4}, 0, 0, 1);
        WHEN("Euclidean distance is calculated") {
            THEN("the distance is 4") {
                REQUIRE(map.distance_sqr(v1, v2) == 4.0);
            }
        }
    }
    // Edge case
    GIVEN("Two identical vectors and a map") {
        VectorXd v1(2);
        v1 << 1, 5;
        MapRect map(1, 1, {4, 4}, 0, 0, 1);
        WHEN("Euclidean distance is calculated") {
            THEN("the distance is 0") {
                REQUIRE(map.distance_sqr(v1, v1) == 0.0);
            }
        }
    }
}

SCENARIO("Neighbours are properly returned", "[MapRect]") {
    GIVEN("A map of side_len 4 and sigma 0") {
        MapRect map(1, 1, {4, 4}, 0, 0, 1);
        // Edge case
        WHEN("Neighbours are computed") {
            THEN("1 neighbour is returned") {
                REQUIRE(map.neighbors(map.get_nodes().at(0), 1).size() == 1);
            }
        }
    }
    GIVEN("A map of side_len 4 and sigma 4") {
        MapRect map(1, 1, {4, 4}, 4, 0, 1);
        // Positive case
        WHEN("Neighbours are computed at iteration t=1 and for a node in the middle") {
            THEN("5 neighbour is returned") {
                REQUIRE(map.neighbors(map.get_nodes().at(6), 1).size() == 5);
            }
        }
    }
    GIVEN("A map of side_len 4 and sigma 1") {
        MapRect map(1, 1, {4, 4}, 1, 0, 1);
        // Positive case
        WHEN("Neighbours are computed at iteration t=0 and for a node in the middle") {
            THEN("5 neighbours are returned") {
                REQUIRE(map.neighbors(map.get_nodes().at(6), 0).size() == 5);
            }
        }
        // Positive case
        WHEN("Neighbours are computed at iteration t=1 and for a node in the middle") {
            THEN("1 neighbour is returned") {
                REQUIRE(map.neighbors(map.get_nodes().at(6), 1).size() == 1);
            }
        }
        // Corner case
        WHEN("Neighbours are computed at iteration t=0 and for a node in the corner") {
            THEN("3 neighbours are returned") {
                REQUIRE(map.neighbors(map.get_nodes().at(0), 0).size() == 3);
            }
        }
        // Edge case
        WHEN("Neighbours are computed at iteration t=0 and for a node on the side") {
            THEN("4 neighbours are returned") {
                REQUIRE(map.neighbors(map.get_nodes().at(8), 0).size() == 4);
            }
        }
    }
}

SCENARIO("MapRect can find bmus", "[MapRect]") {
    GIVEN("MapRect with side_len 4 and dim 3 and a 3d vector of interest") {
        MapRect map(1, 3, {4, 4}, 0, 0, 1);
        VectorXd v1(3);
        v1 << 2, 0, 0;

        // Positive case
        WHEN("BMU is computed and there is a node exactly at the the vector of interest and all other nodes are random") {
            VectorXd v2(3);
            v2 << 1, 1, 1;

            vector<VectorXd> data;
            data.push_back(v2);
            data.push_back(v1);

            map.node_initialisation(data);
            map.get_nodes().at(3).set_pos(v1);
            THEN("Map should return this node") {
                REQUIRE(map.find_bmu(v1).get_pos() == v1);
            }
        }
        // Positive case
        WHEN("BMU is computed and there is a node close to the vector of interest") {
            VectorXd v2(3);
            v2 << 0, 0, 0;
            for (int i = 0; i < 16; i++) {
                map.get_nodes().at(i).set_pos(v2);
            }
            VectorXd v3(3);
            v3 << 1, 2, 5;

            map.get_nodes().at(3).set_pos(v3);
            THEN("Map should return this node") {
                REQUIRE(map.find_bmu(v3).get_pos() == v3);
            }
        }
        // Edge case
        WHEN("BMU is computed and there are 2 nodes equidistant to the vector of interest") {
            VectorXd v2(3);
            v2 << 0, 0, 0;
            for (int i = 0; i < 16; i++) {
                map.get_nodes().at(i).set_pos(v2);
            }
            VectorXd v3(3);
            v3 << 1, 0, 0;
            VectorXd v4(3);
            v4 << 2, 0, 0;

            map.get_nodes().at(3).set_pos(v3);
            map.get_nodes().at(7).set_pos(v4);
            THEN("Map should return either node") {
                bool result = (map.find_bmu(v1).get_pos() == v3 || map.find_bmu(v1).get_pos() == v4);
                REQUIRE(result == true);
            }
        }
    }
}