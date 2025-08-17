import requests
from ..data import Urls
from ..courier_generator import register_new_courier_and_return_login_password

class TestCourier:

    def test_create_courier_success(self, create_courier):
        login, password, firstName = create_courier
        assert login and password and firstName, "Courier not created"
    
    def test_create_duplicate_courier(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "First creation failed"
        login, password, first_name = courier_data
    
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json().get('message', '')
        
    def test_create_courier_with_existed_login(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "First creation failed"
        login, _, _ = courier_data
    
        payload = {"login": login, "password": 'password', "firstName": 'first_name'}
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json().get('message', '')
    
    def test_create_courier_missing_field(self):
        payload = {"login": "testlogin", "firstName": "testname"}
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get('message', '')
    
    def test_create_courier_returns_ok_true(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Creation failed"
        payload = {"login": courier_data[0], "password": courier_data[1], "firstName": courier_data[2]}
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        if response.status_code == 201:
            assert response.json() == {"ok": True}
    
    def test_login_success(self, create_courier):
        login, password, _ = create_courier
        payload = {"login": login, "password": password}
        response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=payload)
        assert response.status_code == 200
        assert 'id' in response.json()
        
    def test_login_without_field_login(self, create_courier):
        _, password, _ = create_courier
        payload = {"password": password}
        response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=payload)
        assert response.status_code == 400
        assert  response.json()["message"] == "Недостаточно данных для входа" 
        
    def test_login_with_wrong_password(self, create_courier):
        login, _, _ = create_courier
        payload = {"login": login, "password": '1234567'}
        response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=payload)
        assert response.status_code == 404
        assert  response.json()["message"] == "Учетная запись не найдена"
        
    def test_login_with_wrong_password_and_login(self):
        payload = {"login": '11111', "password": '1234567'}
        response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=payload)
        assert response.status_code == 404
        assert  response.json()["message"] == "Учетная запись не найдена"