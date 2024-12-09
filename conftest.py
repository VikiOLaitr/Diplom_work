import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from Page.ApiPage import ApiPage
from Page.UiPage import SearchPage


@pytest.fixture(scope="session")
def browser():
    with allure.step("Открыть и настроить браузер"):
        """Инициализация браузера для сессии."""
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        browser.implicity_wait(4)
        browser.maximize_window()
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()


@pytest.fixture(scope="session")
def base_url():
    """Базовый URL для API тестов."""
    return "https://web-gate.chitai-gorod.ru/api"


@pytest.fixture(scope="session")
def api_client(base_url):
    """
    Фикстура для инициализации API-клиента.

    Эта фикстура создает экземпляр API-клиента, используя базовый URL и
    возвращает его для использования в тестах API.
    """
    # Определите базовые данные
    base_url = "https://web-gate.chitai-gorod.ru/api/v2/search/product"
    token = "ВАШ ТОКЕН"
    return ApiPage(base_url, token)


@pytest.fixture
def search_page(browser):
    page = SearchPage(browser)
    page.open("https://www.chitai-gorod.ru/")
    return page
