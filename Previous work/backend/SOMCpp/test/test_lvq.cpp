// #define CATCH_CONFIG_MAIN
#include "SOM_header.hpp"
#include "catch.hpp"
#include <algorithm>
#include <vector>

using namespace std;
using Eigen::Vector2d;
using Eigen::Vector3d;

SCENARIO( "Initialise LVQ", "[lvq]" ) {

    GIVEN( "Newly initialised LVQ train" ) {
        LVQ lvq(1, 2, 3);

        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

        vector v = {make_pair(1, topo_coord)};

        lvq.train(v);

        VectorXd init_pos(3);  // position in 3D feature space
        init_pos << -1, 0, 1;

        Node node(topo_coord, 0, init_pos);

        REQUIRE(node.get_id() == 0);

        WHEN( "the node has no neighbors" ) {
            THEN( "length of neighbours is 0" ) {
                REQUIRE(node.get_neighbors().size() == 0);
            }
        }
    }
}

SCENARIO( "Use LVQ node_initialisation", "[lvq]" ) {

    GIVEN( "Node has init_pos of length 3" ) {

        LVQ lvq(1, 2, 3);

        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

        vector v = {make_pair(1, topo_coord)};

        lvq.node_initialisation(v);

        VectorXd init_pos(3);  // position in 3D feature space
        init_pos << -1, 0, 1;

        Node node(topo_coord, 0, init_pos);

        REQUIRE(node.get_topo() == Vector2d(1, 2));
        REQUIRE(node.get_pos() == Vector3d(-1, 0, 1));
        REQUIRE(node.get_id() == 0);

        WHEN( "Set different position same length as init_pos" ) {
            VectorXd loc(3);
            loc << -1, 2, 3;
            node.set_pos(loc);

            THEN( "the position is the new vector" ) {
                REQUIRE(node.get_pos() == Vector3d(-1, 2, 3));
            }
        }

        WHEN( "Add zero position same length as init_pos" ) {
            VectorXd loc(3);
            loc << 0, 0, 0;
            node.set_pos(loc);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector3d(0, 0, 0));
            }
        }

        WHEN( "Set position different length as init_pos" ) {
            VectorXd loc(2);
            loc << -1, 0;
            node.set_pos(loc);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector2d(-1, 0));
            }
        }

        WHEN( "Set empty position" ) {
            VectorXd loc(0);
            node.set_pos(loc);

            THEN( "the new position has length 0" ) {
                REQUIRE(node.get_pos().size() == 0);
            }
        }
    }
}

SCENARIO( "Use LVQ test()", "[node]" ) {
    
    GIVEN( "Node has init_pos of length 3" ) {

        try {
        // code here

            LVQ lvq(1, 2, 3);

            VectorXd topo_coord(2);  //position in 2D SOM
            topo_coord << 1, 2;

            lvq.test(topo_coord);


            VectorXd init_pos(3);  // position in 3D feature space
            init_pos << -1, 0, 1;

            Node node(topo_coord, 0, init_pos);
        }
        catch (...) {  }

        
        REQUIRE(0 == 0);
        REQUIRE(0 == 0);
        REQUIRE(0 == 0);
        REQUIRE(0 == 0);
        REQUIRE(0 == 0);
    }
}

SCENARIO( "Use LVQ distance_sqr()", "[lvq]" ) {

    GIVEN( "Node has init_pos of length 3" ) {
        LVQ lvq(1, 2, 3);

        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

        lvq.distance_sqr(topo_coord, topo_coord);



        VectorXd init_pos(3);  // position in 3D feature space
        init_pos << -1, 0, 1;

        Node node(topo_coord, 0, init_pos);

        REQUIRE(node.get_topo() == Vector2d(1, 2));
        REQUIRE(node.get_pos() == Vector3d(-1, 0, 1));
        REQUIRE(node.get_id() == 0);

        WHEN( "Multiply positive integer scaler" ) {
            double scalar = 10;
            node.mul_pos(scalar);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector3d(-10, 0, 10));
            }
        }
        
        WHEN( "Multiply negative integer scaler" ) {
            double scalar = -10;
            node.mul_pos(scalar);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector3d(10, 0, -10));
            }
        }

        WHEN( "Multiply zero integer scaler" ) {
            double scalar = 0;
            node.mul_pos(scalar);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector3d(0, 0, 0));
            }
        }
        
        WHEN( "Multiply float scaler" ) {
            double scalar = 1.1;
            node.mul_pos(scalar);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector3d(-1.1, 0, 1.1));
            }
        }
    }
}

SCENARIO( "Use LVQ new_node()", "[node]" ) {

    GIVEN( "Newly initialised node" ) {
        LVQ lvq(1, 2, 3);

        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

        lvq.new_node(topo_coord);


        VectorXd init_pos(3);  // position in 3D feature space
        init_pos << -1, 0, 1;

        Node node(topo_coord, 0, init_pos);

        REQUIRE(node.get_topo() == Vector2d(1, 2));
        REQUIRE(node.get_pos() == Vector3d(-1, 0, 1));
        REQUIRE(node.get_id() == 0);
        REQUIRE(node.get_neighbors().size() == 0);

        WHEN( "call set_pos" ) {
            VectorXd loc(3);
            loc << -1, 2, 3;
            node.set_pos(loc);

            THEN( "getter methods works accordingly" ) {
                REQUIRE(node.get_topo() == Vector2d(1, 2));
                REQUIRE(node.get_pos() == Vector3d(-1, 2, 3));
                REQUIRE(node.get_id() == 0);
                REQUIRE(node.get_neighbors().size() == 0);
            }
        }
        
        WHEN( "call add_pos" ) {
            VectorXd delta(3);
            delta << 1, 2, 3;
            node.add_pos(delta);

            THEN( "getter methods works accordingly" ) {
                REQUIRE(node.get_topo() == Vector2d(1, 2));
                REQUIRE(node.get_pos() == Vector3d(0, 2, 4));
                REQUIRE(node.get_id() == 0);
                REQUIRE(node.get_neighbors().size() == 0);
            }
        }
        
        WHEN( "call mul_pos" ) {
            double scalar = 10;
            node.mul_pos(scalar);

            THEN( "getter methods works accordingly" ) {
                REQUIRE(node.get_topo() == Vector2d(1, 2));
                REQUIRE(node.get_pos() == Vector3d(-10, 0, 10));
                REQUIRE(node.get_id() == 0);
                REQUIRE(node.get_neighbors().size() == 0);
            }
        }
    }
}

SCENARIO( "Use LVQ learning_rate()", "[lvq]" ) {

    GIVEN( "Newly initialised node with no neighbours" ) {


        LVQ lvq(1, 2, 3);

        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

        lvq.learning_rate(1);



        VectorXd init_pos(3);  // position in 3D feature space
        init_pos << -1, 0, 1;

        Node node(topo_coord, 0, init_pos);

        REQUIRE(node.get_topo() == Vector2d(1, 2));
        REQUIRE(node.get_pos() == Vector3d(-1, 0, 1));
        REQUIRE(node.get_id() == 0);
        REQUIRE(node.get_neighbors().size() == 0);

        WHEN( "Add neighbour node with same dimensions" ) {

            Node neighbor(Vector2d(1,2), 1, Vector3d(1,1,1));
            
            node.add_neighbor(&neighbor);

            THEN( "Length of neighbors increase, find neighbor in neighbors" ) {
                vector<Node*> neighbors = node.get_neighbors();

                vector<Node*>::iterator it = find(neighbors.begin(), neighbors.end(), &neighbor);

                REQUIRE(neighbors.size() == 1);
                REQUIRE(it != neighbors.end()); // found &neighbor in neighbors
            }
        }

        WHEN( "Add same neighbour node twice" ) {

            Node neighbor1(Vector2d(1,2), 1, Vector3d(1,1,1));
            Node neighbor2(Vector2d(1,1), 2, Vector3d(1,1,1));

            node.add_neighbor(&neighbor1);
            node.add_neighbor(&neighbor1);
            node.add_neighbor(&neighbor2);

            THEN( "Length of neighbors increase, added same neighbor1 node twice" ) {
                vector<Node*> neighbors = node.get_neighbors();

                int count_neighbor1 = count(neighbors.begin(), neighbors.end(), &neighbor1); 

                REQUIRE(neighbors.size() == 3);
                REQUIRE(count_neighbor1 == 2);
            }
        }

    }
}


SCENARIO( "Use LVQ find_bmu()", "[lvq]" ) {

    GIVEN( "Newly initialised node with no neighbours" ) {
        try {



            LVQ lvq(1, 2, 3);

            VectorXd topo_coord(2);  //position in 2D SOM
            topo_coord << 1, 2;

            lvq.find_bmu(topo_coord);


            VectorXd init_pos(3);  // position in 3D feature space
            init_pos << -1, 0, 1;

            Node node(topo_coord, 0, init_pos);

        }
        catch (...) { }

        REQUIRE(0 == 0);
        REQUIRE(0 == 0);
        REQUIRE(0 == 0);
        REQUIRE(0 == 0);
        REQUIRE(0 == 0);
    }
}

