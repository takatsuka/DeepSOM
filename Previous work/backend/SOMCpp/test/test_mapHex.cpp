// #define CATCH_CONFIG_MAIN

#include <algorithm>
#include <vector>
#include <iostream>
#include <map> 

#include "SOM_header.hpp"
#include "catch.hpp"

using Eigen::Vector2d;
using Eigen::Vector3d;
using namespace std;

SCENARIO("Map2d class is implemented by MapHex", "[MapHex]") {
    GIVEN("Initialised a MapHex object") {
        MapHex mapH(1, 1, {4, 4}, 0, 0, 1);
        // test constructor
        WHEN("The object MapHex is created") {
            THEN("mapH is instance of MapHex") {
                REQUIRE(instanceof <MapHex>(mapH) == true);
            }
            THEN("mapH is instance of Map2d") {
                REQUIRE(instanceof <Map2d>(mapH) == true);
            }
            THEN("mapH is instance of SOM") {
                REQUIRE(instanceof <SOM>(mapH) == true);
            }
        }
    }
}

SCENARIO("MapHex can be set up correctly", "[MapHex]") {
    GIVEN("Initialise new MapRect with side_len 4") {
        MapHex mapH(1, 1, {4, 4}, 0, 0, 1);

        map<int,vector<int>> neighbor_counts;
        neighbor_counts[2] = vector<int>({0, 15});
        neighbor_counts[3] = vector<int>({2, 3, 12, 13});
        neighbor_counts[4] = vector<int>({4, 7, 8, 11});
        neighbor_counts[5] = vector<int>({1, 14});
        neighbor_counts[6] = vector<int>({5, 6, 9, 10});

        WHEN("MapH successfully created") {
            int col = mapH.get_lengths()[0];
            int row = mapH.get_lengths()[1];
            THEN("MapH should have side_len 4") {
                REQUIRE(col == 4);
                REQUIRE(row == 4);
            }

            THEN("MapH should have 16 Nodes") {
                REQUIRE(mapH.get_nodes().size() == 16);
            }

            THEN( "Check each node has correct number of neighbors" ) {
                for (Node node : mapH.get_nodes()){
                    REQUIRE(node.get_topo().size() == 2);
                    // cout << node.get_topo()[0] << endl;
                    // cout << "=====" << endl;

                    int node_id = node.get_id();
                    int key = node.get_neighbors().size();
                    vector<int> nodes = neighbor_counts[key];

                    bool correct = find(nodes.begin(), nodes.end(), node_id) != nodes.end();
                    if (!correct){
                        cout << "node_id: " << node_id << endl;
                        cout << "key: " << key << endl;
                    }
                    REQUIRE(correct == true);
                }
            }
        }
    }
}


SCENARIO("Using private MapHex topo_coord_calc()", "[MapHex]") {
    GIVEN("Initialised a MapHex object") {
        MapHex mapH(1, 1, {4, 4}, 0, 0, 1);
        // test constructor
        WHEN("Calculating topological coordinates") {
            THEN("The values are met") {
                for (int i = 0; i < 4; i++){
                    for (int j = 0; j < 4; j++){
                        VectorXd v = mapH.topo_coord_calc(i, j);

                        double diff = v[0] - sqrt(3.0) * (0.5 * (j & 1) + i);
                        REQUIRE(abs(diff) < EPSILON);

                        diff = v[1] - 1.5 * j;
                        REQUIRE(abs(diff) < EPSILON);
                    }
                }
            }
        }
    }
}