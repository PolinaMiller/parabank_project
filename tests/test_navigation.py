import pytest
from pages.navigation_page import NavigationService
from pages.login_page import LoginService


@pytest.fixture
def nav_service(driver, base_url):
    """
    Фикстура для выполнения входа в систему и инициализации сервисного объекта NavigationService.

    Шаги:
      1. Открыть базовый URL.
      2. Выполнить вход с использованием учетной записи "john" через LoginService.
      3. Вернуть объект NavigationService для дальнейшего использования в тестах.
    """
    driver.get(base_url)
    login_service = LoginService(driver)
    login_service.login("john", "demo")
    return NavigationService(driver)


def test_welcome_message(driver, base_url):
    """
    Тест проверяет, что после входа в систему на странице отображается приветственное сообщение "Welcome".
    """
    driver.get(base_url)
    login_service = LoginService(driver)
    login_service.login("john", "demo")
    assert "Welcome" in driver.page_source, "Приветственное сообщение не отображается."


@pytest.mark.parametrize("link_text, expected_text", [
    ("Open New Account", "Open New Account"),
    ("Accounts Overview", "Accounts Overview"),
    ("Transfer Funds", "Transfer Funds"),
    ("Bill Pay", "Bill Pay"),
    ("Find Transactions", "Find Transactions"),
    ("Update Contact Info", "Update Contact Info"),
    ("Request Loan", "Request Loan"),
    ("Log Out", "Customer Login")
])
def test_navigation_links(nav_service, driver, link_text, expected_text):
    """
    Тест переходит по каждой навигационной ссылке и проверяет, что после перехода
    на странице отображается ожидаемый текст.

    :param nav_service: Сервисный объект NavigationService, созданный фикстурой после входа в систему.
    :param link_text: Текст ссылки, по которой происходит навигация.
    :param expected_text: Ожидаемый текст на целевой странице после навигации.
    """
    nav_service.navigate_to(link_text)
    assert expected_text in driver.page_source, (
        f"Страница '{link_text}' не отображается как ожидалось. Ожидается наличие '{expected_text}'."
    )
