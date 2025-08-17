import pytest
import requests
from .data import Urls
from .courier_generator import register_new_courier_and_return_login_password, delete_courier

@pytest.fixture
def create_courier():
    courier_data = register_new_courier_and_return_login_password()
    if not courier_data:
        pytest.fail("Failed to create courier")
    
    login, password, firstName = courier_data
    payload = {"login": login, "password": password, "firstName": firstName}

    requests.post(Urls.COURIER_ENDPOINT, json=payload)
   
    yield login, password, firstName
    
    def delete_courier(courier_id):
            delete_courier(courier_id)