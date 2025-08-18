import requests
import random
import string
import allure
from ..data import Urls, Message
from ..courier_generator import register_new_courier_and_return_login_password, delete_courier

@allure.feature("Создание и авторизация курьера")
class TestCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string
    
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
    
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        login_payload = {"login": login, "password": password}
        login_response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=login_payload)
        courier_id = login_response.json().get('id')
        delete_courier(courier_id)
    
    @allure.title("Создание существующего курьера")
    def test_create_duplicate_courier(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        assert response.status_code == 409
        assert Message.login_error in response.json().get('message', '')
    
    @allure.title("Создание курьера с уже существующим логином")    
    def test_create_courier_with_existed_login(self):
        login, password, first_name = register_new_courier_and_return_login_password()
        
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        
        payload = {"login": login, "password": 'password', "firstName": 'first_name'}
        response_with_existed_login = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        assert response_with_existed_login.status_code == 409
        assert Message.login_error in response_with_existed_login.json().get('message', '')
    
    @allure.title("Создание курьера без одного из обязательных полей")
    def test_create_courier_missing_field(self):
        payload = {"login": "testlogin", "firstName": "testname"}
        response = requests.post(Urls.COURIER_ENDPOINT, json=payload)
        assert response.status_code == 400
        assert Message.data_creation_error in response.json().get('message', '')
        
    @allure.title("Успешная авторизация курьера")
    def test_login_success(self, create_courier):
        login, password, _ = create_courier
        payload = {"login": login, "password": password}
        response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=payload)
        assert response.status_code == 200
        assert 'id' in response.json()
    
    @allure.title("Авторизация курьера при незаполненном обязательном поле")    
    def test_login_without_field_login(self, create_courier):
        _, password, _ = create_courier
        payload = {"password": password}
        response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=payload)
        assert response.status_code == 400
        assert  response.json()["message"] == Message.data_login_error
    
    @allure.title("Авторизация курьера с несуществующим паролем")    
    def test_login_with_wrong_password(self, create_courier):
        login, _, _ = create_courier
        payload = {"login": login, "password": '1234567'}
        response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=payload)
        assert response.status_code == 404
        assert  response.json()["message"] == Message.account_not_found
    
    @allure.title("Авторизация курьера с несуществующей парой логин-пароль")    
    def test_login_with_wrong_password_and_login(self):
        payload = {"login": '11111', "password": '1234567'}
        response = requests.post(Urls.COURIER_LOGIN_ENDPOINT, json=payload)
        assert response.status_code == 404
        assert  response.json()["message"] == Message.account_not_found