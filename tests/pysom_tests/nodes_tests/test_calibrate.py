import numpy as np
from pysom.nodes.calibrate import Calibrate
from pysom.nodes.som import SOM
from pysom.graph import Graph
import pytest


@pytest.fixture()
def g_cal_test():
    g = Graph()
    som = g.create(SOM, props={'size': 4, 'dim': 4})
    g.connect(g.start, som, 1)
    t = np.array([[0, 1, 1, 0]])  # cat
    cal = g.create(Calibrate, props={'labels': ['dog', 'monkey', 'human', 'unicorn'], 'test': t})
    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)
    dat = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 0]])
    g.set_input(dat)
    yield {'graph': g, 'cal': cal}


@pytest.fixture()
def g_cal():
    g = Graph()
    som = g.create(SOM, props={'size': 2, 'dim': 4})
    g.connect(g.start, som, 1)
    cal = g.create(Calibrate, props={'labels': ['dog', 'monkey', 'human', 'unicorn']})
    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)
    dat = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 1]])
    g.set_input(dat)
    yield {'graph': g, 'cal': cal}


def test_get_output(g_cal, g_cal_test):
    g, cal = g_cal['graph'], g_cal['cal']
    assert isinstance(g.find_node(cal).get_output(slot=0), Calibrate)
    g.find_node(cal).get_output(slot=1)
    g_test, cal_test = g_cal_test['graph'], g_cal_test['cal']
    label = g_test.find_node(cal_test).get_output(slot=1)
    assert label == ['dog']


def test_cal_str(g_cal):
    g, cal = g_cal['graph'], g_cal['cal']
    assert g.find_node(cal).__str__() == "Calibrate 4"
    assert str(g.find_node(cal)) == "Calibrate 4"


def test_check_slot(g_cal):
    g, cal = g_cal['graph'], g_cal['cal']
    assert not g.find_node(cal).check_slot(slot=2)
    assert g.find_node(cal).check_slot(slot=1)
    assert g.find_node(cal).check_slot(slot=0)


@pytest.fixture()
def g_cal_default():
    g = Graph()
    som = g.create(SOM, props={'size': 4, 'dim': 4})
    g.connect(g.start, som, 1)
    t = np.array([[9, 9, 9, 9], [0, 0, 0, 0]])
    cal = g.create(Calibrate, props={'labels': ['dog', 'dog', 'dog', 'dog'], 'test': t})
    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)
    dat = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 1]])
    g.set_input(dat)
    yield {'graph': g, 'cal': cal}


def test_default(g_cal_default):
    g, cal = g_cal_default['graph'], g_cal_default['cal']
    label = g.find_node(cal).get_output(slot=1)
    assert label == ['dog', 'dog']
