from base_class import BaseClass


class test_class(BaseClass):
    """Testing the MonitorBase class."""

    def __init__(self):
        pass

    def test_func1(self):
        return 5

    def test_func2(self, a=1, b=2):
        return a, b


def test_creation():
    """Testing the creation of the test_class object."""
    obj = test_class()
    assert obj is not None


def test_func1():
    """Testing the test_func1 method."""
    obj = test_class()
    assert obj.test_func1() == 5


def test_func2():
    """Testing the test_func2 method."""
    obj = test_class()
    assert obj.test_func2() == (1, 2)
    assert obj.test_func2(3, 4) == (3, 4)
