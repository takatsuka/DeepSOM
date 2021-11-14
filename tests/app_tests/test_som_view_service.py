import pytest
from unittest.mock import Mock, MagicMock
import numpy as np

from app.src.py.som_view_service import SomViewService
from pysom.graph import GraphCompileError
from pysom.nodes.calibrate import Calibrate
from pysom.nodes.som import SOM


def setup_function():
    global service
    global mock_database
    mock_database = Mock()
    service = SomViewService(mock_database)


def test_init():
    assert service.ds == mock_database
    assert service.input_key is None
    assert service.som is None
    assert service.cal is None
    assert service.links is None
    assert service.nodes is None


def test_generate_som_nodes():
    mock_som = MagicMock(spec=SOM)
    mock_som.size = 2
    service.som = mock_som
    assert service.generate_nodes() == [{'id': 0}, {'id': 1}, {
        'id': 2}, {'id': 3}]


def test_generate_calibrate_nodes():
    mock_som = MagicMock(spec=SOM)
    mock_som.size = 1
    service.som = mock_som
    mock_calibrate = Mock()
    mock_calibrate.logit.return_value = np.array([[1, 1, 1]])
    mock_calibrate.get_output.return_value = {
        (1, 1): []
    }
    service.cal = mock_calibrate
    service.generate_nodes()
    assert service.nodes == [{'c': '#5dffff', 'id': 0, 'l': ''}]


def test_rect_links(mocker):
    mock_som = MagicMock(spec=SOM)
    mock_som.get_weights.return_value = [1, 1, 1, 1]
    mock_som.size = 2
    service.som = mock_som
    assert service.rect_links() == [
        {
            'source': 0, 'target': 1, 'value': 0.0}, {
            'source': 2, 'target': 3, 'value': 0.0}, {
                'source': 0, 'target': 2, 'value': 0.0}, {
                    'source': 1, 'target': 3, 'value': 0.0}]


def test_set_input_bad_data():
    mock_database.get_object_data.return_value = None
    actual = service.set_input("fake key")
    assert not actual['status'] and actual['msg'] == 'Input data does not exist.'

    mock_database.get_object_data.return_value = "fake data"
    actual = service.set_input("another fake key")
    assert not actual['status'] and actual['msg'] == 'Input data is neither a SOM node or Calibrate node.'


def test_set_input_bad_nodes():
    mock_som = Mock(spec=SOM)
    mock_database.get_object_data.return_value = mock_som
    service.rect_links = MagicMock(return_value="some links")
    service.generate_nodes = MagicMock(
        return_value=None, side_effect=Exception)
    actual = service.set_input("key")
    assert not actual['status']


def test_set_input_som_success():
    mock_som = Mock(spec=SOM)
    mock_database.get_object_data.return_value = mock_som
    service.rect_links = MagicMock(return_value="some links")
    service.generate_nodes = MagicMock(return_value=None)
    actual = service.set_input("key")
    assert not actual['status'] and actual['msg'] == "key"
    assert service.links == "some links"
    assert service.som == mock_som


def test_set_input_calibrate_success():
    mock_calibrate = Mock(spec=Calibrate)
    mock_calibrate.get_input.return_value = "a som"
    mock_database.get_object_data.return_value = mock_calibrate
    service.rect_links = MagicMock(return_value="some links")
    service.generate_nodes = MagicMock(return_value=None)
    actual = service.set_input("key")
    assert actual['status'] and actual['msg'] == "key"
    assert service.links == "some links"
    assert service.som == "a som"
    assert service.cal == mock_calibrate


def test_get_som_viz_data():
    actual = service.get_som_viz_data()
    assert not actual['status'] and actual['msg'] == 'Not available'

    service.nodes = "some nodes"
    service.links = "some links"
    actual = service.get_som_viz_data()
    assert actual['status'] and actual['msg'] == "Ok"
    assert actual['obj']['links'] == "some links"
    assert actual['obj']['nodes'] == "some nodes"
