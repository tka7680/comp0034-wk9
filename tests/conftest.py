import os
import pytest
from selenium.webdriver import Chrome, ChromeOptions
import socket
import subprocess
import time

@pytest.fixture(scope="module")
def chrome_driver():
    """
    Fixture to create a Chrome driver. 
    
    On GitHub or other container it needs to run headless, i.e. the browser doesn't open and display on screen.
    Running locally you may want to display the tests in a large window to visibly check the behaviour. 
    """
    options = ChromeOptions()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    driver = Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def flask_port():
    """Gets a free port from the operating system."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="session")
def live_server_flask(flask_port):
    """Runs the Flask app as a live server for Selenium tests (Paralympic app)

    Renamed to live_server_flask to avoid issues with pytest-flask live_server
    """
    # Construct the command string to run flask with formatted dictionary
    command = """flask --app 'paralympics_flask:create_app(test_config={"TESTING": True, "WTF_CSRF_ENABLED": False})' run --port """ + str(
        flask_port)
    try:
        server = subprocess.Popen(command, shell=True)
        # Allow time for the app to start
        time.sleep(3)
        yield server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")