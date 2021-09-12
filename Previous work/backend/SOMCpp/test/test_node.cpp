// #define CATCH_CONFIG_MAIN
#include "SOM_header.hpp"
#include "catch.hpp"
#include <algorithm>
#include <vector>

using namespace std;
using Eigen::Vector2d;
using Eigen::Vector3d;

SCENARIO( "Nodes can be set up correctly", "[node]" ) {

    GIVEN( "Newly initialised node" ) {
        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

        VectorXd init_pos(3);  // position in 3D feature space
        init_pos << -1, 0, 1;

        Node node(topo_coord, 0, init_pos);

        REQUIRE(node.get_topo() == Vector2d(1, 2));
        REQUIRE(node.get_pos() == Vector3d(-1, 0, 1));
        REQUIRE(node.get_id() == 0);

        WHEN( "the node has no neighbors" ) {
            THEN( "length of neighbours is 0" ) {
                REQUIRE(node.get_neighbors().size() == 0);
            }
        }
    }
}

SCENARIO( "Nodes can set position", "[node]" ) {

    GIVEN( "Node has init_pos of length 3" ) {
        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

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

SCENARIO( "Nodes can add position", "[node]" ) {
    
    GIVEN( "Node has init_pos of length 3" ) {
        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

        VectorXd init_pos(3);  // position in 3D feature space
        init_pos << -1, 0, 1;

        Node node(topo_coord, 0, init_pos);

        REQUIRE(node.get_topo() == Vector2d(1, 2));
        REQUIRE(node.get_pos() == Vector3d(-1, 0, 1));
        REQUIRE(node.get_id() == 0);

        WHEN( "Add positive position same length as init_pos" ) {
            VectorXd delta(3);
            delta << 1, 2, 3;
            node.add_pos(delta);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector3d(0, 2, 4));
            }
        }

        WHEN( "Add negative position same length as init_pos" ) {
            VectorXd delta(3);
            delta << -1, -2, -3;
            node.add_pos(delta);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector3d(-2, -2, -2));
            }
        }

        WHEN( "Add zero position same length as init_pos" ) {
            VectorXd delta(3);
            delta << 0, 0, 0;
            node.add_pos(delta);

            THEN( "the position changes accordingly" ) {
                REQUIRE(node.get_pos() == Vector3d(-1, 0, 1));
            }
        }

        WHEN( "Add position different length as init_pos, throws error" ) {
            VectorXd delta(2);
            delta << -1, 0;

            THEN( "An exception is thrown" ) {
                REQUIRE_THROWS(node.add_pos(delta));
            }
        }
    }
}

SCENARIO( "Nodes can multiply position by a scaler", "[node]" ) {

    GIVEN( "Node has init_pos of length 3" ) {
        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

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

SCENARIO( "Node getter methods work correctly after modification", "[node]" ) {

    GIVEN( "Newly initialised node" ) {
        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

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

SCENARIO( "Node can add and get neighbours", "[node]" ) {

    GIVEN( "Newly initialised node with no neighbours" ) {
        VectorXd topo_coord(2);  //position in 2D SOM
        topo_coord << 1, 2;

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

        WHEN( "Add neighbour with different dimensions" ) {
            VectorXd topo_coor_neighbor(3);  //position in 2D SOM
            topo_coor_neighbor << 1, 2, 3;

            VectorXd init_pos_neighbor(4);  // position in 3D feature space
            init_pos_neighbor << 1, 1, 1, 1;

            Node neighbor(topo_coor_neighbor, 1, init_pos_neighbor);

            node.add_neighbor(&neighbor);

            THEN( "Length of neighbors increase" ) {
                vector<Node*> neighbors = node.get_neighbors();

                vector<Node*>::iterator it = find(neighbors.begin(), neighbors.end(), &neighbor);

                REQUIRE(neighbors.size() == 1);
                REQUIRE(it != neighbors.end()); // found &neighbor with different dimensions in neighbors
            }
        }
    }
}

