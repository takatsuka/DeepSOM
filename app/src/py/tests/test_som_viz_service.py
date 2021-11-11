import pytest
from unittest.mock import MagicMock, mock_open
import json

from som_viz_service import *


def test_lerp():
    assert lerp(1, 1, 1) == 1

def test_bilinear(mocker):
    assert bilinear(1, 1, 0, 0, 1, 0) == 1

def test_position(mocker):
    test_data = json.loads(open("tests/resources/test_fashion.json").read())
    json.loads = MagicMock(return_value=test_data)
    mocker.patch("builtins.open", mock_open(read_data="data"))
    service = SOMVisualizationService()

    assert any(service.position(1, 1))

def test_som_visualisation_service_init(mocker):
    json_contents = {'weights': [1, 1, 1]}
    json.loads = MagicMock(return_value=json_contents)
    mocker.patch("builtins.open", mock_open(read_data="data"))
    service = SOMVisualizationService()

    assert service.filename == "/Volumes/Sweep SSD/comp3988pre/fashioncp.json"
    assert service.data == json_contents
    assert (service.weights==np.array([1, 1, 1])).all()

def test_get_dim(mocker):
    json_contents = {'weights': [[1, 1], [1, 1]], 'w': 2, 'h': 2}
    json.loads = MagicMock(return_value=json_contents)
    mocker.patch("builtins.open", mock_open(read_data="data"))
    service = SOMVisualizationService()

    assert service.get_dim() == 2