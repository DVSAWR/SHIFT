from fastapi.testclient import TestClient
import time

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_create_token():
    # positive
    user_name, password = "qwe", "password"
    response = client.put(f"http://127.0.0.1:8000/user/create_token?user_name={user_name}&password={password}")
    assert response.status_code == 200

    # wrong user_name
    user_name, password = "wrong_qwe", "password"
    response = client.put(f"http://127.0.0.1:8000/user/create_token?user_name={user_name}&password={password}")
    assert response.status_code == 400

    # wrong password
    user_name, password = "qwe", "wrong_password"
    response = client.put(f"http://127.0.0.1:8000/user/create_token?user_name={user_name}&password={password}")
    assert response.status_code == 401


def test_get_raising_datetime():
    # positive
    user_name = "qwe"
    response = client.get(f"http://127.0.0.1:8000/user/get_raising_datetime/{user_name}")
    assert response.status_code == 200

    # wrong user_name
    user_name = "wrong_qwe"
    response = client.get(f"http://127.0.0.1:8000/user/get_raising_datetime/{user_name}")
    assert response.status_code == 400


def test_get_salary():
    # positive
    user_name, password = "qwe", "password"
    token = client.put("http://127.0.0.1:8000/user/create_token?user_name=qwe&password=password")
    response = client.get(
        f"http://127.0.0.1:8000/user/get_salary/{user_name}?password={password}&token={token.text[2:29]}")
    assert response.status_code == 200

    # wrong user_name
    user_name, password = "wrong_qwe", "password"
    response = client.get(
        f"http://127.0.0.1:8000/user/get_salary/{user_name}?password={password}&token={token.text[2:29]}")
    assert response.status_code == 400

    # wrong password
    user_name, password = "qwe", "wrong_password"
    response = client.get(
        f"http://127.0.0.1:8000/user/get_salary/{user_name}?password={password}&token={token.text[2:29]}")
    assert response.status_code == 401

    # wrong token_create_datetime
    time.sleep(15)
    user_name, password = "qwe", "password"
    response = client.get(
        f"http://127.0.0.1:8000/user/get_salary/{user_name}?password={password}&token={token.text[2:29]}")
    assert response.status_code == 401

    # wrong token
    token = "wrong_token"
    user_name, password = "qwe", "password"
    response = client.get(
        f"http://127.0.0.1:8000/user/get_salary/{user_name}?password={password}&token={token}")
    assert response.status_code == 401
