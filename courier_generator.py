import requests
import random
import string
import allure
from .data import Urls

@allure.step("Создание данных для регистрации и логина курьера")
def register_new_courier_and_return_login_password():

    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
    
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return login, password, first_name

@allure.step("Удаление созданного курьера")
def delete_courier(courier_id):
    response = requests.delete(f'{Urls.COURIER_ENDPOINT}{courier_id}')
    return response