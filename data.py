class Urls:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
    COURIER_ENDPOINT = f"{BASE_URL}/courier"
    COURIER_LOGIN_ENDPOINT = f"{BASE_URL}/courier/login"
    ORDER_ENDPOINT = f"{BASE_URL}/orders"
    
class Order:
    order_data = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Address 1",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 5,
        "deliveryDate": "2025-08-18",
        "comment": "Test comment"
    }
    
    
class Message:
    login_error = "Этот логин уже используется"
    data_creation_error = "Недостаточно данных"
    data_login_error = "Недостаточно данных для входа" 
    account_not_found = "Учетная запись не найдена"