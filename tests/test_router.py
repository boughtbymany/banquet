import re
from unittest.mock import patch, MagicMock
import pytest

from banquet.router import BanquetRouter

@pytest.fixture
def simple_open_api_spec():
    return {
        "paths": {
            "/example": {"get": {"x-handler": "test_function"}},
            "/another": {
                "post": {"x-handler": "test_other_function"},
                "delete": {"x-handler": "test_delete_function"},
            },
        }
    }

@pytest.fixture
def dynamic_open_api_spec():
    return {
        "paths": {
            "/example/{id}": {"get": {"x-handler": "test_function"}},
            "/another/{id}/{name}": {
                "post": {"x-handler": "test_other_function"},
            },
        }
    }

@pytest.fixture
def function_dir():
    return "functions/"  



@patch("banquet.router.BanquetHandler", MagicMock({}))
class TestRouter:
    def test_router_setup_from_openapi(self, simple_open_api_spec, function_dir):
        router = BanquetRouter(simple_open_api_spec, function_dir)
        assert len(router.routes["GET"].values()) == 1
        assert len(router.routes["POST"].values()) == 1
        assert len(router.routes["DELETE"].values()) == 1
        
    def test_router_setup_from_openapi_dynamic_urls(self, dynamic_open_api_spec, function_dir):
        router = BanquetRouter(dynamic_open_api_spec, function_dir)
        assert len(router.routes["GET"].values()) == 1
        url_pattern = list(router.routes["GET"].keys())[0]
        assert isinstance(url_pattern, re.Pattern) == True

    @patch("banquet.router.BanquetHandler")
    def test_router_resolves(self, mock_banquet_handler, simple_open_api_spec, function_dir):
        mock_banquet_handler.return_value = {"x-handler": "test_function"}
        router = BanquetRouter(simple_open_api_spec, function_dir)
        conf, params = router.resolve("GET", "/example")
        assert conf["x-handler"] == "test_function"
        assert params is None
