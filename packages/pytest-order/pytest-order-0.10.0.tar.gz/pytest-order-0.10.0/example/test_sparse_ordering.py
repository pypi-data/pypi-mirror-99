"""Test file showing the behavior of the --sparse-ordering option.
See https://pytest-dev.github.io/pytest-order/dev/#sparse-ordering
"""
import pytest


@pytest.mark.order(3)
def test_two():
    assert True


def test_three():
    assert True


def test_four():
    assert True


@pytest.mark.order(1)
def test_one():
    assert True
