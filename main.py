import requests

keys = {
    "password": "qdasda",
    "user_id_phone": "123131452",
    "X-API-KEY": "1eads132rsa"
}

response = requests.get("https://httpbin.org/headers", headers=keys)
print(response.json())