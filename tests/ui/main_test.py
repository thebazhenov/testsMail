import pytest
from conftest import base_test

@pytest.fixture(scope="function", autouse=False)
def delete_all_message(base_test):
    response = base_test.system.purges_all_mails()
    assert response.status_code == 200

class TestMainPage:
    pass