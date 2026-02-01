import configuration
import requests
import data

# === Funciones helper ===
def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

def post_products_kits(products_ids):
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
                         json=products_ids,
                         headers=data.headers)

# === Tests ===
def test_get_users_table():
    response = get_users_table()
    assert response.status_code == 200

def test_post_new_user():
    response = post_new_user(data.user_body)
    response_body = response.json()
    print(f"\nCódigo: {response.status_code}")
    print(f"Cuerpo: {response_body}")
    assert response.status_code == 201

def test_post_products_kits():
    response = post_products_kits(data.product_ids)
    response_body = response.json()
    print(f"\nCódigo: {response.status_code}")
    print(f"Kits: {response_body}")
    assert response.status_code == 200