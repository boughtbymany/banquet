import pytest

from banquet.builder import build_spec_for_routes


@pytest.fixture
def routes():
    return [["get:/example:test_function"], ["post:/another:test_other_function"]]


@pytest.fixture
def valid_spec():
    return {
        "paths": {
            "/example": {"get": {"x-handler": "test_function"}},
            "/another": {"post": {"x-handler": "test_other_function"}},
        }
    }


def test_builder_creates_valid_spec(routes, valid_spec):
    assert build_spec_for_routes(routes) == valid_spec
