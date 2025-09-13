import os
from email.policy import default
import pytest
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from demoqa.utils import attachments
from dotenv import load_dotenv


DEFAULT_BROWSER_VERSION = "128.0"

"""Настройка параметров для браузера"""
def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='128.0'
    )


"""Загрузка переменных сред из файла .env"""
@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


"""Получение информации о значении параметра browser из командной строки"""
@pytest.fixture(scope='session', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION


    """Настройка драйвера"""
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)


    """Создание переменных, cсылающихся на секретные данные"""
    selenoid_login = os.getenv('SELENOID_LOGIN')
    selenoid_password = os.getenv('SELENOID_PASSWORD')


    """Создание драйвера"""
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_password}@selenoid.autotests.cloud/wd/hub",
        options=options
    )


    """Передача драйвера в Selene"""
    browser.config.driver = driver


    """Настройка параметров браузера"""
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 20


    yield browser


    """Добавление аттачей после теста"""
    attachments.add_screenshot(browser)
    attachments.add_logs(browser)
    attachments.add_html(browser)
    attachments.add_video(browser)


    """Закрытие браузера"""
    browser.quit()