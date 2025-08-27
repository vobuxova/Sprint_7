import requests
import pytest
import allure
from ..data import Urls, Order

@allure.feature("Создание заказа и просмотр списка заказов")
class TestOrder:
    @allure.title("Создание заказа")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None  
    ])
    def test_create_order(self, color):
        payload = Order.order_data
        if color:
            payload["color"] = color
        
        response = requests.post(Urls.ORDER_ENDPOINT, json=payload)
        
        assert response.status_code == 201
        assert 'track' in response.json()
    
    @allure.title("Просмотр списка заказов")
    def test_get_orders_list(self):
        response = requests.get(Urls.ORDER_ENDPOINT)
        
        assert response.status_code == 200
        assert 'orders' in response.json()
        assert isinstance(response.json()['orders'], list)