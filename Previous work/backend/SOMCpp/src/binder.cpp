#include <math.h>
#include <pybind11/eigen.h>
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iomanip>  // std::setprecision
#include <typeindex>
#include <typeinfo>

#include "DeepSOM.hpp"
#include "LVQ.hpp"
#include "Map2d.hpp"
#include "MapHex.hpp"
#include "MapRect.hpp"
#include "Node.hpp"
#include "SOM.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

// Dummy class to provide an concrete implementation of abstract classes
class PySOM : public SOM {
   public:
    using SOM::SOM;

    vector<Node> &get_nodes() override {
        PYBIND11_OVERLOAD_PURE(vector<Node> &, SOM, get_nodes);
    }

    const vector<Node> &get_nodes() const override {
        PYBIND11_OVERLOAD_PURE(const vector<Node> &, SOM, get_nodes);
    }

    double neighbor_multiplier(Node &best, Node &n2, int t) override {
        PYBIND11_OVERLOAD_PURE(double, SOM, neighbor_multiplier, best, n2, t);
    }

    double learning_rate(int t) override {
        PYBIND11_OVERLOAD_PURE(double, SOM, learning_rate, t);
    }

    double neighbor_size(int t) override {
        PYBIND11_OVERLOAD_PURE(double, SOM, neighbor_size, t);
    }

    void node_initialisation(vector<VectorXd> &datas) override {
        PYBIND11_OVERLOAD_PURE(void, SOM, node_initialisation, datas);
    }
};

// A method to pickle Map2d objects
py::tuple pickle_Map2d(const Map2d &p) {
    vector<VectorXd> pos;
    // Get all the position of the nodes
    for (const Node &node : p.get_nodes()) {
        pos.push_back(node.get_pos());
    }

    return py::make_tuple(p.get_t_lim(),
                          p.get_inp_dim(),
                          p.get_lengths(),
                          p.get_sigma(),
                          p.get_l(),
                          p.get_alpha(),
                          pos);
}

// Unpickle to Map2d. Need to specify which type of Map2d to unpickle to
template <typename T>
T *unpickle_Map2d(py::tuple &t) {
    static_assert(is_base_of<Map2d, T>::value, "cannot pickle");
    T *p = new T(t[0].cast<int>(),
                 t[1].cast<int>(),
                 t[2].cast<vector<int>>(),
                 t[3].cast<int>(),
                 t[4].cast<double>(),
                 t[5].cast<double>());
    vector<VectorXd> pos = t[6].cast<vector<VectorXd>>();
    vector<Node> &nodes = p->get_nodes();
    // Reset node positions
    for (int i = 0; i < p->get_node_num(); i++) {
        nodes[i].set_pos(pos[i]);
    }
    return p;
}

PYBIND11_MODULE(SOMCpp, m) {
    py::class_<Node>(m, "Node")
        .def(py::init<const VectorXd &, int, const VectorXd &>(), "topo_coord"_a, "id_v"_a, "init_pos"_a)
        .def_property_readonly("position", &Node::get_pos)
        .def_property_readonly("topo", &Node::get_topo)
        .def_property_readonly("neighbors", &Node::get_neighbors)
        .def_property_readonly("id_v", &Node::get_id)
        .def("__repr__",
             [](const Node &a) {
                 std::stringstream ss;
                 ss << "{Topo: (";
                 for (int i = 0; i < a.get_topo().rows(); ++i) {
                     ss << setprecision(5) << a.get_topo().coeff(i, 0) << ", ";
                 }
                 ss << "), ";

                 ss << "Pos: (";
                 for (int i = 0; i < a.get_pos().rows(); ++i) {
                     ss << setprecision(5) << a.get_pos().coeff(i, 0) << ", ";
                 }
                 ss << ")}";
                 return ss.str();
             });

    py::class_<SOM, PySOM>(m, "SOM")
        .def(py::init<int, int>())
        .def("stochastic_train", &SOM::stochastic_train)
        // pybind11 has broken support for references in functionals
        .def(
            "batch_train", [](SOM &a, vector<VectorXd> &datas, function<void(SOM * som, int t)> post_cb_ptr) {
            if(post_cb_ptr){
                // If a callback was supplied, convert the passed in reference to a pointer and use it
                a.batch_train(datas, [post_cb_ptr](SOM& som, int t) {
                    post_cb_ptr(&som, t);
                });
            }else{
                // If a callback was not supplied, use the default.
                a.batch_train(datas);
            } }, "datas"_a, "post_cb_ptr"_a = function<void(SOM * som, int t)>())
        .def("find_bmu", &SOM::find_bmu, "inp_vec"_a)
        // find_bmu_k returns a vector of pointers. The object's lifetime must exceed that of the pointers
        .def("find_bmu_k", &SOM::find_bmu_k, "inp_vec"_a, "k"_a, py::return_value_policy::reference_internal)
        .def<vector<Node> &(SOM::*)()>("get_nodes", &SOM::get_nodes);

    py::class_<MapRect, SOM>(m, "MapRect")
        .def(py::init<int, int, vector<int>, int, double, double>(), "t_lim"_a, "inp_dim"_a, "lengths"_a, "sigma"_a = 0, "l"_a = 0, "alpha"_a = 1)
        .def_property_readonly("lengths", &MapRect::get_lengths)
        // Define pickle support
        .def(py::pickle([](const MapRect &p) { return pickle_Map2d(p); },
                        [](py::tuple t) {
                            return unpickle_Map2d<MapRect>(t);
                        }));

    py::class_<MapHex, SOM>(m, "MapHex")
        .def(py::init<int, int, vector<int>, int, double, double>(), "t_lim"_a, "inp_dim"_a, "lengths"_a, "sigma"_a = 0, "l"_a = 0, "alpha"_a = 1)
        .def_property_readonly("lengths", &MapHex::get_lengths)
        // Define pickle support
        .def(py::pickle([](const MapHex &p) { return pickle_Map2d(p); },
                        [](py::tuple t) {
                            return unpickle_Map2d<MapHex>(t);
                        }));

    py::class_<DeepSOM>(m, "DeepSOM")
        .def(py::init<int>(), "t_lim"_a)
        .def(
            "batch_train", [](DeepSOM &a, vector<VectorXd> &datas, function<void(DeepSOM * som, int t)> post_cb_ptr) {
            if(post_cb_ptr){
                // If a callback was supplied, convert the passed in reference to a pointer and use it
                a.batch_train(datas, [post_cb_ptr](DeepSOM& som, int t) {
                    post_cb_ptr(&som, t);
                });
            }else{
                // If a callback was not supplied, use the default.
                a.batch_train(datas);
            } }, "datas"_a, "post_cb_ptr"_a = function<void(DeepSOM * deep_som, int t)>())
        .def(
            "batch_train_block", [](DeepSOM &a, vector<VectorXd> &datas, function<void(DeepSOM * som, int t)> post_cb_ptr) {
            if(post_cb_ptr){
                // If a callback was supplied, convert the passed in reference to a pointer and use it
                a.batch_train_block(datas, [post_cb_ptr](DeepSOM& som, int t) {
                    post_cb_ptr(&som, t);
                });
            }else{
                // If a callback was not supplied, use the default.
                a.batch_train_block(datas);
            } }, "datas"_a, "post_cb_ptr"_a = function<void(DeepSOM * deep_som, int t)>())
        // Python does not support templates, so template parameters need to be filled manually
        .def(
            "add_MapHex", [](DeepSOM &a, int t_lim, int inp_dim, vector<int> lengths, int sigma, double l, double alpha) {
                return a.add_SOM<MapHex>(t_lim, inp_dim, lengths, sigma, l, alpha);
            },
            "t_lim"_a, "inp_dim"_a, "lengths"_a, "sigma"_a = 0, "l"_a = 0, "alpha"_a = 0.2)
        .def(
            "add_MapRect", [](DeepSOM &a, int t_lim, int inp_dim, vector<int> lengths, int sigma, double l, double alpha) {
                return a.add_SOM<MapRect>(t_lim, inp_dim, lengths, sigma, l, alpha);
            },
            "t_lim"_a, "inp_dim"_a, "lengths"_a, "sigma"_a = 0, "l"_a = 0, "alpha"_a = 0.2)
        .def("add_link", &DeepSOM::add_link)
        .def("set_combine", &DeepSOM::set_combine)
        .def("set_get_data", &DeepSOM::set_get_data)
        // Pointer to reference conversion required
        .def("set_get_output", [](DeepSOM &a, int target, function<VectorXd(SOM *, VectorXd &)> get_output_ptr) { a.set_get_output(target, [get_output_ptr](SOM &som, VectorXd &vec) -> VectorXd {
                                                                                                                      return get_output_ptr(&som, vec);
                                                                                                                  }); })
        // Pointer to reference conversion required
        .def("set_train_cb", [](DeepSOM &a, int target, function<void(SOM * som, int t)> train_cb_ptr) { a.set_train_cb(target, [train_cb_ptr](SOM &som, int t) {
                                                                                                             return train_cb_ptr(&som, t);
                                                                                                         }); })
        .def("test", [](DeepSOM &a, VectorXd &to_test, function<VectorXd(SOM *, VectorXd &)> get_output_ptr) -> VectorXd { return a.test(to_test, [get_output_ptr](SOM &som, VectorXd &vec) -> VectorXd {
                                                                                                                               return get_output_ptr(&som, vec);
                                                                                                                           }); })
        .def("test_inputs", &DeepSOM::test_inputs)
        // DeepSOM needs to lives longer than the returned SOM
        .def("get_SOM", &DeepSOM::get_SOM, py::return_value_policy::reference_internal)
        .def("get_root", &DeepSOM::get_root)
        .def("get_node_num", &DeepSOM::get_node_num)
        .def(py::pickle([](const DeepSOM &p) {
                vector<py::tuple> SOMs;
                vector<size_t> ti;

                for (int i = 0; i < p.get_node_num(); i++){
                    // Cast from the internal SOM* to Map2d*
                    Map2d* m2d = dynamic_cast<Map2d*>(&p.get_SOM(i));
                    // Store the type of SOM used
                    ti.emplace_back(typeid(p.get_SOM(i)).hash_code());
                    if(m2d){
                        SOMs.push_back(pickle_Map2d(*m2d));
                    }else{
                        // This code is currently unreachable, as only Map2ds exist
                        __builtin_unreachable();
                    }
                }
                return py::make_tuple(p.get_t_lim(),
                                      p.get_adj(),
                                      SOMs,
                                      p.get_node_num(),
                                      ti); }, [](py::tuple t) {
                int node_num = t[3].cast<int>();
                DeepSOM* p = new DeepSOM(t[0].cast<int>());
                vector<py::tuple> SOMs = t[2].cast<vector<py::tuple>>();
                vector<size_t> ti = t[4].cast<vector<size_t>>();

                for (int i = 0; i < node_num; i++){
                    SOM* som;
                    // Check which type of SOM was originally created
                    if(ti[i] == type_index(typeid(MapRect)).hash_code()){
                        som = unpickle_Map2d<MapRect>(SOMs[i]);
                    }else if(ti[i] == type_index(typeid(MapHex)).hash_code()){
                        som = unpickle_Map2d<MapHex>(SOMs[i]);
                    }else{
                        __builtin_unreachable();
                    }
                    p->add_SOM(som);
                }
                // Manually add link based on adjacency matrix
                vector<vector<int>> adj = t[1].cast<vector<vector<int>>>();
                p->link_from_adj(adj);
                return p; }));

    py::class_<LVQ>(m, "LVQ")
        .def(py::init<int, int, int, double, double>(), "t_lim"_a, "inp_dim"_a, "total_class"_a, "alpha"_a = 1, "l"_a = 0)
        .def("train", &LVQ::train)
        .def("test", &LVQ::test)
        .def("predict", [](LVQ &a, vector<VectorXd> data) {
            vector<int> preds;
            for (int i = 0; i < (int)data.size(); i++) {
                preds.emplace_back(a.test(data[i]));
            }
            return preds;}) 
        //.def("predict", &LVQ::test)
        .def("fit", [](LVQ &a, vector<VectorXd> data, vector<int> class_v) {
            vector<pair<int, VectorXd>> merged;
            assert(class_v.size() == data.size());
            for (int i = 0; i < (int)class_v.size(); i++){
                merged.emplace_back(class_v[i], data[i]);
            }
            a.train(merged);});
}