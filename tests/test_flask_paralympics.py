import requests


def test_server_is_up_and_running(live_server_flask, flask_port):
    """
    GIVEN a live server
    WHEN a GET HTTP request to the home page is made
    THEN the HTTP response should have a bytes string "paralympics" in the data and a status code of 200
    """
    url = f'http://127.0.0.1:{flask_port}/'
    response = requests.get(url)
    assert response.status_code == 200
    assert b"Paralympics" in response.content