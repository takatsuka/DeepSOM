import pytest
from unittest.mock import Mock

from model_compiler import *
from pysom.graph import Graph
from pysom.nodes.som import dist_euclidean, nhood_gaussian

test_export = {"nodes": {"1": {"name": "Input", "id": 1, "x": 71, "y": 155, "props": {"dim": 3}, "template": "inout"}, "2": {"name": "Output", "id": 2, "x": 857, "y": 217, "props": {"dim": 2}, "template": "inout"}, "3": {"name": "SOM", "id": 3, "x": 274, "y": 85, "props": {"dim": 10, "shape": "rect", "inputDim": 3, "train_iter": 1000, "distance_func": "euclidean", "nhood_func": "gaussian", "sigma": 2, "lr": 0.7}, "template": "som"}, "4": {"name": "get_bmu_", "id": 4, "x": 509, "y": 355, "props": {"shape": "weights"}, "template": "get_bmu"}}, "connections": [{"from": 1, "to": 3, "props": {"slot": 1, "order": 0}}, {"from": 3, "to": 4, "props": {"slot": 0, "order": 0}}, {"from": 4, "to": 2, "props": {"slot": 1, "order": 0}}], "i": 4}
test_export_bad_link = {"nodes": {"1": {"name": "Input", "id": 1, "x": 101, "y": 200, "props": {"dim": 3}, "template": "inout"}}, "connections": [{"from": 1, "to": 1, "props": {"slot": 0, "order": 0}}],  "i": 1}
test_export_missing_node = {"nodes": {"1": {"name": "Input", "id": 1, "x": 101, "y": 200, "props": {"dim": 3}, "template": "inout"}}, "connections": [{"from": 1, "to": 1, "props": {"slot": 0, "order": 0}}],  "i": 1}
test_export_bad_template = {"nodes": {"1": {"name": "Input", "id": 1, "x": 101, "y": 200, "props": {"dim": 3}, "template": "inout"}, "2": {"name": "Output", "id": 2, "x": 600, "y": 201, "props": {"dim": 2}, "template": "fake template"}}, "connections": [{"from": 1, "to": 2, "props": {"slot": 0, "order": 0}}],  "i": 2}

som_test_props = {"dim": 10, "shape": "rect", "inputDim": 3, "train_iter": 1000, "distance_func": "euclidean", "nhood_func": "gaussian", "sigma": 2, "lr": 0.7}
bmu_test_props = {"shape": "weights"}
test_props = {"selections": [{"type": "idx", "sel": [0, 1]}], "axis": 1}
calibrate_test_props = {"label_key": "fake key"}

def test_dist_props():
    assert dist_props(test_props) == {'selections': [(1, [0, 1])]}

def test_concat_props():
    assert concat_props(test_props) == {'axis': 1}

def test_som_props():
    props = som_props(som_test_props)
    assert props['size'] == 10
    assert props['dim'] == 3
    assert props['sigma'] == 2
    assert props['lr'] == 0.7
    assert props['n_iters'] == 1000
    assert props['hexagonal'] == False
    assert props['dist'] == dist_euclidean
    assert props['nhood'] == nhood_gaussian

def test_bmu_props():
    assert bmu_props(bmu_test_props) == {'output': 'w'}

def test_calibrate_props():
    mock_datastore = Mock()
    mock_datastore.get_object_data.return_value = None
    with pytest.raises(GraphCompileError):
        calibrate_props(calibrate_test_props, mock_datastore, {'name': 'test'})

    mock_datastore.get_object_data.return_value = "Badly formatted data"
    with pytest.raises(GraphCompileError):
        calibrate_props(calibrate_test_props, mock_datastore, {'name': 'test'})

    mock_datastore.get_object_data.return_value = np.array([1, 1, 1])
    assert calibrate_props(calibrate_test_props, mock_datastore, {'name', 'test'})

def test_parse_dict_bad_node():
    with pytest.raises(GraphCompileError):
        parse_dict(test_export_missing_node, "fake datastore")

def test_parse_dict_bad_template():
    with pytest.raises(GraphCompileError):
        parse_dict(test_export_bad_template, "fake datastore")

def test_parse_dict_bad_connection():
    with pytest.raises(GraphCompileError):
        parse_dict(test_export_bad_link, "fake datastore")

def test_parse_dict_success():
    assert type(parse_dict(test_export, "fake datastore")) == Graph