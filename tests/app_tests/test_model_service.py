import pytest
import numpy as np
from unittest.mock import Mock, MagicMock
from pysom.graph import GraphCompileError

import os
from app.src.py.model_service import ModelService


def setup_function():
    global model
    global mock_database
    mock_database = Mock()
    model = ModelService(mock_database)


def teardown_function():
    pass


def test_init():
    assert model.ds == mock_database
    assert model.input_key is None
    assert model.graph is None
    assert model.model_export is None
    assert model.model_output is None


def test_set_input():
    actual = model.set_input("fake key")
    assert model.input_key == "fake key"
    assert actual["status"] and actual["msg"] == "fake key"


def test_update_model():
    model.update_model("fake model")
    assert model.model_export == "fake model"


def test_compile_missing_export(mocker):
    actual = model.compile()
    assert not actual['status'] and actual['msg'] == "Missing model data?"


def test_compile_graph_compile_error():
    model.model_export = {
        "nodes": {
            "1": {
                "name": "Input",
                "id": 1,
                "x": 137,
                "y": 226,
                "props": {"dim": 3},
                "template": "inout"
            }
        }, "connections": [{"from": 1, "to": 1, "props": {"slot": 0, "order": 0}}], "i": 1}

    actual = model.compile()
    assert not actual['status'] and actual['msg'] == "Can not connect to node itself: 1"


def test_compile_graph_exception():
    model.model_export = "fake export"
    actual = model.compile()
    assert not actual['status']


def test_compile_success():
    model.model_export = {
        "nodes": {},
        "connections": {}
    }
    actual = model.compile()

    assert actual['status'] and actual['msg'] == "good"


def test_train_missing_components():
    actual = model.train()
    assert not actual['status'] and actual['msg'] == 'Model not present.'

    model.graph = "fake graph"
    actual = model.train()
    assert not actual['status'] and actual['msg'] == "Input data not set."


def test_train_invalid_components():
    mock_database.get_object_data = MagicMock(return_value=None)
    model.graph = "fake graph"
    model.input_key = "fake key"

    actual = model.train()
    assert not actual['status'] and actual['msg'] == 'Input data does not exist.'
    mock_database.get_object_data.called_only_once_with('fake key')


def test_train_exception(mocker):
    mock_database.get_object_data = MagicMock(return_value="fake data")
    model.input_key = "fake key"

    def throwGraphCompileError():
        raise GraphCompileError("help")

    def throwExceptionError():
        raise Exception("halp please")

    mock_graph = Mock()
    model.graph = mock_graph
    mock_graph.set_input = MagicMock()
    mock_graph.set_param = MagicMock()
    mock_graph.get_output = Mock(side_effect=throwGraphCompileError)

    actual = model.train()
    assert not actual['status'] and actual['msg'] == 'help'

    mock_graph.get_output = Mock(side_effect=throwExceptionError)
    actual = model.train()
    assert not actual['status'] and actual['msg'].startswith(
        "Error ocurred during evaluations:")


def test_train_success(mocker):
    mock_database.get_object_data = MagicMock(return_value="fake data")
    mock_graph = Mock()
    mocker.patch.object(mock_graph, "nodes", [])
    model.graph = mock_graph
    model.input_key = "fake key"
    mock_graph.set_input = MagicMock()
    mock_graph.set_param = MagicMock()
    mock_graph.get_output = MagicMock(return_value="fake output")

    actual = model.train()

    assert actual['status'] and actual["msg"] == "Training finished."
    assert model.model_output == "fake output"
    mock_graph.set_input.called_only_once()
    mock_graph.set_param.called_only_once()
    mock_graph.get_output.called_only_once()


def test_export_output(mocker):
    actual = model.export_output("name", False)
    assert not actual['status'] and actual['msg'] == 'Output data not avaliable. Train or Run the model first to generate data.'

    model.model_output = "fake output"
    actual = model.export_output("name", False)
    assert not actual['status'] and actual['msg'] == 'Output data format is not supported for export. Please check the output connection of your graph.'

    mock_database.save_object_data = MagicMock(return_value="name")
    model.model_output = np.array([1, 1, 1])

    actual = model.export_output("name", False)
    assert actual['status'] and actual['msg'] == 'name'
    mock_database.save_object_data.called_only_once_with(
        'matrix', 'name', model.model_output)

    actual = model.export_output("opaque name", True)
    assert actual['status'] and actual['msg'] == 'name'
    mock_database.save_object_data.called_only_once_with(
        'opaque', 'name', model.model_output)


def test_export_node():
    actual = model.export_node("name", 1)
    assert not actual['status'] and actual['msg'] == 'Output data not avaliable. Train or Run the model first to generate data.'

    model.model_output = "fake output"
    actual = model.export_node("name", 1)
    assert not actual['status'] and actual['msg'] == 'Model not present.'

    mock_graph_fail = Mock()
    mock_graph_fail.find_node.return_value = None
    model.graph = mock_graph_fail
    actual = model.export_node("name", 1)
    assert not actual['status'] and actual['msg'] == 'Requested Node does not present.'

    mock_graph_success = Mock()
    mock_graph_success.find_node.return_value = "real node"
    mock_database.save_object_data.return_value = "real key"
    model.graph = mock_graph_success
    actual = model.export_node("name", 1)

    assert actual['status'] and actual['msg'] == "real key"
    mock_database.save_object_data.called_only_once_with(
        'opaque', 'name', 'real node')


def test_debug_output_str():
    actual = model.debug_output_str()
    assert not actual['status'] and actual['msg'] == 'Output data not avaliable. Train or Run the model first to generate data.'

    model.model_output = "fake output"
    actual = model.debug_output_str()
    assert actual['status'] and actual['msg'] == 'fake output'
