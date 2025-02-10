import pytest
import allure
import logging
from selenium.webdriver.common.by import By
from pages.login_page import LoginService
from pages.account_overview_page import AccountOverviewService

# Настройка логирования: вывод сообщений уровня INFO и выше.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.fixture
def account_overview_service(driver, base_url):
    """
    Фикстура для входа в систему и получения объекта AccountOverviewService.

    Шаги:
      1. Открыть базовый URL приложения.
      2. Выполнить вход с учетными данными ("john"/"demo") через LoginService.
      3. Вернуть объект AccountOverviewService для дальнейшего использования в тестах.
    """
    with allure.step("Открыть базовый URL приложения"):
        logger.info("Открытие базового URL: %s", base_url)
        driver.get(base_url)
    with allure.step("Выполнить вход с корректными учетными данными ('john'/'demo')"):
        logger.info("Выполняется вход с данными: john/demo")
        login_service = LoginService(driver)
        login_service.login("john", "demo")
    return AccountOverviewService(driver)


@allure.feature("Обзор аккаунтов")
@allure.story("Отображение страницы обзора аккаунтов")
def test_account_overview_displayed(account_overview_service):
    """
    Проверяет, что страница обзора аккаунтов отображается корректно.
    """
    with allure.step("Проверить отображение заголовка 'Accounts Overview'"):
        logger.info("Проверка отображения заголовка 'Accounts Overview'")
        assert account_overview_service.is_account_overview_displayed(), \
            "Account Overview is not displayed."


@allure.feature("Обзор аккаунтов")
@allure.story("Просмотр истории транзакций")
def test_view_transaction_history(account_overview_service, driver):
    """
    Проверяет, что после запроса истории транзакций для аккаунта с номером '13344'
    отображается страница с текстом 'Account Activity'.
    """
    with allure.step("Перейти к истории транзакций для аккаунта '13344'"):
        logger.info("Переход к истории транзакций для аккаунта '13344'")
        account_overview_service.view_transaction_history("13344")
    with allure.step("Проверить, что на странице отображается 'Account Activity'"):
        logger.info("Проверка, что страница содержит текст 'Account Activity'")
        assert "Account Activity" in driver.page_source, "Transaction history is not displayed."
