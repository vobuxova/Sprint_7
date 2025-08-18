import pytest
import requests
from .data import Urls
from .courier_generator import register_new_courier_and_return_login_password, delete_courier

@pytest.fixture
def create_courier():
    login, password, first_name = register_new_courier_and_return_login_password()
    payload = {"login": login, "password": password, "firstName": first_name}

    requests.post(Urls.COURIER_ENDPOINT, json=payload)
   
    yield login, password, first_name
    
    login_payload = {"login": login, "password": password}
    login_response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=login_payload)
    courier_id = login_response.json().get('id')
    
    if courier_id:
        delete_courier(courier_id)