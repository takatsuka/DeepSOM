import pytest
from unittest.mock import Mock, MagicMock, mock_open
import webview
import json
import os

from som_scatterview_service import SOMScatterviewService

def setup_function():
    global service
    global mock_database
    mock_database = Mock()
    service = SOMScatterviewService(mock_database)

def test_init():
    assert service.cache == {
            "DATASET_PATH": None,
            "DATASET": None,
            "AXES": None,
            "WEIGHTS": None,
            "WEIGHTS_NODES": None,
            "WEIGHTS_EDGES": None
        }
    assert service.datastore == mock_database

def test_scatter_som_weights_by_training_epoch():
    assert service.update_scatter_som_weights_by_training_epoch(0) == None
    
    fake_weights = {
        'w': 2,
        'h': 2,
        'weightspb': {
            "0": [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]
        }
    }
    service.cache["WEIGHTS"] = fake_weights
    service.update_scatter_som_weights_by_training_epoch(0)
    assert service.cache['WEIGHTS_NODES'] == [
        {'x': 1.0, 'y': 1.0, 'z': 1.0},
        {'x': 1.0, 'y': 1.0, 'z': 1.0},
        {'x': 1.0, 'y': 1.0, 'z': 1.0},
        {'x': 1.0, 'y': 1.0, 'z': 1.0}
    ]
    assert service.cache["WEIGHTS_EDGES"] == [
        [{'x': 1.0, 'y': 1.0, 'z': 1.0}, {'x': 1.0, 'y': 1.0, 'z': 1.0}],
        [{'x': 1.0, 'y': 1.0, 'z': 1.0}, {'x': 1.0, 'y': 1.0, 'z': 1.0}],
        [{'x': 1.0, 'y': 1.0, 'z': 1.0}, {'x': 1.0, 'y': 1.0, 'z': 1.0}],
        [{'x': 1.0, 'y': 1.0, 'z': 1.0}, {'x': 1.0, 'y': 1.0, 'z': 1.0}]
    ]

def test_update_scatter_dataset():
    service.update_scatter_dataset([[1, 1, 1]])
    assert service.cache["DATASET"] == [{'x': 1.0, 'y': 1.0, 'z': 1.0, "id": 'point_0'}]

def test_get_scatter_som_weights():
    service.cache["WEIGHTS_NODES"] = "fake nodes"
    service.cache["WEIGHTS_EDGES"] = "fake edges"
    assert service.get_scatter_som_weights() == ["fake nodes", "fake edges"]

def test_get_scatter_dataset():
    service.cache["DATASET"] = "fake dataset"
    assert service.get_scatter_dataset() == "fake dataset"

def test_upload_scatter_weights_from_json_file_fail(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = None
    mocker.patch.object(webview, "windows", [mock_window])
    assert service.upload_scatter_weights_from_json_file() == None

    mock_window.create_file_dialog.return_value = []
    mocker.patch.object(webview, "windows", [mock_window])
    assert service.upload_scatter_weights_from_json_file() == None

    mock_window.create_file_dialog.return_value = ["fake json file"]
    mocker.patch.object(webview, "windows", [mock_window])
    mock_path = Mock()
    mock_path.exists.return_value = False
    mocker.patch.object(os, "path", mock_path)
    assert service.upload_scatter_weights_from_json_file() == None

def test_upload_scatter_weights_from_json_file_success(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["real json file"]
    mocker.patch.object(webview, "windows", [mock_window])
    mock_path = Mock()
    mock_path.exists.return_value = True
    mocker.patch.object(os, "path", mock_path)
    test_data = {'weights': [1, 1, 1]}
    json.loads = MagicMock(return_value=test_data)
    mocker.patch("builtins.open", mock_open(read_data="data"))
    service.update_scatter_som_weights_by_training_epoch = MagicMock()

    assert service.upload_scatter_weights_from_json_file() == 3

def test_upload_scatter_dataset_fail(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = None
    mocker.patch.object(webview, "windows", [mock_window])
    assert service.upload_scatter_dataset() == None

    mock_window.create_file_dialog.return_value = []
    mocker.patch.object(webview, "windows", [mock_window])
    assert service.upload_scatter_dataset() == None

    mock_window.create_file_dialog.return_value = ["fake csv file"]
    mocker.patch.object(webview, "windows", [mock_window])
    mock_path = Mock()
    mock_path.exists.return_value = False
    mocker.patch.object(os, "path", mock_path)
    assert service.upload_scatter_dataset() == None

def test_upload_scatter_dataset_success(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["real csv file"]
    mocker.patch.object(webview, "windows", [mock_window])
    mock_path = Mock()
    mock_path.exists.return_value = True
    mock_path.abspath.return_value = "absolute path to real file"
    mock_path.basename.return_value = "real file"
    mocker.patch.object(os, "path", mock_path)
    test_data = "1,1,1"
    json.loads = MagicMock(return_value=test_data)
    mocker.patch("builtins.open", mock_open(read_data="data"))
    service.update_scatter_dataset = MagicMock()

    assert service.upload_scatter_dataset() == "real file"
    assert service.cache["DATASET_PATH"] == "absolute path to real file"

def test_reset_datastore():
    service.cache["DATASET_PATH"] = "a path"
    service.resetDatastore()
    assert service.cache == {
            "DATASET_PATH": None,
            "DATASET": None,
            "AXES": None,
            "WEIGHTS": None,
            "WEIGHTS_NODES": None,
            "WEIGHTS_EDGES": None
        }