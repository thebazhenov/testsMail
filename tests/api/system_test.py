import pytest

from services.urls import API_URL
from services.api.system import System
from services.api.system.models import ChecksReadiness

class TestSystem:

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(cls):
        cls.system_api = System(base_url=API_URL)


    def test_check_greenmail_readiness(self):
        response = self.system_api.checks_greenmail_readiness()
        assert response.status_code == 200
        model = ChecksReadiness(**response.json())
        assert model.message == "Service running"

