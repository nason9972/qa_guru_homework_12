import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selene import browser

from utils import attach

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    options = Options()
    browser_version = os.getenv("BROWSER_VERSION")

    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", BROWSER_VERSION)
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True
    })

    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )


    browser.config.driver = driver
    browser.config.timeout = 10
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.base_url = "https://demoqa.com"

    yield


    session_id = driver.session_id


    attach.add_screenshot(driver)
    attach.add_logs(driver)
    attach.add_html(driver)
    attach.add_video(driver)

    driver.quit()