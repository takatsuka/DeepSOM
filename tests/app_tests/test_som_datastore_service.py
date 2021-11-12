import pytest
import json
import filecmp
import os
import webview
import numpy as np
from unittest.mock import Mock, MagicMock

from app.src.py.som_datastore_service import SOMDatastoreService

def setup_function():
    global ds
    ds = SOMDatastoreService()

def teardown_function():
    pass

def test_init():
    assert len(ds.data_instances) == 0
    assert ds.ws_path == None
    assert ds.ws_name == "lol"
    assert np.all(ds.loaders["matrix"]([1, 1, 1]))
    assert ds.loaders["model"](1) == 1
    assert ds.dumpers["matrix"](np.array([1, 1, 1])) == [1, 1, 1]
    assert ds.dumpers["model"](1) == 1
    assert np.any((ds.importers["matrix"]([[3], np.float64, "AAAAAAAA8D8AAAAAAAAAQAAAAAAAAAhA"])))
    assert ds.importers["model"](1) == 1

def test_ensure_unique():
    assert ds.ensure_unique("not exist") == "not exist"
    ds.save_object("exists", "matrix", [], False)
    assert ds.ensure_unique("exists") == "exists_(1)"

    ds.save_object("exists_(1)", "matrix", [], False)
    assert ds.ensure_unique("exists") == "exists_(2)"


def test_open_file_fail(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["fake_file"]
    mocker.patch.object(webview, "windows", [mock_window])

    mock_path = Mock()
    mock_path.exists.return_value = False
    mocker.patch.object(os, "path", mock_path)

    filepath = ds.open_file()
    assert filepath == None

    mock_window.create_file_dialog.return_value = []
    mocker.patch.object(webview, "windows", [mock_window])

    filepath = ds.open_file()
    assert filepath == None

def test_open_file_success(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["real_file"]
    mocker.patch.object(webview, "windows", [mock_window])

    mock_path = Mock()
    mock_path.exists.return_value = True
    mocker.patch.object(os, "path", mock_path)

    filepath = ds.open_file()
    mock_window.create_file_dialog.assert_called_once()
    assert filepath == "real_file"

def test_import_data_from_csv_fail(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = None
    mocker.patch.object(webview, "windows", [mock_window])
    unique_spy = mocker.spy(ds, "ensure_unique")
    file_spy = mocker.spy(ds, "open_file")
    
    actual = ds.import_data_from_csv()

    assert actual == None
    unique_spy.assert_not_called()
    file_spy.assert_called_once()

def test_import_data_from_csv_duplicate(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["tests/app_tests/resources/test_csv.txt"]
    mocker.patch.object(webview, "windows", [mock_window])

    ds.save_object("test_csv.txt", "matrix", [1, 1, 1], False)
    unique_spy = mocker.spy(ds, "ensure_unique")
    file_spy = mocker.spy(ds, "open_file")
    actual = ds.import_data_from_csv()

    assert actual == "test_csv.txt_(1)"
    assert ds.get_object("test_csv.txt_(1)") == [[1.0, 1.0, 1.0]]
    unique_spy.assert_called_once()
    file_spy.assert_called_once()

def test_import_data_from_csv_success(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["tests/app_tests/resources/test_csv.txt"]
    mocker.patch.object(webview, "windows", [mock_window])
    unique_spy = mocker.spy(ds, "ensure_unique")
    file_spy = mocker.spy(ds, "open_file")

    actual = ds.import_data_from_csv()

    assert actual == "test_csv.txt"
    assert ds.get_object("test_csv.txt") == [[1.0, 1.0, 1.0]]
    unique_spy.assert_called_once()
    file_spy.assert_called_once()

    mock_window.create_file_dialog.return_value = ["tests/app_tests/resources/empty.txt"]
    mocker.patch.object(webview, "windows", [mock_window])
    assert ds.import_data_from_csv() == "empty.txt"

def test_import_json_fail(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = None
    mocker.patch.object(webview, "windows", [mock_window])
    unique_spy = mocker.spy(ds, "ensure_unique")
    file_spy = mocker.spy(ds, "open_file")

    actual = ds.import_json("model")
    assert(actual == None)
    unique_spy.assert_not_called()
    file_spy.assert_called_once()
    

def test_import_duplicate_json(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["tests/app_tests/resources/test_json.json"]
    mocker.patch.object(webview, "windows", [mock_window])
    
    ds.save_object("test_json.json", "model", "json object", False)
    unique_spy = mocker.spy(ds, "ensure_unique")
    file_spy = mocker.spy(ds, "open_file")
    actual = ds.import_json("model")

    assert actual == "test_json.json_(1)"
    unique_spy.assert_called_once()
    file_spy.assert_called_once()

def test_import_json_success(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["tests/app_tests/resources/test_json.json"]
    mocker.patch.object(webview, "windows", [mock_window])
    unique_spy = mocker.spy(ds, "ensure_unique")
    file_spy = mocker.spy(ds, "open_file")

    actual = ds.import_json("model")

    expected = {
        "test": "true"
    }
    assert actual == "test_json.json"
    assert ds.get_object(actual) == expected
    unique_spy.assert_called_once()
    file_spy.assert_called_once()

def test_save_json():
    ds.save_json("some key", "model", "some json object")
    assert ds.get_object("some key") == "some json object"

    ds.save_json("some key", "model", "another json object")
    assert ds.get_object("some key") == "some json object"
    assert ds.get_object("some key_(1)") == "another json object"

def test_save_object():
    ds.save_json("some key", "model", "some object")
    descriptor = ds.save_object("some key", "model", "another object", False)
    assert descriptor != "some key"
    assert ds.get_object(descriptor) == "another object"

    descriptor = ds.save_object("some key", "model", "another one", True)
    assert descriptor == "some key"
    assert ds.get_object(descriptor) == "another one"

    descriptor = ds.save_object("bad key", "bad type", "object", False)
    assert descriptor == None

def test_get_object():
    assert ds.get_object("fake key") == None

    ds.save_object_data("bad type", "bad key", "object")
    assert ds.get_object("bad key") == None

    ds.save_object("fake key", "model", "object", False)
    assert ds.get_object("fake key") == "object"

def test_fetch_objects():
    ds.save_object("key 1", "model", "model1", False)
    ds.save_object("key 2", "matrix", [], False)
    ds.save_object("key 3", "model", "model3", False)
    
    actual = ds.fetch_objects('')
    assert len(actual) == 3
    assert ("key 1" in actual and "key 2" in actual) and "key 3" in actual

    actual = ds.fetch_objects("model")
    assert "key 1" in actual and "key 3" in actual

    actual = ds.fetch_objects("matrix")
    assert "key 2" in actual

    actual = ds.fetch_objects("fake type")
    assert actual == []

def test_remove_object():
    ds.save_object("key 1", "model", "model1", False)
    ds.remove_object("fake key")
    assert ds.get_object("key 1") == "model1"

    ds.remove_object("key 1")
    assert ds.get_object("key 1") == None

def test_rename_object():
    ds.save_object("key", "model", "model", False)
    ds.save_object("another key", "model", "another model", False)

    actual = ds.rename_object("fake key", "new key")
    assert actual["status"] == False and actual["msg"] == "Object does not exist."

    actual = ds.rename_object("key", "another key")
    assert actual["status"] == False and actual["msg"] == "New key already exists."

    actual = ds.rename_object("key", "")
    assert actual["status"] == False and actual["msg"] == "Gotcha hacker."

    actual = ds.rename_object("key", "key")
    assert actual["status"] == True and actual["msg"] == "key"
    assert ds.get_object("key") == "model"

    actual = ds.rename_object("key", "new key")
    assert actual["status"] == True and actual["msg"] == "new key"
    assert ds.get_object("key") == None
    assert ds.get_object("new key") == "model"

def test_fetch_object_repr():
    ds.save_object("key", "matrix", [1, 2, 3], False)

    actual = ds.fetch_object_repr("fake key")
    assert actual["status"] == False and actual["msg"] == "Object does not exist."

    actual = ds.fetch_object_repr("key")
    assert (actual["status"] == True and actual["type"] == "<class 'numpy.ndarray'>") and actual["repr"] == "array([1., 2., 3.])"

def test_current_workspace():
    assert ds.current_workspace_name() == "lol"

def test_load_workspace_fail():
    ds.open_file = MagicMock(return_value=None)
    assert ds.load_workspace() == None

def test_load_workspace_success(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = ["tests/app_tests/resources/test_workspace.json"]
    mocker.patch.object(webview, "windows", [mock_window])
    file_spy = mocker.spy(ds, "open_file")
    close_spy = mocker.spy(ds, "close_all_instances")

    ds.load_workspace()

    expected = {
        "should save 1": {
            "type": "matrix",
            "content": np.array([1, 2, 3])
        },
        "should save 2:": {
            "type": "model",
            "content": "content"
        }
    }
    assert ds.ws_name == "test_workspace.json"
    assert ds.ws_path == "tests/app_tests/resources/test_workspace.json"
    file_spy.assert_called_once()
    close_spy.assert_called_once()

def test_new_workspace():
    ds.new_workspace()
    assert ds.ws_name == "untitled"
    assert ds.ws_path == None
    assert len(ds.data_instances) == 0

def test_save_current_workspace(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = "tests/app_tests/resources/test_workspace"
    mocker.patch.object(webview, "windows", [mock_window])
    
    spy = mocker.spy(ds, "save_workspace")
    ds.save_current_workspace()

    spy.assert_called_once()

def test_save_workspace_as(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = "tests/app_tests/resources/test_workspace"
    mocker.patch.object(webview, "windows", [mock_window])
    
    spy = mocker.spy(ds, "save_workspace")
    ds.save_workspace_as()

    spy.assert_called_once()
    assert ds.ws_path == "tests/app_tests/resources/test_workspace"

def test_save_workspace(mocker):
    mock_window = Mock()
    mock_window.create_file_dialog.return_value = "tests/app_tests/resources/test_workspace_actual.json"
    mocker.patch.object(webview, "windows", [mock_window])

    ds.save_object("should save 1", "matrix", [1, 2, 3], False)
    ds.save_object("should save 2", "model", "content", False)
    ds.save_object_data("opaque", "should not save", "SOM object")

    ds.save_workspace()

    assert ds.ws_name == "test_workspace_actual.json"
    assert ds.ws_path == "tests/app_tests/resources/test_workspace_actual.json"
    assert filecmp.cmp("tests/app_tests/resources/test_workspace_actual.json", "tests/app_tests/resources/test_workspace_expected.json")

def test_get_object_data():
    ds.save_object("key", "matrix", [1, 2, 3], False)

    actual = ds.get_object_data("fake key")
    assert actual == None

    actual = ds.get_object_data("key")
    assert isinstance(actual, np.ndarray)

def test_save_object_data():
    ds.save_object_data("matrix", "new key", [1, 2, 3])
    assert ds.get_object_data("new key") == [1, 2, 3]

def test_close_all_instances():
    ds.close_all_instances()
    assert len(ds.data_instances) == 0

    