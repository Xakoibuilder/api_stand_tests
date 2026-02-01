import test_sender_stand_request as sender_stand_request
import data


def get_user_body(first_name):
    """Genera cuerpo de solicitud con nombre personalizado"""
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    """Validación para nombres VÁLIDOS (2-15 letras latinas)"""
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1


def negative_assert_symbol(first_name):
    """
    Validación para nombres INVÁLIDOS (símbolos/longitud incorrecta)
    Verifica que la API rechace correctamente el nombre con código 400
    """
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400

    expected_message = "Has introducido un nombre de usuario no válido. El nombre solo puede contener letras del alfabeto latino, la longitud debe ser de 2 a 15 caracteres."
    assert response.json()["message"] == expected_message


def negative_assert_no_firstname(user_body):
    """
    Validación para solicitudes SIN firstName (falta o vacío)
    Verifica que la API rechace correctamente con código 400
    """
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400

    expected_message = "No se han aprobado todos los parámetros requeridos"
    assert response.json()["message"] == expected_message


# === TESTS POSITIVOS ===
def test_create_user_2_letter_in_first_name_get_success_response():
    """Prueba 1: Nombre permitido de 2 caracteres"""
    positive_assert("Aa")
    print("\n✅ Prueba 1 PASSED: Nombre de 2 caracteres aceptado")


def test_create_user_15_letter_in_first_name_get_success_response():
    """Prueba 2: Nombre permitido de 15 caracteres"""
    positive_assert("Aaaaaaaaaaaaaaa")
    print("\n✅ Prueba 2 PASSED: Nombre de 15 caracteres aceptado")


# === TESTS NEGATIVOS ===
def test_create_user_1_letter_in_first_name_get_error_response():
    """Prueba 3: Nombre NO permitido de 1 caracter"""
    negative_assert_symbol("A")
    print("\n✅ Prueba 3 PASSED: Nombre de 1 caracter rechazado correctamente")


def test_create_user_16_letter_in_first_name_get_error_response():
    """Prueba 4: Nombre NO permitido de 16 caracteres"""
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")
    print("\n✅ Prueba 4 PASSED: Nombre de 16 caracteres rechazado correctamente")


def test_create_user_has_space_in_first_name_get_error_response():
    """Prueba 5: Nombre con espacio NO permitido"""
    negative_assert_symbol("A Aaa")
    print("\n✅ Prueba 5 PASSED: Nombre con espacio rechazado correctamente")


def test_create_user_has_special_symbol_in_first_name_get_error_response():
    """Prueba 6: Nombre con carácter especial NO permitido"""
    negative_assert_symbol("\"№%@\\,")
    print("\n✅ Prueba 6 PASSED: Nombre con caracteres especiales rechazado correctamente")


def test_create_user_has_number_in_first_name_get_error_response():
    """Prueba 7: Nombre con número NO permitido"""
    negative_assert_symbol("123")
    print("\n✅ Prueba 7 PASSED: Nombre con números rechazado correctamente")


def test_create_user_no_first_name_get_error_response():
    """Prueba 8: Error - La solicitud no contiene el parámetro 'firstName'"""
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)
    print("\n✅ Prueba 8 PASSED: Solicitud sin firstName rechazada correctamente")


def test_create_user_empty_first_name_get_error_response():
    """Prueba 9: Error - El parámetro 'firstName' está vacío"""
    user_body = data.user_body.copy()
    user_body["firstName"] = ""
    negative_assert_no_firstname(user_body)
    print("\n✅ Prueba 9 PASSED: Solicitud con firstName vacío rechazada correctamente")


def test_create_user_number_type_first_name_get_error_response():
    """Prueba 10: Error - El parámetro 'firstName' tiene tipo de dato numérico"""
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    print("\n✅ Prueba 10 PASSED: Solicitud con firstName tipo numérico rechazada correctamente")