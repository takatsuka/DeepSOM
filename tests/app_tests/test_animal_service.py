import pytest
from unittest.mock import Mock, MagicMock

from app.src.py.animal_service import AnimalService
from pysom.nodes.calibrate import Calibrate
from pysom.nodes.som import SOM
import traceback


def setup_function():
    global service
    global mock_datastore
    mock_datastore = Mock()
    service = AnimalService(mock_datastore)


def test_init():
    assert service.ds == mock_datastore
    assert service.input_key == None
    assert service.som == None
    assert service.cal == None
    assert service.animals == None


def test_set_input_fail():
    mock_datastore.get_object_data.return_value = None
    actual = service.set_input("fake key")
    assert actual['status'] == False and actual['msg'] == 'Input data does not exist.'

    mock_datastore.get_object_data.return_value = "fake data"
    actual = service.set_input("fake key")
    assert actual['status'] == False and actual['msg'] == 'Input data is neither a SOM node or Calibrate node.'


def test_set_input_exception(mocker):
    mock_som = Mock(spec=SOM)
    mock_som.size = 1
    mock_datastore.get_object_data.return_value = mock_som
    mocker.patch("traceback.format_exc").return_value = "stacktrace"
    actual = service.set_input("fake key")
    assert actual['status'] == False and actual['msg'] == "stacktrace"


def test_set_calibrate_input():
    mock_som = Mock(spec=SOM)
    mock_som.size = 1
    mock_calibrate = Mock(spec=Calibrate)
    mock_calibrate.get_input.return_value = mock_som
    mock_calibrate.get_output.return_value = {
        (0, 0): {
            "animal 1": 1,
            "animal 2": 2
        }
    }
    mock_datastore.get_object_data.return_value = mock_calibrate

    actual = service.set_input("key")
    assert actual['status'] == True and actual['msg'] == ""
    assert service.animals == [[['animal 1', 'animal 2']]]


def test_get_animal_data():
    actual = service.get_animal_data()
    assert actual['status'] == False and actual['msg'] == 'Not available'

    service.animals = "animals"
    actual = service.get_animal_data()
    assert actual['status'] == True and actual['msg'] == 'Ok'
    assert actual['obj'] == 'animals'
