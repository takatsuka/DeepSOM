import pytest
from unittest.mock import MagicMock, mock_open
import json

from app.src.py.som_viz_service import *


def _set_up():
    global test_contents
    test_contents = json.loads(
        open("tests/app_tests/resources/test_fashioncp.json").read())


def test_lerp():
    assert lerp(1, 1, 1) == 1


def test_bilinear(mocker):
    assert bilinear(1, 1, 0, 0, 1, 0) == 1


def test_som_visualisation_service_init(mocker):
    json_contents = {'weights': []}
    json.loads = MagicMock(return_value=json_contents)
    mocker.patch("builtins.open", mock_open(read_data="data"))
    service = SOMVisualizationService()

    assert service.filename == "/Volumes/Sweep SSD/comp3988pre/fashioncp.json"
    assert service.data == json_contents
    assert (service.weights == np.array([])).all()


def test_position(mocker):
    json_contents = {'weights': []}
    json.loads = MagicMock(return_value=json_contents)
    mocker.patch("builtins.open", mock_open(read_data="data"))
    position_service = SOMVisualizationService()
    position_service.data = test_contents
    position_service.weights = np.array(test_contents["weights"])
    assert any(position_service.position(1, 1))


def test_get_dim(mocker):
    json_contents = {'weights': [[1, 1], [1, 1]], 'w': 2, 'h': 2}
    json.loads = MagicMock(return_value=json_contents)
    mocker.patch("builtins.open", mock_open(read_data="data"))
    dim_service = SOMVisualizationService()
    assert dim_service.get_dim() == 2


_set_up()
