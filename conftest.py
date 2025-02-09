import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def explicit_wait(driver):
    """
    Фикстура, возвращающая функцию для явного ожидания видимости элемента.
    Использование в тесте:
        element = explicit_wait((By.ID, "some_id"), timeout=15)
    """
    def wait_for(locator, timeout=15):
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    return wait_for


@pytest.fixture(scope="session")
def base_url():
    return "https://parabank.parasoft.com/parabank"
