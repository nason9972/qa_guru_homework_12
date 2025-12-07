import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser
from utils import attach
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DEFAULT_BROWSER_VERSION = "100.0"


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='128.0'
    )
@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = Options()
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", browser_version)
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True
    })
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
        options=options
    )


    browser.config.driver = driver
    browser.config.timeout = 10
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.base_url = "https://demoqa.com"

    yield browser


    session_id = driver.session_id


    attach.add_screenshot(driver)
    attach.add_logs(driver)
    attach.add_html(driver)
    attach.add_video(driver)

    driver.quit()