import requests
import pytest
from ..data import Urls


@pytest.mark.parametrize("color", [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    None  
])
def test_create_order(color):
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Address 1",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 5,
        "deliveryDate": "2025-08-18",
        "comment": "Test comment"
    }
    if color:
        payload["color"] = color
    
    response = requests.post(Urls.ORDER_ENDPOINT, json=payload)
    
    assert response.status_code == 201
    assert 'track' in response.json()

def test_get_orders_list():
    response = requests.get(Urls.ORDER_ENDPOINT)
    
    assert response.status_code == 200
    assert 'orders' in response.json()
    assert isinstance(response.json()['orders'], list)